# l3build and release guide

`build.lua` is the authoritative l3build configuration. No repository-local `l3build.lua` is retained because TeX Live l3build internally looks up a file with that name; a local shim shadows the tool internals and breaks `l3build check`.

## Source-of-truth policy

- `tex/latex/insr/` contains the installable class and package implementations.
- The root-level `insr.cls` and supported public compatibility classes are installed as public entrypoints; root-level `insr-*.sty` files are Overleaf/source-tree shims and are not installed as separate package implementations.
- Runtime data directories (`config/`, `framework/`, `profiles/`, `templates/`, `themes/`, `palettes/`, `typography/`, `i18n/`, and first-party `plugins/`) are installed with repository-relative subpaths so TeX lookup works in both source-tree and installed modes.
- Project manuscript prose under `content/` is included in source archives and documentation builds, but installed package smoke tests use neutral external consumer fixtures and must not require repository-relative content.
- Generated release archives must not contain TeX build debris such as `.aux`, `.toc`, `.log`, `.out`, `.fls`, or `.fdb_latexmk` files.
- Overleaf checkouts remain supported by committing the root shims and runtime configuration files.
- `insr-version.json` is the canonical version and release metadata source.

## Regression tests

Regression tests live in `testfiles/` as `.lvt` files with matching `.tlg` references. Prefer deterministic `\typeout` assertions over page-metric-sensitive output.

Run:

```bash
l3build check
```

When an intentional diagnostic changes, regenerate and review the corresponding `.tlg` before committing it.

## CTAN smoke test

Run:

```bash
l3build ctan
unzip -l <generated-archive>.zip
```

The archive must include the license, README, installable package files, documentation, and no temporary build files. This repository does not automatically upload to CTAN.

## Installed-package smoke test

Run:

```bash
bash scripts/test-installed-package.sh
```

The script builds the l3build TDS archive, installs it into an isolated temporary `TEXMFHOME`, creates neutral consumer documents outside the repository, verifies `kpsewhich` resolution from that tree, and compiles the fixtures without `TEXINPUTS`/`BIBINPUTS` pointing at the checkout.
