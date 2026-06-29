import type { EditorCommand } from './interactionModes'
import { vsdxSymbolDefinitions, type VsdxSymbolDefinition } from './vsdxSymbolCatalog.generated'

export type ShapeCatalogStatus = 'available' | 'planned'

export type ShapeCatalogItem = {
  id: string
  title: string
  categoryId: string
  command?: EditorCommand
  status: ShapeCatalogStatus
  keywords: string[]
  preview: string
  sourceRef?: string
  widthMm?: number
  heightMm?: number
  connectionCount?: number
  propertyNames?: string[]
  dataFieldIds?: string[]
  vsdxMasterId?: string
}

export type ShapeCatalogCategory = {
  id: string
  title: string
  description: string
  sourceRef?: string
}

export const shapeCatalogCategories: ShapeCatalogCategory[] = [
  { id: 'busbars_lines_grounding', title: 'Линии / шины / заземление', description: 'Линии связи, ЛЭП, кабели, шины, ответвления, заземление', sourceRef: 'VSDX + ГОСТ Р 56303-2014' },
  { id: 'switching', title: 'Коммутационные аппараты', description: 'Выключатели, разъединители, тележки, ЗН, отделители', sourceRef: 'VSDX masters' },
  { id: 'transformers', title: 'Трансформаторы', description: 'Силовые трансформаторы, автотрансформаторы, ТН, ТТ; свойства обмоток и соединений', sourceRef: 'VSDX masters + semantic data fields' },
  { id: 'compensation_filters', title: 'Компенсация / фильтры', description: 'Реакторы, ДГР, конденсаторы, фильтры, компенсаторы', sourceRef: 'VSDX masters' },
  { id: 'surge_arresters', title: 'Разрядники / ОПН', description: 'Разрядники, искровые промежутки, ОПН', sourceRef: 'VSDX masters' },
  { id: 'generators_motors', title: 'Генераторы / двигатели', description: 'Генераторы, ДЭС, синхронные и асинхронные двигатели', sourceRef: 'VSDX masters' },
  { id: 'fuses', title: 'Предохранители', description: 'Плавкие, инерционные, пробивные, на тележке', sourceRef: 'VSDX masters' },
  { id: 'vsdx_symbols', title: 'Прочие VSDX-фигуры', description: 'Фигуры из Visio-библиотеки, не попавшие в базовые группы', sourceRef: 'VSDX masters' },
  { id: 'primitives', title: 'Графика', description: 'Базовые графические примитивы' },
  { id: 'text', title: 'Текст и размеры', description: 'Надписи, подписи, размеры' },
  { id: 'images', title: 'Изображения', description: 'Подложки, сканы, растровые вставки' },
]

const coreShapeCatalogItems: ShapeCatalogItem[] = [
  {
    id: 'busbar',
    title: 'Шина',
    categoryId: 'busbars_lines_grounding',
    command: 'create_sample_busbar',
    status: 'available',
    keywords: ['шина', 'секция', 'busbar', 'ошиновка'],
    preview: '▰',
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
  },
  {
    id: 'rectangle',
    title: 'Прямоугольник',
    categoryId: 'primitives',
    command: 'create_rectangle',
    status: 'available',
    keywords: ['прямоугольник', 'rectangle'],
    preview: '▭',
  },
  {
    id: 'ellipse',
    title: 'Эллипс',
    categoryId: 'primitives',
    command: 'create_ellipse',
    status: 'available',
    keywords: ['эллипс', 'окружность', 'circle'],
    preview: '○',
  },
  {
    id: 'primitive_line',
    title: 'Линия',
    categoryId: 'primitives',
    command: 'create_line',
    status: 'available',
    keywords: ['линия', 'отрезок', 'line'],
    preview: '╱',
  },
]

function knownCategory(categoryId: string): string {
  return shapeCatalogCategories.some((category) => category.id === categoryId)
    ? categoryId
    : 'vsdx_symbols'
}

function sourceSummary(definition: VsdxSymbolDefinition): string {
  const size = definition.widthMm && definition.heightMm
    ? `${definition.widthMm} × ${definition.heightMm} мм`
    : 'размер не определён'
  const fields = definition.dataFields.length
    ? `; поля: ${definition.dataFields.map((field) => field.label).slice(0, 4).join(', ')}`
    : ''
  const rawProps = definition.propertyNames.length ? `; ShapeSheet Prop=${definition.propertyNames.length}` : ''
  return `VSDX master ${definition.masterId}: ${size}; ports=${definition.connectionCount}; shapes=${definition.shapeCount}${rawProps}${fields}`
}

function vsdxToShapeCatalogItem(definition: VsdxSymbolDefinition): ShapeCatalogItem {
  return {
    id: definition.id,
    title: definition.title,
    categoryId: knownCategory(definition.categoryId),
    status: 'planned',
    keywords: [
      definition.title,
      definition.categoryId,
      `master ${definition.masterId}`,
      'vsdx',
      ...definition.propertyNames,
      ...definition.userCellNames,
      ...definition.dataFields.map((field) => field.label),
    ],
    preview: definition.preview,
    sourceRef: sourceSummary(definition),
    widthMm: definition.widthMm,
    heightMm: definition.heightMm,
    connectionCount: definition.connectionCount,
    propertyNames: definition.propertyNames,
    dataFieldIds: definition.dataFields.map((field) => field.id),
    vsdxMasterId: definition.masterId,
  }
}

export const vsdxShapeCatalogItems: ShapeCatalogItem[] = vsdxSymbolDefinitions.map(vsdxToShapeCatalogItem)

export const shapeCatalogItems: ShapeCatalogItem[] = [
  ...coreShapeCatalogItems,
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
  })
}