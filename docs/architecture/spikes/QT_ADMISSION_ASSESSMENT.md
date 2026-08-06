# Qt admission assessment

Status: `NOT_ADMITTED_TO_FULL_SPIKE`  
Work item: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`  
Date: 2026-08-06

## Admission question

Qt was not automatically entitled to a third full implementation. It could enter only if a material advantage justified one of two costly paths:

1. abandon Vue/TypeScript/SVG and build a new native scene/editor stack; or
2. retain the web renderer through Qt WebEngine/WebChannel and add another host/binding/packaging layer.

## Assessment

| Criterion | Native Qt scene | Qt WebEngine/WebChannel | Admission consequence |
|---|---|---|---|
| Reuse of the accepted shared Vue/TypeScript/SVG scenario | No | Partial | Native path discards the already proven editor/rendering layer; WebEngine path duplicates Electron's Chromium-host role with extra bindings. |
| Canonical TypeScript core | Requires bindings or rewrite | Retainable through JS | Neither path improves single writable ownership compared with the shared TypeScript core proven in both mandatory candidates. |
| Windows/Linux rendering parity | New renderer must be proven independently | Chromium version/distribution becomes Qt packaging concern | No demonstrated advantage over Electron's bundled engine or Tauri's OS webview trade-off. |
| Python VSDX/VSSX tooling | Local process possible | Local process possible | No differentiating advantage. |
| Native dialogs/clipboard/drag/drop/printing | Strong native APIs | Strong native APIs plus WebChannel bridge | Advantage exists, but adapters already work without making the domain/editor core host-specific. It does not compensate for migration cost. |
| Runtime languages | C++/QML or Python bindings plus tooling | C++/Python plus TypeScript plus Python tooling | Equal or larger maintenance surface. |
| Packaging/test infrastructure | Separate Qt deployment and plugin matrix | Qt + WebEngine deployment matrix | A third independent infrastructure would be required before product work. |
| Prototype migration cost | Very high | High | Conflicts with the requirement to preserve useful Vue/TypeScript/SVG knowledge without inheriting old architecture. |
| Demonstrated blocker in Tauri/Electron | None in the controlled scenario | None | Admission condition is absent. |

## Strongest argument for Qt

A native Qt scene could become attractive if later evidence shows that the accepted SVG/editor architecture cannot meet large-scheme interaction, print fidelity, accessibility or platform integration requirements. Qt also provides mature native widgets and printing APIs.

That is not current evidence. It is a contingent future hypothesis. Admitting Qt now would confuse a possible future escape route with a proven present requirement.

## Decision

Qt is **not admitted** to a full executable candidate in this work item.

This is not a permanent technology ban. Reconsideration requires a new evidence-backed architecture decision showing at least one material blocker that cannot be resolved within the selected host and shared renderer, together with a quantified migration benefit exceeding the cost of:

- replacing or embedding Vue/TypeScript/SVG;
- introducing bindings and a new runtime language surface;
- creating separate Windows/Linux packaging, signing and test infrastructure;
- re-proving editor interactions, output and Visio tooling boundaries.

No such blocker or advantage was demonstrated in `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`.
