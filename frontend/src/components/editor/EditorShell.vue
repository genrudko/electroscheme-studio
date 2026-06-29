<template>
  <section class="editor-shell">
    <RibbonBar
      :active-mode="activeMode"
      @set-mode="setMode"
      @command="dispatchCommand"
    />

    <main class="editor-main">
      <CanvasViewport
        :active-mode="activeMode"
        :command="pendingCommand"
        @mode-change="setMode"
        @status-change="updateStatus"
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
    />
  </section>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import RibbonBar from './RibbonBar.vue'
import CanvasViewport from './CanvasViewport.vue'
import StatusBar from './StatusBar.vue'
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

const status = reactive<EditorStatus>({
  pointer: null,
  snapKind: null,
  snapLabel: '',
  selectedObjectName: '',
  message: 'Editor shell ready.',
})

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
    ? 'Pick virtual base point. It snaps to grid, slots and object centers.'
    : mode === 'paste_by_point'
      ? 'Pick paste point.'
      : `Mode switched to ${mode}.`
}

function dispatchCommand(command: EditorCommand): void {
  pendingCommand.value = command
}
</script>

<style scoped>
.editor-shell {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  background: #e5edf7;
  color: #0f172a;
}

.editor-main {
  min-height: 0;
  overflow: hidden;
}
</style>