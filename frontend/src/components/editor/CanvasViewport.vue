<template>
  <div class="canvas-workspace" @pointerdown="hideContextMenu">
    <div class="canvas-frame" :class="{ 'without-rulers': !settings.rulersVisible }">
      <div v-if="settings.rulersVisible" class="ruler-corner">0,0</div>

      <div v-if="settings.rulersVisible" ref="topRulerRef" class="top-ruler" @pointerdown.prevent="onTopRulerPointerDown">
        <template v-for="tick in topRulerTicks" :key="`top_${tick.value}`">
          <span class="ruler-tick top" :class="{ major: tick.major }" :style="{ left: `${tick.screen}px` }"></span>
          <span v-if="tick.major" class="ruler-label top" :style="{ left: `${tick.screen + 3}px` }">{{ tick.value }}</span>
        </template>
      </div>

      <div v-if="settings.rulersVisible" ref="leftRulerRef" class="left-ruler" @pointerdown.prevent="onLeftRulerPointerDown">
        <template v-for="tick in leftRulerTicks" :key="`left_${tick.value}`">
          <span class="ruler-tick left" :class="{ major: tick.major }" :style="{ top: `${tick.screen}px` }"></span>
          <span v-if="tick.major" class="ruler-label left" :style="{ top: `${tick.screen + 2}px` }">{{ tick.value }}</span>
        </template>
      </div>

      <div ref="canvasSurfaceRef" class="canvas-surface" @wheel.prevent="onWheelZoom">
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
              <path :d="`M ${settings.gridStep} 0 L 0 0 0 ${settings.gridStep}`" fill="none" stroke="#e5e7eb" stroke-width="0.6" />
            </pattern>
            <pattern id="editor-grid-major" :width="majorGridStep" :height="majorGridStep" patternUnits="userSpaceOnUse">
              <rect :width="majorGridStep" :height="majorGridStep" fill="url(#editor-grid)" />
              <path :d="`M ${majorGridStep} 0 L 0 0 0 ${majorGridStep}`" fill="none" stroke="#cbd5e1" stroke-width="0.75" />
            </pattern>
          </defs>

          <rect :x="viewOrigin.x" :y="viewOrigin.y" :width="viewBoxWidth" :height="viewBoxHeight" fill="#ffffff" />
          <rect v-if="settings.gridVisible" :x="viewOrigin.x" :y="viewOrigin.y" :width="viewBoxWidth" :height="viewBoxHeight" fill="url(#editor-grid-major)" />

          <g v-if="settings.pageVisible" class="iso-page-layer">
            <rect class="iso-page" :x="pageRect.x" :y="pageRect.y" :width="pageRect.width" :height="pageRect.height" rx="1" />
            <text class="iso-page-label" :x="pageRect.x + 8" :y="pageRect.y + 16">{{ settings.pageFormat }} {{ settings.pageOrientation === 'landscape' ? 'альбомная' : 'книжная' }}</text>
          </g>

          <g v-if="settings.originVisible" class="origin-layer">
            <line x1="-10" y1="0" x2="10" y2="0" class="origin-line" />
            <line x1="0" y1="-10" x2="0" y2="10" class="origin-line" />
            <circle cx="0" cy="0" r="1.2" class="origin-dot" />
            <text x="4" y="-4" class="origin-label">0,0</text>
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
              v-for="primitive in primitiveObjects"
              :key="primitive.id"
              class="primitive-object"
              :class="{ selected: isSelected('primitive', primitive.id) }"
              :data-primitive-id="primitive.id"
              @pointerdown.stop="onPrimitivePointerDown($event, primitive.id)"
            >
              <rect
                v-if="primitive.kind === 'rectangle'"
                :x="primitive.x"
                :y="primitive.y"
                :width="primitive.width"
                :height="primitive.height"
                :fill="primitive.fill"
                :stroke="primitive.stroke"
                :stroke-width="primitive.strokeWidth"
              />
              <ellipse
                v-else-if="primitive.kind === 'ellipse'"
                :cx="primitive.x + primitive.width / 2"
                :cy="primitive.y + primitive.height / 2"
                :rx="Math.abs(primitive.width / 2)"
                :ry="Math.abs(primitive.height / 2)"
                :fill="primitive.fill"
                :stroke="primitive.stroke"
                :stroke-width="primitive.strokeWidth"
              />
              <line
                v-else
                :x1="primitive.x"
                :y1="primitive.y"
                :x2="primitive.x + primitive.width"
                :y2="primitive.y + primitive.height"
                :stroke="primitive.stroke"
                :stroke-width="primitive.strokeWidth"
              />
            </g>

            <g
              v-for="busbar in busbars"
              :key="busbar.id"
              class="busbar-object"
              :class="{ selected: isSelected('busbar', busbar.id) }"
              :data-busbar-id="busbar.id"
              @pointerdown.stop="onBusbarPointerDown($event, busbar.id)"
            >
              <rect class="busbar" :style="{ fill: voltageColorById(busbar.voltageClassId) }" :x="busbar.x" :y="busbar.y" :width="busbar.width" :height="busbar.height" rx="1" />
            </g>

            <circle v-for="slot in baySlots" :key="slot.id" class="bay-slot" :cx="slot.x" :cy="slot.y" r="5" :data-slot-id="slot.id" />

            <text
              v-for="object in textObjects"
              :key="object.id"
              class="canvas-text"
              :class="{ selected: isSelected('text', object.id) }"
              :x="object.anchor.x"
              :y="object.anchor.y"
              :font-size="object.fontSize"
              :font-family="object.fontFamily"
              :font-weight="object.bold ? '700' : '400'"
              :font-style="object.italic ? 'italic' : 'normal'"
              :fill="object.fill"
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
            <text class="ghost-text" :x="ghostText.anchor.x" :y="ghostText.anchor.y" :font-size="ghostText.fontSize" :transform="`rotate(${ghostText.rotationDeg} ${ghostText.anchor.x} ${ghostText.anchor.y})`" dominant-baseline="middle" text-anchor="middle">
              {{ ghostText.text }}
            </text>
          </g>

          <g v-if="virtualPoint && showVirtualPoint" class="virtual-point-layer">
            <line :x1="virtualPoint.x - 6" :y1="virtualPoint.y" :x2="virtualPoint.x + 6" :y2="virtualPoint.y" class="virtual-point-line" />
            <line :x1="virtualPoint.x" :y1="virtualPoint.y - 6" :x2="virtualPoint.x" :y2="virtualPoint.y + 6" class="virtual-point-line" />
            <circle :cx="virtualPoint.x" :cy="virtualPoint.y" r="2.5" class="virtual-point-ring" />
          </g>

          <g v-if="settings.guidesVisible && activeGuidePoint" class="guide-layer">
            <line :x1="activeGuidePoint.x" :y1="viewOrigin.y" :x2="activeGuidePoint.x" :y2="viewOrigin.y + viewBoxHeight" class="guide-line" />
            <line :x1="viewOrigin.x" :y1="activeGuidePoint.y" :x2="viewOrigin.x + viewBoxWidth" :y2="activeGuidePoint.y" class="guide-line" />
          </g>

          <rect
            v-if="marqueeRect"
            class="selection-marquee"
            :x="marqueeRect.x"
            :y="marqueeRect.y"
            :width="marqueeRect.width"
            :height="marqueeRect.height"
          />

          <g v-if="busbars.length === 0 && textObjects.length === 0 && primitiveObjects.length === 0" class="empty-canvas-hint">
            
            <text x="0" y="10" text-anchor="middle" dominant-baseline="middle" class="hint-small">Добавьте объект через ленту либо ПКМ-меню</text>
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
          <select v-model="selectedBusbar.voltageClassId" @change="syncBusbarLabels(selectedBusbar)">
            <option v-for="item in voltageClassColors" :key="item.id" :value="item.id">{{ item.label }} — {{ item.colorName }}</option>
          </select>
        </label>
        <label>Ячеек <input v-model.number="selectedBusbar.slots" type="number" min="1" max="40" step="1" @change="normalizeBusbarSlots(selectedBusbar)" /></label>
        <label>Шаг ячеек <input v-model.number="selectedBusbar.slotSpacing" type="number" min="8" step="1" @change="normalizeBusbarSlots(selectedBusbar)" /></label>
        <label>Подпись <input v-model="selectedBusbar.label" type="text" @change="syncBusbarLabels(selectedBusbar)" /></label>
        <div class="button-pair">
          <button type="button" class="panel-button" @click="addBusbarSlot(selectedBusbar)">+ Ячейка</button>
          <button type="button" class="panel-button" @click="removeBusbarSlot(selectedBusbar)">− Ячейка</button>
        </div>
      </template>

      <template v-else-if="selectedSymbol && selectedElements.length === 1">
        <h2>Свойства символа</h2>
        <label>Наименование <input v-model="selectedSymbol.label" type="text" /></label>
        <label>X <input v-model.number="selectedSymbol.x" type="number" step="1" @change="attachSymbolToNearestSlot(selectedSymbol, 48)" /></label>
        <label>Y <input v-model.number="selectedSymbol.y" type="number" step="1" @change="attachSymbolToNearestSlot(selectedSymbol, 48)" /></label>
        <label>Класс напряжения
          <select v-model="selectedSymbol.voltageClassId">
            <option v-for="item in voltageClassColors" :key="item.id" :value="item.id">{{ item.label }} — {{ item.colorName }}</option>
          </select>
        </label>
        <p class="settings-summary">Нижняя точка: {{ selectedSymbol.attachedSlotId ? `привязана к ${selectedSymbol.attachedSlotId}` : 'не привязана' }}</p>
      </template>

      <template v-else-if="selectedPrimitive && selectedElements.length === 1">
        <h2>Свойства примитива</h2>
        <label>X <input v-model.number="selectedPrimitive.x" type="number" step="1" /></label>
        <label>Y <input v-model.number="selectedPrimitive.y" type="number" step="1" /></label>
        <label>Ширина / X2 <input v-model.number="selectedPrimitive.width" type="number" step="1" /></label>
        <label>Высота / Y2 <input v-model.number="selectedPrimitive.height" type="number" step="1" /></label>
        <label>Линия <input v-model="selectedPrimitive.stroke" type="color" /></label>
        <label>Заливка <input v-model="selectedPrimitive.fill" type="color" /></label>
        <label>Толщина линии <input v-model.number="selectedPrimitive.strokeWidth" type="number" min="0.2" step="0.2" /></label>
      </template>

      <template v-else-if="selectedText && selectedElements.length === 1">
        <h2>Свойства текста</h2>
        <label>Текст <input v-model="selectedText.text" type="text" /></label>
        <label>Размер <input v-model.number="selectedText.fontSize" type="number" min="4" step="1" /></label>
        <label>Цвет <input v-model="selectedText.fill" type="color" /></label>
      </template>

      <template v-else>
        <h2>Свойства</h2>
        <p>Выберите объект на канвасе. Ctrl+клик — мультивыбор. Добавление фигур выполняется через библиотеку слева, ленту или ПКМ-меню.</p>
      </template>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import CanvasContextMenu from './CanvasContextMenu.vue'
import { isoPageSizes, normalizeCanvasSettings, type CanvasSettings } from '../../lib/editor/canvasSettings'
import type { EditorCommand, EditorInteractionMode } from '../../lib/editor/interactionModes'
import { formatPoint, rectsIntersect, snapPoint, type Point, type SnapCandidate, type SnapKind } from '../../lib/editor/snapService'
import { createReferenceClipboard, placeItemAtReferencePoint, type ReferenceClipboardPayload, type TextClipboardItem } from '../../lib/editor/referenceClipboard'
import { voltageClassColors, voltageColorById, voltageKvById, type VoltageClassId } from '../../lib/editor/voltageClasses'

type TextObjectRole = 'bay-label' | 'bus-label' | 'free-text-box'
type PrimitiveKind = 'rectangle' | 'ellipse' | 'line'

type CanvasTextObject = {
  id: string
  text: string
  anchor: Point
  center: Point
  rotationDeg: number
  fontSize: number
  fontFamily: string
  fill: string
  bold: boolean
  italic: boolean
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
  voltageClassId: VoltageClassId
}

type PrimitiveObject = {
  id: string
  kind: PrimitiveKind
  x: number
  y: number
  width: number
  height: number
  stroke: string
  fill: string
  strokeWidth: number
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
  | { kind: 'primitive'; id: string }

type WorldRect = { x: number; y: number; width: number; height: number }
type RulerTick = { value: number; screen: number; major: boolean }

type DragBaseline = {
  selected: SelectedElement
  x: number
  y: number
  anchorX?: number
  anchorY?: number
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
  settingsChange: [settings: CanvasSettings]
  commandHandled: []
}>()

const svgRef = ref<SVGSVGElement | null>(null)
const topRulerRef = ref<HTMLDivElement | null>(null)
const leftRulerRef = ref<HTMLDivElement | null>(null)
const canvasSurfaceRef = ref<HTMLDivElement | null>(null)

let resizeObserver: ResizeObserver | null = null

const viewOrigin = reactive<Point>({ x: -450, y: -260 })
const canvasPixels = reactive({ width: 900, height: 520 })
const selectedElements = ref<SelectedElement[]>([])
const virtualPoint = ref<Point | null>(null)
const activeGuidePoint = ref<Point | null>(null)
const referenceClipboard = ref<ReferenceClipboardPayload | null>(null)
const copyBaseSelection = ref<CanvasTextObject | null>(null)
const message = ref('Редактор готов. Линейки синхронизированы с сеткой, Ctrl+клик — мультивыбор.')
const contextMenu = reactive({ visible: false, x: 0, y: 0, point: { x: 0, y: 0 } as Point })
const marqueeRect = ref<WorldRect | null>(null)

const busbars = ref<BusbarObject[]>([])
const textObjects = ref<CanvasTextObject[]>([])
const primitiveObjects = ref<PrimitiveObject[]>([])
const guides = ref<CanvasGuide[]>([])

const majorGridStep = computed(() => props.settings.gridStep * 5)
const viewBoxWidth = computed(() => canvasPixels.width / props.settings.zoom)
const viewBoxHeight = computed(() => canvasPixels.height / props.settings.zoom)
const canvasViewBox = computed(() => `${viewOrigin.x} ${viewOrigin.y} ${viewBoxWidth.value} ${viewBoxHeight.value}`)
const showVirtualPoint = computed(() => props.activeMode === 'copy_by_reference' || props.activeMode === 'paste_by_point' || props.activeMode === 'create_guide')
const topRulerTicks = computed(() => createRulerTicks(viewOrigin.x, viewBoxWidth.value, props.settings.zoom, props.settings.gridStep, majorGridStep.value))
const leftRulerTicks = computed(() => createRulerTicks(viewOrigin.y, viewBoxHeight.value, props.settings.zoom, props.settings.gridStep, majorGridStep.value))
const verticalGuides = computed(() => guides.value.filter((guide) => guide.orientation === 'vertical'))
const horizontalGuides = computed(() => guides.value.filter((guide) => guide.orientation === 'horizontal'))

const pageSize = computed(() => {
  const base = isoPageSizes[props.settings.pageFormat]
  if (props.settings.pageOrientation === 'landscape') return { width: Math.max(base.width, base.height), height: Math.min(base.width, base.height) }
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
      slots.push({ id: `${busbar.id}_slot_${index + 1}`, busbarId: busbar.id, x: firstX + index * busbar.slotSpacing, y })
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

const selectedPrimitive = computed(() => {
  if (selectedElements.value.length !== 1 || selectedElements.value[0].kind !== 'primitive') return null
  return primitiveObjects.value.find((object) => object.id === selectedElements.value[0].id) ?? null
})

const selectedObjectName = computed(() => {
  if (selectedElements.value.length > 1) return `${selectedElements.value.length} объектов`
  return selectedText.value?.text ?? selectedBusbar.value?.label ?? selectedPrimitive.value?.kind ?? ''
})

const snapCandidates = computed<SnapCandidate[]>(() => {
  const candidates: SnapCandidate[] = [{ x: 0, y: 0, kind: 'origin', label: 'Начало координат' }]

  if (props.settings.snapSlots) {
    candidates.push(...baySlots.value.map((slot) => ({ x: slot.x, y: slot.y, kind: 'slot' as const, label: slot.id })))
  }

  if (props.settings.snapObjects) {
    candidates.push(...textObjects.value.map((object) => ({ x: object.center.x, y: object.center.y, kind: 'object' as const, label: object.text })))
    candidates.push(...busbars.value.map((busbar) => ({ x: busbar.x + busbar.width / 2, y: busbar.y + busbar.height / 2, kind: 'object' as const, label: busbar.label })))
    candidates.push(...primitiveObjects.value.map((primitive) => ({ x: primitive.x + primitive.width / 2, y: primitive.y + primitive.height / 2, kind: 'object' as const, label: primitive.kind })))
  }

  if (props.settings.snapGuides && virtualPoint.value) {
    for (const guide of guides.value) {
      if (guide.orientation === 'vertical') candidates.push({ x: guide.position, y: virtualPoint.value.y, kind: 'guide', label: `X ${guide.position}` })
      else candidates.push({ x: virtualPoint.value.x, y: guide.position, kind: 'guide', label: `Y ${guide.position}` })
    }
  }

  return candidates
})

const ghostText = computed<CanvasTextObject | null>(() => {
  if (props.activeMode !== 'paste_by_point' || !referenceClipboard.value || !virtualPoint.value) return null
  return placeItemAtReferencePoint(referenceClipboard.value.items[0], referenceClipboard.value, virtualPoint.value) as CanvasTextObject
})

onMounted(() => {
  if (!canvasSurfaceRef.value) return
  resizeObserver = new ResizeObserver((entries) => {
    const entry = entries[0]
    if (!entry) return
    canvasPixels.width = Math.max(320, entry.contentRect.width)
    canvasPixels.height = Math.max(240, entry.contentRect.height)
  })
  resizeObserver.observe(canvasSurfaceRef.value)
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
})

function createRulerTicks(origin: number, span: number, zoom: number, step: number, majorStep: number): RulerTick[] {
  const first = Math.floor(origin / step) * step
  const ticks: RulerTick[] = []
  for (let value = first; value <= origin + span + step; value += step) {
    const screen = (value - origin) * zoom
    ticks.push({ value, screen, major: Math.abs(value % majorStep) < 0.0001 })
  }
  return ticks
}

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

function worldPointFromCanvasClient(clientX: number, clientY: number): Point | null {
  const surface = canvasSurfaceRef.value
  if (!surface) return null
  const rect = surface.getBoundingClientRect()
  return {
    x: viewOrigin.x + (clientX - rect.left) / props.settings.zoom,
    y: viewOrigin.y + (clientY - rect.top) / props.settings.zoom,
  }
}

function worldPointFromTopRuler(event: PointerEvent): Point | null {
  const ruler = topRulerRef.value
  if (!ruler) return null
  const rect = ruler.getBoundingClientRect()
  return { x: viewOrigin.x + (event.clientX - rect.left) / props.settings.zoom, y: 0 }
}

function worldPointFromLeftRuler(event: PointerEvent): Point | null {
  const ruler = leftRulerRef.value
  if (!ruler) return null
  const rect = ruler.getBoundingClientRect()
  return { x: 0, y: viewOrigin.y + (event.clientY - rect.top) / props.settings.zoom }
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
  const point = worldPointFromCanvasClient(event.clientX, event.clientY)
  if (!point) return null
  const snapped = snapCanvasPoint(point)
  virtualPoint.value = { x: snapped.x, y: snapped.y }
  activeGuidePoint.value = { x: snapped.x, y: snapped.y }
  setStatus(virtualPoint.value, snapped.kind, snapped.label)
  return virtualPoint.value
}

function autoBusbarWidth(busbar: BusbarObject): number {
  return 24 + Math.max(0, busbar.slots - 1) * busbar.slotSpacing
}

function canvasObjectToClipboardItem(object: CanvasTextObject): TextClipboardItem {
  return { kind: 'text', text: object.text, sourceId: object.id, anchor: { ...object.anchor }, center: { ...object.center }, rotationDeg: object.rotationDeg, fontSize: object.fontSize, role: object.role }
}

function defaultTextStyle() {
  return { fontFamily: 'Arial', fill: '#111827', bold: false, italic: false }
}

function createSampleBusbar(): void {
  const nextIndex = busbars.value.length + 1
  const busbar: BusbarObject = {
    id: `busbar_${nextIndex}`,
    x: -180,
    y: -12 + (nextIndex - 1) * 80,
    width: 0,
    height: 20,
    slots: 8,
    slotSpacing: 48,
    labelStart: 1,
    label: `${nextIndex}С 10 кВ`,
    voltageKv: 10,
    voltageClassId: '10',
  }
  busbar.width = autoBusbarWidth(busbar)
  busbars.value.push(busbar)
  ensureBusbarLabels(busbar)
  selectSingle('busbar', busbar.id)
  message.value = 'Шина добавлена. Цвет берётся по кодификатору классов напряжения.'
  setStatus(virtualPoint.value, null, '')
}

function ensureBusbarLabels(busbar: BusbarObject): void {
  textObjects.value = textObjects.value.filter((object) => object.busbarId !== busbar.id)
  const style = defaultTextStyle()

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
      ...style,
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
    ...style,
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
  busbar.voltageKv = voltageKvById(busbar.voltageClassId)
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
    ...defaultTextStyle(),
  })
  selectSingle('text', id)
  message.value = 'Текст добавлен.'
  setStatus({ x: snapped.x, y: snapped.y }, snapped.kind, snapped.label)
}

function createPrimitive(kind: PrimitiveKind): void {
  const point = virtualPoint.value ?? { x: 0, y: 0 }
  const snapped = snapCanvasPoint(point)
  const id = `primitive_${primitiveObjects.value.length + 1}`
  primitiveObjects.value.push({
    id,
    kind,
    x: snapped.x,
    y: snapped.y,
    width: kind === 'line' ? 80 : 90,
    height: kind === 'line' ? 0 : 45,
    stroke: '#111827',
    fill: kind === 'line' ? 'none' : '#ffffff',
    strokeWidth: 1.2,
  })
  selectSingle('primitive', id)
  message.value = `Добавлен примитив: ${kind}.`
  setStatus({ x: snapped.x, y: snapped.y }, snapped.kind, snapped.label)
}

function copySelectedFromCenter(): void {
  if (!selectedText.value) {
    message.value = 'Сейчас копирование с базовой точкой работает для одного текста.'
    setStatus(virtualPoint.value, null, '')
    return
  }
  referenceClipboard.value = createReferenceClipboard([canvasObjectToClipboardItem(selectedText.value)], { ...selectedText.value.center })
  message.value = 'Скопировано от центра выбранного текста. Укажите точку вставки.'
  emit('modeChange', 'paste_by_point')
  setStatus(virtualPoint.value, 'object', selectedText.value.text)
}

function beginCopyByReference(): void {
  if (!selectedText.value) {
    message.value = 'Сейчас копирование с базовой точкой работает для одного текста.'
    setStatus(virtualPoint.value, null, '')
    return
  }
  copyBaseSelection.value = selectedText.value
  message.value = 'Укажите базовую точку. Она привязывается к сетке, объектам и направляющим.'
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
    ...defaultTextStyle(),
  })
  selectSingle('text', id)
  message.value = `Вставлено относительно базовой точки в ${formatPoint(point)}.`
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
    } else if (selected.kind === 'busbar') {
      busbars.value = busbars.value.filter((object) => object.id !== selected.id)
      textObjects.value = textObjects.value.filter((object) => object.busbarId !== selected.id)
    } else {
      primitiveObjects.value = primitiveObjects.value.filter((object) => object.id !== selected.id)
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
  const fallback = orientation === 'vertical' ? viewOrigin.x + viewBoxWidth.value / 2 : viewOrigin.y + viewBoxHeight.value / 2
  const raw = position ?? fallback
  const snapped = Math.round(raw / props.settings.gridStep) * props.settings.gridStep
  const guide = { id: `guide_${orientation}_${guides.value.length + 1}`, orientation, position: snapped }
  guides.value.push(guide)
  message.value = orientation === 'vertical' ? `Вертикальная направляющая X=${snapped}.` : `Горизонтальная направляющая Y=${snapped}.`
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
  else if (command === 'create_rectangle') createPrimitive('rectangle')
  else if (command === 'create_ellipse') createPrimitive('ellipse')
  else if (command === 'create_line') createPrimitive('line')
  else if (command === 'create_vertical_guide') createGuide('vertical')
  else if (command === 'create_horizontal_guide') createGuide('horizontal')
  else if (command === 'clear_guides') clearGuides()
  else if (command === 'zoom_100') setZoom(1)
  else if (command === 'zoom_fit') { viewOrigin.x = -viewBoxWidth.value / 2; viewOrigin.y = -viewBoxHeight.value / 2; setZoom(1) }
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

  if ((event.target as Element).closest('.canvas-text') || (event.target as Element).closest('.busbar-object') || (event.target as Element).closest('.primitive-object')) return

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

  startMarqueeSelection(event, point)
}

function onObjectPointerDown(event: PointerEvent, objectId: string): void {
  if (event.ctrlKey) toggleSelection('text', objectId)
  else if (!isSelected('text', objectId)) selectSingle('text', objectId)
  startSelectionDrag(event, { kind: 'text', id: objectId })
}

function onBusbarPointerDown(event: PointerEvent, busbarId: string): void {
  if (event.ctrlKey) toggleSelection('busbar', busbarId)
  else if (!isSelected('busbar', busbarId)) selectSingle('busbar', busbarId)
  startSelectionDrag(event, { kind: 'busbar', id: busbarId })
}

function onPrimitivePointerDown(event: PointerEvent, primitiveId: string): void {
  if (event.ctrlKey) toggleSelection('primitive', primitiveId)
  else if (!isSelected('primitive', primitiveId)) selectSingle('primitive', primitiveId)
  startSelectionDrag(event, { kind: 'primitive', id: primitiveId })
}

function startSelectionDrag(event: PointerEvent, dragged: SelectedElement): void {
  if (props.activeMode !== 'select') {
    message.value = 'Объект выбран. Для перетаскивания включите режим «Выбор».'
    setStatus(virtualPoint.value, 'object', selectedObjectName.value)
    return
  }

  if (!isSelected(dragged.kind, dragged.id)) selectedElements.value = [dragged]

  const startPoint = worldPointFromCanvasClient(event.clientX, event.clientY)
  if (!startPoint) return

  const selection = selectedElements.value.length ? [...selectedElements.value] : [dragged]
  const baselines: DragBaseline[] = []

  for (const selected of selection) {
    if (selected.kind === 'busbar') {
      const busbar = busbars.value.find((item) => item.id === selected.id)
      if (busbar) baselines.push({ selected, x: busbar.x, y: busbar.y })
    } else if (selected.kind === 'text') {
      const text = textObjects.value.find((item) => item.id === selected.id)
      if (text) baselines.push({ selected, x: text.center.x, y: text.center.y, anchorX: text.anchor.x, anchorY: text.anchor.y })
    } else {
      const primitive = primitiveObjects.value.find((item) => item.id === selected.id)
      if (primitive) baselines.push({ selected, x: primitive.x, y: primitive.y })
    }
  }

  const primary = baselines.find((item) => item.selected.kind === dragged.kind && item.selected.id === dragged.id) ?? baselines[0]
  if (!primary) return

  const pointerId = event.pointerId
  ;(event.currentTarget as Element).setPointerCapture?.(pointerId)

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    const current = worldPointFromCanvasClient(moveEvent.clientX, moveEvent.clientY)
    if (!current) return

    const rawPrimary = { x: primary.x + current.x - startPoint.x, y: primary.y + current.y - startPoint.y }
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
      } else if (base.selected.kind === 'text') {
        const text = textObjects.value.find((item) => item.id === base.selected.id)
        if (!text) continue
        text.center = { x: base.x + dx, y: base.y + dy }
        text.anchor = { x: (base.anchorX ?? base.x) + dx, y: (base.anchorY ?? base.y) + dy }
      } else {
        const primitive = primitiveObjects.value.find((item) => item.id === base.selected.id)
        if (!primitive) continue
        primitive.x = base.x + dx
        primitive.y = base.y + dy
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

function objectWorldRect(selected: SelectedElement): WorldRect | null {
  if (selected.kind === 'busbar') {
    const busbar = busbars.value.find((item) => item.id === selected.id)
    return busbar ? { x: busbar.x, y: busbar.y, width: busbar.width, height: busbar.height } : null
  }
  if (selected.kind === 'primitive') {
    const primitive = primitiveObjects.value.find((item) => item.id === selected.id)
    return primitive ? {
      x: Math.min(primitive.x, primitive.x + primitive.width),
      y: Math.min(primitive.y, primitive.y + primitive.height),
      width: Math.abs(primitive.width),
      height: Math.abs(primitive.height),
    } : null
  }
  const text = textObjects.value.find((item) => item.id === selected.id)
  return text ? { x: text.center.x - 25, y: text.center.y - 12, width: 50, height: 24 } : null
}

function allSelectableElements(): SelectedElement[] {
  return [
    ...busbars.value.map((item) => ({ kind: 'busbar' as const, id: item.id })),
    ...textObjects.value.map((item) => ({ kind: 'text' as const, id: item.id })),
    ...primitiveObjects.value.map((item) => ({ kind: 'primitive' as const, id: item.id })),
  ]
}

function startMarqueeSelection(event: PointerEvent, startPoint: Point): void {
  const pointerId = event.pointerId
  svgRef.value?.setPointerCapture?.(pointerId)
  const additive = event.ctrlKey
  const initialSelection = [...selectedElements.value]
  let moved = false

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    const current = worldPointFromCanvasClient(moveEvent.clientX, moveEvent.clientY)
    if (!current) return
    moved = true
    marqueeRect.value = {
      x: Math.min(startPoint.x, current.x),
      y: Math.min(startPoint.y, current.y),
      width: Math.abs(current.x - startPoint.x),
      height: Math.abs(current.y - startPoint.y),
    }
  }

  const up = (upEvent: PointerEvent) => {
    if (upEvent.pointerId !== pointerId) return
    window.removeEventListener('pointermove', move)
    window.removeEventListener('pointerup', up)

    if (moved && marqueeRect.value && marqueeRect.value.width > 2 && marqueeRect.value.height > 2) {
      const found = allSelectableElements().filter((item) => {
        const rect = objectWorldRect(item)
        return rect ? rectsIntersect(marqueeRect.value as WorldRect, rect) : false
      })
      selectedElements.value = additive ? mergeSelection(initialSelection, found) : found
      message.value = `Рамкой выделено объектов: ${found.length}.`
    } else if (!additive) {
      selectedElements.value = []
      message.value = 'Канвас выбран.'
    }

    marqueeRect.value = null
    setStatus(virtualPoint.value, null, '')
  }

  window.addEventListener('pointermove', move)
  window.addEventListener('pointerup', up)
}

function mergeSelection(a: SelectedElement[], b: SelectedElement[]): SelectedElement[] {
  const map = new Map<string, SelectedElement>()
  for (const item of a) map.set(elementKey(item.kind, item.id), item)
  for (const item of b) map.set(elementKey(item.kind, item.id), item)
  return [...map.values()]
}

function onGuidePointerDown(event: PointerEvent, guideId: string): void {
  const guide = guides.value.find((item) => item.id === guideId)
  if (!guide) return
  const pointerId = event.pointerId
  ;(event.currentTarget as Element).setPointerCapture?.(pointerId)

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    const point = worldPointFromCanvasClient(moveEvent.clientX, moveEvent.clientY)
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
  const point = worldPointFromTopRuler(event)
  if (!point) return
  const guide = createGuide('vertical', point.x)
  onGuidePointerDown(event, guide.id)
}

function onLeftRulerPointerDown(event: PointerEvent): void {
  const point = worldPointFromLeftRuler(event)
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
  const cursor = worldPointFromCanvasClient(event.clientX, event.clientY)
  const surface = canvasSurfaceRef.value
  if (!cursor || !surface) return
  const rect = surface.getBoundingClientRect()
  const fx = (event.clientX - rect.left) / rect.width
  const fy = (event.clientY - rect.top) / rect.height
  const factor = event.deltaY < 0 ? 1.08 : 0.92
  const nextZoom = Math.min(Math.max(props.settings.zoom * factor, 0.2), 6)
  const nextWidth = canvasPixels.width / nextZoom
  const nextHeight = canvasPixels.height / nextZoom
  viewOrigin.x = cursor.x - nextWidth * fx
  viewOrigin.y = cursor.y - nextHeight * fy
  emit('settingsChange', normalizeCanvasSettings({ ...props.settings, zoom: nextZoom }))
  message.value = `Масштаб: ${Math.round(nextZoom * 100)}%.`
  setStatus(cursor, null, '')
}

function onContextMenu(event: MouseEvent): void {
  const point = worldPointFromCanvasClient(event.clientX, event.clientY)
  contextMenu.visible = true
  contextMenu.x = event.clientX
  contextMenu.y = event.clientY
  contextMenu.point = point ?? { x: 0, y: 0 }

  const targetText = (event.target as Element).closest('.canvas-text')
  const targetBusbar = (event.target as Element).closest('.busbar-object')
  const targetPrimitive = (event.target as Element).closest('.primitive-object')
  if (targetText) selectSingle('text', targetText.getAttribute('data-object-id') ?? '')
  else if (targetBusbar) {
    const busbarId = targetBusbar.getAttribute('data-busbar-id')
    if (busbarId) selectSingle('busbar', busbarId)
  } else if (targetPrimitive) {
    const primitiveId = targetPrimitive.getAttribute('data-primitive-id')
    if (primitiveId) selectSingle('primitive', primitiveId)
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

.top-ruler,
.left-ruler {
  position: relative;
  background: #f8fafc;
  overflow: hidden;
}

.top-ruler {
  height: 28px;
  border-bottom: 1px solid #cbd5e1;
  cursor: ns-resize;
}

.left-ruler {
  width: 32px;
  border-right: 1px solid #cbd5e1;
  cursor: ew-resize;
}

.ruler-tick {
  position: absolute;
  background: #94a3b8;
  pointer-events: none;
}

.ruler-tick.top {
  bottom: 0;
  width: 1px;
  height: 9px;
}

.ruler-tick.top.major {
  height: 18px;
  background: #64748b;
}

.ruler-tick.left {
  right: 0;
  height: 1px;
  width: 10px;
}

.ruler-tick.left.major {
  width: 20px;
  background: #64748b;
}

.ruler-label {
  position: absolute;
  color: #475569;
  font-size: 10px;
  line-height: 1;
  pointer-events: none;
  user-select: none;
}

.ruler-label.top {
  top: 4px;
}

.ruler-label.left {
  left: 3px;
  transform: translateY(-50%);
}

.canvas-surface {
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
  fill: none;
  stroke: #8797ad;
  stroke-width: 0.7;
}

.iso-page-label {
  fill: #64748b;
  font-family: Arial, sans-serif;
  font-size: 9px;
  pointer-events: none;
}

.origin-line {
  stroke: #ef4444;
  stroke-width: 0.45;
  opacity: 0.42;
  stroke-dasharray: 2 2;
}

.origin-dot {
  fill: #ef4444;
  opacity: 0.44;
}

.origin-label {
  fill: #ef4444;
  font-size: 6px;
  font-family: Arial, sans-serif;
  opacity: 0.55;
}

.busbar-object,
.primitive-object {
  cursor: move;
}

.busbar-object.selected .busbar,
.primitive-object.selected rect,
.primitive-object.selected ellipse,
.primitive-object.selected line {
  stroke: #2563eb !important;
  stroke-width: 1.4 !important;
}

.busbar {
  stroke: #111827;
  stroke-width: 0.8;
}

.bay-slot {
  fill: #ffffff;
  stroke: #111827;
  stroke-width: 1.2;
  pointer-events: none;
}

.canvas-text {
  font-family: Arial, sans-serif;
  cursor: grab;
  user-select: none;
}

.canvas-text.selected {
  paint-order: stroke;
  stroke: rgba(37, 99, 235, 0.35);
  stroke-width: 1.8px;
}

.ghost-text {
  fill: #2563eb;
  opacity: 0.35;
  font-family: Arial, sans-serif;
  pointer-events: none;
}

.virtual-point-line {
  stroke: #f59e0b;
  stroke-width: 0.9;
  pointer-events: none;
}

.virtual-point-ring {
  fill: none;
  stroke: #f59e0b;
  stroke-width: 0.9;
  pointer-events: none;
}

.guide-line {
  stroke: #2563eb;
  stroke-width: 0.7;
  stroke-dasharray: 3 3;
  opacity: 0.55;
  pointer-events: none;
}

.user-guide-line {
  stroke: #0ea5e9;
  stroke-width: 0.8;
  stroke-dasharray: 5 4;
  cursor: move;
  pointer-events: stroke;
}

.selection-marquee {
  fill: rgba(37, 99, 235, 0.08);
  stroke: #2563eb;
  stroke-width: 0.8;
  stroke-dasharray: 3 3;
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

.properties-panel label.inline {
  display: flex;
  align-items: center;
  gap: 7px;
}

.properties-panel input,
.properties-panel select {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 6px 8px;
  background: white;
}

.properties-panel input[type="color"] {
  min-height: 32px;
  padding: 2px;
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