#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=${DEBIAN_FRONTEND:-noninteractive}

sudo apt-get update
sudo apt-get install --no-install-recommends -y \
  latexmk \
  texlive-luatex \
  biber \
  texlive-bibtex-extra \
  texlive-latex-recommended \
  texlive-latex-extra \
  texlive-fonts-recommended \
  fonts-hosny-amiri \
  fonts-noto-core \
  fonts-noto-cjk

command -v latexmk
command -v lualatex
command -v biber
kpsewhich biblatex.sty >/dev/null
kpsewhich fontspec.sty >/dev/null
