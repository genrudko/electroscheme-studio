import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const scripts = path.dirname(fileURLToPath(new URL("../run-candidate-scenario.mjs", import.meta.url)));

async function createCandidateBundle(directory) {
  const packageRoot = path.join(directory, "candidate-package");
  await mkdir(packageRoot, { recursive: true });
  const candidate = path.join(packageRoot, "candidate.mjs");
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
  const archive = path.join(directory, "candidate.tar.gz");
  const archiveBytes = Buffer.from("deterministic-test-archive");
  await writeFile(archive, archiveBytes);
  const manifest = path.join(directory, "candidate-package-manifest.json");
  await writeFile(manifest, JSON.stringify({
    protocol: "electroscheme-candidate-package/1",
    candidate: "test-candidate",
    package_root: packageRoot,
    archive_path: archive,
    archive_sha256: createHash("sha256").update(archiveBytes).digest("hex"),
    archive_size_bytes: archiveBytes.length,
    unpacked_tree_sha256: "0".repeat(64),
    unpacked_size_bytes: 1,
    unpacked_file_count: 1,
    artifact_layout_round_trip_verified: true
  }), "utf8");
  return { candidate, manifest };
}

function packageEnvironment(manifest) {
  return {
    ...process.env,
    SPIKE_PACKAGE_MANIFEST: manifest,
    SPIKE_REQUIRE_PACKAGE_MANIFEST: "1"
  };
}

test("scenario harness observes early exit and records verified package evidence", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "electroscheme-scenario-harness-"));
  const { candidate, manifest } = await createCandidateBundle(directory);
  const output = path.join(directory, "scenario.json");
  const { stdout } = await execFileAsync(process.execPath, [
    path.join(scripts, "run-candidate-scenario.mjs"),
    "test-candidate",
    output,
    "--",
    process.execPath,
    candidate
  ], { timeout: 15_000, env: packageEnvironment(manifest) });
  const result = JSON.parse(await readFile(output, "utf8"));
  assert.equal(result.status, "ok");
  assert.equal(result.checks.immediate_exit, true);
  assert.equal(result.harness.package_evidence.artifact_layout_round_trip_verified, true);
  assert.equal(result.harness.package_evidence.launched_from_verified_package_root, true);
  assert.match(stdout, /immediate_exit/);
});

test("measurement harness uses candidate pid and records verified package evidence", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "electroscheme-measurement-harness-"));
  const { candidate, manifest } = await createCandidateBundle(directory);
  const output = path.join(directory, "measurement.json");
  await execFileAsync(process.execPath, [
    path.join(scripts, "measure-candidate.mjs"),
    "test-candidate",
    output,
    "--",
    process.execPath,
    candidate
  ], { timeout: 15_000, env: packageEnvironment(manifest) });
  const result = JSON.parse(await readFile(output, "utf8"));
  assert.equal(result.candidate, "test-candidate");
  assert.equal(result.ready.candidate, "test-candidate");
  assert.equal(result.measurement_root_pid, result.ready.pid);
  assert.equal(result.package_evidence.artifact_layout_round_trip_verified, true);
  assert.equal(result.package_evidence.launched_from_verified_package_root, true);
  assert.equal(typeof result.startup_to_renderer_ready_ms, "number");
  assert.ok(result.idle_process_tree_rss_bytes > 0);
});
