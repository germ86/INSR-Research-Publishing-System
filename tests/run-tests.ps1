$ErrorActionPreference = 'Stop'
python tools/validate_project.py
python tools/validate_bibliography.py references.bib
python tools/validate_palette.py
Get-ChildItem examples/*.tex | ForEach-Object { Write-Host "fixture: $($_.FullName)" }
if (Get-Command latexmk -ErrorAction SilentlyContinue) { latexmk main.tex } else { Write-Host 'latexmk not installed; static tests completed' }
