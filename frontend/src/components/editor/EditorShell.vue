<template>
  <section class="editor-shell">
    <RibbonBar
      :active-mode="activeMode"
      :settings="canvasSettings"
      @set-mode="setMode"
      @command="dispatchCommand"
      @settings-change="updateCanvasSettings"
    />

    <main class="editor-main">
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
import { reactive, ref } from 'vue'
import RibbonBar from './RibbonBar.vue'
import CanvasViewport from './CanvasViewport.vue'
import StatusBar from './StatusBar.vue'
import { defaultCanvasSettings, normalizeCanvasSettings, type CanvasSettings } from '../../lib/editor/canvasSettings'
import type { EditorCommand, EditorInteractionMode } from '../../lib/editor/interactionModes'
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

const canvasSettings = reactive<CanvasSettings>({ ...defaultCanvasSettings })

const status = reactive<EditorStatus>({
  pointer: null,
  snapKind: null,
  snapLabel: '',
  selectedObjectName: '',
  message: 'Редактор готов.',
})

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
  pendingCommand.value = command
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
}

.editor-main {
  min-height: 0;
  overflow: hidden;
}
</style>