\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-paper}[2026/07/14 v0.1 INSR journal article class]
\newif\ifinsr@twocolumn
\DeclareOption{twocolumn}{\insr@twocolumntrue}
\DeclareOption{blindreview}{\PassOptionsToPackage{blindreview}{insr-base}}
\DeclareOption{python}{\PassOptionsToPackage{python}{insr-base}}
\DeclareOption{externalize}{\PassOptionsToPackage{externalize}{insr-base}}
\DeclareOption{review}{\PassOptionsToPackage{review}{insr-base}}
\DeclareOption{minted}{\PassOptionsToPackage{minted}{insr-base}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\ifinsr@twocolumn\LoadClass[10pt,twocolumn]{article}\else\LoadClass[11pt]{article}\fi
\RequirePackage{insr-base}
\RequirePackage{geometry}
\geometry{a4paper,margin=2.6cm}
\RequirePackage{titlesec}
\titleformat{\section}{\sffamily\Large\bfseries\color{INSRNavy}}{\thesection}{0.7em}{}
\titleformat{\subsection}{\sffamily\large\bfseries\color{INSRGraphite}}{\thesubsection}{0.7em}{}
\RequirePackage{abstract}
\renewcommand{\abstractnamefont}{\sffamily\bfseries\color{INSRNavy}}
\renewcommand{\abstracttextfont}{\small}
\newenvironment{INSRStructuredAbstract}{\begin{insrbox}{Structured abstract}\begin{description}[leftmargin=2.8cm,style=nextline]}{\end{description}\end{insrbox}}
\newcommand{\INSRKeywords}[1]{\par\noindent\textbf{Keywords:} #1\par}
\newcommand{\INSRFunding}[1]{\ifinsr@blindreview\else\section*{Funding}#1\fi}
\newcommand{\INSRAcknowledgements}[1]{\ifinsr@blindreview\else\section*{Acknowledgements}#1\fi}
