-- l3build metadata for ISPP v4.0. Core builds require LuaLaTeX and Biber only.
module = "insr"
sourcefiles = {"insr.cls", "config/*.tex", "content/*.tex", "themes/*.tex", "plugins/*.tex", "i18n/*.tex", "examples/*.tex", "templates/*.tex", "*.tex", "*.bib"}
installfiles = {"insr.cls", "adapters/*.tex"}
docfiles = {"README.md", "examples/*.tex", "templates/*.tex"}
typesetfiles = {"main.tex"}
typesetexe = "lualatex"
checkengines = {"luatex"}
