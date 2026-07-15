# Testing Guide

Local normative commands:

```bash
scripts/test.sh --static-only
scripts/test.sh
latexmk main.tex
```

When TeX Live is installed, `scripts/test.sh` delegates to the repository test runner and compiles primary smoke documents. Static validation also checks configuration, palettes, bibliography fields and CI job shape.

## Overleaf doctor and modular architecture checks

Run these checks locally before opening a pull request:

```bash
python3 tools/overleaf_doctor.py check
python3 -m unittest tests/test_overleaf_doctor.py
./tests/run-tests.sh --static-only
./scripts/test.sh --compile
```

`./scripts/test.sh --compile` compiles with `latexmk` when TeX Live is installed and otherwise reports that static validation completed. A PDF only counts as successful when `latexmk` exits with code 0.
