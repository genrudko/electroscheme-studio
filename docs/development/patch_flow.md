# Patch Flow

Working directories:

`	ext
Project root: G:\electroscheme-studio
Patch folder: C:\1
`

Apply patches from PowerShell:

`powershell
cd C:\1
.\patch_XXX_name.ps1
`

After each patch, send:

- full PowerShell output;
- generated log from G:\electroscheme-studio\_logs.

Patch status values:

- OK — patch applied successfully;
- WARNING — patch applied, but follow-up is needed;
- FAILED — patch did not complete.
