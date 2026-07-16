# INSR Scientific Publishing Platform

INSR is a modular, LuaLaTeX-first scientific publishing framework for the Integrative Neuro-Somatic Recalibration research program. It is designed around one stable public entry point, central configuration, class-safe adapters, reusable style packages, Overleaf compatibility, and reproducible local/CI builds.

## INSR v4.0 public entry model

The production entry architecture is intentionally small:

- one public class: `insr.cls`;
- one public root document: `main.tex`;
- one authoritative project configuration file: `config/project-config.tex`.

Do **not** switch output types by editing `main.tex` or by changing to a legacy class. Select the semantic document genre and rendering format in `config/active-target.tex` with `document/type` and `output/target`; keep project-wide defaults such as theme, palette, typography and metadata in `config/project-config.tex`.

The canonical root document is always:

```tex
\documentclass{insr}

\begin{document}

\INSRMakeTitle
\INSRRenderDocument

\end{document}
```

## Quick start

1. Set the compiler to **LuaLaTeX**.
2. Keep `main.tex` unchanged.
3. Edit `config/active-target.tex` to select `document/type` and `output/target`; edit `config/project-config.tex` for theme, palette, typography and metadata.
4. Compile `main.tex`.

A minimal configuration looks like this:

```tex
\INSRBootstrap{
  document/type = position-paper,
  output/target = paper
}

\INSRConfigure{
  design/theme = clinical,
  design/palette = neuroclinical,
  design/font = libertinus,
  localization/language = english,
  metadata/title = {Integrative Neuro-Somatic Recalibration},
  metadata/author = {Fabio Schmeil},
  metadata/institution = {Independent Research Development}
}
```

Normal spaces in human-readable metadata are supported; `~` is not required for titles, authors or institutions.

## Package architecture

`insr.cls` is a bootstrap class only. It loads early configuration, resolves the requested base class, and delegates runtime implementation to packages under `tex/latex/insr/`:

| Package | Responsibility |
| --- | --- |
| `insr-core.sty` | shared state, lifecycle flags, messages and early public API |
| `insr-config.sty` | configuration keys, defaults and document-type resolution |
| `insr-metadata.sty` | title, author/institution compatibility API and PDF metadata preparation |
| `insr-content.sty` | content manifest rendering and `INSRContentUnit` support |
| `insr-adapters.sty` | adapter loading, readiness checks and public structural dispatch |
| `insr-bibliography.sty` | BibLaTeX loading and safe bibliography printing |
| `insr-localization.sty` | Babel/fontspec language setup and RTL/LTR helpers |
| `insr-typography.sty` | typography preset loading |
| `insr-colors.sty` | palette loading and semantic colour setup |
| `insr-layout.sty` | common layout packages, theme loading and PDF metadata activation |
| `insr-boxes.sty` | semantic scientific statements and note/block environments |
| `insr-accessibility.sty` | accessibility helpers and alt-text hooks |
| `insr-neuro.sty` | domain-specific neuro/clinical helper commands |
| `insr-utils.sty` | dynamic file loading and diagnostics |

Runtime adapters remain small `.tex` modules in `framework/adapters/` and document profiles live in `profiles/documents/`. Adapter files must use the internal `\__insr_adapter_...` namespace and are finalized through `insr-adapters.sty`.

## Content model

`\INSRRenderDocument` loads `content/manifest.tex` by default. The productive manifest currently orders the INSR position-paper files under `content/insr-position-paper/`; placeholders are allowed only to keep the build syntactically complete until substantive paper drafting begins. Public content commands include:

- `INSRContentUnit`;
- `\INSRFullText`;
- `\INSRSummary`;
- `\INSRKeyMessage`;
- `\INSRSpeakerNotes`;
- `\INSROnlyFor`;
- `\INSRExceptFor`.

The runtime packages must not contain hard-coded manuscript prose. Scientific content belongs under `content/`.

## Examples

Official examples use the public `insr` class and set `config/load-project=false` so they do not inherit productive position-paper metadata, templates or bibliography settings. Focused examples may pass class options such as `document/type=slides` to demonstrate a specific adapter without editing the production `config/project-config.tex`.

```bash
latexmk -lualatex main.tex
latexmk -lualatex examples/minimal-paper/main.tex
latexmk -lualatex examples/minimal-slides/main.tex
latexmk -lualatex examples/clinical-manual/main.tex
```

See `examples/README.md` for the example policy. To list every documented entrypoint used by local tests, run `python3 tools/overleaf_doctor.py list-entrypoints --plain`.

## Overleaf workflow

1. Upload or sync the repository to Overleaf.
2. Set the main document to `main.tex`.
3. Set the compiler to LuaLaTeX.
4. Change document output only in `config/project-config.tex`.
5. Use Biber when bibliography output is enabled.

Python is optional. The diagnostic helper can be run locally or in CI, but normal PDF generation must not depend on it:

```bash
python3 tools/overleaf_doctor.py check
python3 tools/overleaf_doctor.py list-entrypoints
python3 tools/overleaf_doctor.py generate-overleaf-report
```

## Local validation

```bash
python3 tools/overleaf_doctor.py check
python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py
./tests/run-tests.sh --static-only
./scripts/test.sh --compile
```

When TeX Live is installed, `./scripts/test.sh --compile` compiles the root and official example entrypoints with `latexmk`.

## Deprecated compatibility wrappers

Legacy classes remain only as temporary compatibility wrappers:

- `tex/latex/insr/insr-paper.cls`;
- `tex/latex/insr/insr-beamer.cls`;
- `tex/latex/insr/insr-manual.cls`.

Do not use them for new documents. New projects should use `\documentclass{insr}` and configuration keys instead.

## Corporate design reference

The default neuroclinical design uses restrained navy/teal/cyan accents and semantic palette tokens. Content should rely on semantic INSR commands and environments rather than raw colour names.

| Reference colour | Hex | Intended use |
| --- | --- | --- |
| Primary navy | `#16324F` | identity, headings, title bars |
| Deep teal | `#0F7C82` | methods, clinical/research accents |
| Accent cyan | `#5CCFE6` | restrained highlights and links |
| Ice background | `#F8FAFC` | soft backgrounds |
| Graphite text | `#2D3748` | body text |

## Further documentation

- `docs/CONFIGURATION_REFERENCE.md` — configuration keys and defaults.
- `docs/OVERLEAF_GUIDE.md` — Overleaf setup and diagnostics.
- `docs/TESTING_GUIDE.md` — local and CI validation commands.
- `docs/THEME_DEVELOPER_GUIDE.md` — theme extension notes.
- `docs/PALETTE_DEVELOPER_GUIDE.md` — palette extension notes.
- `docs/TEMPLATE_DEVELOPER_GUIDE.md` — template/profile extension notes.

## Publication-ready front matter

INSR includes a dedicated publication layer for journal manuscripts, position papers, white papers, reports, manuals, books, theses and grant proposals. Configure it with `publication/*`, `metadata/*` and `layout/*` keys, then call the stable public API `\INSRMakeTitle`. See `FRONTMATTER_GUIDE.md` for DOI handling, blind-review suppression, running headers/footers and examples.

Page styles are centralized in `tex/latex/insr/insr-page-style.sty`; see `PAGESTYLE_GUIDE.md` for semantic title/frontmatter/main/references/appendix styles and palette-integrated header, footer and TOC colors.

Native distribution-style classes are available for production documents: `insr-paper`, `insr-book`, `insr-beamer`, `insr-poster`, `insr-handout` and `insr-manual`. They all inherit the shared `insr` architecture and remain compatible with the v4 public API.

### Active target workflow

The root `main.tex` remains stable. Select the generated output in `config/active-target.tex` with the bootstrap-only setting `\INSRBootstrap{document/type=position-paper, output/target=paper}`. Broader project values remain in `config/project-config.tex` and no longer need to restate the target. Target selection occurs before the base class is loaded, preserving safe KOMA/Beamer switching while retaining the modular `.sty` architecture.

Frontmatter now suppresses empty optional fields, resolves author affiliation IDs to publication-facing institution names, moves CRediT roles into author contributions, and can generate suggested citations from visible author metadata.


### Release readiness and golden reference

The neutral golden-reference project lives in `examples/reference-publication/` and exercises paper, slides, handout and poster entry points without scientific or clinical claims. Metadata exports are prepared with `python3 tools/insr_metadata.py export-all --outdir build/metadata`; release bundles are prepared locally with `python3 tools/insr_release.py prepare --version <version>`. See `docs/RELEASE_GUIDE.md`.

### Root build placeholder and TOC policy

INSR v4 keeps placeholder rendering central in `tex/latex/insr/insr-content.sty`. Authors should mark intentional empty content with `\INSRPlaceholder` or `placeholder=true`; legacy prose placeholders are accepted only with a migration warning. Production builds and `content/placeholders=error` fail required empty units with unit ID, visible title, source, and target. `\INSRTableOfContents` is the only global TOC API and is guarded against duplicate visible contents pages.
