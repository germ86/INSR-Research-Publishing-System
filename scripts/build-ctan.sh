#!/usr/bin/env bash
set -euo pipefail

pkg="insr-latex"
version="0.1.0"
outdir="dist/${pkg}-${version}"
rm -rf dist
mkdir -p "$outdir/tex/latex/insr" "$outdir/doc/latex/insr" "$outdir/examples" "$outdir/.github/workflows"
cp tex/latex/insr/* "$outdir/tex/latex/insr/"
cp doc/latex/insr/* "$outdir/doc/latex/insr/"
cp examples/*.tex "$outdir/examples/"
cp README.md CHANGELOG.md LICENSE build.lua latexmkrc main.tex references.bib "$outdir/"
cp .github/workflows/latex.yml "$outdir/.github/workflows/"
( cd dist && zip -qr "${pkg}-${version}.zip" "${pkg}-${version}" )
echo "Created dist/${pkg}-${version}.zip"
