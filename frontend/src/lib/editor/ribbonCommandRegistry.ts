import type { EditorCommand } from './interactionModes'

export type RibbonTabId =
  | 'home'
  | 'insert'
  | 'drawing'
  | 'design'
  | 'data'
  | 'view'
  | 'export'

export type RibbonCommandGroup = {
  id: string
  title: string
  commands: EditorCommand[]
}

export const ribbonCommandRegistry: Record<RibbonTabId, RibbonCommandGroup[]> = {
  home: [
    { id: 'clipboard', title: 'Буфер', commands: ['cut', 'copy', 'paste', 'copy_by_reference', 'paste_by_point'] },
    { id: 'tools', title: 'Инструменты', commands: ['select', 'pan'] },
  ],
  insert: [
    { id: 'shapes', title: 'Фигуры', commands: ['create_sample_busbar', 'create_text', 'create_rectangle', 'create_ellipse', 'create_line'] },
  ],
  drawing: [
    { id: 'draw_tools', title: 'Рисование', commands: ['select', 'create_line', 'create_rectangle', 'create_ellipse'] },
  ],
  design: [
    { id: 'page', title: 'Параметры страницы', commands: ['zoom_fit'] },
  ],
  data: [
    { id: 'shape_data', title: 'Данные фигуры', commands: ['toggle_shape_data_panel'] },
  ],
  view: [
    { id: 'view', title: 'Вид', commands: ['create_vertical_guide', 'create_horizontal_guide', 'clear_guides', 'toggle_layers_panel'] },
  ],
  export: [
    { id: 'export', title: 'Экспорт', commands: [] },
  ],
}