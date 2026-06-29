<template>
  <header class="ribbon-bar">
    <div class="ribbon-title">
      <strong>ElectroScheme Studio</strong>
      <span>Редактор схем</span>
    </div>

    <nav class="ribbon-tabs" aria-label="Лента команд редактора">
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
        <h3>Инструменты</h3>
        <div class="button-row">
          <button type="button" :class="{ active: activeMode === 'select' }" @click="$emit('setMode', 'select')">↖ Выбор</button>
          <button type="button" :class="{ active: activeMode === 'pan' }" @click="$emit('setMode', 'pan')">✋ Панорама</button>
        </div>
      </section>

      <section class="ribbon-group wide">
        <h3>Буфер</h3>
        <div class="button-row">
          <button type="button" @click="$emit('command', 'copy')">⧉ Копировать</button>
          <button type="button" @click="$emit('setMode', 'copy_by_reference')">⌖ С базовой точкой</button>
          <button type="button" @click="$emit('command', 'paste')">▣ Вставить</button>
          <button type="button" @click="$emit('setMode', 'paste_by_point')">⌖ Вставить по точке</button>
        </div>
      </section>

      <section class="ribbon-group">
        <h3>Объекты</h3>
        <div class="button-row">
          <button type="button" @click="$emit('command', 'create_sample_busbar')">＋ Шина</button>
          <button type="button" @click="$emit('command', 'create_text')">Текст</button>
        </div>
      </section>

      <section class="ribbon-group">
        <h3>Поворот</h3>
        <div class="button-row compact">
          <button type="button" @click="$emit('command', 'rotate_0')">0°</button>
          <button type="button" @click="$emit('command', 'rotate_90')">+90°</button>
          <button type="button" @click="$emit('command', 'rotate_minus_90')">-90°</button>
        </div>
      </section>

      <section class="ribbon-group canvas-settings">
        <h3>Канвас</h3>
        <div class="settings-grid">
          <label>
            Масштаб
            <input
              :value="settings.zoom"
              type="range"
              min="0.5"
              max="2.5"
              step="0.1"
              @input="onNumberSetting('zoom', $event)"
            />
            <span>{{ Math.round(settings.zoom * 100) }}%</span>
          </label>

          <label>
            Шаг сетки
            <input
              :value="settings.gridStep"
              type="number"
              min="2"
              max="100"
              step="1"
              @change="onNumberSetting('gridStep', $event)"
            />
          </label>

          <label>
            Допуск
            <input
              :value="settings.snapTolerance"
              type="number"
              min="1"
              max="50"
              step="1"
              @change="onNumberSetting('snapTolerance', $event)"
            />
          </label>
        </div>
      </section>

      <section class="ribbon-group snap-settings">
        <h3>Привязки</h3>
        <div class="toggle-row">
          <label><input :checked="settings.gridVisible" type="checkbox" @change="onBooleanSetting('gridVisible', $event)" /> Сетка</label>
          <label><input :checked="settings.guidesVisible" type="checkbox" @change="onBooleanSetting('guidesVisible', $event)" /> Направляющие</label>
          <label><input :checked="settings.snapEnabled" type="checkbox" @change="onBooleanSetting('snapEnabled', $event)" /> Привязки</label>
          <label><input :checked="settings.snapGrid" type="checkbox" @change="onBooleanSetting('snapGrid', $event)" /> к сетке</label>
          <label><input :checked="settings.snapSlots" type="checkbox" @change="onBooleanSetting('snapSlots', $event)" /> к ячейкам</label>
          <label><input :checked="settings.snapObjects" type="checkbox" @change="onBooleanSetting('snapObjects', $event)" /> к объектам</label>
        </div>
      </section>

      <section class="ribbon-group">
        <h3>Отладка</h3>
        <div class="button-row">
          <button type="button" @click="$emit('command', 'clear_generated')">Очистить вставки</button>
        </div>
      </section>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { CanvasSettings } from '../../lib/editor/canvasSettings'
import { normalizeCanvasSettings } from '../../lib/editor/canvasSettings'
import type { EditorCommand, EditorInteractionMode } from '../../lib/editor/interactionModes'

const props = defineProps<{
  activeMode: EditorInteractionMode
  settings: CanvasSettings
}>()

const emit = defineEmits<{
  setMode: [mode: EditorInteractionMode]
  command: [command: EditorCommand]
  settingsChange: [settings: CanvasSettings]
}>()

const tabs = ['Главная', 'Вставка', 'Символы', 'Шины / ячейки', 'Соединения', 'Текст', 'Вид', 'Экспорт']
const activeTab = ref('Главная')

function patchSettings(patch: Partial<CanvasSettings>): void {
  emit('settingsChange', normalizeCanvasSettings({ ...props.settings, ...patch }))
}

function onBooleanSetting(key: keyof CanvasSettings, event: Event): void {
  const checked = (event.target as HTMLInputElement).checked
  patchSettings({ [key]: checked } as Partial<CanvasSettings>)
}

function onNumberSetting(key: keyof CanvasSettings, event: Event): void {
  const value = Number((event.target as HTMLInputElement).value)
  if (!Number.isFinite(value)) return
  patchSettings({ [key]: value } as Partial<CanvasSettings>)
}
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
  min-width: 132px;
  padding: 8px;
  border: 1px solid #dbeafe;
  border-radius: 10px;
  background: #f8fbff;
}

.ribbon-group.wide {
  min-width: 310px;
}

.ribbon-group.canvas-settings {
  min-width: 260px;
}

.ribbon-group.snap-settings {
  min-width: 310px;
}

.ribbon-group h3 {
  margin: 0 0 6px;
  color: #475569;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.button-row,
.toggle-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.button-row.compact {
  max-width: 128px;
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
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
}

.button-row button:hover {
  background: #eff6ff;
}

.button-row button.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.settings-grid {
  display: grid;
  grid-template-columns: 1fr 78px 74px;
  gap: 8px;
  align-items: end;
}

.settings-grid label,
.toggle-row label {
  display: grid;
  gap: 4px;
  color: #334155;
  font-size: 11px;
  font-weight: 800;
}

.settings-grid input[type="number"] {
  width: 100%;
  border: 1px solid #bfdbfe;
  border-radius: 7px;
  padding: 5px 6px;
}

.settings-grid span {
  color: #64748b;
  font-size: 11px;
}

.toggle-row label {
  display: flex;
  align-items: center;
  gap: 5px;
  min-width: 84px;
}
</style>