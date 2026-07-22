# Palette Developer Guide

Palettes map base colour roles to concrete colour values. Required base roles include primary, secondary, accent, background, surface, surface-alt, text, text-muted, rule, link, success, warning, danger, info, evidence, clinical, research, method, result, limitation and safety.

## Base colours versus rendered semantic roles

`INSRPrimary` and `INSRSecondary` are identity colours; they are not automatically safe as text colours. The runtime derives rendered roles such as `INSRHeading`, `INSRHeaderText`, `INSRFooterText`, `INSRTOCHeading`, `INSRTOCSection`, `INSRTOCSubsection`, `INSRTOCNumber` and `INSRTOCPageNumber` from the active palette and `design/mode`.

In `design/mode = dark`, text-bearing roles derive from `INSRText` and `INSRTextMuted`, while accent and numbering roles derive from `INSRAccent` and `INSRLink`. In `design/mode = light`, headings may use the primary identity colour. `design/mode = print` normalizes the page to a white background and dark text while retaining the document structure.

The palette must therefore provide readable `INSRText` and `INSRTextMuted` values against `INSRBackground`. Normal body text should meet a WCAG contrast ratio of at least 4.5:1. Do not solve a dark-palette contrast problem by making the brand primary artificially bright; keep identity and text roles separate.

Accessibility high-contrast overrides are loaded before rendered aliases are resolved. This ordering is required because `\colorlet` copies the colour value that exists at the time the alias is created.

Place custom palettes under `palettes/custom/` and select them with `design/palette = custom/name`. Set the matching `design/mode` in configuration and test paper plus slides output because Beamer requires explicit foreground and background roles in addition to page colours.
