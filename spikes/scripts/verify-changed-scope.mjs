import { execFileSync } from "node:child_process";
const base=process.env.SPIKE_BASE_SHA;
if(!base) throw new Error("SPIKE_BASE_SHA is required");
const files=execFileSync("git",["diff","--name-only",`${base}...HEAD`],{encoding:"utf8"}).trim().split(/\r?\n/).filter(Boolean);
const allowed=[".github/workflows/desktop-platform-spike.yml","AGENTS.md","docs/","spikes/"];
const violations=files.filter(f=>!allowed.some(prefix=>prefix.endsWith("/")?f.startsWith(prefix):f===prefix));
if(violations.length) throw new Error(`prototype/product scope violation: ${violations.join(", ")}`);
console.log(JSON.stringify({base,files,violations},null,2));
