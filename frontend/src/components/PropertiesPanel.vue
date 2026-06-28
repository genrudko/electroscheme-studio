<script setup lang="ts">
import type { SchemeSymbol } from '../lib/types'

defineProps<{
  symbol: SchemeSymbol | null
}>()
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
      </dl>
      <pre class="json-preview">{{ symbol.properties ?? {} }}</pre>
    </template>
    <p v-else class="hint">Выберите элемент на схеме</p>
  </section>
</template>
