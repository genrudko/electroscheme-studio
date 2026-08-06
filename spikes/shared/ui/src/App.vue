<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { CommandHistory, createCanonicalFixture, encodeClipboard, parseProject, renderDeterministicPdf, serializeProject } from "@core";
import { host } from "./host.ts";
const history = new CommandHistory(createCanonicalFixture());
const project = ref(history.current);
const selected = ref("object-symbol-0001");
const status = ref("initializing");
const candidate = host.candidate();
const objects = computed(() => project.value.objects);
function move() { project.value = history.execute({ type: "MoveObjects", objectIds: [selected.value], dx: 17, dy: 24, grid: 10 }); status.value = "moved through command path"; }
function undo() { project.value = history.undo(); status.value = "undo"; }
function redo() { project.value = history.redo(); status.value = "redo"; }
async function copy() { await host.writeStructured(encodeClipboard(project.value,[selected.value])); status.value="structured clipboard copied"; }
async function paste() { const text=await host.readStructured(); status.value=`structured clipboard ${text.length} bytes`; }
async function openFile() { const text=await host.openProject(); if(text){ project.value=parseProject(text); status.value="opened through native dialog adapter"; } }
async function saveFile() { const ok=await host.saveProject("desktop-platform-spike.esspike.json",serializeProject(project.value)); status.value=ok?"saved through native dialog adapter":"save cancelled"; }
async function onBrowserDrop(event: DragEvent) { event.preventDefault(); const file=event.dataTransfer?.files[0]; if(!file)return; const text=await host.readBrowserDroppedFile(file); if(text){ project.value=parseProject(text); status.value="opened through browser-to-host drag/drop adapter"; } }
async function pdf() { const ok=await host.exportPdf("desktop-platform-spike.pdf",renderDeterministicPdf(project.value)); status.value=ok?"deterministic PDF exported":"PDF export cancelled"; }
let unsubscribe: (()=>void)|undefined;
onMounted(async()=>{ unsubscribe=await host.subscribe(async path=>{ project.value=parseProject(await host.readDroppedPath(path)); status.value="opened through native drag/drop adapter"; }); status.value=`ready on ${await host.platform()}`; await host.markReady(); });
onUnmounted(()=>unsubscribe?.());
</script>
<template>
  <main @dragover.prevent @drop="onBrowserDrop">
    <header><strong>ElectroScheme executable spike</strong><span>{{ candidate }}</span><span>{{ status }}</span></header>
    <nav><button @click="openFile">Open</button><button @click="saveFile">Save</button><button @click="move">Move + snap</button><button @click="undo">Undo</button><button @click="redo">Redo</button><button @click="copy">Copy</button><button @click="paste">Paste</button><button @click="pdf">PDF</button></nav>
    <svg viewBox="0 0 800 500" aria-label="shared editor fixture">
      <defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M 20 0 L 0 0 0 20" fill="none" stroke="#ddd" stroke-width="1"/></pattern></defs>
      <rect width="800" height="500" fill="url(#grid)"/>
      <g v-for="o in objects" :key="o.id" :data-object-id="o.id" @click="selected=o.id">
        <rect v-if="o.kind==='busbar'" :x="o.x" :y="o.y" :width="o.width" :height="o.height" />
        <g v-else :transform="`translate(${o.x} ${o.y})`"><rect :width="o.width" :height="o.height" rx="4"/><text :x="o.width/2" :y="o.height/2+5" text-anchor="middle">TEST</text></g>
      </g>
    </svg>
  </main>
</template>
<style>
:root{font-family:system-ui,sans-serif;color:#111;background:#f4f5f7}body{margin:0}main{display:grid;grid-template-rows:auto auto 1fr;height:100vh}header,nav{display:flex;gap:12px;align-items:center;padding:10px 14px;background:white;border-bottom:1px solid #ccc}header span:last-child{margin-left:auto}button{padding:6px 10px}svg{width:100%;height:100%;background:white}svg g{fill:white;stroke:#111;stroke-width:2}svg text{fill:#111;stroke:none;font-size:14px}
</style>
