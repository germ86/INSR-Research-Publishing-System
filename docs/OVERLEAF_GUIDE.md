# Overleaf Guide

Use LuaLaTeX. Keep `main.tex` unchanged, select the semantic document source and rendered output in `config/active-target.tex`, and keep broader project defaults in `config/project-config.tex`. The project avoids mandatory shell escape and mandatory Python. Biber is required for complete APA bibliography rendering.

## Modular v4 architecture and doctor

The canonical Overleaf main document is `main.tex`. The public class `insr.cls` loads short package names such as `insr-core`; canonical root-level `insr-*.sty` shims forward those requests to the authoritative implementation files under `tex/latex/insr/`. This avoids package-name warnings caused by loading repository paths as package names and avoids mutating `\input@path`.

Use the optional standard-library helper before uploading or when debugging an Overleaf import:

```bash
python3 tools/overleaf_doctor.py check
python3 tools/overleaf_doctor.py list-entrypoints
python3 tools/overleaf_doctor.py report
```

The helper is diagnostic only. Normal LaTeX builds do not require Python.

## GitHub import and synchronization

A transient GitHub API error can appear even when Overleaf has already created the project. Confirm that `main.tex`, `insr.cls`, the root-level `insr-*.sty` shims, `config/`, and `tex/latex/insr/` are present before repeating the import. After every import or GitHub pull, use **Recompile from scratch** once to remove stale auxiliary files.

Do not replace short requests such as:

```tex
\RequirePackage{insr-core}
```

with repository-path requests such as:

```tex
\RequirePackage{tex/latex/insr/insr-core}
```

The latter form causes the warning “You have requested package … but the package provides …”.

## Position-paper content

The productive root build reads `content/manifest.tex`, which currently orders the INSR position-paper files in `content/insr-position-paper/`. Those files may contain explicit placeholders while substantive scientific drafting is pending, but they must remain syntactically valid so the root document can compile.

Official examples use `config/load-project=false` and provide local metadata in class options. This prevents examples from accidentally inheriting the productive position-paper title, author, institution, template or bibliography settings.

## Publication-layer Overleaf checks

Run `python3 tools/overleaf_doctor.py check` before upload. Keep generated LaTeX files out of the upload, and use `config/load-project=false` in official examples so they do not inherit production publication metadata.

After compiling locally or in CI, meaningful warning regressions can be checked with:

```bash
python3 tools/check_latex_log.py main.log
```

The checker rejects INSR package-path mismatches, the known `\showhyphens` compatibility warning, duplicate `pdfauthor` metadata, missing `ngerman` BibLaTeX localisation, and unknown INSR document/output targets.

## Switching document source and output target

For Overleaf, keep `main.tex` unchanged and edit only `config/active-target.tex`:

```tex
\INSRBootstrap{
  document/type = position-paper,
  output/target = paper
}
```

`document/type` selects the semantic source and its profile. `output/target` selects the rendering adapter and base class. For example, a single RCT source can be rendered as paper, slides, handout, or poster by keeping `document/type = rct-protocol` and changing only `output/target` to a registered compatible target.

Use `python3 tools/overleaf_doctor.py check-target <registered-combination>` to validate a named combination from `config/target-registry.tex`.

## Reference publication workflow

Overleaf builds continue to use `main.tex` plus `config/active-target.tex` for source and target switching. The reference publication example under `examples/reference-publication/` uses `config/load-project=false` entry points so it can be compiled independently without changing the productive root document.

## Root build guardrails

Before validating the root document, remove stale TeX auxiliaries and require a zero `latexmk` exit code; an emitted PDF after a failing TeX run is not considered successful. The root content currently contains controlled development placeholders, rendered centrally by `tex/latex/insr/insr-content.sty` according to `document/build-profile` and `content/placeholders`.
