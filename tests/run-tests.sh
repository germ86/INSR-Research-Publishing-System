#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Resolve INSR packages through the canonical root-level shims. Keeping the
# nested implementation directory out of the package search root prevents
# package-name mismatch warnings in local and Overleaf-equivalent builds.
export TEXINPUTS=".:./examples//:${TEXINPUTS:-}"
export BIBINPUTS=".//:${BIBINPUTS:-}"

static_only=false
require_tex=false
for argument in "$@"; do
  case "$argument" in
    --static-only) static_only=true ;;
    --require-tex) require_tex=true ;;
    --help|-h)
      echo "Usage: tests/run-tests.sh [--static-only] [--require-tex]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $argument" >&2
      echo "Usage: tests/run-tests.sh [--static-only] [--require-tex]" >&2
      exit 2
      ;;
  esac
done

if [[ "$static_only" == true && "$require_tex" == true ]]; then
  echo "--static-only and --require-tex cannot be combined" >&2
  exit 2
fi

python3 tools/overleaf_doctor.py check
python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py
python3 tools/insr_integrity.py
python3 -m unittest discover -s tests

mapfile -t documents < <(python3 tools/overleaf_doctor.py list-entrypoints --plain)
documents+=(tests/fixtures/position-paper-editorial-content-unit.tex)
documents+=(tests/fixtures/slides-editorial-content-unit.tex)
documents+=(tests/fixtures/document-type-slides-overrides-submission.tex)
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

missing_tools=()
for tool in latexmk lualatex biber; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    missing_tools+=("$tool")
  fi
done

if (( ${#missing_tools[@]} > 0 )); then
  if [[ "$require_tex" == true ]]; then
    printf 'required TeX tool(s) missing:' >&2
    printf ' %s' "${missing_tools[@]}" >&2
    printf '\n' >&2
    exit 1
  fi
  printf 'TeX compilation skipped; missing tool(s):'
  printf ' %s' "${missing_tools[@]}"
  printf '\n'
  echo "static tests completed"
  exit 0
fi

for document in "${documents[@]}"; do
  output_dir="build/compile/${document%.*}"
  mkdir -p "$output_dir"
  latexmk -C -outdir="$output_dir" "$document"
  latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir="$output_dir" "$document"
  log_file="$output_dir/$(basename "${document%.*}").log"
  if [[ -f "$log_file" ]]; then
    python3 tools/check_latex_log.py "$log_file"
  fi
done
