import { app, BrowserWindow, clipboard, dialog, ipcMain, type IpcMainInvokeEvent } from "electron";
import { spawn } from "node:child_process";
import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const spikeRoot = app.isPackaged ? app.getAppPath() : path.resolve(here, "../..");
const toolRoot = app.isPackaged ? path.join(process.resourcesPath, "app.asar.unpacked") : spikeRoot;
const ui = path.join(spikeRoot, "shared/ui/dist/index.html");
let windowRef: BrowserWindow | null = null;

type SavePayload = { defaultName: string; content: string };
type WritePayload = { path: string; content: string };
type PdfPayload = { defaultName: string; bytes: number[] };
type ToolResult = { exitCode: number; stdout: string; stderr: string };

function register(): void {
  ipcMain.handle("platform", () => process.platform);
  ipcMain.handle("mark-ready", () => { if (process.env.SPIKE_SMOKE === "1") setTimeout(() => app.quit(), 100); });
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
  ipcMain.handle("clipboard-write", (_event: IpcMainInvokeEvent, text: string) => clipboard.writeText(text, "clipboard"));
  ipcMain.handle("clipboard-read", () => clipboard.readText("clipboard"));
  ipcMain.handle("export-pdf", async (_event: IpcMainInvokeEvent, { defaultName, bytes }: PdfPayload) => {
    const result = await dialog.showSaveDialog({ defaultPath: defaultName, filters: [{ name: "PDF", extensions: ["pdf"] }] });
    if (result.canceled || !result.filePath) return false;
    await fs.writeFile(result.filePath, Buffer.from(bytes));
    return true;
  });
  ipcMain.handle("run-visio-tool", (_event: IpcMainInvokeEvent, args: string[]) => new Promise<ToolResult>(resolve => {
    const tool = path.join(toolRoot, "tools/visio_spike_tool.py");
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
  windowRef = new BrowserWindow({
    width: 1000,
    height: 700,
    show: true,
    webPreferences: {
      preload: path.join(here, "preload.js"),
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
