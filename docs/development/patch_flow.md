# Patch Flow

Working directories:

```text
Project root: G:\electroscheme-studio
Patch folder: C:\1
```

Apply patches from PowerShell:

```powershell
cd C:\1
.\patch_XXX_name.ps1
```

## Logging standard

Each patch writes one main log only:

```text
G:\electroscheme-studio\_logs\<patch_name>_<timestamp>.transcript.log
```

The transcript log is the only file the user normally sends back for analysis.

A small patch marker may be written to:

```text
G:\electroscheme-studio\_patches\<patch_name>.applied.json
```

Do not create a second summary `.log` unless a machine-readable summary is explicitly needed.

## Patch status values

- `OK` — patch applied successfully.
- `WARNING` — patch applied, but follow-up is needed.
- `FAILED` — patch did not complete.

## Encoding rule

All generated source/config/docs files must be UTF-8 without BOM.

In Windows PowerShell 5.1, do not use:

```powershell
Set-Content -Encoding UTF8
```

Use .NET instead:

```powershell
$encoding = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($Path, $Content, $encoding)
```