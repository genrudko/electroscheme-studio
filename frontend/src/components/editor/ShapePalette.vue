<template>
  <!-- palette-command-source:create_circuit_breaker; commands are declared in shapeCatalog.ts and emitted through item.command -->
  <aside class="shape-palette">
    <header class="palette-header"><h2>Фигуры</h2></header>
    <label class="search-box"><span>Поиск фигур</span><input v-model="query" type="search" placeholder="шина, выключатель, ТН…" /></label>
    <div class="palette-body">
      <section class="palette-section">
        <h3>Библиотеки</h3>
        <button v-for="category in categories" :key="category.id" type="button" :class="{ active: activeCategoryId === category.id }" @click="activeCategoryId = activeCategoryId === category.id ? null : category.id">
          <span>{{ category.title }}</span><small>{{ category.description }}</small>
        </button>
      </section>
      <section class="palette-section">
        <h3>Фигуры</h3>
        <button v-for="item in filteredItems" :key="item.id" type="button" class="shape-item" :class="{ planned: item.status === 'planned' }" :draggable="Boolean(item.command)" :disabled="!item.command" :title="item.sourceRef" @click="insertItem(item)" @dragstart="onDragStart($event, item)">
          <span class="preview">{{ item.preview }}</span><span>{{ item.title }}<small v-if="item.status === 'planned'">запланировано</small></span>
        </button>
      </section>
      <section class="palette-section layers-shell"><h3>Слои</h3><div class="layer-row">☑ <span>Схема</span></div><div class="layer-row">☑ <span>Подписи</span></div></section>
    </div>
  </aside>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
import type { EditorCommand } from '../../lib/editor/interactionModes'
import { filterShapeCatalog, shapeCatalogCategories, type ShapeCatalogItem } from '../../lib/editor/shapeCatalog'
const emit = defineEmits<{ insertShape: [command: EditorCommand] }>()
const query = ref('')
const activeCategoryId = ref<string | null>(null)
const categories = shapeCatalogCategories
const filteredItems = computed(() => filterShapeCatalog(query.value, activeCategoryId.value))
function insertItem(item: ShapeCatalogItem): void { if (item.command) emit('insertShape', item.command) }
function onDragStart(event: DragEvent, item: ShapeCatalogItem): void {
  if (!item.command) { event.preventDefault(); return }
  event.dataTransfer?.setData('application/x-electroscheme-command', item.command)
  event.dataTransfer?.setData('text/plain', item.command)
  if (event.dataTransfer) event.dataTransfer.effectAllowed = 'copy'
}
</script>
<style scoped>
.shape-palette{display:grid;grid-template-rows:auto auto 1fr;min-height:0;border-right:1px solid #cbd5e1;background:#f8fafc;overflow:hidden}.palette-header{padding:10px;border-bottom:1px solid #e2e8f0}.palette-header h2{margin:0;color:#1d4ed8;font-size:16px}.search-box{display:grid;gap:5px;padding:8px 10px;color:#475569;font-size:12px;font-weight:700}.search-box input{border:1px solid #cbd5e1;border-radius:7px;padding:7px 8px}.palette-body{min-height:0;overflow:auto;padding:8px}.palette-section{display:grid;gap:6px;margin-bottom:12px}.palette-section h3{margin:0;color:#64748b;font-size:11px;text-transform:uppercase}.palette-section button,.shape-item,.layer-row{display:grid;grid-template-columns:auto 1fr;gap:8px;align-items:center;border:1px solid #dbeafe;border-radius:8px;background:white;color:#0f172a;cursor:pointer;padding:7px 8px;text-align:left}.palette-section button{grid-template-columns:1fr}.palette-section button.active{border-color:#2563eb;background:#eff6ff}.palette-section small{color:#64748b;font-size:11px}.shape-item{grid-template-columns:28px 1fr!important}.shape-item.planned{opacity:.68;cursor:default}.shape-item:disabled{cursor:default}.preview{display:grid;place-items:center;width:28px;height:24px;border:1px solid #cbd5e1;border-radius:5px;color:#6d0ad6;font-size:18px;font-weight:800}.layers-shell{border-top:1px solid #e2e8f0;padding-top:10px}
</style>
