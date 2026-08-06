import { contextBridge, ipcRenderer, webUtils } from "electron";
contextBridge.exposeInMainWorld("electroHost", {
  candidate: () => "electron",
  platform: () => ipcRenderer.invoke("platform"),
  markReady: () => ipcRenderer.invoke("mark-ready"),
  openProject: () => ipcRenderer.invoke("open-project"),
  saveProject: (defaultName: string, content: string) => ipcRenderer.invoke("save-project", { defaultName, content }),
  readPath: (path: string) => ipcRenderer.invoke("read-path", path),
  writePath: (path: string, content: string) => ipcRenderer.invoke("write-path", { path, content }),
  writeStructured: (text: string) => ipcRenderer.invoke("clipboard-write", text),
  readStructured: () => ipcRenderer.invoke("clipboard-read"),
  subscribe: async () => () => {},
  readDroppedPath: (path: string) => ipcRenderer.invoke("read-path", path),
  readBrowserDroppedFile: (file: File) => ipcRenderer.invoke("read-path", webUtils.getPathForFile(file)),
  exportPdf: (defaultName: string, bytes: Uint8Array) => ipcRenderer.invoke("export-pdf", { defaultName, bytes: Array.from(bytes) }),
  runVisioTool: (args: string[]) => ipcRenderer.invoke("run-visio-tool", args)
});
