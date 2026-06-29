<template>
  <section class="parametric-busbar-panel" aria-label="Parametric busbar model">
    <header class="panel-header">
      <div>
        <p class="eyebrow">Parametric symbol</p>
        <h2>Busbar generator</h2>
        <p class="description">
          Side-aware labels, larger end offset and draggable/rotatable bus caption.
        </p>
      </div>
      <button type="button" class="primary-button" :disabled="loading" @click="refreshPreview">
        {{ loading ? 'Generating…' : 'Generate preview' }}
      </button>
    </header>

    <div v-if="error" class="status error">{{ error }}</div>

    <div class="layout">
      <aside class="controls">
        <label class="field">Name
          <input v-model="form.name_ru" type="text" />
        </label>

        <label class="field">Voltage class, kV
          <input v-model.number="form.voltage_kv" type="number" min="0.4" max="1150" step="0.1" />
        </label>

        <label class="field">Connection points
          <input v-model.number="form.connection_count" type="number" min="0" max="64" step="1" />
        </label>

        <label class="field">Spacing between points
          <input v-model.number="form.connection_spacing" type="number" min="5" max="300" step="0.25" />
        </label>

        <label class="field">End slot offset
          <input v-model.number="form.end_slot_offset" type="number" min="0" max="300" step="0.25" />
        </label>

        <label class="check-field">
          <input v-model="form.fit_length_to_slots" type="checkbox" />
          Fit bus length to offset + spacing
        </label>

        <label class="field">Bus thickness, mm
          <input v-model.number="form.thickness_mm" type="number" min="2" max="60" step="0.5" />
        </label>

        <label class="field">Slot diameter
          <input v-model.number="form.slot_diameter" type="number" min="2" max="30" step="0.5" />
        </label>

        <label class="field">Connection side
          <select v-model="form.connection_side">
            <option value="top">Top / left</option>
            <option value="bottom">Bottom / right</option>
            <option value="both">Both sides</option>
          </select>
        </label>

        <label class="field">Orientation
          <select v-model="form.orientation">
            <option value="horizontal">Horizontal</option>
            <option value="vertical">Vertical</option>
          </select>
        </label>

        <section class="numbering-box">
          <label class="check-field">
            <input v-model="form.bay_numbering_enabled" type="checkbox" />
            Number cells / bay slots
          </label>

          <label class="check-field">
            <input v-model="form.bay_label_both_side_separate_rows" type="checkbox" />
            Separate label rows for both-side busbar
          </label>

          <label class="field">Number style
            <select v-model="form.bay_numbering_style">
              <option value="number_only">Number only</option>
              <option value="prefix_number">Prefix + number</option>
            </select>
          </label>

          <label class="field">Start number
            <input v-model.number="form.bay_numbering_start" type="number" min="0" max="9999" step="1" />
          </label>

          <label class="field">Step
            <input v-model.number="form.bay_numbering_step" type="number" min="1" max="100" step="1" />
          </label>

          <label class="field">Label offset
            <input v-model.number="form.bay_label_offset" type="number" min="0" max="120" step="1" />
          </label>
        </section>

        <section class="numbering-box">
          <h3>Bus caption</h3>

          <label class="field">Caption
            <input v-model="form.bus_label" type="text" maxlength="64" />
          </label>

          <label class="field">Caption position
            <select v-model="form.bus_label_position">
              <option value="auto">Auto</option>
              <option value="right">Right</option>
              <option value="left">Left</option>
              <option value="top">Top</option>
              <option value="bottom">Bottom</option>
            </select>
          </label>

          <label class="field">Caption gap
            <input v-model.number="form.bus_label_gap" type="number" min="0" max="240" step="1" />
          </label>

          <label class="field">Manual offset X
            <input v-model.number="form.bus_label_offset_x" type="number" min="-1000" max="1000" step="1" />
          </label>

          <label class="field">Manual offset Y
            <input v-model.number="form.bus_label_offset_y" type="number" min="-1000" max="1000" step="1" />
          </label>

          <label class="field">Rotation mode
            <select v-model="form.bus_label_rotation_mode">
              <option value="auto">Auto</option>
              <option value="manual">Manual</option>
            </select>
          </label>

          <div class="preset-row">
            <button type="button" @click="setRotation(0)">0°</button>
            <button type="button" @click="setRotation(90)">+90°</button>
            <button type="button" @click="setRotation(-90)">-90°</button>
            <button type="button" @click="setRotation(180)">180°</button>
          </div>
        </section>
      </aside>

      <main class="preview-area">
        <p class="hint">Tip: drag the bus caption directly in the preview. It moves immediately and the model offsets are refreshed on release.</p>

        <div class="preview-card">
          <svg
            v-if="preview"
            ref="previewSvg"
            class="preview-svg"
            :viewBox="viewBoxString"
            role="img"
            :aria-label="preview.name_ru"
            @pointerdown="onPreviewPointerDown"
            v-html="preview.svg_fragment"
          />
          <div v-else class="status">No preview yet.</div>
        </div>

        <div v-if="preview" class="summary">
          <article><span>Points</span><strong>{{ preview.bay_slots.length }}</strong></article>
          <article><span>End offset</span><strong>{{ preview.capabilities.busbar.end_slot_offset }}</strong></article>
          <article><span>Caption X/Y</span><strong>{{ form.bus_label_offset_x }}, {{ form.bus_label_offset_y }}</strong></article>
          <article><span>Rotation</span><strong>{{ form.bus_label_rotation_mode }} {{ form.bus_label_rotation_deg }}°</strong></article>
        </div>

        <details v-if="preview" class="terminal-list" open>
          <summary>Bay slot data</summary>
          <table>
            <thead>
              <tr>
                <th>Label</th>
                <th>Slot</th>
                <th>Side</th>
                <th>Bus point</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="slot in preview.bay_slots" :key="slot.id">
                <td><strong>{{ slot.label || '—' }}</strong></td>
                <td><code>{{ slot.id }}</code></td>
                <td>{{ slot.side }}</td>
                <td>{{ slot.bus_x.toFixed(2) }}, {{ slot.bus_y.toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </details>
      </main>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'

type BusbarConnectionSide = 'top' | 'bottom' | 'both'
type BusbarOrientation = 'horizontal' | 'vertical'
type BusLabelPosition = 'auto' | 'right' | 'left' | 'top' | 'bottom'
type BayNumberingStyle = 'number_only' | 'prefix_number'
type RotationMode = 'auto' | 'manual'

type BusbarPreviewRequest = {
  id: string
  name_ru: string
  voltage_kv: number
  length: number
  fit_length_to_slots: boolean
  connection_count: number
  connection_side: BusbarConnectionSide
  orientation: BusbarOrientation
  thickness_mm: number
  connection_spacing: number
  end_slot_offset: number
  slot_diameter: number
  margin: number
  bay_depth: number
  bay_numbering_enabled: boolean
  bay_numbering_prefix: string
  bay_numbering_style: BayNumberingStyle
  bay_numbering_start: number
  bay_numbering_step: number
  bay_label_offset: number
  bay_label_both_side_separate_rows: boolean
  bus_label: string
  bus_label_position: BusLabelPosition
  bus_label_gap: number
  bus_label_offset_x: number
  bus_label_offset_y: number
  bus_label_rotation_mode: RotationMode
  bus_label_rotation_deg: number
}

type ParametricBaySlot = {
  id: string
  terminal_id: string
  index: number
  side: string
  bus_x: number
  bus_y: number
  label: string
}

type ParametricSymbolPreview = {
  id: string
  name_ru: string
  kind: 'busbar'
  viewBox: { x: number; y: number; width: number; height: number }
  svg_fragment: string
  bay_slots: ParametricBaySlot[]
  capabilities: Record<string, any>
}

const loading = ref(false)
const error = ref('')
const preview = ref<ParametricSymbolPreview | null>(null)
const previewSvg = ref<SVGSVGElement | null>(null)

const form = reactive<BusbarPreviewRequest>({
  id: 'param_busbar_1',
  name_ru: 'Шина 10 кВ',
  voltage_kv: 10,
  length: 260,
  fit_length_to_slots: true,
  connection_count: 5,
  connection_side: 'bottom',
  orientation: 'horizontal',
  thickness_mm: 12,
  connection_spacing: 48,
  end_slot_offset: 14,
  slot_diameter: 8,
  margin: 24,
  bay_depth: 90,
  bay_numbering_enabled: true,
  bay_numbering_prefix: 'Яч. ',
  bay_numbering_style: 'number_only',
  bay_numbering_start: 1,
  bay_numbering_step: 1,
  bay_label_offset: 16,
  bay_label_both_side_separate_rows: true,
  bus_label: '1С 10 кВ',
  bus_label_position: 'auto',
  bus_label_gap: 34,
  bus_label_offset_x: 0,
  bus_label_offset_y: 0,
  bus_label_rotation_mode: 'auto',
  bus_label_rotation_deg: 0,
})

const viewBoxString = computed(() => {
  if (!preview.value) return '0 0 100 100'
  const vb = preview.value.viewBox
  return `${vb.x} ${vb.y} ${vb.width} ${vb.height}`
})

function setRotation(degrees: number): void {
  form.bus_label_rotation_mode = 'manual'
  form.bus_label_rotation_deg = degrees
  void refreshPreview()
}

function clientToSvgPoint(event: PointerEvent): DOMPoint | null {
  const svg = previewSvg.value
  if (!svg) return null
  const point = svg.createSVGPoint()
  point.x = event.clientX
  point.y = event.clientY
  const ctm = svg.getScreenCTM()
  if (!ctm) return null
  return point.matrixTransform(ctm.inverse())
}

function findBusLabelTarget(start: Element | null): SVGTextElement | null {
  let current: Element | null = start
  while (current && current !== previewSvg.value) {
    if (current.getAttribute('data-role') === 'bus-label') {
      return current as SVGTextElement
    }
    current = current.parentElement
  }
  return null
}

function setLabelVisualPosition(target: SVGTextElement, x: number, y: number): void {
  const rotation = Number(target.getAttribute('data-rotation') ?? '0') || 0
  const roundedX = Math.round(x * 10) / 10
  const roundedY = Math.round(y * 10) / 10
  target.setAttribute('x', String(roundedX))
  target.setAttribute('y', String(roundedY))
  target.setAttribute('transform', `rotate(${rotation} ${roundedX} ${roundedY})`)
}

function onPreviewPointerDown(event: PointerEvent): void {
  const target = findBusLabelTarget(event.target as Element | null)
  if (!target) return

  event.preventDefault()

  const start = clientToSvgPoint(event)
  if (!start) return

  const baseX = Number(target.getAttribute('x') ?? '0') || 0
  const baseY = Number(target.getAttribute('y') ?? '0') || 0
  const startOffsetX = form.bus_label_offset_x
  const startOffsetY = form.bus_label_offset_y
  const pointerId = event.pointerId

  target.style.cursor = 'grabbing'
  previewSvg.value?.setPointerCapture?.(pointerId)

  const move = (moveEvent: PointerEvent) => {
    if (moveEvent.pointerId !== pointerId) return
    const current = clientToSvgPoint(moveEvent)
    if (!current) return
    const dx = current.x - start.x
    const dy = current.y - start.y
    form.bus_label_offset_x = Math.round((startOffsetX + dx) * 10) / 10
    form.bus_label_offset_y = Math.round((startOffsetY + dy) * 10) / 10
    setLabelVisualPosition(target, baseX + dx, baseY + dy)
  }

  const up = (upEvent: PointerEvent) => {
    if (upEvent.pointerId !== pointerId) return
    target.style.cursor = 'grab'
    previewSvg.value?.releasePointerCapture?.(pointerId)
    window.removeEventListener('pointermove', move)
    window.removeEventListener('pointerup', up)
    void refreshPreview()
  }

  window.addEventListener('pointermove', move)
  window.addEventListener('pointerup', up)
}

async function refreshPreview(): Promise<void> {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch('/api/parametric-symbols/busbar/preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    preview.value = (await response.json()) as ParametricSymbolPreview
  } catch (err) {
    error.value = err instanceof Error ? err.message : String(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  void refreshPreview()
})
</script>

<style scoped>
.parametric-busbar-panel {
  margin: 18px;
  padding: 18px;
  border: 1px solid rgba(59, 130, 246, 0.25);
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(239, 246, 255, 0.95), rgba(255, 255, 255, 0.98));
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
  color: #0f172a;
}

.panel-header { display: flex; justify-content: space-between; gap: 16px; margin-bottom: 16px; }
.eyebrow { margin: 0 0 4px; font-size: 12px; font-weight: 800; letter-spacing: 0.08em; color: #2563eb; text-transform: uppercase; }
.panel-header h2 { margin: 0; font-size: 22px; }
.description { margin: 4px 0 0; color: #64748b; }

.primary-button {
  align-self: flex-start;
  border: 0;
  border-radius: 999px;
  padding: 10px 16px;
  background: #2563eb;
  color: white;
  font-weight: 800;
  cursor: pointer;
}

.primary-button:disabled { opacity: 0.55; cursor: default; }
.status { padding: 16px; border-radius: 12px; background: #eff6ff; color: #1e40af; }
.status.error { background: #fef2f2; color: #991b1b; }
.layout { display: grid; grid-template-columns: minmax(250px, 320px) 1fr; gap: 16px; }
.controls, .preview-area { border: 1px solid #dbeafe; border-radius: 14px; background: white; padding: 14px; }

.field {
  display: grid;
  gap: 6px;
  margin-bottom: 12px;
  color: #475569;
  font-size: 12px;
  font-weight: 800;
}

.field input, .field select {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 9px 10px;
  color: #0f172a;
  background: white;
}

.check-field { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; color: #334155; font-size: 12px; font-weight: 800; }
.numbering-box { margin-top: 14px; padding: 12px; border: 1px solid #dbeafe; border-radius: 12px; background: #eff6ff; }
.numbering-box h3 { margin: 0 0 10px; font-size: 14px; }
.preset-row { display: flex; flex-wrap: wrap; gap: 6px; }
.preset-row button { border: 1px solid #bfdbfe; border-radius: 999px; padding: 6px 9px; background: white; color: #1d4ed8; cursor: pointer; font-weight: 800; }

.preview-card {
  min-height: 360px;
  display: grid;
  place-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background:
    linear-gradient(90deg, rgba(148, 163, 184, 0.14) 1px, transparent 1px),
    linear-gradient(rgba(148, 163, 184, 0.14) 1px, transparent 1px);
  background-size: 18px 18px;
  --busbar-color: #6d0ad6;
  --slot-stroke: #ffffff;
  --label-color: #111111;
}

.preview-svg { width: 96%; max-height: 340px; touch-action: none; }
.preview-svg :deep([data-role='bus-label']) { cursor: grab; user-select: none; }
.hint { margin: 0 0 10px; color: #64748b; font-size: 12px; font-weight: 700; }
.summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin: 12px 0; }
.summary article { border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; }
.summary span { display: block; color: #64748b; font-size: 12px; }
.summary strong { display: block; margin-top: 3px; font-size: 18px; }
.terminal-list { margin-top: 12px; }
.terminal-list table { width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 12px; }
.terminal-list th, .terminal-list td { border-bottom: 1px solid #e2e8f0; padding: 6px 8px; text-align: left; }

@media (max-width: 980px) {
  .layout { grid-template-columns: 1fr; }
}
</style>