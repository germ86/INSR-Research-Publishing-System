# INSR v4.0 Configuration Reference

Select the semantic document type and rendering output in `config/active-target.tex` with `\INSRBootstrap{document/type=..., output/target=...}`. Keep broader project defaults in `config/project-config.tex` with `\INSRConfigure{...}`. `main.tex` must remain the stable public entry document.

Core keys:

- `document/type`: article, paper, position-paper, whitepaper, report, book, monograph, thesis, slides, handout, poster, letter, grant, protocol, clinical-trial-protocol, rct, systematic-review, narrative-review, technical-documentation, developer-documentation, manual.
- `output/target`: paper, slides, handout, poster, executive-brief, submission-package, web, book, thesis, manual, report, article, letter.
- `document/target`: deprecated compatibility alias for legacy one-dimensional target names; new projects should use `document/type` plus `output/target`.
- `document/density`: compact, standard, spacious.
- `document/build-profile`: development, review, release.
- `design/theme`: insr-default, clinical, research, editorial, technical, minimal, dark, protocol, consortium, conference, documentation, accessible, or a custom theme file.
- `design/palette`: any file in `palettes/` or `palettes/custom/`.
- `design/font`: libertinus, stix-two, ibm-plex, inter, source-serif-sans, noto, latin-modern.
- `typography/microtype`: false by default in the supported build matrix; set to true only when the installed microtype/kernel combination is known not to emit `\showhyphens` patch diagnostics.
- `design/mode`: light, dark, print.
- `accessibility/high-contrast`: true or false.
- `localization/language`: english, ngerman, arabic, hebrew.
- `localization/direction`: ltr or rtl.
- `bibliography/resource`: BibLaTeX resource path.

Unknown document types, themes, palettes and fonts warn and fall back safely.

## Normal spaces in metadata

Configuration is read with normal LaTeX document syntax, so human-readable metadata may use ordinary spaces:

```tex
\INSRConfigure{
  metadata/title = {A Title With Normal Spaces},
  metadata/author = {First Last}
}
```

Tildes are not required for ordinary metadata spacing.

## Project-config loading and precedence

Configuration precedence is:

1. safe internal defaults;
2. `config/project-config.tex` when `config/load-project=true`;
3. explicit class options;
4. profile defaults for values that are still unset;
5. theme, palette, typography and adapter finalisation.

`config/load-project` defaults to `true`. Official examples set `config/load-project=false` in their class options so they do not inherit productive position-paper metadata or content settings from the root project configuration.

The alias `localization/language = german` is normalized to `ngerman`; `english`, `ngerman`, `arabic` and `hebrew` remain the supported canonical language identifiers.

## Publication configuration hierarchy

Publication-specific project values are split across `config/metadata-config.tex`, `config/publication-config.tex`, `config/layout-config.tex` and `config/authors-config.tex`; the implementation layer remains `tex/latex/insr/insr-config.sty`.

## Active target, frontmatter, and placeholders

The canonical Overleaf entrypoint remains `main.tex`. Select the semantic document type and output format in `config/active-target.tex` with `\INSRBootstrap{document/type=position-paper, output/target=paper}`. Keep type/target selection in that bootstrap file; place other user overrides in `config/project-config.tex`. Target resolution happens before `\LoadClass`, so Beamer and KOMA outputs are selected safely.

Implemented targets are validated by `tools/overleaf_doctor.py check-target <target>` and share the single source tree under `content/insr-position-paper`. Current public keys include `content/source`, `content/placeholders`, `layout/page-numbering`, `frontmatter/toc`, `frontmatter/abstract-numbered`, `frontmatter/keywords`, `publication/citation-mode`, and `publication/suggested-citation`.

Automatic citation mode derives the suggested citation from the registered visible authors, title/subtitle, publication date, and publisher. Manual mode uses `publication/suggested-citation` exactly as configured. Pending DOI values are displayed as pending metadata, not fabricated DOI URLs.


## Release metadata keys

`publication/year` is an optional explicit year override used by metadata exports and automatic citation formatting. Prefer it when `publication/date` is localized or otherwise not safely machine-readable.

## Placeholder, role, and citation semantics

Content units support semantic keys `role`, `numbered`, `toc`, `required`, and `placeholder`. The default is `required=true`; production builds or `content/placeholders=error` raise a precise content-unit error for required empty/placeholder units, while optional units (`required=false`) may be omitted. Use `\INSRPlaceholder` or `placeholder=true` for controlled placeholders; legacy placeholder prose is accepted temporarily with a migration warning.

`\INSRTableOfContents` is the single public global TOC API. Paper-like targets use the class-native `\tableofcontents` heading with one stable bookmark destination; Beamer targets render one Agenda frame. Repeated global calls are ignored and diagnosed in development builds.

Automatic suggested citations are assembled from semantic author, year, title, subtitle, version, and publisher components. `publication/year` is used for the year; full publication dates remain title-page metadata. Pending DOI values are displayed as pending metadata rather than linked identifiers.

CRediT role lists are parsed as comma lists and mapped to publication-facing labels, including Writing -- Original Draft, Writing -- Review and Editing, Formal Analysis, Data Curation, Funding Acquisition, and Resources. Unknown role slugs warn in development and are not printed as raw technical identifiers.

Review builds render neutral placeholder text. Production builds fail required placeholder units, while optional units marked `required=false` may remain silent. The repository's official position-paper content uses explicit `\INSRPlaceholder` markers rather than legacy placeholder prose.
