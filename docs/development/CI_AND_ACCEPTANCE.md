# CI and Acceptance Strategy

Статус: canonical foundation document

## 1. Principle

Verification depth follows risk and changed ownership.

A two-button UI repair must not wait for full NPT corpus, switching scenarios and release packaging before the owner can see it. Conversely, a topology/state/normative change must not be accepted because a screenshot looks good.

## 2. Lane model

```text
L0 FAST STATIC
L1 TARGETED OWNER/MODULE TESTS
L2 VISUAL/PREVIEW ACCEPTANCE
L3 INTEGRATION/CORPUS/SCENARIO
L4 CROSS-PLATFORM/PACKAGING
L5 FULL/NIGHTLY/RELEASE
```

Workflow selection is based on changed paths plus explicit work-item risk classification; path filters are assistance, not the sole safety mechanism.

## 3. UI-only lane

Typical scope:

- design tokens;
- spacing/icons;
- shared control layout;
- non-domain interaction presentation.

Before visual acceptance:

- compile/type/build affected UI;
- targeted UI/component tests;
- UI Gallery screenshot/headless render;
- preview artifact.

Then owner visual acceptance.

Only after accepted direction, run additional platform/integration gates if the change affects shared shell/windowing/HiDPI or release baseline.

Do not run private NPT corpus/switching rule suites merely because a button margin changed.

## 4. Domain lane

Changes to neutral project/equipment/terminal/connection/state/persistence require:

- core unit tests;
- affected module tests;
- invariant tests;
- serialization round-trip/migration tests;
- import/switching integration tests if contract touched;
- compile/build relevant UI bindings.

UI screenshot is added if visible behavior changes.

## 5. Import lane

Requires:

- source parser/mapping tests;
- staging and ambiguity tests;
- reconciliation diff tests;
- destructive-change safety tests;
- provenance tests;
- atomic transaction/undo tests;
- auto-layout preservation of constraints;
- representative vertical-slice fixture.

Large synthetic datasets benchmark regression where relevant.

## 6. Scheme/canvas lane

Requires depending on change:

- geometry/layout unit tests;
- topology/view separation invariant;
- selection/hit-test interaction tests;
- deterministic render/visual snapshot;
- performance budget check for core canvas changes;
- print/export evidence;
- owner visual review.

## 7. NPT compatibility lane

Public/normal lane:

- synthetic/cleared XSDE/XTABL fixtures;
- parser/writer tests;
- preservation tests;
- typed property tests;
- safe-save validation.

Private self-hosted corpus lane when NPT format handling changes:

- full XSDE parse/unchanged round-trip;
- representative save/edit cases;
- XTABL corpus round-trip;
- signal catalog checks where affected;
- renderer comparison corpus when established;
- no proprietary corpus upload as public artifact.

NPT lane is not required for unrelated UI Core fixes.

## 8. Switching/topology/compliance lane

Highest logical risk short of real-equipment control.

Requires:

- rule-ID indexed unit tests;
- positive/negative/UNKNOWN scenarios;
- topology/state transition tests;
- sequence revalidation tests;
- local-policy non-weakening tests;
- applicable source/profile version checks;
- regression scenarios from accepted operational examples;
- deterministic explanation/result tests where practical.

Normative rule semantic change requires source/provenance review, not only green CI.

## 9. Project format/migration lane

Changing native schema requires:

- old-version load fixtures;
- migration to new schema;
- semantic comparison;
- unknown extension preservation policy tests;
- save/reopen;
- rollback/recovery behavior;
- representative real project migration before release.

## 10. Cross-platform lane

Run when framework/platform/native integration is touched or before release:

- Windows build/test/package;
- Linux build/test/package;
- native file/dialog/clipboard/drop adapter tests where automatable;
- artifact restore/start;
- platform-specific owner/manual gates as defined.

Not every domain-only commit needs a fresh expensive full installer matrix before code review if targeted libraries are platform-neutral and protected by later gates.

## 11. Performance lane

Run on:

- canvas rendering/spatial index/layout architecture changes;
- large table/tree infrastructure changes;
- topology algorithm changes;
- import reconciliation changes affecting large data;
- release/nightly.

Store raw measurements and environment metadata. Use regression thresholds with tolerance rather than flaky exact milliseconds.

## 12. Visual-first acceptance

For user-visible UI repairs/features:

```text
implement
→ fast targeted build/test
→ screenshot/preview artifact
→ owner review
→ repair if needed
→ only then expensive relevant gates
```

This is the default because previous projects wasted time running broad CI before discovering obvious visual rejection.

Automated visual tests complement, not replace, owner acceptance for major UX changes.

## 13. Failure retention

Do not rewrite history by pretending a later green build means an earlier owner-observed failure never occurred.

For important platform/compatibility defects, keep concise evidence of:

- observed failure;
- root cause;
- repair head;
- regression test;
- accepted retest.

## 14. Full suite

Full suite is appropriate for:

- release candidate;
- nightly/periodic health check;
- broad architecture refactor;
- dependency/toolchain update;
- native project schema migration;
- cross-cutting Domain Core contract change.

It may include all public tests plus private corpus lane and platform packaging where runners permit.

## 15. Preview artifacts

UI work should produce one of:

- UI Gallery screenshots/archive;
- portable app preview;
- targeted screen recording only when interaction cannot be conveyed in screenshot;
- PDF/export artifact for output changes.

The owner should not need SSH/build tools to inspect normal UI work.

## 16. Acceptance evidence by class

| Change | Minimum evidence before acceptance |
|---|---|
| text/docs | doc validation/review |
| UI visual | targeted tests + screenshot/preview + owner visual |
| shared UI infrastructure | above + relevant window/HiDPI/component tests |
| Domain Core | unit/invariant/round-trip + affected integration |
| Import | reconciliation/ambiguity/undo + representative vertical slice |
| NPT format | preservation + private corpus when relevant |
| topology/switching | scenario/invariant/UNKNOWN + normative provenance |
| packaging/platform | Windows/Linux package/start + manual native evidence |
| normative rule | source review + rule tests + coverage update |

## 17. Flakiness policy

Do not normalize flaky tests by blind reruns.

A flaky gate is a defect in the verification system:

- isolate cause;
- reduce nondeterminism;
- define tolerance if measurement inherently varies;
- quarantine only with explicit issue/owner and expiry condition.

## 18. CI budget

Track runner wall-clock and feedback latency.

A workflow that becomes slower without added risk coverage should be challenged.

Target principles:

- fast UI preview lane: minutes, not tens of minutes/hours;
- targeted core/module lane: bounded to changed subsystem;
- full private corpus/release lane: allowed to be heavier but not on every trivial commit.

Exact thresholds are set after Infrastructure/Platform spikes provide measurements.
