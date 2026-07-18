# Plugin dependency model

Plugins are registered with `\insr_plugin_register:nn` and loaded publicly with `\INSRUsePlugin{name}`.

Supported metadata keys include:

- `version`
- `min-core-version`
- `dependencies`
- `optional-dependencies`
- `conflicts`
- `provides`
- `init`

Loading behavior:

1. Already-loaded plugins are idempotent and produce a narrow duplicate-load warning.
2. Required dependencies load before the requesting plugin.
3. Missing dependencies produce a structured `plugin-missing-dependency` error.
4. Dependency cycles produce a structured `plugin-cycle` error.
5. Conflicts with already-loaded plugins produce a structured `plugin-conflict` error.
6. Unsupported core versions produce a structured `plugin-core-version` error.
7. Direct legacy package loading remains supported.
