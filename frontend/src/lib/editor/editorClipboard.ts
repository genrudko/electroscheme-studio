import type { EditorObject } from './editorDocument'

export type EditorClipboardPayload = {
  schemaVersion: 1
  source: 'electroscheme-studio'
  createdAt: string
  objects: EditorObject[]
  basePoint?: { x: number; y: number }
}

export function createEditorClipboardPayload(objects: EditorObject[], basePoint?: { x: number; y: number }): EditorClipboardPayload {
  return {
    schemaVersion: 1,
    source: 'electroscheme-studio',
    createdAt: new Date().toISOString(),
    objects: structuredClone(objects),
    basePoint,
  }
}