export type EditorInteractionMode =
  | 'select'
  | 'pan'
  | 'copy_by_reference'
  | 'paste_by_point'
  | 'create_guide'

export type EditorCommand =
  | 'select'
  | 'pan'
  | 'copy'
  | 'cut'
  | 'paste'
  | 'undo'
  | 'redo'
  | 'copy_by_reference'
  | 'paste_by_point'
  | 'rotate_0'
  | 'rotate_90'
  | 'rotate_minus_90'
  | 'delete'
  | 'clear_generated'
  | 'create_sample_busbar'
  | 'create_text'
  | 'create_rectangle'
  | 'create_ellipse'
  | 'create_line'
  | 'create_vertical_guide'
  | 'create_horizontal_guide'
  | 'clear_guides'
  | 'zoom_fit'
  | 'zoom_100'
  | 'add_busbar_slot'
  | 'remove_busbar_slot'
  | 'toggle_layers_panel'
  | 'toggle_shape_data_panel'

export const interactionModeLabels: Record<EditorInteractionMode, string> = {
  select: 'Выбор',
  pan: 'Панорама',
  copy_by_reference: 'Выбор базовой точки',
  paste_by_point: 'Вставка по точке',
  create_guide: 'Создание направляющей',
}

export const commandLabels: Record<EditorCommand, string> = {
  select: 'Выбор',
  pan: 'Панорама',
  copy: 'Копировать',
  cut: 'Вырезать',
  paste: 'Вставить',
  undo: 'Отменить',
  redo: 'Повторить',
  copy_by_reference: 'Копировать с базовой точкой',
  paste_by_point: 'Вставить по точке',
  rotate_0: 'Поворот 0°',
  rotate_90: 'Поворот +90°',
  rotate_minus_90: 'Поворот -90°',
  delete: 'Удалить',
  clear_generated: 'Очистить созданные копии',
  create_sample_busbar: 'Шина',
  create_text: 'Текст',
  create_rectangle: 'Прямоугольник',
  create_ellipse: 'Эллипс',
  create_line: 'Линия',
  create_vertical_guide: 'Вертикальная направляющая',
  create_horizontal_guide: 'Горизонтальная направляющая',
  clear_guides: 'Очистить направляющие',
  zoom_fit: 'Вписать в окно',
  zoom_100: '100%',
  add_busbar_slot: '+ Ячейка',
  remove_busbar_slot: '− Ячейка',
  toggle_layers_panel: 'Слои',
  toggle_shape_data_panel: 'Данные фигуры',
}