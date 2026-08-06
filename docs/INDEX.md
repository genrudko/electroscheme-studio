# ElectroScheme Studio — Documentation Index

Статус: canonical index  
Программа: `PROJECT-REFOUNDATION-001`  
Baseline main: `6e1209d800c0cc65da4a922506586d5a100c2a84`

## Порядок чтения

1. `README.md` — назначение и текущий статус репозитория.
2. `AGENTS.md` — обязательный GitHub workflow и правила изменения проекта.
3. `docs/project/CURRENT_STATE.md` — фактическое текущее состояние.
4. `docs/project/PRODUCT_SCOPE.md` — целевой продукт, границы и конкурентная позиция.
5. `docs/research/MARKET_ANALYSIS_INTAKE_2026-08-06.md` — принятый рыночный вход, проверенные стратегические выводы и границы доказательности.
6. `docs/architecture/VISIO_INTEROPERABILITY_CONTRACT.md` — обязательный переходный мост Visio, уровни совместимости и запрет скрытых потерь.
7. `docs/project/PROTOTYPE_QUARANTINE.md` — запрет автоматического наследования прототипа и правила migration disposition.
8. `docs/project/MVP_AND_DEMO.md` — проверяемые пользовательские результаты MVP, demo и pilot.
9. `docs/project/IMPLEMENTATION_PROGRAM.yaml` — последовательность фаз, зависимости и gates.
10. `docs/architecture/SYSTEM_ARCHITECTURE.md` — целевая архитектура и migration direction.
11. `docs/architecture/DOMAIN_INVARIANTS.md` — обязательные правила модели документа и электрической топологии.
12. `docs/quality/ACCEPTANCE_GATES.md` — CI, тесты, visual evidence и cross-platform требования.
13. `docs/decisions/0002_desktop_first_refoundation.md` — принятое решение о desktop-first переосновании.
14. `docs/project/NEXT_WORK_ITEM.md` — готовый контракт следующего desktop/platform/core spike.

## Владение документами

| Документ | Владеет |
|---|---|
| `README.md` | Входная точка и публичный статус |
| `AGENTS.md` | Процесс разработки и change discipline |
| `CURRENT_STATE.md` | Изменяемый фактический срез GitHub/проекта |
| `PRODUCT_SCOPE.md` | Продуктовые границы и приоритеты |
| `MARKET_ANALYSIS_INTAKE_2026-08-06.md` | Рыночные гипотезы, конкурентные reference roles и проверенные стратегические выводы |
| `VISIO_INTEROPERABILITY_CONTRACT.md` | Обязательная совместимость Visio, mapping boundary, diagnostics и acceptance corpus |
| `PROTOTYPE_QUARANTINE.md` | Классификация, reuse и retirement prototype assets |
| `MVP_AND_DEMO.md` | Пользовательские acceptance scenarios |
| `IMPLEMENTATION_PROGRAM.yaml` | Фазы, зависимости, статусы и gates |
| `SYSTEM_ARCHITECTURE.md` | Целевая структура компонентов |
| `DOMAIN_INVARIANTS.md` | Инварианты данных, геометрии и топологии |
| `ACCEPTANCE_GATES.md` | Обязательная проверка изменений |
| `NEXT_WORK_ITEM.md` | Boundary следующего work item |
| `docs/decisions/*` | Принятые архитектурные решения и их последствия |

## Рыночный анализ

Полученный 6 августа 2026 года рыночный анализ принят как стратегический вход и зарегистрирован в `docs/research/MARKET_ANALYSIS_INTAKE_2026-08-06.md`.

Он уже подтверждает:

- фрагментацию рынка между drawing, ECAD, calculation, substation engineering и operational systems;
- нишу low-friction объектного редактора энергетических схем;
- необходимость изучать Модус, ETAP, Engineering Base, EPLAN, Visio, Model Studio, EnergyCS, Автограф и АСМОграф в разных reference roles;
- важность topology/state/document semantics;
- обязательность Visio interoperability как переходного рыночного моста;
- ошибочность раннего включения расчётного комплекса, SCADA и universal CAD scope.

Детальный hands-on benchmark, измеримые пользовательские сценарии и окончательные `must_match / must_exceed / defer / reject` решения остаются фазой `P1_MARKET_AND_WORKFLOW_BASELINE`.

Рыночный анализ может менять:

- приоритеты функций;
- must-match/must-exceed decisions;
- acceptance scenarios;
- post-MVP backlog.

Он не может без отдельного ADR отменить:

- one canonical document model;
- command-based mutations;
- prototype quarantine;
- Windows/Linux requirement;
- local-first boundary;
- доказательность ГОСТ/СТО claims;
- обязательный Visio migration/exchange bridge для принятого compatibility profile.

## Историческая документация

Существующие документы `docs/development/patch_*`, bootstrap-описания, ранние стратегии и отчёты VSDX являются историческими или исследовательскими материалами.

Они:

- не удаляются в `PROJECT-REFOUNDATION-001`;
- не имеют приоритета над canonical документами из этого индекса;
- могут содержать устаревшие планы, локальные пути и patch-script инструкции;
- подлежат классификации/архивации отдельным work item после принятия новой архитектуры.

При противоречии действует следующий приоритет:

```text
accepted ADR
→ DOMAIN_INVARIANTS / SYSTEM_ARCHITECTURE / VISIO_INTEROPERABILITY_CONTRACT
→ PROTOTYPE_QUARANTINE
→ IMPLEMENTATION_PROGRAM / MVP_AND_DEMO / PRODUCT_SCOPE
→ accepted research intake
→ CURRENT_STATE
→ README / AGENTS
→ historical documents
```

`AGENTS.md` имеет высший приоритет по процедуре работы, но не может самовольно менять продуктовые или архитектурные решения без ADR/owner acceptance.