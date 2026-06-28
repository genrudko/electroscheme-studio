<script setup lang="ts">
import { computed } from 'vue'
import type { SymbolDefinition, SymbolState } from '../lib/types'

const props = defineProps<{
  definition: SymbolDefinition
  currentState?: string
  size?: number
}>()

const emit = defineEmits<{
  stateChange: [symbolType: string, newState: string]
}>()

const activeState = computed(() => props.currentState ?? props.definition.default_state)

const stateObj = computed<SymbolState | undefined>(() =>
  props.definition.states.find((s) => s.id === activeState.value)
)

const svgContent = computed(() => {
  const alt = stateObj.value?.alternate_svg
  if (alt) return alt
  return props.definition.svg
})

const viewBox = computed(() => props.definition.viewBox)

const svgWidth = computed(() => {
  if (props.size) return props.size
  return props.definition.default_width
})

const svgHeight = computed(() => {
  if (props.size) return props.size
  return props.definition.default_height
})

const isInteractive = computed(() => props.definition.interactive)

const nextState = computed(() => {
  const states = props.definition.states
  if (states.length < 2) return null
  const idx = states.findIndex((s) => s.id === activeState.value)
  return states[(idx + 1) % states.length]
})

function handleClick() {
  if (!isInteractive.value || !nextState.value) return
  emit('stateChange', props.definition.type, nextState.value.id)
}

const stateLabel = computed(() => stateObj.value?.name ?? activeState.value)
</script>

<template>
  <g
    class="svg-symbol"
    :class="{
      interactive: isInteractive,
      [`state-${activeState}`]: true,
    }"
    @click.stop="handleClick"
  >
    <svg
      :viewBox="viewBox"
      :width="svgWidth"
      :height="svgHeight"
      class="svg-symbol-content"
      v-html="svgContent"
    />
    <title v-if="isInteractive">
      {{ definition.name }} — {{ stateLabel }} (клик для переключения)
    </title>
  </g>
</template>
