<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import {
  CommandHistory,
  createCanonicalFixture,
  encodeClipboard,
  parseProject,
  renderDeterministicPdf,
  serializeProject,
  type AutomationContext
} from "@core";
import { host } from "./host.ts";

const history = new CommandHistory(createCanonicalFixture());
const project = ref(history.current);
const selected = ref("object-symbol-0001");
const status = ref("initializing");
const candidate = host.candidate();
const objects = computed(() => project.value.objects);

function move() {
  project.value = history.execute({ type: "MoveObjects", objectIds: [selected.value], dx: 17, dy: 24, grid: 10 });
  status.value = "moved through command path";
}
function undo() { project.value = history.undo(); status.value = "undo"; }
function redo() { project.value = history.redo(); status.value = "redo"; }
async function copy() { await host.writeStructured(encodeClipboard(project.value, [selected.value])); status.value = "structured clipboard copied"; }
async function paste() { const text = await host.readStructured(); status.value = `structured clipboard ${text.length} bytes`; }
async function openFile() { const text = await host.openProject(); if (text) { project.value = parseProject(text); status.value = "opened through native dialog adapter"; } }
async function saveFile() { const ok = await host.saveProject("desktop-platform-spike.esspike.json", serializeProject(project.value)); status.value = ok ? "saved through native dialog adapter" : "save cancelled"; }
async function onBrowserDrop(event: DragEvent) { event.preventDefault(); const file = event.dataTransfer?.files[0]; if (!file) return; const text = await host.readBrowserDroppedFile(file); if (text) { project.value = parseProject(text); status.value = "opened through browser-to-host drag/drop adapter"; } }
async function pdf() { const ok = await host.exportPdf("desktop-platform-spike.pdf", renderDeterministicPdf(project.value)); status.value = ok ? "deterministic PDF exported" : "PDF export cancelled"; }

async function sha256(value: string | Uint8Array): Promise<string> {
  const bytes = typeof value === "string" ? new TextEncoder().encode(value) : value;
  const buffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength) as ArrayBuffer;
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return Array.from(new Uint8Array(digest), item => item.toString(16).padStart(2, "0")).join("");
}

async function runAutomationScenario(context: AutomationContext): Promise<void> {
  const result: Record<string, unknown> = {
    protocol: "electroscheme-desktop-scenario/1",
    candidate,
    platform: await host.platform(),
    native_dialog_gate: "MANUAL_INTERACTION_EVIDENCE_REQUIRED",
    native_drag_drop_gate: "MANUAL_OS_EVENT_EVIDENCE_REQUIRED"
  };
  try {
    const sourceText = await host.readPath(context.canonicalFixturePath);
    const loaded = parseProject(sourceText);
    const serialized = serializeProject(loaded);
    await host.writePath(context.roundTripPath, serialized);
    const reopened = await host.readPath(context.roundTripPath);

    const clipboardPayload = encodeClipboard(loaded, ["object-symbol-0001"]);
    await host.writeStructured(clipboardPayload);
    const clipboardRoundTrip = await host.readStructured();

    const pdfBytes = renderDeterministicPdf(loaded);
    await host.writeBytesPath(context.pdfPath, pdfBytes);

    const vsdx = await host.runVisioTool(["inspect", "vsdx", context.vsdxFixturePath]);
    const vssx = await host.runVisioTool(["inspect", "vssx", context.vssxFixturePath]);
    const generated = await host.runVisioTool(["generate-vsdx", context.canonicalFixturePath, context.generatedVsdxPath]);
    const generatedInspection = await host.runVisioTool(["inspect", "vsdx", context.generatedVsdxPath]);

    const checks = {
      canonical_read: sourceText.length > 0,
      deterministic_round_trip: reopened === serialized && serializeProject(parseProject(reopened)) === serialized,
      structured_clipboard_round_trip: clipboardRoundTrip === clipboardPayload,
      deterministic_pdf_written: pdfBytes.length > 0,
      controlled_vsdx_read: vsdx.exitCode === 0 && JSON.parse(vsdx.stdout).status === "ok",
      controlled_vssx_read: vssx.exitCode === 0 && JSON.parse(vssx.stdout).status === "ok",
      minimal_vsdx_write: generated.exitCode === 0 && JSON.parse(generated.stdout).status === "ok",
      generated_vsdx_package_read: generatedInspection.exitCode === 0 && JSON.parse(generatedInspection.stdout).status === "ok"
    };
    result.checks = checks;
    result.hashes = {
      canonical_json_sha256: await sha256(serialized),
      clipboard_sha256: await sha256(clipboardPayload),
      pdf_sha256: await sha256(pdfBytes)
    };
    result.outputs = {
      roundTripPath: context.roundTripPath,
      pdfPath: context.pdfPath,
      generatedVsdxPath: context.generatedVsdxPath
    };
    result.tool_results = {
      vsdx: JSON.parse(vsdx.stdout),
      vssx: JSON.parse(vssx.stdout),
      generated: JSON.parse(generated.stdout),
      generatedInspection: JSON.parse(generatedInspection.stdout)
    };
    result.status = Object.values(checks).every(Boolean) ? "ok" : "failed";
  } catch (error) {
    result.status = "failed";
    result.error = error instanceof Error ? error.stack ?? error.message : String(error);
  }
  await host.writePath(context.resultPath, `${JSON.stringify(result, null, 2)}\n`);
  if (result.status !== "ok") throw new Error(`automated desktop scenario failed: ${String(result.error ?? "check failure")}`);
}

let unsubscribe: (() => void) | undefined;
onMounted(async () => {
  try {
    unsubscribe = await host.subscribe(async path => {
      project.value = parseProject(await host.readDroppedPath(path));
      status.value = "opened through native drag/drop adapter";
    });
    status.value = `ready on ${await host.platform()}`;
    const automation = await host.automationContext();
    if (automation) {
      status.value = "running automated platform scenario";
      await runAutomationScenario(automation);
      status.value = "automated platform scenario passed";
    }
  } catch (error) {
    status.value = error instanceof Error ? error.message : String(error);
  } finally {
    await host.markReady();
  }
});
onUnmounted(() => unsubscribe?.());
</script>

<template>
  <main @dragover.prevent @drop="onBrowserDrop">
    <header><strong>ElectroScheme executable spike</strong><span>{{ candidate }}</span><span>{{ status }}</span></header>
    <nav><button @click="openFile">Open</button><button @click="saveFile">Save</button><button @click="move">Move + snap</button><button @click="undo">Undo</button><button @click="redo">Redo</button><button @click="copy">Copy</button><button @click="paste">Paste</button><button @click="pdf">PDF</button></nav>
    <svg viewBox="0 0 800 500" aria-label="shared editor fixture">
      <defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M 20 0 L 0 0 0 20" fill="none" stroke="#ddd" stroke-width="1"/></pattern></defs>
      <rect width="800" height="500" fill="url(#grid)"/>
      <g v-for="object in objects" :key="object.id" :data-object-id="object.id" @click="selected = object.id">
        <rect v-if="object.kind === 'busbar'" :x="object.x" :y="object.y" :width="object.width" :height="object.height" />
        <g v-else :transform="`translate(${object.x} ${object.y})`"><rect :width="object.width" :height="object.height" rx="4"/><text :x="object.width / 2" :y="object.height / 2 + 5" text-anchor="middle">TEST</text></g>
      </g>
    </svg>
  </main>
</template>

<style>
:root{font-family:system-ui,sans-serif;color:#111;background:#f4f5f7}body{margin:0}main{display:grid;grid-template-rows:auto auto 1fr;height:100vh}header,nav{display:flex;gap:12px;align-items:center;padding:10px 14px;background:white;border-bottom:1px solid #ccc}header span:last-child{margin-left:auto}button{padding:6px 10px}svg{width:100%;height:100%;background:white}svg g{fill:white;stroke:#111;stroke-width:2}svg text{fill:#111;stroke:none;font-size:14px}
</style>
