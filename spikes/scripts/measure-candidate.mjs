import { spawn, spawnSync } from "node:child_process";
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { performance } from "node:perf_hooks";
import { loadVerifiedPackageManifest } from "./package-manifest.mjs";

const separator = process.argv.indexOf("--");
if (separator < 0) throw new Error("usage: measure-candidate.mjs <candidate> <output> -- <command> [args]");
const candidate = process.argv[2];
const output = process.argv[3];
const command = process.argv[separator + 1];
const args = process.argv.slice(separator + 2);
if (!candidate || !output || !command) throw new Error("candidate, output and command are required");
const packageEvidence = await loadVerifiedPackageManifest(candidate, command, args);
const readyFile = path.resolve(path.dirname(output), `${candidate}-ready.json`);
await mkdir(path.dirname(output), { recursive: true });
await rm(readyFile, { force: true });
const electronWindows = candidate === "electron" && process.platform === "win32";
const electronLog = electronWindows ? path.resolve(path.dirname(output), "electron-chromium-measure-windows.log") : null;
if (electronLog) await rm(electronLog, { force: true });
const launchArgs = electronWindows ? [...args, "--no-stdio-init"] : args;
const launchEnv = {
  ...process.env,
  SPIKE_MEASURE: "1",
  SPIKE_READY_FILE: readyFile,
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

const started = performance.now();
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

function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
async function waitForReady() {
  const readyTimeoutMs = candidate === "tauri" ? 60_000 : 30_000;
  const deadline = performance.now() + readyTimeoutMs;
  while (performance.now() < deadline) {
    try { return JSON.parse(await readFile(readyFile, "utf8")); } catch {}
    if (observedExit) {
      throw new Error(`${candidate} exited with ${formatExitCode(observedExitCode)} before reporting ready${await electronDiagnosticSuffix()}`);
    }
    await sleep(50);
  }
  child.kill();
  throw new Error(`${candidate} did not report ready within ${readyTimeoutMs / 1000} seconds${await electronDiagnosticSuffix()}`);
}
function descendantsLinux(rootPid) {
  const rows = spawnSync("ps", ["-e", "-o", "pid=,ppid=,rss="], { encoding: "utf8" }).stdout.trim().split(/\r?\n/).map(line => line.trim().split(/\s+/).map(Number));
  const selected = new Set([rootPid]);
  let changed = true;
  while (changed) { changed = false; for (const [pid, ppid] of rows) if (selected.has(ppid) && !selected.has(pid)) { selected.add(pid); changed = true; } }
  return rows.filter(([pid]) => selected.has(pid)).reduce((sum, row) => sum + (row[2] ?? 0) * 1024, 0);
}
function descendantsWindows(rootPid) {
  const script = `$r=${rootPid};$a=Get-CimInstance Win32_Process|Select-Object ProcessId,ParentProcessId,WorkingSetSize;$s=New-Object 'System.Collections.Generic.HashSet[int]';[void]$s.Add($r);do{$c=$false;foreach($p in $a){if($s.Contains([int]$p.ParentProcessId)-and-not $s.Contains([int]$p.ProcessId)){[void]$s.Add([int]$p.ProcessId);$c=$true}}}while($c);($a|Where-Object{$s.Contains([int]$_.ProcessId)}|Measure-Object WorkingSetSize -Sum).Sum`;
  const result = spawnSync("powershell", ["-NoProfile", "-Command", script], { encoding: "utf8" });
  if (result.status !== 0) throw new Error(result.stderr || "PowerShell process measurement failed");
  return Number(result.stdout.trim());
}
async function waitForExit() {
  let timer;
  try {
    return await Promise.race([
      exitPromise,
      new Promise((_, reject) => {
        timer = setTimeout(() => {
          child.kill();
          reject(new Error(`${candidate} did not exit after measurement`));
        }, 10_000);
      })
    ]);
  } finally {
    clearTimeout(timer);
  }
}

const ready = await waitForReady();
if (!Number.isInteger(ready.pid) || ready.pid <= 0) throw new Error(`${candidate} ready evidence does not contain a valid process pid`);
const startupMs = performance.now() - started;
await sleep(400);
const rssBytes = process.platform === "win32" ? descendantsWindows(ready.pid) : descendantsLinux(ready.pid);
if (!Number.isFinite(rssBytes) || rssBytes <= 0) throw new Error(`${candidate} process-tree RSS was not measurable from pid ${ready.pid}`);
const exitCode = await waitForExit();
if (exitCode !== 0) throw new Error(`${candidate} exited with ${formatExitCode(exitCode)}${await electronDiagnosticSuffix()}`);
const result = {
  candidate,
  runner: `${process.platform}-${process.arch}`,
  command: [command, ...launchArgs],
  startup_to_renderer_ready_ms: startupMs,
  idle_process_tree_rss_bytes: rssBytes,
  measurement_root_pid: ready.pid,
  measurement_scope: "single CI launch; ready marker emitted after Vue mount and host handshake; RSS is the candidate-reported root process plus descendants 400 ms after ready; display-server wrapper processes are excluded",
  package_evidence: packageEvidence,
  electron_windows_diagnostics: electronWindows ? {
    no_stdio_init: true,
    chromium_log: electronLog,
    stack_dumping_enabled: true
  } : null,
  ready
};
await writeFile(output, JSON.stringify(result, null, 2) + "\n", "utf8");
console.log(JSON.stringify(result, null, 2));
