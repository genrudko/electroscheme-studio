# NPM security finding classification — DESKTOP-PLATFORM-AND-CORE-SPIKE-001

Date: 2026-08-06

## Finding before repair

The bootstrap audit for the exact dependency intent containing `vite@7.1.1` reported one direct high-severity finding.

- package: `vite`;
- affected direct version: `7.1.1`;
- dependency chain: root spike package -> direct `vite`;
- package class: development/build dependency used only by the architecture spike;
- production dependency audit: no affected packaged application dependency;
- affected aggregate audit range: `7.0.0 - 7.3.3`;
- non-major patched version offered by npm audit: `7.3.6`;
- relevant high advisories:
  - `GHSA-v2wj-q39q-566r` — `server.fs.deny` bypass with queries;
  - `GHSA-p9ff-h696-f583` — arbitrary file read through the Vite development-server WebSocket;
  - `GHSA-fx2h-pf6j-xcff` — Windows alternate-path deny bypass.

The finding applies to Vite development-server and file-serving boundaries. The spike CI uses Vite for a production static build; Vite and its Node dependency tree are not copied into either packaged Electron input or the Tauri portable package. That limits packaged-runtime exposure but does not justify retaining a known vulnerable build tool.

## Decision

`UPDATE`.

The exact direct pin was changed from `vite@7.1.1` to `vite@7.3.6`. No `npm audit fix --force`, broad dependency refresh or major-version upgrade was used.

The alternatives were rejected as follows:

- `ISOLATE` was unnecessary because a patched compatible version exists and the package is already absent from runtime artifacts;
- `ACCEPT_TEMPORARILY` was unjustified because the update is non-major and preserves the spike contract;
- `REMOVE` was not appropriate because the shared Vue renderer still needs a deterministic production bundler during this spike.

## Evidence after repair

- committed npm lock SHA-256: `0bd9554bba53000a3d01247979e0b1e2e84c5493b7331fe4e418b59d1d9099eb`;
- committed Cargo lock SHA-256: `c58ede42a2c003b66d03e17a14af53247929a29f0d8871d5a8f2eb98a8b50cb3`;
- bootstrap audit after the exact update: zero info/low/moderate/high/critical findings;
- final candidate workflow requires both all-dependencies and production-only audit success;
- final candidate workflow installs with `npm ci --ignore-scripts`;
- build jobs fail if the committed npm or Cargo lock changes.

## Packaged-candidate impact

- Electron package: Vite is not copied into `electron/package-input`; only compiled renderer assets, Electron runtime, controlled fixtures and the Python tool boundary are packaged.
- Tauri package: Vite is absent; the package contains compiled frontend assets, the Rust host executable, controlled fixtures and the Python tool boundary.
- Build environment: the repaired exact Vite version remains part of the trusted build surface and is therefore audited and locked.

## Acceptance interpretation

A zero audit result is necessary evidence for this exact lock projection, not a general claim that npm dependencies can never acquire future advisories. Subsequent work items must rerun the locked audit and classify new findings rather than silently refreshing the lock or treating spike-only dependencies as irrelevant.
