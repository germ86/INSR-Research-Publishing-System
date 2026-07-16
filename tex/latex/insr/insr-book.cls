\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-book}[2026/07/16 INSR book document class]
\PassOptionsToClass{document/type=book}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
