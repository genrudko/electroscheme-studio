import type { CanvasSettings } from './canvasSettings'
import type { VoltageClassId } from './voltageClasses'

export type EditorObjectKind =
  | 'busbar'
  | 'text'
  | 'primitive'
  | 'image'
  | 'guide'
  | 'connector'
  | 'symbol'

export type EditorPoint = {
  x: number
  y: number
}

export type EditorLayer = {
  id: string
  name: string
  visible: boolean
  locked: boolean
  printable: boolean
  color?: string
  order: number
}

export type EditorObjectBase = {
  id: string
  kind: EditorObjectKind
  layerId: string
  name: string
  position: EditorPoint
  rotationDeg: number
  locked: boolean
  selected?: boolean
  data?: Record<string, unknown>
}

export type BusbarEditorObject = EditorObjectBase & {
  kind: 'busbar'
  voltageClassId: VoltageClassId
  voltageKv: number
  width: number
  height: number
  slots: number
  slotSpacing: number
  endSlotOffset: number
  label: string
  labelStart: number
}

export type TextEditorObject = EditorObjectBase & {
  kind: 'text'
  text: string
  fontFamily: string
  fontSize: number
  fill: string
  bold: boolean
  italic: boolean
  underline: boolean
  align: 'left' | 'center' | 'right'
}

export type PrimitiveEditorObject = EditorObjectBase & {
  kind: 'primitive'
  primitiveKind: 'rectangle' | 'ellipse' | 'line' | 'polyline' | 'arc'
  width: number
  height: number
  stroke: string
  fill: string
  strokeWidth: number
}

export type ImageEditorObject = EditorObjectBase & {
  kind: 'image'
  src: string
  width: number
  height: number
  opacity: number
}

export type EditorObject =
  | BusbarEditorObject
  | TextEditorObject
  | PrimitiveEditorObject
  | ImageEditorObject

export type EditorSelectionState = {
  objectIds: string[]
  primaryObjectId: string | null
}

export type EditorDocument = {
  schemaVersion: 1
  id: string
  title: string
  createdAt: string
  modifiedAt: string
  settings: CanvasSettings
  layers: EditorLayer[]
  objects: EditorObject[]
  selection: EditorSelectionState
}

export function createDefaultLayers(): EditorLayer[] {
  return [
    { id: 'layer_scheme', name: 'Схема', visible: true, locked: false, printable: true, color: '#2563eb', order: 10 },
    { id: 'layer_text', name: 'Подписи', visible: true, locked: false, printable: true, color: '#111827', order: 20 },
    { id: 'layer_guides', name: 'Направляющие', visible: true, locked: false, printable: false, color: '#0ea5e9', order: 30 },
    { id: 'layer_images', name: 'Изображения', visible: true, locked: false, printable: true, color: '#64748b', order: 40 },
  ]
}

export function createEmptyEditorDocument(settings: CanvasSettings): EditorDocument {
  const now = new Date().toISOString()
  return {
    schemaVersion: 1,
    id: `document_${Date.now()}`,
    title: 'Новая схема',
    createdAt: now,
    modifiedAt: now,
    settings,
    layers: createDefaultLayers(),
    objects: [],
    selection: {
      objectIds: [],
      primaryObjectId: null,
    },
  }
}