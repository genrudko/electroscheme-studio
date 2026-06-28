<script setup lang="ts">
import type { SchemeSymbol, Connection } from '../lib/types'

defineProps<{
  symbols: SchemeSymbol[]
  connections: Connection[]
  selectedId: string
}>()

const emit = defineEmits<{
  select: [id: string]
}>()

function resolveTerminal(ref: string, symbols: SchemeSymbol[]) {
  const [symId, tId] = ref.split('.')
  const sym = symbols.find((s) => s.id === symId)
  return sym?.terminals.find((t) => t.id === tId) ?? null
}
</script>

<template>
  <div class="sheet-wrap">
    <svg
      class="sheet"
      viewBox="0 0 420 297"
      role="img"
      aria-label="Electrical scheme"
    >
      <defs>
        <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" class="grid-line" />
        </pattern>
      </defs>

      <rect x="0" y="0" width="420" height="297" class="sheet-bg" />
      <rect x="10" y="10" width="400" height="277" class="frame" />
      <rect x="10" y="10" width="400" height="277" fill="url(#grid)" opacity="0.55" />

      <!-- Symbols -->
      <template v-for="sym in symbols" :key="sym.id">
        <!-- Busbar -->
        <g
          v-if="sym.type === 'busbar'"
          class="symbol"
          :class="{ selected: selectedId === sym.id }"
          @click="emit('select', sym.id)"
        >
          <line
            :x1="sym.x" :y1="sym.y"
            :x2="sym.x + (sym.width ?? 0)" :y2="sym.y"
            class="primary-line thick"
          />
          <text :x="sym.x - 18" :y="sym.y + 4" class="label">{{ sym.label }}</text>
        </g>

        <!-- Circuit breaker -->
        <g
          v-else-if="sym.type === 'circuit_breaker'"
          class="symbol"
          :class="{ selected: selectedId === sym.id }"
          @click="emit('select', sym.id)"
        >
          <line :x1="sym.x" :y1="sym.y - 22" :x2="sym.x" :y2="sym.y - 8" class="primary-line" />
          <rect :x="sym.x - 8" :y="sym.y - 8" width="16" height="16" rx="2" class="device-box" />
          <line :x1="sym.x - 6" :y1="sym.y + 6" :x2="sym.x + 6" :y2="sym.y - 6" class="primary-line" />
          <line :x1="sym.x" :y1="sym.y + 8" :x2="sym.x" :y2="sym.y + 35" class="primary-line" />
          <text :x="sym.x + 12" :y="sym.y + 4" class="label">{{ sym.label }}</text>
        </g>

        <!-- Fallback -->
        <g
          v-else
          class="symbol"
          :class="{ selected: selectedId === sym.id }"
          @click="emit('select', sym.id)"
        >
          <rect :x="sym.x - 10" :y="sym.y - 10" width="20" height="20" rx="3" class="device-box" />
          <text :x="sym.x + 14" :y="sym.y + 4" class="label">{{ sym.label }}</text>
        </g>
      </template>

      <!-- Connections -->
      <g v-for="conn in connections" :key="conn.id" class="connection">
        <template v-if="resolveTerminal(conn.from, symbols) && resolveTerminal(conn.to, symbols)">
          <line
            :x1="resolveTerminal(conn.from, symbols)!.x"
            :y1="resolveTerminal(conn.from, symbols)!.y"
            :x2="resolveTerminal(conn.to, symbols)!.x"
            :y2="resolveTerminal(conn.to, symbols)!.y"
            class="primary-line"
          />
        </template>
      </g>

      <text x="20" y="282" class="title-block">ElectroScheme Studio — demo A3 sheet</text>
    </svg>
  </div>
</template>
