# Public API reference

| Interface | Kind | Status | Replacement |
| --- | --- | --- | --- |
| `\INSRConfigure{...}` | configuration command | stable | n/a |
| `\INSRBootstrap{...}` | pre-class bootstrap command | stable | n/a |
| `\INSRMetadata{...}` | metadata command | stable | n/a |
| `\INSRUseTheme{theme}` | theme activation command | stable | n/a |
| `\INSRUsePlugin{plugin}` | plugin activation command | stable | n/a |
| `\INSRSelectTarget{target}` | compatibility command | deprecated | `\INSRConfigure{build/preset = ...}` or canonical target keys |

Canonical key namespaces include `build/*`, `document/*`, `design/*`, `typography/*`, `metadata/*`, `bibliography/*`, `accessibility/*`, `localization/*`, `output/*`, `diagnostics/*`, and `compatibility/*`. Existing implemented keys remain accepted through the compatibility layer where present.
