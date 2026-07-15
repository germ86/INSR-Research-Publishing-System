# INSR Scientific Publishing Platform

INSR is a modular, LuaLaTeX-first scientific publishing framework for the Integrative Neuro-Somatic Recalibration research program. It is designed around one stable public entry point, central configuration, class-safe adapters, reusable style packages, Overleaf compatibility, and reproducible local/CI builds.


## INSR v4.0 public entry model

The production entry architecture is:

- one public class: `insr.cls`;
- one public entry document: `main.tex`;
- one authoritative configuration file: `config/project-config.tex`.

Switch paper, slides, poster, book, manual or protocol output by changing `document/type` in `config/project-config.tex`, not by editing `main.tex`. Legacy classes under `tex/latex/insr/` are deprecated compatibility surfaces while the v4.0 `insr.cls` architecture becomes authoritative.

## Overleaf compatibility findings

The production entry architecture is intentionally small:

- one public class: `insr.cls`;
- one public root document: `main.tex`;
- one authoritative project configuration file: `config/project-config.tex`.

Do **not** switch output types by editing `main.tex` or by changing to a legacy class. Switch paper, slides, poster, book, manual, protocol or review output by changing the `document/type` key in `config/project-config.tex`.

The canonical root document is always:

```tex
\documentclass{insr}

\begin{document}

\INSRMakeTitle
\INSRRenderDocument

- `tex/latex/insr/insr-base.sty`: shared colors, typography, multilingual setup, acronyms, `biblatex`/APA, boxes and research macros.
- `tex/latex/insr/insr-paper.cls`: journal-paper class with optional `blindreview`, `twocolumn`, `python`, `externalize`, `minted` and `review` options.
- `tex/latex/insr/insr-beamer.cls`: 16:9 presentation class with minimalist INSR navigation, speaker-ready design primitives and the same shared optional feature flags.
- `tex/latex/insr/insr-manual.cls`: clinical manual/protocol class with therapist notes, fidelity checklists and the same shared optional feature flags.
- `latexmkrc`: shared LuaLaTeX build settings for local builds, GitHub Actions and Overleaf.

## Quick start

Set the compiler to **LuaLaTeX** in Overleaf. The repository root `main.tex` is a Beamer smoke test for CI; use the dedicated files under `examples/` as starting points for papers, presentations and manuals.

```tex
\INSRConfigure{
  document/type = paper,
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

`\INSRRenderDocument` loads `content/manifest.tex` by default. The manifest should include reusable content units from `content/shared/` or future document-specific content directories. Public content commands include:

- `INSRContentUnit`;
- `\INSRFullText`;
- `\INSRSummary`;
- `\INSRKeyMessage`;
- `\INSRSpeakerNotes`;
- `\INSROnlyFor`;
- `\INSRExceptFor`.

The runtime packages must not contain hard-coded manuscript prose. Scientific content belongs under `content/`.

## Examples

Official examples use the public `insr` class. Focused examples may pass class options such as `document/type=slides` to demonstrate a specific adapter without editing the production `config/project-config.tex`.

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


## Class-adaptive metadata helpers

The shared base package provides metadata commands that adapt to the active document class:

- `\INSRAddAuthor[short]{name}{institution}` uses `authblk` affiliations in article/report-style classes and Beamer author/institute metadata in presentations.
- `\INSRInstitute[short]{institution}` records an institution without forcing a document-class-specific command in user documents.
- `\INSRORCID{id}` links an ORCID identifier.
- `\INSRTitlePage` emits `\maketitle` for non-Beamer documents and a title frame for Beamer documents.
- `\INSRKeywords{...}` and `\INSRAcknowledgements{...}` are available across classes with class-appropriate rendering.

See `docs/repository-audit-report.md` for the latest architecture and CI audit.

## Build commands

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

1. Develop and review the framework in GitHub.
2. Sync the repository to Overleaf Premium through Overleaf's Git integration.
3. Compile with LuaLaTeX using the included `latexmkrc`.
4. Use CI to compile static checks, the root smoke document, paper examples, Beamer examples and manual/documentation examples as separate jobs.

## Modular package architecture

`insr.cls` is the only public class. It now acts as a bootstrap layer: it loads early configuration and metadata support, resolves the base class, and then delegates implementation to modular packages under `tex/latex/insr/` (`insr-core`, `insr-config`, `insr-metadata`, `insr-content`, `insr-adapters`, `insr-bibliography`, `insr-localization`, `insr-typography`, `insr-colors`, `insr-layout`, `insr-boxes`, `insr-accessibility`, `insr-neuro`, and `insr-utils`). Runtime document adapters remain in `framework/adapters/` and are finalized through `insr-adapters.sty`.

For Overleaf diagnostics, run `python3 tools/overleaf_doctor.py check`. This helper is optional and never required for normal LuaLaTeX compilation.
