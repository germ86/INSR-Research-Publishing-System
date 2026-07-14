#!/usr/bin/env bash
set -euo pipefail
python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py
for fixture in examples/*.tex; do
  echo "fixture: $fixture"
done
if command -v latexmk >/dev/null 2>&1; then
  latexmk -C main.tex >/dev/null 2>&1 || true
  latexmk main.tex
else
  echo "latexmk not installed; static tests completed"
fi
