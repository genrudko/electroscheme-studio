# ElectroScheme Studio — Documentation Index

Статус: canonical index  
Активный work item: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001` — acceptance candidate  
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
14. `docs/decisions/0003_canonical_core_and_tool_boundaries.md` — pure TypeScript canonical core, FastAPI/Python/tool boundaries.
15. `docs/decisions/0004_desktop_host_and_runtime_boundaries.md` — Tauri desktop-host candidate pending owner acceptance.
16. `docs/architecture/spikes/DESKTOP_PLATFORM_AND_CORE_SPIKE_EXECUTION.md` — исполнимый план текущего spike.
17. `docs/architecture/spikes/DESKTOP_PLATFORM_COMPARISON.md` — factual Tauri/Electron comparison and selection evidence.
18. `docs/architecture/spikes/CANDIDATE_EVIDENCE_BASELINE_2026-08-06.md` — официальный-source baseline по Tauri, Electron и Qt admission gate.
19. `docs/architecture/spikes/PROTOTYPE_ASSET_INVENTORY.yaml` — factual inventory и dispositions прототипа.
20. `docs/architecture/spikes/PROTOTYPE_MIGRATION_MAP.md` — migration/disposition map.
21. `docs/architecture/spikes/VISIO_INTEROPERABILITY_SPIKE_REPORT.md` — automated Visio boundary and remaining manual gate.
22. `docs/project/CANONICAL_DOCUMENT_CORE_001_SCOPE.md` — exact production scope after P2.
23. `docs/project/NEXT_WORK_ITEM.md` — current next-work-item contract.

## Владение документами

| Документ | Владеет |
|---|---|
| `README.md` | Входная точка и публичный статус |
| `AGENTS.md` | Процесс разработки и change discipline |
| `CURRENT_STATE.md` | Изменяемый фактический срез GitHub и проекта |
| `PRODUCT_SCOPE.md` | Продуктовые границы и приоритеты |
| `IMPLEMENTATION_PROGRAM.yaml` | Фазы, зависимости, статусы и gates |
| `SYSTEM_ARCHITECTURE.md` | Целевая структура компонентов |
| `DOMAIN_INVARIANTS.md` | Инварианты данных, геометрии и топологии |
| `VISIO_INTEROPERABILITY_CONTRACT.md` | Compatibility boundary, diagnostics и acceptance corpus |
| `ACCEPTANCE_GATES.md` | Обязательная проверка изменений |
| `DESKTOP_PLATFORM_COMPARISON.md` | Измеренная сравнительная evidence-база выбора host |
| `0003_canonical_core_and_tool_boundaries.md` | Canonical core/runtime-tool ownership |
| `0004_desktop_host_and_runtime_boundaries.md` | Desktop host/runtime decision candidate |
| `PROTOTYPE_ASSET_INVENTORY.yaml` | Exact paths/SHAs, findings, dispositions и retirement conditions |
| `CANONICAL_DOCUMENT_CORE_001_SCOPE.md` | Точный production boundary следующего work item |
| `NEXT_WORK_ITEM.md` | Что разрешено начинать после принятия текущего work item |
| `docs/decisions/*` | Принятые/предлагаемые архитектурные решения и последствия |

## Активный work item

`DESKTOP-PLATFORM-AND-CORE-SPIKE-001` находится в стадии окончательной приёмки.

Автоматизировано доказано:

- один pure TypeScript canonical writable core boundary;
- Tauri secure packaged scenario на Windows/Linux;
- deterministic package/archive evidence;
- cross-platform logical-output equality;
- controlled VSDX/VSSX read и minimal VSDX write;
- prototype asset dispositions;
- Qt не прошёл admission threshold;
- Electron retained only as comparison evidence because Windows secure packaged startup fails.

Для окончательной owner acceptance остаются только:

- `OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED`;
- `OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED`.

PR #4 должен оставаться Draft до явной команды владельца.

## Следующий work item

После принятия и merge PR #4:

`CANONICAL-DOCUMENT-CORE-001`

Он не должен начинаться внутри текущего spike.

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

Они не имеют приоритета над canonical документами и не удаляются автоматически.

При противоречии действует приоритет:

```text
accepted ADR
→ DOMAIN_INVARIANTS / SYSTEM_ARCHITECTURE / VISIO_INTEROPERABILITY_CONTRACT
→ PROTOTYPE_QUARANTINE
→ IMPLEMENTATION_PROGRAM / MVP_AND_DEMO / PRODUCT_SCOPE
→ active spike execution/comparison/evidence/inventory
→ accepted research intake
→ CURRENT_STATE
→ README / AGENTS
→ historical documents
```

`AGENTS.md` имеет высший приоритет по процедуре работы, но не может самовольно менять продуктовые или архитектурные решения без ADR и owner acceptance.
