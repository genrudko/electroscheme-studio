# Current State — ElectroScheme Studio

Дата среза: 2026-08-06  
Статус: `PROJECT-REFOUNDATION-001` in progress

## GitHub baseline

- Repository: `genrudko/electroscheme-studio`
- Default branch: `main`
- Accepted prototype baseline head: `6e1209d800c0cc65da4a922506586d5a100c2a84`
- Active issue: #1 `PROJECT-REFOUNDATION-001`
- Active branch: `governance/project-refoundation-001`
- Active PR: создаётся как Draft в рамках issue #1

До явного merge-командования `main` остаётся неизменённым prototype baseline.

## Фактическая зрелость

Проект содержит работоспособные исследовательские элементы редактора, но не является MVP.

### Существующие полезные активы

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
- ГОСТ/СТО-oriented цветовые и визуальные исследования.

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
6. CI проверяет только наличие нескольких файлов и не защищает продукт от регрессий.
7. Cross-platform desktop packaging отсутствует.
8. Windows/Linux platform gates отсутствуют.
9. README и часть документации не соответствуют фактическому состоянию.
10. UI развивался серией repair/override patches, что создало design/CSS debt.

## Принятые решения переоснования

- Проект остаётся самостоятельным приложением, не частью ЭОД.
- Цель — desktop-first/local-first продукт для Windows и Linux.
- Browser-only WebUI не является обязательным.
- Vue/TypeScript/SVG не выбрасываются автоматически; их судьба определяется архитектурным spike.
- Существующие активы сохраняются как prototype/research assets.
- Переписывание с нуля не начинается до asset inventory и comparative spike.
- GitHub заменяет локальный patch-script workflow как canonical delivery process.
- Конкурентное преимущество определяется специализированными электротехническими сценариями, а не абсолютным количеством универсальных CAD-функций.
- ГОСТ/СТО claims требуют нормативной трассировки и acceptance evidence.

## Что не принято

На текущем этапе не выбран окончательно:

- desktop shell;
- основной runtime-язык canonical domain/editor core;
- необходимость постоянного FastAPI runtime внутри desktop application;
- окончательная repository layout;
- способ packaging Python VSDX tooling;
- формат installer/update delivery;
- точная схема лицензирования и внешнего распространения.

Эти решения не должны приниматься «по вкусу». Они входят в сравнительный spike.

## Текущий work item boundary

`PROJECT-REFOUNDATION-001` изменяет только governance/canonical documentation.

Запрещено в этом PR:

- удалять или переносить product code;
- выбирать desktop shell;
- выполнять широкую реорганизацию каталогов;
- исправлять UI;
- добавлять новые symbols/features;
- выдавать prototype за MVP.

## Следующий обязательный work item

После принятия и merge `PROJECT-REFOUNDATION-001`:

```text
DESKTOP-PLATFORM-AND-CORE-SPIKE-001
```

Его задача:

1. построить минимальный одинаковый editor scenario для кандидатов desktop architecture;
2. сравнить Windows/Linux packaging, filesystem, dialogs, clipboard, printing, updater path и SVG/pointer behavior;
3. определить runtime boundary между desktop host, UI и domain/editor core;
4. создать asset inventory и migration map для существующего prototype;
5. принять ADR о desktop shell и canonical core ownership;
6. не развивать продуктовые функции до принятия решения.

## Состояние программы

| Phase | Status |
|---|---|
| P0 Project refoundation | IN_PROGRESS |
| P1 Desktop/platform and core spike | BLOCKED_BY_P0 |
| P2 Canonical document core | NOT_STARTED |
| P3 Editor kernel | NOT_STARTED |
| P4 Symbol platform | NOT_STARTED |
| P5 Electrical topology | NOT_STARTED |
| P6 MVP vertical slice | NOT_STARTED |
| P7 ГОСТ/СТО profiles and release output | NOT_STARTED |
| P8 Cross-platform packaging | NOT_STARTED |
| P9 Demo and pilot | NOT_STARTED |
| P10 Advanced product capabilities | NOT_STARTED |
