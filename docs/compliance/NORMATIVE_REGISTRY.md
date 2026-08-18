# Initial Normative Source Registry

Статус: canonical foundation registry  
Verification snapshot: **2026-08-18**

> This registry is an initial source baseline, not a declaration that all requirements from the listed documents are already implemented. Every software rule still needs scope extraction, applicability review and acceptance evidence.

## 1. Verification discipline

Preferred source authority:

```text
Official Internet Portal of Legal Information / official issuer
→ official Rosstandart standards catalogue
→ authoritative legal-reference system for consolidated/current-edition cross-check
→ secondary source only as discovery support
```

For each production source store official publication/registration identifiers whenever available.

## 2. Electrical safety / operational regulations

### RU-OT-903N — ПОТЭЭ

- Issuer: Ministry of Labour and Social Protection of the Russian Federation.
- Order: **15.12.2020 № 903н**.
- Title: `Об утверждении Правил по охране труда при эксплуатации электроустановок`.
- Ministry of Justice registration: **30.12.2020 № 61957**.
- Official publication identifier: **0001202012300142**, published 30.12.2020.
- Amendment identified: order **29.04.2022 № 279н**, official publication **0001202206010011**.
- Current-edition cross-check at 2026-08-18: edition dated **29.04.2025**, including order **№ 287н**, effective from 01.09.2025; consolidated references state validity through **01.09.2031**.
- Registry state: `ACTIVE / SOURCE_TEXT_EXTRACTION_PENDING`.
- Product relevance: work/operational electrical-safety requirements, personnel/actions/checks that may constrain switching workflows.
- Caution: many requirements are organizational/procedural and cannot be reduced to topology predicates.

### RU-PTEEP-811 — ПТЭЭП / ПТЭЭПЭЭ

- Issuer: Ministry of Energy of the Russian Federation.
- Order: **12.08.2022 № 811**.
- Title: `Об утверждении Правил технической эксплуатации электроустановок потребителей электрической энергии`.
- Ministry of Justice registration: **07.10.2022 № 70433**.
- Official publication identifier: **0001202210070065**, published 07.10.2022.
- Effective from: **07.01.2023**.
- Current-edition cross-check at 2026-08-18: no later amendment to the rule text was identified in the consolidated reference checked; retain continuous monitoring.
- Registry state: `ACTIVE / SOURCE_TEXT_EXTRACTION_PENDING`.
- Product relevance: consumer electrical-installation operation, documentation/personnel/maintenance rules, selected switching/project validation depending on project role.
- Applicability warning: does not automatically apply in the same way to every object/user; Compliance Core must resolve organization/object scope.

### RU-PTEES-1070 — ПТЭЭС

- Issuer: Ministry of Energy of the Russian Federation.
- Order: **04.10.2022 № 1070**.
- Title: `Об утверждении Правил технической эксплуатации электрических станций и сетей Российской Федерации и о внесении изменений ...`.
- Ministry of Justice registration: **06.12.2022 № 71384**.
- Official publication identifier: **0001202212060056**.
- Amendment chain currently identified for consolidated edition:
  - 29.11.2024 **№ 2321**;
  - 09.12.2024 **№ 2398**;
  - 30.10.2025 **№ 1427** (registered 30.03.2026 № 85786, effective 11.04.2026);
  - 08.04.2026 **№ 343** (registered 15.06.2026 № 87018, effective 27.06.2026).
- Current-edition cross-check at 2026-08-18: **08.04.2026**.
- Registry state: `ACTIVE / SOURCE_TEXT_EXTRACTION_PENDING`.
- Product relevance: operation of power stations/networks, technical state/operations and selected switching/topology requirements for applicable energy-sector objects.

### RU-SWITCH-757 — Правила переключений в электроустановках

- Issuer: Ministry of Energy of the Russian Federation.
- Order: **13.09.2018 № 757**.
- Title: `Об утверждении Правил переключений в электроустановках`.
- Ministry of Justice registration: **22.11.2018 № 52754**.
- Consolidated amendment chain currently identified:
  - 23.06.2022 **№ 582**;
  - 12.08.2022 **№ 811** (changes to the order-level provisions);
  - 04.10.2022 **№ 1070**;
  - 01.09.2023 **№ 714**, official publication **0001202312210014**;
  - 09.12.2024 **№ 2398**;
  - 08.04.2026 **№ 343**, effective 27.06.2026.
- Current-edition cross-check at 2026-08-18: **08.04.2026**.
- Registry state: `ACTIVE / HIGH_PRIORITY_FOR_SWITCHING_MODULE`.
- Product relevance: direct requirements for organization/order/sequence of switching, switching programs, standard programs, switching forms and standard forms.
- Priority: this is one of the first sources to be decomposed into machine-checkable/assisted-review rule coverage.

## 3. ПУЭ

Registry ID family: `RU-PUE-*`.

**Do not create one fictitious `PUE_CURRENT` source.**

PУЭ is historically issued/updated in separate editions/chapters and has a complicated applicability/status history. The product must register relevant chapters separately with:

- exact chapter/edition;
- approving act/source;
- effective/status evidence;
- project applicability;
- replacement/supersession relationships.

Foundation state: `DISCOVERY_REQUIRED_PER_CHAPTER`.

Initial priority chapters are selected from real product workflows (switchgear, grounding, conductors/cables, substations, etc.), not by attempting to ingest all PУЭ into code at once.

## 4. ESKD / electrical scheme standards

Official Rosstandart catalogue is source authority for status/changes.

### GOST-2.701-2008

- `Единая система конструкторской документации. Схемы. Виды и типы. Общие требования к выполнению`.
- Rosstandart status at verification: **Действует**.
- Registration order: **25.12.2008 № 702-ст**.
- Known correction registered 05.12.2011 / published in ИУС 2-2012.
- Product role: scheme type/document/common execution baseline.
- Registry state: `ACTIVE / GRAPHICS_PROFILE_SOURCE`.

### GOST-2.702-2011

- `Единая система конструкторской документации. Правила выполнения электрических схем`.
- Rosstandart status at verification: **Действует**.
- Registration order: **03.08.2011 № 211-ст**.
- Effective date: **01.01.2012**.
- Known correction: ИУС 1-2021.
- Product role: electrical scheme execution rules.
- Registry state: `ACTIVE / HIGH_PRIORITY_GRAPHICS_PROFILE_SOURCE`.

### Related ESKD graphical-symbol family — discovery/coverage set

The native symbol/profile work must review the applicable current members of the ESKD UGO/line family rather than relying on memory or NPT/Visio appearance. Initial candidate family includes standards in the `ГОСТ 2.72x`, `ГОСТ 2.75x` and related ESKD series as applicable to specific equipment/connection types.

Registry state: `OFFICIAL_CATALOGUE_REVIEW_REQUIRED_BEFORE_ENCODING`.

Do not claim coverage of a family until each exact designation/status is verified in Rosstandart catalogue.

## 5. Enterprise/site/manufacturer sources

These are not globally registered public norms. They enter a project through controlled overlays.

Source categories:

```text
MANUFACTURER_MANUAL
MANUFACTURER_TECHNICAL_REQUIREMENT
ENTERPRISE_STANDARD
ENTERPRISE_OPERATION_INSTRUCTION
SITE_SWITCHING_INSTRUCTION
SITE_EQUIPMENT_INSTRUCTION
PROJECT_REQUIREMENT
```

Each instance requires:

- organization/site/equipment scope;
- document identifier/revision/date;
- approval/effective period where known;
- authorized storage/reference;
- mapped rules/templates;
- relationship to mandatory baseline.

See `LOCAL_POLICY_OVERLAYS.md`.

## 6. Initial rule-extraction priority

Do not encode all sources at once.

### Priority A — Switching vertical slice

1. `RU-SWITCH-757` current 2026 edition;
2. applicable sections of `RU-PTEES-1070` and/or `RU-PTEEP-811` according to target object role;
3. applicable `RU-OT-903N` requirements;
4. selected site instruction overlay;
5. selected manufacturer/equipment constraints.

### Priority B — Scheme/graphics vertical slice

1. `GOST-2.701-2008`;
2. `GOST-2.702-2011`;
3. exact current UGO/line standards for the first equipment families;
4. optional approved enterprise graphical profile only where it does not conflict with the selected required baseline.

## 7. Registry update policy

Every entry has `last_verified_at` and must be rechecked before release if:

- significant time passed;
- an amendment is known/published;
- source status changed;
- affected module is being released into operational use.

A changed source creates a review task; production rules are not silently rewritten.

## 8. Known limitation of this initial snapshot

Foundation has verified the identity/current-edition chain of the highest-priority sources, but has **not** yet performed clause-by-clause rule extraction or legal applicability opinion for every project type.

That work belongs to Compliance Core implementation and domain review, with official source text preserved/referenced in the controlled normative corpus.
