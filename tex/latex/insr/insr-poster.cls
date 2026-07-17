\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-poster}[2026/07/17 INSR poster document class]
\PassOptionsToClass{document/type=poster,output/target=poster}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
