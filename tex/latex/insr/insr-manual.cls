\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-manual}[2026/07/14 v0.1 INSR clinical manual class]
\DeclareOption{blindreview}{\PassOptionsToPackage{blindreview}{insr-base}}
\DeclareOption{rtl}{\PassOptionsToPackage{rtl}{insr-base}}
\DeclareOption{python}{\PassOptionsToPackage{python}{insr-base}}
\DeclareOption{review}{\PassOptionsToPackage{review}{insr-base}}
\DeclareOption{minted}{\PassOptionsToPackage{minted}{insr-base}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax
\LoadClass{insr}
