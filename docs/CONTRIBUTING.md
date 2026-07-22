# Contributing

Before opening a pull request, run:

```bash
git diff --check
python3 tools/overleaf_doctor.py check
python3 tools/validate_project.py
python3 tools/validate_bibliography.py references.bib
python3 tools/validate_palette.py
python3 -m unittest
./tests/run-tests.sh --static-only
```

If `latexmk` and LuaLaTeX are installed, also run `./tests/run-tests.sh` to compile all official entrypoints. Do not suppress warnings; fix the INSR root cause or document genuinely external toolchain warnings.
