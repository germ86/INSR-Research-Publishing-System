\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-poster}[2026/07/16 INSR poster document class]
\PassOptionsToClass{document/type=poster}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
