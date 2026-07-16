\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-manual}[2026/07/16 INSR manual document class]
\PassOptionsToClass{document/type=manual}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
