import { spawn } from "node:child_process";
import { readFile, rm } from "node:fs/promises";
import path from "node:path";

const separator = process.argv.indexOf("--");
if (separator < 0) throw new Error("usage: run-candidate-scenario.mjs <candidate> <output> -- <command> [args]");
const candidate = process.argv[2];
const output = path.resolve(process.argv[3]);
const command = process.argv[separator + 1];
const args = process.argv.slice(separator + 2);
if (!candidate || !output || !command) throw new Error("candidate, output and command are required");
await rm(output, { force: true });

const child = spawn(command, args, {
  env: { ...process.env, SPIKE_SCENARIO_RESULT: output, SPIKE_SMOKE: "1" },
  stdio: ["ignore", "inherit", "inherit"]
});

function sleep(milliseconds) { return new Promise(resolve => setTimeout(resolve, milliseconds)); }
async function waitForResult() {
  const deadline = Date.now() + 60_000;
  while (Date.now() < deadline) {
    try { return JSON.parse(await readFile(output, "utf8")); } catch { await sleep(100); }
  }
  child.kill();
  throw new Error(`${candidate} did not produce scenario evidence within 60 seconds`);
}

const result = await waitForResult();
const exitCode = await new Promise((resolve, reject) => {
  const timer = setTimeout(() => { child.kill(); reject(new Error(`${candidate} did not exit after scenario`)); }, 10_000);
  child.on("error", reject);
  child.on("close", code => { clearTimeout(timer); resolve(code); });
});
if (exitCode !== 0) throw new Error(`${candidate} exited with ${exitCode}`);
if (result.status !== "ok") throw new Error(`${candidate} scenario status is ${result.status}: ${result.error ?? "check failure"}`);
const failed = Object.entries(result.checks ?? {}).filter(([, value]) => value !== true).map(([name]) => name);
if (failed.length) throw new Error(`${candidate} scenario checks failed: ${failed.join(", ")}`);
console.log(JSON.stringify(result, null, 2));
