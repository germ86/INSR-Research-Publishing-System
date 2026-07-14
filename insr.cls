%% INSR Scientific Publishing Platform v4.0
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr}[2026/07/14 v4.0 INSR Scientific Publishing Platform]
\RequirePackage{expl3}
\RequirePackage{xparse}
\ExplSyntaxOn
\msg_new:nnn { insr } { unknown-option } { Unknown~INSR~class~option~'#1'.~Using~safe~defaults. }
\msg_new:nnn { insr } { unknown-document-type } { Unknown~document-type~'#1'.~Falling~back~to~paper/article. }
\msg_new:nnn { insr } { missing-config } { Missing~config/project-config.tex.~Using~safe~defaults. }
\msg_new:nnn { insr } { missing-plugin } { Plugin~'#1'~not~found.~Continuing. }
\tl_new:N \g_insr_document_type_tl
\tl_new:N \g_insr_language_tl
\tl_new:N \g_insr_direction_tl
\tl_new:N \g_insr_theme_tl
\tl_new:N \g_insr_palette_tl
\tl_new:N \g_insr_fontset_tl
\tl_new:N \g_insr_title_tl
\tl_new:N \g_insr_subtitle_tl
\tl_new:N \g_insr_shorttitle_tl
\tl_new:N \g_insr_date_tl
\tl_new:N \g_insr_bibresource_tl
\tl_new:N \g_insr_keywords_tl
\tl_new:N \g_insr_funding_tl
\tl_new:N \g_insr_ethics_tl
\tl_new:N \g_insr_registration_tl
\tl_new:N \g_insr_declarations_tl
\tl_new:N \g_insr_correspondence_tl
\tl_new:N \g_insr_pdfsubject_tl
\bool_new:N \g_insr_python_bool
\bool_new:N \g_insr_high_contrast_bool
\seq_new:N \g_insr_author_seq
\seq_new:N \g_insr_institution_seq
\seq_new:N \g_insr_logo_seq
\tl_gset:Nn \g_insr_document_type_tl { paper }
\tl_gset:Nn \g_insr_language_tl { english }
\tl_gset:Nn \g_insr_direction_tl { ltr }
\tl_gset:Nn \g_insr_theme_tl { clinical }
\tl_gset:Nn \g_insr_palette_tl { default }
\tl_gset:Nn \g_insr_fontset_tl { libertinus }
\tl_gset:Nn \g_insr_date_tl { \today }
\tl_gset:Nn \g_insr_bibresource_tl { references.bib }
\keys_define:nn { insr/setup }
  {
    document-type .tl_gset:N = \g_insr_document_type_tl,
    type .tl_gset:N = \g_insr_document_type_tl,
    language .tl_gset:N = \g_insr_language_tl,
    direction .tl_gset:N = \g_insr_direction_tl,
    theme .tl_gset:N = \g_insr_theme_tl,
    palette .tl_gset:N = \g_insr_palette_tl,
    fontset .tl_gset:N = \g_insr_fontset_tl,
    title .tl_gset:N = \g_insr_title_tl,
    subtitle .tl_gset:N = \g_insr_subtitle_tl,
    short-title .tl_gset:N = \g_insr_shorttitle_tl,
    date .tl_gset:N = \g_insr_date_tl,
    bibliography .tl_gset:N = \g_insr_bibresource_tl,
    keywords .tl_gset:N = \g_insr_keywords_tl,
    funding .tl_gset:N = \g_insr_funding_tl,
    ethics .tl_gset:N = \g_insr_ethics_tl,
    registration .tl_gset:N = \g_insr_registration_tl,
    declarations .tl_gset:N = \g_insr_declarations_tl,
    correspondence .tl_gset:N = \g_insr_correspondence_tl,
    pdfsubject .tl_gset:N = \g_insr_pdfsubject_tl,
    python .bool_gset:N = \g_insr_python_bool,
    high-contrast .bool_gset:N = \g_insr_high_contrast_bool,
    unknown .code:n = { \msg_warning:nnn { insr } { unknown-option } { \l_keys_key_str } }
  }
\NewDocumentCommand \INSRSetup { m } { \keys_set:nn { insr/setup } { #1 } }
\NewDocumentCommand \INSRAuthor { O{} m m O{} O{} } { \seq_gput_right:Nn \g_insr_author_seq { {#1}{#2}{#3}{#4}{#5} } }
\NewDocumentCommand \INSRInstitution { O{} m O{} } { \seq_gput_right:Nn \g_insr_institution_seq { {#1}{#2}{#3} } }
\NewDocumentCommand \INSRLogo { O{} m m } { \seq_gput_right:Nn \g_insr_logo_seq { {#1}{#2}{#3} } }
\DeclareOption*{\msg_warning:nnn { insr } { unknown-option } { \CurrentOption }}
\ProcessOptions\relax
\InputIfFileExists{config/project-config.tex}{}{\msg_warning:nn { insr } { missing-config }}
\str_case:VnF \g_insr_document_type_tl
  {
    { paper } { \input{adapters/insr-adapter-paper.tex} }
    { slides } { \input{adapters/insr-adapter-slides.tex} }
    { presentation } { \input{adapters/insr-adapter-slides.tex} }
    { protocol } { \input{adapters/insr-adapter-protocol.tex} }
    { manual } { \input{adapters/insr-adapter-manual.tex} }
    { report } { \input{adapters/insr-adapter-report.tex} }
    { thesis } { \input{adapters/insr-adapter-thesis.tex} }
    { poster } { \input{adapters/insr-adapter-poster.tex} }
    { letter } { \input{adapters/insr-adapter-letter.tex} }
  }
  { \msg_warning:nnx { insr } { unknown-document-type } { \tl_use:N \g_insr_document_type_tl } \tl_gset:Nn \g_insr_document_type_tl { paper } \input{adapters/insr-adapter-paper.tex} }
\ExplSyntaxOff
\RequirePackage{ifluatex}
\ifluatex\else\ClassError{insr}{INSR requires LuaLaTeX}{Select LuaLaTeX. The ordinary build also needs Biber for references.}\fi
\RequirePackage{fontspec}
\RequirePackage[bidi=basic,english,ngerman,arabic,hebrew]{babel}
\babelprovide[import,main]{english}
\babelprovide[import]{ngerman}
\babelprovide[import]{arabic}
\babelprovide[import]{hebrew}
\defaultfontfeatures{Ligatures=TeX,Scale=MatchLowercase}
\IfFontExistsTF{Libertinus Serif}{\setmainfont{Libertinus Serif}}{\setmainfont{TeX Gyre Pagella}}
\IfFontExistsTF{Fira Sans}{\setsansfont{Fira Sans}}{\setsansfont{TeX Gyre Heros}}
\IfFontExistsTF{Fira Code}{\setmonofont{Fira Code}}{\setmonofont{Latin Modern Mono}}
\babelfont[arabic]{rm}[Renderer=HarfBuzz]{Amiri}
\babelfont[hebrew]{rm}[Renderer=HarfBuzz]{FreeSerif}
\RequirePackage{xcolor}
\definecolor{INSRNavy}{HTML}{0A2342}
\definecolor{INSRTeal}{HTML}{17A2B8}
\definecolor{INSRAmber}{HTML}{FFC107}
\definecolor{INSRSlate}{HTML}{F8F9FA}
\definecolor{INSRGraphite}{HTML}{343A40}
\definecolor{INSRWhite}{HTML}{FFFFFF}
\ExplSyntaxOn
\bool_if:NT \g_insr_high_contrast_bool { \colorlet{INSRTeal}{blue!70!black} \colorlet{INSRAmber}{orange!85!black} }
\ExplSyntaxOff
\RequirePackage{graphicx}
\RequirePackage{booktabs,tabularx,longtable,array}
\RequirePackage{amsmath,amssymb,mathtools}
\RequirePackage{csquotes}
\RequirePackage{microtype}
\RequirePackage{hyperref}
\RequirePackage[capitalise,nameinlink,noabbrev]{cleveref}
\RequirePackage[backend=biber,style=apa,sortcites=true]{biblatex}
\RequirePackage[acronym,shortcuts]{glossaries-extra}
\RequirePackage{tikz}
\RequirePackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\ExplSyntaxOn
\tl_if_blank:VF \g_insr_bibresource_tl { \addbibresource{\g_insr_bibresource_tl} }
\bool_if:NT \g_insr_python_bool { \IfFileExists{pyluatex.sty}{\RequirePackage{pyluatex}}{\msg_warning:nnn { insr } { unknown-option } { pyluatex-not-installed } } }
\hypersetup{unicode=true,colorlinks=true,linkcolor=INSRNavy,citecolor=INSRTeal,urlcolor=INSRTeal,pdftitle={\g_insr_title_tl},pdfsubject={\g_insr_pdfsubject_tl},pdfauthor={INSR Consortium}}
\ExplSyntaxOff
\@ifclassloaded{beamer}{
  \usetheme{default}\usefonttheme{professionalfonts}\setbeamertemplate{navigation symbols}{}
  \setbeamercolor{frametitle}{fg=white,bg=INSRNavy}\setbeamercolor{structure}{fg=INSRTeal}\setbeamercolor{alerted text}{fg=INSRAmber!80!black}
  \setbeamertemplate{footline}{\leavevmode\hbox{\begin{beamercolorbox}[wd=.82\paperwidth,ht=2.5ex,dp=1ex,leftskip=1em]{author in head/foot}\insertshorttitle\end{beamercolorbox}\begin{beamercolorbox}[wd=.18\paperwidth,ht=2.5ex,dp=1ex,center]{date in head/foot}\insertframenumber/\inserttotalframenumber\end{beamercolorbox}}}
}{\RequirePackage[a4paper,margin=2.7cm]{geometry}}
\ExplSyntaxOn
\cs_new_protected:Npn \insr_apply_title: {
  \tl_if_blank:NF \g_insr_title_tl { \title{\g_insr_title_tl} }
  \tl_if_blank:NF \g_insr_date_tl { \date{\g_insr_date_tl} }
  \seq_if_empty:NF \g_insr_author_seq { \author{\seq_use:Nn \g_insr_author_seq { \and }} }
}
\NewDocumentCommand \INSRMakeTitle {} { \insr_apply_title: \maketitle \INSRPrintLogos }
\NewDocumentCommand \INSRPrintLogos {} { \seq_map_inline:Nn \g_insr_logo_seq { \insr_logo_render:nnn ##1 } }
\cs_new_protected:Npn \insr_logo_render:nnn #1#2#3 { \IfFileExists{#2}{\includegraphics[height=1.2cm]{#2}}{\fbox{\footnotesize #1}}\quad }
\NewDocumentCommand \INSRAbstract { m } { \begin{abstract}#1\end{abstract} }
\NewDocumentCommand \INSRKeywords {} { \tl_if_blank:NF \g_insr_keywords_tl { \par\noindent\textbf{Keywords:~}\g_insr_keywords_tl\par } }
\NewDocumentCommand \INSRDeclarations {} { \tl_if_blank:NF \g_insr_funding_tl { \section*{Funding}\g_insr_funding_tl } \tl_if_blank:NF \g_insr_ethics_tl { \section*{Ethics}\g_insr_ethics_tl } \tl_if_blank:NF \g_insr_registration_tl { \section*{Registration}\g_insr_registration_tl } \tl_if_blank:NF \g_insr_declarations_tl { \section*{Declarations}\g_insr_declarations_tl } }
\NewDocumentCommand \INSRPrintBibliography { O{} } { \@ifclassloaded{beamer}{\begin{frame}[allowframebreaks]{References}\printbibliography[#1]\end{frame}}{\printbibliography[#1]} }
\NewDocumentCommand \INSRSection { m } { \@ifclassloaded{beamer}{\begin{frame}[plain]\centering\vfill{\Huge\sffamily\bfseries\color{INSRNavy}#1}\vfill\end{frame}}{\section{#1}} }
\NewDocumentCommand \INSRSubsection { m } { \@ifclassloaded{beamer}{\begin{frame}[plain]\centering\Large #1\end{frame}}{\subsection{#1}} }
\NewDocumentCommand \INSRIfTargetTF { m m m } { \str_if_eq:VnTF \g_insr_document_type_tl {#1} {#2} {#3} }
\NewDocumentCommand \INSRContentUnit { m m m m m m } { \INSRIfTargetTF{slides}{\begin{frame}{#1}#4\par\medskip\alert{#5}\end{frame}}{#3\par} }
\NewDocumentCommand \INSRKeyMessage { m } { \begin{tcolorbox}[colback=INSRTeal!8,colframe=INSRTeal,title=Key~message]#1\end{tcolorbox} }
\NewDocumentCommand \INSRNote { m } { \marginpar{\scriptsize #1} }
\NewDocumentCommand \INSRAltFigure { O{} m m } { \begin{figure}[htbp]\centering #3\caption[#1]{#2}\end{figure} }
\NewDocumentCommand \INSRRTL { m } { \foreignlanguage{arabic}{#1} }
\NewDocumentCommand \INSRLTR { m } { \foreignlanguage{english}{#1} }
\NewDocumentCommand \INSRMixed { m m } { \foreignlanguage{#1}{#2} }
\NewDocumentCommand \INSRLoadPlugin { m } { \InputIfFileExists{plugins/#1.tex}{}{\msg_warning:nnn { insr } { missing-plugin } {#1}} }
\NewDocumentCommand \INSRClinicalStop { m } { \textcolor{red!70!black}{\textbf{Clinical~hard-stop:~}#1} }
\NewDocumentCommand \INSRSomaticHold { m } { \textcolor{INSRAmber!80!black}{\textbf{Somatic~hold:~}#1} }
\NewDocumentCommand \INSRBeginDocument {} { \selectlanguage{\g_insr_language_tl} }
\newacronym{insr}{INSR}{Integrative Neuro-Somatic Recalibration}
\newacronym{cptsd}{C-PTSD}{Complex Posttraumatic Stress Disorder}
\newacronym{hrv}{HRV}{heart-rate variability}
\newacronym{eda}{EDA}{electrodermal activity}
\ExplSyntaxOff
