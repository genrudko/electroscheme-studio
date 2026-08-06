export interface AutomationContext {
  resultPath: string;
  canonicalFixturePath: string;
  vsdxFixturePath: string;
  vssxFixturePath: string;
  roundTripPath: string;
  pdfPath: string;
  generatedVsdxPath: string;
}

export interface FileDialogPort {
  openProject(): Promise<string | null>;
  saveProject(defaultName: string, content: string): Promise<boolean>;
}

export interface ProjectFileStore {
  readPath(path: string): Promise<string>;
  writePath(path: string, content: string): Promise<void>;
  writeBytesPath(path: string, bytes: Uint8Array): Promise<void>;
}

export interface ClipboardPort {
  writeStructured(text: string): Promise<void>;
  readStructured(): Promise<string>;
}

export interface NativeDragDropPort {
  subscribe(handler: (path: string) => void): Promise<() => void>;
  readDroppedPath(path: string): Promise<string>;
  readBrowserDroppedFile(file: File): Promise<string | null>;
}

export interface PrintPort {
  exportPdf(defaultName: string, bytes: Uint8Array): Promise<boolean>;
}

export interface ProcessToolPort {
  runVisioTool(args: string[]): Promise<{ exitCode: number; stdout: string; stderr: string }>;
}

export interface SystemInfoPort {
  candidate(): "electron" | "tauri" | "browser-test";
  platform(): Promise<string>;
  automationContext(): Promise<AutomationContext | null>;
  markReady(): Promise<void>;
}

export interface HostPorts extends FileDialogPort, ProjectFileStore, ClipboardPort, NativeDragDropPort, PrintPort, ProcessToolPort, SystemInfoPort {}
