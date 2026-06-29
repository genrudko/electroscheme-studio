<template>
  <aside class="shape-palette stencil-palette">
    <header class="palette-header">
      <div>
        <h2>Фигуры</h2>
        <small>VSDX-библиотеки</small>
      </div>
      <button type="button" title="Свернуть панель">‹</button>
    </header>

    <label class="search-box">
      <span>Поиск</span>
      <input v-model="query" type="search" placeholder="выключатель, ТН, автотрансформатор…" />
    </label>

    <div class="palette-toolbar" aria-label="Режим иконок библиотеки">
      <button type="button" :class="{ active: iconMode === 'library' }" @click="iconMode = 'library'">Библиотека</button>
      <button type="button" :class="{ active: iconMode === 'smart' }" @click="iconMode = 'smart'">УГО</button>
      <button type="button" :class="{ active: iconMode === 'none' }" @click="iconMode = 'none'">Без иконок</button>
    </div>

    <div class="palette-body">
      <section class="palette-section library-section">
        <h3>Библиотеки</h3>
        <button
          v-for="category in categories"
          :key="category.id"
          type="button"
          class="library-card"
          :class="{ active: activeCategoryId === category.id }"
          @click="activeCategoryId = activeCategoryId === category.id ? null : category.id"
        >
          <span class="library-card-title">{{ category.title }}</span>
          <small>{{ category.description }}</small>
        </button>
      </section>

      <section class="palette-section figure-section">
        <h3>Фигуры</h3>
        <button
          v-for="item in filteredItems"
          :key="item.id"
          type="button"
          class="shape-item"
          :class="{ planned: item.status === 'planned', available: Boolean(item.command), 'no-icon': iconMode === 'none' }"
          :draggable="Boolean(item.command)"
          :aria-disabled="!item.command"
          :title="itemTooltip(item)"
          @click="insertItem(item)"
          @dragstart="onDragStart($event, item)"
        >
          <span v-if="iconMode !== 'none'" class="preview stencil-icon" :data-icon-kind="paletteIconKind(item)" v-html="paletteIconSvg(item)"></span>

          <span class="shape-text">
            <span class="shape-title-row">
              <span class="shape-title">{{ item.title }}</span>
              <span v-if="item.status === 'planned'" class="planned-dot" title="Запланировано к точной отрисовке из VSDX"></span>
            </span>
            <small v-if="shapeMeta(item)" class="shape-meta">{{ shapeMeta(item) }}</small>
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
import { getLibraryIconKind, getSmartIconKind, type PaletteIconKind, type PaletteIconMode } from '../../lib/editor/paletteIconPolicy'

const emit = defineEmits<{
  insertShape: [command: EditorCommand]
}>()

const query = ref('')
const activeCategoryId = ref<string | null>(null)
const iconMode = ref<PaletteIconMode>('library')
const categories = shapeCatalogCategories
const layers = createDefaultLayers()

const filteredItems = computed(() => filterShapeCatalog(query.value, activeCategoryId.value))

function insertItem(item: ShapeCatalogItem): void {
  if (!item.command) return
  emit('insertShape', item.command)
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

function shapeMeta(item: ShapeCatalogItem): string {
  if (item.status === 'available') return item.sourceRef ? 'доступно' : ''
  return item.libraryPageName ?? ''
}

function itemTooltip(item: ShapeCatalogItem): string {
  const details = [
    item.title,
    item.libraryPageName ? `Библиотека: ${item.libraryPageName}` : '',
    item.semanticCategoryId ? `Семантика: ${item.semanticCategoryId}` : '',
    item.vsdxMasterId ? `VSDX master: ${item.vsdxMasterId}` : '',
    item.widthMm && item.heightMm ? `Размер: ${item.widthMm} × ${item.heightMm} мм` : '',
    typeof item.connectionCount === 'number' ? `Порты: ${item.connectionCount}` : '',
    item.sourceRef ?? '',
  ].filter(Boolean)

  return details.join('\n')
}

function paletteIconKind(item: ShapeCatalogItem): PaletteIconKind {
  if (item.status === 'available') return 'library-generic'
  return iconMode.value === 'smart' ? getSmartIconKind(item) : getLibraryIconKind(item)
}

function paletteIconSvg(item: ShapeCatalogItem): string {
  if (item.status === 'available' && item.svgPreview) return item.svgPreview
  return iconForKind(paletteIconKind(item))
}

function iconSvg(body: string): string {
  return `<svg viewBox="0 0 64 40" aria-hidden="true" role="img">${body}</svg>`
}

function iconForKind(kind: PaletteIconKind): string {
  switch (kind) {
    case 'library-transformers':
      return iconSvg('<rect x="10" y="12" width="44" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="28" cy="20" r="6" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="36" cy="20" r="6" fill="none" stroke="currentColor" stroke-width="2"/>')
    case 'library-switching':
      return iconSvg('<rect x="12" y="10" width="40" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20h24M32 6v8M32 26v8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>')
    case 'library-machines':
      return iconSvg('<circle cx="32" cy="20" r="12" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 20h8M44 20h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><text x="32" y="25" text-anchor="middle" font-family="Arial" font-size="14" font-weight="700" fill="currentColor">M</text>')
    case 'library-lines':
      return iconSvg('<rect x="8" y="16" width="48" height="8" rx="1.5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="20" cy="20" r="2.5" fill="#fff" stroke="currentColor" stroke-width="1.6"/><circle cx="32" cy="20" r="2.5" fill="#fff" stroke="currentColor" stroke-width="1.6"/><circle cx="44" cy="20" r="2.5" fill="#fff" stroke="currentColor" stroke-width="1.6"/>')
    case 'library-protection':
      return iconSvg('<path d="M32 5 48 12v8c0 9-6 14-16 16-10-2-16-7-16-16v-8L32 5z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M35 12 26 22h7l-4 8 10-11h-7l3-7z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>')
    case 'library-compensation':
      return iconSvg('<path d="M14 20c0-5 5-5 5 0s5 5 5 0 5-5 5 0 5 5 5 0 5-5 5 0 5 5 5 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>')
    case 'exact-circuit-breaker':
      return iconSvg('<path d="M32 4v10M32 26v10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="19" y="14" width="26" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M24 22h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="32" cy="20" r="2.2" fill="currentColor"/>')
    case 'exact-withdrawable-truck':
      return iconSvg('<path d="M32 4v7M32 29v7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="14" y="11" width="36" height="18" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 17h24M20 23h24" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="22" cy="31" r="2.2" fill="currentColor"/><circle cx="42" cy="31" r="2.2" fill="currentColor"/>')
    case 'exact-disconnector':
      return iconSvg('<path d="M32 4v9M32 27v9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="32" cy="15" r="2.4" fill="currentColor"/><circle cx="32" cy="25" r="2.4" fill="currentColor"/><path d="M31 24 45 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>')
    case 'exact-earthing-switch':
      return iconSvg('<path d="M32 4v16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M22 20h20M25 26h14M28 31h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="32" cy="15" r="2.3" fill="currentColor"/>')
    case 'exact-short-circuiter':
      return iconSvg('<path d="M32 4v10M32 25v11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="32" cy="16" r="2.2" fill="currentColor"/><circle cx="32" cy="24" r="2.2" fill="currentColor"/><path d="M24 16h16M23 24h18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>')
    case 'exact-transformer':
      return iconSvg('<path d="M18 20h8M38 20h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="29" cy="20" r="7" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="35" cy="20" r="7" fill="none" stroke="currentColor" stroke-width="2"/>')
    case 'exact-machine-generator':
      return machineIcon('G')
    case 'exact-machine-motor':
      return machineIcon('M')
    case 'exact-busbar':
      return iconForKind('library-lines')
    case 'exact-arrester':
      return iconSvg('<path d="M32 4v8M32 28v8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M35 12 25 23h7l-3 9 10-12h-7l3-8z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>')
    case 'exact-fuse':
      return iconSvg('<path d="M32 4v9M32 27v9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="22" y="13" width="20" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M26 23c4-8 8 8 12-1" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>')
    case 'exact-reactor':
      return iconForKind('library-compensation')
    case 'exact-capacitor':
      return iconSvg('<path d="M32 4v10M32 26v10M24 16h16M24 24h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>')
    case 'library-generic':
    default:
      return iconSvg('<rect x="18" y="10" width="28" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M24 20h16M32 14v12" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>')
  }
}

function machineIcon(letter: 'G' | 'M'): string {
  return iconSvg(`<circle cx="32" cy="20" r="13" fill="none" stroke="currentColor" stroke-width="2"/><text x="32" y="25" text-anchor="middle" font-family="Arial" font-size="15" font-weight="700" fill="currentColor">${letter}</text><path d="M10 20h9M45 20h9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>`)
}
</script>

<style scoped>
.shape-palette {
  display: grid;
  grid-template-rows: auto auto auto 1fr;
  min-width: 0;
  min-height: 0;
  border-right: 1px solid #cbd5e1;
  background: #f8fafc;
  overflow: hidden;
}

.palette-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 10px 7px;
  border-bottom: 1px solid #e2e8f0;
}

.palette-header h2 {
  margin: 0;
  color: #1d4ed8;
  font-size: 15px;
}

.palette-header small {
  color: #64748b;
  font-size: 10px;
  font-weight: 700;
}

.palette-header button {
  border: 0;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  font-size: 20px;
}

.search-box {
  display: grid;
  gap: 5px;
  padding: 8px 10px 6px;
  color: #475569;
  font-size: 12px;
  font-weight: 700;
}

.search-box input {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 7px;
  padding: 7px 8px;
  background: white;
}

.palette-toolbar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  padding: 0 8px 7px;
  border-bottom: 1px solid #e2e8f0;
}

.palette-toolbar button {
  min-width: 0;
  border: 1px solid #d5e3f6;
  border-radius: 7px;
  background: #fff;
  color: #45607f;
  cursor: pointer;
  font-size: 10px;
  font-weight: 800;
  padding: 5px 4px;
}

.palette-toolbar button.active {
  border-color: #2563eb;
  background: #eff6ff;
  color: #174ea6;
}

.palette-body {
  min-height: 0;
  overflow: auto;
  padding: 8px;
}

.palette-section {
  display: grid;
  gap: 6px;
  margin-bottom: 12px;
}

.palette-section h3 {
  margin: 0 0 3px;
  color: #64748b;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.library-card,
.shape-item,
.layer-row {
  border: 1px solid #dbeafe;
  border-radius: 8px;
  background: white;
  color: #0f172a;
  cursor: pointer;
  text-align: left;
}

.library-card {
  display: grid;
  gap: 3px;
  padding: 7px 8px;
}

.library-card.active {
  border-color: #2563eb;
  background: #eff6ff;
  box-shadow: 0 0 0 1px rgba(37, 99, 235, .1);
}

.library-card-title {
  font-size: 12px;
  font-weight: 800;
}

.library-card small {
  color: #64748b;
  font-size: 10px;
  line-height: 1.16;
}

.shape-item {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  align-items: center;
  gap: 8px;
  min-height: 42px;
  padding: 6px 7px;
}

.shape-item.no-icon {
  grid-template-columns: minmax(0, 1fr);
}

.shape-item:hover {
  border-color: #93c5fd;
  background: #f8fbff;
}

.shape-item.planned {
  cursor: default;
}

.shape-item.available {
  cursor: grab;
}

.shape-item.available:active {
  cursor: grabbing;
}

.preview {
  display: grid;
  place-items: center;
  width: 32px;
  height: 28px;
  border: 1px solid #d6e3f4;
  border-radius: 5px;
  color: #6d0ad6;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
  overflow: hidden;
  pointer-events: none;
}

.preview :deep(svg) {
  display: block;
  width: 100%;
  height: 100%;
}

.preview :deep(*) {
  pointer-events: none;
  vector-effect: non-scaling-stroke;
}

.shape-text {
  min-width: 0;
  display: grid;
  gap: 2px;
}

.shape-title-row {
  display: flex;
  align-items: flex-start;
  gap: 5px;
  min-width: 0;
}

.shape-title {
  min-width: 0;
  color: #142033;
  font-size: 12px;
  font-weight: 760;
  line-height: 1.14;
  white-space: normal;
  overflow-wrap: anywhere;
}

.shape-meta {
  color: #64748b;
  font-size: 10px;
  line-height: 1.12;
  white-space: normal;
  overflow-wrap: anywhere;
}

.planned-dot {
  flex: 0 0 auto;
  width: 5px;
  height: 5px;
  margin-top: 5px;
  border-radius: 999px;
  background: #94a3b8;
  opacity: .62;
}

.layer-row {
  display: grid;
  grid-template-columns: auto auto 1fr auto;
  align-items: center;
  gap: 8px;
  padding: 7px 8px;
  cursor: default;
}

.layer-color {
  width: 11px;
  height: 11px;
  border-radius: 3px;
}

.layers-shell {
  border-top: 1px solid #e2e8f0;
  padding-top: 10px;
}
</style>
