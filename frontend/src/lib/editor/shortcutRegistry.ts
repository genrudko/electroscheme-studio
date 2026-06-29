import type { EditorCommand } from './interactionModes'

export type EditorShortcut = {
  id: string
  label: string
  command: EditorCommand
  ctrl?: boolean
  shift?: boolean
  alt?: boolean
  key: string
}

export const editorShortcuts: EditorShortcut[] = [
  { id: 'copy', label: 'Ctrl+C', command: 'copy', ctrl: true, key: 'c' },
  { id: 'cut', label: 'Ctrl+X', command: 'cut', ctrl: true, key: 'x' },
  { id: 'paste', label: 'Ctrl+V', command: 'paste', ctrl: true, key: 'v' },
  { id: 'undo', label: 'Ctrl+Z', command: 'undo', ctrl: true, key: 'z' },
  { id: 'redo', label: 'Ctrl+Y', command: 'redo', ctrl: true, key: 'y' },
  { id: 'redo_shift_z', label: 'Ctrl+Shift+Z', command: 'redo', ctrl: true, shift: true, key: 'z' },
  { id: 'delete', label: 'Delete', command: 'delete', key: 'Delete' },
  { id: 'escape_select', label: 'Esc', command: 'select', key: 'Escape' },
]

export function shortcutSummary(): string {
  return editorShortcuts.map((shortcut) => shortcut.label).join(' · ')
}