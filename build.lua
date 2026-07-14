-- l3build configuration for the INSR LaTeX package.
module = "insr"

sourcefiles = {
  "tex/latex/insr/*.sty",
  "tex/latex/insr/*.cls",
  "*.tex",
  "*.bib",
  "latexmkrc",
  "README.md",
  "LICENSE",
  "CHANGELOG.md"
}
installfiles = {
  "tex/latex/insr/*.sty",
  "tex/latex/insr/*.cls"
}
docfiles = {
  "README.md",
  "CHANGELOG.md",
  "LICENSE",
  "doc/latex/insr/*.tex",
  "examples/*.tex"
}
typesetfiles = {"main.tex", "doc/latex/insr/insr-latex-manual.tex"}
typesetexe = "lualatex"
checkengines = {"luatex"}

uploadconfig = {
  pkg = "insr",
  version = "0.1.0 2026-07-14",
  author = "INSR Research Consortium",
  license = "lppl1.3c",
  summary = "LuaLaTeX framework for INSR research papers, presentations and clinical manuals",
  topic = {"class", "presentation", "multilingual", "psychology"},
  ctanPath = "/macros/luatex/latex/insr",
  repository = "https://github.com/INSR-Research-Publishing-System/INSR-Research-Publishing-System",
  bugtracker = "https://github.com/INSR-Research-Publishing-System/INSR-Research-Publishing-System/issues",
  description = [[
The package provides a LuaLaTeX-first framework for Integrative Neuro-Somatic
Recalibration (INSR) research documents. It includes shared corporate design,
multilingual LTR/RTL support, APA bibliography defaults, acronym handling,
scientific paper, Beamer and clinical manual classes, and Overleaf/GitHub build
support.
]]
}
