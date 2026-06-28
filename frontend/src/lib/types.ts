export interface Terminal {
  id: string
  x: number
  y: number
}

export interface Waypoint {
  x: number
  y: number
}

/** Routing style applied when no explicit ``points`` are set. */
export type RouteMode = 'straight' | 'ortho' | 'manual'

/** Visual class of a connection. Controls line width and stroke style. */
export type ConnectionKind = 'wire' | 'control' | 'bus' | 'polyline'

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
  current_state?: string
  properties?: Record<string, unknown>
}

export interface Connection {
  id: string
  /** Terminal reference ``"<symbol_id>.<terminal_id>"``. */
  from: string
  /** Terminal reference ``"<symbol_id>.<terminal_id>"``. */
  to: string
  /** Optional intermediate bend points (sheet coordinates, mm). */
  points?: Waypoint[]
  /** Routing style when ``points`` is empty. */
  route_mode?: RouteMode
  /** Visual class of the line. */
  kind?: ConnectionKind
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

export interface GostReference {
  id: string
  title: string
  description: string
  status: string
}

export interface SymbolCategory {
  id: string
  name: string
  gost: string
}

export interface SymbolTerminalDef {
  id: string
  rx: number
  ry: number
}

export interface SymbolState {
  id: string
  name: string
  alternate_svg: string | null
}

export interface SymbolDefinition {
  id: string
  type: string
  name: string
  category: string
  gost: string
  gost_ref: string
  viewBox: string
  default_width: number
  default_height: number
  terminals: SymbolTerminalDef[]
  default_properties: Record<string, string>
  svg: string
  interactive: boolean
  default_state: string
  current_state: string
  states: SymbolState[]
  // GOST compliance metadata
  letter_designation?: string
  module_width?: number
  module_height?: number
  line_width_main?: number
  line_width_contour?: number
}

export interface SymbolLibrary {
  version: string
  description: string
  gost_references: GostReference[]
  categories: SymbolCategory[]
  symbols: SymbolDefinition[]
}
