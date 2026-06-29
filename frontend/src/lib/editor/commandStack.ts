export type CommandStackState = { undoDepth: number; redoDepth: number; canUndo: boolean; canRedo: boolean; lastCommandLabel: string }
export class EditorCommandStack {
  state(lastCommandLabel = ''): CommandStackState { return { undoDepth: 0, redoDepth: 0, canUndo: false, canRedo: false, lastCommandLabel } }
  undo(): CommandStackState { return this.state('') }
  redo(): CommandStackState { return this.state('') }
}
