# INSR LaTeX Framework

A modular LuaLaTeX framework for the Integrative Neuro-Somatic Recalibration (INSR) research program. It supports scientific papers, Beamer presentations and clinical manuals with a shared corporate design, multilingual LTR/RTL typesetting, multi-author affiliation handling and Overleaf/GitHub workflows.

## Overleaf compatibility findings

These implementation notes were checked against the current Overleaf documentation on 14 July 2026. See the Overleaf pages on [selecting a TeX Live version and compiler](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler), [typesetting non-Latin languages](https://docs.overleaf.com/troubleshooting-and-support/typesetting-non-latin-languages), [TeX Live support](https://docs.overleaf.com/troubleshooting-and-support/tex-live) and [compile timeouts](https://docs.overleaf.com/troubleshooting-and-support/fixing-and-preventing-compile-timeouts).

- Overleaf lets projects choose pdfLaTeX, LaTeX, XeLaTeX or LuaLaTeX; LuaLaTeX is recommended here because it supports UTF-8, OpenType fonts and non-Latin scripts with `polyglossia`.
- Overleaf uses TeX Live and supports standard packages including `fontspec`, TikZ, `biblatex` and Biber.
- For non-Latin scripts such as Arabic, Farsi and Hebrew, Overleaf recommends XeLaTeX or LuaLaTeX with `babel` or `polyglossia`.
- PythonTeX is not used as a default path because current Overleaf v2 guidance treats it as unsupported; Python execution in cloud LaTeX projects should be treated as optional and security-sensitive. This framework exposes a `python` option that loads `pyluatex` when present, but the default workflow keeps analyses reproducible outside LaTeX and imports generated tables/figures.
- For large TikZ/PGFPlots workloads, use the `externalize` option and Overleaf Premium compile time where available.

## Corporate design

| Token | Hex | Intended use |
| --- | --- | --- |
| INSR Navy | `#0A2342` | primary identity, headings, presentation bars |
| Somatic Teal | `#17A2B8` | links, methods, digital-health accents |
| Alert Amber | `#FFC107` | somatic-hold and caution states |
| Clean Slate | `#F8F9FA` | soft backgrounds |
| Graphite | `#343A40` | body contrast and neutral text |

## Package status

This repository is now organized as a complete LaTeX package distribution: runtime files live in `tex/latex/insr`, documentation lives in `doc/latex/insr`, examples live in `examples`, `build.lua` supports l3build-style packaging metadata, and `scripts/build-ctan.sh` creates a release ZIP for GitHub releases or Overleaf uploads.

## Modules

- `tex/latex/insr/insr-base.sty`: shared colors, typography, multilingual setup, acronyms, `biblatex`/APA, boxes and research macros.
- `tex/latex/insr/insr-paper.cls`: journal-paper class with optional `blindreview`, `twocolumn`, `python` and `externalize` options.
- `tex/latex/insr/insr-beamer.cls`: 16:9 presentation class with minimalist INSR navigation and speaker-ready design primitives.
- `tex/latex/insr/insr-manual.cls`: clinical manual/protocol class with therapist notes and fidelity checklists.
- `latexmkrc`: shared LuaLaTeX build settings for local builds, GitHub Actions and Overleaf.
- `doc/latex/insr/insr-latex-manual.tex`: package manual source.
- `build.lua` and `scripts/build-ctan.sh`: package/release metadata and ZIP generation.

## Quick start

Set the compiler to **LuaLaTeX** in Overleaf and keep `main.tex` in the project root.

```tex
\documentclass{insr-paper}
\addbibresource{references.bib}
\title{INSR Study Protocol}
\INSRAddAuthor[1]{First Author}{Institution}
\begin{document}
\maketitle
\section{Purpose}
\gls{insr} is a \gls{cdss} research framework.
\printglossary[type=\acronymtype]
\printbibliography
\end{document}
```

## Class and package options

- `blindreview`: masks author and institution metadata where supported.
- `twocolumn`: enables a compact paper layout for `insr-paper`.
- `rtl`: switches the default language direction for RTL-first workflows.
- `python`: loads `pyluatex` when present.
- `minted`: loads `minted` for syntax highlighting when present.
- `review`: loads `todonotes` when present and enables colored clinical, biostatistical and technical review notes.
- `externalize`: enables TikZ externalization for large PGFPlots/TikZ workloads.

## Build commands

```bash
latexmk main.tex
latexmk examples/paper-demo.tex
latexmk examples/beamer-demo.tex
latexmk examples/manual-demo.tex
./scripts/build-ctan.sh
```

## GitHub and Overleaf workflow

1. Develop and review the framework in GitHub.
2. Sync the repository to Overleaf Premium through Overleaf's Git integration.
3. Compile with LuaLaTeX using the included `latexmkrc`.
4. Use CI to compile the root demonstrator PDF on each push.
