# INSR v4.0 Configuration Reference

Select output only in `config/project-config.tex` with `\INSRConfigure{...}`. `main.tex` must remain the stable public entry document.

Core keys:

- `document/type`: article, paper, position-paper, whitepaper, report, book, monograph, thesis, slides, handout, poster, letter, grant, protocol, clinical-trial-protocol, rct, systematic-review, narrative-review, technical-documentation, developer-documentation, manual.
- `document/density`: compact, standard, spacious.
- `document/build-profile`: development, review, release.
- `design/theme`: insr-default, clinical, research, editorial, technical, minimal, dark, protocol, consortium, conference, documentation, accessible, or a custom theme file.
- `design/palette`: any file in `palettes/` or `palettes/custom/`.
- `design/font`: libertinus, stix-two, ibm-plex, inter, source-serif-sans, noto, latin-modern.
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

The canonical Overleaf entrypoint remains `main.tex`. Select the output in `config/active-target.tex` with `\INSRSelectTarget{position-paper}` or with the `output/target` key in `config/project-config.tex`. Target resolution happens before `\LoadClass`, so Beamer and KOMA outputs are selected safely.

Implemented targets are validated by `tools/overleaf_doctor.py check-target <target>` and share the single source tree under `content/insr-position-paper`. Current public keys include `content/source`, `content/placeholders`, `layout/page-numbering`, `frontmatter/toc`, `frontmatter/abstract-numbered`, `frontmatter/keywords`, `publication/citation-mode`, and `publication/suggested-citation`.

Automatic citation mode derives the suggested citation from the registered visible authors, title/subtitle, publication date, and publisher. Manual mode uses `publication/suggested-citation` exactly as configured. Pending DOI values are displayed as pending metadata, not fabricated DOI URLs.
