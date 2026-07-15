# INSR examples

All listed files are independent LuaLaTeX entry documents and are compiled in CI.

## Overleaf

Overleaf compiles the file selected under **Menu → Main document**. Opening a file in the editor does not change the main document.

1. Set **Compiler** to **LuaLaTeX**.
2. Select the exact entrypoint, for example `examples/position-paper/main.tex`.
3. Clear cached files.
4. Recompile from scratch.
5. Return to `main.tex` for productive project work.

The root `main.tex` must remain canonical and configuration-driven. Do not hard-code document type, theme, palette, or font in it.
