# l3build and release guide

`build.lua` is the authoritative l3build configuration. No repository-local `l3build.lua` is retained because TeX Live l3build internally looks up a file with that name; a local shim shadows the tool internals and breaks `l3build check`.

## Source-of-truth policy

- `tex/latex/insr/` contains the installable class and package implementations.
- Root-level `insr-*.sty` files are Overleaf/source-tree shims and are not separate package implementations.
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
