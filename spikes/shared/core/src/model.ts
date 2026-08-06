export type StableId = string;
export type DiagnosticSeverity = "info" | "warning" | "error";

export interface SourceProvenance {
  sourceKind: "native" | "vsdx" | "vssx";
  sourceId: string;
  sourcePackageSha256?: string;
  importMappingVersion: string;
}

export interface CompatibilityDiagnostic {
  id: StableId;
  severity: DiagnosticSeverity;
  code: string;
  message: string;
  objectIds: StableId[];
}

export interface ForeignPayload {
  mediaType: string;
  encoding: "utf8" | "base64";
  content: string;
  authoritative: false;
}

export interface Port {
  id: StableId;
  role: string;
  x: number;
  y: number;
}

export interface EquipmentIdentity {
  id: StableId;
  family: string;
  designation: string;
  properties: Record<string, string | number | boolean>;
}

export interface DiagramObject {
  id: StableId;
  representationId: StableId;
  kind: "temporary_test_symbol" | "busbar";
  x: number;
  y: number;
  width: number;
  height: number;
  rotation: number;
  ports: Port[];
  properties: Record<string, string | number | boolean>;
  source?: SourceProvenance;
  foreignPayload?: ForeignPayload;
}

export interface DiagramRepresentation {
  id: StableId;
  equipmentId?: StableId;
  sheetId: StableId;
  objectIds: StableId[];
  profileVersion: string;
}

export interface Connection {
  id: StableId;
  fromPortId: StableId;
  toPortId: StableId;
  electricalKind: "temporary_spike_connection";
}

export interface Layer {
  id: StableId;
  name: string;
  visible: boolean;
  locked: boolean;
}

export interface Sheet {
  id: StableId;
  name: string;
  width: number;
  height: number;
  layerIds: StableId[];
  representationIds: StableId[];
}

export interface EngineeringDocument {
  id: StableId;
  documentType: "normal_single_line_spike";
  profileVersion: string;
  sheetIds: StableId[];
}

export interface CanonicalProject {
  schemaVersion: 1;
  projectId: StableId;
  title: string;
  documentIds: StableId[];
  documents: EngineeringDocument[];
  sheets: Sheet[];
  layers: Layer[];
  equipment: EquipmentIdentity[];
  representations: DiagramRepresentation[];
  objects: DiagramObject[];
  connections: Connection[];
  diagnostics: CompatibilityDiagnostic[];
}

export function cloneProject(project: CanonicalProject): CanonicalProject {
  return structuredClone(project);
}

export function validateProject(project: CanonicalProject): string[] {
  const errors: string[] = [];
  if (project.schemaVersion !== 1) errors.push("unsupported schemaVersion");
  const ids = new Set<string>();
  const add = (kind: string, id: string) => {
    if (!id) errors.push(`${kind} id is empty`);
    if (ids.has(id)) errors.push(`duplicate id ${id}`);
    ids.add(id);
  };
  add("project", project.projectId);
  project.documents.forEach(v => add("document", v.id));
  project.sheets.forEach(v => add("sheet", v.id));
  project.layers.forEach(v => add("layer", v.id));
  project.equipment.forEach(v => add("equipment", v.id));
  project.representations.forEach(v => add("representation", v.id));
  project.objects.forEach(v => { add("object", v.id); v.ports.forEach(p => add("port", p.id)); });
  project.connections.forEach(v => add("connection", v.id));
  const ports = new Set(project.objects.flatMap(o => o.ports.map(p => p.id)));
  for (const c of project.connections) {
    if (!ports.has(c.fromPortId)) errors.push(`missing fromPortId ${c.fromPortId}`);
    if (!ports.has(c.toPortId)) errors.push(`missing toPortId ${c.toPortId}`);
  }
  const reps = new Set(project.representations.map(v => v.id));
  for (const o of project.objects) if (!reps.has(o.representationId)) errors.push(`missing representation ${o.representationId}`);
  return errors;
}
