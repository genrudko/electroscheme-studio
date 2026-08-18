# UI Core Architecture

Статус: canonical foundation document

## 1. Why UI Core is architecture

The product must not become a technically correct engineering engine hidden behind an archaic or exhausting interface.

UI Core is a first-class shared subsystem with the same design seriousness as Domain Core.

Target UX:

> modern, dense, professional desktop engineering UI for long work sessions, large projects, keyboard+mouse and multiple monitors.

Reject both extremes:

- legacy/MS-DOS/early-Win32-looking usability and visual hierarchy;
- sparse mobile/tablet composition with excessive whitespace and oversized controls.

## 2. UI Core ownership

UI Core owns reusable interaction and presentation infrastructure:

```text
UI Core
├── Application Shell
├── Workspace / Documents
├── Multi-window
├── Design System / Themes
├── Commands / Shortcuts
├── Selection infrastructure
├── Property Inspector framework
├── Tree/List/Table infrastructure
├── Search / Command Palette
├── Dialogs / Notifications
├── Status / Diagnostics surfaces
├── Canvas framework primitives
├── Clipboard / Drag-drop UX contracts
├── HiDPI / mixed-DPI handling
├── Accessibility / keyboard focus
└── UI Gallery / visual test fixtures
```

UI Core does **not** own switching rules, NPT semantics or equipment-specific validation.

## 3. Application shell

The shell must support:

- project/workspace identity;
- main navigation without hiding working area behind unnecessary chrome;
- document tabs;
- split document regions where useful;
- detachable documents/windows;
- persistent tool panels;
- status/diagnostics;
- global search/command access;
- module-contributed views/actions through explicit contracts.

Avoid copying Office Ribbon or IDE docking blindly. Use them only as reference patterns where they reduce real task cost.

## 4. Workspace and multi-monitor

Multi-monitor is a first-class acceptance scenario.

Expected use:

```text
Monitor 1 — main electrical scheme
Monitor 2 — equipment/properties/search
Monitor 3 — switching/TBP sequence
Monitor 4 — table/NPT/diagnostics/secondary view
```

Workspace model must persist:

- open documents/views;
- window positions/sizes;
- monitor assignment with fallback when monitor topology changes;
- splits/tabs;
- visible panels;
- panel sizing/order;
- selected project context where safe.

A corrupt/stale workspace must not block project opening; provide safe/default recovery.

## 5. Design system

The design system must define at minimum:

- typography scale;
- spacing scale;
- control density;
- borders/elevation/separators;
- semantic colors;
- focus/hover/pressed/selected/disabled/error/warning states;
- icons/pictograms;
- table/tree row density;
- panel headers;
- dialogs;
- dark/light themes if retained;
- engineering status colors independent from decorative theme colors.

Do not encode important engineering meaning only by color.

## 6. UI Gallery

Create early and keep continuously runnable.

Gallery contains all shared controls and states without requiring a full project/runtime:

```text
Buttons / Toolbar
Text / Numeric / Enum editors
Property rows/groups
Tabs / Document headers
Trees / virtual lists
Virtual tables
Search results
Dialogs
Notifications
Validation messages
Context menus
Command palette
Canvas selection handles
Symbol state samples
Empty/loading/error states
```

Purpose:

- rapid visual iteration;
- screenshot regression;
- theme/HiDPI checks;
- agent/developer inspection;
- prevent every module from inventing controls.

## 7. Property Inspector

Shared Inspector framework must support typed descriptors/editors without making UI Core know business semantics.

Example registration:

```text
Domain property descriptor
  → editor kind / units / validation / help / read-only state
```

Modules may contribute specialized editors:

- equipment state/property editor;
- signal/KKS chooser;
- NPT typed `scdCommand` editor;
- compliance/source selector.

Inspector needs:

- single and multi-selection;
- mixed-value state;
- validation feedback;
- undo/redo command integration;
- searchable/filterable property groups;
- keyboard-friendly editing.

## 8. Trees and tables

Electrical projects can contain tens/hundreds of thousands of listable entities. UI must use virtualization and incremental loading/filtering where appropriate.

Requirements:

- stable selection;
- fast sort/filter/search;
- keyboard navigation;
- column presets;
- copy/export selected data;
- clear validation/status indicators;
- no full DOM/control creation per row if framework benchmark says it does not scale.

Platform Spike includes a 100k-row representative table.

## 9. Command system

Actions should be addressable through a shared command registry:

```text
command ID
label
icon
shortcut
availability/canExecute
execution
context
```

This allows one action to appear consistently in toolbar/context menu/command palette/shortcut without duplicated enablement logic.

Shortcuts must be discoverable and configurable only when product evidence justifies customization complexity.

## 10. Canvas framework

UI Core owns shared viewport interaction infrastructure, while Scheme/NPT modules own rendering semantics.

Shared concerns may include:

- viewport transform;
- zoom/pan;
- spatial hit-testing contract;
- selection model;
- marquee selection;
- pointer capture;
- snapping/guides;
- overlays/handles;
- keyboard navigation;
- viewport diagnostics/performance instrumentation.

Do not implement one heavyweight desktop control per visual primitive without benchmark evidence.

## 11. Scheme editing UX principles

High-value interactions should minimize mode confusion.

Examples:

- selection is predictable and reversible;
- reconnecting an electrical terminal is visually and semantically distinct from moving routed line geometry;
- ambiguous/destructive operations show clear effect before commit;
- auto-layout never silently destroys locked/manual placement;
- validation messages locate the affected equipment/view/rule;
- selection/property edits preserve context when switching views.

## 12. Error and uncertainty UX

Differentiate:

```text
INFO
WARNING
ERROR
BLOCKED
UNKNOWN / REQUIRES_CONFIRMATION
```

In engineering/switching contexts, uncertainty must remain visible rather than being normalized into a normal-looking state.

Messages should answer:

- what happened;
- what entity/rule/source is involved;
- whether work can continue;
- what user action resolves it.

## 13. UX budgets

Budgets are product requirements, refined by usability measurement.

Initial qualitative targets:

- common project navigation/search should be immediate and keyboard-accessible;
- property editing must not require modal dialog chains;
- generating a repetitive 84-WTG table/scheme structure should be a data-driven operation, not days of row-by-row editing;
- restoring a normal multi-monitor workspace should not require manual rearrangement every launch;
- importing data should surface all ambiguity in one review workflow rather than interrupting with dozens of sequential dialogs.

## 14. Developer UX budget

UI Core must also optimize iteration:

- shared component can be run in Gallery without full product;
- visual snapshot available on headless runner where framework permits;
- small UI patch produces targeted preview quickly;
- visual acceptance precedes unrelated full-system gates;
- app-wide theme/layout changes have centralized tokens/components, not broad override stacks.

## 15. HiDPI and mixed DPI

Acceptance must cover:

- 100/125/150/200% scale classes where supported;
- moving windows between monitors with different scale factors;
- crisp vector scheme rendering;
- stable text/control sizes;
- no coordinate mismatch between rendered canvas and hit-testing.

## 16. Accessibility

Professional desktop software still needs:

- visible keyboard focus;
- logical tab order;
- shortcuts not colliding unpredictably;
- readable contrast;
- non-color-only status cues;
- scalable text/control metrics within practical engineering density.

## 17. Visual acceptance contract

A UI change is not accepted because it compiles.

Depending on scope, evidence may include:

- UI Gallery screenshot;
- targeted headless screenshot;
- interaction test;
- owner preview build;
- mixed-DPI/multi-window manual check.

For a small UI-only patch, do not block first visual review on full NPT corpus/topology/switching suites.

## 18. Framework independence

This document is framework-neutral. Avalonia and Qt must each prove they can implement these contracts during Platform Spike.

Do not distort UI requirements merely to fit a preferred framework.
