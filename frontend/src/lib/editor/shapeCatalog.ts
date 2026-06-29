import type { EditorCommand } from './interactionModes'

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
}

export type ShapeCatalogCategory = {
  id: string
  title: string
  description: string
  sourceRef?: string
}

export const shapeCatalogCategories: ShapeCatalogCategory[] = [
  { id: 'busbars_lines_grounding', title: 'Линии / шины / заземление', description: 'Линии связи, ЛЭП, кабели, шины, ответвления, заземление', sourceRef: 'Elektroshema / ГОСТ Р 56303-2014' },
  { id: 'switching', title: 'Коммутационные аппараты', description: 'Выключатели, разъединители, тележки, ЗН, отделители', sourceRef: 'Elektroshema / ГОСТ Р 56303-2014' },
  { id: 'transformers', title: 'Трансформаторы', description: 'Силовые трансформаторы, автотрансформаторы, ТН, ТТ', sourceRef: 'Elektroshema / ГОСТ Р 56303-2014' },
  { id: 'compensation_filters', title: 'Компенсация / фильтры', description: 'Реакторы, ДГР, конденсаторы, фильтры, компенсаторы', sourceRef: 'Elektroshema / ГОСТ Р 56303-2014' },
  { id: 'surge_arresters', title: 'Разрядники / ОПН', description: 'Разрядники, искровые промежутки, ОПН', sourceRef: 'Elektroshema / ГОСТ Р 56303-2014' },
  { id: 'generators_motors', title: 'Генераторы / двигатели', description: 'Генераторы, ДЭС, синхронные и асинхронные двигатели', sourceRef: 'Elektroshema / ГОСТ Р 56303-2014' },
  { id: 'fuses', title: 'Предохранители', description: 'Плавкие, инерционные, пробивные, на тележке', sourceRef: 'Elektroshema / ГОСТ Р 56303-2014' },
  { id: 'primitives', title: 'Графика', description: 'Базовые графические примитивы' },
  { id: 'text', title: 'Текст и размеры', description: 'Надписи, подписи, размеры' },
  { id: 'images', title: 'Изображения', description: 'Подложки, сканы, растровые вставки' },
]

export const shapeCatalogItems: ShapeCatalogItem[] = [
  {
    id: 'busbar',
    title: 'Шина',
    categoryId: 'busbars_lines_grounding',
    command: 'create_sample_busbar',
    status: 'available',
    keywords: ['шина', 'секция', 'busbar', 'ошиновка'],
    preview: '▰',
    sourceRef: 'Шина выполняется цветом класса напряжения, точки подключения белые.',
  },
  {
    id: 'line',
    title: 'Линия электрической связи',
    categoryId: 'busbars_lines_grounding',
    command: 'create_line',
    status: 'available',
    keywords: ['линия', 'связь', 'ошиновка', 'кабель', 'лэп'],
    preview: '╱',
    sourceRef: 'Толщина линии связи 0,4 мм в базовом профиле.',
  },
  {
    id: 'grounding',
    title: 'Заземление',
    categoryId: 'busbars_lines_grounding',
    status: 'planned',
    keywords: ['заземление', 'земля', 'ground'],
    preview: '⏚',
    sourceRef: 'УГО заземления из раздела линий/шин/заземления.',
  },
  {
    id: 'circuit_breaker',
    title: 'Выключатель',
    categoryId: 'switching',
    status: 'planned',
    keywords: ['выключатель', 'включено', 'отключено', 'breaker'],
    preview: '□',
    sourceRef: 'Коммутационные аппараты.',
  },
  {
    id: 'disconnector',
    title: 'Разъединитель',
    categoryId: 'switching',
    status: 'planned',
    keywords: ['разъединитель', 'лр', 'disconnect'],
    preview: '⟋',
    sourceRef: 'Коммутационные аппараты.',
  },
  {
    id: 'earthing_switch',
    title: 'Заземляющий разъединитель',
    categoryId: 'switching',
    status: 'planned',
    keywords: ['зн', 'заземляющий', 'earthing switch'],
    preview: '⏚',
    sourceRef: 'Коммутационные аппараты.',
  },
  {
    id: 'power_transformer',
    title: 'Трансформатор',
    categoryId: 'transformers',
    status: 'planned',
    keywords: ['трансформатор', 'тр', 'тсн', 'transformer'],
    preview: '○○',
    sourceRef: 'Графическое обозначение трансформаторов.',
  },
  {
    id: 'voltage_transformer',
    title: 'Трансформатор напряжения',
    categoryId: 'transformers',
    status: 'planned',
    keywords: ['тн', 'трансформатор напряжения', 'voltage transformer'],
    preview: 'ТН',
    sourceRef: 'Графическое обозначение трансформаторов.',
  },
  {
    id: 'current_transformer',
    title: 'Трансформатор тока',
    categoryId: 'transformers',
    status: 'planned',
    keywords: ['тт', 'трансформатор тока', 'current transformer'],
    preview: 'ТТ',
    sourceRef: 'Графическое обозначение трансформаторов.',
  },
  {
    id: 'reactor',
    title: 'Реактор',
    categoryId: 'compensation_filters',
    status: 'planned',
    keywords: ['реактор', 'дгр', 'компенсация', 'filter'],
    preview: '⌁',
    sourceRef: 'Устройства компенсации, фильтры.',
  },
  {
    id: 'capacitor',
    title: 'Конденсатор',
    categoryId: 'compensation_filters',
    status: 'planned',
    keywords: ['конденсатор', 'бск', 'capacitor'],
    preview: '⊣⊢',
    sourceRef: 'Устройства компенсации, фильтры.',
  },
  {
    id: 'surge_arrester',
    title: 'ОПН / разрядник',
    categoryId: 'surge_arresters',
    status: 'planned',
    keywords: ['опн', 'разрядник', 'surge arrester'],
    preview: '⚡',
    sourceRef: 'Разрядники, ОПН.',
  },
  {
    id: 'generator',
    title: 'Генератор',
    categoryId: 'generators_motors',
    status: 'planned',
    keywords: ['генератор', 'generator'],
    preview: 'G',
    sourceRef: 'Генераторы, электродвигатели.',
  },
  {
    id: 'motor',
    title: 'Двигатель',
    categoryId: 'generators_motors',
    status: 'planned',
    keywords: ['двигатель', 'motor'],
    preview: 'M',
    sourceRef: 'Генераторы, электродвигатели.',
  },
  {
    id: 'fuse',
    title: 'Предохранитель',
    categoryId: 'fuses',
    status: 'planned',
    keywords: ['предохранитель', 'fuse'],
    preview: '⌁',
    sourceRef: 'Предохранители.',
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

export function filterShapeCatalog(query: string, categoryId: string | null): ShapeCatalogItem[] {
  const normalized = query.trim().toLowerCase()
  return shapeCatalogItems.filter((item) => {
    const categoryMatch = !categoryId || item.categoryId === categoryId
    if (!categoryMatch) return false
    if (!normalized) return true
    return item.title.toLowerCase().includes(normalized)
      || item.keywords.some((keyword) => keyword.toLowerCase().includes(normalized))
      || item.sourceRef?.toLowerCase().includes(normalized)
  })
}