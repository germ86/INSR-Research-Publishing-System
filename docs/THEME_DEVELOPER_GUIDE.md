# Theme Developer Guide

Themes control layout and component rendering. They do not define semantic colours; palettes do that. A theme may load another theme first to inherit its behaviour and then override spacing, headers, footers, Beamer navigation, block styles or title rendering.

Create custom themes under `themes/`. Use semantic colour names such as `INSRPrimary`, `INSRSurfaceAlt`, `INSRRule`, and `INSRSafety`. Do not hard-code palette-specific colour names in content.
