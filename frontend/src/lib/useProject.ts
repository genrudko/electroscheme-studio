import { ref, computed } from 'vue'
import type { Connection, Project, SchemeSymbol, SymbolLibrary, SymbolDefinition, Terminal, Waypoint } from './types'
import {
  fetchProject,
  fetchSymbolLibrary,
  addSymbol,
  removeSymbol,
  addConnection,
  updateConnection,
  removeConnection,
} from './api'

const FALLBACK_PROJECT: Project = {
  version: '0.1',
  project: { name: 'Offline Demo', code: 'offline-demo' },
  sheets: [
    { id: 'sheet_1', name: 'Demo Sheet', format: 'A3', orientation: 'landscape', width_mm: 420, height_mm: 297 }
  ],
  symbols: [
    {
      id: 'busbar_1', type: 'busbar', label: '1C',
      x: 60, y: 60, width: 260, height: 0,
      terminals: [{ id: 't1', x: 120, y: 60 }, { id: 't2', x: 220, y: 60 }]
    },
    {
      id: 'q1', type: 'circuit_breaker_contact', label: 'Q1',
      x: 120, y: 110, width: 53, rotation: 0,
      terminals: [{ id: 'a', x: 120, y: 80 }, { id: 'b', x: 120, y: 145 }],
      current_state: 'closed',
      properties: { name: 'Автоматический выключатель', voltage_kv: 10 }
    },
    {
      id: 'fu1', type: 'fuse', label: 'FU1',
      x: 200, y: 110, width: 53, rotation: 0,
      terminals: [{ id: 'a', x: 200, y: 80 }, { id: 'b', x: 200, y: 145 }],
      current_state: 'intact',
      properties: { name: 'Предохранитель', rating_a: 16 }
    },
    {
      id: 'km1', type: 'contactor', label: 'KM1',
      x: 280, y: 110, width: 53, rotation: 0,
      terminals: [{ id: 'a', x: 280, y: 80 }, { id: 'b', x: 280, y: 145 }],
      current_state: 'closed',
      properties: { name: 'Контактор', coil_voltage: 220 }
    }
  ],
  connections: [{ id: 'conn_1', from: 'busbar_1.t1', to: 'q1.a' }]
}

const project = ref<Project>(FALLBACK_PROJECT)
const selectedId = ref<string>('q1')
const selectedConnectionId = ref<string>('')
const connectionMode = ref<'select' | 'wire'>('select')
const loading = ref(false)
const error = ref<string | null>(null)

const symbolLibrary = ref<SymbolLibrary | null>(null)
const libraryLoading = ref(false)

const libraryByCategory = computed(() => {
  if (!symbolLibrary.value) return []
  const cats = symbolLibrary.value.categories
  const syms = symbolLibrary.value.symbols
  return cats.map((cat) => ({
    ...cat,
    symbols: syms.filter((s) => s.category === cat.id),
  }))
})

function nextSymbolId(type: string, existing: SchemeSymbol[]): string {
  let idx = 1
  const ids = new Set(existing.map((s) => s.id))
  while (ids.has(`${type}_${idx}`)) idx++
  return `${type}_${idx}`
}

function nextConnectionId(existing: Connection[]): string {
  let idx = existing.length + 1
  const ids = new Set(existing.map((c) => c.id))
  while (ids.has(`conn_${idx}`)) idx++
  return `conn_${idx}`
}

function buildTerminalsFor(def: SymbolDefinition, x: number, y: number, width: number): Terminal[] {
  if (!def.terminals || def.terminals.length === 0) return []
  const vb = def.viewBox.trim().split(/\s+/).map(Number)
  const vbWidth = vb[2] || width
  const scale = vbWidth > 0 ? width / vbWidth : 1
  return def.terminals.map((t) => ({
    id: t.id,
    x: Math.round(x + t.rx * width),
    y: Math.round(y + t.ry * (vb[3] || def.default_height) * scale),
  }))
}

export function useProject() {
  const symbols = computed(() => project.value.symbols)
  const connections = computed(() => project.value.connections)
  const sheets = computed(() => project.value.sheets)
  const currentSheet = computed(() => project.value.sheets[0] ?? null)

  const selectedSymbol = computed<SchemeSymbol | null>(() =>
    project.value.symbols.find((s) => s.id === selectedId.value) ?? null
  )

  function selectSymbol(id: string) {
    selectedId.value = id
    selectedConnectionId.value = ''
  }

  function selectConnection(id: string) {
    selectedConnectionId.value = id
    selectedId.value = ''
  }

  function setConnectionMode(mode: 'select' | 'wire') {
    connectionMode.value = mode
    if (mode === 'select') {
      selectedConnectionId.value = ''
    }
  }

  function toggleState(symbolId: string, newState: string) {
    const sym = project.value.symbols.find((s) => s.id === symbolId)
    if (sym) {
      sym.current_state = newState
    }
  }

  /** Create a new connection between two terminal refs. Returns the new id. */
  async function createConnection(
    fromRef: string,
    toRef: string,
    options?: { points?: Waypoint[]; route_mode?: Connection['route_mode']; kind?: Connection['kind'] },
  ): Promise<string | null> {
    if (!fromRef || !toRef || fromRef === toRef) return null
    const conn: Connection = {
      id: nextConnectionId(project.value.connections),
      from: fromRef,
      to: toRef,
      points: options?.points ?? [],
      route_mode: options?.route_mode ?? 'ortho',
      kind: options?.kind ?? 'wire',
    }
    project.value.connections.push(conn)
    try {
      await addConnection(conn)
    } catch (e: unknown) {
      // rollback local state on API failure so we don't drift
      project.value.connections = project.value.connections.filter((c) => c.id !== conn.id)
      error.value = e instanceof Error ? e.message : String(e)
      return null
    }
    return conn.id
  }

  /** Insert a waypoint at the given index on a connection. */
  async function insertWaypoint(connId: string, point: Waypoint, index?: number) {
    const c = project.value.connections.find((cc) => cc.id === connId)
    if (!c) return
    const pts: Waypoint[] = [...(c.points ?? [])]
    const at = index === undefined
      ? pts.length
      : Math.max(0, Math.min(index, pts.length))
    pts.splice(at, 0, { x: point.x, y: point.y })
    c.points = pts
    c.route_mode = 'manual'
    try {
      await updateConnection({ ...c })
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e)
    }
  }

  /** Remove the i-th waypoint from a connection (no-op if index out of range). */
  async function removeWaypoint(connId: string, index: number) {
    const c = project.value.connections.find((cc) => cc.id === connId)
    if (!c) return
    const pts: Waypoint[] = [...(c.points ?? [])]
    if (index < 0 || index >= pts.length) return
    pts.splice(index, 1)
    c.points = pts
    if (pts.length === 0) c.route_mode = 'ortho'
    try {
      await updateConnection({ ...c })
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e)
    }
  }

  async function deleteConnectionById(connId: string) {
    const before = project.value.connections.length
    project.value.connections = project.value.connections.filter((c) => c.id !== connId)
    if (project.value.connections.length === before) return
    if (selectedConnectionId.value === connId) selectedConnectionId.value = ''
    try {
      await removeConnection(connId)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e)
    }
  }

  async function loadFromApi() {
    loading.value = true
    error.value = null
    try {
      project.value = await fetchProject()
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e)
    } finally {
      loading.value = false
    }
  }

  async function loadSymbolLibrary() {
    libraryLoading.value = true
    try {
      symbolLibrary.value = await fetchSymbolLibrary()
    } catch {
      // keep null
    } finally {
      libraryLoading.value = false
    }
  }

  async function addSymbolFromLibrary(def: SymbolDefinition, x: number, y: number) {
    const id = nextSymbolId(def.type, project.value.symbols)
    const width = def.default_width
    const sym: SchemeSymbol = {
      id,
      type: def.type,
      label: id.toUpperCase(),
      x,
      y,
      width,
      rotation: 0,
      terminals: buildTerminalsFor(def, x, y, width),
      current_state: def.default_state ?? 'normal',
      properties: { ...def.default_properties },
    }
    project.value.symbols.push(sym)
    selectedId.value = id
    try {
      await addSymbol(sym)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e)
    }
  }

  async function removeSymbolById(symbolId: string) {
    project.value.symbols = project.value.symbols.filter((s) => s.id !== symbolId)
    project.value.connections = project.value.connections.filter(
      (c) => !c.from.startsWith(symbolId + '.') && !c.to.startsWith(symbolId + '.')
    )
    if (selectedId.value === symbolId) selectedId.value = ''
    try {
      await removeSymbol(symbolId)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e)
    }
  }

  return {
    project,
    symbols,
    connections,
    sheets,
    currentSheet,
    selectedId,
    selectedSymbol,
    selectedConnectionId,
    connectionMode,
    selectSymbol,
    selectConnection,
    setConnectionMode,
    toggleState,
    loadFromApi,
    loadSymbolLibrary,
    addSymbolFromLibrary,
    removeSymbolById,
    createConnection,
    deleteConnectionById,
    insertWaypoint,
    removeWaypoint,
    symbolLibrary,
    libraryByCategory,
    libraryLoading,
    loading,
    error,
  }
}
