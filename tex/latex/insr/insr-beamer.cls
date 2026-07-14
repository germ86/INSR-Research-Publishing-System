\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-beamer}[2026/07/14 v0.2 deprecated wrapper for INSR v4]
\ClassWarningNoLine{insr-beamer}{insr-beamer is deprecated; use \string\documentclass{insr} with document/type=slides in config/project-config.tex}
\PassOptionsToClass{document/type=slides}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
