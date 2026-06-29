export type EditorInteractionMode = 'select' | 'pan' | 'copy_by_reference' | 'paste_by_point' | 'create_guide'

export type EditorCommand =
  | 'select' | 'pan' | 'copy' | 'cut' | 'paste' | 'undo' | 'redo'
  | 'copy_by_reference' | 'paste_by_point'
  | 'rotate_0' | 'rotate_90' | 'rotate_minus_90'
  | 'delete' | 'clear_generated'
  | 'create_sample_busbar' | 'create_text' | 'create_rectangle' | 'create_ellipse' | 'create_line' | 'create_circuit_breaker'
  | 'create_vertical_guide' | 'create_horizontal_guide' | 'clear_guides'
  | 'zoom_fit' | 'zoom_100' | 'add_busbar_slot' | 'remove_busbar_slot'
  | 'toggle_layers_panel' | 'toggle_shape_data_panel'

export const interactionModeLabels: Record<EditorInteractionMode, string> = {
  select: 'Выбор',
  pan: 'Панорама',
  copy_by_reference: 'Выбор базовой точки',
  paste_by_point: 'Вставка по точке',
  create_guide: 'Создание направляющей',
}
