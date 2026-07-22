\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-paper}[2026/07/17 INSR paper document class]
\PassOptionsToClass{document/type=paper,output/target=paper}{insr}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{insr}}
\ProcessOptions\relax
\LoadClass{insr}
