import type { CanonicalProject } from "./model.ts";
import { validateProject } from "./model.ts";

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .filter(([, v]) => v !== undefined)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([k, v]) => [k, canonicalize(v)])
    );
  }
  return value;
}

export function serializeProject(project: CanonicalProject): string {
  const errors = validateProject(project);
  if (errors.length) throw new Error(`Invalid project: ${errors.join("; ")}`);
  // The editor exposes the canonical document through Vue reactive proxies.
  // structuredClone rejects Proxy objects, so create a plain JSON-compatible
  // canonical copy through the same recursive projection used for serialization.
  const normalized = canonicalize(project) as CanonicalProject;
  normalized.documentIds.sort();
  normalized.documents.sort((a,b) => a.id.localeCompare(b.id)).forEach(v => v.sheetIds.sort());
  normalized.sheets.sort((a,b) => a.id.localeCompare(b.id)).forEach(v => { v.layerIds.sort(); v.representationIds.sort(); });
  normalized.layers.sort((a,b) => a.id.localeCompare(b.id));
  normalized.equipment.sort((a,b) => a.id.localeCompare(b.id));
  normalized.representations.sort((a,b) => a.id.localeCompare(b.id)).forEach(v => v.objectIds.sort());
  normalized.objects.sort((a,b) => a.id.localeCompare(b.id)).forEach(v => v.ports.sort((a,b) => a.id.localeCompare(b.id)));
  normalized.connections.sort((a,b) => a.id.localeCompare(b.id));
  normalized.diagnostics.sort((a,b) => a.id.localeCompare(b.id)).forEach(v => v.objectIds.sort());
  return `${JSON.stringify(canonicalize(normalized), null, 2)}\n`;
}

export function parseProject(text: string): CanonicalProject {
  const parsed = JSON.parse(text) as CanonicalProject;
  const errors = validateProject(parsed);
  if (errors.length) throw new Error(`Invalid project: ${errors.join("; ")}`);
  return parsed;
}
