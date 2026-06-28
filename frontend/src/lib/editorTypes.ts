export type ToolType =
  | 'select'
  | 'line'
  | 'rect'
  | 'circle'
  | 'ellipse'
  | 'arc'
  | 'text'
  | 'path'
  | 'polyline'
  | 'group'
  | 'pan'

export interface EditorElement {
  id: string
  type: string
  stroke: string
  fill: string
  strokeWidth: number
  opacity: number
  visible: boolean
  locked: boolean
  x: number
  y: number
  rotation: number
  data: Record<string, unknown>
  children?: EditorElement[]
}

export interface EditorViewport {
  x: number
  y: number
  zoom: number
  width: number
  height: number
}

export interface GridSettings {
  size: number
  snap: boolean
  visible: boolean
}

export interface ArcParams {
  cx: number
  cy: number
  r: number
  startAngle: number
  endAngle: number
}

export interface PathCommand {
  cmd: string
  args: number[]
}
