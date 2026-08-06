import { cp, mkdir, rm } from "node:fs/promises";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const suffix = process.platform === "win32" ? ".exe" : "";
const source = path.join(root, "tauri", "src-tauri", "target", "release", `electroscheme-tauri-spike${suffix}`);
const generatedVisio = path.join(root, "evidence", "generated", "visio-fixtures");
const out = path.join(root, "evidence", "generated", `tauri-portable-${process.platform}-x64`);

await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
await cp(source, path.join(out, `ElectroSchemeSpikeTauri${suffix}`));
await cp(path.join(root, "tools"), path.join(out, "tools"), { recursive: true });
await cp(path.join(root, "shared", "fixtures"), path.join(out, "fixtures"), { recursive: true });
await mkdir(path.join(out, "fixtures", "visio"), { recursive: true });
for (const name of ["controlled-minimal.vsdx", "controlled-master.vssx"]) {
  await cp(path.join(generatedVisio, name), path.join(out, "fixtures", "visio", name));
}
console.log(JSON.stringify({ candidate: "tauri", output: out }, null, 2));
