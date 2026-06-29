export type PaletteDragPayloadStatus = 'available' | 'planned'

export type PaletteDragPayload = {
  id: string
  status?: PaletteDragPayloadStatus
  command?: string
  title: string
  categoryId?: string
  libraryPageName?: string
  semanticCategoryId?: string
  vsdxMasterId?: string
  widthMm?: number
  heightMm?: number
  connectionCount?: number
}

export const PALETTE_SHAPE_MIME = 'application/x-electroscheme-shape-catalog-item'

let currentPaletteDragPayload: PaletteDragPayload | null = null

export function setPaletteDragPayload(payload: PaletteDragPayload): void {
  currentPaletteDragPayload = payload
}

export function getPaletteDragPayload(): PaletteDragPayload | null {
  return currentPaletteDragPayload
}

export function clearPaletteDragPayload(): void {
  currentPaletteDragPayload = null
}

export function serializePaletteDragPayload(payload: PaletteDragPayload): string {
  return JSON.stringify(payload)
}

export function parsePaletteDragPayload(raw: string | null | undefined): PaletteDragPayload | null {
  if (!raw) return null
  try {
    const parsed = JSON.parse(raw) as PaletteDragPayload
    if (!parsed || typeof parsed.title !== 'string' || parsed.title.trim().length === 0) return null
    return parsed
  } catch {
    return null
  }
}

export function readPaletteDragPayloadFromEvent(event: DragEvent): PaletteDragPayload | null {
  const nativePayload = parsePaletteDragPayload(event.dataTransfer?.getData(PALETTE_SHAPE_MIME))
  return nativePayload ?? currentPaletteDragPayload
}


export const PALETTE_POINTER_DROP_EVENT = 'electroscheme:palette-pointer-drop'

export type PalettePointerDropDetail = {
  clientX: number
  clientY: number
  payload: PaletteDragPayload
}
