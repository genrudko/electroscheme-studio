# Unified Product Vision

Статус: canonical foundation document  
Work item: `UNIFIED-FOUNDATION-001`

## 1. Product thesis

Продукт — единый локальный desktop-комплекс для электротехнической инженерии и эксплуатации, в котором **одна нейтральная модель электроустановки** используется для создания/редактирования схем, импорта структурированных перечней, совместимости с NPT и подготовки/проверки оперативных переключений.

Ценность комплекса не в том, чтобы быть ещё одним универсальным drawing editor. Его преимущество должно возникать из общей электротехнической семантики:

```text
оборудование
+ терминалы
+ соединения
+ topology
+ state
+ signals
+ normative rules
+ controlled views
```

## 2. Почему объединение оправдано

Три прежних проекта решали разные задачи, но начали сходиться на одной и той же предметной модели.

### Scheme Studio

Нуждается в equipment/terminal/connection/topology model для интеллектуальных электрических схем.

### NPT Engineering Toolkit

Нуждается в той же модели, чтобы переводить NPT-specific структуры в нейтральные объекты и обратно без превращения NPT в архитектурную основу всего продукта.

### Switching / TBP

Нуждается в equipment/topology/state/rules model для моделирования операций, проверки последовательностей и формирования бланков.

Следовательно, три независимых модели создавали бы дублирование, расхождения и невозможность повторно использовать проект объекта.

## 3. Core user promise

Инженер должен иметь возможность **описать объект данными один раз** и использовать эту модель в разных рабочих сценариях.

Пример:

```text
структурированный перечень оборудования/соединений
        ↓
ElectricalProject
        ├── normal single-line view
        ├── operational view
        ├── NPT-compatible representation
        ├── equipment/table views
        └── switching simulation / TBP
```

## 4. Killer workflow

Стратегически важнейший workflow:

> Импортировать правильно структурированный CSV/XLSX перечень оборудования и соединений, получить построенную electrical topology и автоматически сгенерированную схему, после чего инженер исправляет только неоднозначности и компоновку.

Это должно уменьшить зависимость от вручную поддерживаемых Visio/NPT drawing corpora и исключить повторное рисование одного объекта для каждого software tool.

Программа не должна маскировать неуверенность. После импорта пользователь видит:

- однозначно распознанные сущности;
- предположения, требующие подтверждения;
- конфликты/ошибки;
- diff при повторном импорте.

## 5. Product values

### Engineering semantics over drawing primitives

Выключатель — не картинка выключателя. Он имеет identity, type, terminals, state, properties, signal bindings, applicable rules и один или несколько graphical representations.

### Human authority over silent automation

Автоматизация должна сокращать рутину, а не прятать инженерные допущения.

### Traceable compliance over folklore

Нормативное требование существует в продукте только как правило с идентифицированным источником, редакцией, областью применимости и доказуемым поведением.

### Modern professional UX

Пользователь не должен расплачиваться за сложную domain model архаичным интерфейсом. Complex engineering software может и должно быть современным, плотным и быстрым.

### Fast iteration is a product-development requirement

Architecture и CI должны позволять увидеть малый UI change быстро. Системная надёжность достигается risk-based gates, а не запуском всего мира после изменения двух кнопок.

### Standalone first

Комплекс работает самостоятельно. NPT и EOD являются optional compatibility/integration boundaries, а не обязательными runtime dependencies.

## 6. Target users and environments

Primary users:

- оперативный/оперативно-ремонтный персонал;
- инженерно-технический персонал электроэнергетики;
- специалисты, поддерживающие электрические схемы, мнемосхемы и operational documentation;
- инженеры, формирующие/проверяющие переключения;
- специалисты по внедрению/поддержке NPT-compatible projects.

Primary usage assumptions:

- desktop workstation;
- potentially several monitors;
- large electrical projects;
- long continuous sessions;
- keyboard+mouse;
- local/offline operation required;
- Windows and Linux are target platform classes, exact supported distributions/releases are fixed after platform spike and packaging evidence.

## 7. Product modules

### Domain Core

Neutral source of truth for project/equipment/terminals/connections/topology/state/signals/rules/views.

### UI Core

Shared application shell, workspace, design system, commands, inspectors, data views and canvas infrastructure.

### Equipment Library

Semantic equipment type definitions, terminal configurations, properties, state models and approved native graphic profiles.

### Import & Reconciliation

CSV/XLSX mapping profiles, staging, normalization, ambiguity handling, diff/reconciliation and provenance.

### Scheme Studio

Electrical diagram views, domain-aware auto-layout, manual layout constraints, rendering, editing and output.

### NPT Compatibility

XSDE/XTABL read/write, NPT-specific properties/IDs, signal catalog/adapters and compatibility validation.

### Switching / TBP

Switching operations, sequence modeling, rule evaluation, interlocks, simulation and document generation.

### Compliance Core

Normative registry, applicability, profile composition, local policy overlays and explainable validation.

### Optional EOD Adapter

Thin integration only if feasibility/cost gate passes.

## 8. What the product is not

The current vision does not include building a replacement full SCADA runtime, historian, universal CAD, remote control platform or arbitrary automation platform.

The product may import operational/signal semantics needed for engineering, simulation and NPT compatibility, but that does not turn it into an online process-control system.

## 9. Success criteria

The product direction is successful when representative workflows prove that:

1. a structured equipment/topology list can become a usable electrical project and scheme with substantially less manual work than drawing from scratch;
2. engineer corrections survive re-import;
3. one domain model feeds multiple controlled views/modules;
4. scheme symbols/output are traceable to applicable graphical standards profiles;
5. switching validation identifies uncertainty and explains restrictions using versioned rules;
6. site-specific rules can be configured without weakening mandatory requirements;
7. NPT compatibility preserves required vendor-format information without contaminating neutral core;
8. UI remains responsive, discoverable and multi-monitor capable on realistic project sizes;
9. common UI changes can be visually accepted in minutes/hours, not days;
10. the standalone product remains usable if NPT or EOD integrations are absent.

## 10. Naming

`ElectroScheme Studio` remains the repository name during Foundation only for continuity. A separate future naming decision may choose a product-family/complex name after module boundaries and user-facing positioning stabilize.
