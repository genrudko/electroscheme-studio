export type CanvasSettings = {
  zoom: number
  gridVisible: boolean
  gridStep: number
  snapEnabled: boolean
  snapTolerance: number
  snapGrid: boolean
  snapSlots: boolean
  snapObjects: boolean
  snapGuides: boolean
  guidesVisible: boolean
  rulersVisible: boolean
}

export const defaultCanvasSettings: CanvasSettings = {
  zoom: 1,
  gridVisible: true,
  gridStep: 12,
  snapEnabled: true,
  snapTolerance: 7,
  snapGrid: true,
  snapSlots: true,
  snapObjects: true,
  snapGuides: true,
  guidesVisible: true,
  rulersVisible: true,
}

export function normalizeCanvasSettings(settings: CanvasSettings): CanvasSettings {
  return {
    ...settings,
    zoom: Math.min(Math.max(settings.zoom, 0.25), 4),
    gridStep: Math.min(Math.max(settings.gridStep, 2), 100),
    snapTolerance: Math.min(Math.max(settings.snapTolerance, 1), 50),
  }
}