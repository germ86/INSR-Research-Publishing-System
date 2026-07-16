# Release Checklist

1. Run all static validators and unit tests.
2. Run full `latexmk -lualatex` builds for root, examples, fixtures and documentation.
3. Check `.log`, `.blg` and `.ilg` files for warnings.
4. Verify Overleaf upload excludes generated files.
5. Confirm Zenodo metadata: DOI status, repository, license, version and citation recommendation.
6. Tag the release and publish artifacts only after CI passes.
