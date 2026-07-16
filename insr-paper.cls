\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-paper}[2026/07/16 INSR paper document class]
\PassOptionsToClass{document/type=paper}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
