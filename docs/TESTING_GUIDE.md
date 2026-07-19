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

`.github/workflows/ci.yml` is the required pull-request and `main` validation workflow. It runs two ordered gates:

1. **Static validation** checks shell syntax and executes the complete Python/static suite without requiring TeX Live.
2. **LuaLaTeX build matrix** installs the documented toolchain and runs the compile suite with `--require-tex`, so a missing compiler, `latexmk`, or Biber fails instead of producing a false-positive green check.

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

The compile runner obtains official entrypoints from `tools/overleaf_doctor.py list-entrypoints --plain`, verifies every path exists, cleans each document with `latexmk -C`, and compiles with LuaLaTeX plus `-halt-on-error`. A generated PDF only counts as successful when `latexmk` exits with code 0.

### GitHub bibliography and font failures

A log can show `Output written on main.pdf` and still fail when `latexmk` exits nonzero because BibLaTeX has not converged. Treat `Package biblatex Warning: Please (re)run Biber on the file: main` together with `LaTeX Warning: There were undefined references` as a toolchain/convergence failure: Biber must run and LuaLaTeX must rerun until references settle. The repository `latexmkrc` enables this with `$bibtex_use = 2`, the explicit `biber %O %B` command and enough repeat passes. Root smoke builds without a configured `bibliography/resource` do not load the BibLaTeX backend, so they should not emit a Biber rerun warning merely because the framework bibliography package is present.

`tools/check_latex_log.py` also fails generic fatal LaTeX patterns such as package errors, `LaTeX Error`, undefined control sequences, emergency stops and missing output PDFs. Use it on every produced log before treating a generated PDF as successful.

Multilingual examples also require usable Arabic/Hebrew fonts. The INSR typography layer falls back from Amiri/Noto language fonts to TeX Gyre/Latin Modern so missing optional fonts do not abort smoke builds before the actual document can be validated.

Palette mode metadata is tracked in `palettes/manifest.json`; tests compare the active `design/mode` with the active palette background luminance rather than pinning the project to a single palette name.

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

## Build-profile smoke checks

The root project defaults to `document/build-profile = development` so incomplete content units can remain visible during drafting. Before a productive/release handoff, switch the project or a smoke fixture to `document/build-profile = production` and keep `content/placeholders` unset or set to `error`; required placeholders must then fail intentionally. The aliases `productive`, `prod`, and `release` normalize to `production`, but release scripts should use the canonical `production` spelling.

For review copies, use `document/build-profile = review`. This keeps the same target/palette/theme resolution while rendering neutral placeholder text for reviewers.

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
