\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-book}[2026/07/17 INSR book document class]
\PassOptionsToClass{document/type=book,output/target=book}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
