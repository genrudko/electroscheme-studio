<template>
  <section class="editor-shell" :style="{ '--ess-ui-scale': String(canvasSettings.uiScale) }" @keydown.capture="onShellKeydown" tabindex="0">
    <RibbonBar
      :active-mode="activeMode"
      :settings="canvasSettings"
      @set-mode="setMode"
      @command="dispatchCommand"
      @settings-change="updateCanvasSettings"
    />

    <main class="editor-main">
      <ShapePalette @insert-shape="dispatchCommand" />

      <CanvasViewport
        :active-mode="activeMode"
        :command="pendingCommand"
        :settings="canvasSettings"
        @mode-change="setMode"
        @status-change="updateStatus"
        @settings-change="updateCanvasSettings"
        @command-handled="pendingCommand = null"
      />
    </main>

    <StatusBar
      :mode="activeMode"
      :pointer="status.pointer"
      :snap-kind="status.snapKind"
      :snap-label="status.snapLabel"
      :selected-object-name="status.selectedObjectName"
      :message="status.message"
      :settings="canvasSettings"
      @settings-change="updateCanvasSettings"
    />
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import RibbonBar from './RibbonBar.vue'
import ShapePalette from './ShapePalette.vue'
import CanvasViewport from './CanvasViewport.vue'
import StatusBar from './StatusBar.vue'
import { defaultCanvasSettings, normalizeCanvasSettings, type CanvasSettings } from '../../lib/editor/canvasSettings'
import { EditorCommandStack, type CommandStackState } from '../../lib/editor/commandStack'
import { createEmptyEditorDocument } from '../../lib/editor/editorDocument'
import type { EditorCommand, EditorInteractionMode } from '../../lib/editor/interactionModes'
import { shortcutSummary } from '../../lib/editor/shortcutRegistry'
import type { Point, SnapKind } from '../../lib/editor/snapService'

type EditorStatus = {
  pointer: Point | null
  snapKind: SnapKind | null
  snapLabel: string
  selectedObjectName: string
  message: string
}

const activeMode = ref<EditorInteractionMode>('select')
const pendingCommand = ref<EditorCommand | null>(null)
const commandStack = new EditorCommandStack()
const shortcutHelpText = shortcutSummary()
const commandStackState = reactive<CommandStackState>(commandStack.state())
const editorDocument = createEmptyEditorDocument(defaultCanvasSettings)

const canvasSettings = reactive<CanvasSettings>({ ...defaultCanvasSettings })

const status = reactive<EditorStatus>({
  pointer: null,
  snapKind: null,
  snapLabel: '',
  selectedObjectName: '',
  message: 'Редактор готов.',
})

onMounted(() => {
  status.message = `Документ: ${editorDocument.title}. Слои и палитра фигур подключены. Горячие клавиши: .`
})

function syncStackState(next: CommandStackState): void {
  commandStackState.undoDepth = next.undoDepth
  commandStackState.redoDepth = next.redoDepth
  commandStackState.canUndo = next.canUndo
  commandStackState.canRedo = next.canRedo
  commandStackState.lastCommandLabel = next.lastCommandLabel
}

function updateCanvasSettings(next: CanvasSettings): void {
  const normalized = normalizeCanvasSettings(next)
  canvasSettings.zoom = normalized.zoom
  canvasSettings.gridVisible = normalized.gridVisible
  canvasSettings.gridStep = normalized.gridStep
  canvasSettings.snapEnabled = normalized.snapEnabled
  canvasSettings.snapTolerance = normalized.snapTolerance
  canvasSettings.snapGrid = normalized.snapGrid
  canvasSettings.snapSlots = normalized.snapSlots
  canvasSettings.snapObjects = normalized.snapObjects
  canvasSettings.snapGuides = normalized.snapGuides
  canvasSettings.guidesVisible = normalized.guidesVisible
  canvasSettings.rulersVisible = normalized.rulersVisible
  canvasSettings.originVisible = normalized.originVisible
  canvasSettings.pageVisible = normalized.pageVisible
  canvasSettings.pageFormat = normalized.pageFormat
  canvasSettings.pageOrientation = normalized.pageOrientation
  canvasSettings.displayProfileId = normalized.displayProfileId
  canvasSettings.uiScale = normalized.uiScale
  canvasSettings.ribbonCollapsed = normalized.ribbonCollapsed
  editorDocument.settings = { ...normalized }
}

function updateStatus(next: EditorStatus): void {
  status.pointer = next.pointer
  status.snapKind = next.snapKind
  status.snapLabel = next.snapLabel
  status.selectedObjectName = next.selectedObjectName
  status.message = next.message
}

function setMode(mode: EditorInteractionMode): void {
  activeMode.value = mode
  status.message = mode === 'copy_by_reference'
    ? 'Укажите виртуальную базовую точку. Она привязывается к сетке, ячейкам, объектам и направляющим.'
    : mode === 'paste_by_point'
      ? 'Укажите точку вставки.'
      : `Режим: ${mode}.`
}

function dispatchCommand(command: EditorCommand): void {
  if (command === 'undo') {
    syncStackState(commandStack.undo())
    status.message = 'Undo: фундамент command stack подключён; операции CanvasViewport будут подключаться следующим этапом.'
    return
  }

  if (command === 'redo') {
    syncStackState(commandStack.redo())
    status.message = 'Redo: фундамент command stack подключён; операции CanvasViewport будут подключаться следующим этапом.'
    return
  }

  if (command === 'cut') {
    pendingCommand.value = 'copy'
    setTimeout(() => { pendingCommand.value = 'delete' }, 0)
    return
  }

  pendingCommand.value = command
}

function onShellKeydown(event: KeyboardEvent): void {
  const target = event.target as HTMLElement | null
  const tagName = target?.tagName?.toLowerCase()
  if (tagName === 'input' || tagName === 'textarea' || tagName === 'select' || target?.isContentEditable) return

  const key = event.key.toLowerCase()

  if (event.ctrlKey && key === 'z') {
    event.preventDefault()
    dispatchCommand('undo')
  } else if (event.ctrlKey && (key === 'y' || (event.shiftKey && key === 'z'))) {
    event.preventDefault()
    dispatchCommand('redo')
  } else if (event.ctrlKey && key === 'c') {
    event.preventDefault()
    dispatchCommand('copy')
  } else if (event.ctrlKey && key === 'x') {
    event.preventDefault()
    dispatchCommand('cut')
  } else if (event.ctrlKey && key === 'v') {
    event.preventDefault()
    dispatchCommand('paste')
  } else if (event.key === 'Delete') {
    event.preventDefault()
    dispatchCommand('delete')
  } else if (event.key === 'Escape') {
    event.preventDefault()
    setMode('select')
  }
}
</script>

<style scoped>
.editor-shell {
  display: grid;
  grid-template-rows: 112px 1fr 34px;
  height: 100vh;
  min-height: 0;
  background: #e5edf7;
  color: #0f172a;
  overflow: hidden;
  outline: none;
}

.editor-main {
  display: grid;
  grid-template-columns: 250px 1fr;
  min-height: 0;
  overflow: hidden;
}
</style>