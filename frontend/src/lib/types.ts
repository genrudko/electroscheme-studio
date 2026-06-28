export interface Terminal {
  id: string
  x: number
  y: number
}

export interface SchemeSymbol {
  id: string
  type: string
  label: string
  x: number
  y: number
  width?: number
  height?: number
  rotation?: number
  terminals: Terminal[]
  properties?: Record<string, unknown>
}

export interface Connection {
  id: string
  from: string
  to: string
}

export interface Sheet {
  id: string
  name: string
  format: string
  orientation: string
  width_mm: number
  height_mm: number
}

export interface ProjectMeta {
  name: string
  code: string
}

export interface Project {
  version: string
  project: ProjectMeta
  sheets: Sheet[]
  symbols: SchemeSymbol[]
  connections: Connection[]
}
