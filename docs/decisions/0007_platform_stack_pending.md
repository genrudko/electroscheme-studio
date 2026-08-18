# ADR 0007 — Desktop Platform Stack

Status: **PENDING EVIDENCE**  
Date opened: 2026-08-18

## Context

The previous Tauri/Vue/TypeScript/SVG spike proved useful packaging/native-integration and Visio-path lessons, but the new unified scope requires a heavier professional desktop application: large engineering canvas, 100k-row data views, multi-window/multi-monitor workspace, rich properties/tables and strong headless/visual testing.

Owner direction requires a fresh comparison rather than inheriting Tauri as the final choice.

## Candidates admitted to final spike

1. C#/.NET + Avalonia.
2. C++ + Qt 6/QML (with custom scene/rendering implementation as needed).

## Decision rule

No candidate is accepted before the equivalent executable contract in `docs/development/PLATFORM_STACK_SPIKE.md` is completed and owner manual evidence is available.

The selected stack must balance:

- representative canvas performance;
- professional desktop UI/multi-monitor behavior;
- large table/tree performance;
- testing/visual CI;
- packaging;
- iteration speed;
- small-team maintainability;
- exact licensing/dependency obligations.

## Current disposition of Tauri spike

Draft PR #4 remains research evidence and must not be merged as the product architecture baseline solely because automated checks are green.

Useful assets may later be salvaged (Visio tooling methodology, benchmark/packaging lessons, controlled fixtures), independent from UI stack selection.

## Required output

The Platform Stack Spike replaces this PENDING document with/updates it to an ACCEPTED decision containing raw benchmark references and explicit rationale.
