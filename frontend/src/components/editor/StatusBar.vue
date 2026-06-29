<template>
  <footer class="editor-status-bar">
    <div class="status-left">
      <span><strong>Режим:</strong> {{ modeLabel }}</span>
      <span><strong>Курсор:</strong> {{ pointerText }}</span>
      <span><strong>Привязка:</strong> {{ snapText }}</span>
      <span><strong>Выбор:</strong> {{ selectionText }}</span>
      <span class="status-message">{{ message }}</span>
    </div>

    <div class="zoom-bar">
      <button type="button" @click="setZoom(1)">100%</button>
      <input
        :value="settings.zoom"
        type="range"
        min="0.25"
        max="4"
        step="0.05"
        title="Масштаб канваса"
        @input="onZoomInput"
      />
      <span>{{ Math.round(settings.zoom * 100) }}%</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { CanvasSettings } from '../../lib/editor/canvasSettings'
import { normalizeCanvasSettings } from '../../lib/editor/canvasSettings'
import type { EditorInteractionMode } from '../../lib/editor/interactionModes'
import { interactionModeLabels } from '../../lib/editor/interactionModes'
import type { Point, SnapKind } from '../../lib/editor/snapService'

const props = defineProps<{
  mode: EditorInteractionMode
  pointer: Point | null
  snapKind: SnapKind | null
  snapLabel: string
  selectedObjectName: string
  message: string
  settings: CanvasSettings
}>()

const emit = defineEmits<{
  settingsChange: [settings: CanvasSettings]
}>()

const modeLabel = computed(() => interactionModeLabels[props.mode])
const pointerText = computed(() => props.pointer ? `X=${props.pointer.x.toFixed(1)} Y=${props.pointer.y.toFixed(1)}` : '—')
const snapText = computed(() => props.snapKind ? `${props.snapKind}: ${props.snapLabel}` : '—')
const selectionText = computed(() => props.selectedObjectName || 'нет')

function setZoom(zoom: number): void {
  emit('settingsChange', normalizeCanvasSettings({ ...props.settings, zoom }))
}

function onZoomInput(event: Event): void {
  const zoom = Number((event.target as HTMLInputElement).value)
  if (!Number.isFinite(zoom)) return
  setZoom(zoom)
}
</script>

<style scoped>
.editor-status-bar {
  display: grid;
  grid-template-columns: 1fr 270px;
  align-items: center;
  gap: 12px;
  min-height: 34px;
  padding: 5px 10px;
  border-top: 1px solid #dbe3ef;
  background: #f8fafc;
  color: #334155;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
}

.status-left {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
  overflow: hidden;
}

.status-left span {
  flex: 0 0 auto;
}

.status-message {
  flex: 1 1 auto !important;
  min-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.zoom-bar {
  display: grid;
  grid-template-columns: 52px 1fr 46px;
  align-items: center;
  gap: 8px;
}

.zoom-bar button {
  border: 1px solid #bfdbfe;
  border-radius: 7px;
  background: white;
  color: #1e3a8a;
  cursor: pointer;
  font-size: 12px;
  font-weight: 800;
  padding: 4px 6px;
}

.zoom-bar span {
  text-align: right;
  color: #475569;
  font-weight: 800;
}
</style>