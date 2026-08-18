# Unified Electrical Engineering Platform — Documentation Index

Статус: **canonical index for `UNIFIED-FOUNDATION-001`**  
Repository: `genrudko/electroscheme-studio`  
Active issue: #5  
Active branch: `architecture/unified-foundation-001`

## 1. Порядок чтения нового проекта

1. `README.md` — краткое назначение и текущий product direction.
2. `AGENTS.md` — обязательный operating/development contract.
3. `docs/project/CURRENT_STATE.md` — фактический текущий срез.
4. `docs/project/UNIFIED_PRODUCT_VISION.md` — зачем существует единый комплекс и какой user value он должен дать.
5. `docs/project/UNIFIED_SCOPE_AND_ROADMAP.md` — scope, исключения, фазы и первые vertical slices.
6. `docs/project/MIGRATION_PLAN_UNIFIED.md` — как используются/мигрируют ElectroScheme Studio, NPT Toolkit и TBP без механического слияния кода.
7. `docs/architecture/UNIFIED_SYSTEM_ARCHITECTURE.md` — modular-monolith структура и ownership.
8. `docs/architecture/DOMAIN_AND_PROJECT_MODEL.md` — `ElectricalProject`, equipment/terminal/connection/topology/state/view invariants.
9. `docs/architecture/UI_CORE.md` — design system, workspace, multi-window, shared controls/canvas и UX budgets.
10. `docs/architecture/IMPORT_AND_AUTO_LAYOUT.md` — CSV/XLSX mapping, staging, reconciliation, topology construction, layout constraints.
11. `docs/architecture/SWITCHING_AND_INTERLOCKS.md` — switching sequence/state transition/interlock model.
12. `docs/architecture/NPT_COMPATIBILITY_BOUNDARY.md` — XSDE/XTABL/NPT signal compatibility без загрязнения Core.
13. `docs/architecture/EOD_INTEGRATION_BOUNDARY.md` — optional EOD adapter и reject/cost gate.
14. `docs/compliance/NORMATIVE_ARCHITECTURE.md` — нормативный rule engine, provenance, applicability и versioning.
15. `docs/compliance/NORMATIVE_REGISTRY.md` — initial source registry и правила поддержания актуальности.
16. `docs/compliance/GRAPHICS_GOST_PROFILE.md` — графический ГОСТ/ЕСКД profile architecture.
17. `docs/compliance/LOCAL_POLICY_OVERLAYS.md` — manufacturer/enterprise/site/project тонкая настройка и non-weakening.
18. `docs/compliance/SAFETY_BOUNDARIES.md` — границы автоматизации и safety claims.
19. `docs/development/DEVELOPMENT_PLATFORM.md` — GitHub + existing VPS + self-hosted runner.
20. `docs/development/PLATFORM_STACK_SPIKE.md` — Avalonia vs Qt executable decision contract.
21. `docs/development/CI_AND_ACCEPTANCE.md` — risk-based CI, visual-first acceptance, preview builds.
22. `docs/decisions/0003_unified_electrical_platform.md` — решение об объединении продукта.
23. `docs/decisions/0004_domain_model_source_of_truth.md` — решение о neutral domain authority.
24. `docs/decisions/0005_layered_normative_policy.md` — rule layering/non-weakening.
25. `docs/decisions/0006_github_vps_development_plane.md` — control/execution plane.

## 2. PENDING decisions

До доказательного spike **не считаются принятыми**:

- final platform stack: Avalonia/C#/.NET vs Qt 6/C++/QML;
- exact native project package format;
- full plugin/dynamic-module mechanism;
- EOD integration implementation;
- полнота извлекаемой NPT topology из `nodes`/Tech relationships;
- exact scope автоматизируемых normative rules;
- final product/brand name and repository rename.

## 3. Legacy/research documentation

Существующие документы project refoundation, Visio interoperability, market research, prototype quarantine, VSDX/VSSX research, old patch/development history и Draft PR #4 **не удаляются**.

Они имеют статус:

```text
historical / research / migration evidence
```

если явно не включены в новый canonical reading order выше.

Особенно сохраняются:

- `docs/architecture/VISIO_INTEROPERABILITY_CONTRACT.md` и связанные Visio исследования — как migration/interoperability evidence;
- prototype disposition материалы — как источник reuse/retire решений;
- Tauri/WebView platform spike в PR #4 — как измерительный и implementation evidence, но не как выбранный stack;
- market/reference-product исследования — как product discovery input.

## 4. Source authority

При конфликте содержания:

```text
explicit owner instruction
→ accepted ADR
→ new canonical architecture/compliance docs from this INDEX
→ CURRENT_STATE / roadmap / migration plan
→ current research evidence
→ historical project-refoundation/prototype documents
```

`AGENTS.md` имеет высший приоритет только по operating process, но не может сам менять product/domain/normative решения.

## 5. Normative-source authority

Для нормативных фактов приоритет источников:

```text
official publication / official standards catalogue
→ official issuer material
→ authoritative legal/reference system used as cross-check
→ secondary explanatory source
```

Ни одна зафиксированная редакция не считается бессрочно «актуальной». `NORMATIVE_REGISTRY.md` хранит дату проверки, effective dates, amendments/supersedes и статус review.

## 6. Documentation change rule

Если код/архитектура меняют:

- source-of-truth model;
- module boundary;
- normative behavior;
- project storage;
- import semantics;
- safety boundary;
- UI Core contract;
- deployment/development process;

соответствующий canonical owner document обновляется в том же PR.
