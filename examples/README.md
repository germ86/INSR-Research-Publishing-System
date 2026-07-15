# INSR examples

All files listed below are independent LuaLaTeX entry documents and are compiled in CI.

## Overleaf

Overleaf always compiles the file selected under **Menu → Main document**. Opening an example in the editor does not change the main document.

To compile an example:

1. Open **Menu**.
2. Set **Compiler** to **LuaLaTeX**.
3. Set **Main document** to the exact example path, for example `examples/position-paper/main.tex`.
4. Clear cached files.
5. Recompile from scratch.

Return the setting to `main.tex` for productive project work.

## Canonical project entry point

The repository root must remain:

```latex
\documentclass{insr}

\begin{document}

\INSRMakeTitle
\INSRRenderDocument

\end{document}
```

Do not put document-type, theme, palette, or font options into root `main.tex`. Configure the productive document in `config/project-config.tex`.

## Official focused examples

- `minimal-paper/main.tex`
- `minimal-slides/main.tex`
- `position-paper/main.tex`
- `clinical-manual/main.tex`
- `clinical-protocol/main.tex`
- `rct-protocol/main.tex`
- `systematic-review/main.tex`
- `thesis/main.tex`
- `conference-poster/main.tex`
- `grant-proposal/main.tex`
- `technical-documentation/main.tex`
- `custom-theme/main.tex`
- `custom-palette/main.tex`
- `theme-gallery/main.tex`

The root-level smoke examples and package manual are also compiled by CI.
