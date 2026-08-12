import type { CanonicalProject, DiagramObject, StableId } from "./model.ts";

export interface StructuredClipboard {
  schema: "electroscheme-spike-clipboard/1";
  objects: DiagramObject[];
}

function plainDiagramObject(object: DiagramObject): DiagramObject {
  // Vue exposes editor objects through reactive proxies. structuredClone rejects
  // Proxy objects, while the clipboard protocol is deliberately JSON-only.
  return JSON.parse(JSON.stringify(object)) as DiagramObject;
}

export function encodeClipboard(project: CanonicalProject, objectIds: StableId[]): string {
  const selected = new Set(objectIds);
  const payload: StructuredClipboard = {
    schema: "electroscheme-spike-clipboard/1",
    objects: project.objects.filter(object => selected.has(object.id)).map(plainDiagramObject)
  };
  return JSON.stringify(payload);
}

export function decodeClipboard(text: string): StructuredClipboard {
  const parsed = JSON.parse(text) as StructuredClipboard;
  if (parsed.schema !== "electroscheme-spike-clipboard/1" || !Array.isArray(parsed.objects)) {
    throw new Error("unsupported clipboard payload");
  }
  for (const object of parsed.objects) {
    if (!object || typeof object !== "object" || typeof object.id !== "string" || typeof object.kind !== "string") {
      throw new Error("invalid clipboard object");
    }
  }
  return parsed;
}
