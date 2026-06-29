<template>
  <section class="parametric-busbar-panel" aria-label="Parametric busbar model">
    <header class="panel-header">
      <div>
        <p class="eyebrow">Parametric symbol</p>
        <h2>Busbar generator</h2>
        <p class="description">
          Visual model aligned to Visio feedback: slots inside the busbar, labels above/aside, adjustable spacing and bus caption.
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
          <input v-model.number="form.connection_spacing" type="number" min="5" max="300" step="1" />
        </label>

        <label class="field">Bus thickness, mm
          <input v-model.number="form.thickness_mm" type="number" min="2" max="60" step="0.5" />
        </label>

        <label class="field">Slot diameter
          <input v-model.number="form.slot_diameter" type="number" min="2" max="30" step="0.5" />
        </label>

        <label class="field">Minimum bar length
          <input v-model.number="form.length" type="number" min="80" max="1600" step="10" />
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

        <label class="field">Bus caption
          <input v-model="form.bus_label" type="text" maxlength="64" />
        </label>

        <label class="field">Bus caption position
          <select v-model="form.bus_label_position">
            <option value="auto">Auto</option>
            <option value="right">Right</option>
            <option value="left">Left</option>
            <option value="top">Top</option>
            <option value="bottom">Bottom</option>
          </select>
        </label>

        <section class="numbering-box">
          <label class="check-field">
            <input v-model="form.bay_numbering_enabled" type="checkbox" />
            Number cells / bay slots
          </label>

          <label class="field">Number style
            <select v-model="form.bay_numbering_style">
              <option value="number_only">Number only</option>
              <option value="prefix_number">Prefix + number</option>
            </select>
          </label>

          <label class="field">Number prefix
            <input v-model="form.bay_numbering_prefix" type="text" maxlength="32" />
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
      </aside>

      <main class="preview-area">
        <div class="preview-card">
          <svg
            v-if="preview"
            class="preview-svg"
            :viewBox="viewBoxString"
            role="img"
            :aria-label="preview.name_ru"
            v-html="preview.svg_fragment"
          />
          <div v-else class="status">No preview yet.</div>
        </div>

        <div v-if="preview" class="summary">
          <article>
            <span>Points</span>
            <strong>{{ preview.bay_slots.length }}</strong>
          </article>
          <article>
            <span>Labels</span>
            <strong>{{ numberedSlotCount }}</strong>
          </article>
          <article>
            <span>Computed length</span>
            <strong>{{ preview.capabilities.busbar.length }}</strong>
          </article>
          <article>
            <span>Thickness</span>
            <strong>{{ preview.capabilities.busbar.thickness_mm }}</strong>
          </article>
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
                <th>Anchor</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="slot in preview.bay_slots" :key="slot.id">
                <td><strong>{{ slot.label || '—' }}</strong></td>
                <td><code>{{ slot.id }}</code></td>
                <td>{{ slot.side }}</td>
                <td>{{ slot.bus_x.toFixed(1) }}, {{ slot.bus_y.toFixed(1) }}</td>
                <td>{{ slot.equipment_anchor_x.toFixed(1) }}, {{ slot.equipment_anchor_y.toFixed(1) }}</td>
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

type BusbarPreviewRequest = {
  id: string
  name_ru: string
  voltage_kv: number
  length: number
  connection_count: number
  connection_side: BusbarConnectionSide
  orientation: BusbarOrientation
  thickness_mm: number
  connection_spacing: number
  slot_diameter: number
  margin: number
  bay_depth: number
  bay_numbering_enabled: boolean
  bay_numbering_prefix: string
  bay_numbering_style: BayNumberingStyle
  bay_numbering_start: number
  bay_numbering_step: number
  bay_label_offset: number
  bus_label: string
  bus_label_position: BusLabelPosition
}

type ParametricBaySlot = {
  id: string
  terminal_id: string
  index: number
  side: string
  bus_x: number
  bus_y: number
  terminal_x: number
  terminal_y: number
  equipment_anchor_x: number
  equipment_anchor_y: number
  preferred_routing_direction: string
  label_number?: number | null
  label: string
  label_x?: number | null
  label_y?: number | null
}

type ParametricSymbolPreview = {
  id: string
  name_ru: string
  kind: 'busbar'
  viewBox: { x: number; y: number; width: number; height: number }
  svg_fragment: string
  bay_slots: ParametricBaySlot[]
  parameters: BusbarPreviewRequest
  capabilities: Record<string, any>
}

const loading = ref(false)
const error = ref('')
const preview = ref<ParametricSymbolPreview | null>(null)

const form = reactive<BusbarPreviewRequest>({
  id: 'param_busbar_1',
  name_ru: 'Шина 10 кВ',
  voltage_kv: 10,
  length: 260,
  connection_count: 5,
  connection_side: 'bottom',
  orientation: 'horizontal',
  thickness_mm: 12,
  connection_spacing: 48,
  slot_diameter: 8,
  margin: 24,
  bay_depth: 90,
  bay_numbering_enabled: true,
  bay_numbering_prefix: 'Яч. ',
  bay_numbering_style: 'number_only',
  bay_numbering_start: 1,
  bay_numbering_step: 1,
  bay_label_offset: 14,
  bus_label: '1С 10 кВ',
  bus_label_position: 'auto',
})

const viewBoxString = computed(() => {
  if (!preview.value) return '0 0 100 100'
  const vb = preview.value.viewBox
  return `${vb.x} ${vb.y} ${vb.width} ${vb.height}`
})

const numberedSlotCount = computed(() => {
  return preview.value?.bay_slots.filter((slot) => Boolean(slot.label)).length ?? 0
})

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

.panel-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #2563eb;
  text-transform: uppercase;
}

.panel-header h2 {
  margin: 0;
  font-size: 22px;
}

.description {
  margin: 4px 0 0;
  color: #64748b;
}

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

.primary-button:disabled {
  opacity: 0.55;
  cursor: default;
}

.status {
  padding: 16px;
  border-radius: 12px;
  background: #eff6ff;
  color: #1e40af;
}

.status.error {
  background: #fef2f2;
  color: #991b1b;
}

.layout {
  display: grid;
  grid-template-columns: minmax(250px, 320px) 1fr;
  gap: 16px;
}

.controls,
.preview-area {
  border: 1px solid #dbeafe;
  border-radius: 14px;
  background: white;
  padding: 14px;
}

.field {
  display: grid;
  gap: 6px;
  margin-bottom: 12px;
  color: #475569;
  font-size: 12px;
  font-weight: 800;
}

.field input,
.field select {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 9px 10px;
  color: #0f172a;
  background: white;
}

.check-field {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  color: #334155;
  font-size: 12px;
  font-weight: 800;
}

.numbering-box {
  margin-top: 14px;
  padding: 12px;
  border: 1px solid #dbeafe;
  border-radius: 12px;
  background: #eff6ff;
}

.preview-card {
  min-height: 340px;
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

.preview-svg {
  width: 96%;
  max-height: 320px;
}

.summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 10px;
  margin: 12px 0;
}

.summary article {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 10px;
}

.summary span {
  display: block;
  color: #64748b;
  font-size: 12px;
}

.summary strong {
  display: block;
  margin-top: 3px;
  font-size: 18px;
}

.terminal-list {
  margin-top: 12px;
}

.terminal-list table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
  font-size: 12px;
}

.terminal-list th,
.terminal-list td {
  border-bottom: 1px solid #e2e8f0;
  padding: 6px 8px;
  text-align: left;
}

@media (max-width: 980px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>