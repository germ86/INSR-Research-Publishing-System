# INSR LaTeX Framework

A modular LuaLaTeX framework for the Integrative Neuro-Somatic Recalibration (INSR) research program. It supports scientific papers, Beamer presentations and clinical manuals with a shared corporate design, multilingual LTR/RTL typesetting, multi-author affiliation handling and Overleaf/GitHub workflows.

## Overleaf compatibility findings

These implementation notes were checked against the current Overleaf documentation on 14 July 2026. See the Overleaf pages on [selecting a TeX Live version and compiler](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler), [typesetting non-Latin languages](https://docs.overleaf.com/troubleshooting-and-support/typesetting-non-latin-languages), [TeX Live support](https://docs.overleaf.com/troubleshooting-and-support/tex-live) and [compile timeouts](https://docs.overleaf.com/troubleshooting-and-support/fixing-and-preventing-compile-timeouts).

- Overleaf lets projects choose pdfLaTeX, LaTeX, XeLaTeX or LuaLaTeX; LuaLaTeX is recommended here because it supports UTF-8, OpenType fonts and non-Latin scripts with `polyglossia`.
- Overleaf uses TeX Live and supports standard packages including `fontspec`, TikZ, `biblatex` and Biber.
- For non-Latin scripts such as Arabic, Farsi and Hebrew, Overleaf recommends XeLaTeX or LuaLaTeX with `babel` or `polyglossia`.
- Python execution in cloud LaTeX projects should be treated as optional and security-sensitive. This framework exposes a `python` option that loads `pyluatex` when present, but the default workflow keeps analyses reproducible outside LaTeX and imports generated tables/figures.
- For large TikZ/PGFPlots workloads, use the `externalize` option and Overleaf Premium compile time where available.

## Corporate design

| Token | Hex | Intended use |
| --- | --- | --- |
| INSR Navy | `#0A2342` | primary identity, headings, presentation bars |
| Somatic Teal | `#17A2B8` | links, methods, digital-health accents |
| Alert Amber | `#FFC107` | somatic-hold and caution states |
| Clean Slate | `#F8F9FA` | soft backgrounds |
| Graphite | `#343A40` | body contrast and neutral text |

## Modules

- `tex/latex/insr/insr-base.sty`: shared colors, typography, multilingual setup, acronyms, `biblatex`/APA, boxes and research macros.
- `tex/latex/insr/insr-paper.cls`: journal-paper class with optional `blindreview`, `twocolumn`, `python` and `externalize` options.
- `tex/latex/insr/insr-beamer.cls`: 16:9 presentation class with minimalist INSR navigation and speaker-ready design primitives.
- `tex/latex/insr/insr-manual.cls`: clinical manual/protocol class with therapist notes and fidelity checklists.
- `latexmkrc`: shared LuaLaTeX build settings for local builds, GitHub Actions and Overleaf.

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

## Build commands

```bash
latexmk main.tex
latexmk examples/paper-demo.tex
latexmk examples/beamer-demo.tex
latexmk examples/manual-demo.tex
```

## GitHub and Overleaf workflow

1. Develop and review the framework in GitHub.
2. Sync the repository to Overleaf Premium through Overleaf's Git integration.
3. Compile with LuaLaTeX using the included `latexmkrc`.
4. Use CI to compile the root demonstrator PDF on each push.
