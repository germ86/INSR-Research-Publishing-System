# INSR Page Style Guide

INSR centralizes publication page styles in `tex/latex/insr/insr-page-style.sty`. Themes no longer load or configure `scrlayer-scrpage`; themes describe layout intent and palettes provide semantic colors.

## Semantic styles

The page-style module provides title page, front matter, table of contents, main text, chapter page, references, appendix and blind-review styles through semantic commands:

```tex
\INSRPageStyleTitle
\INSRPageStyleFrontMatter
\INSRPageStyleTOC
\INSRPageStyleMain
\INSRPageStyleChapter
\INSRPageStyleReferences
\INSRPageStyleAppendix
```

## Placeholders

Header and footer configuration accepts `running-title`, `current-section`, `page-number`, `total-pages`, `version` and `doi`.

## Palette integration

Headers, footers and table-of-contents links use semantic colors derived from the active palette: `INSRHeaderText`, `INSRHeaderAccent`, `INSRFooterText`, `INSRFooterAccent`, `INSRTOCHeading`, `INSRTOCSection`, `INSRTOCSubsection`, `INSRTOCCurrent`, `INSRTOCPageNumber`, `INSRTOCLink` and `INSRTOCLeader`.

## Professional separators

Header and footer separators are controlled through `layout/header-separator-style`, `layout/footer-separator-style`, `layout/header-separator-thickness`, `layout/footer-separator-thickness`, `layout/header-separator-spacing`, `layout/footer-separator-spacing` and `layout/separator-opacity`. Supported styles are `single`, `double`, `accent` and `minimal`. Separator colors come from theme-level `INSRHeaderSeparator` and `INSRFooterSeparator`, which derive from the active palette.

## Page styles and contents

Page styles use three header zones and three footer zones backed by semantic palette colors. Separator rules use KOMA `headsepline` and `footsepline` options rather than deprecated `scrlayer-scrpage` commands. The default footer uses body-only numbering, with `layout/page-numbering` reserved for `body-only`, `physical`, and `frontmatter-roman` workflows.

`\INSRTableOfContents` provides a palette-aware contents page for paper-like outputs and an agenda frame for Beamer outputs. The default position-paper profile enables the contents page and leaves Abstract unnumbered so Introduction starts the numbered main text.


## Release page-style checks

Release candidates should inspect the root document and the reference-publication paper for title page, table of contents, normal content page, bibliography and appendix page styles. `body-only`, `physical` and `frontmatter-roman` numbering modes must be checked in a TeX-enabled environment.
