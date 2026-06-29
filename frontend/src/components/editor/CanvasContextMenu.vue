<template>
  <div v-if="visible" class="canvas-context-menu" :style="{ left: `${x}px`, top: `${y}px` }" @pointerdown.stop @contextmenu.prevent.stop>
    <button type="button" @click="$emit('command', 'create_sample_busbar')">Добавить шину</button>
    <button type="button" @click="$emit('command', 'create_circuit_breaker')">Добавить выключатель</button>
    <button type="button" @click="$emit('command', 'create_text')">Добавить текст</button>
    <button type="button" @click="$emit('command', 'create_rectangle')">Прямоугольник</button>
    <button type="button" @click="$emit('command', 'create_ellipse')">Эллипс</button>
    <button type="button" @click="$emit('command', 'create_line')">Линия</button><hr />
    <button type="button" :disabled="!hasSelection" @click="$emit('command', 'rotate_90')">Повернуть +90°</button>
    <button type="button" :disabled="!hasSelection" class="danger" @click="$emit('command', 'delete')">Удалить</button>
  </div>
</template>
<script setup lang="ts">
import type { EditorCommand } from '../../lib/editor/interactionModes'
defineProps<{ visible: boolean; x: number; y: number; hasSelection: boolean; canPaste: boolean }>()
defineEmits<{ command: [command: EditorCommand] }>()
</script>
<style scoped>
.canvas-context-menu{position:fixed;z-index:50;min-width:240px;padding:6px;border:1px solid #cbd5e1;border-radius:10px;background:white;box-shadow:0 16px 35px rgba(15,23,42,.2)}.canvas-context-menu button{display:block;width:100%;border:0;border-radius:7px;background:transparent;color:#0f172a;cursor:pointer;padding:8px 10px;text-align:left;font-weight:700}.canvas-context-menu button:hover:not(:disabled){background:#eff6ff;color:#1d4ed8}.canvas-context-menu button:disabled{color:#94a3b8;cursor:default}.canvas-context-menu button.danger{color:#b91c1c}.canvas-context-menu hr{border:0;border-top:1px solid #e2e8f0;margin:6px}
</style>
