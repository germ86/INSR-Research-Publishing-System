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
