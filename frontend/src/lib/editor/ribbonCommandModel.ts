import type { EditorIconId } from './editorIconSet'

export type RibbonCommandId =
  | 'select'
  | 'pan'
  | 'copy'
  | 'paste'
  | 'copy-by-point'
  | 'paste-by-point'
  | 'text'
  | 'rectangle'
  | 'ellipse'
  | 'line'
  | 'connector'
  | 'insert-image'
  | 'show-grid'
  | 'show-rulers'
  | 'show-guides'
  | 'layers'
  | 'ui-settings'
  | 'export-svg'
  | 'export-pdf'

export type RibbonCommandModel = {
  id: RibbonCommandId
  label: string
  icon: EditorIconId
  description: string
}

export type RibbonGroupModel = {
  id: string
  title: string
  commands: RibbonCommandModel[]
}

export type RibbonTabModel = {
  id: string
  title: string
  groups: RibbonGroupModel[]
}

export const visioLikeRibbonTabs: RibbonTabModel[] = [
  {
    id: 'home',
    title: 'Главная',
    groups: [
      {
        id: 'tools',
        title: 'Инструменты',
        commands: [
          { id: 'select', label: 'Указатель', icon: 'select', description: 'Выбор, рамка выделения, Ctrl-мультивыбор' },
          { id: 'pan', label: 'Панорама', icon: 'pan', description: 'Панорамирование канваса' },
        ],
      },
      {
        id: 'clipboard',
        title: 'Буфер',
        commands: [
          { id: 'copy', label: 'Копировать', icon: 'copy', description: 'Копирование выделения' },
          { id: 'paste', label: 'Вставить', icon: 'paste', description: 'Вставка из буфера' },
          { id: 'copy-by-point', label: 'С базовой точкой', icon: 'copyByPoint', description: 'Копирование с опорной точкой' },
          { id: 'paste-by-point', label: 'Вставить по точке', icon: 'copyByPoint', description: 'Точная вставка относительно базовой точки' },
        ],
      },
    ],
  },
  {
    id: 'insert',
    title: 'Вставка',
    groups: [
      {
        id: 'figures',
        title: 'Фигуры',
        commands: [
          { id: 'text', label: 'Текст', icon: 'text', description: 'Текстовый блок' },
          { id: 'insert-image', label: 'Изображение', icon: 'image', description: 'Вставка подложки/скана' },
        ],
      },
    ],
  },
  {
    id: 'drawing',
    title: 'Рисование',
    groups: [
      {
        id: 'primitives',
        title: 'Примитивы',
        commands: [
          { id: 'rectangle', label: 'Прямоугольник', icon: 'rectangle', description: 'Графический прямоугольник' },
          { id: 'ellipse', label: 'Эллипс', icon: 'ellipse', description: 'Окружность/эллипс' },
          { id: 'line', label: 'Линия', icon: 'line', description: 'Линия/отрезок' },
        ],
      },
    ],
  },
  {
    id: 'symbols',
    title: 'Символы',
    groups: [
      {
        id: 'libraries',
        title: 'Библиотеки',
        commands: [
          { id: 'select', label: 'Выбрать символ', icon: 'select', description: 'Работа с VSDX-библиотекой символов' },
        ],
      },
    ],
  },
  {
    id: 'connections',
    title: 'Соединения',
    groups: [
      {
        id: 'connectors',
        title: 'Связи',
        commands: [
          { id: 'connector', label: 'Соединительная линия', icon: 'connector', description: 'Электрическая связь между портами/точками подключения' },
        ],
      },
    ],
  },
  {
    id: 'view',
    title: 'Вид',
    groups: [
      {
        id: 'show',
        title: 'Показать',
        commands: [
          { id: 'show-rulers', label: 'Линейки', icon: 'ruler', description: 'Показать/скрыть линейки' },
          { id: 'show-grid', label: 'Сетка', icon: 'grid', description: 'Показать/скрыть сетку' },
          { id: 'show-guides', label: 'Направляющие', icon: 'guides', description: 'Показать/скрыть направляющие' },
          { id: 'layers', label: 'Слои', icon: 'layers', description: 'Панель слоёв' },
          { id: 'ui-settings', label: 'Интерфейс', icon: 'settings', description: 'Масштаб UI и параметры редактора' },
        ],
      },
    ],
  },
  {
    id: 'export',
    title: 'Экспорт',
    groups: [
      {
        id: 'export',
        title: 'Вывод',
        commands: [
          { id: 'export-svg', label: 'SVG', icon: 'export', description: 'Экспорт схемы в SVG' },
          { id: 'export-pdf', label: 'PDF', icon: 'export', description: 'Экспорт листа в PDF' },
        ],
      },
    ],
  },
]
