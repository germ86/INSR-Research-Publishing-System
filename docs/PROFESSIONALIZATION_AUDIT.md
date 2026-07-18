# INSR professionalization audit

This audit records the verified repository shape used for the first professionalization phase.

## Public entrypoints

- Root class: `insr.cls` loads `insr-core`, `insr-config`, metadata, utility, localization, bibliography, typography, color, layout, frontmatter, page-style, box, accessibility, neuro, content, and adapter modules.
- Compatibility classes: `insr-paper.cls`, `insr-beamer.cls`, `insr-poster.cls`, `insr-handout.cls`, `insr-book.cls`, `insr-manual.cls`, and `insr-core.cls`.
- Root `*.sty` files are source-tree shims into `tex/latex/insr/` for Overleaf and local checkout compatibility.

## Public API policy

Stable user-facing commands are LaTeX2e commands beginning with `INSR`, including `\INSRConfigure`, `\INSRBootstrap`, `\INSRMetadata`, `\INSRMakeTitle`, `\INSRRenderDocument`, `\INSRUseTheme`, and `\INSRUsePlugin`.

Internal implementation functions use the expl3 `insr` namespace, for example `\insr_plugin_register:nn`, `\insr_theme_register:nn`, and resolver functions in `insr-config`. Internal functions are not documented as direct end-user APIs.

## Registries

- Target graph: `config/target-registry.tex` registers document types, output targets, aliases, and build combinations.
- Theme registry: `config/theme-registry.tex` registers first-party theme names and their palette/typography metadata.
- Plugin registry: `config/plugin-registry.tex` registers first-party plugin capabilities while preserving direct package loading.
- JSON project schema: `schema/insr-project.schema.json` defines the machine-readable project configuration contract.

## Current validation findings

- Python static tests initially exposed drift in active target configuration, palette mode defaults, and contradictory static assumptions about `\input@path` mutation. The checked-in tests now reflect the path-neutral shim policy and the active Overleaf target selector.
- `python -m pytest -q` passes.
- l3build configuration exists in both `build.lua` and `l3build.lua`; future CTAN work should consolidate the source-of-truth decision without removing compatibility prematurely.

## Known limitations

- The plugin registry currently records metadata and loaded-state diagnostics; dependency/conflict enforcement is staged for a follow-up regression-tested PR.
- The JSON CLI validates the repository target registry, themes, fontsets, ORCID syntax, unknown top-level fields, and deterministic TeX escaping; full JSON Schema validation is intentionally kept dependency-free for CI portability.
- Accessibility remains a layered feature set and does not claim PDF/UA conformance.

## Stabilization update

- `build.lua` is now the authoritative l3build configuration. `l3build.lua` is retained only as a compatibility shim that delegates to `build.lua`.
- Version and release metadata are centralized in `insr-version.json`; Python tooling reads the JSON schema version from this file.
- CTAN metadata now points to `https://github.com/germ86/INSR-Research-Publishing-System` and the matching issue tracker. CTAN upload remains manual-only until maintainer/uploader contact metadata is finalized.
- l3build regression fixtures live in `testfiles/` and focus on deterministic log assertions for configuration, target resolution, plugin behavior, theme/fontset state, localization, and metadata.
- Theme activation now resolves palette, typography/fontset, and header/footer rule state. Direct palette selection remains supported through `design/palette`.
- Fontsets are registered in `config/fontset-registry.tex`; typography preset files continue to perform engine/font availability fallbacks during LuaLaTeX builds.
