import { spawn } from "node:child_process";
import { readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { loadVerifiedPackageManifest } from "./package-manifest.mjs";

const separator = process.argv.indexOf("--");
if (separator < 0) throw new Error("usage: run-candidate-scenario.mjs <candidate> <output> -- <command> [args]");
const candidate = process.argv[2];
const output = path.resolve(process.argv[3]);
const command = process.argv[separator + 1];
const args = process.argv.slice(separator + 2);
if (!candidate || !output || !command) throw new Error("candidate, output and command are required");
await rm(output, { force: true });
const packageEvidence = await loadVerifiedPackageManifest(candidate, command, args);
const electronWindows = candidate === "electron" && process.platform === "win32";
const electronLog = electronWindows ? path.resolve(path.dirname(output), "electron-chromium-windows.log") : null;
if (electronLog) await rm(electronLog, { force: true });
const launchArgs = electronWindows ? [...args, "--no-stdio-init"] : args;
const launchEnv = {
  ...process.env,
  SPIKE_SCENARIO_RESULT: output,
  SPIKE_SMOKE: "1",
  ...(electronWindows ? {
    ELECTRON_ENABLE_LOGGING: "1",
    ELECTRON_ENABLE_STACK_DUMPING: "1",
    ELECTRON_LOG_FILE: electronLog
  } : {})
};

function formatExitCode(code) {
  if (typeof code !== "number") return String(code ?? "unknown");
  return `${code} (0x${(code >>> 0).toString(16).padStart(8, "0")})`;
}
async function electronDiagnosticSuffix() {
  if (!electronLog) return "";
  try {
    const text = await readFile(electronLog, "utf8");
    const tail = text.slice(-16_000);
    return `\nElectron Chromium log (${electronLog}):\n${tail || "<empty>"}`;
  } catch {
    return `\nElectron Chromium log was not created at ${electronLog}`;
  }
}

const child = spawn(command, launchArgs, {
  env: launchEnv,
  stdio: ["ignore", "inherit", "inherit"]
});
let observedExit = false;
let observedExitCode = null;
const exitPromise = new Promise((resolve, reject) => {
  child.once("error", reject);
  child.once("close", code => {
    observedExit = true;
    observedExitCode = code;
    resolve(code);
  });
});

function sleep(milliseconds) { return new Promise(resolve => setTimeout(resolve, milliseconds)); }
async function waitForResult() {
  const deadline = Date.now() + 60_000;
  while (Date.now() < deadline) {
    try { return JSON.parse(await readFile(output, "utf8")); } catch {}
    if (observedExit) {
      throw new Error(`${candidate} exited with ${formatExitCode(observedExitCode)} before producing scenario evidence${await electronDiagnosticSuffix()}`);
    }
    await sleep(100);
  }
  child.kill();
  throw new Error(`${candidate} did not produce scenario evidence within 60 seconds${await electronDiagnosticSuffix()}`);
}

async function waitForExit() {
  let timer;
  try {
    return await Promise.race([
      exitPromise,
      new Promise((_, reject) => {
        timer = setTimeout(() => {
          child.kill();
          reject(new Error(`${candidate} did not exit after scenario`));
        }, 10_000);
      })
    ]);
  } finally {
    clearTimeout(timer);
  }
}

const result = await waitForResult();
const exitCode = await waitForExit();
if (exitCode !== 0) throw new Error(`${candidate} exited with ${formatExitCode(exitCode)}${await electronDiagnosticSuffix()}`);
if (result.status !== "ok") throw new Error(`${candidate} scenario status is ${result.status}: ${result.error ?? "check failure"}`);
const failed = Object.entries(result.checks ?? {}).filter(([, value]) => value !== true).map(([name]) => name);
if (failed.length) throw new Error(`${candidate} scenario checks failed: ${failed.join(", ")}`);
result.harness = {
  launch_command: [command, ...launchArgs],
  working_directory: process.cwd(),
  package_evidence: packageEvidence,
  electron_windows_diagnostics: electronWindows ? {
    no_stdio_init: true,
    chromium_log: electronLog,
    stack_dumping_enabled: true
  } : null
};
await writeFile(output, JSON.stringify(result, null, 2) + "\n", "utf8");
console.log(JSON.stringify(result, null, 2));
