import { packager } from "@electron/packager";
import { cp, mkdir, rm } from "node:fs/promises";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const input = path.join(root, "electron", "package-input");
const generatedVisio = path.join(root, "evidence", "generated", "visio-fixtures");
const packagedVisio = path.join(input, "shared", "fixtures", "visio");

await rm(input, { recursive: true, force: true });
await mkdir(input, { recursive: true });
await cp(path.join(root, "electron", "dist"), path.join(input, "dist"), { recursive: true });
await cp(path.join(root, "shared", "ui", "dist"), path.join(input, "shared", "ui", "dist"), { recursive: true });
await cp(path.join(root, "shared", "fixtures"), path.join(input, "shared", "fixtures"), { recursive: true });
await mkdir(packagedVisio, { recursive: true });
for (const name of ["controlled-minimal.vsdx", "controlled-master.vssx"]) {
  await cp(path.join(generatedVisio, name), path.join(packagedVisio, name));
}
await cp(path.join(root, "tools"), path.join(input, "tools"), { recursive: true });
await cp(path.join(root, "electron", "package.json"), path.join(input, "package.json"));

const out = path.join(root, "evidence", "generated", "electron-package");
await rm(out, { recursive: true, force: true });
const result = await packager({
  dir: input,
  name: "ElectroSchemeSpikeElectron",
  electronVersion: "43.3.0",
  platform: process.platform,
  arch: "x64",
  out,
  overwrite: true,
  asar: { unpackDir: "{tools,shared/fixtures}" }
});
console.log(JSON.stringify({ candidate: "electron", outputs: result }, null, 2));
