\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-handout}[2026/07/16 INSR handout document class]
\PassOptionsToClass{document/type=handout}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
