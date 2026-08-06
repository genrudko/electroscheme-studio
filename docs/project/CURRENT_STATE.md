# Current State — ElectroScheme Studio

Дата среза: 2026-08-06  
Статус: `PROJECT-REFOUNDATION-001` in progress

## GitHub baseline

- Repository: `genrudko/electroscheme-studio`
- Default branch: `main`
- Prototype baseline head: `6e1209d800c0cc65da4a922506586d5a100c2a84`
- Active issue: #1 `PROJECT-REFOUNDATION-001`
- Active branch: `governance/project-refoundation-001`
- Active Draft PR: #2 `[PROJECT-REFOUNDATION-001] Re-found product architecture and GitHub workflow`

До явного merge-командования `main` остаётся неизменённым prototype baseline. PR #2 остаётся Draft.

Exact branch head, `ahead_by`, `behind_by`, changed-file count and current workflow results are volatile GitHub state and must be read from PR #2 before every continuation or acceptance action. They are intentionally not self-recorded as immutable values inside a commit that changes the head itself.

## Фактическая зрелость

Проект содержит исследовательские элементы редактора, но не является MVP, product UX baseline или compatibility baseline.

### Существующие исследовательские активы

- Vue 3 + TypeScript + SVG frontend prototype;
- FastAPI/Pydantic backend prototype;
- SVG canvas с сеткой, масштабированием, линейками и направляющими;
- выделение, мультивыбор, базовые примитивы и текст;
- pointer-based drag/drop research;
- параметрическая модель шин и bay slots;
- заготовка command stack;
- backend-модель проекта, символов, терминалов и соединений;
- VSDX/VSSX inspector и ShapeSheet metrics extraction;
- converter VSDX masters → reviewable draft symbols;
- generated symbol catalog и review workflow;
- ГОСТ/СТО-oriented исследования.

Наличие в этом списке не означает разрешение на автоматический reuse. Действует `docs/project/PROTOTYPE_QUARANTINE.md`.

### Критические ограничения baseline

1. Существуют параллельные и несовместимые state/document models:
   - backend `Project`;
   - frontend `useProject`;
   - frontend `EditorDocument`;
   - локальные коллекции и состояния `CanvasViewport`.
2. Undo/redo stack не является обязательным mutation path для реальных операций.
3. `CanvasViewport` объединяет слишком много ответственности.
4. Backend хранит активный проект преимущественно in-memory.
5. VSDX drafts в основном не являются принятыми рабочими символами.
6. Текущие VSDX tools преимущественно читают/конвертируют отдельные masters и не доказывают editable document import, VSDX export или round-trip compatibility.
7. CI проверяет только наличие нескольких файлов и не защищает продукт от регрессий.
8. Cross-platform desktop packaging отсутствует.
9. Windows/Linux platform gates отсутствуют.
10. README и часть старой документации не соответствовали фактическому состоянию.
11. UI развивался серией repair/override patches, что создало design/CSS debt.
12. Внешний вид и пользовательский опыт текущего build не приняты владельцем как направление нового продукта.

## Принятые решения переоснования

- Проект остаётся самостоятельным приложением, не частью ЭОД.
- Цель — desktop-first/local-first продукт для Windows и Linux.
- Browser-only WebUI не является обязательным.
- Vue/TypeScript/SVG не выбрасываются автоматически; их судьба определяется архитектурным spike.
- Прототип помещён в карантин, а не объявлен основой нового продукта.
- Для UI/CSS, взаимодействий и state ownership решение по умолчанию — `reimplement_from_contract`.
- Reuse допускается только через asset disposition, новые тесты и owner acceptance.
- Переписывание всего репозитория с нуля не начинается до asset inventory и comparative spike.
- GitHub заменяет локальный patch-script workflow как canonical delivery process.
- Конкурентное преимущество определяется специализированными электротехническими сценариями.
- ГОСТ/СТО claims требуют нормативной трассировки и acceptance evidence.
- Рыночный анализ от 2026-08-06 принят как стратегический вход и зарегистрирован в `docs/research/MARKET_ANALYSIS_INTAKE_2026-08-06.md`.
- Долгосрочный контур включает главные, нормальные, временно-нормальные, однолинейные, трёхлинейные и эксплуатационные representations.
- Первый MVP остаётся ограничен однолинейной нормальной схемой.
- Первый MVP обязан включать editable import утверждённого VSDX-подмножества и migration path для утверждённых VSSX masters.
- До Pilot обязательны editable VSDX export, открытие результата в Microsoft Visio и controlled round-trip corpus.
- Visio interoperability является обязательным adoption/migration bridge, а не optional post-MVP feature.
- VSDX/VSSX — source/import/export subsystem, а не semantic authority и не canonical internal document model.
- Silent import/export losses запрещены; unsupported content должен диагностироваться и сохраняться/блокироваться по явной стратегии.
- Legacy `.vsd/.vss` входят в corpus inventory; до Pilot требуется локальный документированный migration path.
- CIM — будущий exchange adapter и источник архитектурных понятий, а не обязательная внутренняя UI/document model.
- Canonical model должен позволять одну equipment identity и несколько controlled diagram representations, не реализуя все виды схем в MVP.

## Принятые конкурентные reference roles

- Visio, Автограф, АСМОграф: low-friction editing, библиотеки, свободная компоновка и большие схемы;
- Модус: эксплуатационная энергетическая семантика, topology, states and CIM-oriented preparation;
- ETAP: intelligent single-line, continuity and energized/de-energized presentation;
- AUCOTEC Engineering Base PTD: shared data for primary, secondary, protection and control;
- EPLAN/Zuken/SEE/WSCAD: documentation automation;
- Model Studio CS/EnergyCS: Russian project, normative and calculation context.

Ни один продукт не принят как единый архитектурный или UX-шаблон.

## Что не принято

На текущем этапе не выбран окончательно:

- desktop shell;
- основной runtime-язык canonical domain/editor core;
- необходимость постоянного FastAPI runtime внутри desktop application;
- окончательная repository layout;
- способ packaging Python VSDX tooling;
- формат installer/update delivery;
- точная схема лицензирования и внешнего распространения;
- окончательная приоритизация post-MVP функций;
- конкретный внутренний формат project package;
- конкретный CIM profile coverage;
- состав расчётных adapters;
- точный первый Visio compatibility profile и tolerance;
- corpus реальных VSDX/VSSX/VSD/VSS;
- механизм migration для legacy `.vsd/.vss`;
- необходимость и допустимость Windows-only bridge для отдельных legacy форматов.

Эти решения не должны приниматься «по вкусу», по инерции прототипа или только по vendor feature lists.

## Текущий work item boundary

`PROJECT-REFOUNDATION-001` изменяет только governance/canonical documentation.

Запрещено в PR #2:

- удалять или переносить product code;
- выбирать desktop shell;
- выполнять широкую реорганизацию каталогов;
- исправлять старый UI;
- добавлять новые symbols/features;
- выдавать prototype за MVP;
- делать prototype appearance compatibility requirement;
- превращать VSDX в canonical project format;
- заявлять arbitrary/lossless Visio compatibility;
- начинать calculation/SCADA/CIM implementation.

## Следующие потоки

### P1 Market/workflow baseline

Полученный анализ является входом, но не заменяет hands-on benchmark.

P1 должен сформировать:

- source-traceable competitor capability/reference-role matrix;
- 8–12 реальных user workflows;
- pain-point inventory;
- reproducible/manual evidence для priority products;
- task time/action count/error observations;
- must-match/must-exceed/defer/reject decisions;
- точную reference scheme для MVP;
- recommendation по начальному normative profile;
- representative Visio VSDX/VSSX corpus;
- inventory версий Visio и реально используемых ShapeSheet/connector/property features;
- prevalence и migration requirements для `.vsd/.vss`;
- supported compatibility subset и loss-tolerance proposal.

### Следующий implementation work item

После принятия и merge `PROJECT-REFOUNDATION-001`:

```text
DESKTOP-PLATFORM-AND-CORE-SPIKE-001
```

Его контракт находится в `docs/project/NEXT_WORK_ITEM.md`.

Spike обязан доказать controlled VSDX read, VSSX read, minimal VSDX write и открытие generated VSDX в Microsoft Visio на Windows, не выбирая VSDX внутренней моделью продукта.

## Проверки

- Current PR changes remain documentation/governance only.
- Product code changes: `0`.
- Existing CI remains a prototype placeholder and cannot be represented as product verification.
- Acceptance requires a fresh factual read of PR #2 exact head, compare state and workflow runs.

## Состояние программы

| Phase | Status |
|---|---|
| P0 Project refoundation | IN_PROGRESS |
| P1 Market and workflow baseline | STRATEGIC_INPUT_RECEIVED / HANDS_ON_VALIDATION_PENDING |
| P2 Desktop/platform/core and Visio-path spike | BLOCKED_BY_P0 |
| P3 Canonical document core | NOT_STARTED |
| P4 Editor kernel and design system | NOT_STARTED |
| P5 Symbol platform and VSSX migration | NOT_STARTED |
| P6 Electrical topology | NOT_STARTED |
| P7 Normal single-line MVP plus accepted VSDX import | NOT_STARTED |
| P8 ГОСТ/СТО profiles and output | NOT_STARTED |
| P9 Packaging, Visio export, Demo and Pilot | NOT_STARTED |
| P10 Advanced product capabilities | NOT_STARTED |