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
  | 'copy_by_reference'
  | 'paste'
  | 'paste_by_point'
  | 'rotate_0'
  | 'rotate_90'
  | 'rotate_minus_90'
  | 'delete'
  | 'clear_generated'
  | 'create_sample_busbar'
  | 'create_text'
  | 'create_vertical_guide'
  | 'create_horizontal_guide'
  | 'clear_guides'
  | 'zoom_fit'
  | 'zoom_100'
  | 'add_busbar_slot'
  | 'remove_busbar_slot'

export const interactionModeLabels: Record<EditorInteractionMode, string> = {
  select: 'Выбор',
  pan: 'Панорама',
  copy_by_reference: 'Выбор базовой точки',
  paste_by_point: 'Вставка по точке',
  create_guide: 'Создание направляющей',
}

export function commandToMode(command: EditorCommand): EditorInteractionMode | null {
  if (command === 'select') return 'select'
  if (command === 'pan') return 'pan'
  if (command === 'copy_by_reference') return 'copy_by_reference'
  if (command === 'paste_by_point') return 'paste_by_point'
  return null
}