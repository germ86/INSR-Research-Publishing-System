# Testing Guide

Local normative commands:

```bash
scripts/test.sh --static-only
scripts/test.sh
latexmk main.tex
```

When TeX Live is installed, `scripts/test.sh` delegates to the repository test runner and compiles primary smoke documents. Static validation also checks configuration, palettes, bibliography fields and CI job shape.
