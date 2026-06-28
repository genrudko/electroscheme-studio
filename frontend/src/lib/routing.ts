/**
 * Connection routing for ElectroScheme Studio.
 *
 * Implements orthogonal (Manhattan) polyline generation per
 * ГОСТ 2.702-2011 § 5.3 ("линии связи должны иметь минимальное
 * количество изломов"). Provides:
 *
 *   * ``buildPolyline``    — build the full point list for a connection
 *   * ``findJunctions``    — collect points where >= 2 segments share coordinates
 *   * ``distanceToSegment``— for snap-to-line logic
 *   * ``snapToBusbar``     — project a point onto a busbar segment
 */

export interface Point {
  x: number
  y: number
}

export type RouteMode = 'straight' | 'ortho' | 'manual'
export type ConnectionKind = 'wire' | 'control' | 'bus' | 'polyline'

export interface ConnectionLike {
  id?: string
  from: string
  to: string
  points?: Point[]
  route_mode?: RouteMode
  kind?: ConnectionKind
}

/** Resolve a terminal reference like ``"sym_id.term_id"`` to a sheet point. */
export function resolveTerminalRef(
  ref: string,
  terminalsByRef: Map<string, Point>,
): Point | null {
  return terminalsByRef.get(ref) ?? null
}

/**
 * Build the full polyline point list for a connection.
 *
 * Order is: ``from → points → to``.
 *
 * Routing strategy:
 *   * ``manual``  — use ``points`` verbatim
 *   * ``ortho``   — L-shape or Z-shape between axis-aligned terminals;
 *                   respects existing ``points`` (treated as fixed bends)
 *   * ``straight``— direct line (used as fallback)
 */
export function buildPolyline(
  conn: ConnectionLike,
  terminalsByRef: Map<string, Point>,
): Point[] {
  const a = resolveTerminalRef(conn.from, terminalsByRef)
  const b = resolveTerminalRef(conn.to, terminalsByRef)
  if (!a || !b) return []

  const waypoints: Point[] = (conn.points ?? []).map((p) => ({ x: p.x, y: p.y }))
  const mode: RouteMode = conn.route_mode ?? 'straight'

  if (mode === 'manual') {
    return [a, ...waypoints, b]
  }

  if (mode === 'straight') {
    return waypoints.length > 0 ? [a, ...waypoints, b] : [a, b]
  }

  // ortho: L-shape with one bend. Choose bend at (x2,y1) or (x1,y2)
  // depending on which yields a shorter horizontal segment, so the
  // visible "long axis" matches the dominant separation.
  if (waypoints.length > 0) {
    return [a, ...waypoints, b]
  }

  // axis-aligned: just one segment
  if (a.x === b.x || a.y === b.y) {
    return [a, b]
  }

  const dx = Math.abs(b.x - a.x)
  const dy = Math.abs(b.y - a.y)
  if (dx >= dy) {
    // horizontal first
    return [a, { x: b.x, y: a.y }, b]
  }
  // vertical first
  return [a, { x: a.x, y: b.y }, b]
}

/**
 * Compute every point in the scheme where >= 2 segments share coordinates.
 *
 * Each junction is reported once. The set includes:
 *   * connection endpoints (from / to) whose coordinate equals another
 *     endpoint or waypoint in the same scheme
 *   * waypoints whose coordinate equals another waypoint or endpoint
 *
 * Returns ``Map<string, { point, refs: string[] }>`` keyed by ``"x,y"``.
 */
export function findJunctions(
  connections: ConnectionLike[],
  terminalsByRef: Map<string, Point>,
  tolerance: number = 0.5,
): Map<string, { point: Point; refs: string[] }> {
  const bucket = new Map<string, { point: Point; refs: string[] }>()
  const add = (p: Point, ref: string) => {
    const key = `${Math.round(p.x / tolerance)}_${Math.round(p.y / tolerance)}`
    const existing = bucket.get(key)
    if (existing) {
      if (!existing.refs.includes(ref)) existing.refs.push(ref)
    } else {
      bucket.set(key, { point: { x: p.x, y: p.y }, refs: [ref] })
    }
  }

  for (const c of connections) {
    const a = resolveTerminalRef(c.from, terminalsByRef)
    if (a) add(a, c.from)
    const b = resolveTerminalRef(c.to, terminalsByRef)
    if (b) add(b, c.to)
    for (const w of c.points ?? []) add(w, `waypoint@${c.id}`)
  }

  // keep only buckets with >= 2 unique refs
  const out = new Map<string, { point: Point; refs: string[] }>()
  for (const [k, v] of bucket) {
    if (v.refs.length >= 2) out.set(k, v)
  }
  return out
}

/** Squared distance from point ``p`` to segment ``a→b``. */
export function distanceSquaredToSegment(p: Point, a: Point, b: Point): number {
  const dx = b.x - a.x
  const dy = b.y - a.y
  const len2 = dx * dx + dy * dy
  if (len2 === 0) {
    const ex = p.x - a.x
    const ey = p.y - a.y
    return ex * ex + ey * ey
  }
  let t = ((p.x - a.x) * dx + (p.y - a.y) * dy) / len2
  t = Math.max(0, Math.min(1, t))
  const cx = a.x + t * dx
  const cy = a.y + t * dy
  const ex = p.x - cx
  const ey = p.y - cy
  return ex * ex + ey * ey
}

/**
 * Snap a point onto a horizontal or vertical line segment if within
 * ``tolerance``. Returns the snapped point or the original point.
 */
export function snapToSegment(
  p: Point,
  a: Point,
  b: Point,
  tolerance: number,
): Point {
  const d2 = distanceSquaredToSegment(p, a, b)
  if (d2 > tolerance * tolerance) return p
  const dx = b.x - a.x
  const dy = b.y - a.y
  const len2 = dx * dx + dy * dy
  if (len2 === 0) return { x: a.x, y: a.y }
  let t = ((p.x - a.x) * dx + (p.y - a.y) * dy) / len2
  t = Math.max(0, Math.min(1, t))
  return { x: a.x + t * dx, y: a.y + t * dy }
}

/**
 * Try to snap a point onto any of the busbar segments in ``busbars``.
 *
 * ``busbars`` are horizontal segments ``{ a, b }``.
 *
 * Returns the snapped point if any busbar is within ``tolerance`` mm,
 * otherwise the original point. Also returns the matched busbar id
 * (or null) so the caller can mark the connection as joining it.
 */
export function snapToBusbar(
  p: Point,
  busbars: Array<{ id: string; a: Point; b: Point }>,
  tolerance: number,
): { point: Point; busbarId: string | null } {
  let best: { point: Point; busbarId: string | null; d2: number } | null = null
  for (const bb of busbars) {
    const snapped = snapToSegment(p, bb.a, bb.b, tolerance)
    const ex = snapped.x - p.x
    const ey = snapped.y - p.y
    const d2 = ex * ex + ey * ey
    if (d2 <= tolerance * tolerance) {
      if (!best || d2 < best.d2) {
        best = { point: snapped, busbarId: bb.id, d2 }
      }
    }
  }
  return best ? { point: best.point, busbarId: best.busbarId } : { point: p, busbarId: null }
}

/** Convert polyline points into an SVG ``points`` attribute. */
export function pointsToSvgPath(pts: Point[]): string {
  if (pts.length === 0) return ''
  const head = `M ${pts[0].x} ${pts[0].y}`
  const rest = pts.slice(1).map((p) => `L ${p.x} ${p.y}`).join(' ')
  return `${head} ${rest}`.trim()
}

/** Extract horizontal busbar segments from SchemeSymbol list. */
export function extractBusbars(
  symbols: Array<{ id: string; type: string; x: number; y: number; width?: number }>,
): Array<{ id: string; a: Point; b: Point }> {
  const out: Array<{ id: string; a: Point; b: Point }> = []
  for (const s of symbols) {
    if (s.type !== 'busbar') continue
    const w = s.width ?? 0
    if (w <= 0) continue
    out.push({
      id: s.id,
      a: { x: s.x, y: s.y },
      b: { x: s.x + w, y: s.y },
    })
  }
  return out
}
