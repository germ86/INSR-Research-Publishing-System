# Plugin author guide

Plugins may be loaded publicly with:

```tex
\INSRUsePlugin{neuro}
```

First-party plugins are registered in `config/plugin-registry.tex` with the internal API `\insr_plugin_register:nn`. Direct package loading remains supported for compatibility; the registry is the preferred future extension point.

A plugin record should describe name, version, package or content module, and supported targets. Dependency and conflict enforcement will be expanded without changing the public loading command.
