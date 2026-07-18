# Theme author guide

Themes are activated publicly with:

```tex
\INSRUseTheme{medical}
```

First-party themes are registered in `config/theme-registry.tex` via `\insr_theme_register:nn`. Existing palette files under `palettes/` remain independently usable through `design/palette`.

Theme metadata separates palette, typography, and contrast intent so layout modules can derive header/footer separator colours from semantic palette roles instead of hard-coded global colours.
