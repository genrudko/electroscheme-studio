<template>
  <div class="canvas-workspace" @pointerdown="hideContextMenu">
    <svg
      ref="svgRef"
      class="editor-canvas"
      viewBox="0 0 900 520"
      @pointermove="onPointerMove"
      @pointerdown="onCanvasPointerDown"
      @contextmenu.prevent.stop="onContextMenu"
    >
      <defs>
        <pattern id="editor-grid" width="12" height="12" patternUnits="userSpaceOnUse">
          <path d="M 12 0 L 0 0 0 12" fill="none" stroke="#e5e7eb" stroke-width="0.6" />
        </pattern>
        <pattern id="editor-grid-major" width="60" height="60" patternUnits="userSpaceOnUse">
          <rect width="60" height="60" fill="url(#editor-grid)" />
          <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#cbd5e1" stroke-width="0.9" />
        </pattern>
      </defs>

      <rect x="0" y="0" width="900" height="520" fill="url(#editor-grid-major)" />

      <g class="object-layer">
        <rect class="busbar" x="96" y="180" width="360" height="20" rx="2" />
        <circle
          v-for="slot in baySlots"
          :key="slot.id"
          class="bay-slot"
          :cx="slot.x"
          :cy="slot.y"
          r="5"
          :data-slot-id="slot.id"
        />
        <text
          v-for="object in textObjects"
          :key="object.id"
          class="canvas-text"
          :class="{ selected: object.id === selectedObjectId }"
          :x="object.anchor.x"
          :y="object.anchor.y"
          :font-size="object.fontSize"
          :data-object-id="object.id"
          :data-role="object.role"
          :data-generated="object.generated ? 'true' : 'false'"
          :transform="`rotate(${object.rotationDeg} ${object.anchor.x} ${object.anchor.y})`"
          dominant-baseline="middle"
          text-anchor="middle"
          @pointerdown.stop="onObjectPointerDown($event, object.id)"
        >
          {{ object.text }}
        </text>
      </g>

      <g v-if="ghostText" class="ghost-layer">
        <text
          class="ghost-text"
          :x="ghostText.anchor.x"
          :y="ghostText.anchor.y"
          :font-size="ghostText.fontSize"
          :transform="`rotate(${ghostText.rotationDeg} ${ghostText.anchor.x} ${ghostText.anchor.y})`"
          dominant-baseline="middle"
          text-anchor="middle"
        >
          {{ ghostText.text }}
        </text>
      </g>

      <g v-if="virtualPoint" class="virtual-point-layer">
        <line :x1="virtualPoint.x - 9" :y1="virtualPoint.y" :x2="virtualPoint.x + 9" :y2="virtualPoint.y" class="virtual-point-line" />
        <line :x1="virtualPoint.x" :y1="virtualPoint.y - 9" :x2="virtualPoint.x" :y2="virtualPoint.y + 9" class="virtual-point-line" />
        <circle :cx="virtualPoint.x" :cy="virtualPoint.y" r="4" class="virtual-point-ring" />
      </g>

      <g v-if="activeGuidePoint" class="guide-layer">
        <line :x1="activeGuidePoint.x" y1="0" :x2="activeGuidePoint.x" y2="520" class="guide-line" />
        <line x1="0" :y1="activeGuidePoint.y" x2="900" :y2="activeGuidePoint.y" class="guide-line" />
      </g>
    </svg>

    <CanvasContextMenu
      :visible="contextMenu.visible"
      :x="contextMenu.x"
      :y="contextMenu.y"
      :has-selection="Boolean(selectedObject)"
      :can-paste="Boolean(referenceClipboard)"
      @command="onContextCommand"
    />

    <aside class="properties-panel">
      <h2>Properties</h2>
      <template v-if="selectedObject">
        <label>Text
          <input v-model="selectedObject.text" type="text" />
        </label>
        <label>X
          <input v-model.number="selectedObject.anchor.x" type="number" step="1" />
        </label>
        <label>Y
          <input v-model.number="selectedObject.anchor.y" type="number" step="1" />
        </label>
        <label>Rotation
          <input v-model.number="selectedObject.rotationDeg" type="number" step="90" />
        </label>
      </template>
      <p v-else>Select a text object on the canvas.</p>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import CanvasContextMenu from './CanvasContextMenu.vue'
import type { EditorCommand, EditorInteractionMode } from '../../lib/editor/interactionModes'
import { formatPoint, snapPoint, type Point, type SnapCandidate, type SnapKind } from '../../lib/editor/snapService'
import {
  createReferenceClipboard,
  placeItemAtReferencePoint,
  type ReferenceClipboardPayload,
  type TextClipboardItem,
} from '../../lib/editor/referenceClipboard'

type TextObjectRole = 'bay-label' | 'bus-label' | 'free-text-box'

type CanvasTextObject = {
  id: string
  text: string
  anchor: Point
  center: Point
  rotationDeg: number
  fontSize: number
  role: TextObjectRole
  generated?: boolean
}

const props = defineProps<{
  activeMode: EditorInteractionMode
  command: EditorCommand | null
}>()

const emit = defineEmits<{
  modeChange: [mode: EditorInteractionMode]
  statusChange: [status: {
    pointer: Point | null
    snapKind: SnapKind | null
    snapLabel: string
    selectedObjectName: string
    message: string
  }]
  commandHandled: []
}>()

const svgRef = ref<SVGSVGElement | null>(null)
const selectedObjectId = ref<string | null>('bay_label_1')
const virtualPoint = ref<Point | null>(null)
const activeGuidePoint = ref<Point | null>(null)
const referenceClipboard = ref<ReferenceClipboardPayload | null>(null)
const copyBaseSelection = ref<CanvasTextObject | null>(null)
const message = ref('Editor shell ready. Use Ribbon or right-click canvas commands.')
const contextMenu = reactive({ visible: false, x: 0, y: 0, point: { x: 0, y: 0 } as Point })

const baySlots = Array.from({ length: 8 }, (_, index) => ({
  id: `slot_${index + 1}`,
  x: 108 + index * 48,
  y: 190,
}))

const textObjects = ref<CanvasTextObject[]>([
  ...baySlots.map((slot, index) => ({
    id: `bay_label_${index + 1}`,
    text: String(index + 1),
    anchor: { x: slot.x, y: 156 },
    center: { x: slot.x, y: 156 },
    rotationDeg: 0,
    fontSize: 16,
    role: 'bay-label' as const,
  })),
  {
    id: 'bus_label_1',
    text: '1С 10 кВ',
    anchor: { x: 512, y: 190 },
    center: { x: 512, y: 190 },
    rotationDeg: 0,
    fontSize: 18,
    role: 'bus-label',
  },
])

const selectedObject = computed(() => textObjects.value.find((object) => object.id === selectedObjectId.value) ?? null)

const snapCandidates = computed<SnapCandidate[]>(() => [
  ...baySlots.map((slot) => ({ x: slot.x, y: slot.y, kind: 'slot' as const, label: slot.id })),
  ...textObjects.value.map((object) => ({
    x: object.center.x,
    y: object.center.y,
    kind: 'object' as const,
    label: object.text,
  })),
])

const ghostText = computed<CanvasTextObject | null>(() => {
  if (props.activeMode !== 'paste_by_point' || !referenceClipboard.value || !virtualPoint.value) return null
  return placeItemAtReferencePoint(referenceClipboard.value.items[0], referenceClipboard.value, virtualPoint.value) as CanvasTextObject
})

function svgPointFromPointer(event: PointerEvent): Point | null {
  const svg = svgRef.value
  if (!svg) return null
  const point = svg.createSVGPoint()
  point.x = event.clientX
  point.y = event.clientY
  const ctm = svg.getScreenCTM()
  if (!ctm) return null
  const transformed = point.matrixTransform(ctm.inverse())
  return { x: transformed.x, y: transformed.y }
}

function snapCanvasPoint(point: Point) {
  return snapPoint(point, {
    enabled: true,
    gridSize: 12,
    tolerance: 7,
    candidates: snapCandidates.value,
  })
}

function setStatus(pointer: Point | null, snapKind: SnapKind | null, snapLabel: string): void {
  emit('statusChange', {
    pointer,
    snapKind,
    snapLabel,
    selectedObjectName: selectedObject.value?.text ?? '',
    message: message.value,
  })
}

function updateVirtualPointFromEvent(event: PointerEvent): Point | null {
  const point = svgPointFromPointer(event)
  if (!point) return null
  const snapped = snapCanvasPoint(point)
  virtualPoint.value = { x: snapped.x, y: snapped.y }
  activeGuidePoint.value = { x: snapped.x, y: snapped.y }
  setStatus(virtualPoint.value, snapped.kind, snapped.label)
  return virtualPoint.value
}

function canvasObjectToClipboardItem(object: CanvasTextObject): TextClipboardItem {
  return {
    kind: 'text',
    text: object.text,
    sourceId: object.id,
    anchor: { ...object.anchor },
    center: { ...object.center },
    rotationDeg: object.rotationDeg,
    fontSize: object.fontSize,
    role: object.role,
  }
}

function copySelectedFromCenter(): void {
  if (!selectedObject.value) {
    message.value = 'Select an object before copy.'
    setStatus(virtualPoint.value, null, '')
    return
  }

  referenceClipboard.value = createReferenceClipboard(
    [canvasObjectToClipboardItem(selectedObject.value)],
    { ...selectedObject.value.center },
  )
  message.value = 'Copied from selected object center. Use Paste by point.'
  emit('modeChange', 'paste_by_point')
  setStatus(virtualPoint.value, 'object', selectedObject.value.text)
}

function beginCopyByReference(): void {
  if (!selectedObject.value) {
    message.value = 'Select an object before copy by reference.'
    setStatus(virtualPoint.value, null, '')
    return
  }

  copyBaseSelection.value = selectedObject.value
  message.value = 'Pick the virtual base point. It snaps to grid, slots and object centers.'
  emit('modeChange', 'copy_by_reference')
  setStatus(virtualPoint.value, null, '')
}

function pasteAtPoint(point: Point): void {
  if (!referenceClipboard.value) {
    message.value = 'Clipboard is empty.'
    setStatus(point, null, '')
    return
  }

  const source = referenceClipboard.value.items[0]
  const placed = placeItemAtReferencePoint(source, referenceClipboard.value, point)
  const id = `${placed.sourceId}_${textObjects.value.length + 1}`

  textObjects.value.push({
    id,
    text: placed.text,
    anchor: { ...placed.anchor },
    center: { ...placed.center },
    rotationDeg: placed.rotationDeg,
    fontSize: placed.fontSize,
    role: 'free-text-box',
    generated: true,
  })

  selectedObjectId.value = id
  message.value = `Pasted relative to base point at ${formatPoint(point)}. Click another point to repeat.`
  setStatus(point, 'grid', 'Paste point')
}

function rotateSelected(degrees: number): void {
  if (!selectedObject.value) return
  selectedObject.value.rotationDeg = degrees
  message.value = `Rotated selected object to ${degrees}°.`
  setStatus(virtualPoint.value, null, '')
}

function deleteSelected(): void {
  if (!selectedObject.value) return
  textObjects.value = textObjects.value.filter((object) => object.id !== selectedObjectId.value)
  selectedObjectId.value = null
  message.value = 'Object deleted.'
  setStatus(virtualPoint.value, null, '')
}

function clearGenerated(): void {
  textObjects.value = textObjects.value.filter((object) => !object.generated)
  selectedObjectId.value = null
  message.value = 'Generated pasted objects cleared.'
  setStatus(virtualPoint.value, null, '')
}

function handleCommand(command: EditorCommand): void {
  if (command === 'copy') copySelectedFromCenter()
  else if (command === 'copy_by_reference') beginCopyByReference()
  else if (command === 'paste' || command === 'paste_by_point') {
    message.value = referenceClipboard.value ? 'Pick paste point.' : 'Clipboard is empty.'
    emit('modeChange', 'paste_by_point')
    setStatus(virtualPoint.value, null, '')
  }
  else if (command === 'rotate_0') rotateSelected(0)
  else if (command === 'rotate_90') rotateSelected(90)
  else if (command === 'rotate_minus_90') rotateSelected(-90)
  else if (command === 'delete') deleteSelected()
  else if (command === 'clear_generated') clearGenerated()
  emit('commandHandled')
}

function onPointerMove(event: PointerEvent): void {
  updateVirtualPointFromEvent(event)
}

function onCanvasPointerDown(event: PointerEvent): void {
  if ((event.target as Element).closest('.canvas-text')) return

  const point = updateVirtualPointFromEvent(event)
  if (!point) return

  if (props.activeMode === 'copy_by_reference' && copyBaseSelection.value) {
    referenceClipboard.value = createReferenceClipboard([canvasObjectToClipboardItem(copyBaseSelection.value)], point)
    message.value = `Base point saved at ${formatPoint(point)}. Pick paste point.`
    emit('modeChange', 'paste_by_point')
    setStatus(point, 'grid', 'Base point')
    return
  }

  if (props.activeMode === 'paste_by_point') {
    pasteAtPoint(point)
    return
  }

  selectedObjectId.value = null
  message.value = 'Canvas selected.'
  setStatus(point, 'grid', 'Canvas')
}

function onObjectPointerDown(event: PointerEvent, objectId: string): void {
  selectedObjectId.value = objectId

  if (props.activeMode !== 'select') {
    message.value = 'Object selected. Use Select mode to drag it.'
    setStatus(virtualPoint.value, 'object', selectedObject.value?.text ?? '')
    return
  }

  const object = selectedObject.value
  const startPoint = svgPointFromPointer(event)
  if (!object || !startPoint) return

  const baseAnchor = { ...object.anchor }
  const baseCenter = { ...object.center }
  const pointerId = event.pointerId

  ;(event.currentTarget as Element).setPointerCapture?.(pointerId)

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    const current = svgPointFromPointer(moveEvent)
    if (!current) return
    const rawCenter = {
      x: baseCenter.x + current.x - startPoint.x,
      y: baseCenter.y + current.y - startPoint.y,
    }
    const snapped = snapCanvasPoint(rawCenter)
    const dx = snapped.x - baseCenter.x
    const dy = snapped.y - baseCenter.y
    object.center = { x: snapped.x, y: snapped.y }
    object.anchor = { x: baseAnchor.x + dx, y: baseAnchor.y + dy }
    virtualPoint.value = { x: snapped.x, y: snapped.y }
    activeGuidePoint.value = { x: snapped.x, y: snapped.y }
    message.value = `Dragging ${object.text}.`
    setStatus(virtualPoint.value, snapped.kind, snapped.label)
  }

  const up = (upEvent: PointerEvent) => {
    if (upEvent.pointerId !== pointerId) return
    window.removeEventListener('pointermove', move)
    window.removeEventListener('pointerup', up)
    message.value = `Placed ${object.text}.`
    setStatus(virtualPoint.value, null, '')
  }

  window.addEventListener('pointermove', move)
  window.addEventListener('pointerup', up)
}

function onContextMenu(event: MouseEvent): void {
  const point = svgPointFromPointer(event as unknown as PointerEvent)
  contextMenu.visible = true
  contextMenu.x = event.clientX
  contextMenu.y = event.clientY
  contextMenu.point = point ?? { x: 0, y: 0 }

  const targetObject = (event.target as Element).closest('.canvas-text')
  if (targetObject) {
    selectedObjectId.value = targetObject.getAttribute('data-object-id')
  }
}

function onContextCommand(command: EditorCommand): void {
  hideContextMenu()
  if (command === 'copy_by_reference') beginCopyByReference()
  else if (command === 'paste_by_point') emit('modeChange', 'paste_by_point')
  else handleCommand(command)
}

function hideContextMenu(): void {
  contextMenu.visible = false
}

watch(() => props.command, (command) => {
  if (command) handleCommand(command)
})

setStatus(null, null, '')
</script>

<style scoped>
.canvas-workspace {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 260px;
  min-height: 0;
  background: #e5edf7;
}

.editor-canvas {
  width: 100%;
  height: 100%;
  min-height: 540px;
  background: white;
  cursor: crosshair;
}

.busbar {
  fill: var(--busbar-color, #6d0ad6);
  stroke: #3b0764;
  stroke-width: 1;
}

.bay-slot {
  fill: #ffffff;
  stroke: #3b0764;
  stroke-width: 1.5;
}

.canvas-text {
  fill: #111827;
  font-family: Arial, sans-serif;
  cursor: grab;
  user-select: none;
}

.canvas-text.selected {
  paint-order: stroke;
  stroke: rgba(37, 99, 235, 0.35);
  stroke-width: 4px;
}

.ghost-text {
  fill: #2563eb;
  opacity: 0.35;
  font-family: Arial, sans-serif;
  pointer-events: none;
}

.virtual-point-line {
  stroke: #f59e0b;
  stroke-width: 1.6;
  pointer-events: none;
}

.virtual-point-ring {
  fill: none;
  stroke: #f59e0b;
  stroke-width: 1.6;
  pointer-events: none;
}

.guide-line {
  stroke: #2563eb;
  stroke-width: 1;
  stroke-dasharray: 4 4;
  opacity: 0.75;
  pointer-events: none;
}

.properties-panel {
  border-left: 1px solid #cbd5e1;
  background: #f8fafc;
  padding: 14px;
  overflow: auto;
}

.properties-panel h2 {
  margin: 0 0 12px;
  font-size: 15px;
}

.properties-panel label {
  display: grid;
  gap: 5px;
  margin-bottom: 10px;
  color: #475569;
  font-size: 12px;
  font-weight: 800;
}

.properties-panel input {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 7px 8px;
}
</style>