import { invoke } from "@tauri-apps/api/core";
import { getCurrentWebview } from "@tauri-apps/api/webview";
import type { HostPorts } from "@core";

function tauriPorts(): HostPorts {
  return {
    candidate: () => "tauri",
    platform: () => invoke<string>("platform"),
    markReady: () => invoke<void>("mark_ready"),
    openProject: () => invoke<string | null>("open_project"),
    saveProject: (defaultName, content) => invoke<boolean>("save_project", { defaultName, content }),
    readPath: path => invoke<string>("read_path", { path }),
    writePath: (path, content) => invoke<void>("write_path", { path, content }),
    writeStructured: text => invoke<void>("clipboard_write", { text }),
    readStructured: () => invoke<string>("clipboard_read"),
    subscribe: async handler => getCurrentWebview().onDragDropEvent(event => {
      if (event.payload.type === "drop") event.payload.paths.forEach(handler);
    }),
    readDroppedPath: path => invoke<string>("read_path", { path }),
    readBrowserDroppedFile: async () => null,
    exportPdf: (defaultName, bytes) => invoke<boolean>("export_pdf", { defaultName, bytes: Array.from(bytes) }),
    runVisioTool: args => invoke("run_visio_tool", { args })
  };
}

function browserTestPorts(): HostPorts {
  let clipboard = "";
  return {
    candidate: () => "browser-test", platform: async () => navigator.platform, markReady: async () => {},
    openProject: async () => null, saveProject: async () => false,
    readPath: async () => { throw new Error("not available"); }, writePath: async () => { throw new Error("not available"); },
    writeStructured: async text => { clipboard = text; }, readStructured: async () => clipboard,
    subscribe: async () => () => {}, readDroppedPath: async () => { throw new Error("not available"); }, readBrowserDroppedFile: async file => file.text(),
    exportPdf: async () => false,
    runVisioTool: async () => ({ exitCode: 127, stdout: "", stderr: "not available" })
  };
}
export const host: HostPorts = window.electroHost ?? (window.__TAURI_INTERNALS__ ? tauriPorts() : browserTestPorts());
