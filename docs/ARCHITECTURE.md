# INSR Architecture

INSR is a LuaLaTeX-first scientific publishing framework built around a thin class bootstrap, reusable implementation packages, structural adapters and project-local `.tex` configuration overlays.

* `insr.cls` is the canonical public entrypoint.
* `tex/latex/insr/insr-*.sty` packages implement configuration, metadata, localization, typography, colors, layout, frontmatter, page styles, content and adapters.
* Native classes such as `insr-paper.cls` and `insr-beamer.cls` delegate to `insr.cls` and set `document/type`.
* `framework/adapters/*.tex` contains structural rendering only.
* `tex/latex/insr/insr-frontmatter.sty` owns scientific frontmatter rendering.
* `tex/latex/insr/insr-page-style.sty` owns headers, footers, separator lines and semantic page styles.
* `config/*.tex` contains project-specific values; implementation remains in `insr-config.sty`.
