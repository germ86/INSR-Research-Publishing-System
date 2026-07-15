# Overleaf Guide

Use LuaLaTeX. Keep `main.tex` unchanged and switch output through `config/project-config.tex`. The project avoids mandatory shell escape and mandatory Python. Biber is required for complete APA bibliography rendering.

## Modular v4 architecture and doctor

The canonical Overleaf main document is `main.tex`; keep the compiler set to LuaLaTeX and change output type only in `config/project-config.tex` or in focused example class options. The public class `insr.cls` bootstraps modular packages from `tex/latex/insr/` and then loads runtime adapters from `framework/adapters/`.

Use the optional standard-library helper before uploading or when debugging an Overleaf import:

```bash
python3 tools/overleaf_doctor.py check
python3 tools/overleaf_doctor.py list-entrypoints
python3 tools/overleaf_doctor.py generate-overleaf-report
```

The helper is diagnostic only. Normal LaTeX builds do not require Python.
