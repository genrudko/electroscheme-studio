<template>
  <div class="canvas-workspace" @pointerdown="hideContextMenu">
    <div class="canvas-frame" :class="{ 'without-rulers': !settings.rulersVisible }">
      <div v-if="settings.rulersVisible" class="ruler-corner">0</div>

      <svg
        v-if="settings.rulersVisible"
        class="top-ruler"
        :viewBox="canvasViewBox"
        preserveAspectRatio="none"
        @pointerdown.prevent="onTopRulerPointerDown"
      >
        <rect :x="viewOrigin.x" :y="viewOrigin.y" :width="viewBoxWidth" height="24" fill="#f8fafc" />
        <g v-for="tick in rulerXTicks" :key="`x_${tick}`">
          <line
            :x1="tick"
            :x2="tick"
            :y1="viewOrigin.y"
            :y2="viewOrigin.y + (tick % majorGridStep === 0 ? 18 : 10)"
            stroke="#94a3b8"
            stroke-width="1"
          />
          <text
            v-if="tick % majorGridStep === 0"
            :x="tick + 2"
            :y="viewOrigin.y + 22"
            font-size="10"
            fill="#475569"
          >{{ tick }}</text>
        </g>
      </svg>

      <svg
        v-if="settings.rulersVisible"
        class="left-ruler"
        :viewBox="canvasViewBox"
        preserveAspectRatio="none"
        @pointerdown.prevent="onLeftRulerPointerDown"
      >
        <rect :x="viewOrigin.x" :y="viewOrigin.y" width="24" :height="viewBoxHeight" fill="#f8fafc" />
        <g v-for="tick in rulerYTicks" :key="`y_${tick}`">
          <line
            :x1="viewOrigin.x"
            :x2="viewOrigin.x + (tick % majorGridStep === 0 ? 18 : 10)"
            :y1="tick"
            :y2="tick"
            stroke="#94a3b8"
            stroke-width="1"
          />
          <text
            v-if="tick % majorGridStep === 0"
            :x="viewOrigin.x + 3"
            :y="tick - 2"
            font-size="10"
            fill="#475569"
          >{{ tick }}</text>
        </g>
      </svg>

      <div
        ref="canvasScrollRef"
        class="canvas-scroll"
        @wheel.prevent="onWheelZoom"
      >
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

          <g v-if="settings.guidesVisible" class="guide-object-layer">
            <line
              v-for="guide in verticalGuides"
              :key="guide.id"
              :x1="guide.position"
              y1="0"
              :x2="guide.position"
              :y2="canvasHeight"
              class="user-guide-line"
              @pointerdown.stop="onGuidePointerDown($event, guide.id)"
            />
            <line
              v-for="guide in horizontalGuides"
              :key="guide.id"
              x1="0"
              :y1="guide.position"
              :x2="canvasWidth"
              :y2="guide.position"
              class="user-guide-line"
              @pointerdown.stop="onGuidePointerDown($event, guide.id)"
            />
          </g>

          <g class="object-layer">
            <g
              v-for="busbar in busbars"
              :key="busbar.id"
              class="busbar-object"
              :class="{ selected: selectedElement?.kind === 'busbar' && selectedElement.id === busbar.id }"
              @pointerdown.stop="onBusbarPointerDown($event, busbar.id)"
            >
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
              :class="{ selected: selectedElement?.kind === 'text' && selectedElement.id === object.id }"
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
      </div>
    </div>

    <CanvasContextMenu
      :visible="contextMenu.visible"
      :x="contextMenu.x"
      :y="contextMenu.y"
      :has-selection="Boolean(selectedElement)"
      :can-paste="Boolean(referenceClipboard)"
      @command="onContextCommand"
    />

    <aside class="properties-panel">
      <template v-if="selectedBusbar">
        <h2>Свойства шины</h2>
        <label>X <input v-model.number="selectedBusbar.x" type="number" step="1" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <label>Y <input v-model.number="selectedBusbar.y" type="number" step="1" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <label>Длина <input v-model.number="selectedBusbar.width" type="number" min="24" step="1" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <label>Толщина <input v-model.number="selectedBusbar.height" type="number" min="4" step="1" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <label>Ячеек <input v-model.number="selectedBusbar.slots" type="number" min="1" max="40" step="1" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <label>Шаг ячеек <input v-model.number="selectedBusbar.slotSpacing" type="number" min="8" step="1" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <label>Подпись <input v-model="selectedBusbar.label" type="text" @change="syncBusbarLabels(selectedBusbar)" /></label>
      </template>

      <template v-else-if="selectedText">
        <h2>Свойства текста</h2>
        <label>Текст <input v-model="selectedText.text" type="text" /></label>
        <label>X <input v-model.number="selectedText.anchor.x" type="number" step="1" /></label>
        <label>Y <input v-model.number="selectedText.anchor.y" type="number" step="1" /></label>
        <label>Поворот <input v-model.number="selectedText.rotationDeg" type="number" step="90" /></label>
      </template>

      <template v-else>
        <h2>Свойства</h2>
        <p>Выберите объект на канвасе.</p>
        <button type="button" class="panel-button" @click="createSampleBusbar">Добавить шину</button>
        <button type="button" class="panel-button" @click="createTextObject">Добавить текст</button>
      </template>

      <hr />

      <h3>Канвас</h3>
      <p class="settings-summary">
        Масштаб: {{ Math.round(settings.zoom * 100) }}%<br />
        Сетка: {{ settings.gridVisible ? 'вкл' : 'выкл' }}, шаг {{ settings.gridStep }}<br />
        Линейки: {{ settings.rulersVisible ? 'вкл' : 'выкл' }}<br />
        Направляющих: {{ guides.length }}
      </p>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import CanvasContextMenu from './CanvasContextMenu.vue'
import { normalizeCanvasSettings, type CanvasSettings } from '../../lib/editor/canvasSettings'
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
  busbarId?: string
  slotIndex?: number
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
  label: string
}

type BaySlot = {
  id: string
  busbarId: string
  x: number
  y: number
}

type CanvasGuide = {
  id: string
  orientation: 'vertical' | 'horizontal'
  position: number
}

type SelectedElement =
  | { kind: 'text'; id: string }
  | { kind: 'busbar'; id: string }
  | null

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
  settingsChange: [settings: CanvasSettings]
  commandHandled: []
}>()

const svgRef = ref<SVGSVGElement | null>(null)
const canvasScrollRef = ref<HTMLDivElement | null>(null)
const canvasWidth = 1600
const canvasHeight = 1000
const viewOrigin = reactive<Point>({ x: 0, y: 0 })
const selectedElement = ref<SelectedElement>(null)
const virtualPoint = ref<Point | null>(null)
const activeGuidePoint = ref<Point | null>(null)
const referenceClipboard = ref<ReferenceClipboardPayload | null>(null)
const copyBaseSelection = ref<CanvasTextObject | null>(null)
const message = ref('Пустой редактор готов. Добавьте шину или текст через ленту либо ПКМ.')
const contextMenu = reactive({ visible: false, x: 0, y: 0, point: { x: 0, y: 0 } as Point })

const busbars = ref<BusbarObject[]>([])
const textObjects = ref<CanvasTextObject[]>([])
const guides = ref<CanvasGuide[]>([])

const majorGridStep = computed(() => props.settings.gridStep * 5)
const viewBoxWidth = computed(() => 900 / props.settings.zoom)
const viewBoxHeight = computed(() => 520 / props.settings.zoom)
const canvasViewBox = computed(() => `${viewOrigin.x} ${viewOrigin.y} ${viewBoxWidth.value} ${viewBoxHeight.value}`)
const showVirtualPoint = computed(() => props.activeMode === 'copy_by_reference' || props.activeMode === 'paste_by_point' || props.activeMode === 'create_guide')
const rulerXTicks = computed(() => createTicks(viewOrigin.x, viewOrigin.x + viewBoxWidth.value, props.settings.gridStep))
const rulerYTicks = computed(() => createTicks(viewOrigin.y, viewOrigin.y + viewBoxHeight.value, props.settings.gridStep))
const verticalGuides = computed(() => guides.value.filter((guide) => guide.orientation === 'vertical'))
const horizontalGuides = computed(() => guides.value.filter((guide) => guide.orientation === 'horizontal'))

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

const selectedText = computed(() => {
  if (selectedElement.value?.kind !== 'text') return null
  return textObjects.value.find((object) => object.id === selectedElement.value?.id) ?? null
})

const selectedBusbar = computed(() => {
  if (selectedElement.value?.kind !== 'busbar') return null
  return busbars.value.find((object) => object.id === selectedElement.value?.id) ?? null
})

const selectedObjectName = computed(() => selectedText.value?.text ?? selectedBusbar.value?.label ?? '')

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

    candidates.push(...busbars.value.map((busbar) => ({
      x: busbar.x + busbar.width / 2,
      y: busbar.y + busbar.height / 2,
      kind: 'object' as const,
      label: busbar.label,
    })))
  }

  if (props.settings.snapGuides) {
    for (const guide of guides.value) {
      if (guide.orientation === 'vertical') {
        candidates.push({ x: guide.position, y: virtualPoint.value?.y ?? 0, kind: 'guide', label: `X ${guide.position}` })
      } else {
        candidates.push({ x: virtualPoint.value?.x ?? 0, y: guide.position, kind: 'guide', label: `Y ${guide.position}` })
      }
    }
  }

  return candidates
})

const ghostText = computed<CanvasTextObject | null>(() => {
  if (props.activeMode !== 'paste_by_point' || !referenceClipboard.value || !virtualPoint.value) return null
  return placeItemAtReferencePoint(referenceClipboard.value.items[0], referenceClipboard.value, virtualPoint.value) as CanvasTextObject
})

function createTicks(from: number, to: number, step: number): number[] {
  const first = Math.floor(from / step) * step
  const ticks: number[] = []
  for (let value = first; value <= to + step; value += step) {
    ticks.push(value)
  }
  return ticks
}

function svgPointFromPointer(event: PointerEvent | MouseEvent): Point | null {
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
    selectedObjectName: selectedObjectName.value,
    message: message.value,
  })
}

function updateVirtualPointFromEvent(event: PointerEvent | MouseEvent): Point | null {
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

  const busbar: BusbarObject = {
    id: busbarId,
    x,
    y,
    width,
    height: 20,
    slots,
    slotSpacing,
    labelStart: 1,
    label: `${nextIndex}С 10 кВ`,
  }

  busbars.value.push(busbar)
  ensureBusbarLabels(busbar)
  selectedElement.value = { kind: 'busbar', id: busbar.id }

  message.value = 'Шина добавлена как редактируемый объект. Её можно перемещать и менять параметры.'
  setStatus(virtualPoint.value, null, '')
}

function ensureBusbarLabels(busbar: BusbarObject): void {
  textObjects.value = textObjects.value.filter((object) => object.busbarId !== busbar.id)

  for (let index = 0; index < busbar.slots; index += 1) {
    const slotX = busbar.x + 12 + index * busbar.slotSpacing
    textObjects.value.push({
      id: `${busbar.id}_bay_label_${index + 1}`,
      text: String(busbar.labelStart + index),
      anchor: { x: slotX, y: busbar.y - 34 },
      center: { x: slotX, y: busbar.y - 34 },
      rotationDeg: 0,
      fontSize: 16,
      role: 'bay-label',
      busbarId: busbar.id,
      slotIndex: index,
    })
  }

  textObjects.value.push({
    id: `${busbar.id}_caption`,
    text: busbar.label,
    anchor: { x: busbar.x + busbar.width + 52, y: busbar.y + busbar.height / 2 },
    center: { x: busbar.x + busbar.width + 52, y: busbar.y + busbar.height / 2 },
    rotationDeg: 0,
    fontSize: 18,
    role: 'bus-label',
    busbarId: busbar.id,
  })
}

function syncBusbarLabels(busbar: BusbarObject | null): void {
  if (!busbar) return
  busbar.slots = Math.max(1, Math.round(busbar.slots))
  busbar.slotSpacing = Math.max(8, busbar.slotSpacing)
  busbar.width = Math.max(24, busbar.width)
  busbar.height = Math.max(4, busbar.height)
  ensureBusbarLabels(busbar)
  message.value = `Параметры шины обновлены: ${busbar.label}.`
  setStatus(virtualPoint.value, 'object', busbar.label)
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

  selectedElement.value = { kind: 'text', id }
  message.value = 'Текст добавлен на канвас.'
  setStatus({ x: snapped.x, y: snapped.y }, snapped.kind, snapped.label)
}

function copySelectedFromCenter(): void {
  if (!selectedText.value) {
    message.value = 'Сейчас копирование работает для текста. Выберите текстовый объект.'
    setStatus(virtualPoint.value, null, '')
    return
  }

  referenceClipboard.value = createReferenceClipboard(
    [canvasObjectToClipboardItem(selectedText.value)],
    { ...selectedText.value.center },
  )
  message.value = 'Скопировано от центра выбранного объекта. Укажите точку вставки.'
  emit('modeChange', 'paste_by_point')
  setStatus(virtualPoint.value, 'object', selectedText.value.text)
}

function beginCopyByReference(): void {
  if (!selectedText.value) {
    message.value = 'Сейчас копирование с базовой точкой работает для текста. Выберите текстовый объект.'
    setStatus(virtualPoint.value, null, '')
    return
  }

  copyBaseSelection.value = selectedText.value
  message.value = 'Укажите виртуальную базовую точку. Она привязывается к сетке, ячейкам, объектам и направляющим.'
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

  selectedElement.value = { kind: 'text', id }
  message.value = `Вставлено относительно базовой точки в ${formatPoint(point)}. Можно указать следующую точку.`
  setStatus(point, 'grid', 'Точка вставки')
}

function rotateSelected(degrees: number): void {
  if (!selectedText.value) return
  selectedText.value.rotationDeg = degrees
  message.value = `Выбранный текст повернут на ${degrees}°.`
  setStatus(virtualPoint.value, null, '')
}

function deleteSelected(): void {
  if (!selectedElement.value) return

  if (selectedElement.value.kind === 'text') {
    textObjects.value = textObjects.value.filter((object) => object.id !== selectedElement.value?.id)
  } else if (selectedElement.value.kind === 'busbar') {
    const id = selectedElement.value.id
    busbars.value = busbars.value.filter((object) => object.id !== id)
    textObjects.value = textObjects.value.filter((object) => object.busbarId !== id)
  }

  selectedElement.value = null
  message.value = 'Объект удалён.'
  setStatus(virtualPoint.value, null, '')
}

function clearGenerated(): void {
  textObjects.value = textObjects.value.filter((object) => !object.generated)
  selectedElement.value = null
  message.value = 'Вставленные копии очищены.'
  setStatus(virtualPoint.value, null, '')
}

function createGuide(orientation: 'vertical' | 'horizontal', position?: number): void {
  const fallback = orientation === 'vertical'
    ? viewOrigin.x + viewBoxWidth.value / 2
    : viewOrigin.y + viewBoxHeight.value / 2

  const raw = position ?? fallback
  const snapped = Math.round(raw / props.settings.gridStep) * props.settings.gridStep

  guides.value.push({
    id: `guide_${orientation}_${guides.value.length + 1}`,
    orientation,
    position: snapped,
  })

  message.value = orientation === 'vertical'
    ? `Добавлена вертикальная направляющая X=${snapped}.`
    : `Добавлена горизонтальная направляющая Y=${snapped}.`
  setStatus(virtualPoint.value, 'guide', message.value)
}

function clearGuides(): void {
  guides.value = []
  message.value = 'Направляющие очищены.'
  setStatus(virtualPoint.value, null, '')
}

function setZoom(nextZoom: number): void {
  emit('settingsChange', normalizeCanvasSettings({ ...props.settings, zoom: nextZoom }))
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
  else if (command === 'create_vertical_guide') createGuide('vertical')
  else if (command === 'create_horizontal_guide') createGuide('horizontal')
  else if (command === 'clear_guides') clearGuides()
  else if (command === 'zoom_100') setZoom(1)
  else if (command === 'zoom_fit') {
    viewOrigin.x = 0
    viewOrigin.y = 0
    setZoom(1)
  }
  emit('commandHandled')
}

function onPointerMove(event: PointerEvent): void {
  updateVirtualPointFromEvent(event)
}

function onCanvasPointerDown(event: PointerEvent): void {
  if (event.button === 1) {
    startMiddleButtonPan(event)
    return
  }

  if ((event.target as Element).closest('.canvas-text') || (event.target as Element).closest('.busbar-object')) return

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

  selectedElement.value = null
  message.value = 'Канвас выбран.'
  setStatus(point, 'grid', 'Канвас')
}

function onObjectPointerDown(event: PointerEvent, objectId: string): void {
  selectedElement.value = { kind: 'text', id: objectId }
  startTextDrag(event, objectId)
}

function startTextDrag(event: PointerEvent, objectId: string): void {
  if (props.activeMode !== 'select') {
    message.value = 'Объект выбран. Для перетаскивания включите режим «Выбор».'
    setStatus(virtualPoint.value, 'object', selectedText.value?.text ?? '')
    return
  }

  const object = textObjects.value.find((item) => item.id === objectId)
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
    message.value = `Перемещение текста: ${object.text}.`
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

function onBusbarPointerDown(event: PointerEvent, busbarId: string): void {
  selectedElement.value = { kind: 'busbar', id: busbarId }

  if (props.activeMode !== 'select') {
    message.value = 'Шина выбрана. Для перемещения включите режим «Выбор».'
    setStatus(virtualPoint.value, 'object', selectedBusbar.value?.label ?? '')
    return
  }

  const busbar = busbars.value.find((item) => item.id === busbarId)
  const startPoint = svgPointFromPointer(event)
  if (!busbar || !startPoint) return

  const base = { x: busbar.x, y: busbar.y }
  const pointerId = event.pointerId

  ;(event.currentTarget as Element).setPointerCapture?.(pointerId)

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    const current = svgPointFromPointer(moveEvent)
    if (!current) return

    const rawPoint = {
      x: base.x + current.x - startPoint.x,
      y: base.y + current.y - startPoint.y,
    }
    const snapped = snapCanvasPoint(rawPoint)

    busbar.x = snapped.x
    busbar.y = snapped.y
    syncBusbarLabels(busbar)

    virtualPoint.value = { x: snapped.x, y: snapped.y }
    activeGuidePoint.value = { x: snapped.x, y: snapped.y }
    message.value = `Перемещение шины: ${busbar.label}.`
    setStatus(virtualPoint.value, snapped.kind, snapped.label)
  }

  const up = (upEvent: PointerEvent) => {
    if (upEvent.pointerId !== pointerId) return
    window.removeEventListener('pointermove', move)
    window.removeEventListener('pointerup', up)
    message.value = `Шина размещена: ${busbar.label}.`
    setStatus(virtualPoint.value, null, '')
  }

  window.addEventListener('pointermove', move)
  window.addEventListener('pointerup', up)
}

function onGuidePointerDown(event: PointerEvent, guideId: string): void {
  const guide = guides.value.find((item) => item.id === guideId)
  if (!guide) return
  const pointerId = event.pointerId
  ;(event.currentTarget as Element).setPointerCapture?.(pointerId)

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    const point = svgPointFromPointer(moveEvent)
    if (!point) return
    const snapped = snapCanvasPoint(point)
    guide.position = guide.orientation === 'vertical' ? snapped.x : snapped.y
    virtualPoint.value = { x: snapped.x, y: snapped.y }
    activeGuidePoint.value = { x: snapped.x, y: snapped.y }
    message.value = 'Перемещение направляющей.'
    setStatus(virtualPoint.value, 'guide', guide.id)
  }

  const up = (upEvent: PointerEvent) => {
    if (upEvent.pointerId !== pointerId) return
    window.removeEventListener('pointermove', move)
    window.removeEventListener('pointerup', up)
    message.value = 'Направляющая размещена.'
    setStatus(virtualPoint.value, 'guide', guide.id)
  }

  window.addEventListener('pointermove', move)
  window.addEventListener('pointerup', up)
}

function onTopRulerPointerDown(event: PointerEvent): void {
  const start = svgPointFromPointer(event)
  if (!start) return
  createGuide('vertical', start.x)
  const guide = guides.value[guides.value.length - 1]
  if (!guide) return
  onGuidePointerDown(event, guide.id)
}

function onLeftRulerPointerDown(event: PointerEvent): void {
  const start = svgPointFromPointer(event)
  if (!start) return
  createGuide('horizontal', start.y)
  const guide = guides.value[guides.value.length - 1]
  if (!guide) return
  onGuidePointerDown(event, guide.id)
}

function startMiddleButtonPan(event: PointerEvent): void {
  event.preventDefault()
  const start = { x: event.clientX, y: event.clientY }
  const startOrigin = { ...viewOrigin }
  const pointerId = event.pointerId
  svgRef.value?.setPointerCapture?.(pointerId)

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    const dx = (start.x - moveEvent.clientX) / props.settings.zoom
    const dy = (start.y - moveEvent.clientY) / props.settings.zoom
    viewOrigin.x = Math.max(0, Math.min(canvasWidth - viewBoxWidth.value, startOrigin.x + dx))
    viewOrigin.y = Math.max(0, Math.min(canvasHeight - viewBoxHeight.value, startOrigin.y + dy))
    message.value = 'Панорамирование средней кнопкой.'
    setStatus(virtualPoint.value, null, '')
  }

  const up = (upEvent: PointerEvent) => {
    if (upEvent.pointerId !== pointerId) return
    window.removeEventListener('pointermove', move)
    window.removeEventListener('pointerup', up)
  }

  window.addEventListener('pointermove', move)
  window.addEventListener('pointerup', up)
}

function onWheelZoom(event: WheelEvent): void {
  const factor = event.deltaY < 0 ? 1.08 : 0.92
  const nextZoom = Math.min(Math.max(props.settings.zoom * factor, 0.25), 4)
  emit('settingsChange', normalizeCanvasSettings({ ...props.settings, zoom: nextZoom }))
  message.value = `Масштаб: ${Math.round(nextZoom * 100)}%.`
  setStatus(virtualPoint.value, null, '')
}

function onContextMenu(event: MouseEvent): void {
  const point = svgPointFromPointer(event)
  contextMenu.visible = true
  contextMenu.x = event.clientX
  contextMenu.y = event.clientY
  contextMenu.point = point ?? { x: 0, y: 0 }

  const targetText = (event.target as Element).closest('.canvas-text')
  const targetBusbar = (event.target as Element).closest('.busbar-object')
  if (targetText) {
    selectedElement.value = { kind: 'text', id: targetText.getAttribute('data-object-id') ?? '' }
  } else if (targetBusbar) {
    const busbarId = targetBusbar.getAttribute('data-busbar-id')
    if (busbarId) selectedElement.value = { kind: 'busbar', id: busbarId }
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
  height: 100%;
  background: #e5edf7;
  overflow: hidden;
}

.canvas-frame {
  display: grid;
  grid-template-columns: 32px 1fr;
  grid-template-rows: 28px 1fr;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.canvas-frame.without-rulers {
  grid-template-columns: 1fr;
  grid-template-rows: 1fr;
}

.ruler-corner {
  display: grid;
  place-items: center;
  border-right: 1px solid #cbd5e1;
  border-bottom: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #64748b;
  font-size: 10px;
  font-weight: 800;
}

.top-ruler {
  width: 100%;
  height: 28px;
  border-bottom: 1px solid #cbd5e1;
  background: #f8fafc;
  cursor: ns-resize;
}

.left-ruler {
  width: 32px;
  height: 100%;
  border-right: 1px solid #cbd5e1;
  background: #f8fafc;
  cursor: ew-resize;
}

.canvas-scroll {
  min-width: 0;
  min-height: 0;
  overflow: auto;
  background: #dbeafe;
}

.editor-canvas {
  width: 100%;
  height: 100%;
  min-width: 900px;
  min-height: 520px;
  display: block;
  background: white;
  cursor: crosshair;
}

.busbar-object {
  cursor: move;
}

.busbar-object.selected .busbar {
  stroke: #2563eb;
  stroke-width: 3;
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
  pointer-events: none;
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

.user-guide-line {
  stroke: #0ea5e9;
  stroke-width: 1.2;
  stroke-dasharray: 8 5;
  cursor: move;
  pointer-events: stroke;
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
  padding: 12px;
  overflow: hidden;
}

.properties-panel h2,
.properties-panel h3 {
  margin: 0 0 10px;
  font-size: 14px;
}

.properties-panel label {
  display: grid;
  gap: 4px;
  margin-bottom: 8px;
  color: #475569;
  font-size: 12px;
  font-weight: 800;
}

.properties-panel input {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 6px 8px;
}

.properties-panel p,
.settings-summary {
  color: #475569;
  font-size: 12px;
  line-height: 1.4;
}

.properties-panel hr {
  border: 0;
  border-top: 1px solid #e2e8f0;
  margin: 12px 0;
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