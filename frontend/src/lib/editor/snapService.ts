export type Point = { x: number; y: number }
export type SnapKind = 'grid' | 'slot' | 'terminal' | 'object' | 'guide' | 'origin' | 'free'
export type SnapResult = Point & { kind: SnapKind; label: string }
export type SnapCandidate = Point & { kind: Exclude<SnapKind, 'grid' | 'free'>; label: string }
export type SnapOptions = { gridSize: number; enabled: boolean; snapGrid?: boolean; tolerance: number; candidates?: SnapCandidate[] }

export function snapPoint(point: Point, options: SnapOptions): SnapResult {
  if (!options.enabled) return { ...point, kind: 'free', label: 'Свободно' }
  let best: SnapResult | null = null
  let bestDistance = Number.POSITIVE_INFINITY
  for (const candidate of options.candidates ?? []) {
    const distance = Math.hypot(point.x - candidate.x, point.y - candidate.y)
    if (distance < bestDistance && distance <= options.tolerance) {
      best = { x: candidate.x, y: candidate.y, kind: candidate.kind, label: candidate.label }
      bestDistance = distance
    }
  }
  if (options.snapGrid !== false) {
    const x = Math.round(point.x / options.gridSize) * options.gridSize
    const y = Math.round(point.y / options.gridSize) * options.gridSize
    const distance = Math.hypot(point.x - x, point.y - y)
    if (distance < bestDistance && distance <= options.tolerance) best = { x, y, kind: 'grid', label: `Сетка ${options.gridSize}` }
  }
  return best ?? { ...point, kind: 'free', label: 'Свободно' }
}

export function rectsIntersect(a: { x: number; y: number; width: number; height: number }, b: { x: number; y: number; width: number; height: number }): boolean {
  return a.x <= b.x + b.width && a.x + a.width >= b.x && a.y <= b.y + b.height && a.y + a.height >= b.y
}
