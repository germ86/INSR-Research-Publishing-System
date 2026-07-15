#!/usr/bin/env bash
set -euo pipefail

static_only=false
if [[ "${1:-}" == "--static-only" ]]; then
  static_only=true
fi

python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py

supported_documents=(
  main.tex
  examples/paper-demo.tex
  examples/minimal-english-paper.tex
  examples/beamer-demo.tex
  examples/german-scientific-presentation.tex
  examples/manual-demo.tex
  doc/latex/insr/insr-latex-manual.tex
)

for fixture in "${supported_documents[@]}"; do
  if [[ ! -f "$fixture" ]]; then
    echo "missing supported fixture: $fixture" >&2
    exit 1
  fi
  echo "fixture: $fixture"
done

if [[ "$static_only" == true ]]; then
  echo "static tests completed"
  exit 0
fi

if command -v latexmk >/dev/null 2>&1; then
  for document in "${supported_documents[@]}"; do
    echo "compiling: $document"
    latexmk -lualatex -interaction=nonstopmode -halt-on-error "$document"
  done
else
  echo "latexmk not installed; static tests completed"
fi
