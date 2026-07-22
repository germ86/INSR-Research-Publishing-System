\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-manual}[2026/07/17 INSR manual document class]
\PassOptionsToClass{document/type=manual,output/target=manual}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
