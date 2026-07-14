\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-paper}[2026/07/14 v0.2 deprecated wrapper for INSR v4]
\ClassWarningNoLine{insr-paper}{insr-paper is deprecated; use \string\documentclass{insr} with document/type=paper in config/project-config.tex}
\PassOptionsToClass{document/type=paper}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
