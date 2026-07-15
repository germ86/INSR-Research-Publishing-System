# INSR examples

Every official example uses the public `insr` class and sets `config/load-project=false` so it does not inherit productive position-paper metadata from `config/project-config.tex`.

Compile from the repository root with LuaLaTeX, for example:

```bash
latexmk -lualatex examples/minimal-paper/main.tex
latexmk -lualatex examples/minimal-slides/main.tex
```

List the complete official example matrix with:

```bash
python3 tools/overleaf_doctor.py list-entrypoints --plain
```

The root `main.tex` remains the canonical Overleaf entrypoint. Focused examples may use class options such as `document/type=slides` to demonstrate a specific adapter without changing productive configuration.
