<template>
  <section class="imported-symbol-review" aria-label="Imported Visio symbol review">
    <header class="review-header">
      <div>
        <p class="eyebrow">Visio import review</p>
        <h2>Imported draft symbols</h2>
        <p class="description">
          Review imported Visio masters before promoting them to the core symbol library.
        </p>
      </div>
      <button type="button" class="refresh-button" :disabled="loading" @click="loadData">
        {{ loading ? 'Loading…' : 'Refresh' }}
      </button>
    </header>

    <div v-if="error" class="status error">
      {{ error }}
    </div>

    <div v-else-if="loading && !report" class="status">
      Loading imported symbol review…
    </div>

    <template v-else>
      <div class="summary-grid">
        <article class="summary-card">
          <span class="summary-label">Drafts</span>
          <strong>{{ summaryValue('loaded_count') }}</strong>
        </article>
        <article class="summary-card">
          <span class="summary-label">With terminals</span>
          <strong>{{ report?.summary?.with_terminals ?? 0 }}</strong>
        </article>
        <article class="summary-card">
          <span class="summary-label">Without terminals</span>
          <strong>{{ report?.summary?.without_terminals ?? 0 }}</strong>
        </article>
        <article class="summary-card">
          <span class="summary-label">Warnings</span>
          <strong>{{ report?.summary?.with_warnings ?? 0 }}</strong>
        </article>
        <article class="summary-card">
          <span class="summary-label">Errors</span>
          <strong>{{ report?.summary?.with_errors ?? 0 }}</strong>
        </article>
        <article class="summary-card">
          <span class="summary-label">Avg quality</span>
          <strong>{{ report?.summary?.average_quality ?? '—' }}</strong>
        </article>
      </div>

      <div class="review-layout">
        <aside class="review-sidebar">
          <label class="field">
            Search
            <input v-model="search" type="search" placeholder="Name, id, category…" />
          </label>

          <label class="field">
            Category
            <select v-model="categoryFilter">
              <option value="">All categories</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </label>

          <label class="field">
            Issue filter
            <select v-model="issueFilter">
              <option value="all">All</option>
              <option value="errors">With errors</option>
              <option value="warnings">With warnings</option>
              <option value="no-terminals">Without terminals</option>
              <option value="priority">Priority equipment</option>
            </select>
          </label>

          <div class="category-list">
            <h3>Categories</h3>
            <button
              v-for="[category, count] in categoryEntries"
              :key="category"
              type="button"
              :class="{ active: categoryFilter === category }"
              @click="categoryFilter = categoryFilter === category ? '' : category"
            >
              <span>{{ category }}</span>
              <strong>{{ count }}</strong>
            </button>
          </div>
        </aside>

        <main class="review-main">
          <div class="list-toolbar">
            <span>{{ filteredSymbols.length }} symbols</span>
            <span v-if="selectedItem">Selected: {{ selectedItem.name_ru }}</span>
          </div>

          <div class="symbol-list" role="list">
            <button
              v-for="item in filteredSymbols"
              :key="item.id"
              type="button"
              class="symbol-row"
              :class="{ selected: selectedItem?.id === item.id }"
              @click="selectSymbol(item)"
            >
              <span class="symbol-name">{{ item.name_ru }}</span>
              <code>{{ item.id }}</code>
              <span class="symbol-meta">
                {{ item.category }} · terminals {{ item.terminal_count }} · score {{ item.quality_score }}
              </span>
              <span class="issue-line">
                <span v-if="item.error_count" class="pill danger">errors {{ item.error_count }}</span>
                <span v-if="item.warning_count" class="pill warn">warnings {{ item.warning_count }}</span>
                <span v-if="!item.error_count && !item.warning_count" class="pill ok">clean</span>
              </span>
            </button>
          </div>
        </main>

        <aside class="detail-panel">
          <template v-if="selectedItem">
            <div class="preview-card">
              <div v-if="detailLoading" class="status">Loading symbol…</div>
              <svg
                v-else-if="selectedSymbol"
                class="symbol-preview"
                :viewBox="viewBoxString(selectedSymbol)"
                role="img"
                :aria-label="selectedItem.name_ru"
                v-html="selectedSymbol.svg_fragment"
              />
              <div v-else class="status">Select a symbol to load preview.</div>
            </div>

            <h3>{{ selectedItem.name_ru }}</h3>
            <code class="selected-id">{{ selectedItem.id }}</code>

            <dl class="details">
              <div>
                <dt>Category</dt>
                <dd>{{ selectedItem.category }}</dd>
              </div>
              <div>
                <dt>Quality</dt>
                <dd>{{ selectedItem.quality_score }}</dd>
              </div>
              <div>
                <dt>Terminals</dt>
                <dd>{{ selectedItem.terminal_count }} / {{ selectedItem.terminal_with_coordinates }}</dd>
              </div>
              <div>
                <dt>Status</dt>
                <dd>{{ selectedItem.review_status }}</dd>
              </div>
            </dl>

            <div class="flags">
              <span v-for="flag in activeFlags(selectedItem)" :key="flag" class="badge">
                {{ flag }}
              </span>
            </div>

            <details class="issue-details" open>
              <summary>Issues</summary>
              <ul v-if="selectedItem.errors.length || selectedItem.warnings.length">
                <li v-for="err in selectedItem.errors" :key="`e-${err}`" class="error-text">
                  {{ err }}
                </li>
                <li v-for="warn in selectedItem.warnings.slice(0, 20)" :key="`w-${warn}`" class="warning-text">
                  {{ warn }}
                </li>
              </ul>
              <p v-else class="ok-text">No validator issues.</p>
            </details>
          </template>

          <div v-else class="empty-detail">
            Select an imported draft symbol to inspect geometry, terminals and review warnings.
          </div>
        </aside>
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type ReviewSummary = {
  with_terminals: number
  without_terminals: number
  with_warnings: number
  without_warnings: number
  with_errors: number
  without_errors: number
  average_quality: number
  by_category: Record<string, number>
}

type ReviewItem = {
  path: string
  id: string
  name_ru: string
  category: string
  review_status: string
  terminal_count: number
  terminal_with_coordinates: number
  warning_count: number
  error_count: number
  quality_score: number
  feature_flags: Record<string, boolean>
  errors: string[]
  warnings: string[]
  info: string[]
}

type ReviewReport = {
  draft_count: number
  loaded_count: number
  summary: ReviewSummary
  symbols: ReviewItem[]
}

type ImportedSymbolsResponse = {
  review_status: string
  review_report: ReviewReport | null
}

type ImportedSymbolDetail = {
  id: string
  name_ru: string
  review_status: string
  viewBox: {
    x: number
    y: number
    width: number
    height: number
  }
  svg_fragment: string
}

const loading = ref(false)
const detailLoading = ref(false)
const error = ref('')
const report = ref<ReviewReport | null>(null)
const selectedItem = ref<ReviewItem | null>(null)
const selectedSymbol = ref<ImportedSymbolDetail | null>(null)
const search = ref('')
const categoryFilter = ref('')
const issueFilter = ref<'all' | 'errors' | 'warnings' | 'no-terminals' | 'priority'>('all')

const priorityCategories = new Set([
  'busbar',
  'circuit_breaker',
  'disconnector',
  'earthing_switch',
  'kru_trolley',
])

const categories = computed(() => {
  const byCategory = report.value?.summary?.by_category ?? {}
  return Object.keys(byCategory).sort((a, b) => a.localeCompare(b, 'ru'))
})

const categoryEntries = computed(() => {
  const byCategory = report.value?.summary?.by_category ?? {}
  return Object.entries(byCategory).sort((a, b) => b[1] - a[1])
})

const filteredSymbols = computed(() => {
  const query = search.value.trim().toLowerCase()
  return (report.value?.symbols ?? []).filter((item) => {
    if (categoryFilter.value && item.category !== categoryFilter.value) return false
    if (query) {
      const haystack = `${item.name_ru} ${item.id} ${item.category}`.toLowerCase()
      if (!haystack.includes(query)) return false
    }
    if (issueFilter.value === 'errors' && item.error_count <= 0) return false
    if (issueFilter.value === 'warnings' && item.warning_count <= 0) return false
    if (issueFilter.value === 'no-terminals' && item.terminal_count > 0) return false
    if (issueFilter.value === 'priority' && !priorityCategories.has(item.category)) return false
    return true
  })
})

function summaryValue(key: keyof ReviewReport): number | string {
  return report.value?.[key] ?? '—'
}

function viewBoxString(symbol: ImportedSymbolDetail): string {
  const vb = symbol.viewBox
  return `${vb.x ?? 0} ${vb.y ?? 0} ${vb.width || 100} ${vb.height || 100}`
}

function activeFlags(item: ReviewItem): string[] {
  return Object.entries(item.feature_flags ?? {})
    .filter(([, value]) => Boolean(value))
    .map(([key]) => key)
}

async function loadData(): Promise<void> {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch('/api/imported-symbols')
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const data = (await response.json()) as ImportedSymbolsResponse
    report.value = data.review_report
    const first = report.value?.symbols?.[0] ?? null
    if (!selectedItem.value && first) {
      await selectSymbol(first)
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : String(err)
  } finally {
    loading.value = false
  }
}

async function selectSymbol(item: ReviewItem): Promise<void> {
  selectedItem.value = item
  selectedSymbol.value = null
  detailLoading.value = true
  try {
    const response = await fetch(`/api/imported-symbols/${encodeURIComponent(item.id)}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    selectedSymbol.value = (await response.json()) as ImportedSymbolDetail
  } catch (err) {
    error.value = err instanceof Error ? err.message : String(err)
  } finally {
    detailLoading.value = false
  }
}

onMounted(() => {
  void loadData()
})
</script>

<style scoped>
.imported-symbol-review {
  margin: 18px;
  padding: 18px;
  border: 1px solid rgba(148, 163, 184, 0.4);
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 250, 252, 0.96));
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
  color: #0f172a;
}

.review-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #2563eb;
  text-transform: uppercase;
}

.review-header h2 {
  margin: 0;
  font-size: 22px;
}

.description {
  margin: 4px 0 0;
  color: #64748b;
}

.refresh-button {
  border: 0;
  border-radius: 999px;
  padding: 10px 16px;
  background: #2563eb;
  color: white;
  font-weight: 700;
  cursor: pointer;
}

.refresh-button:disabled {
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

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(135px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}

.summary-card {
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 12px;
  background: white;
}

.summary-label {
  display: block;
  color: #64748b;
  font-size: 12px;
}

.summary-card strong {
  display: block;
  margin-top: 4px;
  font-size: 24px;
}

.review-layout {
  display: grid;
  grid-template-columns: minmax(210px, 250px) minmax(320px, 1fr) minmax(310px, 380px);
  gap: 14px;
}

.review-sidebar,
.review-main,
.detail-panel {
  min-height: 520px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  background: white;
}

.review-sidebar {
  padding: 12px;
}

.field {
  display: grid;
  gap: 6px;
  margin-bottom: 12px;
  color: #475569;
  font-size: 12px;
  font-weight: 700;
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

.category-list h3 {
  margin: 16px 0 8px;
  font-size: 14px;
}

.category-list button {
  width: 100%;
  display: flex;
  justify-content: space-between;
  gap: 8px;
  border: 0;
  border-radius: 10px;
  padding: 8px 10px;
  margin-bottom: 4px;
  background: transparent;
  color: #334155;
  cursor: pointer;
  text-align: left;
}

.category-list button:hover,
.category-list button.active {
  background: #eff6ff;
  color: #1d4ed8;
}

.review-main {
  overflow: hidden;
}

.list-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 12px;
  border-bottom: 1px solid #e2e8f0;
  color: #64748b;
  font-size: 12px;
  font-weight: 700;
}

.symbol-list {
  max-height: 610px;
  overflow: auto;
  padding: 8px;
}

.symbol-row {
  width: 100%;
  display: grid;
  gap: 4px;
  border: 1px solid transparent;
  border-radius: 12px;
  padding: 10px;
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.symbol-row:hover {
  background: #f8fafc;
}

.symbol-row.selected {
  border-color: #93c5fd;
  background: #eff6ff;
}

.symbol-name {
  font-weight: 800;
  color: #0f172a;
}

.symbol-row code,
.selected-id {
  color: #475569;
  font-size: 12px;
}

.symbol-meta {
  color: #64748b;
  font-size: 12px;
}

.issue-line {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.pill,
.badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 3px 7px;
  font-size: 11px;
  font-weight: 700;
}

.pill.ok {
  background: #dcfce7;
  color: #166534;
}

.pill.warn {
  background: #fef3c7;
  color: #92400e;
}

.pill.danger {
  background: #fee2e2;
  color: #991b1b;
}

.detail-panel {
  padding: 12px;
  overflow: auto;
}

.preview-card {
  min-height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background:
    linear-gradient(90deg, rgba(148, 163, 184, 0.14) 1px, transparent 1px),
    linear-gradient(rgba(148, 163, 184, 0.14) 1px, transparent 1px);
  background-size: 18px 18px;
  color: #4b5563;
  --voltage-color: #4b5563;
}

.symbol-preview {
  width: 90%;
  max-height: 210px;
}

.detail-panel h3 {
  margin: 12px 0 4px;
}

.details {
  display: grid;
  gap: 8px;
  margin: 12px 0;
}

.details div {
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 8px;
}

.details dt {
  color: #64748b;
  font-size: 12px;
}

.details dd {
  margin: 0;
  font-weight: 700;
}

.flags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin: 8px 0 12px;
}

.badge {
  background: #e0f2fe;
  color: #075985;
}

.issue-details {
  margin-top: 10px;
  font-size: 13px;
}

.error-text {
  color: #b91c1c;
}

.warning-text {
  color: #92400e;
}

.ok-text {
  color: #047857;
}

.empty-detail {
  height: 100%;
  display: grid;
  place-items: center;
  color: #64748b;
  text-align: center;
  padding: 20px;
}

@media (max-width: 1200px) {
  .review-layout {
    grid-template-columns: 1fr;
  }

  .review-sidebar,
  .review-main,
  .detail-panel {
    min-height: auto;
  }
}
</style>