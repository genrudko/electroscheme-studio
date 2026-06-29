<template>
  <header class="ribbon-bar">
    <div class="ribbon-title">
      <strong>ElectroScheme Studio</strong>
      <span>Editor prototype</span>
    </div>

    <nav class="ribbon-tabs" aria-label="Editor ribbon">
      <button
        v-for="tab in tabs"
        :key="tab"
        type="button"
        :class="{ active: tab === activeTab }"
        @click="activeTab = tab"
      >
        {{ tab }}
      </button>
    </nav>

    <div class="ribbon-content">
      <section class="ribbon-group">
        <h3>Tools</h3>
        <div class="button-row">
          <button type="button" :class="{ active: activeMode === 'select' }" @click="$emit('setMode', 'select')">Select</button>
          <button type="button" :class="{ active: activeMode === 'pan' }" @click="$emit('setMode', 'pan')">Pan</button>
        </div>
      </section>

      <section class="ribbon-group">
        <h3>Clipboard</h3>
        <div class="button-row">
          <button type="button" @click="$emit('command', 'copy')">Copy</button>
          <button type="button" @click="$emit('setMode', 'copy_by_reference')">Copy by reference</button>
          <button type="button" @click="$emit('command', 'paste')">Paste</button>
          <button type="button" @click="$emit('setMode', 'paste_by_point')">Paste by point</button>
        </div>
      </section>

      <section class="ribbon-group">
        <h3>Transform</h3>
        <div class="button-row">
          <button type="button" @click="$emit('command', 'rotate_0')">0°</button>
          <button type="button" @click="$emit('command', 'rotate_90')">+90°</button>
          <button type="button" @click="$emit('command', 'rotate_minus_90')">-90°</button>
        </div>
      </section>

      <section class="ribbon-group wide">
        <h3>Snap</h3>
        <div class="button-row">
          <button type="button" class="active">Grid</button>
          <button type="button">Slots</button>
          <button type="button">Terminals</button>
          <button type="button">Objects</button>
        </div>
      </section>

      <section class="ribbon-group">
        <h3>Debug</h3>
        <div class="button-row">
          <button type="button" @click="$emit('command', 'clear_generated')">Clear generated</button>
        </div>
      </section>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { EditorCommand, EditorInteractionMode } from '../../lib/editor/interactionModes'

defineProps<{
  activeMode: EditorInteractionMode
}>()

defineEmits<{
  setMode: [mode: EditorInteractionMode]
  command: [command: EditorCommand]
}>()

const tabs = ['Home', 'Insert', 'Symbols', 'Busbars / Bays', 'Connections', 'Text', 'View', 'Export']
const activeTab = ref('Home')
</script>

<style scoped>
.ribbon-bar {
  display: grid;
  grid-template-columns: 230px 1fr;
  grid-template-rows: 34px auto;
  border-bottom: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #0f172a;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08);
  z-index: 3;
}

.ribbon-title {
  grid-row: 1 / 3;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 10px 16px;
  border-right: 1px solid #dbe3ef;
  background: #111827;
  color: white;
}

.ribbon-title strong {
  font-size: 15px;
}

.ribbon-title span {
  color: #cbd5e1;
  font-size: 12px;
}

.ribbon-tabs {
  display: flex;
  align-items: end;
  gap: 2px;
  padding: 4px 8px 0;
}

.ribbon-tabs button {
  height: 30px;
  border: 1px solid transparent;
  border-bottom: 0;
  border-radius: 8px 8px 0 0;
  padding: 0 12px;
  background: transparent;
  color: #334155;
  cursor: pointer;
  font-weight: 700;
}

.ribbon-tabs button.active {
  background: white;
  border-color: #cbd5e1;
  color: #1d4ed8;
}

.ribbon-content {
  display: flex;
  gap: 8px;
  padding: 8px;
  background: white;
  overflow-x: auto;
}

.ribbon-group {
  min-width: 130px;
  padding: 8px;
  border: 1px solid #dbeafe;
  border-radius: 10px;
  background: #f8fbff;
}

.ribbon-group.wide {
  min-width: 220px;
}

.ribbon-group h3 {
  margin: 0 0 6px;
  color: #475569;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.button-row button {
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: white;
  color: #1e3a8a;
  cursor: pointer;
  font-weight: 800;
  font-size: 12px;
  padding: 7px 9px;
}

.button-row button.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}
</style>