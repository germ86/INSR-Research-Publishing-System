# INSR Architecture

INSR is a LuaLaTeX-first scientific publishing framework built around a stable public class, reusable package APIs, adapter-specific rendering modules, project-local configuration overlays, and bibliography data files. This document summarizes which file types belong to which architectural layer and how authors should route content for paper, slide, and poster outputs.

## Layered file responsibilities

| Files | Layer | Responsibility |
| --- | --- | --- |
| `insr.cls` | Stable public class | The canonical entry point for new documents. It bootstraps configuration, selects the base class/profile implied by the active target, and loads the package implementation. Treat it as the public contract that content projects depend on. |
| `tex/latex/insr/*.sty` | Package/API layer | Reusable implementation packages for configuration, metadata, content rendering, bibliography, localization, typography, palettes, layout, page styles, boxes, accessibility, domain helpers, utilities, and adapter dispatch. Public macros should be defined or routed here rather than in content files. |
| `framework/adapters/*.tex` | Adapter-specific rendering layer | Thin rendering modules for output targets such as paper, slides, handout, poster, and related profiles. Adapters translate semantic INSR structures into target-specific TeX/Beamer/KOMA output and should avoid owning project metadata or manuscript prose. |
| `config/*.tex` | Project configuration | Project-local values such as active target, theme, palette, typography, localization, metadata, publication settings, bibliography resource paths, and build defaults. These files configure behavior; they should not implement framework internals. |
| `examples/**/references.bib` and future project `.bib` files | Literature data | BibLaTeX databases containing citation metadata for examples and projects. They are data inputs consumed by the bibliography package and must stay separate from rendering logic. |

## Bibliography routing rule

Content files that should render correctly through INSR output adapters must call the public adapter-aware bibliography macro:

```tex
\INSRPrintBibliography
```

Do not call raw BibLaTeX `\printbibliography` from adapter-routed content when the same source may be rendered as paper, slides, handout, or poster. `\INSRPrintBibliography` preserves normal bibliography behavior for paper-like outputs while allowing Beamer and other adapters to place references in the target-specific structure, such as a dedicated References frame.

## Output examples

### Paper

A paper keeps the stable public class and selects a paper-like preset in project configuration:

```tex
% main.tex
\documentclass{insr}

\begin{document}
\INSRMakeTitle
\INSRRenderDocument
\end{document}
```

```tex
% config/active-target.tex
\INSRBootstrap{
  document/type = position-paper,
  build/preset = position-paper
}
```

Paper content can include citations and should end adapter-routed references with:

```tex
\INSRPrintBibliography
```

### Slides

Slides use the same public root class and switch output through configuration instead of changing `main.tex`:

```tex
% config/active-target.tex
\INSRBootstrap{
  document/type = position-paper,
  output/target = slides,
  build/preset = slides
}
```

The slide adapter in `framework/adapters/` receives semantic content from the package/API layer and renders it as Beamer-compatible frames. If references are needed, content still calls `\INSRPrintBibliography`; the adapter decides how the references frame is produced.

### Poster

Posters follow the same layering: stable class, project configuration, package API, and adapter rendering:

```tex
% config/active-target.tex
\INSRBootstrap{
  document/type = position-paper,
  output/target = poster,
  build/preset = poster
}
```

Poster-specific layout belongs in the poster adapter and supporting packages, not in bibliography data or manuscript prose. Project-specific poster metadata and bibliography resource choices belong in `config/*.tex`.

## Extension guidance

* Add durable public commands in `tex/latex/insr/*.sty`, then let adapters consume those commands.
* Keep adapter files focused on target rendering decisions.
* Keep project values in `config/*.tex` so examples and downstream projects can override them safely.
* Keep citation records in `.bib` files, including `examples/**/references.bib` for examples and project-local `.bib` files for future publications.
