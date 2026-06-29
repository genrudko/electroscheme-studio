import type { EditorCommand } from './interactionModes'

export type ShapeCatalogStatus = 'available' | 'planned'
export type ShapeCatalogItem = { id: string; title: string; categoryId: string; command?: EditorCommand; status: ShapeCatalogStatus; keywords: string[]; preview: string; sourceRef?: string }
export type ShapeCatalogCategory = { id: string; title: string; description: string; sourceRef?: string }

export const shapeCatalogCategories: ShapeCatalogCategory[] = [
  { id: 'busbars_lines_grounding', title: 'Линии / шины / заземление', description: 'Линии связи, кабели, шины, заземление' },
  { id: 'switching', title: 'Коммутационные аппараты', description: 'Выключатели, разъединители, ЗН' },
  { id: 'transformers', title: 'Трансформаторы', description: 'ТР, ТН, ТТ' },
  { id: 'primitives', title: 'Графика', description: 'Базовые графические примитивы' },
  { id: 'text', title: 'Текст и размеры', description: 'Надписи, подписи, размеры' },
]

export const shapeCatalogItems: ShapeCatalogItem[] = [
  { id: 'busbar', title: 'Шина', categoryId: 'busbars_lines_grounding', command: 'create_sample_busbar', status: 'available', keywords: ['шина', 'секция', 'busbar'], preview: '▰', sourceRef: 'Цвет шины по классу напряжения, точки подключения белые.' },
  { id: 'circuit_breaker', title: 'Выключатель', categoryId: 'switching', command: 'create_circuit_breaker', status: 'available', keywords: ['выключатель', 'breaker', 'в-10'], preview: '□', sourceRef: 'Первый рабочий символ с точками подключения.' },
  { id: 'disconnector', title: 'Разъединитель', categoryId: 'switching', status: 'planned', keywords: ['разъединитель', 'лр'], preview: '⟋' },
  { id: 'power_transformer', title: 'Трансформатор', categoryId: 'transformers', status: 'planned', keywords: ['трансформатор', 'тр'], preview: '○○' },
  { id: 'text', title: 'Текст', categoryId: 'text', command: 'create_text', status: 'available', keywords: ['текст', 'надпись'], preview: 'A' },
  { id: 'rectangle', title: 'Прямоугольник', categoryId: 'primitives', command: 'create_rectangle', status: 'available', keywords: ['прямоугольник'], preview: '▭' },
  { id: 'ellipse', title: 'Эллипс', categoryId: 'primitives', command: 'create_ellipse', status: 'available', keywords: ['эллипс'], preview: '○' },
  { id: 'primitive_line', title: 'Линия', categoryId: 'primitives', command: 'create_line', status: 'available', keywords: ['линия'], preview: '╱' },
]

export function filterShapeCatalog(query: string, categoryId: string | null): ShapeCatalogItem[] {
  const normalized = query.trim().toLowerCase()
  return shapeCatalogItems.filter((item) => {
    if (categoryId && item.categoryId !== categoryId) return false
    if (!normalized) return true
    return item.title.toLowerCase().includes(normalized) || item.keywords.some((keyword) => keyword.toLowerCase().includes(normalized))
  })
}
