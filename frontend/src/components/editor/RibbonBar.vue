<template>
  <header class="ribbon-bar">
    <div class="ribbon-title">
      <strong>ElectroScheme Studio</strong>
      <span>Редактор схем</span>
    </div>

    <nav class="ribbon-tabs" aria-label="Лента команд редактора">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        :class="{ active: tab.id === activeTab }"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </nav>

    <div class="ribbon-content">
      <template v-if="activeTab === 'home'">
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
      </template>

      <template v-else-if="activeTab === 'insert'">
        <section class="ribbon-group">
          <h3>Объекты</h3>
          <div class="button-row">
            <button type="button" @click="$emit('command', 'create_sample_busbar')">＋ Шина</button>
            <button type="button" @click="$emit('command', 'create_text')">Текст</button>
          </div>
        </section>

        <section class="ribbon-group">
          <h3>Направляющие</h3>
          <div class="button-row">
            <button type="button" @click="$emit('command', 'create_vertical_guide')">Вертикальная</button>
            <button type="button" @click="$emit('command', 'create_horizontal_guide')">Горизонтальная</button>
          </div>
        </section>
      </template>

      <template v-else-if="activeTab === 'busbars'">
        <section class="ribbon-group wide">
          <h3>Шины / ячейки</h3>
          <div class="button-row">
            <button type="button" @click="$emit('command', 'create_sample_busbar')">Добавить шину</button>
            <button type="button" @click="$emit('command', 'add_busbar_slot')">+ Ячейка</button>
            <button type="button" @click="$emit('command', 'remove_busbar_slot')">− Ячейка</button>
          </div>
        </section>
      </template>

      <template v-else-if="activeTab === 'view'">
        <section class="ribbon-group canvas-settings">
          <h3>Канвас</h3>
          <div class="settings-grid">
            <label>
              Шаг сетки
              <input :value="settings.gridStep" type="number" min="2" max="100" step="1" @change="onNumberSetting('gridStep', $event)" />
            </label>
            <label>
              Допуск
              <input :value="settings.snapTolerance" type="number" min="1" max="50" step="1" @change="onNumberSetting('snapTolerance', $event)" />
            </label>
            <label>
              Лист
              <select :value="settings.pageFormat" @change="onTextSetting('pageFormat', $event)">
                <option value="A4">A4</option>
                <option value="A3">A3</option>
                <option value="A2">A2</option>
                <option value="A1">A1</option>
                <option value="A0">A0</option>
              </select>
            </label>
            <label>
              Ориентация
              <select :value="settings.pageOrientation" @change="onTextSetting('pageOrientation', $event)">
                <option value="landscape">Альбомная</option>
                <option value="portrait">Книжная</option>
              </select>
            </label>
          </div>
        </section>

        <section class="ribbon-group snap-settings">
          <h3>Отображение и привязки</h3>
          <div class="toggle-row">
            <label><input :checked="settings.rulersVisible" type="checkbox" @change="onBooleanSetting('rulersVisible', $event)" /> Линейки</label>
            <label><input :checked="settings.pageVisible" type="checkbox" @change="onBooleanSetting('pageVisible', $event)" /> Лист ISO</label>
            <label><input :checked="settings.originVisible" type="checkbox" @change="onBooleanSetting('originVisible', $event)" /> Центр 0,0</label>
            <label><input :checked="settings.gridVisible" type="checkbox" @change="onBooleanSetting('gridVisible', $event)" /> Сетка</label>
            <label><input :checked="settings.guidesVisible" type="checkbox" @change="onBooleanSetting('guidesVisible', $event)" /> Направляющие</label>
            <label><input :checked="settings.snapEnabled" type="checkbox" @change="onBooleanSetting('snapEnabled', $event)" /> Привязки</label>
            <label><input :checked="settings.snapGrid" type="checkbox" @change="onBooleanSetting('snapGrid', $event)" /> к сетке</label>
            <label><input :checked="settings.snapSlots" type="checkbox" @change="onBooleanSetting('snapSlots', $event)" /> к ячейкам</label>
            <label><input :checked="settings.snapObjects" type="checkbox" @change="onBooleanSetting('snapObjects', $event)" /> к объектам</label>
            <label><input :checked="settings.snapGuides" type="checkbox" @change="onBooleanSetting('snapGuides', $event)" /> к направляющим</label>
          </div>
        </section>

        <section class="ribbon-group">
          <h3>Направляющие</h3>
          <div class="button-row">
            <button type="button" @click="$emit('command', 'create_vertical_guide')">Вертикальная</button>
            <button type="button" @click="$emit('command', 'create_horizontal_guide')">Горизонтальная</button>
            <button type="button" @click="$emit('command', 'clear_guides')">Очистить</button>
          </div>
        </section>
      </template>

      <template v-else-if="activeTab === 'text'">
        <section class="ribbon-group">
          <h3>Текст</h3>
          <div class="button-row">
            <button type="button" @click="$emit('command', 'create_text')">Добавить текст</button>
            <button type="button" @click="$emit('command', 'rotate_0')">0°</button>
            <button type="button" @click="$emit('command', 'rotate_90')">+90°</button>
            <button type="button" @click="$emit('command', 'rotate_minus_90')">-90°</button>
          </div>
        </section>
      </template>

      <template v-else>
        <section class="ribbon-group placeholder">
          <h3>{{ activeTabLabel }}</h3>
          <p>Раздел подготовлен под следующие редакторские команды.</p>
        </section>
      </template>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
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

const tabs = [
  { id: 'home', label: 'Главная' },
  { id: 'insert', label: 'Вставка' },
  { id: 'symbols', label: 'Символы' },
  { id: 'busbars', label: 'Шины / ячейки' },
  { id: 'connections', label: 'Соединения' },
  { id: 'text', label: 'Текст' },
  { id: 'view', label: 'Вид' },
  { id: 'export', label: 'Экспорт' },
] as const

const activeTab = ref<(typeof tabs)[number]['id']>('home')
const activeTabLabel = computed(() => tabs.find((tab) => tab.id === activeTab.value)?.label ?? activeTab.value)

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

function onTextSetting(key: keyof CanvasSettings, event: Event): void {
  const value = (event.target as HTMLSelectElement).value
  patchSettings({ [key]: value } as Partial<CanvasSettings>)
}
</script>

<style scoped>
.ribbon-bar {
  display: grid;
  grid-template-columns: 230px 1fr;
  grid-template-rows: 32px 80px;
  border-bottom: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #0f172a;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08);
  z-index: 3;
  overflow: hidden;
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

.ribbon-title strong { font-size: 15px; }
.ribbon-title span { color: #cbd5e1; font-size: 12px; }

.ribbon-tabs {
  display: flex;
  align-items: end;
  gap: 2px;
  padding: 4px 8px 0;
  overflow: hidden;
}

.ribbon-tabs button {
  height: 28px;
  border: 1px solid transparent;
  border-bottom: 0;
  border-radius: 8px 8px 0 0;
  padding: 0 10px;
  background: transparent;
  color: #334155;
  cursor: pointer;
  font-weight: 700;
  font-size: 12px;
}

.ribbon-tabs button.active {
  background: white;
  border-color: #cbd5e1;
  color: #1d4ed8;
}

.ribbon-content {
  display: flex;
  align-items: stretch;
  gap: 8px;
  padding: 6px 8px;
  background: white;
  overflow: hidden;
}

.ribbon-group {
  min-width: 132px;
  padding: 7px;
  border: 1px solid #dbeafe;
  border-radius: 10px;
  background: #f8fbff;
  overflow: hidden;
}

.ribbon-group.wide { min-width: 320px; }
.ribbon-group.canvas-settings { min-width: 330px; }
.ribbon-group.snap-settings { min-width: 520px; }
.ribbon-group.placeholder { min-width: 380px; }

.ribbon-group h3 {
  margin: 0 0 5px;
  color: #475569;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.ribbon-group p {
  margin: 0;
  color: #64748b;
  font-size: 12px;
  line-height: 1.35;
}

.button-row,
.toggle-row {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.button-row button {
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: white;
  color: #1e3a8a;
  cursor: pointer;
  font-weight: 800;
  font-size: 12px;
  padding: 6px 8px;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
}

.button-row button:hover { background: #eff6ff; }

.settings-grid {
  display: grid;
  grid-template-columns: 74px 74px 78px 92px;
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

.settings-grid input,
.settings-grid select {
  width: 100%;
  border: 1px solid #bfdbfe;
  border-radius: 7px;
  padding: 5px 6px;
  background: white;
}

.toggle-row label {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 92px;
}
</style>