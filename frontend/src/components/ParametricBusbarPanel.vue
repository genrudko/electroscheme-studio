<template>
  <section class="parametric-busbar-panel" aria-label="Parametric busbar model">
    <header class="panel-header">
      <div>
        <p class="eyebrow">Parametric symbol</p>
        <h2>Busbar generator</h2>
        <p class="description">
          Generate a busbar with terminals, snap anchors and semantic bay slots for future automatic scheme generation.
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

        <label class="field">Voltage, kV
          <input v-model.number="form.voltage_kv" type="number" min="0.4" max="1150" step="0.1" />
        </label>

        <label class="field">Length
          <input v-model.number="form.length" type="number" min="80" max="1200" step="10" />
        </label>

        <label class="field">Connection count
          <input v-model.number="form.connection_count" type="number" min="0" max="64" step="1" />
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

        <label class="field">Stroke width
          <input v-model.number="form.stroke_width" type="number" min="1" max="16" step="0.5" />
        </label>

        <label class="field">Bay depth
          <input v-model.number="form.bay_depth" type="number" min="20" max="260" step="10" />
        </label>
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
            <span>Terminals</span>
            <strong>{{ preview.terminals.length }}</strong>
          </article>
          <article>
            <span>Bay slots</span>
            <strong>{{ preview.bay_slots.length }}</strong>
          </article>
          <article>
            <span>ViewBox</span>
            <strong>{{ Math.round(preview.viewBox.width) }} × {{ Math.round(preview.viewBox.height) }}</strong>
          </article>
          <article>
            <span>Auto layout</span>
            <strong>{{ preview.capabilities.auto_scheme_generation?.can_host_bays ? 'yes' : 'no' }}</strong>
          </article>
        </div>

        <details v-if="preview" class="terminal-list" open>
          <summary>Bay slots for automatic scheme generation</summary>
          <table>
            <thead>
              <tr>
                <th>Slot</th>
                <th>Terminal</th>
                <th>Side</th>
                <th>Bus point</th>
                <th>Equipment anchor</th>
                <th>Route</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="slot in preview.bay_slots" :key="slot.id">
                <td><code>{{ slot.id }}</code></td>
                <td><code>{{ slot.terminal_id }}</code></td>
                <td>{{ slot.side }}</td>
                <td>{{ slot.bus_x.toFixed(1) }}, {{ slot.bus_y.toFixed(1) }}</td>
                <td>{{ slot.equipment_anchor_x.toFixed(1) }}, {{ slot.equipment_anchor_y.toFixed(1) }}</td>
                <td>{{ slot.preferred_routing_direction }}</td>
              </tr>
            </tbody>
          </table>
        </details>

        <details v-if="preview" class="terminal-list">
          <summary>Generated terminals / snap anchors</summary>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Role</th>
                <th>Side</th>
                <th>X</th>
                <th>Y</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="terminal in preview.terminals" :key="terminal.id">
                <td><code>{{ terminal.id }}</code></td>
                <td>{{ terminal.role }}</td>
                <td>{{ terminal.side }}</td>
                <td>{{ terminal.x.toFixed(1) }}</td>
                <td>{{ terminal.y.toFixed(1) }}</td>
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

type BusbarPreviewRequest = {
  id: string
  name_ru: string
  voltage_kv: number
  length: number
  connection_count: number
  connection_side: BusbarConnectionSide
  orientation: BusbarOrientation
  stroke_width: number
  margin: number
  lead_length: number
  bay_depth: number
}

type ParametricTerminal = {
  id: string
  x: number
  y: number
  role: string
  side: string
  index?: number
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
  allowed_equipment_kinds: string[]
  reserved: boolean
}

type ParametricSymbolPreview = {
  id: string
  name_ru: string
  kind: 'busbar'
  viewBox: { x: number; y: number; width: number; height: number }
  svg_fragment: string
  terminals: ParametricTerminal[]
  snap_anchors: ParametricTerminal[]
  bay_slots: ParametricBaySlot[]
  parameters: BusbarPreviewRequest
  capabilities: Record<string, any>
}

const loading = ref(false)
const error = ref('')
const preview = ref<ParametricSymbolPreview | null>(null)

const form = reactive<BusbarPreviewRequest>({
  id: 'param_busbar_1',
  name_ru: 'Шина 35 кВ',
  voltage_kv: 35,
  length: 420,
  connection_count: 8,
  connection_side: 'bottom',
  orientation: 'horizontal',
  stroke_width: 4,
  margin: 20,
  lead_length: 24,
  bay_depth: 90,
})

const viewBoxString = computed(() => {
  if (!preview.value) return '0 0 100 100'
  const vb = preview.value.viewBox
  return `${vb.x} ${vb.y} ${vb.width} ${vb.height}`
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
  grid-template-columns: minmax(220px, 280px) 1fr;
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

.preview-card {
  min-height: 290px;
  display: grid;
  place-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background:
    linear-gradient(90deg, rgba(148, 163, 184, 0.14) 1px, transparent 1px),
    linear-gradient(rgba(148, 163, 184, 0.14) 1px, transparent 1px);
  background-size: 18px 18px;
  color: #4b5563;
  --voltage-color: #4b5563;
  --slot-color: #2563eb;
}

.preview-svg {
  width: 92%;
  max-height: 275px;
}

.summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
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