<script setup lang="ts">
import { computed, ref } from 'vue'

type SymbolKind = 'busbar' | 'circuit_breaker'

interface Terminal {
  id: string
  x: number
  y: number
}

interface SchemeSymbol {
  id: string
  type: SymbolKind
  label: string
  x: number
  y: number
  width?: number
  height?: number
  rotation?: number
  terminals: Terminal[]
  properties?: Record<string, unknown>
}

const symbols = ref<SchemeSymbol[]>([
  {
    id: 'busbar_1',
    type: 'busbar',
    label: '1C',
    x: 60,
    y: 60,
    width: 260,
    height: 0,
    terminals: [
      { id: 't1', x: 120, y: 60 },
      { id: 't2', x: 220, y: 60 }
    ]
  },
  {
    id: 'q1',
    type: 'circuit_breaker',
    label: 'Q1',
    x: 120,
    y: 110,
    rotation: 90,
    terminals: [
      { id: 'a', x: 120, y: 80 },
      { id: 'b', x: 120, y: 145 }
    ],
    properties: {
      name: 'Demo circuit breaker',
      voltage_kv: 10,
      state: 'closed'
    }
  }
])

const selectedId = ref<string>('q1')

const selectedSymbol = computed(() => {
  return symbols.value.find((symbol) => symbol.id === selectedId.value) ?? null
})

function selectSymbol(id: string) {
  selectedId.value = id
}
</script>

<template>
  <main class="app-shell">
    <aside class="sidebar sidebar-left">
      <div class="brand">
        <div class="brand-mark">ES</div>
        <div>
          <h1>ElectroScheme Studio</h1>
          <p>ГОСТ-oriented WebUI prototype</p>
        </div>
      </div>

      <section class="panel">
        <h2>Библиотека</h2>
        <button class="tool-button">Шина</button>
        <button class="tool-button">Выключатель</button>
        <button class="tool-button">Разъединитель</button>
        <button class="tool-button">Трансформатор</button>
      </section>

      <section class="panel">
        <h2>Схема</h2>
        <div class="tree-item active">Demo Sheet / A3</div>
        <div class="tree-item">1C</div>
        <div class="tree-item">Q1</div>
      </section>
    </aside>

    <section class="workspace">
      <header class="toolbar">
        <span>SVG canvas</span>
        <span class="toolbar-muted">MVP bootstrap</span>
      </header>

      <div class="sheet-wrap">
        <svg
          class="sheet"
          viewBox="0 0 420 297"
          role="img"
          aria-label="Demo electrical scheme"
        >
          <defs>
            <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
              <path d="M 10 0 L 0 0 0 10" class="grid-line" />
            </pattern>
          </defs>

          <rect x="0" y="0" width="420" height="297" class="sheet-bg" />
          <rect x="10" y="10" width="400" height="277" class="frame" />
          <rect x="10" y="10" width="400" height="277" fill="url(#grid)" opacity="0.55" />

          <g
            class="symbol"
            :class="{ selected: selectedId === 'busbar_1' }"
            @click="selectSymbol('busbar_1')"
          >
            <line x1="60" y1="60" x2="320" y2="60" class="primary-line thick" />
            <text x="42" y="64" class="label">1C</text>
          </g>

          <g class="connection">
            <line x1="120" y1="60" x2="120" y2="88" class="primary-line" />
          </g>

          <g
            class="symbol"
            :class="{ selected: selectedId === 'q1' }"
            @click="selectSymbol('q1')"
          >
            <line x1="120" y1="88" x2="120" y2="102" class="primary-line" />
            <rect x="112" y="102" width="16" height="16" rx="2" class="device-box" />
            <line x1="114" y1="116" x2="126" y2="104" class="primary-line" />
            <line x1="120" y1="118" x2="120" y2="145" class="primary-line" />
            <text x="132" y="114" class="label">Q1</text>
          </g>

          <text x="20" y="282" class="title-block">ElectroScheme Studio — demo A3 sheet</text>
        </svg>
      </div>
    </section>

    <aside class="sidebar sidebar-right">
      <section class="panel">
        <h2>Свойства</h2>
        <template v-if="selectedSymbol">
          <dl class="props">
            <dt>ID</dt>
            <dd>{{ selectedSymbol.id }}</dd>
            <dt>Тип</dt>
            <dd>{{ selectedSymbol.type }}</dd>
            <dt>Обозначение</dt>
            <dd>{{ selectedSymbol.label }}</dd>
            <dt>Точек подключения</dt>
            <dd>{{ selectedSymbol.terminals.length }}</dd>
          </dl>

          <pre class="json-preview">{{ selectedSymbol.properties ?? {} }}</pre>
        </template>
      </section>

      <section class="panel">
        <h2>Проверки</h2>
        <div class="check ok">SVG-рендер: OK</div>
        <div class="check ok">Выбор элемента: OK</div>
        <div class="check warn">Модель соединений: MVP</div>
      </section>
    </aside>
  </main>
</template>
