import { ref, computed } from 'vue'
import type { Project, SchemeSymbol } from './types'
import { fetchProject } from './api'

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
      id: 'q1', type: 'circuit_breaker', label: 'Q1',
      x: 120, y: 110, rotation: 90,
      terminals: [{ id: 'a', x: 120, y: 80 }, { id: 'b', x: 120, y: 145 }],
      properties: { name: 'Demo circuit breaker', voltage_kv: 10, state: 'closed' }
    }
  ],
  connections: [{ id: 'conn_1', from: 'busbar_1.t1', to: 'q1.a' }]
}

const project = ref<Project>(FALLBACK_PROJECT)
const selectedId = ref<string>('q1')
const loading = ref(false)
const error = ref<string | null>(null)

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
  }

  async function loadFromApi() {
    loading.value = true
    error.value = null
    try {
      project.value = await fetchProject()
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e)
      // keep fallback data
    } finally {
      loading.value = false
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
    selectSymbol,
    loadFromApi,
    loading,
    error,
  }
}
