# INSR Scientific Publishing Platform (ISPP v4.0)

ISPP v4.0 is a greenfield LuaLaTeX scientific publishing framework for INSR research. It exposes one public class, `insr.cls`, one public root document, `main.tex`, and one central configuration file, `config/project-config.tex`.

## Architecture

- **Two-phase bootstrap:** `insr.cls` defines configuration commands, reads `config/project-config.tex`, then selects the safe base class adapter (`article`, `beamer`, `report`, `book`, or `letter`).
- **Safe Overleaf core:** the ordinary build requires only LuaLaTeX and Biber. No shell escape, Python, Node.js, network access, or external binary is mandatory.
- **Single-source semantics:** `\INSRContentUnit` can emit full text for article-like outputs and compact frames for slides from the same source.
- **Namespaced API:** public commands use the `\INSR...` prefix.
- **Internationalization:** `babel` and LuaLaTeX provide LTR, RTL, and mixed-direction helpers.
- **Accessibility:** metadata and semantic figure commands are built into the public API.
- **Templates and plugins:** project-local templates, theme manifests, localization files, and soft-failing plugins provide extension points without competing public classes.

## Corporate design

| Semantic color | Hex |
| --- | --- |
| INSR Navy | `#0A2342` |
| Somatic Teal | `#17A2B8` |
| Alert Amber | `#FFC107` |
| Clean Slate | `#F8F9FA` |

## Build

```bash
latexmk main.tex
biber main
latexmk main.tex
```

Local smoke tests:

```bash
./tests/run-tests.sh
pwsh ./tests/run-tests.ps1
```

## Repository tree

- `adapters/` — private base-class adapters for paper, slides, protocol, manual, report, thesis, poster, and letter outputs.
- `content/` — semantic content manifest and shared content units.
- `themes/` — design-token and palette extensions.
- `templates/` — working templates for paper, scientific presentation, poster, grant, protocol, RCT, systematic review, thesis, and documentation.
- `plugins/` — optional soft-failing extension modules.
- `i18n/` — localization snippets for English, German, Arabic, and Hebrew.
- `tools/` — optional offline validators and pyluatex example.
- `tests/` — shell and PowerShell local test runners.

## Public entry points

- `main.tex` — public root document.
- `insr.cls` — public class and two-phase bootstrap.
- `config/project-config.tex` — central project configuration, metadata, authors, institutions, logos, funding, ethics, declarations, bibliography, theme and language settings.

## Optional Python tooling

Python tooling is optional and never required for the core build. The class supports `python=true`, which attempts to load `pyluatex` when present. Offline validators live in `tools/` and can be run locally before Overleaf synchronization.
