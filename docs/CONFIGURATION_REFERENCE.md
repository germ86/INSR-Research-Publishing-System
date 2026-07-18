# INSR v4.0 Configuration Reference

Select the complete root build in `config/active-target.tex` with the one-switch key `build/preset`. Keep broader project defaults in `config/project-config.tex` with `\INSRConfigure{...}`. `main.tex` must remain the stable public entry document.

Core keys:

- `build/preset`: a registered document/output combination. Common presets are `position-paper`, `slides`, `handout`, `position-paper-poster`, `rct-protocol`, `rct-protocol-slides`, `clinical-protocol`, `submission-package`, `book` and `thesis`. The preset resolves the semantic document type, output target, base class, adapter, profile and content source together.
- `document/type`: article, paper, position-paper, whitepaper, report, book, monograph, thesis, slides, handout, poster, letter, grant, protocol, clinical-trial-protocol, rct, systematic-review, narrative-review, technical-documentation, developer-documentation, manual.
- `output/target`: paper, slides, handout, poster, executive-brief, submission-package, web, book, thesis, manual, report, article, letter.
- `document/target`: compatibility alias for earlier one-dimensional target names. New root builds should use `build/preset`.
- `document/density`: compact, standard, spacious.
- `document/build-profile`: development, review, release.
- `design/theme`: insr-default, clinical, research, editorial, technical, minimal, dark, protocol, consortium, conference, documentation, accessible, or a custom theme file.
- `design/palette`: any file in `palettes/` or `palettes/custom/`.
- `design/font`: libertinus, stix-two, ibm-plex, inter, source-serif-sans, noto, latin-modern.
- `typography/microtype`: false by default in the supported build matrix; set to true only when the installed microtype/kernel combination is known not to emit `\showhyphens` patch diagnostics.
- `design/mode`: light, dark, print. This is operational rather than decorative: it selects contrast-safe semantic colours for headings, the table of contents, headers, footers and presentation text. Match dark palettes such as `midnight` with `design/mode = dark`.
- `accessibility/high-contrast`: true or false. The high-contrast palette override is applied before rendered semantic colour aliases are resolved.
- `localization/language`: english, ngerman, arabic, hebrew.
- `localization/direction`: ltr or rtl.
- `bibliography/resource`: BibLaTeX resource path.

Unknown presets, document types, themes, palettes, modes and fonts warn and fall back safely or preserve the previous valid selection.

## One-switch build selection

The active Overleaf configuration intentionally retains `document/type` and `output/target` as compatibility metadata for older tooling, but `build/preset` is placed last and is authoritative. Change only its value:

```tex
\INSRBootstrap{
  document/type = position-paper,
  output/target = slides,
  build/preset = slides
}
```

To return to the paper build, change only:

```tex
build/preset = position-paper
```

To render the same position-paper source through Beamer, use `build/preset = slides`. For an RCT presentation, use `build/preset = rct-protocol-slides`. For a journal submission bundle, use `build/preset = submission-package`.

For compatibility, output-shaped values supplied through `document/type`, such as `document/type = slides`, are now detected as registered combination shorthands and resolve both dimensions. This prevents a stale `paper` or `submission-package` output from overriding an attempted slide switch. Explicit `build/preset` remains the preferred and least ambiguous mechanism.

## Semantic colour roles

Palette files define base roles such as `INSRPrimary`, `INSRBackground`, `INSRText`, `INSRTextMuted`, `INSRAccent` and `INSRLink`. The runtime derives rendered roles from them:

- `INSRHeading` for normal document headings;
- `INSRHeaderText` and `INSRFooterText` for running page furniture;
- `INSRTOCHeading`, `INSRTOCSection`, `INSRTOCSubsection`, `INSRTOCNumber`, `INSRTOCPageNumber` and `INSRTOCLink` for contents rendering;
- Beamer normal text and background colours for slide, handout and poster targets.

In dark mode, text-bearing roles use `INSRText` or `INSRTextMuted`, not the potentially dark identity colour `INSRPrimary`. This separation prevents a valid dark brand colour from becoming unreadable on a dark page.

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
4. document-profile defaults for values that were not explicitly set by the project or class options;
5. theme, palette, typography, page-style, frontmatter and adapter finalisation.

Within a single `\INSRBootstrap{...}` block, keys are processed in order. The checked-in `config/active-target.tex` therefore places `build/preset` last so that it resolves and overrides the compatibility fields atomically.

`document/target`, `design/theme` and `design/palette` are independent dimensions. Theme activation may provide a default palette and fontset, but an explicit `design/palette` or `design/font` is preserved even when the theme is processed later. Document profiles should use `\INSRProfileDefaults{...}` for design defaults so an RCT profile can suggest `design/theme=clinical` without overwriting `design/theme=editorial` or a project-selected palette.

`config/load-project` defaults to `true`. Official examples set `config/load-project=false` in their class options so they do not inherit productive position-paper metadata or content settings from the root project configuration.

The alias `localization/language = german` is normalized to `ngerman`; `english`, `ngerman`, `arabic` and `hebrew` remain the supported canonical language identifiers.

## Publication configuration hierarchy

Publication-specific project values are split across `config/metadata-config.tex`, `config/publication-config.tex`, `config/layout-config.tex` and `config/authors-config.tex`; the implementation layer remains `tex/latex/insr/insr-config.sty`.

## Active target, frontmatter, and placeholders

The canonical Overleaf entrypoint remains `main.tex`. Keep build selection in `config/active-target.tex`; place theme, palette, typography, localization and metadata overrides in `config/project-config.tex`. Preset resolution happens before `\LoadClass`, so switching from KOMA paper output to Beamer slides changes the actual base class rather than merely changing a label.

Implemented combinations are validated by `tools/overleaf_doctor.py check-target <registered-combination>`. Current public keys include `content/source`, `content/placeholders`, `layout/page-numbering`, `frontmatter/toc`, `frontmatter/abstract-numbered`, `frontmatter/keywords`, `publication/citation-mode`, and `publication/suggested-citation`.

Automatic citation mode derives the suggested citation from the registered visible authors, title/subtitle, publication date, and publisher. Manual mode uses `publication/suggested-citation` exactly as configured. Pending DOI values are displayed as pending metadata, not fabricated DOI URLs.

## Release metadata keys

`publication/year` is an optional explicit year override used by metadata exports and automatic citation formatting. Prefer it when `publication/date` is localized or otherwise not safely machine-readable.

## Placeholder, role, TOC, and citation semantics

Content units support semantic keys `role`, `numbered`, `toc`, `required`, and `placeholder`. The default is `required=true`; production builds or `content/placeholders=error` raise a precise content-unit error for required empty/placeholder units, while optional units (`required=false`) may be omitted. Use `\INSRPlaceholder` or `placeholder=true` for controlled placeholders; legacy placeholder prose is accepted temporarily with a migration warning.

`\INSRTableOfContents` is the single public global TOC API. Paper-like targets use the localized class-native `\contentsname`, a stable bookmark destination, a dedicated TOC page style and explicit semantic contents colours. Beamer targets render one localized contents frame. Repeated global calls are ignored and diagnosed in development builds.

Content files must call the public `\INSRPrintBibliography` adapter macro instead of raw `\printbibliography`. The adapter preserves paper-like bibliography output and lets Beamer targets render the bibliography in the target-specific References frame.

Automatic suggested citations are assembled from semantic author, year, title, subtitle, version, and publisher components. `publication/year` is used for the year; full publication dates remain title-page metadata. Pending DOI values are displayed as pending metadata rather than linked identifiers.

CRediT role lists are parsed as comma lists and mapped to publication-facing labels, including Writing -- Original Draft, Writing -- Review and Editing, Formal Analysis, Data Curation, Funding Acquisition, and Resources. Unknown role slugs warn in development and are not printed as raw technical identifiers.

Review builds render neutral placeholder text. Production builds fail required placeholder units, while optional units marked `required=false` may remain silent. The repository's official position-paper content uses explicit `\INSRPlaceholder` markers rather than legacy placeholder prose.
