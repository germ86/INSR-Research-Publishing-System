# CTAN/TDS Packaging Notes

Package name: `insr`

Version: `0.1.0`

License: LPPL-1.3c

Maintainer: INSR Research Consortium

## TDS layout

- Runtime files: `tex/latex/insr/*.sty` and `tex/latex/insr/*.cls`
- Documentation: `README.md`, `CHANGELOG.md`, `LICENSE`, `doc/latex/insr/insr-latex-manual.tex`
- Examples: `examples/*.tex`
- Build metadata: `build.lua`, `latexmkrc`

## Local package archive

Run:

```bash
./scripts/build-ctan.sh
```

The script creates `dist/insr-latex-0.1.0.zip`, which mirrors a TDS-friendly repository distribution suitable for GitHub releases or Overleaf uploads.

## Notes on Python and shell escape

`pythontex` is intentionally not part of the package defaults because Overleaf's v2 FAQ states that `pythontex` is not currently supported in Overleaf v2. The framework instead provides an optional `python` flag for `pyluatex` when the target environment has it installed, and an optional `minted` flag for syntax highlighting. The shared `latexmkrc` enables shell escape to support minted and TikZ externalization in trusted projects.
