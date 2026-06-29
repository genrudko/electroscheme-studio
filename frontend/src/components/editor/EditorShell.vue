<template>
  <section class="editor-shell" @keydown.capture="onShellKeydown" tabindex="0">
    <RibbonBar :active-mode="activeMode" :settings="canvasSettings" @set-mode="setMode" @command="dispatchCommand" @settings-change="updateCanvasSettings" />
    <main class="editor-main">
      <ShapePalette @insert-shape="dispatchCommand" />
      <CanvasViewport :active-mode="activeMode" :command="pendingCommand" :settings="canvasSettings" @mode-change="setMode" @status-change="updateStatus" @settings-change="updateCanvasSettings" @command-handled="pendingCommand = null" />
    </main>
    <footer class="status-bar">Режим: {{ activeMode }} · {{ status.message }} · {{ status.selectedObjectName }}</footer>
  </section>
</template>
<script setup lang="ts">
import { reactive, ref } from 'vue'
import RibbonBar from './RibbonBar.vue'
import ShapePalette from './ShapePalette.vue'
import CanvasViewport from './CanvasViewport.vue'
import { defaultCanvasSettings, normalizeCanvasSettings, type CanvasSettings } from '../../lib/editor/canvasSettings'
import type { EditorCommand, EditorInteractionMode } from '../../lib/editor/interactionModes'
import type { Point, SnapKind } from '../../lib/editor/snapService'
const activeMode = ref<EditorInteractionMode>('select')
const pendingCommand = ref<EditorCommand | null>(null)
const canvasSettings = reactive<CanvasSettings>({ ...defaultCanvasSettings })
const status = reactive<{ pointer: Point | null; snapKind: SnapKind | null; snapLabel: string; selectedObjectName: string; message: string }>({ pointer: null, snapKind: null, snapLabel: '', selectedObjectName: '', message: 'Редактор готов.' })
function updateCanvasSettings(next: CanvasSettings): void { Object.assign(canvasSettings, normalizeCanvasSettings(next)) }
function updateStatus(next: typeof status): void { Object.assign(status, next) }
function setMode(mode: EditorInteractionMode): void { activeMode.value = mode }
function dispatchCommand(command: EditorCommand): void { pendingCommand.value = command }
function onShellKeydown(event: KeyboardEvent): void {
  const target = event.target as HTMLElement | null
  const tag = target?.tagName?.toLowerCase()
  if (tag === 'input' || tag === 'textarea' || tag === 'select' || target?.isContentEditable) return
  const key = event.key.toLowerCase()
  if (event.ctrlKey && key === 'c') { event.preventDefault(); dispatchCommand('copy') }
  else if (event.ctrlKey && key === 'v') { event.preventDefault(); dispatchCommand('paste') }
  else if (event.key === 'Delete') { event.preventDefault(); dispatchCommand('delete') }
  else if (event.key === 'Escape') { event.preventDefault(); setMode('select') }
}
</script>
<style scoped>
.editor-shell{display:grid;grid-template-rows:112px 1fr 30px;height:100vh;min-height:0;background:#e5edf7;color:#0f172a;overflow:hidden;outline:none}.editor-main{display:grid;grid-template-columns:250px 1fr;min-height:0;overflow:hidden}.status-bar{display:flex;align-items:center;padding:0 10px;border-top:1px solid #cbd5e1;background:#f8fafc;color:#475569;font-size:12px}
</style>
