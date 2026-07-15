#!/usr/bin/env bash
set -euo pipefail

static_only=false
if [[ "${1:-}" == "--static-only" ]]; then static_only=true; fi

python3 tools/overleaf_doctor.py check
python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py
python3 -m unittest tests/test_overleaf_doctor.py

mapfile -t supported_documents < <(python3 tools/overleaf_doctor.py list-entrypoints --plain)

for fixture in "${supported_documents[@]}"; do
  [[ -f "$fixture" ]] || { echo "missing supported fixture: $fixture" >&2; exit 1; }
  echo "fixture: $fixture"
done

if [[ "$static_only" == true ]]; then
  echo "static tests completed"
  exit 0
fi

if command -v latexmk >/dev/null 2>&1; then
  export TEXINPUTS=".//:./tex/latex/insr//:./examples//:${TEXINPUTS:-}"
  export BIBINPUTS=".//:${BIBINPUTS:-}"
  for document in "${supported_documents[@]}"; do
    echo "compiling: $document"
    latexmk -C "$document"
    latexmk -lualatex -interaction=nonstopmode -halt-on-error "$document"
  done
else
  echo "latexmk not installed; static tests completed"
fi
