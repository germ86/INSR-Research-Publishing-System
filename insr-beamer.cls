\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-beamer}[2026/07/17 INSR beamer document class]
\PassOptionsToClass{document/type=slides,output/target=slides}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
