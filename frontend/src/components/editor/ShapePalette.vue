<template>
  <aside class="shape-palette">
    <header class="palette-header">
      <h2>Фигуры</h2>
      <button type="button" title="Свернуть панель">‹</button>
    </header>

    <label class="search-box">
      <span>Поиск фигур</span>
      <input v-model="query" type="search" placeholder="шина, выключатель, ТН…" />
    </label>

    <div class="palette-body">
      <section class="palette-section">
        <h3>Библиотеки</h3>
        <button
          v-for="category in categories"
          :key="category.id"
          type="button"
          :class="{ active: activeCategoryId === category.id }"
          @click="activeCategoryId = activeCategoryId === category.id ? null : category.id"
        >
          <span>{{ category.title }}</span>
          <small>{{ category.description }}</small>
        </button>
      </section>

      <section class="palette-section">
        <h3>Фигуры</h3>
        <button
          v-for="item in filteredItems"
          :key="item.id"
          type="button"
          class="shape-item"
          :class="{ planned: item.status === 'planned', available: Boolean(item.command) }"
          :draggable="Boolean(item.command)"
          :aria-disabled="!item.command"
          :title="item.sourceRef"
          @click="insertItem(item)"
          @dragstart="onDragStart($event, item)"
        >
          <span class="preview" :class="{ 'has-svg-preview': Boolean(item.svgPreview) }">
            <span v-if="item.svgPreview" class="preview-svg" v-html="item.svgPreview"></span>
            <template v-else>{{ item.preview }}</template>
          </span>

          <span class="shape-text">
            <span class="shape-title-row">
              <span class="shape-title">{{ item.title }}</span>
              <span v-if="item.status === 'planned'" class="planned-icon" title="Запланировано" aria-label="Запланировано">⌛</span>
            </span>
            <small v-if="shapeMeta(item)">{{ shapeMeta(item) }}</small>
          </span>
        </button>
      </section>

      <section class="palette-section layers-shell">
        <h3>Слои</h3>
        <div v-for="layer in layers" :key="layer.id" class="layer-row">
          <input type="checkbox" :checked="layer.visible" disabled />
          <span class="layer-color" :style="{ background: layer.color }"></span>
          <span>{{ layer.name }}</span>
          <small>{{ layer.locked ? 'замок' : 'свободен' }}</small>
        </div>
      </section>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { EditorCommand } from '../../lib/editor/interactionModes'
import { filterShapeCatalog, shapeCatalogCategories, type ShapeCatalogItem } from '../../lib/editor/shapeCatalog'
import { createDefaultLayers } from '../../lib/editor/editorDocument'

const emit = defineEmits<{
  insertShape: [command: EditorCommand]
}>()

const query = ref('')
const activeCategoryId = ref<string | null>(null)
const categories = shapeCatalogCategories
const layers = createDefaultLayers()

const filteredItems = computed(() => filterShapeCatalog(query.value, activeCategoryId.value))

function insertItem(item: ShapeCatalogItem): void {
  if (!item.command) return
  emit('insertShape', item.command)
}

function shapeMeta(item: ShapeCatalogItem): string {
  if (item.status === 'available') return item.sourceRef ? 'доступно' : ''
  const size = item.widthMm && item.heightMm ? `${item.widthMm}×${item.heightMm} мм` : ''
  const ports = typeof item.connectionCount === 'number' ? `${item.connectionCount} порт.` : ''
  return [size, ports].filter(Boolean).join(' · ')
}

function onDragStart(event: DragEvent, item: ShapeCatalogItem): void {
  if (!item.command) {
    event.preventDefault()
    return
  }

  event.dataTransfer?.setData('application/x-electroscheme-command', item.command)
  event.dataTransfer?.setData('text/plain', item.command)
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'copy'
    event.dataTransfer.dropEffect = 'copy'
  }
}
</script>

<style scoped>
.shape-palette { display: grid; grid-template-rows: auto auto 1fr; min-width: 0; min-height: 0; border-right: 1px solid #cbd5e1; background: #f8fafc; overflow: hidden; }
.palette-header { display: flex; align-items: center; justify-content: space-between; padding: 10px 10px 6px; border-bottom: 1px solid #e2e8f0; }
.palette-header h2 { margin: 0; color: #1d4ed8; font-size: 16px; }
.palette-header button { border: 0; background: transparent; color: #64748b; cursor: pointer; font-size: 20px; }
.search-box { display: grid; gap: 5px; padding: 8px 10px; color: #475569; font-size: 12px; font-weight: 700; }
.search-box input { width: 100%; border: 1px solid #cbd5e1; border-radius: 7px; padding: 7px 8px; background: white; }
.palette-body { min-height: 0; overflow: auto; padding: 8px; }
.palette-section { display: grid; gap: 6px; margin-bottom: 12px; }
.palette-section h3 { margin: 0 0 3px; color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }
.palette-section button, .shape-item, .layer-row { display: grid; align-items: center; gap: 8px; border: 1px solid #dbeafe; border-radius: 8px; background: white; color: #0f172a; cursor: pointer; padding: 7px 8px; text-align: left; }
.palette-section button { grid-template-columns: 1fr; }
.palette-section button.active { border-color: #2563eb; background: #eff6ff; }
.palette-section small { color: #64748b; font-size: 11px; }
.shape-item { grid-template-columns: 30px 1fr !important; min-height: 42px; }
.shape-item.planned { cursor: default; }
.shape-item[aria-disabled='true'] { cursor: default; }
.preview { display: grid; place-items: center; width: 28px; height: 24px; border: 1px solid #cbd5e1; border-radius: 5px; color: #6d0ad6; font-size: 18px; font-weight: 800; overflow: hidden; pointer-events: none; }
.preview-svg { display: grid; place-items: center; width: 100%; height: 100%; pointer-events: none; }
.preview-svg :deep(svg) { display: block; width: 100%; height: 100%; pointer-events: none; }
.preview-svg :deep(*) { pointer-events: none; }
.shape-text { min-width: 0; display: grid; gap: 2px; }
.shape-title-row { display: flex; align-items: flex-start; gap: 5px; min-width: 0; }
.shape-title { min-width: 0; white-space: normal; overflow-wrap: anywhere; line-height: 1.15; }
.planned-icon { flex: 0 0 auto; display: inline-grid; place-items: center; width: 17px; height: 17px; border-radius: 999px; background: #eef2f7; color: #64748b; font-size: 10px; line-height: 1; }
.layer-row { grid-template-columns: auto auto 1fr auto; cursor: default; }
.layer-color { width: 11px; height: 11px; border-radius: 3px; }
.layers-shell { border-top: 1px solid #e2e8f0; padding-top: 10px; }
</style>
