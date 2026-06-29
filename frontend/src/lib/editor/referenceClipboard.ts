import type { Point } from './snapService'

export type TextClipboardItem = {
  kind: 'text'
  text: string
  sourceId: string
  anchor: Point
  center: Point
  rotationDeg: number
  fontSize: number
  role: string
}

export type ReferenceClipboardPayload = {
  mode: 'copy_by_reference_point'
  basePoint: Point
  items: TextClipboardItem[]
}

export function createReferenceClipboard(
  items: TextClipboardItem[],
  basePoint: Point,
): ReferenceClipboardPayload {
  return {
    mode: 'copy_by_reference_point',
    basePoint,
    items,
  }
}

export function placeItemAtReferencePoint(
  item: TextClipboardItem,
  payload: ReferenceClipboardPayload,
  pastePoint: Point,
): TextClipboardItem {
  const offset = {
    x: item.center.x - payload.basePoint.x,
    y: item.center.y - payload.basePoint.y,
  }
  const nextCenter = {
    x: pastePoint.x + offset.x,
    y: pastePoint.y + offset.y,
  }
  const delta = {
    x: nextCenter.x - item.center.x,
    y: nextCenter.y - item.center.y,
  }

  return {
    ...item,
    sourceId: `${item.sourceId}_copy_${Math.round(nextCenter.x)}_${Math.round(nextCenter.y)}`,
    anchor: {
      x: item.anchor.x + delta.x,
      y: item.anchor.y + delta.y,
    },
    center: nextCenter,
  }
}