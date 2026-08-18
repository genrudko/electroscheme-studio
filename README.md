# Единый электротехнический инженерный комплекс

> Рабочее имя репозитория сохраняется `electroscheme-studio` до отдельного решения о product naming.

Проект переоснован как **единый modular-monolith программный комплекс** для построения, импорта, редактирования, визуализации и анализа электрической модели объекта, выпуска электрических схем, совместимости с NPT Expert/Modus и подготовки/проверки оперативных переключений.

Ранее независимые направления — **ElectroScheme Studio**, **NPT Engineering Toolkit** и **TBP / switching-forms-generator** — рассматриваются как источники знаний, исследовательских активов и будущих модулей одного продукта.

## Главный принцип

Источником истины является нейтральная модель проекта:

```text
ElectricalProject
├── Sites / Objects
├── VoltageLevels
├── Equipment
├── Terminals
├── Connections
├── Topology
├── Signals
├── States
├── Rules / Policies
├── Metadata
└── Views
```

Схема, CSV/XLSX, XSDE, XTABL, Visio и бланк переключений **не являются параллельными источниками истины**. Они являются представлениями, импортами/экспортами, документами либо совместимостными адаптерами общей модели.

## Целевые модули

```text
Application / UI Shell
├── UI Core
├── Domain Core
├── Equipment Library
├── Import & Reconciliation
├── Scheme Studio & Auto Layout
├── NPT Compatibility
└── Switching / TBP & Interlocks
```

Целевая архитектура — **modular monolith**: модули имеют явные границы и могут быть отключаемыми на уровне продукта, но не требуют микросервисной инфраструктуры и не дублируют общую domain model.

## Killer workflow: модель и схема из структурированного перечня

Первый стратегический workflow:

```text
CSV / XLSX
  ↓
column mapping profile
  ↓
normalization
  ↓
staging + validation
  ↓
topology construction
  ↓
ElectricalProject
  ↓
domain-aware auto layout
  ↓
engineer review / manual correction
```

Повторный импорт должен выполнять reconciliation и сохранять ручные layout constraints. Неоднозначные связи не угадываются молча: они попадают в explicit review.

## Нормативный фундамент

Графическая часть схем проектируется на базе версионируемых профилей применимых требований **ГОСТ/ЕСКД**. Switching/TBP module проектируется с трассировкой к применимым нормативным документам электроэнергетики РФ, включая ПОТЭЭ, ПТЭЭП/ПТЭЭПЭЭ, ПТЭЭС, Правила переключений в электроустановках, применимые главы ПУЭ и иные источники.

Продукт не заявляет «полное соответствие» документу по одному названию. Каждое формализованное правило должно иметь provenance, редакцию/дату действия, область применимости и проверяемое поведение.

Локальные инструкции, требования предприятия, особенности объекта и производителя оборудования поддерживаются как versioned policy overlays. Локальный слой может **дополнять или ужесточать**, но не может отключить или ослабить применимое обязательное требование.

## UI/UX

UI Core — самостоятельный фундамент продукта. Цель — современный плотный professional desktop UX, рассчитанный на длительную инженерную работу, большие проекты, мышь+клавиатуру и несколько мониторов.

Не принимаются как направление продукта:

- legacy/MS-DOS-like визуальная и interaction-модель;
- sparse/mobile-first desktop UI;
- UI, где простое инженерное действие требует длинных ритуалов;
- архитектура разработки, где малый visual patch требует полного многосуточного pipeline.

## Platform stack

Финальный стек **не выбран**. Foundation допускает два кандидата:

- Avalonia + C#/.NET;
- Qt 6 + C++/QML.

Решение принимается только по эквивалентному executable Platform Spike: heavy 2D canvas, большие таблицы, multi-window/multi-monitor, HiDPI, headless/visual testing, packaging и измеримая стоимость итерации.

Существующий Tauri/WebView spike в Draft PR #4 остаётся исследовательским материалом и не является новым product baseline.

## Development Platform

```text
ChatGPT Plus / owner
        ↓
GitHub — canonical control plane
        ↓
self-hosted runner
        ↓
VPS — build/test/corpus/artifacts
        ↓
portable preview
        ↓
owner acceptance endpoint
```

Новый обязательный платный сервис, Business workspace или MCP не требуется. Локальный ПК не должен становиться обязательной build machine.

CI строится risk-based: UI-only, domain, NPT compatibility и switching/topology изменения имеют разные gates. Для UI визуальная приёмка должна происходить **до** дорогих системных проверок.

## EOD

Интеграция с Electronic Operational Documentation рассматривается только как **опциональный адаптер**. Самостоятельная работа комплекса обязательна. Если интеграция требует EOD-specific объектов в Domain Core, отдельного fork UI/runtime или существенного удорожания development/release — она отклоняется.

## Текущий work item

- issue: `UNIFIED-FOUNDATION-001` / #5;
- branch: `architecture/unified-foundation-001`;
- цель: полный Foundation-пакет, после которого запускаются Infrastructure Spike и Avalonia-vs-Qt Platform Spike.

До явной команды владельца новый PR остаётся Draft и не merge'ится.

## Начинать чтение

1. `AGENTS.md`
2. `docs/INDEX.md`
3. `docs/project/CURRENT_STATE.md`
4. `docs/project/UNIFIED_PRODUCT_VISION.md`
5. `docs/architecture/UNIFIED_SYSTEM_ARCHITECTURE.md`
6. `docs/compliance/NORMATIVE_ARCHITECTURE.md`
7. `docs/development/DEVELOPMENT_PLATFORM.md`
8. `docs/development/PLATFORM_STACK_SPIKE.md`

Старые Visio, prototype, market и spike материалы не удаляются: они сохраняются как evidence/reference и переоцениваются через migration/disposition, а не принимаются автоматически в новую архитектуру.