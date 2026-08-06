import type { CanonicalProject, Connection, DiagramObject, StableId } from "./model.ts";
import { cloneProject, validateProject } from "./model.ts";

export type EditorCommand =
  | { type: "MoveObjects"; objectIds: StableId[]; dx: number; dy: number; grid: number }
  | { type: "InsertTemporaryObject"; object: DiagramObject }
  | { type: "DeleteObjects"; objectIds: StableId[] }
  | { type: "ConnectPorts"; connection: Connection };

function snap(value: number, grid: number): number { return Math.round(value / grid) * grid; }

export function applyCommand(current: CanonicalProject, command: EditorCommand): CanonicalProject {
  const next = cloneProject(current);
  switch (command.type) {
    case "MoveObjects": {
      const targets = new Set(command.objectIds);
      for (const object of next.objects) {
        if (targets.has(object.id)) {
          object.x = snap(object.x + command.dx, command.grid);
          object.y = snap(object.y + command.dy, command.grid);
        }
      }
      break;
    }
    case "InsertTemporaryObject":
      next.objects.push(structuredClone(command.object));
      break;
    case "DeleteObjects": {
      const deleted = new Set(command.objectIds);
      const deletedPorts = new Set(next.objects.filter(o => deleted.has(o.id)).flatMap(o => o.ports.map(p => p.id)));
      next.objects = next.objects.filter(o => !deleted.has(o.id));
      next.connections = next.connections.filter(c => !deletedPorts.has(c.fromPortId) && !deletedPorts.has(c.toPortId));
      for (const representation of next.representations) representation.objectIds = representation.objectIds.filter(id => !deleted.has(id));
      break;
    }
    case "ConnectPorts":
      next.connections.push(structuredClone(command.connection));
      break;
  }
  const errors = validateProject(next);
  if (errors.length) throw new Error(`Command rejected: ${errors.join("; ")}`);
  return next;
}

export class CommandHistory {
  private undoStack: CanonicalProject[] = [];
  private redoStack: CanonicalProject[] = [];
  private state: CanonicalProject;
  constructor(state: CanonicalProject) { this.state = state; }
  get current(): CanonicalProject { return cloneProject(this.state); }
  execute(command: EditorCommand): CanonicalProject {
    const before = cloneProject(this.state);
    const after = applyCommand(this.state, command);
    this.undoStack.push(before);
    this.redoStack = [];
    this.state = after;
    return this.current;
  }
  undo(): CanonicalProject {
    const previous = this.undoStack.pop();
    if (!previous) return this.current;
    this.redoStack.push(cloneProject(this.state));
    this.state = previous;
    return this.current;
  }
  redo(): CanonicalProject {
    const next = this.redoStack.pop();
    if (!next) return this.current;
    this.undoStack.push(cloneProject(this.state));
    this.state = next;
    return this.current;
  }
}
