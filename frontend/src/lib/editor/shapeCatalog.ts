import type { EditorCommand } from './interactionModes'

export type ShapeCatalogItem = {
  id: string
  title: string
  categoryId: string
  command: EditorCommand
  keywords: string[]
  preview: string
}

export type ShapeCatalogCategory = {
  id: string
  title: string
  description: string
}

export const shapeCatalogCategories: ShapeCatalogCategory[] = [
  { id: 'busbars', title: 'Шины', description: 'Секции шин и ячейки' },
  { id: 'switching', title: 'Коммутационные аппараты', description: 'Выключатели, разъединители, ЗН' },
  { id: 'instrument', title: 'Измерительные аппараты', description: 'ТН, ТТ, измерительные связи' },
  { id: 'primitives', title: 'Графика', description: 'Базовые графические примитивы' },
  { id: 'text', title: 'Текст и размеры', description: 'Надписи, подписи, размеры' },
  { id: 'images', title: 'Изображения', description: 'Подложки, сканы, растровые вставки' },
]

export const shapeCatalogItems: ShapeCatalogItem[] = [
  {
    id: 'busbar_10kv',
    title: 'Шина / секция шин',
    categoryId: 'busbars',
    command: 'create_sample_busbar',
    keywords: ['шина', 'секция', '10кв', '35кв', 'busbar'],
    preview: '▰',
  },
  {
    id: 'text',
    title: 'Текст',
    categoryId: 'text',
    command: 'create_text',
    keywords: ['текст', 'надпись', 'label'],
    preview: 'A',
  },
  {
    id: 'rectangle',
    title: 'Прямоугольник',
    categoryId: 'primitives',
    command: 'create_rectangle',
    keywords: ['прямоугольник', 'rectangle'],
    preview: '▭',
  },
  {
    id: 'ellipse',
    title: 'Эллипс',
    categoryId: 'primitives',
    command: 'create_ellipse',
    keywords: ['эллипс', 'окружность', 'circle'],
    preview: '○',
  },
  {
    id: 'line',
    title: 'Линия',
    categoryId: 'primitives',
    command: 'create_line',
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
  })
}