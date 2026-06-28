<script setup lang="ts">
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import type { SchemeSymbol, Connection, SymbolLibrary, SymbolDefinition, Terminal, Waypoint } from '../lib/types'
import {
  buildPolyline,
  findJunctions,
  pointsToSvgPath,
  snapToBusbar,
  extractBusbars,
  type Point,
} from '../lib/routing'
import SvgSymbol from './SvgSymbol.vue'

const props = defineProps<{
  symbols: SchemeSymbol[]
  connections: Connection[]
  selectedId: string
  selectedConnectionId: string
  library: SymbolLibrary | null
  connectionMode: 'select' | 'wire'
  pendingWireFrom: string
  pendingWirePoints: Waypoint[]
}>()

const emit = defineEmits<{
  select: [id: string]
  selectConnection: [id: string]
  stateChange: [symbolId: string, newState: string]
  dropSymbol: [symbolType: string, x: number, y: number]
  deleteSymbol: [symbolId: string]
  deleteConnection: [id: string]
  wireTerminalClick: [ref: string, x: number, y: number]
  wireCanvasClick: [x: number, y: number]
  wireCancel: []
  insertWaypoint: [connId: string, point: Waypoint]
}>()

// -------- Symbol lookup --------
const defByType = computed(() => {
  if (!props.library) return new Map<string, SymbolDefinition>()
  const m = new Map<string, SymbolDefinition>()
  for (const s of props.library.symbols) m.set(s.type, s)
  return m
})

// -------- Build terminals-by-ref map --------
const terminalsByRef = computed(() => {
  const m = new Map<string, Point>()
  for (const s of props.symbols) {
    for (const t of s.terminals) {
      m.set(`${s.id}.${t.id}`, { x: t.x, y: t.y })
    }
  }
  return m
})

// -------- Busbar segments for snap --------
const busbars = computed(() =>
  extractBusbars(
    props.symbols.map((s) => ({ id: s.id, type: s.type, x: s.x, y: s.y, width: s.width })),
  ),
)

// -------- Polyline geometry per connection --------
const polylines = computed(() => {
  const out: Array<{ id: string; d: string; kind: Connection['kind']; points: Point[] }> = []
  for (const c of props.connections) {
    const pts = buildPolyline(c, terminalsByRef.value)
    if (pts.length < 2) continue
    out.push({
      id: c.id,
      d: pointsToSvgPath(pts),
      kind: c.kind ?? 'wire',
      points: pts,
    })
  }
  return out
})

// -------- Junctions (3+ lines meeting at same coordinate) --------
const junctions = computed(() => {
  return findJunctions(props.connections, terminalsByRef.value, 1.0)
})

// -------- Live preview for pending wire --------
const previewPath = computed(() => {
  if (props.connectionMode !== 'wire' || !props.pendingWireFrom) return ''
  const start = terminalsByRef.value.get(props.pendingWireFrom)
  if (!start) return ''
  const pts: Point[] = [start, ...props.pendingWirePoints]
  return pointsToSvgPath(pts)
})

// -------- Mouse tracking for preview end point --------
const mousePos = ref<Point>({ x: 0, y: 0 })
function svgPoint(evt: DragEvent | MouseEvent, svg: SVGSVGElement): Point {
  const pt = svg.createSVGPoint()
  pt.x = evt.clientX
  pt.y = evt.clientY
  const ctm = svg.getScreenCTM()
  if (!ctm) return { x: 0, y: 0 }
  const local = pt.matrixTransform(ctm.inverse())
  return { x: local.x, y: local.y }
}

const svgRef = ref<SVGSVGElement | null>(null)
function getSvg(): SVGSVGElement | null {
  return svgRef.value
}

function onMouseMove(evt: MouseEvent) {
  const svg = getSvg()
  if (!svg) return
  mousePos.value = svgPoint(evt, svg)
}

function onMouseLeave() {
  mousePos.value = { x: -9999, y: -9999 }
}

// -------- Drop handler (symbol library drag) --------
function onDragOver(evt: DragEvent) {
  if (!evt.dataTransfer) return
  if (!evt.dataTransfer.types.includes('application/x-electroscheme-symbol')) return
  evt.preventDefault()
  evt.dataTransfer.dropEffect = 'copy'
}

function onDrop(evt: DragEvent) {
  const type = evt.dataTransfer?.getData('application/x-electroscheme-symbol')
  if (!type) return
  evt.preventDefault()
  const svg = getSvg()
  if (!svg) return
  const { x, y } = svgPoint(evt, svg)
  emit('dropSymbol', type, Math.round(x), Math.round(y))
}

// -------- Terminal click → wire mode --------
function onTerminalClick(evt: MouseEvent, sym: SchemeSymbol, term: Terminal) {
  if (props.connectionMode !== 'wire') return
  evt.stopPropagation()
  emit('wireTerminalClick', `${sym.id}.${term.id}`, term.x, term.y)
}

function onWireCanvasClick() {
  if (props.connectionMode !== 'wire') return
  emit('wireCanvasClick', Math.round(mousePos.value.x), Math.round(mousePos.value.y))
}

function onConnectionClick(evt: MouseEvent, connId: string) {
  if (props.connectionMode === 'wire') return
  evt.stopPropagation()
  emit('selectConnection', connId)
}

function onWaypointDoubleClick(evt: MouseEvent, connId: string, point: Waypoint) {
  if (props.connectionMode !== 'select') return
  evt.stopPropagation()
  emit('insertWaypoint', connId, point)
}

// -------- Keyboard --------
function onKeyDown(evt: KeyboardEvent) {
  if (evt.key === 'Escape') {
    if (props.connectionMode === 'wire' && (props.pendingWireFrom || props.pendingWirePoints.length)) {
      emit('wireCancel')
      evt.preventDefault()
      return
    }
  }
  if (props.connectionMode === 'wire') return

  if ((evt.key === 'Delete' || evt.key === 'Backspace')) {
    if (props.selectedConnectionId) {
      evt.preventDefault()
      emit('deleteConnection', props.selectedConnectionId)
      return
    }
    if (props.selectedId) {
      evt.preventDefault()
      emit('deleteSymbol', props.selectedId)
    }
  }
}

onMounted(() => window.addEventListener('keydown', onKeyDown))
onBeforeUnmount(() => window.removeEventListener('keydown', onKeyDown))
</script>

<template>
  <div class="sheet-wrap" :class="{ 'wire-mode': connectionMode === 'wire' }" tabindex="0">
    <svg
      ref="svgRef"
      class="sheet"
      viewBox="0 0 420 297"
      role="img"
      aria-label="Electrical scheme"
      @dragover="onDragOver"
      @drop="onDrop"
      @mousemove="onMouseMove"
      @mouseleave="onMouseLeave"
      @click="onWireCanvasClick"
    >
      <defs>
        <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" class="grid-line" />
        </pattern>
        <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
          <path d="M 0 0 L 6 3 L 0 6 Z" fill="currentColor" />
        </marker>
      </defs>

      <rect x="0" y="0" width="420" height="297" class="sheet-bg" />
      <rect x="10" y="10" width="400" height="277" class="frame" />
      <rect x="10" y="10" width="400" height="277" fill="url(#grid)" opacity="0.55" />

      <!-- Busbars (special-cased: drawn as thick lines spanning width) -->
      <g v-for="sym in symbols.filter(s => s.type === 'busbar')" :key="sym.id"
         class="symbol"
         :class="{ selected: selectedId === sym.id }"
         @click.stop="emit('select', sym.id)">
        <line
          :x1="sym.x" :y1="sym.y"
          :x2="sym.x + (sym.width ?? 0)" :y2="sym.y"
          class="primary-line thick"
        />
        <text :x="sym.x - 18" :y="sym.y + 4" class="label">{{ sym.label }}</text>
      </g>

      <!-- Library symbols -->
      <g v-for="sym in symbols.filter(s => s.type !== 'busbar')" :key="sym.id"
         class="symbol"
         :class="{ selected: selectedId === sym.id }"
         :transform="`translate(${sym.x}, ${sym.y})`"
         @click.stop="emit('select', sym.id)">
        <SvgSymbol
          v-if="defByType.has(sym.type)"
          :definition="defByType.get(sym.type)!"
          :current-state="sym.current_state"
          :size="sym.width ?? defByType.get(sym.type)!.default_width"
          @state-change="(t, s) => emit('stateChange', sym.id, s)"
        />
        <rect v-else :x="-10" :y="-10" width="20" height="20" rx="3" class="device-box" />
        <text
          v-if="defByType.has(sym.type)"
          :x="(defByType.get(sym.type)!.default_width / 2) + 4"
          :y="-2"
          class="label"
        >{{ sym.label }}</text>
      </g>

      <!-- Terminal dots (clickable in wire mode) -->
      <g class="terminals-layer">
        <g v-for="sym in symbols" :key="`t-${sym.id}`">
          <circle
            v-for="term in sym.terminals"
            :key="`t-${sym.id}-${term.id}`"
            :cx="term.x" :cy="term.y" r="1.4"
            class="terminal-dot"
            :class="{
              start: connectionMode === 'wire' && pendingWireFrom === `${sym.id}.${term.id}`,
            }"
            @click="onTerminalClick($event, sym, term)"
          />
        </g>
      </g>

      <!-- Connection polylines -->
      <g class="connections-layer">
        <path
          v-for="pl in polylines"
          :key="pl.id"
          :d="pl.d"
          class="connection-line"
          :class="['kind-' + (pl.kind || 'wire'), { selected: selectedConnectionId === pl.id }]"
          @click="onConnectionClick($event, pl.id)"
        />
      </g>

      <!-- Waypoints (visible when selected) -->
      <g class="waypoints-layer">
        <template v-for="pl in polylines" :key="`wp-${pl.id}`">
          <g v-if="selectedConnectionId === pl.id">
            <rect
              v-for="(wp, idx) in pl.points.slice(1, -1)"
              :key="`wp-${pl.id}-${idx}`"
              :x="wp.x - 1.5" :y="wp.y - 1.5" width="3" height="3"
              class="connection-waypoint"
            />
          </g>
        </template>
      </g>

      <!-- Junctions (per ГОСТ 2.721-74: filled dot at line intersections) -->
      <g class="junctions-layer">
        <circle
          v-for="entry in junctions"
          :key="entry[0]"
          :cx="entry[1].point.x" :cy="entry[1].point.y" r="1.4"
          class="junction-dot"
        />
      </g>

      <!-- Live preview line while drawing -->
      <path v-if="previewPath" :d="previewPath" class="connection-line preview" />

      <text x="20" y="282" class="title-block">ElectroScheme Studio — demo A3 sheet</text>
    </svg>
  </div>
</template>
