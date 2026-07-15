# Testing Guide

Local normative commands:

```bash
git diff --check
python3 tools/overleaf_doctor.py check
python3 tools/overleaf_doctor.py list-entrypoints
python3 tools/overleaf_doctor.py list-entrypoints --plain
python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py
python3 -m unittest tests/test_overleaf_doctor.py tests/test_config_static.py
./tests/run-tests.sh --static-only
```

When TeX Live is installed, run:

```bash
./tests/run-tests.sh
# or
./scripts/test.sh --compile
```

The compile runner obtains official entrypoints from `tools/overleaf_doctor.py list-entrypoints --plain`, verifies every path exists, cleans each document with `latexmk -C`, and compiles with LuaLaTeX plus `-halt-on-error`. A generated PDF only counts as successful when `latexmk` exits with code 0.

Static-only mode does not require TeX Live and is suitable for lightweight containers.
