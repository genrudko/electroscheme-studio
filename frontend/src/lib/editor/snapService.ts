export type Point = {
  x: number
  y: number
}

export type SnapKind =
  | 'grid'
  | 'slot'
  | 'terminal'
  | 'object'
  | 'guide'
  | 'free'

export type SnapResult = Point & {
  kind: SnapKind
  label: string
}

export type SnapCandidate = Point & {
  kind: Exclude<SnapKind, 'grid' | 'free'>
  label: string
}

export type SnapOptions = {
  gridSize: number
  enabled: boolean
  tolerance: number
  candidates?: SnapCandidate[]
}

function distance(a: Point, b: Point): number {
  return Math.hypot(a.x - b.x, a.y - b.y)
}

export function snapPoint(point: Point, options: SnapOptions): SnapResult {
  if (!options.enabled) {
    return { ...point, kind: 'free', label: 'Free' }
  }

  let best: SnapResult | null = null
  let bestDistance = Number.POSITIVE_INFINITY

  for (const candidate of options.candidates ?? []) {
    const candidateDistance = distance(point, candidate)
    if (candidateDistance < bestDistance && candidateDistance <= options.tolerance) {
      bestDistance = candidateDistance
      best = {
        x: candidate.x,
        y: candidate.y,
        kind: candidate.kind,
        label: candidate.label,
      }
    }
  }

  const gridX = Math.round(point.x / options.gridSize) * options.gridSize
  const gridY = Math.round(point.y / options.gridSize) * options.gridSize
  const gridPoint = { x: gridX, y: gridY }
  const gridDistance = distance(point, gridPoint)

  if (gridDistance < bestDistance && gridDistance <= options.tolerance) {
    best = {
      x: gridX,
      y: gridY,
      kind: 'grid',
      label: `Grid ${options.gridSize}`,
    }
  }

  return best ?? { ...point, kind: 'free', label: 'Free' }
}

export function formatPoint(point: Point): string {
  return `X=${point.x.toFixed(1)} Y=${point.y.toFixed(1)}`
}