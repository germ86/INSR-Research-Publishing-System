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

## Stabilization notes

The frontmatter renderer now delegates page-state changes to `insr-page-style.sty`, keeping title/frontmatter metadata rendering separate from page-style implementation. DOI values are displayed only when configured and are also forwarded to PDF metadata.

## Publication-quality title-page rules

The title page renders the publication type once, then the title and subtitle. Author output is built from the author/institution registries: internal affiliation IDs are resolved to institution names, ORCID values are shown separately, and CRediT roles are moved into an author-contributions block using human-readable labels.

Optional fields are rendered only when their trimmed value is nonblank. This applies to funding, conflicts of interest, ethics, highlights, key messages, author contributions, data availability, code availability, repository, license, and suggested citation.


## Optional field semantics

Optional frontmatter labels are emitted only when their underlying token-list or author-role data is non-empty. Renderer macros alone do not make Funding, Conflict of interest, Ethics, Highlights, Key messages, Data availability, Code availability or Author contributions visible.
