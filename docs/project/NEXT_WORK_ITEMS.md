# Next Work Items after Unified Foundation

Статус: canonical sequencing contract

## 1. Rule

Do not jump directly from Foundation into feature breadth.

The next work is a short proof chain:

```text
Infrastructure
→ Platform Stack
→ UI Core + Minimal Domain Core
→ Import-to-Scheme vertical slice
```

Each work item gets its own issue/branch/Draft PR after the previous required dependency is accepted.

---

# INFRASTRUCTURE-SPIKE-001

## Objective

Prove that GitHub can control normal development while the existing VPS executes builds/tests and returns artifacts without routine owner SSH.

## Scope

- dedicated unprivileged self-hosted runner account/service;
- repository checkout at exact PR head;
- minimal `./dev`-style command contract (temporary spike implementation permitted);
- fast success/failure test job;
- publish logs/result artifact;
- private corpus path configuration outside Git;
- workspace cleanup/retention;
- security boundary documentation.

## Acceptance scenario

1. push a tiny branch change;
2. workflow dispatches to self-hosted VPS runner;
3. exact head is printed/verified;
4. deterministic test/build succeeds;
5. a small artifact is published to GitHub;
6. coordinator can read state/results from GitHub;
7. owner can obtain the artifact without SSH;
8. deliberately failing commit/job reports useful error;
9. runner returns to clean/usable state.

## Prohibited

- product platform selection;
- installing a second paid orchestration platform;
- granting production SCADA credentials;
- putting proprietary NPT corpus into public artifacts.

---

# PLATFORM-STACK-SPIKE-001

## Dependency

`INFRASTRUCTURE-SPIKE-001` accepted.

## Objective

Select Avalonia/C#/.NET or Qt 6/C++/QML using the exact executable benchmark contract in `docs/development/PLATFORM_STACK_SPIKE.md`.

## Required outputs

- equivalent candidate apps;
- heavy semantic canvas benchmarks;
- 100k-row table benchmark;
- multi-window/workspace implementation;
- UI Gallery/headless visual evidence;
- packaging Windows/Linux;
- development-loop measurements;
- license/dependency report;
- owner manual acceptance;
- updated ADR 0007 to ACCEPTED.

## Prohibited

- feature-driven winner selection before measurements;
- carrying old Tauri spike as automatic winner;
- building full product/domain/symbol library.

---

# UI-CORE-FOUNDATION-001

## Dependency

Platform Stack ADR accepted.

## Objective

Create the first production-quality professional desktop UI foundation in the selected stack.

## Scope

- design tokens/theme;
- UI Gallery;
- application shell;
- workspace/document tabs;
- detachable/multi-window infrastructure;
- persistence/recovery of workspace layout;
- Property Inspector framework;
- tree/virtual table controls;
- command/shortcut system;
- dialogs/notifications/status;
- shared canvas viewport/selection primitives;
- HiDPI/mixed-DPI baseline;
- targeted screenshot/interaction tests.

## Acceptance

Owner manually accepts the visual/interaction direction before broad module work begins.

---

# DOMAIN-CORE-FOUNDATION-001

## Dependency

Platform Stack ADR accepted. May run partly parallel with UI Core once project layout is stable.

## Objective

Implement minimal canonical model required by the first real vertical slice.

## Scope

- project identity/schema version;
- equipment/type reference;
- terminals;
- connections;
- topology graph;
- semantic state with UNKNOWN;
- transactions/commands;
- validation result model;
- provenance skeleton;
- compliance profile refs;
- versioned native persistence and round-trip/migration tests.

## Prohibited

- full CIM;
- full equipment catalogue;
- NPT vendor fields in Core;
- full switching engine;
- UI-framework object serialization as native project model.

---

# IMPORT-TO-SCHEME-VERTICAL-SLICE-001

## Dependencies

UI Core + Domain Core baseline accepted.

## Objective

Prove the highest-value end-to-end workflow on a representative electrical fragment.

## Scenario

```text
CSV/XLSX
→ mapping profile
→ staging
→ explicit ambiguity resolution
→ Equipment/Terminals/Connections
→ topology validation
→ auto-layout
→ editable one-line view
→ manual position/route constraints
→ native save/reopen
→ changed spreadsheet re-import
→ reconciliation diff
→ apply update
→ manual layout preserved
```

## Corpus

Use a small but real/representative electrical structure, ideally a known switchgear/bay or wind-farm fragment with breakers/disconnectors/earthing switch/bus/line/transformer as needed.

Do not use only arbitrary graph nodes/rectangles.

## Acceptance

- electrical identity/topology survives save/reopen;
- ambiguity is never silently guessed;
- layout proposal is understandable;
- user can correct it with low interaction cost;
- re-import preserves manual corrections;
- diagnostics distinguish topology/import/layout/profile issues;
- owner accepts workflow/UI value.

---

# NPT-TOPOLOGY-MAPPING-EXPERIMENT-001

## Scheduling

May run as focused research after minimal Domain Core contracts exist; it does not block the first CSV/XLSX vertical slice.

## Objective

Determine whether NPT XSDE `nodes`/Tech relationships can produce a trustworthy neutral topology mapping.

## Required evidence

- one known real NPT cell/mnemonic;
- extracted raw relationships;
- neutral equipment/terminal/connection graph;
- unresolved mapping report;
- side-by-side comparison with visible one-line scheme;
- state-dependent continuity/energization test;
- explicit conclusion: sufficient / partial / unsuitable.

---

# COMPLIANCE-RULES-SLICE-001

## Scheduling

Begins after Compliance Core data contracts exist and before switching/TBP claims rely on them.

## Objective

Prove source→rule→test→diagnostic lifecycle using a very small set of real current requirements.

## Slice

- one current switching-rule source from Order 757;
- one supporting PTEES/PTEEP/POTEE applicability example;
- one site stricter overlay;
- one attempted weakening conflict;
- one UNKNOWN prerequisite scenario.

No claim of complete document coverage.

---

# EOD-INTEGRATION-FEASIBILITY-001

## Scheduling

Optional. Prefer after standalone app/API/module boundaries exist. It can be pulled earlier only if EOD architecture work materially benefits from early proof.

## Objective

Measure whether Level 1/2 integration is cheap enough.

## Scenario

- EOD-compatible module/launcher entry;
- typed site/project/equipment context;
- launch/focus standalone electrical app;
- direct navigation;
- callback/deep link to EOD;
- standalone run with adapter removed;
- measure integration changed files/dependencies/release impact.

## Required decision

`ACCEPT_LEVEL_1`, `ACCEPT_LEVEL_2`, `DEFER` or `REJECT_TOO_EXPENSIVE`.

---

## First product milestone

Do not call the project MVP merely because infrastructure/platform spikes work.

The first meaningful product milestone is the accepted `IMPORT-TO-SCHEME-VERTICAL-SLICE-001` running on the selected production stack with production-boundary UI/Domain contracts.
