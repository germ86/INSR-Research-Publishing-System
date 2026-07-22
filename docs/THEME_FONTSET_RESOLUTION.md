# Theme and fontset resolution

Themes are registered in `config/theme-registry.tex` and activated with `\INSRUseTheme{name}` or `design/theme = name`.

Activation resolves supported theme state into:

- active theme
- palette
- typography/fontset
- header rule style
- footer rule style

Fontsets are registered in `config/fontset-registry.tex`. The registry records the intended main, sans, mono, math, fallback, scripts, and engine requirements. The typography preset files continue to perform LuaLaTeX font availability checks with deterministic fallbacks so optional fonts do not become mandatory in CI or Overleaf. When both the requested font and TeX Gyre fallback are unavailable, presets fall back to Latin Modern.

Direct `design/palette` selection remains backwards-compatible and does not require using a theme.
