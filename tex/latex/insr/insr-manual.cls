\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-manual}[2026/07/14 v0.1 INSR clinical manual class]
\DeclareOption{blindreview}{\PassOptionsToPackage{blindreview}{insr-base}}
\DeclareOption{rtl}{\PassOptionsToPackage{rtl}{insr-base}}
\DeclareOption{python}{\PassOptionsToPackage{python}{insr-base}}
\DeclareOption{externalize}{\PassOptionsToPackage{externalize}{insr-base}}
\DeclareOption{review}{\PassOptionsToPackage{review}{insr-base}}
\DeclareOption{minted}{\PassOptionsToPackage{minted}{insr-base}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax
\LoadClass[11pt,openany]{report}
\RequirePackage{insr-base}
\RequirePackage{geometry}
\geometry{a4paper,inner=3cm,outer=4cm,marginparwidth=2.7cm,marginparsep=0.5cm,top=2.6cm,bottom=2.6cm}
\RequirePackage{marginnote}
\RequirePackage{titlesec}
\titleformat{\chapter}{\sffamily\Huge\bfseries\color{INSRNavy}}{\thechapter}{0.8em}{}
\titleformat{\section}{\sffamily\Large\bfseries\color{INSRTeal}}{\thesection}{0.7em}{}
\newcommand{\INSRTherapistNote}[1]{\marginnote{\scriptsize\color{INSRTeal}\textbf{Therapist note}\par #1}}
\newenvironment{INSRFidelityChecklist}{\begin{insrclinical}{Fidelity checklist}}{\end{insrclinical}}
\newenvironment{INSRSessionProtocol}{\begin{insrmethod}{Session protocol}\begin{enumerate}[label=\textbf{Step \arabic*:},leftmargin=*]}{\end{enumerate}\end{insrmethod}}
