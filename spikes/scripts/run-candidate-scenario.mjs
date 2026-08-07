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
function exitEvidence(code) {
  if (typeof code !== "number") return { decimal: null, hex: null };
  return { decimal: code, hex: `0x${(code >>> 0).toString(16).padStart(8, "0")}` };
}
async function electronDiagnosticText() {
  if (!electronLog) return null;
  try {
    const text = await readFile(electronLog, "utf8");
    return text.slice(-16_000);
  } catch {
    return null;
  }
}
async function diagnosticSuffix() {
  if (!electronLog) return "";
  const text = await electronDiagnosticText();
  return text === null
    ? `\nElectron Chromium log was not created at ${electronLog}`
    : `\nElectron Chromium log (${electronLog}):\n${text || "<empty>"}`;
}
async function persistFailure(error, exitCode) {
  const exit = exitEvidence(exitCode);
  const nativeWindowsElectron = electronWindows && exit.hex === "0x80000003";
  const failure = {
    candidate,
    status: "failed",
    failure_class: nativeWindowsElectron ? "native_startup_failure" : "candidate_scenario_failure",
    secure_runtime_required: true,
    platform: process.platform,
    architecture: process.arch,
    error: error instanceof Error ? error.message : String(error),
    exit_code_decimal: exit.decimal,
    exit_code_hex: exit.hex,
    harness: {
      launch_command: [command, ...launchArgs],
      working_directory: process.cwd(),
      package_evidence: packageEvidence,
      electron_windows_diagnostics: electronWindows ? {
        no_stdio_init: true,
        chromium_log: electronLog,
        chromium_log_tail: await electronDiagnosticText(),
        stack_dumping_enabled: true
      } : null
    }
  };
  await writeFile(output, JSON.stringify(failure, null, 2) + "\n", "utf8");
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
      throw new Error(`${candidate} exited with ${formatExitCode(observedExitCode)} before producing scenario evidence${await diagnosticSuffix()}`);
    }
    await sleep(100);
  }
  child.kill();
  throw new Error(`${candidate} did not produce scenario evidence within 60 seconds${await diagnosticSuffix()}`);
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

try {
  const result = await waitForResult();
  const exitCode = await waitForExit();
  if (exitCode !== 0) throw new Error(`${candidate} exited with ${formatExitCode(exitCode)}${await diagnosticSuffix()}`);
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
} catch (error) {
  await persistFailure(error, observedExitCode);
  throw error;
}
