import type { CanonicalProject, DiagramObject, StableId } from "./model.ts";
export interface StructuredClipboard { schema: "electroscheme-spike-clipboard/1"; objects: DiagramObject[]; }
export function encodeClipboard(project: CanonicalProject, objectIds: StableId[]): string {
  const selected = new Set(objectIds);
  const payload: StructuredClipboard = { schema: "electroscheme-spike-clipboard/1", objects: project.objects.filter(o => selected.has(o.id)).map(o => structuredClone(o)) };
  return JSON.stringify(payload);
}
export function decodeClipboard(text: string): StructuredClipboard {
  const parsed = JSON.parse(text) as StructuredClipboard;
  if (parsed.schema !== "electroscheme-spike-clipboard/1" || !Array.isArray(parsed.objects)) throw new Error("unsupported clipboard payload");
  return parsed;
}
