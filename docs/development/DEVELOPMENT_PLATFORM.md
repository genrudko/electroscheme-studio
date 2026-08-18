# Development Platform

Статус: canonical foundation document

## 1. Objective

Build a development workflow suitable for one owner/coordinator and automated coding agents without making the local workstation a permanent build/CI administration machine.

The platform must optimize both correctness and **iteration speed**.

## 2. Control/execution plane

Target:

```text
Owner / ChatGPT coordinator
          │
          ▼
GitHub — canonical control plane
(issue / branch / Draft PR / diff / checks / artifacts)
          │
          ▼
Self-hosted GitHub runner
          │
          ▼
Existing VPS — execution plane
(checkout / build / tests / corpus / packaging / benchmarks)
          │
          ▼
GitHub logs + artifacts
          │
          ▼
Owner workstation — acceptance endpoint
```

No new paid Business workspace, MCP control plane or second VPS is required by Foundation.

## 3. Canonical state

GitHub owns:

- source code;
- canonical docs;
- issues/work items;
- branches/PRs;
- accepted architecture decisions;
- CI definitions;
- public/cleared fixtures;
- build/test evidence metadata.

VPS owns only reproducible execution state and private reference data that must not enter public Git.

Local workstation owns no unique canonical development state.

## 4. VPS roles

Existing VPS may host:

```text
runner service account
workspace/checkouts
build caches
private NPT/reference corpus
private site/policy fixtures
logs/artifact staging
optional local coding-agent runtime
```

Private corpora are referenced through configured paths/secrets and are never committed accidentally.

## 5. Runner security baseline

Infrastructure Spike must configure an unprivileged dedicated runner account.

Requirements:

- no production SCADA credentials;
- no blanket root requirement for normal jobs;
- repository-specific runner scope where practical;
- writable paths limited to workspace/cache/artifact areas;
- secrets only for jobs that require them;
- private corpus read/write permissions explicitly controlled;
- workflow changes from untrusted forks must not automatically gain private corpus/secrets;
- regular cleanup/retention policy for workspaces/artifacts.

## 6. One-command development launcher

After platform selection, repository should expose one stable entry point, conceptually:

```text
./dev doctor
./dev build
./dev test core
./dev test ui
./dev test npt
./dev test switching
./dev gallery
./dev preview
./dev package
./dev full
```

Windows developer wrapper may exist, but command semantics remain the same.

The launcher owns environment checks and delegates to framework-specific tooling. Contributors should not memorize long chains of package-manager/compiler commands.

## 7. Environment pinning

Once stack is selected, pin/record:

- SDK/compiler/runtime versions;
- package-manager/lock files;
- build image/OS baseline;
- Qt/.NET dependencies as applicable;
- Python/tooling versions only where still used;
- packaging dependencies;
- private-corpus schema/version fingerprints where practical.

`works on the VPS today` is not reproducibility evidence by itself.

## 8. Local machine role

The owner workstation should normally need only:

- GitHub/ChatGPT access;
- ability to run/download a preview artifact;
- optional minimal local runtime dependencies only if the final portable package cannot eliminate them.

Do not require the owner to:

- SSH for each normal task;
- manually copy patches;
- run Git commands to coordinate work;
- install full compiler stacks for routine acceptance;
- trigger complex CI pipelines by hand.

SSH remains an infrastructure/admin escape hatch, not the normal product-development UX.

## 9. Development feedback tiers

### Tier 0 — static/local agent check

Fast formatting/lint/type/unit checks before push where cheap.

### Tier 1 — targeted PR check

Runs only affected component lanes and produces fast feedback.

### Tier 2 — preview/visual acceptance

Builds a runnable Gallery/app artifact or screenshots for owner review.

### Tier 3 — module/integration gates

Runs relevant domain/corpus/scenario suites after visual/functional direction is accepted.

### Tier 4 — full/nightly/release

Cross-module, packaging, broad corpus, performance and release gates.

A small visible UI repair should normally reach Tier 2 before waiting for Tier 4.

## 10. Private NPT corpus lane

Repository CI uses synthetic/cleared fixtures.

A self-hosted private lane may run full NPT reference corpus checks:

- XSDE parse/round-trip;
- XTABL round-trip;
- renderer comparison fixtures where available;
- signal catalog consistency;
- topology extraction experiments.

The lane must report aggregate evidence without publishing proprietary files as public artifacts.

## 11. Artifacts

Useful build artifacts include:

- UI Gallery preview;
- portable application preview;
- screenshot/visual report;
- benchmark JSON/report;
- test summaries;
- format/corpus diagnostics;
- packaging archive/checksums.

Retention is risk/value based; do not preserve every intermediate artifact forever.

## 12. Coding-agent role

Agents may modify the active branch/work item within scope and use runner checks.

They must not:

- create duplicate issue/branch/PR when one exists;
- broaden scope silently;
- treat VPS workspace as canonical;
- merge/mark Ready without explicit owner command;
- access unrelated private credentials/data;
- rewrite normative rules without source/evidence review.

## 13. Infrastructure Spike acceptance

`INFRASTRUCTURE-SPIKE-001` is complete when a tiny repository change can flow end-to-end:

```text
branch push
→ self-hosted runner automatically checks out exact head
→ executes a deterministic test/build command
→ publishes result/log and a small artifact
→ coordinator reads status through GitHub
→ owner can obtain/run the artifact without SSH
```

Also prove failure path and runner cleanup.

## 14. Portability

Initial development preview/package should be self-contained as far as practical.

Exact installer/update strategy is deferred until framework selection and MVP packaging evidence.

Portable preview is prioritized early because it shortens owner acceptance loops.

## 15. Cost constraint

Baseline assumes existing costs/resources only:

- GitHub repository/actions within available plan/limits;
- existing VPS;
- ChatGPT Plus/current coordination tools.

Any new paid service must demonstrate clear measurable value over this baseline before adoption.
