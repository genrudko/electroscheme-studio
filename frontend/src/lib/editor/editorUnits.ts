export const EDITOR_LENGTH_UNIT = 'мм'
export const BUSBAR_CONNECTION_LIMIT_MAX = 100
export const BUSBAR_CELL_STEP_UNIT = 'мм'
export const VIEW_GRID_STEP_UNIT = 'мм'
export const VIEW_SNAP_TOLERANCE_UNIT = 'мм'

export function mmLabel(label: string): string {
  return label.includes('мм') ? label : `${label} (${EDITOR_LENGTH_UNIT})`
}
