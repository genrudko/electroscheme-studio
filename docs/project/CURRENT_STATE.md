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
6. CI проверяет только наличие нескольких файлов и не защищает продукт от регрессий.
7. Cross-platform desktop packaging отсутствует.
8. Windows/Linux platform gates отсутствуют.
9. README и часть старой документации не соответствовали фактическому состоянию.
10. UI развивался серией repair/override patches, что создало design/CSS debt.
11. Внешний вид и пользовательский опыт текущего build не приняты владельцем как направление нового продукта.

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
- Рыночный анализ выполняется отдельным потоком и интегрируется через фазу P1.

## Что не принято

На текущем этапе не выбран окончательно:

- desktop shell;
- основной runtime-язык canonical domain/editor core;
- необходимость постоянного FastAPI runtime внутри desktop application;
- окончательная repository layout;
- способ packaging Python VSDX tooling;
- формат installer/update delivery;
- точная схема лицензирования и внешнего распространения;
- финальная feature priority до завершения market/workflow analysis.

Эти решения не должны приниматься «по вкусу» или по инерции прототипа.

## Текущий work item boundary

`PROJECT-REFOUNDATION-001` изменяет только governance/canonical documentation.

Запрещено в PR #2:

- удалять или переносить product code;
- выбирать desktop shell;
- выполнять широкую реорганизацию каталогов;
- исправлять старый UI;
- добавлять новые symbols/features;
- выдавать prototype за MVP;
- делать prototype appearance compatibility requirement.

## Следующие потоки

### Market/workflow stream

Отдельный анализ рынка формирует:

- competitor capability matrix;
- user pain points;
- must-match/must-exceed/not-needed decisions;
- обновление продуктовых приоритетов.

Результат после проверки интегрируется в P1 отдельным GitHub work item.

### Следующий implementation work item

После принятия и merge `PROJECT-REFOUNDATION-001`:

```text
DESKTOP-PLATFORM-AND-CORE-SPIKE-001
```

Его контракт находится в `docs/project/NEXT_WORK_ITEM.md`.

## Состояние программы

| Phase | Status |
|---|---|
| P0 Project refoundation | IN_PROGRESS |
| P1 Market and workflow baseline | NOT_STARTED / RESEARCH_EXTERNAL_TO_PR |
| P2 Desktop/platform and core spike | BLOCKED_BY_P0 |
| P3 Canonical document core | NOT_STARTED |
| P4 Editor kernel and design system | NOT_STARTED |
| P5 Symbol platform | NOT_STARTED |
| P6 Electrical topology | NOT_STARTED |
| P7 MVP vertical slice | NOT_STARTED |
| P8 ГОСТ/СТО profiles and output | NOT_STARTED |
| P9 Packaging, Demo and Pilot | NOT_STARTED |
| P10 Advanced product capabilities | NOT_STARTED |
