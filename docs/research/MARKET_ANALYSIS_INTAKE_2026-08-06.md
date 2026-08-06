# Market Analysis Intake — 2026-08-06

Status: accepted strategic input, detailed hands-on benchmarking pending  
Program phase: `P1_MARKET_AND_WORKFLOW_BASELINE`  
Source: owner-provided comparative market analysis dated 2026-08-06, followed by coordinator verification of load-bearing claims against official or primary product/normative sources.

## 1. Purpose and evidence boundary

This document converts the received market analysis into product decisions for ElectroScheme Studio.

It is not:

- a substitute for hands-on trials of competitor products;
- a verified feature-by-feature procurement comparison;
- evidence that every vendor claim is technically complete;
- permission to copy a competitor architecture or interface;
- a declaration that ElectroScheme Studio must implement every listed capability.

Competitor ratings remain analytical until supported by reproducible scenarios, screenshots, trial builds, manuals or owner experience.

## 2. Confirmed market structure

The market is fragmented into different product classes:

1. power-system modeling and calculation platforms;
2. ECAD/documentation systems;
3. substation/data-centric engineering platforms;
4. operational/dispatcher scheme systems;
5. building electrical/BIM systems;
6. general-purpose diagram editors.

No reviewed product is treated as a complete direct template for ElectroScheme Studio.

The strategic gap is the combination of:

- low-friction free layout close to a general diagram editor;
- semantic electrical equipment objects;
- explicit ports and topology;
- switching states and energized/de-energized interpretation;
- Russian normal/temporary-normal scheme semantics;
- controlled document output and lifecycle;
- Windows and Linux local-first delivery.

This gap is a product hypothesis to validate through user workflows and competitor trials, not a claim that no niche product exists anywhere.

## 3. Competitive reference roles

### 3.1 Must study deeply

| Product | Reference role for ElectroScheme Studio | What not to copy blindly |
|---|---|---|
| Модус | operational schemes, topology, connectors, states, CIM-oriented data preparation | legacy UX, proprietary ecosystem coupling, SCADA/trainer complexity in MVP |
| ETAP | intelligent one-line model, continuity, energized/de-energized display, switching scenarios | calculation-suite scope and corporate weight |
| AUCOTEC Engineering Base PTD | one data model across primary, secondary, protection and control | enterprise database/process complexity |
| EPLAN Electric P8 | documentation automation, references, reports, object data | full ECAD breadth and cabinet/manufacturing scope |
| Microsoft Visio | interaction speed, flexible layout, reusable stencils, low learning barrier | drawing-first semantics and weak electrical integrity |
| Model Studio CS / MS Electrical Schemes | Russian project-documentation context, equipment databases, CAD/BIM integration | heavy CAD/BIM platform dependency |
| EnergyCS | Russian calculation methods and graph/model linkage | calculation-first architecture in the first release |
| Автограф and АСМОграф | Russian Visio-replacement workflows, large-scheme editing, Visio interchange, Windows/Linux expectations | general-purpose diagramming scope and unproven electrical semantics |

### 3.2 Study selected mechanics

- Zuken E3.series: data-centric connectivity and multiple representations;
- SEE Electrical: lower-friction ECAD workflow and one-/multi-line support;
- DIgSILENT PowerFactory: scenarios, variants and network data handling;
- WSCAD: documentation automation and rule assistance;
- AutoCAD Electrical: DWG ecosystem, symbol attributes and reports;
- КОМПАС-Электрик: Russian ESKD document sets and component databases;
- Bentley OpenUtilities Substation: connection between electrical and physical substation models;
- QElectroTech: open project/library formats and cross-platform lightweight editing.

## 4. Accepted product positioning

ElectroScheme Studio is:

> a modern Windows/Linux object editor for design and operational power-engineering schemes, combining low-friction drawing with equipment semantics, electrical topology, switching states and evidence-based Russian presentation profiles.

It is not positioned as:

- a replacement for every EPLAN capability;
- a Russian ETAP or PowerFactory;
- a SCADA/EMS/ADMS;
- a universal CAD;
- a general-purpose Visio clone;
- a full calculation suite.

Competitive superiority is scenario-based, not based on total feature count.

## 5. Target document families

The long-term product model must support:

- main electrical connection diagrams;
- normal electrical connection diagrams;
- temporary normal electrical connection diagrams;
- one-line diagrams;
- three-line/phase-explicit diagrams;
- operational scheme views and state snapshots;
- auxiliary-power schemes;
- related simplified protection, control and DC schemes where the common equipment/topology model is applicable.

These families must not all enter the first MVP simultaneously.

## 6. First vertical product focus

The first complete vertical slice remains:

> creation, editing, validation, version-safe persistence and normative output of a realistic one-line normal electrical connection diagram.

The MVP model must already preserve extension points for:

- temporary-normal variants;
- operational state snapshots;
- phase-explicit representations;
- multiple diagram representations of one equipment identity;
- future equipment registers and document revisions.

The MVP must not implement a fake generic abstraction merely to claim future support. Extension points require concrete stable identity, representation and state contracts.

## 7. Must match, must exceed, not needed now

### 7.1 Must match

- fast placement, selection, alignment, copy/paste and navigation expected from Visio-class editors;
- reusable libraries and fragments;
- predictable large-sheet editing and printing;
- properties, search and object identification;
- robust save/open and undo/redo;
- Windows and Linux desktop usability.

### 7.2 Must exceed in the target workflow

- semantic equipment families rather than decorative shapes;
- explicit ports/terminals and electrical connections;
- distinction between visual crossing, junction and electrical connection;
- topology preservation during editing;
- switching states and state-dependent presentation;
- normal-position semantics and diagnostics;
- Russian UGO/profile consistency;
- traceable symbol and normative provenance;
- deterministic project format and migrations;
- diagnostics that navigate to the affected object;
- repeatable PDF/SVG/print output.

### 7.3 Not required in the first product release

- load flow, short-circuit, dynamics, harmonics or protection coordination engines;
- real-time SCADA control and telemetry protocols;
- universal DWG editing;
- automatic conversion between arbitrary one-line, three-line and secondary schemes;
- cloud collaboration and simultaneous editing;
- full BIM/3D substation design;
- full CIM as the internal editing model.

## 8. One equipment identity, multiple representations

The market direction supports a distinction between:

- an engineering equipment identity;
- one or more diagram representations of that equipment;
- document-specific layout and labels;
- shared and representation-specific properties.

This is a post-MVP architecture direction, but the canonical model must not make it impossible.

Automatic generation of every representation is explicitly not assumed. A realistic path is:

1. one stable equipment identity;
2. a representation created from an accepted template;
3. semi-automatic initialization from shared equipment data;
4. user-controlled layout;
5. consistency diagnostics between representations.

## 9. VSDX/VSSX decision

The market analysis confirms the value of semantic symbols, but does not make Visio masters the product's semantic authority.

VSDX/VSSX and ShapeSheet may provide:

- source geometry;
- dimensions;
- connection points;
- formulas and transformation hints;
- existing user libraries and migration data.

They do not automatically prove:

- correct electrical family semantics;
- valid port roles;
- state behavior;
- compliance with a specific GOST/STO revision;
- safe runtime behavior;
- suitability for every representation.

The accepted pipeline remains:

```text
source master
→ extraction
→ normalized candidate
→ engineering semantic mapping
→ normative/profile review
→ automated tests
→ visual/engineering acceptance
→ versioned SymbolDefinition
```

## 10. GOST and Russian information-model implications

### 10.1 Normal schemes

`ГОСТ Р 56303-2014` with Amendment No. 1 defines normal and temporary-normal schemes, modular-grid rules, UGO use and dimensions, line rules, text and title-block requirements. Amendment No. 2 entered public discussion on 29 May 2026.

The product therefore requires versioned compliance profiles rather than hard-coded styling.

### 10.2 Ministry order

Ministry of Energy Order No. 854 of 16 August 2019 is part of the regulatory workflow around graphical execution and coordination of normal/temporary-normal schemes. Legal applicability and current interaction with later amendments must be maintained in a separate normative register.

### 10.3 CIM/information exchange

`ГОСТ Р 58651.9-2023` defines an information-model profile for diagrams and automated exchange, including concepts such as `Diagram`, `DiagramObject`, points and links to equipment/terminals.

Architectural decision:

- CIM-compatible concepts should influence identifiers, terminals, representation separation and exchange adapters;
- CIM is not automatically the internal UI/document format;
- a future adapter must map canonical product data to the applicable profile with explicit loss/coverage diagnostics.

## 11. Strategic risks identified

1. Expanding the first release to every scheme type.
2. Confusing a visually correct symbol with a semantic equipment object.
3. Treating VSDX conversion success as engineering acceptance.
4. Building calculation or SCADA scope before the editor and topology are reliable.
5. Copying enterprise platforms until the product loses the low-friction advantage.
6. Copying Visio interaction patterns without eliminating drawing-first defects.
7. Claiming GOST compliance without revision-specific evidence.
8. Designing one-line and three-line documents as unrelated files with duplicated equipment identities.
9. Making CIM the internal editing model before product workflows are stable.
10. Measuring success by symbol count rather than completed engineering tasks.

## 12. Primary verification sources

Normative and industry sources used for load-bearing verification:

- ГОСТ Р 56303-2014 with Amendment No. 1: https://docs.cntd.ru/document/1200115865
- СО ЕЭС notice on public discussion of Amendment No. 2, 29.05.2026: https://www.so-ups.ru/news/press/info-release-view/news/30368/
- Official publication listing for Ministry of Energy Order No. 854: https://publication.pravo.gov.ru/documents/block/foiv298?index=10
- ГОСТ Р 58651.9-2023: https://docs.cntd.ru/document/1200196021
- Модус graphical editor: https://swman.ru/index.php/графический-редактор
- Модус data engineering/CIM: https://swman.ru/index.php/технологии/data-engineering
- ETAP intelligent single-line diagram: https://etap.com/product/electrical-single-line
- ETAP switching sequence management: https://etap.com/de/product/switching-sequence-management
- AUCOTEC Engineering Base PTD: https://www.aucotec.com/en/products/engineering-base-plants/power-transmission-and-distribution
- Автограф official product site: https://avtograf.tech/
- АСМОграф official product site: https://asmograf.ru/

## 13. Required follow-up in P1

`P1_MARKET_AND_WORKFLOW_BASELINE` must convert this intake into evidence-backed scenarios:

1. define 8–12 real user workflows;
2. perform hands-on or manual/video evidence review for the priority competitors;
3. record task time, action count, errors and limitations;
4. build `must_match / must_exceed / defer / reject` decisions;
5. identify the exact MVP reference scheme and document profile;
6. update acceptance scenarios without broadening the first release into a universal ECAD.
