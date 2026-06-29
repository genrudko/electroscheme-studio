<template>
  <div class="canvas-workspace" @pointerdown="hideContextMenu">
    <svg
      ref="svgRef"
      class="editor-canvas"
      :viewBox="canvasViewBox"
      @pointermove="onPointerMove"
      @pointerdown="onCanvasPointerDown"
      @contextmenu.prevent.stop="onContextMenu"
    >
      <defs>
        <pattern id="editor-grid" :width="settings.gridStep" :height="settings.gridStep" patternUnits="userSpaceOnUse">
          <path
            :d="`M ${settings.gridStep} 0 L 0 0 0 ${settings.gridStep}`"
            fill="none"
            stroke="#e5e7eb"
            stroke-width="0.6"
          />
        </pattern>
        <pattern id="editor-grid-major" :width="majorGridStep" :height="majorGridStep" patternUnits="userSpaceOnUse">
          <rect :width="majorGridStep" :height="majorGridStep" fill="url(#editor-grid)" />
          <path
            :d="`M ${majorGridStep} 0 L 0 0 0 ${majorGridStep}`"
            fill="none"
            stroke="#cbd5e1"
            stroke-width="0.9"
          />
        </pattern>
      </defs>

      <rect x="0" y="0" :width="canvasWidth" :height="canvasHeight" fill="#ffffff" />
      <rect
        v-if="settings.gridVisible"
        x="0"
        y="0"
        :width="canvasWidth"
        :height="canvasHeight"
        fill="url(#editor-grid-major)"
      />

      <g class="object-layer">
        <g v-for="busbar in busbars" :key="busbar.id" class="busbar-object">
          <rect
            class="busbar"
            :x="busbar.x"
            :y="busbar.y"
            :width="busbar.width"
            :height="busbar.height"
            rx="2"
          />
        </g>

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

      <g v-if="virtualPoint && showVirtualPoint" class="virtual-point-layer">
        <line :x1="virtualPoint.x - 9" :y1="virtualPoint.y" :x2="virtualPoint.x + 9" :y2="virtualPoint.y" class="virtual-point-line" />
        <line :x1="virtualPoint.x" :y1="virtualPoint.y - 9" :x2="virtualPoint.x" :y2="virtualPoint.y + 9" class="virtual-point-line" />
        <circle :cx="virtualPoint.x" :cy="virtualPoint.y" r="4" class="virtual-point-ring" />
      </g>

      <g v-if="settings.guidesVisible && activeGuidePoint" class="guide-layer">
        <line :x1="activeGuidePoint.x" y1="0" :x2="activeGuidePoint.x" :y2="canvasHeight" class="guide-line" />
        <line x1="0" :y1="activeGuidePoint.y" :x2="canvasWidth" :y2="activeGuidePoint.y" class="guide-line" />
      </g>

      <g v-if="busbars.length === 0 && textObjects.length === 0" class="empty-canvas-hint">
        <text x="450" y="235" text-anchor="middle" dominant-baseline="middle">
          Пустой канвас
        </text>
        <text x="450" y="265" text-anchor="middle" dominant-baseline="middle" class="hint-small">
          Добавьте шину или текст через ленту либо ПКМ-меню
        </text>
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
      <h2>Свойства</h2>
      <template v-if="selectedObject">
        <label>Текст
          <input v-model="selectedObject.text" type="text" />
        </label>
        <label>X
          <input v-model.number="selectedObject.anchor.x" type="number" step="1" />
        </label>
        <label>Y
          <input v-model.number="selectedObject.anchor.y" type="number" step="1" />
        </label>
        <label>Поворот
          <input v-model.number="selectedObject.rotationDeg" type="number" step="90" />
        </label>
      </template>
      <template v-else>
        <p>Выберите текстовый объект на канвасе.</p>
        <button type="button" class="panel-button" @click="createSampleBusbar">Добавить шину</button>
        <button type="button" class="panel-button" @click="createTextObject">Добавить текст</button>
      </template>

      <hr />

      <h3>Канвас</h3>
      <p class="settings-summary">
        Масштаб: {{ Math.round(settings.zoom * 100) }}%<br />
        Сетка: {{ settings.gridVisible ? 'вкл' : 'выкл' }}, шаг {{ settings.gridStep }}<br />
        Привязки: {{ settings.snapEnabled ? 'вкл' : 'выкл' }}, допуск {{ settings.snapTolerance }}
      </p>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import CanvasContextMenu from './CanvasContextMenu.vue'
import type { CanvasSettings } from '../../lib/editor/canvasSettings'
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

type BusbarObject = {
  id: string
  x: number
  y: number
  width: number
  height: number
  slots: number
  slotSpacing: number
  labelStart: number
}

type BaySlot = {
  id: string
  busbarId: string
  x: number
  y: number
}

const props = defineProps<{
  activeMode: EditorInteractionMode
  command: EditorCommand | null
  settings: CanvasSettings
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
const canvasWidth = 900
const canvasHeight = 520
const selectedObjectId = ref<string | null>(null)
const virtualPoint = ref<Point | null>(null)
const activeGuidePoint = ref<Point | null>(null)
const referenceClipboard = ref<ReferenceClipboardPayload | null>(null)
const copyBaseSelection = ref<CanvasTextObject | null>(null)
const message = ref('Пустой редактор готов. Добавьте шину или текст через ленту либо ПКМ.')
const contextMenu = reactive({ visible: false, x: 0, y: 0, point: { x: 0, y: 0 } as Point })

const busbars = ref<BusbarObject[]>([])
const textObjects = ref<CanvasTextObject[]>([])

const majorGridStep = computed(() => props.settings.gridStep * 5)
const viewBoxWidth = computed(() => canvasWidth / props.settings.zoom)
const viewBoxHeight = computed(() => canvasHeight / props.settings.zoom)
const canvasViewBox = computed(() => `0 0 ${viewBoxWidth.value} ${viewBoxHeight.value}`)
const showVirtualPoint = computed(() => props.activeMode === 'copy_by_reference' || props.activeMode === 'paste_by_point')

const baySlots = computed<BaySlot[]>(() => {
  const slots: BaySlot[] = []

  for (const busbar of busbars.value) {
    const firstX = busbar.x + 12
    const y = busbar.y + busbar.height / 2

    for (let index = 0; index < busbar.slots; index += 1) {
      slots.push({
        id: `${busbar.id}_slot_${index + 1}`,
        busbarId: busbar.id,
        x: firstX + index * busbar.slotSpacing,
        y,
      })
    }
  }

  return slots
})

const selectedObject = computed(() => textObjects.value.find((object) => object.id === selectedObjectId.value) ?? null)

const snapCandidates = computed<SnapCandidate[]>(() => {
  const candidates: SnapCandidate[] = []

  if (props.settings.snapSlots) {
    candidates.push(...baySlots.value.map((slot) => ({
      x: slot.x,
      y: slot.y,
      kind: 'slot' as const,
      label: slot.id,
    })))
  }

  if (props.settings.snapObjects) {
    candidates.push(...textObjects.value.map((object) => ({
      x: object.center.x,
      y: object.center.y,
      kind: 'object' as const,
      label: object.text,
    })))
  }

  return candidates
})

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
    enabled: props.settings.snapEnabled,
    gridSize: props.settings.gridStep,
    snapGrid: props.settings.snapGrid,
    tolerance: props.settings.snapTolerance,
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

function createSampleBusbar(): void {
  const nextIndex = busbars.value.length + 1
  const x = 96
  const y = 180 + (nextIndex - 1) * 80
  const slots = 8
  const slotSpacing = 48
  const width = 24 + (slots - 1) * slotSpacing
  const busbarId = `busbar_${nextIndex}`

  busbars.value.push({
    id: busbarId,
    x,
    y,
    width,
    height: 20,
    slots,
    slotSpacing,
    labelStart: 1,
  })

  for (let index = 0; index < slots; index += 1) {
    const slotX = x + 12 + index * slotSpacing
    textObjects.value.push({
      id: `${busbarId}_bay_label_${index + 1}`,
      text: String(index + 1),
      anchor: { x: slotX, y: y - 34 },
      center: { x: slotX, y: y - 34 },
      rotationDeg: 0,
      fontSize: 16,
      role: 'bay-label',
    })
  }

  textObjects.value.push({
    id: `${busbarId}_caption`,
    text: '1С 10 кВ',
    anchor: { x: x + width + 52, y: y + 10 },
    center: { x: x + width + 52, y: y + 10 },
    rotationDeg: 0,
    fontSize: 18,
    role: 'bus-label',
  })

  message.value = 'Шина добавлена как объект канваса, а не как вшитый фон.'
  setStatus(virtualPoint.value, null, '')
}

function createTextObject(): void {
  const point = virtualPoint.value ?? { x: 180, y: 120 }
  const snapped = snapCanvasPoint(point)
  const id = `text_${textObjects.value.length + 1}`

  textObjects.value.push({
    id,
    text: 'Текст',
    anchor: { x: snapped.x, y: snapped.y },
    center: { x: snapped.x, y: snapped.y },
    rotationDeg: 0,
    fontSize: 16,
    role: 'free-text-box',
  })

  selectedObjectId.value = id
  message.value = 'Текст добавлен на канвас.'
  setStatus({ x: snapped.x, y: snapped.y }, snapped.kind, snapped.label)
}

function copySelectedFromCenter(): void {
  if (!selectedObject.value) {
    message.value = 'Сначала выберите объект для копирования.'
    setStatus(virtualPoint.value, null, '')
    return
  }

  referenceClipboard.value = createReferenceClipboard(
    [canvasObjectToClipboardItem(selectedObject.value)],
    { ...selectedObject.value.center },
  )
  message.value = 'Скопировано от центра выбранного объекта. Укажите точку вставки.'
  emit('modeChange', 'paste_by_point')
  setStatus(virtualPoint.value, 'object', selectedObject.value.text)
}

function beginCopyByReference(): void {
  if (!selectedObject.value) {
    message.value = 'Сначала выберите объект для копирования с базовой точкой.'
    setStatus(virtualPoint.value, null, '')
    return
  }

  copyBaseSelection.value = selectedObject.value
  message.value = 'Укажите виртуальную базовую точку. Она привязывается к сетке, ячейкам и объектам.'
  emit('modeChange', 'copy_by_reference')
  setStatus(virtualPoint.value, null, '')
}

function pasteAtPoint(point: Point): void {
  if (!referenceClipboard.value) {
    message.value = 'Буфер пуст.'
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
  message.value = `Вставлено относительно базовой точки в ${formatPoint(point)}. Можно указать следующую точку.`
  setStatus(point, 'grid', 'Точка вставки')
}

function rotateSelected(degrees: number): void {
  if (!selectedObject.value) return
  selectedObject.value.rotationDeg = degrees
  message.value = `Выбранный объект повернут на ${degrees}°.`
  setStatus(virtualPoint.value, null, '')
}

function deleteSelected(): void {
  if (!selectedObject.value) return
  textObjects.value = textObjects.value.filter((object) => object.id !== selectedObjectId.value)
  selectedObjectId.value = null
  message.value = 'Объект удалён.'
  setStatus(virtualPoint.value, null, '')
}

function clearGenerated(): void {
  textObjects.value = textObjects.value.filter((object) => !object.generated)
  selectedObjectId.value = null
  message.value = 'Вставленные копии очищены.'
  setStatus(virtualPoint.value, null, '')
}

function handleCommand(command: EditorCommand): void {
  if (command === 'copy') copySelectedFromCenter()
  else if (command === 'copy_by_reference') beginCopyByReference()
  else if (command === 'paste' || command === 'paste_by_point') {
    message.value = referenceClipboard.value ? 'Укажите точку вставки.' : 'Буфер пуст.'
    emit('modeChange', 'paste_by_point')
    setStatus(virtualPoint.value, null, '')
  }
  else if (command === 'rotate_0') rotateSelected(0)
  else if (command === 'rotate_90') rotateSelected(90)
  else if (command === 'rotate_minus_90') rotateSelected(-90)
  else if (command === 'delete') deleteSelected()
  else if (command === 'clear_generated') clearGenerated()
  else if (command === 'create_sample_busbar') createSampleBusbar()
  else if (command === 'create_text') createTextObject()
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
    message.value = `Базовая точка сохранена: ${formatPoint(point)}. Укажите точку вставки.`
    emit('modeChange', 'paste_by_point')
    setStatus(point, 'grid', 'Базовая точка')
    return
  }

  if (props.activeMode === 'paste_by_point') {
    pasteAtPoint(point)
    return
  }

  selectedObjectId.value = null
  message.value = 'Канвас выбран.'
  setStatus(point, 'grid', 'Канвас')
}

function onObjectPointerDown(event: PointerEvent, objectId: string): void {
  selectedObjectId.value = objectId

  if (props.activeMode !== 'select') {
    message.value = 'Объект выбран. Для перетаскивания включите режим «Выбор».'
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
    message.value = `Перемещение: ${object.text}.`
    setStatus(virtualPoint.value, snapped.kind, snapped.label)
  }

  const up = (upEvent: PointerEvent) => {
    if (upEvent.pointerId !== pointerId) return
    window.removeEventListener('pointermove', move)
    window.removeEventListener('pointerup', up)
    message.value = `Размещено: ${object.text}.`
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
  grid-template-columns: 1fr 280px;
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

.empty-canvas-hint {
  fill: #64748b;
  font-family: Arial, sans-serif;
  font-size: 22px;
  pointer-events: none;
}

.empty-canvas-hint .hint-small {
  fill: #94a3b8;
  font-size: 13px;
}

.properties-panel {
  border-left: 1px solid #cbd5e1;
  background: #f8fafc;
  padding: 14px;
  overflow: auto;
}

.properties-panel h2,
.properties-panel h3 {
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

.properties-panel p,
.settings-summary {
  color: #475569;
  font-size: 13px;
  line-height: 1.45;
}

.properties-panel hr {
  border: 0;
  border-top: 1px solid #e2e8f0;
  margin: 14px 0;
}

.panel-button {
  display: block;
  width: 100%;
  margin-bottom: 8px;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: white;
  color: #1e3a8a;
  cursor: pointer;
  font-weight: 800;
  padding: 8px 10px;
}
</style>