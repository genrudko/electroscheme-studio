import type { DisplayProfileId } from './schemaStyleProfile'

export type IsoPageFormat = 'A4' | 'A3' | 'A2' | 'A1' | 'A0'
export type PageOrientation = 'portrait' | 'landscape'

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
  originVisible: boolean
  pageVisible: boolean
  pageFormat: IsoPageFormat
  pageOrientation: PageOrientation
  displayProfileId: DisplayProfileId
  modularGridStepMm: number
  ugoLineWidthMm: number
  electricalConnectionLineWidthMm: number
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
  originVisible: true,
  pageVisible: true,
  pageFormat: 'A3',
  pageOrientation: 'landscape',
  displayProfileId: 'gost_r_56303_2014',
  modularGridStepMm: 2.5,
  ugoLineWidthMm: 0.4,
  electricalConnectionLineWidthMm: 0.4,
}

export const isoPageSizes: Record<IsoPageFormat, { width: number; height: number }> = {
  A4: { width: 297, height: 210 },
  A3: { width: 420, height: 297 },
  A2: { width: 594, height: 420 },
  A1: { width: 841, height: 594 },
  A0: { width: 1189, height: 841 },
}

export function normalizeCanvasSettings(settings: CanvasSettings): CanvasSettings {
  return {
    ...settings,
    zoom: Math.min(Math.max(settings.zoom, 0.20), 6),
    gridStep: Math.min(Math.max(settings.gridStep, 2), 100),
    snapTolerance: Math.min(Math.max(settings.snapTolerance, 1), 50),
    displayProfileId: settings.displayProfileId ?? 'gost_r_56303_2014',
    modularGridStepMm: Math.min(Math.max(settings.modularGridStepMm ?? 2.5, 0.5), 20),
    ugoLineWidthMm: Math.min(Math.max(settings.ugoLineWidthMm ?? 0.4, 0.2), 1.0),
    electricalConnectionLineWidthMm: Math.min(Math.max(settings.electricalConnectionLineWidthMm ?? 0.4, 0.2), 1.0),
  }
}