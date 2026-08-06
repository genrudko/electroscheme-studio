import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const scripts = path.dirname(fileURLToPath(new URL("../run-candidate-scenario.mjs", import.meta.url)));

async function createImmediateCandidate(directory) {
  const candidate = path.join(directory, "immediate-candidate.mjs");
  await writeFile(candidate, `
    import { writeFileSync } from "node:fs";
    if (process.env.SPIKE_SCENARIO_RESULT) {
      writeFileSync(process.env.SPIKE_SCENARIO_RESULT, JSON.stringify({ status: "ok", checks: { immediate_exit: true } }));
    }
    if (process.env.SPIKE_READY_FILE) {
      writeFileSync(process.env.SPIKE_READY_FILE, JSON.stringify({ candidate: "immediate", pid: process.pid, ready_epoch_ms: Date.now() }));
    }
  `, "utf8");
  return candidate;
}

test("scenario harness observes a candidate that exits immediately after evidence", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "electroscheme-scenario-harness-"));
  const candidate = await createImmediateCandidate(directory);
  const output = path.join(directory, "scenario.json");
  const { stdout } = await execFileAsync(process.execPath, [
    path.join(scripts, "run-candidate-scenario.mjs"),
    "immediate",
    output,
    "--",
    process.execPath,
    candidate
  ], { timeout: 15_000 });
  const result = JSON.parse(await readFile(output, "utf8"));
  assert.equal(result.status, "ok");
  assert.equal(result.checks.immediate_exit, true);
  assert.match(stdout, /immediate_exit/);
});

test("measurement harness observes a candidate that exits immediately after ready", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "electroscheme-measurement-harness-"));
  const candidate = await createImmediateCandidate(directory);
  const output = path.join(directory, "measurement.json");
  await execFileAsync(process.execPath, [
    path.join(scripts, "measure-candidate.mjs"),
    "immediate",
    output,
    "--",
    process.execPath,
    candidate
  ], { timeout: 15_000 });
  const result = JSON.parse(await readFile(output, "utf8"));
  assert.equal(result.candidate, "immediate");
  assert.equal(result.ready.candidate, "immediate");
  assert.equal(typeof result.startup_to_renderer_ready_ms, "number");
  assert.equal(typeof result.idle_process_tree_rss_bytes, "number");
});
