# Agent Rules — ElectroScheme Studio

## Main objective

Work economically, stably, and predictably.

Do not spend tokens on obvious explanations, full file dumps, broad project reviews, repeated context, or speculative architecture changes.

Product name: **ElectroScheme Studio**  
Repository/folder name: `electroscheme-studio`  
Project root: `G:\electroscheme-studio`  
Patch folder: `C:\1`  
Stack: Python + FastAPI backend, Vue 3 + Vite + TypeScript frontend.

---

## 1. Token economy

Required rules:

1. Do not print full files in chat unless explicitly requested.
2. Do not retell known project context.
3. Do not inspect the whole repository when 2–5 files are enough.
4. Do not propose multiple solutions when one safe solution is needed.
5. Do not rewrite whole files when a small patch is enough.
6. Do not run heavy commands without a reason.
7. Do not introduce new libraries without a clear need.
8. Do not explain every low-level operation.
9. Do not generate long plans for simple tasks.
10. Prefer compact status reports.

Preferred response format:

```text
Done:
- ...

Checks:
- ...

Status:
- OK / WARNING / FAILED

Next:
- ...
```

---

## 2. Patch workflow

All repository changes must be applied through numbered PowerShell patches.

Patch location:

```text
C:\1
```

Project location:

```text
G:\electroscheme-studio
```

Patch naming:

```text
patch_XXX_short_description.ps1
patch_XXX_repairN_short_description.ps1
```

Examples:

```text
patch_004_add_agent_token_economy_rules.ps1
patch_004_repair1_utf8_nobom.ps1
```

---

## 3. Logging standard

Each patch must write exactly one main log:

```text
G:\electroscheme-studio\_logs\<patch_name>_<timestamp>.transcript.log
```

Use:

```powershell
Start-Transcript -Path $TranscriptPath -Force
```

Always close it:

```powershell
Stop-Transcript
```

Do not create a second summary `.log` unless a machine-readable log is explicitly required.

A small patch marker is allowed:

```text
G:\electroscheme-studio\_patches\<patch_name>.applied.json
```

The marker must stay small: patch name, timestamp, actions, warnings, errors, status.

---

## 4. Windows PowerShell 5.1 compatibility

The user's environment is Windows PowerShell 5.1.

Required rules:

1. Do not use PowerShell 7-only syntax.
2. Do not use `Set-Content -Encoding UTF8` for source/config files.
3. In Windows PowerShell 5.1, `-Encoding UTF8` writes UTF-8 with BOM.
4. JSON, TS, Vue, CSS, HTML, Python, TOML, Markdown and script-generated source files must be written as UTF-8 without BOM.

Use this helper:

```powershell
function Write-Utf8NoBomFile {
    param(
        [string]$Path,
        [string]$Content
    )

    $parent = Split-Path $Path -Parent
    if (-not [string]::IsNullOrWhiteSpace($parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}
```

Expected failures must not crash the patch.

Bad:

```powershell
git remote get-url origin
```

Good:

```powershell
git remote
```

Then parse whether `origin` exists.

---

## 5. External command execution

For important external commands, capture stdout/stderr and print them into the transcript.

Use `Start-Process` with redirected output when output matters.

Do not pipe native command stderr into PowerShell when warnings may become terminating errors.

Known case:

- `FastAPI TestClient` / Starlette warnings can become a PowerShell failure when `$ErrorActionPreference = "Stop"`.

For backend bootstrap smoke-tests, prefer direct function checks unless a real HTTP test is specifically needed.

---

## 6. Git and GitHub

Branch:

```text
main
```

Repository:

```text
https://github.com/genrudko/electroscheme-studio
```

Rules:

1. Commit only after checks pass.
2. Keep commits small and logical.
3. Commit message must be short and descriptive.
4. Do not push if build/smoke checks fail.
5. Use HTTPS origin if SSH host key verification is not configured.
6. If `.github/workflows/*.yml` is committed, GitHub CLI token needs `workflow` scope.

Useful command:

```powershell
gh auth refresh -h github.com -s workflow
```

---

## 7. Minimum checks before commit

Backend dependency check:

```powershell
G:\electroscheme-studio\backend\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Backend smoke-test:

```python
from app.main import health, demo_project

assert health()["status"] == "ok"
assert demo_project()["version"] == "0.1"
```

Frontend dependency/build check:

```powershell
cd G:\electroscheme-studio\frontend
npm install
npm run build
```

TypeScript typecheck exists as a separate command:

```powershell
npm run typecheck
```

Do not block early MVP bootstrap on strict typecheck if production Vite build passes.

---

## 8. Scope control

Before editing, identify the minimal file set.

Forbidden without explicit request:

1. Change project name.
2. Change stack.
3. Add DWG/CAD/cloud/multi-user features.
4. Rename public entities broadly.
5. Reformat unrelated files.
6. Add large dependencies.
7. Delete existing docs or source files.
8. Replace architecture without approval.

Allowed:

1. Fix clear bugs.
2. Add small smoke-tests.
3. Improve patch infrastructure.
4. Fix UTF-8 BOM issues.
5. Add documentation that prevents repeated mistakes.
6. Update agent instructions and workflow docs.

---

## 9. Product boundaries

ElectroScheme Studio is a local-first WebUI editor for interactive electrical schemes.

Early-stage non-goals:

1. DWG import/export.
2. Full CAD replacement.
3. Cloud sync.
4. Multi-user mode.
5. PDF/image recognition.
6. Large automatic routing engine.
7. Full ГОСТ/СТО compliance claims.

Early-stage goals:

1. Project model.
2. SVG renderer.
3. Element selection.
4. Properties panel.
5. Terminals and connections.
6. Scheme validation.
7. SVG/PDF/PNG/JPEG export later.
8. ГОСТ-oriented symbol library later.

---

## 10. Repair patches

If a patch fails:

1. Create a minimal repair patch.
2. State the root cause in the patch header.
3. Do not repeat a large patch unless required.
4. Run the same check that failed previously.
5. Improve logging first if the error was hidden.
6. Keep repair patches small and focused.

---

## 11. Dependency discipline

Backend:

1. Add dependencies only when needed.
2. Keep `requirements.txt` and `pyproject.toml` aligned.
3. Avoid unnecessary dev dependencies.

Frontend:

1. Do not add UI frameworks yet.
2. Do not add router before multiple pages exist.
3. Do not add state manager before it is needed.
4. Do not add test framework before MVP stabilizes.
5. Keep JSON files UTF-8 without BOM.

---

## 12. Stability priorities

Priority order:

1. Build passes.
2. Smoke-test passes.
3. Git status is understandable.
4. One transcript log exists.
5. Changed files are UTF-8 without BOM.
6. Commit is small.
7. Explanation is short.

Do not chase perfect architecture at the cost of breaking bootstrap.

---

## 13. User-facing style

After work, report briefly:

```text
Готово.

Сделано:
- ...

Проверки:
- ...

Статус:
- OK / WARNING / FAILED

Лог:
- ...
```

Do not paste full logs, full files, or long theoretical explanations unless explicitly requested.