# INSR Frontmatter Guide

INSR now separates publication front matter from structural adapters through `tex/latex/insr/insr-frontmatter.sty`. Paper, report, manual, book and thesis adapters call semantic renderers instead of `\maketitle`; slides and posters keep their adapter-specific title frames.

## Core configuration

```tex
\INSRConfigure{
  publication/type = {Preprint},
  publication/status = {draft},
  publication/version = {1.0},
  publication/doi = {pending},
  publication/repository = {https://zenodo.org/records/...},
  publication/license = {CC BY 4.0},
  metadata/short-title = {INSR preprint},
  metadata/citation = {Author. Title. INSR, 2026.},
  layout/header = true,
  layout/footer = true
}
```

`publication/doi` renders only when set. Use `pending` or `to be assigned` to print `DOI: Pending`; INSR never invents DOI values.

## Profiles

Use `publication/profile` for document intent: `generic-preprint`, `journal`, `blind-review`, `double-blind`, `technical-report`, `white-paper`, or `position-paper`. Use `publication/review=blind` or `publication/review=double-blind` to suppress identifying author, affiliation, email, ORCID, funding and conflict metadata from the front page while preserving it internally.

## Examples

* Preprint: `examples/publication-zenodo-preprint/main.tex`
* Journal article: `examples/publication-journal-article/main.tex`
* Position paper: `examples/publication-position-paper/main.tex`
* White paper: set `document/type=whitepaper` and `publication/profile=white-paper`.
* Technical report: set `document/type=report` and `publication/profile=technical-report`.
* Blind review: `examples/publication-blind-review/main.tex`
