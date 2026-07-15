\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-manual}[2026/07/14 v0.2 deprecated wrapper for INSR v4]
\ClassWarningNoLine{insr-manual}{insr-manual is deprecated; use \string\documentclass{insr} with document/type=manual in config/project-config.tex}
\PassOptionsToClass{document/type=manual}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
