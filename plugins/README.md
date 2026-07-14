# ISPP Plugin Lifecycle

Plugins are optional project-local `.tex` files loaded with `\INSRLoadPlugin{name}` from `plugins/name.tex`.

Lifecycle:
1. Declare only `\INSR...` public commands.
2. Avoid shell escape and mandatory external tools.
3. Fail soft: missing plugins emit a warning and compilation continues.
