# Patch 040 repair1 — remove source-only port badge wording and resume

Patch 040 failed because smoke found the literal text:

```text
1 порт.
```

It was not rendered as a card badge anymore. It remained in a code comment that described the UI policy.

Repair1 removes that comment wording and resumes patch 040 gates.
