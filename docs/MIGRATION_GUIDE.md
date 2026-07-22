# INSR Migration Guide

## v4-compatible native classes

The canonical `\documentclass{insr}` entrypoint remains supported. New native class entrypoints are available for users who prefer distribution-style classes:

* `insr-paper`
* `insr-book`
* `insr-beamer`
* `insr-poster`
* `insr-handout`
* `insr-manual`

Each class delegates to the common `insr` architecture and sets the appropriate `document/type`, so existing content, adapters, configuration keys and public commands remain compatible.
