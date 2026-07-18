# JSON configuration guide

INSR accepts a deterministic, non-executable JSON project configuration through the developer CLI:

```bash
python3 tools/insr_cli.py configure project.json -o generated-insr-config.tex
```

The schema is versioned in `schema/insr-project.schema.json`. Unknown top-level fields are rejected. Supported initial sections are:

- `schema_version`: currently `1.0`.
- `project.title` and `project.language`.
- `build.preset`, validated against `config/target-registry.tex`.
- `design.theme`, validated against checked-in themes and generic registry themes.
- `typography.fontset`.
- `metadata.authors[].name`, `metadata.authors[].orcid`, and affiliations.

Generated TeX includes a header stating that it is generated and escapes TeX-sensitive characters. JSON values are data only and are not embedded as executable TeX.
