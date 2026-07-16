# INSR Configuration Reference

Existing configuration keys remain supported. Publication-quality output adds these compatible keys:

* `publication/type`, `publication/status`, `publication/version`, `publication/revision`, `publication/date`, `publication/revision-date`
* `publication/doi`, `publication/url`, `publication/repository`, `publication/license`, `publication/copyright`
* `publication/profile`, `publication/review`
* `metadata/short-title`, `metadata/citation`, `metadata/keywords`, `metadata/abstract-word-count`, `metadata/document-word-count`
* `metadata/funding`, `metadata/conflict-of-interest`, `metadata/ethics`, `metadata/graphical-abstract`, `metadata/highlights`, `metadata/key-messages`, `metadata/clinical-significance`, `metadata/abbreviations`, `metadata/author-contributions`, `metadata/data-availability`, `metadata/code-availability`
* `layout/header`, `layout/footer`, `layout/header-left`, `layout/header-center`, `layout/header-right`, `layout/footer-left`, `layout/footer-center`, `layout/footer-right`

Header/footer placeholders: `current-section`, `running-title`, `page-number`, `total-pages`, `version`, `doi`.

## Project configuration hierarchy

The configuration engine remains implemented in `tex/latex/insr/insr-config.sty`. Project-specific values are split across `config/project-config.tex`, `config/metadata-config.tex`, `config/publication-config.tex`, `config/layout-config.tex` and `config/authors-config.tex`. Optional overlays may live in `config/profiles/`.
