# ElectroScheme Studio — Documentation Index

Статус: canonical index  
Программа: `PROJECT-REFOUNDATION-001`  
Baseline main: `6e1209d800c0cc65da4a922506586d5a100c2a84`

## Порядок чтения

1. `README.md` — назначение и текущий статус репозитория.
2. `AGENTS.md` — обязательный GitHub workflow и правила изменения проекта.
3. `docs/project/CURRENT_STATE.md` — фактическое текущее состояние.
4. `docs/project/PRODUCT_SCOPE.md` — целевой продукт, границы и конкурентная позиция.
5. `docs/project/MVP_AND_DEMO.md` — проверяемые пользовательские результаты MVP, demo и pilot.
6. `docs/project/IMPLEMENTATION_PROGRAM.yaml` — последовательность фаз, зависимости и gates.
7. `docs/architecture/SYSTEM_ARCHITECTURE.md` — целевая архитектура и migration direction.
8. `docs/architecture/DOMAIN_INVARIANTS.md` — обязательные правила модели документа и электрической топологии.
9. `docs/quality/ACCEPTANCE_GATES.md` — CI, тесты, visual evidence и cross-platform требования.
10. `docs/decisions/0002_desktop_first_refoundation.md` — принятое решение о desktop-first переосновании.

## Владение документами

| Документ | Владеет |
|---|---|
| `README.md` | Входная точка и публичный статус |
| `AGENTS.md` | Процесс разработки и change discipline |
| `CURRENT_STATE.md` | Изменяемый фактический срез GitHub/проекта |
| `PRODUCT_SCOPE.md` | Продуктовые границы и приоритеты |
| `MVP_AND_DEMO.md` | Пользовательские acceptance scenarios |
| `IMPLEMENTATION_PROGRAM.yaml` | Фазы, зависимости, статусы и gates |
| `SYSTEM_ARCHITECTURE.md` | Целевая структура компонентов |
| `DOMAIN_INVARIANTS.md` | Инварианты данных, геометрии и топологии |
| `ACCEPTANCE_GATES.md` | Обязательная проверка изменений |
| `docs/decisions/*` | Принятые архитектурные решения и их последствия |

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
→ DOMAIN_INVARIANTS / SYSTEM_ARCHITECTURE
→ IMPLEMENTATION_PROGRAM / MVP_AND_DEMO / PRODUCT_SCOPE
→ CURRENT_STATE
→ README / AGENTS
→ historical documents
```

`AGENTS.md` имеет высший приоритет по процедуре работы, но не может самовольно менять продуктовые или архитектурные решения без ADR/owner acceptance.
