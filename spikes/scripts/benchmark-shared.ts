import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { performance } from "node:perf_hooks";
import { CommandHistory, createCanonicalFixture, renderDeterministicPdf, renderDeterministicSvg, serializeProject } from "../shared/core/src/index.ts";

const output = process.argv[2];
if (!output) throw new Error("output path is required");
const timings: number[] = [];
for (let run = 0; run < 25; run += 1) {
  const history = new CommandHistory(createCanonicalFixture());
  const started = performance.now();
  for (let index = 0; index < 1000; index += 1) {
    history.execute({ type: "MoveObjects", objectIds: ["object-symbol-0001"], dx: 1, dy: 1, grid: 10 });
    history.undo();
    history.redo();
  }
  serializeProject(history.current);
  renderDeterministicSvg(history.current);
  timings.push(performance.now() - started);
}
timings.sort((a, b) => a - b);
const fixture = createCanonicalFixture();
const svg = renderDeterministicSvg(fixture);
const pdf = renderDeterministicPdf(fixture);
const result = {
  measurement_scope: "25 in-process runs; each is 1000 command/undo/redo cycles plus serialize and SVG render on the shared two-object fixture",
  node: process.version,
  platform: `${process.platform}-${process.arch}`,
  median_ms: timings[Math.floor(timings.length / 2)],
  min_ms: timings[0],
  max_ms: timings[timings.length - 1],
  logical_output_sha256: {
    canonical_json: createHash("sha256").update(serializeProject(fixture)).digest("hex"),
    svg: createHash("sha256").update(svg).digest("hex"),
    pdf: createHash("sha256").update(pdf).digest("hex")
  }
};
await mkdir(path.dirname(output), { recursive: true });
await writeFile(output, JSON.stringify(result, null, 2) + "\n", "utf8");
console.log(JSON.stringify(result, null, 2));
