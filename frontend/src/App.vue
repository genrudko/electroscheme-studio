<script setup lang="ts">
import ImportedSymbolReviewPanel from './components/ImportedSymbolReviewPanel.vue'
import { onMounted, ref, computed } from 'vue'
import { useProject } from './lib/useProject'
import SchemeCanvas from './components/SchemeCanvas.vue'
import PropertiesPanel from './components/PropertiesPanel.vue'
import SymbolEditor from './components/SymbolEditor.vue'
import type { Waypoint } from './lib/types'
import { snapToBusbar, extractBusbars } from './lib/routing'

const {
  symbols,
  connections,
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
  symbolLibrary,
  libraryByCategory,
  addSymbolFromLibrary,
  removeSymbolById,
  createConnection,
  deleteConnectionById,
  insertWaypoint,
  loading,
  error,
} = useProject()

// pendingWireFrom and pendingWirePoints are exposed from useProject only as state;
// wire-drawing logic is handled here in the App.
const localPendingFrom = ref<string>('')
const localPendingPoints = ref<Waypoint[]>([])
const SNAP_TOLERANCE = 4 // mm
const editorMode = ref<'scheme' | 'symbol-editor'>('scheme')
const symbolEditorRef = ref<InstanceType<typeof SymbolEditor> | null>(null)

onMounted(() => {
  loadFromApi()
  loadSymbolLibrary()
})

function handleDropSymbol(symbolType: string, x: number, y: number) {
  if (!symbolLibrary.value) return
  const def = symbolLibrary.value.symbols.find((s) => s.type === symbolType)
  if (!def) return
  addSymbolFromLibrary(def, x, y)
}

function startWire() {
  setConnectionMode('wire')
  localPendingFrom.value = ''
  localPendingPoints.value = []
}

function stopWire() {
  setConnectionMode('select')
  localPendingFrom.value = ''
  localPendingPoints.value = []
}

// Apply snap-to-busbar at the given coordinate, if the point lies near a busbar.
function snapPoint(x: number, y: number) {
  const bbs = extractBusbars(
    symbols.value.map((s) => ({ id: s.id, type: s.type, x: s.x, y: s.y, width: s.width })),
  )
  const { point, busbarId } = snapToBusbar({ x, y }, bbs, SNAP_TOLERANCE)
  return { point, busbarId }
}

// Wire-drawing state machine:
//   1) terminal click with no pending start → set pending start
//   2) terminal click with pending start → finish connection (with snap)
//   3) canvas click with pending start + start on busbar → insert waypoint with snap
//   4) canvas click with pending start, no busbar → cancel (or finish at point?)
//   5) Esc → cancel
async function handleWireTerminalClick(ref: string, x: number, y: number) {
  const snapped = snapPoint(x, y)
  if (!localPendingFrom.value) {
    // start
    localPendingFrom.value = ref
    localPendingPoints.value = snapped.busbarId
      ? [{ x: snapped.point.x, y: snapped.point.y }]
      : []
    return
  }
  // finish: from → waypoints → to
  if (ref === localPendingFrom.value) {
    // clicked the same terminal → cancel
    stopWire()
    return
  }
  const newId = await createConnection(localPendingFrom.value, ref, {
    points: [...localPendingPoints.value, ...(snapped.busbarId
      ? [{ x: snapped.point.x, y: snapped.point.y }]
      : [])],
    route_mode: localPendingPoints.value.length > 0 ? 'manual' : 'ortho',
    kind: 'wire',
  })
  if (newId) {
    selectConnection(newId)
  }
  localPendingFrom.value = ''
  localPendingPoints.value = []
  setConnectionMode('select')
}

async function handleWireCanvasClick(x: number, y: number) {
  if (connectionMode.value !== 'wire' || !localPendingFrom.value) return
  const snapped = snapPoint(x, y)
  if (snapped.busbarId) {
    // add a busbar-snapped waypoint
    localPendingPoints.value = [
      ...localPendingPoints.value,
      { x: snapped.point.x, y: snapped.point.y },
    ]
  }
  // ignore plain canvas clicks in pure-wire mode (terminal must terminate the wire)
}

function handleWireCancel() {
  localPendingFrom.value = ''
  localPendingPoints.value = []
  setConnectionMode('select')
}

const wireStatus = computed(() => {
  if (connectionMode.value !== 'wire') return ''
  if (!localPendingFrom.value) return 'Режим «Провод»: кликните по терминалу, чтобы начать линию.'
  return `Режим «Провод»: от терминала ${localPendingFrom.value}. Кликните по другому терминалу для завершения.`
})

function onSymbolEditorSave(payload: { svg: string; viewBox: string }) {
  console.log('[SymbolEditor] save', payload)
}
</script>

<template>
  <main class="app-shell">
    <aside class="sidebar sidebar-left">
      <div class="brand">
        <div class="brand-mark">ES</div>
        <div>
          <h1>ElectroScheme Studio</h1>
          <p>ГОСТ-oriented WebUI prototype</p>
        </div>
        <button
          class="mode-toggle"
          :class="{ active: editorMode === 'symbol-editor' }"
          @click="editorMode = editorMode === 'scheme' ? 'symbol-editor' : 'scheme'"
          title="Переключить: Схема / Редактор символов"
        >{{ editorMode === 'scheme' ? '✎ Символы' : '⚡ Схема' }}</button>
      </div>

      <section class="panel">
        <h2>Библиотека ГОСТ</h2>
        <p class="hint">Перетащите символ на схему</p>
        <div v-for="cat in libraryByCategory" :key="cat.id" class="lib-category">
          <div class="lib-category-title">{{ cat.name }}</div>
          <div
            v-for="sym in cat.symbols"
            :key="sym.id"
            class="tool-button lib-symbol lib-draggable"
            draggable="true"
            :title="sym.gost + ', ' + sym.gost_ref"
            @dragstart="(e: DragEvent) => {
              e.dataTransfer?.setData('application/x-electroscheme-symbol', sym.type)
              e.dataTransfer!.effectAllowed = 'copy'
            }"
          >
            <svg :viewBox="sym.viewBox" class="lib-icon" v-html="sym.svg"></svg>
            <span>{{ sym.name }}</span>
          </div>
        </div>
        <div v-if="!libraryByCategory.length" class="toolbar-muted">Загрузка…</div>
      </section>

      <section class="panel">
        <h2>Схема</h2>
        <div
          v-for="sym in symbols"
          :key="sym.id"
          class="tree-item"
          :class="{ active: selectedId === sym.id }"
          @click="selectSymbol(sym.id)"
        >
          {{ sym.label }} ({{ sym.type }})
        </div>
        <div v-if="connections.length" class="lib-category-title" style="margin-top:14px">Соединения</div>
        <div
          v-for="conn in connections"
          :key="conn.id"
          class="tree-item"
          :class="{ active: selectedConnectionId === conn.id }"
          @click="selectConnection(conn.id)"
        >
          {{ conn.id }}: {{ conn.from }} → {{ conn.to }}
          <small v-if="conn.points && conn.points.length"> ({{ conn.points.length }} wp)</small>
        </div>
      </section>
    </aside>

    <!-- SCHEME EDITOR MODE -->
    <template v-if="editorMode === 'scheme'">
      <section class="workspace">
        <header class="toolbar">
          <span>SVG canvas</span>
          <button
            type="button"
            class="toolbar-button"
            :class="{ active: connectionMode === 'wire' }"
            :disabled="connectionMode === 'wire' && !localPendingFrom"
            @click="connectionMode === 'wire' ? handleWireCancel() : startWire()"
          >{{ connectionMode === 'wire' ? 'Отменить провод' : 'Провод' }}</button>
          <span v-if="loading" class="toolbar-muted">Загрузка…</span>
          <span v-else-if="error" class="toolbar-muted toolbar-error">{{ error }}</span>
          <span v-else class="toolbar-muted">{{ symbols.length }} элементов, {{ connections.length }} соединений</span>
          <span v-if="wireStatus" class="wire-status" :class="{ active: !!localPendingFrom }">{{ wireStatus }}</span>
        </header>

        <SchemeCanvas
          :symbols="symbols"
          :connections="connections"
          :selected-id="selectedId"
          :selected-connection-id="selectedConnectionId"
          :library="symbolLibrary"
          :connection-mode="connectionMode"
          :pending-wire-from="localPendingFrom"
          :pending-wire-points="localPendingPoints"
          @select="selectSymbol"
          @select-connection="selectConnection"
          @state-change="toggleState"
          @drop-symbol="handleDropSymbol"
          @delete-symbol="removeSymbolById"
          @delete-connection="deleteConnectionById"
          @wire-terminal-click="handleWireTerminalClick"
          @wire-canvas-click="handleWireCanvasClick"
          @wire-cancel="handleWireCancel"
          @insert-waypoint="insertWaypoint"
        />
      </section>

      <aside class="sidebar sidebar-right">
        <PropertiesPanel
          :symbol="selectedSymbol"
          :library="symbolLibrary"
          @state-change="toggleState"
          @delete="removeSymbolById"
        />

        <section class="panel">
          <h2>Проверки</h2>
          <div class="check ok">SVG-рендер: OK</div>
          <div class="check ok">Выбор элемента: OK</div>
          <div class="check ok">Загрузка с API: OK</div>
          <div class="check ok">Drag &amp; Drop: OK</div>
          <div class="check ok">Модель соединений: орто + узлы + байпас</div>
        </section>
      </aside>
      <ImportedSymbolReviewPanel />
</template>

    <!-- SYMBOL EDITOR MODE -->
    <section v-else class="symbol-editor-area">
      <SymbolEditor
        ref="symbolEditorRef"
        @save="onSymbolEditorSave"
        @close="editorMode = 'scheme'"
      />
    </section>
  </main>
  <ImportedSymbolReviewPanel />
</template>
