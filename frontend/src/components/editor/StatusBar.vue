<template>
  <footer class="editor-status-bar">
    <span><strong>Режим:</strong> {{ modeLabel }}</span>
    <span><strong>Курсор:</strong> {{ pointerText }}</span>
    <span><strong>Привязка:</strong> {{ snapText }}</span>
    <span><strong>Выбор:</strong> {{ selectionText }}</span>
    <span class="status-message">{{ message }}</span>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
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
}>()

const modeLabel = computed(() => interactionModeLabels[props.mode])
const pointerText = computed(() => props.pointer ? `X=${props.pointer.x.toFixed(1)} Y=${props.pointer.y.toFixed(1)}` : '—')
const snapText = computed(() => props.snapKind ? `${props.snapKind}: ${props.snapLabel}` : '—')
const selectionText = computed(() => props.selectedObjectName || 'нет')
</script>

<style scoped>
.editor-status-bar {
  display: flex;
  align-items: center;
  gap: 18px;
  min-height: 30px;
  padding: 6px 12px;
  border-top: 1px solid #dbe3ef;
  background: #f8fafc;
  color: #334155;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
}

.editor-status-bar span {
  flex: 0 0 auto;
}

.status-message {
  flex: 1 1 auto;
  min-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>