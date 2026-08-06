import { spawn, spawnSync } from "node:child_process";
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { performance } from "node:perf_hooks";

const separator = process.argv.indexOf("--");
if (separator < 0) throw new Error("usage: measure-candidate.mjs <candidate> <output> -- <command> [args]");
const candidate = process.argv[2];
const output = process.argv[3];
const command = process.argv[separator + 1];
const args = process.argv.slice(separator + 2);
if (!candidate || !output || !command) throw new Error("candidate, output and command are required");
const readyFile = path.resolve(path.dirname(output), `${candidate}-ready.json`);
await mkdir(path.dirname(output), { recursive: true });
await rm(readyFile, { force: true });
const started = performance.now();
const child = spawn(command, args, {
  env: { ...process.env, SPIKE_MEASURE: "1", SPIKE_READY_FILE: readyFile },
  stdio: ["ignore", "inherit", "inherit"]
});
const exitPromise = new Promise((resolve, reject) => {
  child.once("error", reject);
  child.once("close", code => resolve(code));
});

function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
async function waitForReady() {
  const deadline = performance.now() + 30_000;
  while (performance.now() < deadline) {
    try { return JSON.parse(await readFile(readyFile, "utf8")); } catch { await sleep(50); }
  }
  child.kill();
  throw new Error(`${candidate} did not report ready within 30 seconds`);
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
  return Promise.race([
    exitPromise,
    sleep(10_000).then(() => {
      child.kill();
      throw new Error(`${candidate} did not exit after measurement`);
    })
  ]);
}

const ready = await waitForReady();
const startupMs = performance.now() - started;
await sleep(400);
const rssBytes = process.platform === "win32" ? descendantsWindows(child.pid) : descendantsLinux(child.pid);
const exitCode = await waitForExit();
if (exitCode !== 0) throw new Error(`${candidate} exited with ${exitCode}`);
const result = {
  candidate,
  runner: `${process.platform}-${process.arch}`,
  command: [command, ...args],
  startup_to_renderer_ready_ms: startupMs,
  idle_process_tree_rss_bytes: rssBytes,
  measurement_scope: "single CI launch; ready marker emitted after Vue mount and host handshake; RSS is root process plus descendants 400 ms after ready",
  ready
};
await writeFile(output, JSON.stringify(result, null, 2) + "\n", "utf8");
console.log(JSON.stringify(result, null, 2));
