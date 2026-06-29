export type EditorClipboardPayload = { schemaVersion: 1; source: 'electroscheme-studio'; createdAt: string; objects: unknown[]; basePoint?: { x: number; y: number } }
export function createEditorClipboardPayload(objects: unknown[], basePoint?: { x: number; y: number }): EditorClipboardPayload {
  return { schemaVersion: 1, source: 'electroscheme-studio', createdAt: new Date().toISOString(), objects: structuredClone(objects), basePoint }
}
