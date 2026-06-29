import type { CanvasSettings } from './canvasSettings'
export type EditorLayer = { id: string; name: string; visible: boolean; locked: boolean; printable: boolean; color?: string; order: number }
export type EditorDocument = { schemaVersion: 1; id: string; title: string; settings: CanvasSettings; layers: EditorLayer[] }
export function createDefaultLayers(): EditorLayer[] {
  return [
    { id: 'layer_scheme', name: 'Схема', visible: true, locked: false, printable: true, color: '#2563eb', order: 10 },
    { id: 'layer_text', name: 'Подписи', visible: true, locked: false, printable: true, color: '#111827', order: 20 },
    { id: 'layer_guides', name: 'Направляющие', visible: true, locked: false, printable: false, color: '#0ea5e9', order: 30 },
  ]
}
export function createEmptyEditorDocument(settings: CanvasSettings): EditorDocument {
  return { schemaVersion: 1, id: `document_${Date.now()}`, title: 'Новая схема', settings, layers: createDefaultLayers() }
}
