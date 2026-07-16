# INSR Release Guide

This guide covers the local alpha-release preparation workflow. It prepares files only; it does not publish, tag, upload or create platform releases.

## Gates

Before preparing a release candidate, run the static validators, metadata export, release preparation and, in a TeX-enabled environment, the full LuaLaTeX matrix.

```bash
python3 tools/overleaf_doctor.py check
python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py
python3 -m unittest
python3 tools/insr_metadata.py validate
python3 tools/insr_metadata.py export-all --outdir build/metadata
python3 tools/insr_release.py prepare --version v1.0.0-alpha.1
```

A PDF file is not considered successful unless `latexmk` exits with code 0. Expected negative tests, such as production placeholder failures, must be asserted explicitly.

## Metadata exports

`tools/insr_metadata.py` reads the central TeX configuration files and author registry. It can export `CITATION.cff`, DataCite JSON, CodeMeta JSON and a Zenodo metadata preview. A pending DOI is intentionally omitted from identifier exports.

## Release package

`tools/insr_release.py prepare --version <version>` writes `dist/insr-<version>/`, copies source/configuration/reference-publication files, exports metadata, and creates `release-manifest.json` with SHA-256 checksums. Generated LaTeX intermediates and Python caches are excluded.

## Golden reference

`examples/reference-publication/` is the neutral golden-reference project. It demonstrates publication metadata, authors, ORCID, CRediT, citations, bibliography, tables, figures, appendix and paper/slides/handout/poster entry points without scientific or clinical claims.

## Known external warning policy

Do not globally suppress LaTeX warnings. If TeX Live reports `Command \showhyphens has changed` during Microtype initialization, classify it only after recording the Microtype package version, LaTeX kernel date, exact command and removal criterion in the release notes.
