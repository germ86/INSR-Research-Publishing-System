# Overleaf Guide

Use LuaLaTeX. Keep `main.tex` unchanged, select the complete root build with `build/preset` in `config/active-target.tex`, and keep broader project defaults in `config/project-config.tex`. The project avoids mandatory shell escape and mandatory Python. Biber is required for complete APA bibliography rendering.

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

Do not request the implementation file by repository path (for example, do not put the implementation-directory prefix before `insr-core` in `\RequirePackage`).

That path-shaped form causes the warning “You have requested package … but the package provides …”.

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

## One-switch build selection

For Overleaf, keep `main.tex` unchanged and edit only the last line inside `config/active-target.tex`:

```tex
\INSRBootstrap{
  document/type = position-paper,
  output/target = slides,
  build/preset = slides
}
```

The first two values are retained as compatibility metadata for older repository tooling. `build/preset` is deliberately last and authoritative. Change only that value:

- `position-paper` for the normal paper build;
- `slides` for Beamer slides generated from the position-paper source;
- `handout` for the Beamer handout output;
- `rct-protocol` for the RCT paper;
- `rct-protocol-slides` for RCT slides;
- `clinical-protocol` for the clinical protocol;
- `submission-package` for the submission-oriented paper package.

Preset resolution happens before the base class is loaded. Switching from `position-paper` or `submission-package` to `slides` therefore changes the resolved class to Beamer and the adapter to `framework/adapters/slides.tex`; it does not merely rename the paper.

For compatibility, `document/type = slides`, `document/type = handout`, or `document/type = poster` is also recognized as an output-shaped preset shorthand. Such a shorthand now replaces a stale paper or submission target automatically. `build/preset` is preferred because it is explicit and atomic.

After changing the preset, use **Recompile from scratch**. A previous paper build may leave `.aux`, `.toc`, navigation, or bibliography files that are incompatible with the newly selected Beamer base class.

Use `python3 tools/overleaf_doctor.py check-target <registered-combination>` to validate a named preset from `config/target-registry.tex`.

## Reference publication workflow

Overleaf builds continue to use `main.tex` plus `config/active-target.tex` for source and target switching. The reference publication example under `examples/reference-publication/` uses `config/load-project=false` entry points so it can be compiled independently without changing the productive root document.

## Root build guardrails

Before validating the root document, remove stale TeX auxiliaries and require a zero `latexmk` exit code; an emitted PDF after a failing TeX run is not considered successful. The root content currently contains controlled development placeholders, rendered centrally by `tex/latex/insr/insr-content.sty` according to `document/build-profile` and `content/placeholders`.
