<template>
  <header class="ribbon-bar">
    <div class="ribbon-title"><strong>ElectroScheme Studio</strong><span>Редактор схем</span></div>
    <nav class="ribbon-tabs"><button v-for="tab in tabs" :key="tab.id" type="button" :class="{ active: tab.id === activeTab }" @click="activeTab = tab.id">{{ tab.label }}</button></nav>
    <div class="ribbon-content">
      <template v-if="activeTab === 'home'">
        <section class="ribbon-group"><h3>Инструменты</h3><div class="button-row"><button type="button" :class="{ active: activeMode === 'select' }" @click="$emit('setMode','select')">↖ Выбор</button><button type="button" :class="{ active: activeMode === 'pan' }" @click="$emit('setMode','pan')">✋ Панорама</button></div></section>
        <section class="ribbon-group wide"><h3>Буфер</h3><div class="button-row"><button type="button" @click="$emit('command','copy')">⧉ Копировать</button><button type="button" @click="$emit('command','paste')">▣ Вставить</button><button type="button" @click="$emit('setMode','copy_by_reference')">⌖ С базовой точкой</button></div></section>
      </template>
      <template v-else-if="activeTab === 'insert' || activeTab === 'drawing'">
        <section class="ribbon-group wide"><h3>{{ activeTab === 'insert' ? 'Фигуры' : 'Рисование' }}</h3><div class="button-row"><button type="button" @click="$emit('command','create_sample_busbar')">＋ Шина</button><button type="button" @click="$emit('command','create_circuit_breaker')">□ Выключатель</button><button type="button" @click="$emit('command','create_text')">Текст</button><button type="button" @click="$emit('command','create_rectangle')">Прямоугольник</button><button type="button" @click="$emit('command','create_ellipse')">Эллипс</button><button type="button" @click="$emit('command','create_line')">Линия</button></div></section>
      </template>
      <template v-else-if="activeTab === 'view'">
        <section class="ribbon-group canvas-settings"><h3>Канвас</h3><div class="settings-grid"><label>Шаг <input :value="settings.gridStep" type="number" @change="onNumberSetting('gridStep',$event)" /></label><label>Профиль<select :value="settings.displayProfileId" @change="onTextSetting('displayProfileId',$event)"><option value="gost_r_56303_2014">ГОСТ Р 56303-2014</option><option value="sto_fsk_placeholder">СТО ФСК (позже)</option></select></label></div></section>
      </template>
      <template v-else><section class="ribbon-group placeholder"><h3>{{ activeTabLabel }}</h3><p>Раздел подготовлен под следующие команды.</p></section></template>
    </div>
  </header>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
import type { CanvasSettings } from '../../lib/editor/canvasSettings'
import { normalizeCanvasSettings } from '../../lib/editor/canvasSettings'
import type { EditorCommand, EditorInteractionMode } from '../../lib/editor/interactionModes'
const props = defineProps<{ activeMode: EditorInteractionMode; settings: CanvasSettings }>()
const emit = defineEmits<{ setMode: [mode: EditorInteractionMode]; command: [command: EditorCommand]; settingsChange: [settings: CanvasSettings] }>()
const tabs = [{id:'home',label:'Главная'},{id:'insert',label:'Вставка'},{id:'drawing',label:'Рисование'},{id:'symbols',label:'Символы'},{id:'busbars',label:'Шины / ячейки'},{id:'connections',label:'Соединения'},{id:'text',label:'Текст'},{id:'view',label:'Вид'},{id:'export',label:'Экспорт'}] as const
const activeTab = ref<(typeof tabs)[number]['id']>('home')
const activeTabLabel = computed(() => tabs.find((tab) => tab.id === activeTab.value)?.label ?? activeTab.value)
function patchSettings(patch: Partial<CanvasSettings>): void { emit('settingsChange', normalizeCanvasSettings({ ...props.settings, ...patch })) }
function onNumberSetting(key: keyof CanvasSettings, event: Event): void { const value = Number((event.target as HTMLInputElement).value); if (Number.isFinite(value)) patchSettings({ [key]: value } as Partial<CanvasSettings>) }
function onTextSetting(key: keyof CanvasSettings, event: Event): void { patchSettings({ [key]: (event.target as HTMLSelectElement).value } as Partial<CanvasSettings>) }
</script>
<style scoped>
.ribbon-bar{display:grid;grid-template-columns:230px 1fr;grid-template-rows:32px 80px;border-bottom:1px solid #cbd5e1;background:#f8fafc;color:#0f172a;box-shadow:0 1px 4px rgba(15,23,42,.08);z-index:3;overflow:hidden}.ribbon-title{grid-row:1/3;display:flex;flex-direction:column;justify-content:center;padding:10px 16px;border-right:1px solid #dbe3ef;background:#111827;color:white}.ribbon-title span{color:#cbd5e1;font-size:12px}.ribbon-tabs{display:flex;align-items:end;gap:2px;padding:4px 8px 0;overflow:hidden}.ribbon-tabs button{height:28px;border:1px solid transparent;border-bottom:0;border-radius:8px 8px 0 0;padding:0 10px;background:transparent;color:#334155;cursor:pointer;font-weight:700;font-size:12px}.ribbon-tabs button.active{background:white;border-color:#cbd5e1;color:#1d4ed8}.ribbon-content{display:flex;align-items:stretch;gap:8px;padding:6px 8px;background:white;overflow:hidden}.ribbon-group{min-width:132px;padding:7px;border:1px solid #dbeafe;border-radius:10px;background:#f8fbff;overflow:hidden}.ribbon-group.wide{min-width:420px}.ribbon-group.canvas-settings{min-width:300px}.ribbon-group h3{margin:0 0 5px;color:#475569;font-size:10px;text-transform:uppercase}.button-row{display:flex;flex-wrap:wrap;gap:5px}.button-row button{border:1px solid #bfdbfe;border-radius:8px;background:white;color:#1e3a8a;cursor:pointer;font-weight:800;font-size:12px;padding:6px 8px}.settings-grid{display:grid;grid-template-columns:90px 170px;gap:8px}.settings-grid input,.settings-grid select{border:1px solid #bfdbfe;border-radius:7px;padding:5px 6px;background:white}
</style>
