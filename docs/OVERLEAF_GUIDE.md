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

## Position-paper content

The productive root build reads `content/manifest.tex`, which currently orders the INSR position-paper files in `content/insr-position-paper/`. Those files may contain explicit placeholders while substantive scientific drafting is pending, but they must remain syntactically valid so the root document can compile.

Official examples use `config/load-project=false` and provide local metadata in class options. This prevents examples from accidentally inheriting the productive position-paper title, author, institution, template or bibliography settings.

## Publication-layer Overleaf checks

Run `python3 tools/overleaf_doctor.py check` before upload. Keep generated LaTeX files out of the upload, and use `config/load-project=false` in official examples so they do not inherit production publication metadata.

## Switching output targets

For Overleaf, keep `main.tex` unchanged and edit only `config/active-target.tex`:

```tex
\INSRSelectTarget{position-paper}
```

Valid targets include `position-paper`, `paper`, `journal-paper`, `slides`, `handout`, `poster`, `clinical-manual`, `technical-report`, `executive-brief`, `book`, and `thesis`. The target is read during early project configuration before the base class is loaded.


## Reference publication workflow

Overleaf builds continue to use `main.tex` plus optional `config/active-target.tex` for target switching. The reference publication example under `examples/reference-publication/` uses `config/load-project=false` entry points so it can be compiled independently without changing the productive root document.
