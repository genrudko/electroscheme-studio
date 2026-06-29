export type EditorUndoableCommand = {
  id: string
  label: string
  execute: () => void
  undo: () => void
}

export type CommandStackState = {
  undoDepth: number
  redoDepth: number
  canUndo: boolean
  canRedo: boolean
  lastCommandLabel: string
}

export class EditorCommandStack {
  private undoStack: EditorUndoableCommand[] = []
  private redoStack: EditorUndoableCommand[] = []

  execute(command: EditorUndoableCommand): CommandStackState {
    command.execute()
    this.undoStack.push(command)
    this.redoStack = []
    return this.state(command.label)
  }

  undo(): CommandStackState {
    const command = this.undoStack.pop()
    if (!command) return this.state('')
    command.undo()
    this.redoStack.push(command)
    return this.state(command.label)
  }

  redo(): CommandStackState {
    const command = this.redoStack.pop()
    if (!command) return this.state('')
    command.execute()
    this.undoStack.push(command)
    return this.state(command.label)
  }

  clear(): CommandStackState {
    this.undoStack = []
    this.redoStack = []
    return this.state('')
  }

  state(lastCommandLabel = ''): CommandStackState {
    return {
      undoDepth: this.undoStack.length,
      redoDepth: this.redoStack.length,
      canUndo: this.undoStack.length > 0,
      canRedo: this.redoStack.length > 0,
      lastCommandLabel,
    }
  }
}