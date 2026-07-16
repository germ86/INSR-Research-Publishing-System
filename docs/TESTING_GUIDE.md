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

## Publication stabilization checks

Run the full static suite before a release:

```bash
git diff --check
python3 tools/overleaf_doctor.py check
python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py
python3 -m unittest
./tests/run-tests.sh --static-only
```

If LuaLaTeX/latexmk are available, run `./tests/run-tests.sh` to compile all official entrypoints listed by the Overleaf doctor.

## External-package warning policy

Warnings from external TeX packages should be fixed when caused by INSR configuration. If a warning is unavoidable and originates solely from an external package or a missing local toolchain, document the package/tool, command, and reason in the release notes instead of suppressing it.

## v1.0.0-alpha readiness gates

A release candidate must verify native classes (`insr-paper`, `insr-book`, `insr-beamer`, `insr-poster`, `insr-handout`, `insr-manual`), bibliography, localization examples, themes, headers/footers and Overleaf diagnostics. Treat avoidable warnings as defects.
