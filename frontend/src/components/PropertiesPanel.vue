<script setup lang="ts">
import { computed } from 'vue'
import type { SchemeSymbol, SymbolLibrary } from '../lib/types'

const props = defineProps<{
  symbol: SchemeSymbol | null
  library: SymbolLibrary | null
}>()

const emit = defineEmits<{
  stateChange: [symbolId: string, newState: string]
  delete: [symbolId: string]
}>()

const definition = computed(() => {
  if (!props.symbol || !props.library) return null
  return props.library.symbols.find((s) => s.type === props.symbol!.type) ?? null
})

const currentStateLabel = computed(() => {
  if (!definition.value || !props.symbol) return ''
  const stateId = props.symbol.current_state ?? definition.value.default_state
  const state = definition.value.states.find((s) => s.id === stateId)
  return state?.name ?? stateId
})

const availableStates = computed(() => {
  if (!definition.value) return []
  return definition.value.states
})

function cycleState() {
  if (!props.symbol || !definition.value) return
  const states = definition.value.states
  if (states.length < 2) return
  const current = props.symbol.current_state ?? definition.value.default_state
  const idx = states.findIndex((s) => s.id === current)
  const next = states[(idx + 1) % states.length]
  emit('stateChange', props.symbol.id, next.id)
}
</script>

<template>
  <section class="panel">
    <h2>Свойства</h2>
    <template v-if="symbol">
      <dl class="props">
        <dt>ID</dt>
        <dd>{{ symbol.id }}</dd>
        <dt>Тип</dt>
        <dd>{{ symbol.type }}</dd>
        <dt>Обозначение</dt>
        <dd>{{ symbol.label }}</dd>
        <dt>Точек подключения</dt>
        <dd>{{ symbol.terminals.length }}</dd>
        <template v-if="definition">
          <dt>ГОСТ</dt>
          <dd>{{ definition.gost }}</dd>
          <dt>Размер</dt>
          <dd>{{ definition.default_width }}×{{ definition.default_height }}</dd>
        </template>
      </dl>

      <div v-if="definition && definition.interactive" class="state-section">
        <div class="state-header">
          <span class="state-label">Состояние:</span>
          <span class="state-value" :class="`state-${symbol.current_state ?? definition.default_state}`">
            {{ currentStateLabel }}
          </span>
        </div>
        <div class="state-buttons">
          <button
            v-for="st in availableStates" :key="st.id"
            class="state-btn"
            :class="{ active: (symbol.current_state ?? definition.default_state) === st.id }"
            @click="emit('stateChange', symbol.id, st.id)"
          >
            {{ st.name }}
          </button>
        </div>
      </div>

      <div v-else-if="definition" class="state-section">
        <div class="state-header">
          <span class="state-label">Тип:</span>
          <span class="state-value">Пассивный (не переключаемый)</span>
        </div>
      </div>

      <div class="state-section">
        <button class="state-btn delete-btn" @click="emit('delete', symbol.id)">
          Удалить элемент
        </button>
      </div>

      <pre class="json-preview">{{ symbol.properties ?? {} }}</pre>
    </template>
    <p v-else class="hint">Выберите элемент на схеме</p>
  </section>
</template>
