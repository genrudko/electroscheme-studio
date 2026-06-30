type RulerOrientation = 'horizontal' | 'vertical'

type RulerLabel = {
  value: number
  pos: number
}

const RULER_SELECTOR = [
  '.ruler',
  '.ruler-horizontal',
  '.ruler-vertical',
  '.canvas-ruler',
  '.ruler-layer',
].join(',')

const INTERMEDIATE_LABEL_CLASS = 'ruler-mm-intermediate-label'
const UNIT_BADGE_CLASS = 'ruler-mm-unit-badge'
const INSTALLED_KEY = '__electroschemeRulerMmOverlayInstalled'

declare global {
  interface Window {
    [INSTALLED_KEY]?: boolean
  }
}

function parseNumericLabel(text: string | null | undefined): number | null {
  if (!text) return null
  const compact = text.replace(',', '.').replace(/\s+/g, ' ').trim()
  const match = compact.match(/^-?\d+(?:\.\d+)?$/) ?? compact.match(/^-?\d+(?:\.\d+)?\s*мм$/i)
  if (!match) return null
  const numeric = Number.parseFloat(match[0].replace(/мм/i, '').trim())
  return Number.isFinite(numeric) ? numeric : null
}

function getOrientation(ruler: Element): RulerOrientation {
  const className = String((ruler as HTMLElement | SVGElement).className)
  if (/vertical/i.test(className)) return 'vertical'
  if (/horizontal/i.test(className)) return 'horizontal'

  const rect = ruler.getBoundingClientRect()
  return rect.width >= rect.height ? 'horizontal' : 'vertical'
}

function isOwnOverlay(element: Element): boolean {
  return element.classList.contains(INTERMEDIATE_LABEL_CLASS) || element.classList.contains(UNIT_BADGE_CLASS)
}

function collectLabels(ruler: Element, orientation: RulerOrientation): RulerLabel[] {
  const rect = ruler.getBoundingClientRect()
  const labels: RulerLabel[] = []

  const candidates = Array.from(ruler.querySelectorAll('*'))
  for (const candidate of candidates) {
    if (isOwnOverlay(candidate)) continue

    const value = parseNumericLabel(candidate.textContent)
    if (value === null) continue

    const candidateRect = candidate.getBoundingClientRect()
    if (candidateRect.width <= 0 || candidateRect.height <= 0) continue

    const center = orientation === 'horizontal'
      ? candidateRect.left + candidateRect.width / 2 - rect.left
      : candidateRect.top + candidateRect.height / 2 - rect.top

    const visibleInside = orientation === 'horizontal'
      ? center >= -2 && center <= rect.width + 2
      : center >= -2 && center <= rect.height + 2

    if (!visibleInside) continue

    labels.push({ value, pos: center })
  }

  labels.sort((a, b) => a.pos - b.pos)

  const deduped: RulerLabel[] = []
  for (const label of labels) {
    const previous = deduped[deduped.length - 1]
    if (previous && Math.abs(previous.pos - label.pos) < 8 && Math.abs(previous.value - label.value) < 0.001) {
      continue
    }
    deduped.push(label)
  }

  return deduped
}

function formatMm(value: number): string {
  const rounded = Math.round(value * 10) / 10
  if (Math.abs(rounded - Math.round(rounded)) < 0.001) return String(Math.round(rounded))
  return rounded.toFixed(1).replace('.', ',')
}

function removeOverlays(ruler: Element): void {
  ruler.querySelectorAll(`.${INTERMEDIATE_LABEL_CLASS}, .${UNIT_BADGE_CLASS}`).forEach((element) => element.remove())
}

function ensureHtmlRulerPosition(ruler: Element): HTMLElement | null {
  if (!(ruler instanceof HTMLElement)) return null
  const style = window.getComputedStyle(ruler)
  if (style.position === 'static') ruler.style.position = 'relative'
  return ruler
}

function addHtmlLabel(ruler: HTMLElement, orientation: RulerOrientation, pos: number, value: number): void {
  const label = document.createElement('span')
  label.className = INTERMEDIATE_LABEL_CLASS
  label.textContent = formatMm(value)
  label.title = `${formatMm(value)} мм`

  if (orientation === 'horizontal') {
    label.style.left = `${pos}px`
    label.style.top = '1px'
  } else {
    label.style.top = `${pos}px`
    label.style.right = '2px'
  }

  ruler.appendChild(label)
}

function addHtmlUnitBadge(ruler: HTMLElement, orientation: RulerOrientation): void {
  const badge = document.createElement('span')
  badge.className = UNIT_BADGE_CLASS
  badge.textContent = 'мм'
  badge.title = 'Линейка в миллиметрах'
  if (orientation === 'horizontal') {
    badge.style.right = '4px'
    badge.style.top = '1px'
  } else {
    badge.style.left = '2px'
    badge.style.top = '2px'
  }
  ruler.appendChild(badge)
}

function chooseSubdivisions(pixelGap: number): number {
  if (pixelGap >= 360) return 5
  if (pixelGap >= 260) return 4
  if (pixelGap >= 170) return 3
  if (pixelGap >= 92) return 2
  return 0
}

function renderIntermediateLabels(ruler: Element): void {
  const orientation = getOrientation(ruler)
  const htmlRuler = ensureHtmlRulerPosition(ruler)
  if (!htmlRuler) return

  const labels = collectLabels(ruler, orientation)
  removeOverlays(ruler)

  if (labels.length < 2) {
    addHtmlUnitBadge(htmlRuler, orientation)
    return
  }

  addHtmlUnitBadge(htmlRuler, orientation)

  for (let index = 0; index < labels.length - 1; index += 1) {
    const start = labels[index]
    const end = labels[index + 1]
    const pixelGap = end.pos - start.pos
    const valueGap = end.value - start.value
    if (pixelGap <= 0 || Math.abs(valueGap) < 0.001) continue

    const subdivisions = chooseSubdivisions(pixelGap)
    if (subdivisions <= 0) continue

    for (let step = 1; step <= subdivisions; step += 1) {
      const ratio = step / (subdivisions + 1)
      const pos = start.pos + pixelGap * ratio
      const value = start.value + valueGap * ratio
      addHtmlLabel(htmlRuler, orientation, pos, value)
    }
  }
}

let scheduled = false

function scheduleRulerRefresh(): void {
  if (scheduled) return
  scheduled = true
  window.requestAnimationFrame(() => {
    scheduled = false
    const rulers = Array.from(document.querySelectorAll(RULER_SELECTOR))
      .filter((element) => element instanceof HTMLElement)
      .filter((element) => element.getBoundingClientRect().width > 0 && element.getBoundingClientRect().height > 0)

    for (const ruler of rulers) {
      renderIntermediateLabels(ruler)
    }
  })
}

export function installRulerMmIntermediateLabels(): void {
  if (typeof window === 'undefined' || typeof document === 'undefined') return
  if (window[INSTALLED_KEY]) return
  window[INSTALLED_KEY] = true

  const observer = new MutationObserver(() => scheduleRulerRefresh())

  const start = () => {
    scheduleRulerRefresh()
    if (document.body) {
      observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class', 'transform', 'viewBox'],
      })
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true })
  } else {
    start()
  }

  window.addEventListener('resize', scheduleRulerRefresh, { passive: true })
  window.addEventListener('scroll', scheduleRulerRefresh, { passive: true, capture: true })
  window.setInterval(scheduleRulerRefresh, 750)
}

installRulerMmIntermediateLabels()
