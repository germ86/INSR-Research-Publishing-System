#!/usr/bin/env bash
set -euo pipefail

static_only=false
if [[ "${1:-}" == "--static-only" ]]; then
  static_only=true
fi

python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py

for fixture in examples/*.tex; do
  echo "fixture: $fixture"
done

if [[ "$static_only" == true ]]; then
  echo "static tests completed"
  exit 0
fi

if command -v latexmk >/dev/null 2>&1; then
  documents=(
    main.tex
    examples/paper-demo.tex
    examples/beamer-demo.tex
    examples/manual-demo.tex
  )
  for document in "${documents[@]}"; do
    latexmk "$document"
  done
else
  echo "latexmk not installed; static tests completed"
fi
