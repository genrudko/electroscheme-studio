import type { CanonicalProject, DiagramObject } from "./model.ts";

const esc = (s: string) => s.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll('"', "&quot;");
function renderObject(o: DiagramObject): string {
  if (o.kind === "busbar") return `<rect data-object-id="${esc(o.id)}" x="${o.x}" y="${o.y}" width="${o.width}" height="${o.height}" />`;
  return `<g data-object-id="${esc(o.id)}" transform="translate(${o.x} ${o.y}) rotate(${o.rotation} ${o.width / 2} ${o.height / 2})"><rect x="0" y="0" width="${o.width}" height="${o.height}" rx="4" /><text x="${o.width / 2}" y="${o.height / 2 + 5}" text-anchor="middle">${esc(String(o.properties.label ?? "TEST"))}</text></g>`;
}
export function renderDeterministicSvg(project: CanonicalProject): string {
  const sheet = project.sheets[0];
  if (!sheet) throw new Error("fixture sheet missing");
  const objects = [...project.objects].sort((a,b) => a.id.localeCompare(b.id)).map(renderObject).join("");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${sheet.width} ${sheet.height}" width="${sheet.width}" height="${sheet.height}"><g fill="none" stroke="black" stroke-width="2">${objects}</g></svg>\n`;
}

export function renderDeterministicPdf(project: CanonicalProject): Uint8Array {
  const title = project.title.replace(/[()\\]/g, "_");
  const stream = `BT /F1 12 Tf 40 760 Td (${title}) Tj ET\n`;
  const objects = [
    `1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n`,
    `2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n`,
    `3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n`,
    `4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n`,
    `5 0 obj << /Length ${new TextEncoder().encode(stream).length} >> stream\n${stream}endstream\nendobj\n`
  ];
  let pdf = "%PDF-1.4\n";
  const offsets = [0];
  for (const object of objects) { offsets.push(new TextEncoder().encode(pdf).length); pdf += object; }
  const xref = new TextEncoder().encode(pdf).length;
  pdf += `xref\n0 ${objects.length + 1}\n0000000000 65535 f \n`;
  for (let i=1;i<offsets.length;i++) pdf += `${String(offsets[i]).padStart(10,"0")} 00000 n \n`;
  pdf += `trailer << /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`;
  return new TextEncoder().encode(pdf);
}
