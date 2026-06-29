export type EditorInteractionMode =
  | 'select'
  | 'pan'
  | 'copy_by_reference'
  | 'paste_by_point'

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

export const interactionModeLabels: Record<EditorInteractionMode, string> = {
  select: 'Selection',
  pan: 'Pan',
  copy_by_reference: 'Pick base point',
  paste_by_point: 'Paste by point',
}

export function commandToMode(command: EditorCommand): EditorInteractionMode | null {
  if (command === 'select') return 'select'
  if (command === 'pan') return 'pan'
  if (command === 'copy_by_reference') return 'copy_by_reference'
  if (command === 'paste_by_point') return 'paste_by_point'
  return null
}