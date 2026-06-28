<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import type { ToolType, EditorElement } from '../lib/editorTypes'

const emit = defineEmits<{
  save: [svg: string, viewBox: string]
  close: []
}>()

let _uid = 0
function uid(): string { return `el_${++_uid}` }

const currentTool = ref<ToolType>('select')
const elements = ref<EditorElement[]>([])
const selectedId = ref<string | null>(null)
const viewBox = reactive({ x: -20, y: -20, w: 140, h: 100 })
const grid = reactive({ size: 5, snap: true, visible: true })
const zoom = ref(1)
const panOffset = reactive({ x: 0, y: 0 })
const symbolName = ref('new_symbol')
const symbolId = ref('new_symbol')
const symbolGost = ref('ГОСТ 2.755-87')
const strokeWidth = ref(0.8)
const strokeColor = ref('black')
const fillColor = ref('none')
const fontSize = ref(10)
const textContent = ref('A')
const copiedElements = ref<EditorElement[]>([])

const selectedElement = computed(() => {
  if (!selectedId.value) return null
  return elements.value.find(e => e.id === selectedId.value) ?? null
})

const canvasWidth = computed(() => viewBox.w * zoom.value)
const canvasHeight = computed(() => viewBox.h * zoom.value)

function snap(v: number): number {
  if (!grid.snap) return Math.round(v * 100) / 100
  return Math.round(v / grid.size) * grid.size
}

function svgPoint(e: MouseEvent, svg: SVGSVGElement): { x: number; y: number } {
  const rect = svg.getBoundingClientRect()
  const scaleX = viewBox.w / rect.width
  const scaleY = viewBox.h / rect.height
  return {
    x: snap((e.clientX - rect.left) * scaleX + viewBox.x),
    y: snap((e.clientY - rect.top) * scaleY + viewBox.y),
  }
}

const isDrawing = ref(false)
const drawStart = ref<{ x: number; y: number } | null>(null)
const drawPreview = ref<EditorElement | null>(null)
const dragStart = ref<{ x: number; y: number; elX: number; elY: number } | null>(null)
const isPanning = ref(false)
const panStart = ref<{ mx: number; my: number; vx: number; vy: number } | null>(null)
const polyPoints = ref<{ x: number; y: number }[]>([])
const arcStep = ref(0)

const svgRef = ref<SVGSVGElement | null>(null)

function newElement(type: string, data: Record<string, unknown>, x = 0, y = 0): EditorElement {
  return {
    id: uid().toString(),
    type,
    stroke: strokeColor.value,
    fill: fillColor.value,
    strokeWidth: strokeWidth.value,
    opacity: 1,
    visible: true,
    locked: false,
    x, y,
    rotation: 0,
    data,
  }
}

function onMouseDown(e: MouseEvent) {
  if (!svgRef.value) return
  const pt = svgPoint(e, svgRef.value)
  const tool = currentTool.value

  if (tool === 'pan') {
    isPanning.value = true
    panStart.value = { mx: e.clientX, my: e.clientY, vx: viewBox.x, vy: viewBox.y }
    return
  }

  if (tool === 'select') {
    if (selectedId.value && selectedElement.value && !selectedElement.value.locked) {
      dragStart.value = { x: pt.x, y: pt.y, elX: selectedElement.value.x, elY: selectedElement.value.y }
    }
    return
  }

  if (tool === 'polyline') {
    polyPoints.value.push(pt)
    return
  }

  if (tool === 'arc') {
    arcStep.value++
    if (arcStep.value === 1) {
      drawStart.value = pt
    } else if (arcStep.value === 2) {
      drawStart.value = pt
    } else if (arcStep.value === 3) {
      arcStep.value = 0
    }
    return
  }

  isDrawing.value = true
  drawStart.value = pt

  if (tool === 'text') {
    const el = newElement('text', { text: textContent.value, fontSize: fontSize.value, fontFamily: 'Arial' }, pt.x, pt.y)
    elements.value.push(el)
    selectedId.value = el.id
    isDrawing.value = false
    drawStart.value = null
  }
}

function onMouseMove(e: MouseEvent) {
  if (!svgRef.value) return
  const pt = svgPoint(e, svgRef.value)

  if (isPanning.value && panStart.value) {
    const dx = (e.clientX - panStart.value.mx) * (viewBox.w / svgRef.value.getBoundingClientRect().width)
    const dy = (e.clientY - panStart.value.my) * (viewBox.h / svgRef.value.getBoundingClientRect().height)
    viewBox.x = panStart.value.vx - dx
    viewBox.y = panStart.value.vy - dy
    return
  }

  if (dragStart.value && selectedElement.value) {
    const dx = pt.x - dragStart.value.x
    const dy = pt.y - dragStart.value.y
    selectedElement.value.x = snap(dragStart.value.elX + dx)
    selectedElement.value.y = snap(dragStart.value.elY + dy)
    return
  }

  if (!isDrawing.value || !drawStart.value) return
  const tool = currentTool.value
  const sx = drawStart.value.x
  const sy = drawStart.value.y
  const ex = pt.x
  const ey = pt.y

  let preview: EditorElement | null = null

  if (tool === 'line') {
    preview = newElement('line', { x1: sx, y1: sy, x2: ex, y2: ey })
  } else if (tool === 'rect') {
    const rx = Math.min(sx, ex)
    const ry = Math.min(sy, ey)
    const w = Math.abs(ex - sx)
    const h = Math.abs(ey - sy)
    preview = newElement('rect', { x: rx, y: ry, width: w, height: h, rx: 0, ry: 0 })
    preview.x = 0
    preview.y = 0
  } else if (tool === 'circle') {
    const r = Math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)
    preview = newElement('circle', { cx: sx, cy: sy, r: snap(r) })
  } else if (tool === 'ellipse') {
    const rx = Math.abs(ex - sx)
    const ry = Math.abs(ey - sy)
    preview = newElement('ellipse', { cx: sx, cy: sy, rx: snap(rx), ry: snap(ry) })
  }

  drawPreview.value = preview
}

function onMouseUp(e: MouseEvent) {
  if (isPanning.value) {
    isPanning.value = false
    panStart.value = null
    return
  }

  if (dragStart.value) {
    dragStart.value = null
    return
  }

  if (currentTool.value === 'polyline' || currentTool.value === 'arc') return

  if (isDrawing.value && drawPreview.value) {
    elements.value.push(drawPreview.value)
    selectedId.value = drawPreview.value.id
  }

  isDrawing.value = false
  drawStart.value = null
  drawPreview.value = null
}

function onDblClick(e: MouseEvent) {
  if (currentTool.value === 'polyline' && polyPoints.value.length > 1) {
    const pts = polyPoints.value.map(p => `${p.x},${p.y}`).join(' ')
    const el = newElement('polyline', { points: pts })
    elements.value.push(el)
    selectedId.value = el.id
    polyPoints.value = []
  } else if (currentTool.value === 'arc') {
    arcStep.value = 0
    drawStart.value = null
  }
}

function onWheel(e: WheelEvent) {
  e.preventDefault()
  const factor = e.deltaY > 0 ? 0.9 : 1.1
  zoom.value = Math.max(0.3, Math.min(5, zoom.value * factor))
}

function onKeyDown(e: KeyboardEvent) {
  if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return

  if (e.key === 'Delete' || e.key === 'Backspace') {
    deleteSelected()
  } else if (e.key === 'Escape') {
    selectedId.value = null
    polyPoints.value = []
    arcStep.value = 0
    isDrawing.value = false
    drawStart.value = null
    drawPreview.value = null
  } else if (e.key === 'c' && (e.ctrlKey || e.metaKey)) {
    copySelected()
  } else if (e.key === 'v' && (e.ctrlKey || e.metaKey)) {
    pasteCopied()
  } else if (e.key === 'z' && (e.ctrlKey || e.metaKey)) {
    undo()
  } else if (e.key === 'd' && (e.ctrlKey || e.metaKey)) {
    e.preventDefault()
    duplicateSelected()
  }
}

function deleteSelected() {
  if (!selectedId.value) return
  elements.value = elements.value.filter(e => e.id !== selectedId.value)
  selectedId.value = null
}

function copySelected() {
  if (!selectedElement.value) return
  copiedElements.value = [JSON.parse(JSON.stringify(selectedElement.value))]
}

function pasteCopied() {
  if (!copiedElements.value.length) return
  const clone = JSON.parse(JSON.stringify(copiedElements.value[0]))
  clone.id = uid().toString()
  clone.x += grid.size * 2
  clone.y += grid.size * 2
  elements.value.push(clone)
  selectedId.value = clone.id
}

function duplicateSelected() {
  copySelected()
  pasteCopied()
}

const history = ref<string[]>([])
const historyIndex = ref(-1)

function saveState() {
  const snap = JSON.stringify(elements.value)
  history.value = history.value.slice(0, historyIndex.value + 1)
  history.value.push(snap)
  historyIndex.value = history.value.length - 1
  if (history.value.length > 100) {
    history.value.shift()
    historyIndex.value--
  }
}

function undo() {
  if (historyIndex.value <= 0) return
  historyIndex.value--
  elements.value = JSON.parse(history.value[historyIndex.value])
  selectedId.value = null
}

watch(elements, () => saveState(), { deep: true })

function moveUp() {
  if (!selectedId.value) return
  const idx = elements.value.findIndex(e => e.id === selectedId.value)
  if (idx < elements.value.length - 1) {
    const el = elements.value.splice(idx, 1)[0]
    elements.value.splice(idx + 1, 0, el)
  }
}

function moveDown() {
  if (!selectedId.value) return
  const idx = elements.value.findIndex(e => e.id === selectedId.value)
  if (idx > 0) {
    const el = elements.value.splice(idx, 1)[0]
    elements.value.splice(idx - 1, 0, el)
  }
}

function bringToFront() {
  if (!selectedId.value) return
  const idx = elements.value.findIndex(e => e.id === selectedId.value)
  if (idx >= 0) {
    const el = elements.value.splice(idx, 1)[0]
    elements.value.push(el)
  }
}

function sendToBack() {
  if (!selectedId.value) return
  const idx = elements.value.findIndex(e => e.id === selectedId.value)
  if (idx >= 0) {
    const el = elements.value.splice(idx, 1)[0]
    elements.value.unshift(el)
  }
}

function clearAll() {
  elements.value = []
  selectedId.value = null
  saveState()
}

function buildSvgString(): string {
  const lines: string[] = []
  for (const el of elements.value) {
    if (!el.visible) continue
    lines.push(elementToSvg(el))
  }
  return lines.join('\n  ')
}

function elementToSvg(el: EditorElement): string {
  const t = el.rotation ? ` transform="rotate(${el.rotation} ${el.x} ${el.y})"` : ''
  const op = el.opacity < 1 ? ` opacity="${el.opacity}"` : ''
  const s = ` stroke="${el.stroke}" stroke-width="${el.strokeWidth}" fill="${el.fill}"`

  switch (el.type) {
    case 'line': {
      const d = el.data
      return `<line x1="${d.x1}" y1="${d.y1}" x2="${d.x2}" y2="${d.y2}"${s}${op}${t}/>`
    }
    case 'rect': {
      const d = el.data
      const rx = d.rx ? ` rx="${d.rx}"` : ''
      return `<rect x="${d.x}" y="${d.y}" width="${d.width}" height="${d.height}"${rx}${s}${op}${t}/>`
    }
    case 'circle': {
      const d = el.data
      return `<circle cx="${d.cx}" cy="${d.cy}" r="${d.r}"${s}${op}${t}/>`
    }
    case 'ellipse': {
      const d = el.data
      return `<ellipse cx="${d.cx}" cy="${d.cy}" rx="${d.rx}" ry="${d.ry}"${s}${op}${t}/>`
    }
    case 'text': {
      const d = el.data
      return `<text x="${el.x}" y="${el.y}" font-size="${d.fontSize}" font-family="${d.fontFamily}" fill="${el.stroke}" stroke="none"${op}${t}>${d.text}</text>`
    }
    case 'polyline': {
      const d = el.data
      return `<polyline points="${d.points}"${s}${op}${t}/>`
    }
    case 'path': {
      const d = el.data
      return `<path d="${d.d}"${s}${op}${t}/>`
    }
    default:
      return `<!-- unknown: ${el.type} -->`
  }
}

function exportSvg() {
  const vb = `${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`
  const inner = buildSvgString()
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}">\n  ${inner}\n</svg>`
  emit('save', svg, vb)
}

function copySvgToClipboard() {
  const vb = `${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`
  const inner = buildSvgString()
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}">\n  ${inner}\n</svg>`
  navigator.clipboard.writeText(svg)
}

function loadSymbol(svgStr: string, newViewBox: string) {
  const parser = new DOMParser()
  const doc = parser.parseFromString(svgStr, 'image/svg+xml')
  const svgEl = doc.querySelector('svg')
  if (!svgEl) return

  const vb = svgEl.getAttribute('viewBox')
  if (vb) {
    const parts = vb.split(/[\s,]+/).map(Number)
    if (parts.length === 4) {
      viewBox.x = parts[0]
      viewBox.y = parts[1]
      viewBox.w = parts[2]
      viewBox.h = parts[3]
    }
  }

  elements.value = []
  selectedId.value = null

  function parseChild(node: Element) {
    for (const child of Array.from(node.children)) {
      const tag = child.tagName.toLowerCase()
      const attrs: Record<string, string> = {}
      for (const a of Array.from(child.attributes)) {
        attrs[a.name] = a.value
      }

      const stroke = attrs.stroke || 'black'
      const fill = attrs.fill || 'none'
      const sw = parseFloat(attrs['stroke-width'] || '0.8')
      const op = parseFloat(attrs.opacity || '1')

      let el: EditorElement | null = null

      if (tag === 'line') {
        el = newElement('line', {
          x1: parseFloat(attrs.x1 || '0'),
          y1: parseFloat(attrs.y1 || '0'),
          x2: parseFloat(attrs.x2 || '0'),
          y2: parseFloat(attrs.y2 || '0'),
        })
      } else if (tag === 'rect') {
        el = newElement('rect', {
          x: parseFloat(attrs.x || '0'),
          y: parseFloat(attrs.y || '0'),
          width: parseFloat(attrs.width || '0'),
          height: parseFloat(attrs.height || '0'),
          rx: parseFloat(attrs.rx || '0'),
          ry: parseFloat(attrs.ry || '0'),
        })
      } else if (tag === 'circle') {
        el = newElement('circle', {
          cx: parseFloat(attrs.cx || '0'),
          cy: parseFloat(attrs.cy || '0'),
          r: parseFloat(attrs.r || '0'),
        })
      } else if (tag === 'ellipse') {
        el = newElement('ellipse', {
          cx: parseFloat(attrs.cx || '0'),
          cy: parseFloat(attrs.cy || '0'),
          rx: parseFloat(attrs.rx || '0'),
          ry: parseFloat(attrs.ry || '0'),
        })
      } else if (tag === 'text') {
        el = newElement('text', {
          text: child.textContent || '',
          fontSize: parseFloat(attrs['font-size'] || '10'),
          fontFamily: attrs['font-family'] || 'Arial',
        })
        el.x = parseFloat(attrs.x || '0')
        el.y = parseFloat(attrs.y || '0')
      } else if (tag === 'polyline') {
        el = newElement('polyline', { points: attrs.points || '' })
      } else if (tag === 'path') {
        el = newElement('path', { d: attrs.d || '' })
      } else if (tag === 'g') {
        parseChild(child)
        return
      }

      if (el) {
        el.stroke = stroke === 'currentColor' ? 'black' : stroke
        el.fill = fill
        el.strokeWidth = sw
        el.opacity = op
        elements.value.push(el)
      }
    }
  }

  parseChild(svgEl)
  saveState()
}

function onGridSizeChange(v: number) {
  grid.size = Math.max(1, Math.min(20, v))
}

function resetView() {
  viewBox.x = -20
  viewBox.y = -20
  viewBox.w = 140
  viewBox.h = 100
  zoom.value = 1
}

function updateElementData(key: string, value: unknown) {
  if (!selectedElement.value) return
  selectedElement.value.data[key] = value
}

function updateElementProp(key: string, value: unknown) {
  if (!selectedElement.value) return
  ;(selectedElement.value as Record<string, unknown>)[key] = value
}

onMounted(() => {
  saveState()
  window.addEventListener('keydown', onKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeyDown)
})

defineExpose({ loadSymbol, buildSvgString, elements })
</script>

<template>
  <div class="editor-root">
    <div class="editor-toolbar">
      <div class="toolbar-group">
        <span class="toolbar-label">Режим</span>
        <button class="btn-mode" @click="emit('close')">← Схема</button>
      </div>

      <div class="toolbar-sep" />

      <div class="toolbar-group">
        <span class="toolbar-label">Инструменты</span>
        <div class="tool-row">
          <button v-for="t in (['select','line','rect','circle','ellipse','text','polyline','pan'] as ToolType[])"
                  :key="t"
                  class="tool-btn"
                  :class="{ active: currentTool === t }"
                  :title="t"
                  @click="currentTool = t">
            {{ t === 'select' ? '⬚' : t === 'line' ? '╱' : t === 'rect' ? '▭' : t === 'circle' ? '◯' : t === 'ellipse' ? '⬮' : t === 'text' ? 'T' : t === 'polyline' ? '⌒' : '✋' }}
          </button>
        </div>
      </div>

      <div class="toolbar-sep" />

      <div class="toolbar-group">
        <span class="toolbar-label">Действия</span>
        <div class="tool-row">
          <button class="tool-btn" title="Копировать (Ctrl+C)" @click="copySelected">⧉</button>
          <button class="tool-btn" title="Вставить (Ctrl+V)" @click="pasteCopied">⊞</button>
          <button class="tool-btn" title="Дублировать (Ctrl+D)" @click="duplicateSelected">⧉+</button>
          <button class="tool-btn" title="Удалить (Del)" @click="deleteSelected">✕</button>
          <button class="tool-btn" title="Отмена (Ctrl+Z)" @click="undo">↩</button>
        </div>
      </div>

      <div class="toolbar-sep" />

      <div class="toolbar-group">
        <span class="toolbar-label">Слой</span>
        <div class="tool-row">
          <button class="tool-btn" title="Выше" @click="moveUp">↑</button>
          <button class="tool-btn" title="Ниже" @click="moveDown">↓</button>
          <button class="tool-btn" title="Вперёд" @click="bringToFront">⇥</button>
          <button class="tool-btn" title="Назад" @click="sendToBack">⇤</button>
        </div>
      </div>

      <div class="toolbar-sep" />

      <div class="toolbar-group">
        <span class="toolbar-label">Сетка</span>
        <div class="tool-row">
          <label class="check-label">
            <input type="checkbox" v-model="grid.visible"> Вид
          </label>
          <label class="check-label">
            <input type="checkbox" v-model="grid.snap"> Привязка
          </label>
          <input type="number" class="input-sm" :value="grid.size"
                 @input="onGridSizeChange(Number(($event.target as HTMLInputElement).value))" min="1" max="20">
        </div>
      </div>

      <div class="toolbar-sep" />

      <div class="toolbar-group">
        <div class="tool-row">
          <button class="tool-btn" title="Сброс вида" @click="resetView">⊡</button>
          <button class="tool-btn" title="Очистить всё" @click="clearAll">🗑</button>
        </div>
      </div>
    </div>

    <div class="editor-main">
      <div class="canvas-area" ref="canvasArea">
        <svg ref="svgRef"
             class="editor-canvas"
             :viewBox="`${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`"
             @mousedown="onMouseDown"
             @mousemove="onMouseMove"
             @mouseup="onMouseUp"
             @dblclick="onDblClick"
             @wheel.prevent="onWheel"
             xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern v-if="grid.visible"
                     :id="'grid-' + grid.size"
                     :width="grid.size" :height="grid.size"
                     patternUnits="userSpaceOnUse">
              <path :d="`M ${grid.size} 0 L 0 0 0 ${grid.size}`"
                    fill="none" stroke="#dde2ea" stroke-width="0.15"/>
            </pattern>
            <pattern v-if="grid.visible"
                     :id="'grid-major-' + grid.size"
                     :width="grid.size * 5" :height="grid.size * 5"
                     patternUnits="userSpaceOnUse">
              <rect :width="grid.size * 5" :height="grid.size * 5"
                    :fill="`url(#grid-${grid.size})`"/>
              <path :d="`M ${grid.size * 5} 0 L 0 0 0 ${grid.size * 5}`"
                    fill="none" stroke="#bcc4d0" stroke-width="0.25"/>
            </pattern>
          </defs>

          <rect v-if="grid.visible"
                :x="viewBox.x - 100" :y="viewBox.y - 100"
                :width="viewBox.w + 200" :height="viewBox.h + 200"
                :fill="`url(#grid-major-${grid.size})`"/>

          <line v-for="el in elements.filter(e => e.type === 'line' && e.visible)" :key="el.id"
                :x1="el.data.x1" :y1="el.data.y1"
                :x2="el.data.x2" :y2="el.data.y2"
                :stroke="el.stroke" :stroke-width="el.strokeWidth"
                :fill="el.fill" :opacity="el.opacity"
                :class="{ selected: el.id === selectedId }"
                @click.stop="selectedId = el.id"/>

          <rect v-for="el in elements.filter(e => e.type === 'rect' && e.visible)" :key="el.id"
                :x="el.data.x" :y="el.data.y"
                :width="el.data.width" :height="el.data.height"
                :rx="el.data.rx || 0" :ry="el.data.ry || 0"
                :stroke="el.stroke" :stroke-width="el.strokeWidth"
                :fill="el.fill" :opacity="el.opacity"
                :class="{ selected: el.id === selectedId }"
                @click.stop="selectedId = el.id"/>

          <circle v-for="el in elements.filter(e => e.type === 'circle' && e.visible)" :key="el.id"
                  :cx="el.data.cx" :cy="el.data.cy" :r="el.data.r"
                  :stroke="el.stroke" :stroke-width="el.strokeWidth"
                  :fill="el.fill" :opacity="el.opacity"
                  :class="{ selected: el.id === selectedId }"
                  @click.stop="selectedId = el.id"/>

          <ellipse v-for="el in elements.filter(e => e.type === 'ellipse' && e.visible)" :key="el.id"
                   :cx="el.data.cx" :cy="el.data.cy"
                   :rx="el.data.rx" :ry="el.data.ry"
                   :stroke="el.stroke" :stroke-width="el.strokeWidth"
                   :fill="el.fill" :opacity="el.opacity"
                   :class="{ selected: el.id === selectedId }"
                   @click.stop="selectedId = el.id"/>

          <text v-for="el in elements.filter(e => e.type === 'text' && e.visible)" :key="el.id"
                :x="el.x" :y="el.y"
                :font-size="el.data.fontSize" :font-family="el.data.fontFamily"
                :fill="el.stroke" stroke="none"
                :opacity="el.opacity"
                :class="{ selected: el.id === selectedId }"
                @click.stop="selectedId = el.id">{{ el.data.text }}</text>

          <polyline v-for="el in elements.filter(e => e.type === 'polyline' && e.visible)" :key="el.id"
                    :points="el.data.points"
                    :stroke="el.stroke" :stroke-width="el.strokeWidth"
                    :fill="el.fill" :opacity="el.opacity"
                    stroke-linejoin="round" stroke-linecap="round"
                    :class="{ selected: el.id === selectedId }"
                    @click.stop="selectedId = el.id"/>

          <g v-if="drawPreview">
            <line v-if="drawPreview.type === 'line'"
                  :x1="drawPreview.data.x1" :y1="drawPreview.data.y1"
                  :x2="drawPreview.data.x2" :y2="drawPreview.data.y2"
                  :stroke="drawPreview.stroke" :stroke-width="drawPreview.strokeWidth"
                  fill="none" stroke-dasharray="0.5 0.5"/>
            <rect v-else-if="drawPreview.type === 'rect'"
                  :x="drawPreview.data.x" :y="drawPreview.data.y"
                  :width="drawPreview.data.width" :height="drawPreview.data.height"
                  :stroke="drawPreview.stroke" :stroke-width="drawPreview.strokeWidth"
                  fill="none" stroke-dasharray="0.5 0.5"/>
            <circle v-else-if="drawPreview.type === 'circle'"
                    :cx="drawPreview.data.cx" :cy="drawPreview.data.cy" :r="drawPreview.data.r"
                    :stroke="drawPreview.stroke" :stroke-width="drawPreview.strokeWidth"
                    fill="none" stroke-dasharray="0.5 0.5"/>
            <ellipse v-else-if="drawPreview.type === 'ellipse'"
                     :cx="drawPreview.data.cx" :cy="drawPreview.data.cy"
                     :rx="drawPreview.data.rx" :ry="drawPreview.data.ry"
                     :stroke="drawPreview.stroke" :stroke-width="drawPreview.strokeWidth"
                     fill="none" stroke-dasharray="0.5 0.5"/>
          </g>

          <polyline v-if="polyPoints.length > 0"
                    :points="polyPoints.map(p => `${p.x},${p.y}`).join(' ')"
                    stroke="black" :stroke-width="strokeWidth"
                    fill="none" stroke-dasharray="0.5 0.5"/>
        </svg>

        <div class="canvas-coords">
          {{ Math.round(viewBox.x) }}, {{ Math.round(viewBox.y) }} | zoom: {{ (zoom * 100).toFixed(0) }}%
          | {{ elements.length }} элементов
        </div>
      </div>

      <div class="editor-sidebar">
        <div class="sidebar-section">
          <h3>Символ</h3>
          <label class="field-label">ID
            <input type="text" class="input-field" v-model="symbolId"/>
          </label>
          <label class="field-label">Имя
            <input type="text" class="input-field" v-model="symbolName"/>
          </label>
          <label class="field-label">ГОСТ
            <input type="text" class="input-field" v-model="symbolGost"/>
          </label>
        </div>

        <div class="sidebar-section">
          <h3>Стиль по умолчанию</h3>
          <label class="field-label">Обводка
            <div class="color-row">
              <input type="color" v-model="strokeColor"/>
              <input type="text" class="input-field" v-model="strokeColor"/>
            </div>
          </label>
          <label class="field-label">Заливка
            <div class="color-row">
              <input type="color" v-model="fillColor" :disabled="fillColor === 'none'"/>
              <input type="text" class="input-field" v-model="fillColor"/>
            </div>
          </label>
          <label class="field-label">Толщина линии
            <input type="number" class="input-field" v-model.number="strokeWidth" min="0.1" max="5" step="0.1"/>
          </label>
          <label v-if="currentTool === 'text'" class="field-label">Шрифт
            <input type="number" class="input-field" v-model.number="fontSize" min="4" max="30"/>
          </label>
          <label v-if="currentTool === 'text'" class="field-label">Текст
            <input type="text" class="input-field" v-model="textContent"/>
          </label>
        </div>

        <div v-if="selectedElement" class="sidebar-section">
          <h3>Элемент: {{ selectedElement.type }}</h3>
          <label class="field-label">X
            <input type="number" class="input-field" :value="selectedElement.x"
                   @input="updateElementProp('x', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
          </label>
          <label class="field-label">Y
            <input type="number" class="input-field" :value="selectedElement.y"
                   @input="updateElementProp('y', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
          </label>
          <label class="field-label">Поворот
            <input type="number" class="input-field" :value="selectedElement.rotation"
                   @input="updateElementProp('rotation', Number(($event.target as HTMLInputElement).value))"/>
          </label>
          <label class="field-label">Прозрачность
            <input type="range" min="0" max="1" step="0.05" :value="selectedElement.opacity"
                   @input="updateElementProp('opacity', Number(($event.target as HTMLInputElement).value))"/>
          </label>

          <div v-if="selectedElement.type === 'line'">
            <label class="field-label">x1
              <input type="number" class="input-field" :value="selectedElement.data.x1"
                     @input="updateElementData('x1', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">y1
              <input type="number" class="input-field" :value="selectedElement.data.y1"
                     @input="updateElementData('y1', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">x2
              <input type="number" class="input-field" :value="selectedElement.data.x2"
                     @input="updateElementData('x2', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">y2
              <input type="number" class="input-field" :value="selectedElement.data.y2"
                     @input="updateElementData('y2', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
          </div>

          <div v-if="selectedElement.type === 'rect'">
            <label class="field-label">Ширина
              <input type="number" class="input-field" :value="selectedElement.data.width"
                     @input="updateElementData('width', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">Высота
              <input type="number" class="input-field" :value="selectedElement.data.height"
                     @input="updateElementData('height', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">rx
              <input type="number" class="input-field" :value="selectedElement.data.rx"
                     @input="updateElementData('rx', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
          </div>

          <div v-if="selectedElement.type === 'circle'">
            <label class="field-label">cx
              <input type="number" class="input-field" :value="selectedElement.data.cx"
                     @input="updateElementData('cx', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">cy
              <input type="number" class="input-field" :value="selectedElement.data.cy"
                     @input="updateElementData('cy', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">r
              <input type="number" class="input-field" :value="selectedElement.data.r"
                     @input="updateElementData('r', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
          </div>

          <div v-if="selectedElement.type === 'ellipse'">
            <label class="field-label">cx
              <input type="number" class="input-field" :value="selectedElement.data.cx"
                     @input="updateElementData('cx', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">cy
              <input type="number" class="input-field" :value="selectedElement.data.cy"
                     @input="updateElementData('cy', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">rx
              <input type="number" class="input-field" :value="selectedElement.data.rx"
                     @input="updateElementData('rx', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
            <label class="field-label">ry
              <input type="number" class="input-field" :value="selectedElement.data.ry"
                     @input="updateElementData('ry', Number(($event.target as HTMLInputElement).value))" step="0.5"/>
            </label>
          </div>

          <div v-if="selectedElement.type === 'text'">
            <label class="field-label">Текст
              <input type="text" class="input-field" :value="selectedElement.data.text"
                     @input="updateElementData('text', ($event.target as HTMLInputElement).value)"/>
            </label>
            <label class="field-label">Размер шрифта
              <input type="number" class="input-field" :value="selectedElement.data.fontSize"
                     @input="updateElementData('fontSize', Number(($event.target as HTMLInputElement).value))"/>
            </label>
          </div>

          <div v-if="selectedElement.type === 'polyline'">
            <label class="field-label">Точки
              <textarea class="input-field textarea" :value="selectedElement.data.points"
                        @input="updateElementData('points', ($event.target as HTMLInputElement).value)"/>
            </label>
          </div>

          <div v-if="selectedElement.type === 'path'">
            <label class="field-label">D
              <textarea class="input-field textarea" :value="selectedElement.data.d"
                        @input="updateElementData('d', ($event.target as HTMLInputElement).value)"/>
            </label>
          </div>

          <div class="field-label" style="margin-top: 8px">
            <label class="check-label">
              <input type="checkbox" :checked="selectedElement.locked"
                     @change="updateElementProp('locked', ($event.target as HTMLInputElement).checked)"/>
              Заблокировать
            </label>
          </div>

          <button class="btn-danger" @click="deleteSelected">Удалить элемент</button>
        </div>

        <div class="sidebar-section">
          <h3>Экспорт</h3>
          <div class="export-btns">
            <button class="btn-export" @click="copySvgToClipboard">Копировать SVG</button>
            <button class="btn-export btn-export-save" @click="exportSvg">Сохранить в библиотеку</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.editor-root {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #1a1d23;
  color: #c8cdd5;
  font-size: 13px;
}

.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: #23272e;
  border-bottom: 1px solid #3a3f4a;
  flex-wrap: wrap;
  min-height: 44px;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.toolbar-label {
  font-size: 10px;
  color: #7a8290;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-right: 4px;
  white-space: nowrap;
}

.toolbar-sep {
  width: 1px;
  height: 24px;
  background: #3a3f4a;
  margin: 0 4px;
}

.tool-row {
  display: flex;
  gap: 2px;
}

.tool-btn {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  background: #2a2e36;
  border: 1px solid #3a3f4a;
  border-radius: 4px;
  color: #c8cdd5;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.1s;
}

.tool-btn:hover {
  background: #353a44;
  border-color: #5a9cff;
}

.tool-btn.active {
  background: #1a4a8a;
  border-color: #5a9cff;
  color: #fff;
}

.btn-mode {
  padding: 4px 10px;
  background: #2a2e36;
  border: 1px solid #3a3f4a;
  border-radius: 4px;
  color: #c8cdd5;
  cursor: pointer;
  font-size: 12px;
  white-space: nowrap;
}

.btn-mode:hover {
  background: #353a44;
  border-color: #5a9cff;
}

.check-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  cursor: pointer;
  white-space: nowrap;
}

.check-label input {
  width: 14px;
  height: 14px;
}

.input-sm {
  width: 40px;
  height: 24px;
  background: #2a2e36;
  border: 1px solid #3a3f4a;
  border-radius: 3px;
  color: #c8cdd5;
  text-align: center;
  font-size: 11px;
  padding: 0 2px;
}

.editor-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.canvas-area {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #f5f7fa;
}

.editor-canvas {
  width: 100%;
  height: 100%;
  cursor: crosshair;
}

.editor-canvas .selected {
  outline: 1.5px dashed #5a9cff;
  outline-offset: 1px;
}

.canvas-coords {
  position: absolute;
  bottom: 8px;
  left: 12px;
  font-size: 11px;
  color: #6a7080;
  background: rgba(255, 255, 255, 0.85);
  padding: 2px 8px;
  border-radius: 3px;
}

.editor-sidebar {
  width: 260px;
  background: #23272e;
  border-left: 1px solid #3a3f4a;
  overflow-y: auto;
}

.sidebar-section {
  padding: 12px 14px;
  border-bottom: 1px solid #3a3f4a;
}

.sidebar-section h3 {
  margin: 0 0 8px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #7a8290;
}

.field-label {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-bottom: 8px;
  font-size: 11px;
  color: #9aa0ac;
}

.input-field {
  width: 100%;
  height: 28px;
  background: #2a2e36;
  border: 1px solid #3a3f4a;
  border-radius: 4px;
  color: #c8cdd5;
  padding: 0 8px;
  font-size: 12px;
}

.input-field:focus {
  outline: none;
  border-color: #5a9cff;
}

.textarea {
  height: 60px;
  padding: 6px 8px;
  resize: vertical;
  font-family: monospace;
  font-size: 11px;
}

.color-row {
  display: flex;
  gap: 6px;
  align-items: center;
}

.color-row input[type="color"] {
  width: 28px;
  height: 28px;
  border: 1px solid #3a3f4a;
  border-radius: 4px;
  cursor: pointer;
  padding: 2px;
  background: #2a2e36;
}

.color-row .input-field {
  flex: 1;
}

.btn-danger {
  width: 100%;
  padding: 6px;
  background: #5a2020;
  border: 1px solid #8a3030;
  border-radius: 4px;
  color: #f0a0a0;
  cursor: pointer;
  font-size: 12px;
  margin-top: 8px;
}

.btn-danger:hover {
  background: #7a2020;
}

.export-btns {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.btn-export {
  padding: 8px;
  background: #2a4a2a;
  border: 1px solid #3a6a3a;
  border-radius: 4px;
  color: #a0f0a0;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
}

.btn-export:hover {
  background: #3a6a3a;
}

.btn-export-save {
  background: #2a3a5a;
  border-color: #3a5a8a;
  color: #a0c0f0;
}

.btn-export-save:hover {
  background: #3a5a8a;
}

input[type="range"] {
  width: 100%;
  accent-color: #5a9cff;
}
</style>
