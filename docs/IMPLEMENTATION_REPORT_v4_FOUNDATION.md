# INSR v4.0 Foundation Implementation Report

Date: 2026-07-14

## Source specification availability

The requested normative files `ARCHITECTURE_SPEC_v4.0.md`, `ADR_CATALOG.md`, `IMPLEMENTATION_ROADMAP.md` and `CODEX_MASTER_PROMPT.md` were not present in the repository checkout. The implementation therefore follows the v4.0 requirements supplied in the task text and records this limitation explicitly.

## Files created, modified, moved or removed

Created major runtime directories and files:

- `framework/adapters/` for base-class-specific adapters.
- `profiles/documents/` for document-type profiles.
- `palettes/` and `palettes/custom/` for semantic palette mappings.
- `themes/` for layout/theme rendering.
- `typography/` for typography presets and font fallbacks.
- focused examples under `examples/*/main.tex`.
- documentation guides under `docs/`.
- `scripts/test.sh` and `scripts/test.ps1`.

Modified:

- `insr.cls` as the v4.0 public class and two-phase bootstrap.
- `main.tex` as stable public entry document.
- `config/project-config.tex` as authoritative configuration.
- `README.md`, `CHANGELOG.md`, validators and test runner.

## Legacy architecture migrated or deprecated

The stable architecture is now `insr.cls` + `main.tex` + `config/project-config.tex`. Legacy public classes remain in `tex/latex/insr/` for compatibility and are documented as deprecated surfaces rather than the primary architecture. Further work should convert them to thin wrappers or remove them in a major compatibility break.

## Document types implemented

The resolver handles article, paper, position-paper, whitepaper, report, book, monograph, thesis, slides, handout, poster, letter, grant, protocol, clinical-trial-protocol, rct, systematic-review, narrative-review, technical-documentation, developer-documentation and manual.

## Themes implemented

Implemented built-in theme files: insr-default, clinical, research, editorial, technical, minimal, dark, protocol, consortium, conference, documentation and accessible.

## Palettes implemented

Implemented built-in palettes: neuroclinical, clinical, research, editorial, ocean, forest, slate, graphite, monochrome, high-contrast, colourblind-safe, print, warm-clinical, calm-trauma, neurodiversity, academic-blue, biomedical, public-health, digital-health, midnight and light-minimal. A custom palette example is included under `palettes/custom/`.

## Typography presets implemented

Implemented presets: Libertinus, STIX Two, IBM Plex, Inter, Source Serif/Sans, Noto and Latin Modern. Each preset uses `\IfFontExistsTF` and TeX Live fallbacks.

## Test commands executed

- `./tests/run-tests.sh --static-only`
- `python3 -Werror tools/validate_project.py`
- `git diff --check`
- `./tests/run-tests.sh`

## Test results

Static validation, bibliography validation, palette validation and repository structure checks passed. Local compilation was not executed because this container does not include `latexmk` or TeX Live.

## Warnings still present

- Full compilation must be verified in CI or a TeX Live environment.
- The normative specification files named in the task were not available in this checkout.
- Legacy compatibility classes still exist and should become thin wrappers in a follow-up.

## Deferred work

- Full l3build regression suite.
- True circular theme-inheritance detection beyond the current safe fallback-by-file model.
- Complete content-slot validation for every production template.
- CJK demonstration and font policy.
- Full TeX Live compilation matrix for every adapter/palette/theme/font combination.

## Milestone assessment

Milestones 0 through 3 are partially satisfied: the public entry model, central configuration, adapter foundation, document profiles, design tokens, palettes, themes, typography presets, semantic components, examples and static validation exist. The repository should not yet be called fully production-ready until the complete LuaLaTeX/Biber compilation matrix passes in CI and legacy wrappers are finished.

## Rebase onto current main

The v4 branch was rebased onto `origin/main` after fetching the current main branch. Git reported two textual conflicts:

1. `main.tex`: main contained a legacy `insr-manual` document with Beamer `frame` environments. The v4 side contained the stable public entry document. The merged result preserves the v4 public entry model because this directly fixes the class-incompatible root document defect while keeping the legitimate intention from main that the root remains a demonstrator.
2. `tools/validate_project.py`: main contained legacy checks for required repository files, legacy compatibility commands and wrapper options. The v4 branch contained checks for the new public entry, adapters, profiles, palettes, themes, typography and examples. The merged result keeps both: legacy resource checks and wrapper option checks were incorporated into the v4 validator, while the v4 bootstrap, conflict-marker and stable-root checks remain authoritative.

No conflicted file was resolved by blindly selecting ours or theirs; each was merged semantically to preserve v4 architecture while retaining legitimate validation coverage from main.


## Public API export hardening

A subsequent Overleaf build reported `\INSRMakeTitle` and `\INSRRenderDocument` as undefined even though the v4 class defines them later in the runtime phase. To make the public API robust against stale adapter failures or early execution problems, both commands are now declared before `\LoadClass` and dispatch dynamically to the resolved adapter/template once those internals exist. The class also emits an API diagnostic banner listing the exported public symbols and a class/version banner during compilation. Static validation now enforces that there is exactly one authoritative `insr.cls` in the repository and that the public API is exported before base-class loading.
