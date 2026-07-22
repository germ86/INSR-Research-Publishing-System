#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KEEP="${INSR_KEEP_INSTALLED_TEST:-0}"
WORKDIR="$(mktemp -d)"

cleanup() {
  if [[ "$KEEP" != "1" ]]; then
    rm -rf "$WORKDIR"
  else
    echo "INSR installed-package test workdir: $WORKDIR" >&2
  fi
}
trap cleanup EXIT

cd "$ROOT"
rm -rf build insr-ctan.zip
l3build ctan >/tmp/insr-installed-l3build-ctan.log 2>&1

TDS_ZIP="$ROOT/build/distrib/tds/insr.tds.zip"
if [[ ! -f "$TDS_ZIP" ]]; then
  echo "missing TDS archive: $TDS_ZIP" >&2
  exit 1
fi

TEXMFHOME="$WORKDIR/texmf"
CONSUMER="$WORKDIR/consumer"
mkdir -p "$TEXMFHOME" "$CONSUMER"
unzip -q "$TDS_ZIP" -d "$TEXMFHOME"
mktexlsr "$TEXMFHOME" >/dev/null 2>&1 || true

export TEXMFHOME
unset TEXINPUTS BIBINPUTS BSTINPUTS LUAINPUTS

resolve_report="$WORKDIR/kpsewhich-report.txt"
(
  cd "$CONSUMER"
  for f in \
    insr.cls \
    insr-core.sty \
    insr-config.sty \
    config/target-registry.tex \
    config/theme-registry.tex \
    config/fontset-registry.tex \
    config/plugin-registry.tex \
    framework/adapters/paper.tex \
    profiles/documents/position-paper.profile.tex \
    templates/scientific-presentation.tex \
    palettes/neuroclinical.tex \
    typography/inter.tex \
    i18n/english.tex
  do
    resolved="$(kpsewhich "$f" || true)"
    if [[ -z "$resolved" ]]; then
      echo "missing runtime file via kpsewhich: $f" >&2
      exit 1
    fi
    case "$resolved" in
      "$TEXMFHOME"/*) ;;
      *) echo "repository leakage or wrong TEXMF resolution for $f: $resolved" >&2; exit 1 ;;
    esac
    printf '%s -> %s\n' "$f" "$resolved"
  done
) | tee "$resolve_report"

make_fixture() {
  local name="$1"
  local config="$2"
  local body="${3:-Installed package fixture.}"
  mkdir -p "$CONSUMER/$name"
  cat >"$CONSUMER/$name/main.tex" <<EOF
\documentclass[config/load-project=false]{insr}
\INSRConfigure{$config}
\begin{document}
\INSRMakeTitle
$body
\end{document}
EOF
  : >"$CONSUMER/$name/references.bib"
}

make_fixture minimal-paper 'build/preset=position-paper, metadata/title={Installed Minimal Paper}, design/theme=medical, typography/fontset=inter'
make_fixture slides 'build/preset=slides, metadata/title={Installed Slides}, design/theme=presentation'
make_fixture handout 'build/preset=handout, metadata/title={Installed Handout}, design/theme=minimal'
make_fixture poster 'build/preset=poster, metadata/title={Installed Poster}, design/theme=technical'
make_fixture rct-protocol 'build/preset=rct-protocol, metadata/title={Installed RCT Protocol}, design/theme=clinical' '\INSRUsePlugin{rct}Installed RCT protocol fixture.'
make_fixture multilingual 'build/preset=position-paper, metadata/title={Installed Multilingual}, localization/language=english, design/theme=academic' 'Unicode fixture: English, Deutsch, العربية, עברית.'

mkdir -p "$CONSUMER/bibliography"
cat >"$CONSUMER/bibliography/main.tex" <<'EOF'
\documentclass[config/load-project=false]{insr}
\INSRConfigure{build/preset=position-paper, metadata/title={Installed Bibliography}, bibliography/resource=references.bib}
\begin{document}
\INSRMakeTitle
Bibliography fixture with a citation~\cite{fixture2026}.
\printbibliography
\end{document}
EOF
cat >"$CONSUMER/bibliography/references.bib" <<'EOF'
@article{fixture2026,
  author = {Example, Ada},
  title = {Installed Package Fixture},
  journal = {Journal of Test Fixtures},
  year = {2026}
}
EOF

for d in minimal-paper slides handout poster rct-protocol multilingual bibliography; do
  (
    cd "$CONSUMER/$d"
    latexmk -lualatex -interaction=nonstopmode -halt-on-error main.tex >/tmp/insr-installed-$d.log 2>&1
    if grep -E "($ROOT|TEXINPUTS=|BIBINPUTS=)" main.fls >/dev/null 2>&1; then
      echo "repository path leaked into $d file list" >&2
      exit 1
    fi
  )
done

echo "installed package test passed"
