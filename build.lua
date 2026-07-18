-- Authoritative l3build configuration for the INSR LaTeX package.
-- l3build.lua delegates here for compatibility.
module = "insr"
ctanpkg = "insr"

local version_file = io.open("insr-version.json", "r")
local version_json = version_file and version_file:read("*a") or ""
if version_file then version_file:close() end
local pkg_version = version_json:match('"version"%s*:%s*"([^"]+)"') or "0.1.0"
local pkg_date = version_json:match('"date"%s*:%s*"([^"]+)"') or "2026-07-14"
local repository = version_json:match('"repository"%s*:%s*"([^"]+)"') or "https://github.com/germ86/INSR-Research-Publishing-System"
local bugtracker = version_json:match('"bugtracker"%s*:%s*"([^"]+)"') or (repository .. "/issues")

sourcefiles = {
  "tex/latex/insr/*.sty",
  "tex/latex/insr/*.cls",
  "config/*.tex",
  "framework/**/*.tex",
  "profiles/**/*.tex",
  "palettes/**/*.tex",
  "themes/**/*.tex",
  "typography/**/*.tex",
  "i18n/*.tex",
  "content/**/*.tex",
  "templates/*.tex",
  "plugins/*.tex",
  "insr-version.json"
}

installfiles = {
  "tex/latex/insr/*.sty",
  "tex/latex/insr/*.cls"
}

textfiles = {
  "README.md",
  "CHANGELOG.md",
  "LICENSE",
  "CTAN.md",
  "insr-version.json",
  "schema/*.json",
  "docs/*.md",
  "tools/*.py"
}

binaryfiles = {}

docfiles = {
  "README.md",
  "CHANGELOG.md",
  "LICENSE",
  "CTAN.md",
  "docs/*.md",
  "doc/latex/insr/*.tex",
  "examples/**/*.tex",
  "references.bib"
}

typesetfiles = {"main.tex", "doc/latex/insr/insr-latex-manual.tex"}
typesetexe = "lualatex"
unpackexe = "luatex"
checkengines = {"luatex"}
testfiledir = "testfiles"
supportdir = "testfiles/support"
tagfiles = {"tex/latex/insr/*.sty", "tex/latex/insr/*.cls", "insr.cls"}

-- Keep runtime files in their repository-relative tree. Future TDS work can refine
-- these mappings after the non-.dtx source layout has stabilized.
tdslocations = {
  "tex/latex/insr",
  "doc/latex/insr"
}

uploadconfig = {
  pkg = "insr",
  version = pkg_version .. " " .. pkg_date,
  author = "INSR Research Consortium",
  uploader = "TODO: maintainer/uploader contact required before CTAN upload",
  license = "lppl1.3c",
  summary = "LuaLaTeX framework for INSR research papers, presentations and clinical manuals",
  topic = {"class", "presentation", "multilingual", "psychology"},
  ctanPath = "/macros/luatex/latex/insr",
  repository = repository,
  bugtracker = bugtracker,
  description = [[
The package provides a LuaLaTeX-first framework for Integrative Neuro-Somatic
Recalibration (INSR) research documents. It includes shared design systems,
multilingual LTR/RTL support, APA bibliography defaults, scientific paper,
presentation, poster and clinical manual entrypoints, and Overleaf/GitHub build
support.

CTAN upload is intentionally manual-only until maintainer/uploader contact
metadata and release governance are finalized.
]]
}
