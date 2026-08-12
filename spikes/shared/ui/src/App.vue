<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import {
  CommandHistory,
  createCanonicalFixture,
  decodeClipboard,
  encodeClipboard,
  parseProject,
  renderDeterministicPdf,
  serializeProject,
  type AutomationContext,
  type CanonicalProject
} from "@core";
import { host } from "./host.ts";

let history = new CommandHistory(createCanonicalFixture());
const project = ref(history.current);
const selected = ref("object-symbol-0001");
const status = ref("initializing");
const candidate = host.candidate();
const objects = computed(() => project.value.objects);

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

function adoptProject(next: CanonicalProject, success: string): void {
  history = new CommandHistory(next);
  project.value = history.current;
  selected.value = project.value.objects[0]?.id ?? "";
  status.value = success;
}

function move() {
  project.value = history.execute({ type: "MoveObjects", objectIds: [selected.value], dx: 17, dy: 24, grid: 10 });
  status.value = "moved through command path";
}
function undo() { project.value = history.undo(); status.value = "undo"; }
function redo() { project.value = history.redo(); status.value = "redo"; }

async function copy() {
  try {
    const payload = encodeClipboard(project.value, [selected.value]);
    await host.writeStructured(payload);
    status.value = "structured clipboard copied";
  } catch (error) {
    status.value = `clipboard failed: ${errorMessage(error)}`;
  }
}

async function paste() {
  try {
    const payload = decodeClipboard(await host.readStructured());
    status.value = `structured clipboard accepted: ${payload.objects.length} object(s)`;
  } catch (error) {
    status.value = `clipboard failed: ${errorMessage(error)}`;
  }
}

async function openFile() {
  try {
    const text = await host.openProject();
    if (text === null) {
      status.value = "open cancelled";
      return;
    }
    adoptProject(parseProject(text), "opened through native dialog adapter");
  } catch (error) {
    status.value = `open failed: ${errorMessage(error)}`;
  }
}

async function saveFile() {
  try {
    const ok = await host.saveProject("desktop-platform-spike.esspike.json", serializeProject(project.value));
    status.value = ok ? "saved through native dialog adapter" : "save cancelled";
  } catch (error) {
    const diagnostic = errorMessage(error);
    status.value = diagnostic.startsWith("save failed:") ? diagnostic : `save failed: ${diagnostic}`;
  }
}

async function onBrowserDrop(event: DragEvent) {
  event.preventDefault();
  const file = event.dataTransfer?.files[0];
  if (!file) return;
  try {
    const text = await host.readBrowserDroppedFile(file);
    if (text !== null) adoptProject(parseProject(text), "opened through browser-to-host drag/drop adapter");
  } catch (error) {
    status.value = `drop failed: ${errorMessage(error)}`;
  }
}

async function pdf() {
  try {
    const ok = await host.exportPdf("desktop-platform-spike.pdf", renderDeterministicPdf(project.value));
    status.value = ok ? "deterministic PDF exported" : "PDF export cancelled";
  } catch (error) {
    const diagnostic = errorMessage(error);
    status.value = diagnostic.startsWith("save failed:") ? diagnostic : `save failed: ${diagnostic}`;
  }
}

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
      try {
        const text = await host.readDroppedPath(path);
        adoptProject(parseProject(text), "opened through native drag/drop adapter");
      } catch (error) {
        status.value = `drop failed: ${errorMessage(error)}`;
      }
    });
    status.value = `ready on ${await host.platform()}`;
    const automation = await host.automationContext();
    if (automation) {
      status.value = "running automated platform scenario";
      await runAutomationScenario(automation);
      status.value = "automated platform scenario passed";
    }
  } catch (error) {
    status.value = errorMessage(error);
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
