<template>
  <EditorShell />
</template>

<script setup lang="ts">
import EditorShell from './components/editor/EditorShell.vue'
</script>

<style>
:root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #0f172a;
  background: #e5edf7;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
}
</style>