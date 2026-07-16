# Overleaf Guide

Compile with LuaLaTeX. For publication-ready manuscripts, use the public `insr` class and configure front matter in the document class options or `\INSRConfigure`. Example:

```tex
\documentclass[config/load-project=false,document/type=paper,publication/doi={pending}]{insr}
\begin{document}
\INSRMakeTitle
\section{Introduction}
...
\end{document}
```

Blind review builds use `publication/review=blind` or `publication/review=double-blind` and require no content changes.

## Compatibility checks

Before uploading to Overleaf, run `python3 tools/overleaf_doctor.py check` and ensure every official example uses `config/load-project=false`. Generated LaTeX files (`.aux`, `.log`, `.toc`, `.bcf`, `.run.xml`) should not be uploaded as source files.
