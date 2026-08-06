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

async function createCandidate(directory) {
  const candidate = path.join(directory, "candidate.mjs");
  await writeFile(candidate, `
    import { writeFileSync } from "node:fs";
    if (process.env.SPIKE_SCENARIO_RESULT) {
      writeFileSync(process.env.SPIKE_SCENARIO_RESULT, JSON.stringify({ status: "ok", checks: { immediate_exit: true } }));
    }
    if (process.env.SPIKE_READY_FILE) {
      writeFileSync(process.env.SPIKE_READY_FILE, JSON.stringify({ candidate: "test-candidate", pid: process.pid, ready_epoch_ms: Date.now() }));
      setTimeout(() => process.exit(0), 700);
    }
  `, "utf8");
  return candidate;
}

test("scenario harness observes a candidate that exits immediately after evidence", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "electroscheme-scenario-harness-"));
  const candidate = await createCandidate(directory);
  const output = path.join(directory, "scenario.json");
  const { stdout } = await execFileAsync(process.execPath, [
    path.join(scripts, "run-candidate-scenario.mjs"),
    "test-candidate",
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

test("measurement harness measures the candidate-reported root and observes its early exit", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "electroscheme-measurement-harness-"));
  const candidate = await createCandidate(directory);
  const output = path.join(directory, "measurement.json");
  await execFileAsync(process.execPath, [
    path.join(scripts, "measure-candidate.mjs"),
    "test-candidate",
    output,
    "--",
    process.execPath,
    candidate
  ], { timeout: 15_000 });
  const result = JSON.parse(await readFile(output, "utf8"));
  assert.equal(result.candidate, "test-candidate");
  assert.equal(result.ready.candidate, "test-candidate");
  assert.equal(result.measurement_root_pid, result.ready.pid);
  assert.equal(typeof result.startup_to_renderer_ready_ms, "number");
  assert.ok(result.idle_process_tree_rss_bytes > 0);
});
