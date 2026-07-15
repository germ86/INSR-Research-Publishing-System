# INSR Repository Audit Report

Date: 2026-07-15

## Scope

This audit reviewed the current v4 repository layout, LuaLaTeX bootstrap class, modular packages, runtime adapters, examples, bibliography setup, Overleaf assumptions and GitHub Actions workflow. The goal is to keep the merged v4 architecture buildable and internally consistent.

## Architectural findings and fixes

- **`insr.cls` is the only public class.** It is a thin bootstrap that reads configuration, resolves the base class and delegates implementation to modular packages under `tex/latex/insr/`.
- **Implementation belongs in `.sty` packages.** Core state, configuration, metadata, content, adapters, bibliography, localization, typography, colours, layout, boxes, accessibility, neuro helpers and utilities have separate package owners.
- **Adapters isolate base-class behavior.** Runtime adapters in `framework/adapters/` translate public structural commands such as `\INSRSection` and `\INSRChapter` into class-safe output.
- **The canonical root is stable.** `main.tex` remains `\documentclass{insr}` plus `\INSRMakeTitle` and `\INSRRenderDocument`; it is not a Beamer smoke test and must not be edited to switch output type.
- **Productive output is configuration-driven.** `config/project-config.tex` selects the active INSR position-paper build. Official examples use `config/load-project=false` so they do not inherit productive metadata.
- **Legacy classes are deprecated wrappers.** `insr-paper`, `insr-beamer` and `insr-manual` remain compatibility surfaces only and should not be used for new documents.

## CI/CD and build fixes

- GitHub Actions separates static validation, root smoke, paper examples, slides examples, manual examples and a focused example matrix.
- Local tests obtain official entrypoints from `tools/overleaf_doctor.py list-entrypoints --plain` so documentation, CI and local scripts share one entrypoint registry.
- `TEXINPUTS` and `BIBINPUTS` are configured for root and nested example builds.
- Static-only mode remains available for containers without TeX Live.

## Documentation and Overleaf fixes

- README now documents only the v4 workflow: stable `main.tex`, central config, modular packages, content manifest and deprecated wrappers.
- The Overleaf guide states that Python is diagnostic only and that LuaLaTeX is the required compiler.
- The productive manifest points to `content/insr-position-paper/` placeholders so the root document can build before substantive paper prose is complete.

## Remaining limitations

- The current execution container does not include `latexmk`/TeX Live, so local validation here is static only. GitHub Actions is configured to run real LuaLaTeX builds.
- Position-paper chapter files intentionally contain placeholders; scientific drafting remains pending.
- Full RTL rendering depends on available TeX Live fonts and should be verified in CI/Overleaf.

## Production-readiness assessment

The repository is ready for productive INSR position-paper drafting once CI confirms LuaLaTeX builds in a TeX Live environment. The architecture is stable enough for writing work: root entry, configuration, manifest, examples and adapters now have explicit validation surfaces.
