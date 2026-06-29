import type { EditorCommand } from './interactionModes'
import {
  vsdxLibraryCategories,
  vsdxSymbolDefinitions,
  type VsdxSymbolDefinition,
} from './vsdxSymbolCatalog.generated'

export type ShapeCatalogStatus = 'available' | 'planned'

export type ShapeCatalogItem = {
  id: string
  title: string
  categoryId: string
  command?: EditorCommand
  status: ShapeCatalogStatus
  keywords: string[]
  preview: string
  svgPreview?: string
  sourceRef?: string
  widthMm?: number
  heightMm?: number
  connectionCount?: number
  propertyNames?: string[]
  dataFieldIds?: string[]
  vsdxMasterId?: string
  libraryPageName?: string
  semanticCategoryId?: string
}

export type ShapeCatalogCategory = {
  id: string
  title: string
  description: string
  sourceRef?: string
  order: number
}

const coreCategories: ShapeCatalogCategory[] = [
  { id: 'busbars_lines_grounding', title: 'Линии / шины / заземление', description: 'Рабочие линии, шины, заземление и связи редактора', sourceRef: 'editor-core', order: -30 },
  { id: 'primitives', title: 'Графика', description: 'Базовые графические примитивы', sourceRef: 'editor-core', order: -20 },
  { id: 'text', title: 'Текст и размеры', description: 'Надписи, подписи, размеры', sourceRef: 'editor-core', order: -10 },
]

export const shapeCatalogCategories: ShapeCatalogCategory[] = [
  ...coreCategories,
  ...vsdxLibraryCategories.map((category) => ({
    id: category.id,
    title: category.title,
    description: category.description,
    sourceRef: category.source,
    order: category.order,
  })),
].filter((category, index, all) => all.findIndex((candidate) => candidate.id === category.id) === index)
  .sort((a, b) => a.order - b.order || a.title.localeCompare(b.title, 'ru'))

const availableShapeCatalogItems: ShapeCatalogItem[] = [
  {
    id: 'busbar',
    title: 'Шина',
    categoryId: 'busbars_lines_grounding',
    command: 'create_sample_busbar',
    status: 'available',
    keywords: ['шина', 'секция', 'busbar', 'ошиновка'],
    preview: '▰',
    svgPreview: '<svg viewBox="0 0 64 32" aria-hidden="true"><rect x="7" y="12" width="50" height="8" rx="1.5" fill="#6d0ad6" stroke="#111827" stroke-width="1"/><circle cx="17" cy="16" r="3" fill="#fff" stroke="#111827" stroke-width="1"/><circle cx="32" cy="16" r="3" fill="#fff" stroke="#111827" stroke-width="1"/><circle cx="47" cy="16" r="3" fill="#fff" stroke="#111827" stroke-width="1"/></svg>',
    sourceRef: 'Рабочая параметрическая шина. Цвет класса напряжения по ГОСТ, точки подключения белые.',
  },
  {
    id: 'text',
    title: 'Текст',
    categoryId: 'text',
    command: 'create_text',
    status: 'available',
    keywords: ['текст', 'надпись', 'label'],
    preview: 'A',
    svgPreview: '<svg viewBox="0 0 64 32" aria-hidden="true"><text x="32" y="22" text-anchor="middle" font-size="22" font-family="Arial" font-weight="700" fill="#6d0ad6">A</text></svg>',
  },
  {
    id: 'rectangle',
    title: 'Прямоугольник',
    categoryId: 'primitives',
    command: 'create_rectangle',
    status: 'available',
    keywords: ['прямоугольник', 'rectangle'],
    preview: '▭',
    svgPreview: '<svg viewBox="0 0 64 32" aria-hidden="true"><rect x="14" y="8" width="36" height="18" fill="none" stroke="#6d0ad6" stroke-width="2"/></svg>',
  },
  {
    id: 'ellipse',
    title: 'Эллипс',
    categoryId: 'primitives',
    command: 'create_ellipse',
    status: 'available',
    keywords: ['эллипс', 'окружность', 'circle'],
    preview: '○',
    svgPreview: '<svg viewBox="0 0 64 32" aria-hidden="true"><ellipse cx="32" cy="16" rx="17" ry="9" fill="none" stroke="#6d0ad6" stroke-width="2"/></svg>',
  },
  {
    id: 'primitive_line',
    title: 'Линия',
    categoryId: 'primitives',
    command: 'create_line',
    status: 'available',
    keywords: ['линия', 'отрезок', 'line'],
    preview: '╱',
    svgPreview: '<svg viewBox="0 0 64 32" aria-hidden="true"><path d="M14 25 L50 7" fill="none" stroke="#6d0ad6" stroke-width="2" stroke-linecap="round"/></svg>',
  },
]

function sourceSummary(definition: VsdxSymbolDefinition): string {
  const size = definition.widthMm > 0 && definition.heightMm > 0
    ? `${definition.widthMm} × ${definition.heightMm} мм`
    : 'размер не определён'
  const fields = definition.dataFields.length
    ? `; поля: ${definition.dataFields.map((field) => field.label).slice(0, 4).join(', ')}`
    : ''
  const rawProps = definition.propertyNames.length ? `; ShapeSheet Prop=${definition.propertyNames.length}` : ''
  return `VSDX master ${definition.masterId}; библиотека: ${definition.libraryPageName}; ${size}; ports=${definition.connectionCount}; shapes=${definition.shapeCount}${rawProps}${fields}`
}

function vsdxToShapeCatalogItem(definition: VsdxSymbolDefinition): ShapeCatalogItem {
  return {
    id: definition.id,
    title: definition.title,
    categoryId: definition.libraryPageId,
    status: 'planned',
    keywords: [
      definition.title,
      definition.libraryPageName,
      definition.categoryId,
      `master ${definition.masterId}`,
      'vsdx',
      ...definition.propertyNames,
      ...definition.userCellNames,
      ...definition.dataFields.map((field) => field.label),
    ],
    preview: definition.preview,
    svgPreview: definition.svgPreview,
    sourceRef: sourceSummary(definition),
    widthMm: definition.widthMm,
    heightMm: definition.heightMm,
    connectionCount: definition.connectionCount,
    propertyNames: definition.propertyNames,
    dataFieldIds: definition.dataFields.map((field) => field.id),
    vsdxMasterId: definition.masterId,
    libraryPageName: definition.libraryPageName,
    semanticCategoryId: definition.categoryId,
  }
}

export const vsdxShapeCatalogItems: ShapeCatalogItem[] = vsdxSymbolDefinitions
  .slice()
  .sort((a, b) => a.libraryOrder - b.libraryOrder || a.title.localeCompare(b.title, 'ru'))
  .map(vsdxToShapeCatalogItem)

export const shapeCatalogItems: ShapeCatalogItem[] = [
  ...availableShapeCatalogItems,
  ...vsdxShapeCatalogItems,
]

export function filterShapeCatalog(query: string, categoryId: string | null): ShapeCatalogItem[] {
  const normalized = query.trim().toLowerCase()
  return shapeCatalogItems.filter((item) => {
    const categoryMatch = !categoryId || item.categoryId === categoryId
    if (!categoryMatch) return false
    if (!normalized) return true
    return item.title.toLowerCase().includes(normalized)
      || item.keywords.some((keyword) => keyword.toLowerCase().includes(normalized))
      || item.sourceRef?.toLowerCase().includes(normalized)
      || item.vsdxMasterId?.toLowerCase().includes(normalized)
      || item.libraryPageName?.toLowerCase().includes(normalized)
  })
}