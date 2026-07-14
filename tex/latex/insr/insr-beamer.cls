\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-beamer}[2026/07/14 v0.1 INSR Beamer presentation class]
\DeclareOption{rtl}{\PassOptionsToPackage{rtl}{insr-base}}
\DeclareOption{python}{\PassOptionsToPackage{python}{insr-base}}
\DeclareOption{externalize}{\PassOptionsToPackage{externalize}{insr-base}}
\DeclareOption{review}{\PassOptionsToPackage{review}{insr-base}}
\DeclareOption{minted}{\PassOptionsToPackage{minted}{insr-base}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions\relax
\LoadClass{insr}
