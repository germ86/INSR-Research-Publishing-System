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
