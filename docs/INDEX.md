# ElectroScheme Studio — Documentation Index

Статус: canonical index  
Активный work item: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`  
Accepted main baseline: `b95d7111d9c5a36db4c355ee91f742efea8ecc10`

## Порядок чтения

1. `README.md` — назначение и общий статус продукта.
2. `AGENTS.md` — обязательный GitHub workflow и правила изменения проекта.
3. `docs/project/CURRENT_STATE.md` — фактическое текущее состояние.
4. `docs/project/PRODUCT_SCOPE.md` — целевой продукт и границы.
5. `docs/research/MARKET_ANALYSIS_INTAKE_2026-08-06.md` — принятый рыночный вход и evidence boundary.
6. `docs/architecture/VISIO_INTEROPERABILITY_CONTRACT.md` — обязательный переходный мост Visio и запрет скрытых потерь.
7. `docs/project/PROTOTYPE_QUARANTINE.md` — правила disposition, reuse и retirement прототипа.
8. `docs/project/MVP_AND_DEMO.md` — проверяемые результаты MVP, Demo и Pilot.
9. `docs/project/IMPLEMENTATION_PROGRAM.yaml` — фазы, зависимости и gates.
10. `docs/architecture/SYSTEM_ARCHITECTURE.md` — целевые компонентные границы.
11. `docs/architecture/DOMAIN_INVARIANTS.md` — обязательные инварианты модели и топологии.
12. `docs/quality/ACCEPTANCE_GATES.md` — CI, тесты и evidence.
13. `docs/decisions/0002_desktop_first_refoundation.md` — принятое desktop-first переоснование.
14. `docs/architecture/spikes/DESKTOP_PLATFORM_AND_CORE_SPIKE_EXECUTION.md` — исполнимый план активного spike.
15. `docs/architecture/spikes/CANDIDATE_EVIDENCE_BASELINE_2026-08-06.md` — официальный-source baseline по Tauri, Electron и Qt admission gate.
16. `docs/architecture/spikes/PROTOTYPE_ASSET_INVENTORY.yaml` — factual inventory и dispositions прототипа.
17. `docs/project/NEXT_WORK_ITEM.md` — исторически принятый контракт, по которому создан текущий work item; до завершения spike не является активным будущим заданием.

## Владение документами

| Документ | Владеет |
|---|---|
| `README.md` | Входная точка и публичный статус |
| `AGENTS.md` | Процесс разработки и change discipline |
| `CURRENT_STATE.md` | Изменяемый фактический срез GitHub и проекта |
| `PRODUCT_SCOPE.md` | Продуктовые границы и приоритеты |
| `MARKET_ANALYSIS_INTAKE_2026-08-06.md` | Рыночные гипотезы, reference roles и доказательность |
| `VISIO_INTEROPERABILITY_CONTRACT.md` | Compatibility boundary, diagnostics и acceptance corpus |
| `PROTOTYPE_QUARANTINE.md` | Reuse, migration disposition и retirement прототипа |
| `MVP_AND_DEMO.md` | Пользовательские acceptance scenarios |
| `IMPLEMENTATION_PROGRAM.yaml` | Фазы, зависимости, статусы и gates |
| `SYSTEM_ARCHITECTURE.md` | Целевая структура компонентов |
| `DOMAIN_INVARIANTS.md` | Инварианты данных, геометрии и топологии |
| `ACCEPTANCE_GATES.md` | Обязательная проверка изменений |
| `DESKTOP_PLATFORM_AND_CORE_SPIKE_EXECUTION.md` | Work packages, fixtures и exit criteria текущего spike |
| `CANDIDATE_EVIDENCE_BASELINE_2026-08-06.md` | Проверенные возможности, риски и обязательные эксперименты кандидатов |
| `PROTOTYPE_ASSET_INVENTORY.yaml` | Exact paths/SHAs, findings, dispositions и retirement conditions |
| `docs/decisions/*` | Принятые архитектурные решения и последствия |

## Активный work item

`DESKTOP-PLATFORM-AND-CORE-SPIKE-001` должен:

- сравнить Tauri и Electron на одном исполнимом сценарии;
- допустить Qt к полному сравнению только при доказанном материальном преимуществе;
- доказать один canonical writable document path;
- изолировать desktop/platform adapters;
- классифицировать prototype assets;
- доказать controlled VSDX/VSSX read и минимальный VSDX write;
- подтвердить открытие generated VSDX в Microsoft Visio на Windows;
- принять ADR по desktop host/runtime и canonical core ownership;
- подготовить точный `CANONICAL-DOCUMENT-CORE-001`.

Внутри этого spike запрещено строить полноценный MVP, новый постоянный UI, завершённую библиотеку символов или переносить `CanvasViewport` целиком.

## Рыночный анализ

Анализ от 6 августа 2026 года принят как стратегический вход. Детальный hands-on benchmark и окончательные `must_match / must_exceed / defer / reject` решения остаются фазой `P1_MARKET_AND_WORKFLOW_BASELINE`.

Он не может без отдельного ADR отменить:

- one canonical document model;
- command-based mutations;
- prototype quarantine;
- Windows/Linux requirement;
- local-first boundary;
- доказательность ГОСТ/СТО claims;
- обязательный Visio migration/exchange bridge.

## Историческая документация

`docs/development/patch_*`, bootstrap-описания, ранние стратегии и старые VSDX-отчёты являются историческими или исследовательскими материалами.

Они:

- не удаляются без отдельного accepted work item;
- не имеют приоритета над canonical документами;
- могут содержать устаревшие планы, пути и patch-script инструкции;
- классифицируются в prototype inventory.

При противоречии действует приоритет:

```text
accepted ADR
→ DOMAIN_INVARIANTS / SYSTEM_ARCHITECTURE / VISIO_INTEROPERABILITY_CONTRACT
→ PROTOTYPE_QUARANTINE
→ IMPLEMENTATION_PROGRAM / MVP_AND_DEMO / PRODUCT_SCOPE
→ active spike execution, candidate evidence and inventory documents
→ accepted research intake
→ CURRENT_STATE
→ README / AGENTS
→ historical documents
```

`AGENTS.md` имеет высший приоритет по процедуре работы, но не может самовольно менять продуктовые или архитектурные решения без ADR и owner acceptance.