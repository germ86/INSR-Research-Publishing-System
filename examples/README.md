# INSR examples

Every official example uses the public `insr` class. Compile from the repository root with LuaLaTeX, for example:

```bash
latexmk -lualatex examples/minimal-paper/main.tex
latexmk -lualatex examples/minimal-slides/main.tex
```

The root `main.tex` remains the canonical Overleaf entrypoint. Focused examples may use class options such as `document/type=slides` to demonstrate a specific adapter without changing `config/project-config.tex`.
