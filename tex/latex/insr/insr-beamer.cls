\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr-beamer}[2026/07/14 v0.1 INSR Beamer presentation class]
\DeclareOption{rtl}{\PassOptionsToPackage{rtl}{insr-base}}
\DeclareOption{python}{\PassOptionsToPackage{python}{insr-base}}
\DeclareOption{externalize}{\PassOptionsToPackage{externalize}{insr-base}}
\DeclareOption{review}{\PassOptionsToPackage{review}{insr-base}}
\DeclareOption{minted}{\PassOptionsToPackage{minted}{insr-base}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions\relax
\LoadClass[aspectratio=169,professionalfonts]{beamer}
\RequirePackage{insr-base}
\usetheme{default}
\usefonttheme{professionalfonts}
\setbeamertemplate{navigation symbols}{}
\setbeamercolor{normal text}{fg=INSRGraphite,bg=white}
\setbeamercolor{frametitle}{fg=white,bg=INSRNavy}
\setbeamercolor{title}{fg=INSRNavy}
\setbeamercolor{structure}{fg=INSRTeal}
\setbeamercolor{alerted text}{fg=INSRAmber!80!black}
\setbeamertemplate{frametitle}{\nointerlineskip\begin{beamercolorbox}[wd=\paperwidth,ht=2.8ex,dp=1.1ex,leftskip=1em]{frametitle}\insertframetitle\end{beamercolorbox}}
\setbeamertemplate{footline}{\leavevmode\hbox{\begin{beamercolorbox}[wd=.78\paperwidth,ht=2.5ex,dp=1ex,leftskip=1em]{author in head/foot}\usebeamerfont{author in head/foot}\INSRShort{} — \insertshorttitle\end{beamercolorbox}\begin{beamercolorbox}[wd=.22\paperwidth,ht=2.5ex,dp=1ex,center]{date in head/foot}\insertframenumber{} / \inserttotalframenumber\end{beamercolorbox}}}
\newcommand{\INSRSectionFrame}[1]{\begin{frame}[plain]\centering\vfill{\Huge\sffamily\bfseries\color{INSRNavy}#1}\vfill\end{frame}}
\newenvironment{INSRTakeaway}{\begin{insrbox}{Take-away}}{\end{insrbox}}
