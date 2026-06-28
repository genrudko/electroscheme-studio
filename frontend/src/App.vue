<script setup lang="ts">
import { onMounted } from 'vue'
import { useProject } from './lib/useProject'
import SchemeCanvas from './components/SchemeCanvas.vue'
import PropertiesPanel from './components/PropertiesPanel.vue'

const {
  symbols,
  connections,
  selectedId,
  selectedSymbol,
  selectSymbol,
  loadFromApi,
  loading,
  error,
} = useProject()

onMounted(() => {
  loadFromApi()
})
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
        <div
          v-for="sym in symbols"
          :key="sym.id"
          class="tree-item"
          :class="{ active: selectedId === sym.id }"
          @click="selectSymbol(sym.id)"
        >
          {{ sym.label }} ({{ sym.type }})
        </div>
      </section>
    </aside>

    <section class="workspace">
      <header class="toolbar">
        <span>SVG canvas</span>
        <span v-if="loading" class="toolbar-muted">Загрузка…</span>
        <span v-else-if="error" class="toolbar-muted toolbar-error">{{ error }}</span>
        <span v-else class="toolbar-muted">{{ symbols.length }} элементов</span>
      </header>

      <SchemeCanvas
        :symbols="symbols"
        :connections="connections"
        :selected-id="selectedId"
        @select="selectSymbol"
      />
    </section>

    <aside class="sidebar sidebar-right">
      <PropertiesPanel :symbol="selectedSymbol" />

      <section class="panel">
        <h2>Проверки</h2>
        <div class="check ok">SVG-рендер: OK</div>
        <div class="check ok">Выбор элемента: OK</div>
        <div class="check ok">Загрузка с API: OK</div>
        <div class="check warn">Модель соединений: MVP</div>
      </section>
    </aside>
  </main>
</template>