#!/usr/bin/env bash
set -euo pipefail

export TEXINPUTS=".//:./tex/latex/insr//:./examples//:${TEXINPUTS:-}"
export BIBINPUTS=".//:${BIBINPUTS:-}"

static_only=false
if [[ "${1:-}" == "--static-only" ]]; then
  static_only=true
fi

python3 tools/overleaf_doctor.py check
python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py
python3 -m unittest tests/test_overleaf_doctor.py tests/test_config_static.py

mapfile -t documents < <(python3 tools/overleaf_doctor.py list-entrypoints --plain)
documents+=(tests/fixtures/position-paper-editorial-content-unit.tex)
documents+=(tests/fixtures/slides-editorial-content-unit.tex)
for document in "${documents[@]}"; do
  if [[ ! -f "$document" ]]; then
    echo "missing entrypoint: $document" >&2
    exit 1
  fi
  echo "fixture: $document"
done

if [[ "$static_only" == true ]]; then
  echo "static tests completed"
  exit 0
fi

if command -v latexmk >/dev/null 2>&1; then
  for document in "${documents[@]}"; do
    latexmk -C "$document"
    latexmk -lualatex -interaction=nonstopmode -halt-on-error "$document"
  done
else
  echo "latexmk not installed; static tests completed"
fi
