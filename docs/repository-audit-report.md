# INSR Repository Audit Report

Date: 2026-07-14

## Scope

This audit reviewed the repository layout, LuaLaTeX class architecture, examples, bibliography setup, Overleaf assumptions and GitHub Actions workflow. The goal was to make failures easier to isolate and to align documented features with implemented class/package behaviour.

## Architectural findings and fixes

- **Shared functionality belongs in `insr-base.sty`.** Class-adaptive metadata helpers now live in the base package instead of being duplicated in document classes.
- **Beamer must not rely on article-only author commands.** `\INSRAddAuthor` now uses Beamer `\author`/`\institute` when Beamer is active and `authblk`/`\affil` only for non-Beamer classes.
- **Common metadata helpers are class-aware.** Added shared `\INSRInstitute`, `\INSRORCID`, `\INSRTitlePage`, `\INSRKeywords` and `\INSRAcknowledgements` helpers so user documents have stable commands across document types.
- **Class options are consistent.** `python`, `externalize`, `minted` and `review` are forwarded by paper, Beamer and manual classes to the shared base package. `twocolumn` remains paper-specific and `blindreview` remains supported where meaningful.
- **Root document role clarified.** `main.tex` is a Beamer smoke test and now uses valid frame structure. Dedicated examples remain available for paper and manual workflows.

## CI/CD and build fixes

- Split the GitHub Actions workflow into independent jobs for static validation, root smoke build, paper examples, Beamer examples and manual/documentation examples.
- Added `TEXINPUTS` and `BIBINPUTS` to the workflow environment so TDS-style class files and bibliography resources resolve consistently in CI and Overleaf-like builds.
- Added a `--static-only` test mode for CI static validation without requiring local TeX binaries.
- The local test script still compiles the primary smoke documents when `latexmk` is installed and otherwise reports that only static checks were run.

## Documentation and Overleaf fixes

- Corrected the manual bibliography path from `doc/latex/insr` to the repository root bibliography.
- Updated README usage notes to describe the repository root as a smoke test and to point users to dedicated paper, presentation and manual examples.
- Documented option consistency, class-adaptive metadata helpers and CI job separation.

## Remaining limitations

- The current execution container does not include `latexmk`/TeX Live, so local validation in this environment is static only. GitHub Actions is configured to run real LuaLaTeX builds using `xu-cheng/latex-action`.
- Full Arabic/Hebrew rendering depends on fonts such as Amiri and FreeSerif being available in the TeX environment. The framework selects standard fonts, but exact glyph coverage still depends on the installed TeX Live/font set.
- CJK examples are not yet included. The base architecture is LuaLaTeX-compatible, but future CJK support should add a dedicated example and documented font fallback policy.
- The legacy root `insr.cls` remains for backward compatibility with existing single-source examples. Future releases should decide whether to keep it as a compatibility layer or migrate examples fully to the TDS classes.

## Production-readiness assessment

The framework is now substantially closer to production readiness: class responsibilities are isolated, shared commands are centralised, CI failures are separated by document type and documented options are validated. Before CTAN/public release, the project should run a full TeX Live CI matrix, add CJK and RTL regression documents, and expand l3build-based tests for class options and metadata rendering.
