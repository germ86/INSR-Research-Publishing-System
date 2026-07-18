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

## Continuous integration

`.github/workflows/ci.yml` is the required pull-request and `main` validation workflow and the authoritative PDF-compile workflow. The former standalone `.github/workflows/latex.yml` workflow has been removed so there is only one CI definition for LuaLaTeX/PDF validation.

It runs these ordered gates and PDF coverage jobs:

1. **Static validation** checks shell syntax and executes the complete Python/static suite without requiring TeX Live.
2. **LuaLaTeX build matrix** installs the documented toolchain and runs the strict compile suite, so a missing compiler, `latexmk`, or Biber fails instead of producing a false-positive green check.
3. **Root smoke, paper, slides, manual, and focused example PDF jobs** compile their explicit matrices in the same workflow using LuaLaTeX, `latexmk`, Biber, and the documented font set.
4. **Packaging and installed-package gates** validate the CTAN archive and isolated installed-mode behavior after static/l3build checks.

Failed compile jobs upload LaTeX and Biber logs for seven days. Workflow concurrency cancels superseded runs on the same branch or pull request.

## Local TeX toolchain

For Debian/Ubuntu-based development containers, install the same LuaLaTeX-first toolchain used by the compile runner before running full builds:

```bash
sudo apt-get update
sudo apt-get install -y latexmk texlive-luatex biber texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended fonts-freefont-otf fonts-hosny-amiri fonts-noto-core fonts-noto-cjk
```

`latexmk`, `lualatex`, and `biber` must all be on `PATH`. The font packages provide the Arabic, Hebrew, and broad Unicode fallback fonts used by the multilingual typography presets, avoiding local-only fontspec failures during smoke builds.

When TeX Live is installed, run:

```bash
./tests/run-tests.sh
# or, to require the complete toolchain explicitly
./tests/run-tests.sh --require-tex
./scripts/test.sh --compile
```

The compile runner obtains official entrypoints from `tools/overleaf_doctor.py list-entrypoints --plain`, verifies every path exists, cleans each document with `latexmk -C`, and compiles with LuaLaTeX plus `-halt-on-error`. A generated PDF only counts as successful when `latexmk` exits with code 0. If a PDF exists but the build status is failed because references or Biber are unresolved, follow the Overleaf troubleshooting section in [`docs/OVERLEAF_GUIDE.md`](OVERLEAF_GUIDE.md#troubleshooting-pdf-was-generated-but-the-build-failed).

Static-only mode does not require TeX Live and is suitable for lightweight containers. The default `./tests/run-tests.sh` remains developer-friendly and skips compilation when the toolchain is unavailable; CI and `./scripts/test.sh --compile` use strict mode and fail when required TeX tools are missing.

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

If LuaLaTeX/latexmk are available, run `./tests/run-tests.sh --require-tex` to compile all official entrypoints listed by the Overleaf doctor.

## External-package warning policy

Warnings from external TeX packages should be fixed when caused by INSR configuration. If a warning is unavoidable and originates solely from an external package or a missing local toolchain, document the package/tool, command, and reason in the release notes instead of suppressing it.

## v1.0.0-alpha readiness gates

A release candidate must verify native classes (`insr-paper`, `insr-book`, `insr-beamer`, `insr-poster`, `insr-handout`, `insr-manual`), bibliography, localization examples, themes, headers/footers and Overleaf diagnostics. Treat avoidable warnings as defects.

## Target validation and local builds

Use the standard-library tools for target validation and optional local builds:

```bash
python3 tools/overleaf_doctor.py check-target position-paper
python3 tools/overleaf_doctor.py check-target slides
python3 tools/overleaf_doctor.py check-source insr-position-paper
python3 tools/insr_build.py list-targets
python3 tools/insr_build.py validate
python3 tools/insr_build.py build position-paper
python3 tools/insr_build.py build-all
```

The build tool writes temporary active-target configuration, restores the previous file on exit, and reports `latexmk` failures with nonzero exit codes.

## Golden reference and release checks

Run `python3 tools/insr_metadata.py validate`, `python3 tools/insr_metadata.py export-all --outdir build/metadata` and `python3 tools/insr_release.py prepare --version v1.0.0-alpha.1` as part of release-readiness checks. The golden-reference entry points under `examples/reference-publication/` are included in Overleaf doctor entrypoint discovery and CI matrices.

## Renderer regression checks

`tools/validate_project.py` statically validates that internal `\__insr_...:` renderer/helper calls in the modular package layer are defined or explicitly supplied by adapters. This catches missing central renderers such as `\__insr_render_placeholder:` before merge.

CRediT regression coverage includes a four-role author case and a multi-author case with an unknown role plus an empty role list. These tests verify the controlled rendered role strings and warning text rather than only checking macro names.
