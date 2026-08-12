import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { CommandHistory, createCanonicalFixture, parseProject, renderDeterministicPdf, renderDeterministicSvg, serializeProject, validateProject } from "../src/index.ts";

const canonicalFixtureText = readFileSync(new URL("../../fixtures/canonical-project.json", import.meta.url), "utf8");
const svgFixtureText = readFileSync(new URL("../../fixtures/editor-output.svg", import.meta.url), "utf8");

test("fixture validates and round-trips deterministically", () => {
  const fixture = createCanonicalFixture();
  assert.deepEqual(validateProject(fixture), []);
  const one = serializeProject(fixture);
  assert.equal(one, canonicalFixtureText);
  const two = serializeProject(parseProject(one));
  assert.equal(two, one);
});

test("serializer accepts a reactive-style proxied project", () => {
  const proxied = new Proxy(createCanonicalFixture(), {});
  assert.equal(serializeProject(proxied), canonicalFixtureText);
});

test("move uses command path, snaps, undo and redo", () => {
  const history = new CommandHistory(createCanonicalFixture());
  history.execute({ type: "MoveObjects", objectIds: ["object-symbol-0001"], dx: 17, dy: 24, grid: 10 });
  let symbol = history.current.objects.find(o => o.id === "object-symbol-0001");
  assert.deepEqual([symbol?.x, symbol?.y], [140, 140]);
  history.undo();
  symbol = history.current.objects.find(o => o.id === "object-symbol-0001");
  assert.deepEqual([symbol?.x, symbol?.y], [120, 120]);
  history.redo();
  symbol = history.current.objects.find(o => o.id === "object-symbol-0001");
  assert.deepEqual([symbol?.x, symbol?.y], [140, 140]);
});

test("SVG and PDF outputs are deterministic", () => {
  const fixture = createCanonicalFixture();
  const svg1 = renderDeterministicSvg(fixture);
  const svg2 = renderDeterministicSvg(parseProject(serializeProject(fixture)));
  assert.equal(svg1, svgFixtureText);
  assert.equal(svg2, svg1);
  const pdf1 = renderDeterministicPdf(fixture);
  const pdf2 = renderDeterministicPdf(fixture);
  assert.equal(createHash("sha256").update(pdf1).digest("hex"), createHash("sha256").update(pdf2).digest("hex"));
  assert.equal(new TextDecoder().decode(pdf1).startsWith("%PDF-1.4"), true);
});
