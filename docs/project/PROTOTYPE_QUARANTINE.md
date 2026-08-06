# Prototype Quarantine and Migration Policy

## 1. Статус текущего прототипа

Состояние репозитория на `main` head `6e1209d800c0cc65da4a922506586d5a100c2a84` является исследовательским prototype baseline.

Он не является:

- визуальным эталоном;
- UX-эталоном;
- архитектурным эталоном;
- compatibility contract;
- MVP;
- основанием для требования сохранить существующее поведение.

Выявленные дефекты, неудобства, CSS overrides, нестабильные взаимодействия и временные архитектурные решения не должны переноситься в новый продукт под видом обратной совместимости.

## 2. Основное правило

Наличие кода в прототипе не является аргументом за его повторное использование.

Каждый актив получает одну disposition:

| Disposition | Значение |
|---|---|
| `retain_as_reference` | Сохранить как исследование, данные или evidence; не включать напрямую в runtime |
| `salvage_after_tests` | Допустить reuse только после изоляции, тестов и принятого migration record |
| `reimplement_from_contract` | Реализовать заново по новой спецификации; старый код используется только для понимания проблем |
| `retire` | Не переносить в целевую архитектуру; удалить/архивировать только отдельным принятым work item |

## 3. Решения по умолчанию

### Reimplement from contract

По умолчанию заново проектируются:

- внешний вид приложения;
- layout редактора;
- Ribbon/toolbar/panels;
- design system и CSS;
- CanvasViewport interaction ownership;
- drag/drop implementation;
- selection/mutation integration;
- undo/redo wiring;
- document state/store;
- backend/frontend state synchronization;
- dialogs, notifications and error UX.

### Retain as reference

По умолчанию сохраняются как исходные материалы:

- VSDX/VSSX source files;
- ShapeSheet structure research;
- извлечённые нормативные ссылки;
- список необходимых электротехнических объектов;
- зафиксированные пользовательские проблемы;
- historical screenshots/videos/evidence, если они добавлены в GitHub-controlled evidence.

### Salvage after tests

Потенциально пригодны после проверки:

- VSDX inspector;
- master metrics extractor;
- converter draft geometry;
- parametric busbar calculations;
- coordinate/snap algorithms;
- project schema ideas;
- route/waypoint representation;
- generated catalog data.

## 4. Migration record

Reuse допускается только через запись следующего содержания:

```yaml
asset: path or module
prototype_sha: exact SHA
proposed_disposition: salvage_after_tests
reason_to_reuse: measurable benefit
known_defects: []
target_owner_module: named component
required_refactoring: []
required_tests: []
windows_evidence: required
linux_evidence: required
visual_acceptance: required_or_not_applicable
owner_acceptance: pending
```

Запись хранится в GitHub и является частью PR, который выполняет миграцию.

## 5. Запреты

Запрещено:

- копировать крупный компонент целиком и исправлять его постепенно без migration record;
- сохранять старый CSS ради внешней схожести;
- объявлять старое поведение обязательным без новой acceptance specification;
- тащить два параллельных state model в переходный runtime;
- использовать старую структуру файлов как аргумент против целевой архитектуры;
- принимать prototype tests как достаточные, если они не проверяют новый contract;
- скрывать дефекты широкими `!important`, fallbacks, duplicate handlers или exception lists;
- переносить generated symbol draft в core library без инженерной проверки.

## 6. Fresh UX baseline

До реализации product UI должны быть приняты:

- information architecture;
- основные пользовательские workflows;
- interaction model;
- keyboard/mouse behavior;
- panel and command hierarchy;
- design tokens;
- component states;
- scaling and accessibility requirements;
- Windows/Linux behavior;
- visual acceptance fixtures.

Текущий prototype может использоваться для списка ошибок и необходимых возможностей, но не как макет для копирования.

## 7. Asset inventory gate

`DESKTOP-PLATFORM-AND-CORE-SPIKE-001` обязан сформировать полный inventory минимум для:

- `frontend/src/components/editor/**`;
- `frontend/src/lib/editor/**`;
- старого `useProject`/API flow;
- backend project schemas and services;
- VSDX tools;
- generated symbol data;
- parametric symbol backend;
- CSS/design layers;
- tests and CI;
- historical patch scripts/docs.

Ни один крупный каталог не мигрирует по неявному решению.

## 8. Exit criterion

Карантин считается завершённым только когда:

- каждый актив целевого охвата классифицирован;
- выбран canonical target owner;
- принят список reimplement/salvage/retire;
- новая архитектура не зависит от неоценённого prototype code;
- необходимые источники и данные сохранены;
- legacy runtime можно удалить отдельным безопасным work item без потери полезных знаний.
