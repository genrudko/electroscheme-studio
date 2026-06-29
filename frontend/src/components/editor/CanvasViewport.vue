<template>
  <div class="canvas-workspace" @pointerdown="hideContextMenu">
    <div class="canvas-frame" :class="{ 'without-rulers': !settings.rulersVisible }">
      <div v-if="settings.rulersVisible" class="ruler-corner">0,0</div>

      <svg
        v-if="settings.rulersVisible"
        ref="topRulerRef"
        class="top-ruler"
        :viewBox="topRulerViewBox"
        preserveAspectRatio="none"
        @pointerdown.prevent="onTopRulerPointerDown"
      >
        <rect :x="viewOrigin.x" y="0" :width="viewBoxWidth" height="24" fill="#f8fafc" />
        <g v-for="tick in rulerXTicks" :key="`x_${tick}`">
          <line
            :x1="tick"
            :x2="tick"
            y1="0"
            :y2="tick % majorGridStep === 0 ? 18 : 10"
            stroke="#94a3b8"
            stroke-width="1"
          />
          <text
            v-if="tick % majorGridStep === 0"
            :x="tick + 2"
            y="22"
            font-size="10"
            fill="#475569"
          >{{ tick }}</text>
        </g>
      </svg>

      <svg
        v-if="settings.rulersVisible"
        ref="leftRulerRef"
        class="left-ruler"
        :viewBox="leftRulerViewBox"
        preserveAspectRatio="none"
        @pointerdown.prevent="onLeftRulerPointerDown"
      >
        <rect x="0" :y="viewOrigin.y" width="28" :height="viewBoxHeight" fill="#f8fafc" />
        <g v-for="tick in rulerYTicks" :key="`y_${tick}`">
          <line
            x1="0"
            :x2="tick % majorGridStep === 0 ? 20 : 11"
            :y1="tick"
            :y2="tick"
            stroke="#94a3b8"
            stroke-width="1"
          />
          <text
            v-if="tick % majorGridStep === 0"
            x="3"
            :y="tick - 2"
            font-size="10"
            fill="#475569"
          >{{ tick }}</text>
        </g>
      </svg>

      <div class="canvas-scroll" @wheel.prevent="onWheelZoom">
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
            <filter id="page-shadow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.14" />
            </filter>
          </defs>

          <rect :x="viewOrigin.x" :y="viewOrigin.y" :width="viewBoxWidth" :height="viewBoxHeight" fill="#ffffff" />
          <rect
            v-if="settings.gridVisible"
            :x="viewOrigin.x"
            :y="viewOrigin.y"
            :width="viewBoxWidth"
            :height="viewBoxHeight"
            fill="url(#editor-grid-major)"
          />

          <g v-if="settings.pageVisible" class="iso-page-layer">
            <rect
              class="iso-page"
              :x="pageRect.x"
              :y="pageRect.y"
              :width="pageRect.width"
              :height="pageRect.height"
              rx="2"
            />
            <text
              class="iso-page-label"
              :x="pageRect.x + 8"
              :y="pageRect.y + 16"
            >{{ settings.pageFormat }} {{ settings.pageOrientation === 'landscape' ? 'альбомная' : 'книжная' }}</text>
          </g>

          <g v-if="settings.originVisible" class="origin-layer">
            <line x1="-24" y1="0" x2="24" y2="0" class="origin-line" />
            <line x1="0" y1="-24" x2="0" y2="24" class="origin-line" />
            <circle cx="0" cy="0" r="3" class="origin-dot" />
            <text x="8" y="-8" class="origin-label">0,0</text>
          </g>

          <g v-if="settings.guidesVisible" class="guide-object-layer">
            <line
              v-for="guide in verticalGuides"
              :key="guide.id"
              :x1="guide.position"
              :y1="viewOrigin.y"
              :x2="guide.position"
              :y2="viewOrigin.y + viewBoxHeight"
              class="user-guide-line"
              @pointerdown.stop="onGuidePointerDown($event, guide.id)"
            />
            <line
              v-for="guide in horizontalGuides"
              :key="guide.id"
              :x1="viewOrigin.x"
              :y1="guide.position"
              :x2="viewOrigin.x + viewBoxWidth"
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
              :class="{ selected: isSelected('busbar', busbar.id) }"
              :data-busbar-id="busbar.id"
              @pointerdown.stop="onBusbarPointerDown($event, busbar.id)"
            >
              <rect
                class="busbar"
                :style="{ fill: voltageColor(busbar.voltageKv) }"
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
              :class="{ selected: isSelected('text', object.id) }"
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
            <line :x1="activeGuidePoint.x" :y1="viewOrigin.y" :x2="activeGuidePoint.x" :y2="viewOrigin.y + viewBoxHeight" class="guide-line" />
            <line :x1="viewOrigin.x" :y1="activeGuidePoint.y" :x2="viewOrigin.x + viewBoxWidth" :y2="activeGuidePoint.y" class="guide-line" />
          </g>

          <g v-if="busbars.length === 0 && textObjects.length === 0" class="empty-canvas-hint">
            <text x="0" y="-20" text-anchor="middle" dominant-baseline="middle">Пустой канвас</text>
            <text x="0" y="10" text-anchor="middle" dominant-baseline="middle" class="hint-small">
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
      :has-selection="selectedElements.length > 0"
      :can-paste="Boolean(referenceClipboard)"
      @command="onContextCommand"
    />

    <aside class="properties-panel">
      <template v-if="selectedBusbar && selectedElements.length === 1">
        <h2>Свойства шины</h2>
        <label>X <input v-model.number="selectedBusbar.x" type="number" step="1" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <label>Y <input v-model.number="selectedBusbar.y" type="number" step="1" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <label>Класс напряжения
          <select v-model.number="selectedBusbar.voltageKv" @change="syncBusbarLabels(selectedBusbar)">
            <option :value="0.4">0,4 кВ</option>
            <option :value="6">6 кВ</option>
            <option :value="10">10 кВ</option>
            <option :value="35">35 кВ</option>
            <option :value="110">110 кВ</option>
            <option :value="220">220 кВ</option>
          </select>
        </label>
        <label>Толщина <input v-model.number="selectedBusbar.height" type="number" min="4" step="1" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <label>Ячеек <input v-model.number="selectedBusbar.slots" type="number" min="1" max="40" step="1" @change="normalizeBusbarSlots(selectedBusbar)" /></label>
        <label>Шаг ячеек <input v-model.number="selectedBusbar.slotSpacing" type="number" min="8" step="1" @change="normalizeBusbarSlots(selectedBusbar)" /></label>
        <label>Подпись <input v-model="selectedBusbar.label" type="text" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <div class="button-pair">
          <button type="button" class="panel-button" @click="addBusbarSlot(selectedBusbar)">+ Ячейка</button>
          <button type="button" class="panel-button" @click="removeBusbarSlot(selectedBusbar)">− Ячейка</button>
        </div>
      </template>

      <template v-else-if="selectedText && selectedElements.length === 1">
        <h2>Свойства текста</h2>
        <label>Текст <input v-model="selectedText.text" type="text" /></label>
        <label>X <input v-model.number="selectedText.anchor.x" type="number" step="1" /></label>
        <label>Y <input v-model.number="selectedText.anchor.y" type="number" step="1" /></label>
        <label>Поворот <input v-model.number="selectedText.rotationDeg" type="number" step="90" /></label>
      </template>

      <template v-else-if="selectedElements.length > 1">
        <h2>Мультивыбор</h2>
        <p>Выбрано объектов: {{ selectedElements.length }}. Перетаскивание одного из выбранных объектов перемещает всю группу.</p>
      </template>

      <template v-else>
        <h2>Свойства</h2>
        <p>Выберите объект на канвасе. Shift+клик — мультивыбор.</p>
        <button type="button" class="panel-button" @click="createSampleBusbar">Добавить шину</button>
        <button type="button" class="panel-button" @click="createTextObject">Добавить текст</button>
      </template>

      <hr />

      <h3>Канвас</h3>
      <p class="settings-summary">
        Масштаб: {{ Math.round(settings.zoom * 100) }}%<br />
        Лист: {{ settings.pageFormat }}, {{ settings.pageOrientation === 'landscape' ? 'альбомная' : 'книжная' }}<br />
        Сетка: {{ settings.gridVisible ? 'вкл' : 'выкл' }}, шаг {{ settings.gridStep }}<br />
        Линейки: {{ settings.rulersVisible ? 'вкл' : 'выкл' }}<br />
        Направляющих: {{ guides.length }}<br />
        Начало вида: {{ Math.round(viewOrigin.x) }}, {{ Math.round(viewOrigin.y) }}
      </p>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import CanvasContextMenu from './CanvasContextMenu.vue'
import { isoPageSizes, normalizeCanvasSettings, type CanvasSettings } from '../../lib/editor/canvasSettings'
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
  voltageKv: number
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
const topRulerRef = ref<SVGSVGElement | null>(null)
const leftRulerRef = ref<SVGSVGElement | null>(null)

const viewOrigin = reactive<Point>({ x: -450, y: -260 })
const selectedElements = ref<SelectedElement[]>([])
const virtualPoint = ref<Point | null>(null)
const activeGuidePoint = ref<Point | null>(null)
const referenceClipboard = ref<ReferenceClipboardPayload | null>(null)
const copyBaseSelection = ref<CanvasTextObject | null>(null)
const message = ref('Бесконечный редактор готов. Начало координат отмечено в центре.')
const contextMenu = reactive({ visible: false, x: 0, y: 0, point: { x: 0, y: 0 } as Point })

const busbars = ref<BusbarObject[]>([])
const textObjects = ref<CanvasTextObject[]>([])
const guides = ref<CanvasGuide[]>([])

const viewportPixelWidth = 900
const viewportPixelHeight = 520
const majorGridStep = computed(() => props.settings.gridStep * 5)
const viewBoxWidth = computed(() => viewportPixelWidth / props.settings.zoom)
const viewBoxHeight = computed(() => viewportPixelHeight / props.settings.zoom)
const canvasViewBox = computed(() => `${viewOrigin.x} ${viewOrigin.y} ${viewBoxWidth.value} ${viewBoxHeight.value}`)
const topRulerViewBox = computed(() => `${viewOrigin.x} 0 ${viewBoxWidth.value} 24`)
const leftRulerViewBox = computed(() => `0 ${viewOrigin.y} 28 ${viewBoxHeight.value}`)
const showVirtualPoint = computed(() => props.activeMode === 'copy_by_reference' || props.activeMode === 'paste_by_point' || props.activeMode === 'create_guide')
const rulerXTicks = computed(() => createTicks(viewOrigin.x, viewOrigin.x + viewBoxWidth.value, props.settings.gridStep))
const rulerYTicks = computed(() => createTicks(viewOrigin.y, viewOrigin.y + viewBoxHeight.value, props.settings.gridStep))
const verticalGuides = computed(() => guides.value.filter((guide) => guide.orientation === 'vertical'))
const horizontalGuides = computed(() => guides.value.filter((guide) => guide.orientation === 'horizontal'))

const pageSize = computed(() => {
  const base = isoPageSizes[props.settings.pageFormat]
  if (props.settings.pageOrientation === 'landscape') {
    return { width: Math.max(base.width, base.height), height: Math.min(base.width, base.height) }
  }
  return { width: Math.min(base.width, base.height), height: Math.max(base.width, base.height) }
})

const pageRect = computed(() => ({
  x: -pageSize.value.width / 2,
  y: -pageSize.value.height / 2,
  width: pageSize.value.width,
  height: pageSize.value.height,
}))

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
  if (selectedElements.value.length !== 1 || selectedElements.value[0].kind !== 'text') return null
  return textObjects.value.find((object) => object.id === selectedElements.value[0].id) ?? null
})

const selectedBusbar = computed(() => {
  if (selectedElements.value.length !== 1 || selectedElements.value[0].kind !== 'busbar') return null
  return busbars.value.find((object) => object.id === selectedElements.value[0].id) ?? null
})

const selectedObjectName = computed(() => {
  if (selectedElements.value.length > 1) return `${selectedElements.value.length} объектов`
  return selectedText.value?.text ?? selectedBusbar.value?.label ?? ''
})

const snapCandidates = computed<SnapCandidate[]>(() => {
  const candidates: SnapCandidate[] = [{ x: 0, y: 0, kind: 'origin', label: 'Начало координат' }]

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

  if (props.settings.snapGuides && virtualPoint.value) {
    for (const guide of guides.value) {
      if (guide.orientation === 'vertical') {
        candidates.push({ x: guide.position, y: virtualPoint.value.y, kind: 'guide', label: `X ${guide.position}` })
      } else {
        candidates.push({ x: virtualPoint.value.x, y: guide.position, kind: 'guide', label: `Y ${guide.position}` })
      }
    }
  }

  return candidates
})

const ghostText = computed<CanvasTextObject | null>(() => {
  if (props.activeMode !== 'paste_by_point' || !referenceClipboard.value || !virtualPoint.value) return null
  return placeItemAtReferencePoint(referenceClipboard.value.items[0], referenceClipboard.value, virtualPoint.value) as CanvasTextObject
})

function elementKey(kind: SelectedElement['kind'], id: string): string {
  return `${kind}:${id}`
}

function isSelected(kind: SelectedElement['kind'], id: string): boolean {
  return selectedElements.value.some((item) => elementKey(item.kind, item.id) === elementKey(kind, id))
}

function selectSingle(kind: SelectedElement['kind'], id: string): void {
  selectedElements.value = [{ kind, id }]
}

function toggleSelection(kind: SelectedElement['kind'], id: string): void {
  const key = elementKey(kind, id)
  if (selectedElements.value.some((item) => elementKey(item.kind, item.id) === key)) {
    selectedElements.value = selectedElements.value.filter((item) => elementKey(item.kind, item.id) !== key)
  } else {
    selectedElements.value = [...selectedElements.value, { kind, id }]
  }
}

function createTicks(from: number, to: number, step: number): number[] {
  const first = Math.floor(from / step) * step
  const ticks: number[] = []
  for (let value = first; value <= to + step; value += step) ticks.push(value)
  return ticks
}

function pointFromSvg(svg: SVGSVGElement | null, event: PointerEvent | MouseEvent): Point | null {
  if (!svg) return null
  const point = svg.createSVGPoint()
  point.x = event.clientX
  point.y = event.clientY
  const ctm = svg.getScreenCTM()
  if (!ctm) return null
  const transformed = point.matrixTransform(ctm.inverse())
  return { x: transformed.x, y: transformed.y }
}

function svgPointFromPointer(event: PointerEvent | MouseEvent): Point | null {
  return pointFromSvg(svgRef.value, event)
}

function topRulerPointFromPointer(event: PointerEvent): Point | null {
  const point = pointFromSvg(topRulerRef.value, event)
  return point ? { x: point.x, y: 0 } : null
}

function leftRulerPointFromPointer(event: PointerEvent): Point | null {
  const point = pointFromSvg(leftRulerRef.value, event)
  return point ? { x: 0, y: point.y } : null
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

function voltageColor(voltageKv: number): string {
  if (voltageKv >= 220) return '#dc2626'
  if (voltageKv >= 110) return '#f97316'
  if (voltageKv >= 35) return '#0ea5e9'
  if (voltageKv >= 10) return '#6d0ad6'
  if (voltageKv >= 6) return '#16a34a'
  return '#64748b'
}

function autoBusbarWidth(busbar: BusbarObject): number {
  return 24 + Math.max(0, busbar.slots - 1) * busbar.slotSpacing
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
  const slots = 8
  const busbar: BusbarObject = {
    id: `busbar_${nextIndex}`,
    x: -180,
    y: -12 + (nextIndex - 1) * 80,
    width: 0,
    height: 20,
    slots,
    slotSpacing: 48,
    labelStart: 1,
    label: `${nextIndex}С 10 кВ`,
    voltageKv: 10,
  }
  busbar.width = autoBusbarWidth(busbar)
  busbars.value.push(busbar)
  ensureBusbarLabels(busbar)
  selectSingle('busbar', busbar.id)
  message.value = 'Шина добавлена как редактируемый объект с классом напряжения.'
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

function normalizeBusbarSlots(busbar: BusbarObject | null): void {
  if (!busbar) return
  busbar.slots = Math.max(1, Math.min(40, Math.round(busbar.slots)))
  busbar.slotSpacing = Math.max(8, busbar.slotSpacing)
  busbar.width = autoBusbarWidth(busbar)
  syncBusbarLabels(busbar)
}

function syncBusbarLabels(busbar: BusbarObject | null): void {
  if (!busbar) return
  busbar.height = Math.max(4, busbar.height)
  busbar.width = autoBusbarWidth(busbar)
  ensureBusbarLabels(busbar)
  message.value = `Параметры шины обновлены: ${busbar.label}.`
  setStatus(virtualPoint.value, 'object', busbar.label)
}

function addBusbarSlot(busbar: BusbarObject | null = selectedBusbar.value): void {
  if (!busbar) return
  busbar.slots += 1
  normalizeBusbarSlots(busbar)
}

function removeBusbarSlot(busbar: BusbarObject | null = selectedBusbar.value): void {
  if (!busbar) return
  busbar.slots = Math.max(1, busbar.slots - 1)
  normalizeBusbarSlots(busbar)
}

function createTextObject(): void {
  const point = virtualPoint.value ?? { x: 0, y: 0 }
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

  selectSingle('text', id)
  message.value = 'Текст добавлен на канвас.'
  setStatus({ x: snapped.x, y: snapped.y }, snapped.kind, snapped.label)
}

function copySelectedFromCenter(): void {
  if (!selectedText.value) {
    message.value = 'Сейчас копирование работает для текста. Выберите один текстовый объект.'
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
    message.value = 'Сейчас копирование с базовой точкой работает для одного текста. Выберите текстовый объект.'
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

  selectSingle('text', id)
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
  const selection = [...selectedElements.value]
  for (const selected of selection) {
    if (selected.kind === 'text') {
      textObjects.value = textObjects.value.filter((object) => object.id !== selected.id)
    } else {
      busbars.value = busbars.value.filter((object) => object.id !== selected.id)
      textObjects.value = textObjects.value.filter((object) => object.busbarId !== selected.id)
    }
  }
  selectedElements.value = []
  message.value = 'Выбранные объекты удалены.'
  setStatus(virtualPoint.value, null, '')
}

function clearGenerated(): void {
  textObjects.value = textObjects.value.filter((object) => !object.generated)
  selectedElements.value = []
  message.value = 'Вставленные копии очищены.'
  setStatus(virtualPoint.value, null, '')
}

function createGuide(orientation: 'vertical' | 'horizontal', position?: number): CanvasGuide {
  const fallback = orientation === 'vertical'
    ? viewOrigin.x + viewBoxWidth.value / 2
    : viewOrigin.y + viewBoxHeight.value / 2
  const raw = position ?? fallback
  const snapped = Math.round(raw / props.settings.gridStep) * props.settings.gridStep
  const guide = {
    id: `guide_${orientation}_${guides.value.length + 1}`,
    orientation,
    position: snapped,
  }
  guides.value.push(guide)
  message.value = orientation === 'vertical'
    ? `Добавлена вертикальная направляющая X=${snapped}.`
    : `Добавлена горизонтальная направляющая Y=${snapped}.`
  setStatus(virtualPoint.value, 'guide', message.value)
  return guide
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
    viewOrigin.x = -viewBoxWidth.value / 2
    viewOrigin.y = -viewBoxHeight.value / 2
    setZoom(1)
  }
  else if (command === 'add_busbar_slot') addBusbarSlot()
  else if (command === 'remove_busbar_slot') removeBusbarSlot()
  emit('commandHandled')
}

function onPointerMove(event: PointerEvent): void {
  updateVirtualPointFromEvent(event)
}

function onCanvasPointerDown(event: PointerEvent): void {
  if (event.button === 1 || props.activeMode === 'pan') {
    startCanvasPan(event)
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

  if (!event.shiftKey) selectedElements.value = []
  message.value = 'Канвас выбран.'
  setStatus(point, 'grid', 'Канвас')
}

function onObjectPointerDown(event: PointerEvent, objectId: string): void {
  if (event.shiftKey) toggleSelection('text', objectId)
  else if (!isSelected('text', objectId)) selectSingle('text', objectId)
  startSelectionDrag(event, { kind: 'text', id: objectId })
}

function onBusbarPointerDown(event: PointerEvent, busbarId: string): void {
  if (event.shiftKey) toggleSelection('busbar', busbarId)
  else if (!isSelected('busbar', busbarId)) selectSingle('busbar', busbarId)
  startSelectionDrag(event, { kind: 'busbar', id: busbarId })
}

function startSelectionDrag(event: PointerEvent, dragged: SelectedElement): void {
  if (props.activeMode !== 'select') {
    message.value = 'Объект выбран. Для перетаскивания включите режим «Выбор».'
    setStatus(virtualPoint.value, 'object', selectedObjectName.value)
    return
  }

  if (!isSelected(dragged.kind, dragged.id)) selectedElements.value = [dragged]

  const startPoint = svgPointFromPointer(event)
  if (!startPoint) return

  const selection = selectedElements.value.length ? [...selectedElements.value] : [dragged]
  const baselines = selection.map((selected) => {
    if (selected.kind === 'busbar') {
      const busbar = busbars.value.find((item) => item.id === selected.id)
      return busbar ? { selected, x: busbar.x, y: busbar.y } : null
    }
    const text = textObjects.value.find((item) => item.id === selected.id)
    return text ? { selected, x: text.center.x, y: text.center.y, anchorX: text.anchor.x, anchorY: text.anchor.y } : null
  }).filter((item): item is NonNullable<typeof item> => item !== null)

  const primary = baselines.find((item) => item.selected.kind === dragged.kind && item.selected.id === dragged.id) ?? baselines[0]
  const pointerId = event.pointerId
  ;(event.currentTarget as Element).setPointerCapture?.(pointerId)

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    const current = svgPointFromPointer(moveEvent)
    if (!current) return

    const rawPrimary = {
      x: primary.x + current.x - startPoint.x,
      y: primary.y + current.y - startPoint.y,
    }
    const snapped = snapCanvasPoint(rawPrimary)
    const dx = snapped.x - primary.x
    const dy = snapped.y - primary.y

    for (const base of baselines) {
      if (base.selected.kind === 'busbar') {
        const busbar = busbars.value.find((item) => item.id === base.selected.id)
        if (!busbar) continue
        busbar.x = base.x + dx
        busbar.y = base.y + dy
        ensureBusbarLabels(busbar)
      } else {
        const text = textObjects.value.find((item) => item.id === base.selected.id)
        if (!text) continue
        text.center = { x: base.x + dx, y: base.y + dy }
        text.anchor = { x: (base.anchorX ?? base.x) + dx, y: (base.anchorY ?? base.y) + dy }
      }
    }

    virtualPoint.value = { x: snapped.x, y: snapped.y }
    activeGuidePoint.value = { x: snapped.x, y: snapped.y }
    message.value = selection.length > 1 ? `Групповое перемещение: ${selection.length} объектов.` : 'Перемещение объекта.'
    setStatus(virtualPoint.value, snapped.kind, snapped.label)
  }

  const up = (upEvent: PointerEvent) => {
    if (upEvent.pointerId !== pointerId) return
    window.removeEventListener('pointermove', move)
    window.removeEventListener('pointerup', up)
    message.value = selection.length > 1 ? `Группа размещена: ${selection.length} объектов.` : 'Объект размещён.'
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
  const point = topRulerPointFromPointer(event)
  if (!point) return
  const guide = createGuide('vertical', point.x)
  onGuidePointerDown(event, guide.id)
}

function onLeftRulerPointerDown(event: PointerEvent): void {
  const point = leftRulerPointFromPointer(event)
  if (!point) return
  const guide = createGuide('horizontal', point.y)
  onGuidePointerDown(event, guide.id)
}

function startCanvasPan(event: PointerEvent): void {
  event.preventDefault()
  const start = { x: event.clientX, y: event.clientY }
  const startOrigin = { ...viewOrigin }
  const pointerId = event.pointerId
  svgRef.value?.setPointerCapture?.(pointerId)

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    viewOrigin.x = startOrigin.x + (start.x - moveEvent.clientX) / props.settings.zoom
    viewOrigin.y = startOrigin.y + (start.y - moveEvent.clientY) / props.settings.zoom
    message.value = 'Панорамирование канваса.'
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
  const cursor = svgPointFromPointer(event)
  const svg = svgRef.value
  if (!cursor || !svg) return

  const rect = svg.getBoundingClientRect()
  const fx = (event.clientX - rect.left) / rect.width
  const fy = (event.clientY - rect.top) / rect.height
  const factor = event.deltaY < 0 ? 1.08 : 0.92
  const nextZoom = Math.min(Math.max(props.settings.zoom * factor, 0.2), 6)
  const nextWidth = viewportPixelWidth / nextZoom
  const nextHeight = viewportPixelHeight / nextZoom

  viewOrigin.x = cursor.x - nextWidth * fx
  viewOrigin.y = cursor.y - nextHeight * fy
  emit('settingsChange', normalizeCanvasSettings({ ...props.settings, zoom: nextZoom }))
  message.value = `Масштаб: ${Math.round(nextZoom * 100)}%.`
  setStatus(cursor, null, '')
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
    selectSingle('text', targetText.getAttribute('data-object-id') ?? '')
  } else if (targetBusbar) {
    const busbarId = targetBusbar.getAttribute('data-busbar-id')
    if (busbarId) selectSingle('busbar', busbarId)
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
  overflow: hidden;
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

.iso-page {
  fill: rgba(255, 255, 255, 0.72);
  stroke: #94a3b8;
  stroke-width: 1.2;
  filter: url(#page-shadow);
}

.iso-page-label {
  fill: #64748b;
  font-family: Arial, sans-serif;
  font-size: 10px;
  pointer-events: none;
}

.origin-line {
  stroke: #ef4444;
  stroke-width: 1;
  opacity: 0.48;
  stroke-dasharray: 5 5;
}

.origin-dot {
  fill: #ef4444;
  opacity: 0.55;
}

.origin-label {
  fill: #ef4444;
  font-size: 11px;
  font-family: Arial, sans-serif;
  opacity: 0.70;
}

.busbar-object {
  cursor: move;
}

.busbar-object.selected .busbar {
  stroke: #2563eb;
  stroke-width: 3;
}

.busbar {
  stroke: #111827;
  stroke-width: 1;
}

.bay-slot {
  fill: #ffffff;
  stroke: #111827;
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
  stroke-width: 1.4;
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

.properties-panel input,
.properties-panel select {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 6px 8px;
  background: white;
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

.button-pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
</style>