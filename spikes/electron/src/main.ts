import { app, BrowserWindow, clipboard, dialog, ipcMain, type IpcMainInvokeEvent } from "electron";
import { spawn } from "node:child_process";
import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

app.disableHardwareAcceleration();

const processStartedAt = Date.now();
const here = path.dirname(fileURLToPath(import.meta.url));
const spikeRoot = app.isPackaged ? app.getAppPath() : path.resolve(here, "../..");
const unpackedRoot = app.isPackaged ? path.join(process.resourcesPath, "app.asar.unpacked") : spikeRoot;
const ui = path.join(spikeRoot, "shared/ui/dist/index.html");
let windowRef: BrowserWindow | null = null;

type SavePayload = { defaultName: string; content: string };
type WritePayload = { path: string; content: string };
type WriteBytesPayload = { path: string; bytes: number[] };
type PdfPayload = { defaultName: string; bytes: number[] };
type ToolResult = { exitCode: number; stdout: string; stderr: string };

function automationContext() {
  const resultPath = process.env.SPIKE_SCENARIO_RESULT;
  if (!resultPath) return null;
  const workspace = path.dirname(resultPath);
  const fixtures = path.join(unpackedRoot, "shared", "fixtures");
  return {
    resultPath,
    canonicalFixturePath: path.join(fixtures, "canonical-project.json"),
    vsdxFixturePath: path.join(fixtures, "visio", "controlled-minimal.vsdx"),
    vssxFixturePath: path.join(fixtures, "visio", "controlled-master.vssx"),
    roundTripPath: path.join(workspace, "electron-canonical-roundtrip.json"),
    pdfPath: path.join(workspace, "electron-deterministic-output.pdf"),
    generatedVsdxPath: path.join(workspace, "electron-generated-minimal.vsdx")
  };
}

function register(): void {
  ipcMain.handle("platform", () => process.platform);
  ipcMain.handle("automation-context", () => automationContext());
  ipcMain.handle("mark-ready", async () => {
    const readyFile = process.env.SPIKE_READY_FILE;
    if (readyFile) {
      await fs.writeFile(readyFile, JSON.stringify({ candidate: "electron", pid: process.pid, ready_epoch_ms: Date.now(), process_start_epoch_ms: processStartedAt }) + "\n", "utf8");
    }
    if (process.env.SPIKE_MEASURE === "1") setTimeout(() => app.quit(), 1500);
    else if (process.env.SPIKE_SMOKE === "1") setTimeout(() => app.quit(), 100);
  });
  ipcMain.handle("open-project", async () => {
    const result = await dialog.showOpenDialog({ properties: ["openFile"], filters: [{ name: "ElectroScheme spike", extensions: ["json"] }] });
    return result.canceled || !result.filePaths[0] ? null : fs.readFile(result.filePaths[0], "utf8");
  });
  ipcMain.handle("save-project", async (_event: IpcMainInvokeEvent, { defaultName, content }: SavePayload) => {
    const result = await dialog.showSaveDialog({ defaultPath: defaultName, filters: [{ name: "ElectroScheme spike", extensions: ["json"] }] });
    if (result.canceled || !result.filePath) return false;
    await fs.writeFile(result.filePath, content, "utf8");
    return true;
  });
  ipcMain.handle("read-path", (_event: IpcMainInvokeEvent, filePath: string) => fs.readFile(filePath, "utf8"));
  ipcMain.handle("write-path", async (_event: IpcMainInvokeEvent, { path: filePath, content }: WritePayload) => { await fs.writeFile(filePath, content, "utf8"); });
  ipcMain.handle("write-bytes-path", async (_event: IpcMainInvokeEvent, { path: filePath, bytes }: WriteBytesPayload) => { await fs.writeFile(filePath, Buffer.from(bytes)); });
  ipcMain.handle("clipboard-write", (_event: IpcMainInvokeEvent, text: string) => clipboard.writeText(text, "clipboard"));
  ipcMain.handle("clipboard-read", () => clipboard.readText("clipboard"));
  ipcMain.handle("export-pdf", async (_event: IpcMainInvokeEvent, { defaultName, bytes }: PdfPayload) => {
    const result = await dialog.showSaveDialog({ defaultPath: defaultName, filters: [{ name: "PDF", extensions: ["pdf"] }] });
    if (result.canceled || !result.filePath) return false;
    await fs.writeFile(result.filePath, Buffer.from(bytes));
    return true;
  });
  ipcMain.handle("run-visio-tool", (_event: IpcMainInvokeEvent, args: string[]) => new Promise<ToolResult>(resolve => {
    const tool = path.join(unpackedRoot, "tools", "visio_spike_tool.py");
    const child = spawn(process.platform === "win32" ? "python" : "python3", [tool, ...args], { stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";
    let settled = false;
    const finish = (result: ToolResult): void => { if (!settled) { settled = true; resolve(result); } };
    const timer = setTimeout(() => { child.kill(); finish({ exitCode: -2, stdout, stderr: `${stderr}timeout` }); }, 15_000);
    child.stdout.on("data", data => { stdout += String(data); });
    child.stderr.on("data", data => { stderr += String(data); });
    child.on("error", error => { clearTimeout(timer); finish({ exitCode: -1, stdout, stderr: `${stderr}${error.message}` }); });
    child.on("close", code => { clearTimeout(timer); finish({ exitCode: code ?? -1, stdout, stderr }); });
  }));
}

app.whenReady().then(() => {
  register();
  const automationLaunch = process.env.SPIKE_SMOKE === "1" || process.env.SPIKE_MEASURE === "1";
  windowRef = new BrowserWindow({
    width: 1000,
    height: 700,
    show: !automationLaunch,
    webPreferences: {
      preload: path.join(here, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true
    }
  });
  windowRef.webContents.setWindowOpenHandler(() => ({ action: "deny" }));
  void windowRef.loadFile(ui);
});

app.on("window-all-closed", () => app.quit());
