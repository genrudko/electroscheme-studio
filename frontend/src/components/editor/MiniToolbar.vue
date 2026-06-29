<template>
  <div class="mini-toolbar" :style="{ left: `${x}px`, top: `${y}px` }" @pointerdown.stop>
    <span class="mini-title">{{ title }}</span>
    <button type="button" title="Копировать" @click="$emit('command', 'copy')">⧉</button>
    <button type="button" title="Повернуть +90°" @click="$emit('command', 'rotate_90')">+90°</button>
    <button type="button" title="Повернуть -90°" @click="$emit('command', 'rotate_minus_90')">-90°</button>
    <button type="button" title="Удалить" class="danger" @click="$emit('command', 'delete')">⌫</button>
  </div>
</template>
<script setup lang="ts">
import type { EditorCommand } from '../../lib/editor/interactionModes'
defineProps<{ x: number; y: number; title: string }>()
defineEmits<{ command: [command: EditorCommand] }>()
</script>
<style scoped>
.mini-toolbar{position:absolute;z-index:30;display:flex;align-items:center;gap:4px;transform:translate(-50%,-100%);padding:5px 6px;border:1px solid #cbd5e1;border-radius:8px;background:rgba(255,255,255,.96);box-shadow:0 10px 24px rgba(15,23,42,.17);white-space:nowrap}.mini-title{max-width:120px;overflow:hidden;color:#475569;font-size:11px;font-weight:800;text-overflow:ellipsis}.mini-toolbar button{height:25px;min-width:27px;border:1px solid #dbeafe;border-radius:6px;background:#f8fafc;color:#1e3a8a;cursor:pointer;font-size:11px;font-weight:800}.mini-toolbar button.danger{color:#b91c1c}
</style>
