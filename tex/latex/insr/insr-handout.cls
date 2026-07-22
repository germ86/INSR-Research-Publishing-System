\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-handout}[2026/07/17 INSR handout document class]
\PassOptionsToClass{document/type=handout,output/target=handout}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
