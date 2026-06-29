import type { ShapeCatalogItem } from './shapeCatalog'

export type PaletteIconMode = 'library' | 'smart' | 'none'

export type PaletteIconOverride = {
  masterId?: string
  titleIncludes?: string
  iconKind: PaletteIconKind
  note: string
}

export type PaletteIconKind =
  | 'library-transformers'
  | 'library-switching'
  | 'library-machines'
  | 'library-lines'
  | 'library-protection'
  | 'library-compensation'
  | 'library-generic'
  | 'exact-circuit-breaker'
  | 'exact-disconnector'
  | 'exact-earthing-switch'
  | 'exact-withdrawable-truck'
  | 'exact-transformer'
  | 'exact-machine-generator'
  | 'exact-machine-motor'
  | 'exact-busbar'
  | 'exact-arrester'
  | 'exact-fuse'
  | 'exact-reactor'
  | 'exact-capacitor'
  | 'exact-short-circuiter'

export const paletteIconOverrides: PaletteIconOverride[] = [
  // Fill this table only after visual review. Do not guess aggressively.
  // Example:
  // { masterId: '42', iconKind: 'exact-transformer', note: 'Verified against source VSDX page' },
]

export function normalizePaletteText(value: string | undefined): string {
  return (value ?? '').toLowerCase().replaceAll('ё', 'е')
}

export function itemSearchText(item: ShapeCatalogItem): string {
  return normalizePaletteText([
    item.title,
    item.categoryId,
    item.libraryPageName,
    item.semanticCategoryId,
    item.sourceRef,
    item.vsdxMasterId,
    item.keywords.join(' '),
  ].filter(Boolean).join(' '))
}

export function getOverrideIconKind(item: ShapeCatalogItem): PaletteIconKind | null {
  const title = normalizePaletteText(item.title)
  for (const override of paletteIconOverrides) {
    if (override.masterId && override.masterId === item.vsdxMasterId) return override.iconKind
    if (override.titleIncludes && title.includes(normalizePaletteText(override.titleIncludes))) return override.iconKind
  }
  return null
}

export function getLibraryIconKind(item: ShapeCatalogItem): PaletteIconKind {
  const text = itemSearchText(item)
  const library = normalizePaletteText(item.libraryPageName)

  if (library.includes('трансформ') || text.includes('автотранс') || text.includes('трансформ')) return 'library-transformers'
  if (library.includes('коммутац') || text.includes('выключ') || text.includes('разъедин') || text.includes('тележ')) return 'library-switching'
  if (library.includes('генератор') || library.includes('двигател') || text.includes('двигател') || text.includes('генератор') || text.includes('дэс')) return 'library-machines'
  if (library.includes('шин') || library.includes('кабел') || library.includes('линии') || text.includes('шина') || text.includes('кабель') || text.includes('линия')) return 'library-lines'
  if (text.includes('опн') || text.includes('разряд') || text.includes('защит')) return 'library-protection'
  if (text.includes('реактор') || text.includes('дгр') || text.includes('конденс')) return 'library-compensation'
  return 'library-generic'
}

export function getSmartIconKind(item: ShapeCatalogItem): PaletteIconKind {
  const override = getOverrideIconKind(item)
  if (override) return override

  const text = itemSearchText(item)

  // High-confidence exact matches only. Everything else falls back to library icon.
  if (text.includes('выкатная тележка')) return 'exact-withdrawable-truck'
  if (text.includes('заземляющий разъединитель')) return 'exact-earthing-switch'
  if (text.includes('короткозамыкатель')) return 'exact-short-circuiter'
  if (text.includes('автоматический выключатель') || text === 'выключатель' || text.includes(' выключатель ')) return 'exact-circuit-breaker'
  if (text.includes('разъединитель') && !text.includes('заземляющий')) return 'exact-disconnector'
  if (text.includes('автотрансформатор') || text.includes('трансформатор')) return 'exact-transformer'
  if (text.includes('генератор') || text.includes('дэс')) return 'exact-machine-generator'
  if (text.includes('двигатель')) return 'exact-machine-motor'
  if (text.includes('шина')) return 'exact-busbar'
  if (text.includes('опн') || text.includes('разрядник')) return 'exact-arrester'
  if (text.includes('предохранитель')) return 'exact-fuse'
  if (text.includes('реактор') || text.includes('дгр')) return 'exact-reactor'
  if (text.includes('конденсатор')) return 'exact-capacitor'

  return getLibraryIconKind(item)
}
