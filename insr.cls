%% INSR Scientific Publishing Platform v4.0
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr}[2026/07/14 v4.0 INSR Scientific Publishing Platform]
\RequirePackage{expl3}
\RequirePackage{xparse}
\ExplSyntaxOn
\msg_new:nnn { insr } { missing-config } { Missing~config/project-config.tex;~using~safe~defaults. }
\msg_new:nnn { insr } { unknown-document-type } { Unknown~document/type~'#1'.~Valid~types:~article,~paper,~position-paper,~whitepaper,~report,~book,~monograph,~thesis,~slides,~handout,~poster,~letter,~grant,~protocol,~clinical-trial-protocol,~rct,~systematic-review,~narrative-review,~technical-documentation,~developer-documentation,~manual.~Falling~back~to~paper. }
\msg_new:nnn { insr } { unknown-palette } { Unknown~palette~'#1'.~Falling~back~to~neuroclinical.~See~palettes/*.tex. }
\msg_new:nnn { insr } { unknown-theme } { Unknown~theme~'#1'.~Falling~back~to~insr-default.~See~themes/*.tex. }
\msg_new:nnn { insr } { unknown-font } { Unknown~font~preset~'#1'.~Falling~back~to~libertinus.~See~typography/*.tex. }
\msg_new:nnn { insr } { missing-slot } { Template~slot~'#1'~is~empty;~rendering~demonstrator~content. }
\tl_new:N \g_insr_document_type_tl
\tl_new:N \g_insr_base_class_tl
\tl_new:N \g_insr_adapter_tl
\tl_new:N \g_insr_profile_tl
\tl_new:N \g_insr_template_tl
\tl_new:N \g_insr_density_tl
\tl_new:N \g_insr_build_profile_tl
\tl_new:N \g_insr_theme_tl
\tl_new:N \g_insr_palette_tl
\tl_new:N \g_insr_font_tl
\tl_new:N \g_insr_mode_tl
\tl_new:N \g_insr_language_tl
\tl_new:N \g_insr_direction_tl
\tl_new:N \g_insr_title_tl
\tl_new:N \g_insr_subtitle_tl
\tl_new:N \g_insr_short_title_tl
\tl_new:N \g_insr_date_tl
\tl_new:N \g_insr_author_tl
\tl_new:N \g_insr_institution_tl
\tl_new:N \g_insr_bibresource_tl
\tl_new:N \g_insr_keywords_tl
\bool_new:N \g_insr_high_contrast_bool
\tl_gset:Nn \g_insr_document_type_tl { paper }
\tl_gset:Nn \g_insr_density_tl { standard }
\tl_gset:Nn \g_insr_build_profile_tl { development }
\tl_gset:Nn \g_insr_theme_tl { clinical }
\tl_gset:Nn \g_insr_palette_tl { neuroclinical }
\tl_gset:Nn \g_insr_font_tl { libertinus }
\tl_gset:Nn \g_insr_mode_tl { light }
\tl_gset:Nn \g_insr_language_tl { english }
\tl_gset:Nn \g_insr_direction_tl { ltr }
\tl_gset:Nn \g_insr_title_tl { INSR~Scientific~Publishing~Platform }
\tl_gset:Nn \g_insr_subtitle_tl { LuaLaTeX-first~scientific~publishing }
\tl_gset:Nn \g_insr_short_title_tl { INSR }
\tl_gset:Nn \g_insr_date_tl { \today }
\tl_gset:Nn \g_insr_author_tl { INSR~Research~Consortium }
\tl_gset:Nn \g_insr_institution_tl { Independent~translational~research~program }
\tl_gset:Nn \g_insr_bibresource_tl { references.bib }
\tl_gset:Nn \g_insr_keywords_tl { INSR, scientific publishing, LuaLaTeX }
\keys_define:nn { insr }
  {
    document/type .tl_gset:N = \g_insr_document_type_tl,
    document/density .tl_gset:N = \g_insr_density_tl,
    document/build-profile .tl_gset:N = \g_insr_build_profile_tl,
    design/theme .tl_gset:N = \g_insr_theme_tl,
    design/palette .tl_gset:N = \g_insr_palette_tl,
    design/font .tl_gset:N = \g_insr_font_tl,
    design/mode .tl_gset:N = \g_insr_mode_tl,
    accessibility/high-contrast .bool_gset:N = \g_insr_high_contrast_bool,
    localization/language .tl_gset:N = \g_insr_language_tl,
    localization/direction .tl_gset:N = \g_insr_direction_tl,
    metadata/title .tl_gset:N = \g_insr_title_tl,
    metadata/subtitle .tl_gset:N = \g_insr_subtitle_tl,
    metadata/short-title .tl_gset:N = \g_insr_short_title_tl,
    metadata/date .tl_gset:N = \g_insr_date_tl,
    metadata/author .tl_gset:N = \g_insr_author_tl,
    metadata/institution .tl_gset:N = \g_insr_institution_tl,
    bibliography/resource .tl_gset:N = \g_insr_bibresource_tl,
    metadata/keywords .tl_gset:N = \g_insr_keywords_tl,
    content/template .tl_gset:N = \g_insr_template_tl,
    unknown .code:n = { \msg_warning:nnn { insr } { unknown-theme } { \l_keys_key_str } }
  }
\NewDocumentCommand \INSRConfigure { m } { \keys_set:nn { insr } { #1 } }
\NewDocumentCommand \INSRSetup { m } { \keys_set:nn { insr } { #1 } }
\NewDocumentCommand \INSRAuthor { O{} m m O{} O{} } { \tl_gset:Nn \g_insr_author_tl { #2 } \tl_gset:Nn \g_insr_institution_tl { #3 } }
\NewDocumentCommand \INSRInstitution { O{} m O{} } { \tl_gset:Nn \g_insr_institution_tl { #2 } }
\NewDocumentCommand \INSRLogo { O{} m m } { }
\InputIfFileExists{config/project-config.tex}{}{\msg_warning:nn { insr } { missing-config }}
\DeclareOption*{\keys_set:nn { insr } { \CurrentOption }}
\ProcessOptions\relax
\cs_new_protected:Npn \insr_resolve_document_type: {
  \str_case:VnF \g_insr_document_type_tl
    {
      { article } { \tl_gset:Nn \g_insr_base_class_tl { scrartcl } \tl_gset:Nn \g_insr_adapter_tl { article } }
      { paper } { \tl_gset:Nn \g_insr_base_class_tl { scrartcl } \tl_gset:Nn \g_insr_adapter_tl { paper } }
      { position-paper } { \tl_gset:Nn \g_insr_base_class_tl { scrartcl } \tl_gset:Nn \g_insr_adapter_tl { paper } }
      { whitepaper } { \tl_gset:Nn \g_insr_base_class_tl { scrartcl } \tl_gset:Nn \g_insr_adapter_tl { paper } }
      { report } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { report } }
      { grant } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { report } }
      { protocol } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { report } }
      { clinical-trial-protocol } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { report } }
      { rct } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { report } }
      { systematic-review } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { report } }
      { narrative-review } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { report } }
      { technical-documentation } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { report } }
      { developer-documentation } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { report } }
      { manual } { \tl_gset:Nn \g_insr_base_class_tl { scrreprt } \tl_gset:Nn \g_insr_adapter_tl { manual } }
      { book } { \tl_gset:Nn \g_insr_base_class_tl { scrbook } \tl_gset:Nn \g_insr_adapter_tl { book } }
      { monograph } { \tl_gset:Nn \g_insr_base_class_tl { scrbook } \tl_gset:Nn \g_insr_adapter_tl { book } }
      { thesis } { \tl_gset:Nn \g_insr_base_class_tl { scrbook } \tl_gset:Nn \g_insr_adapter_tl { book } }
      { slides } { \tl_gset:Nn \g_insr_base_class_tl { beamer } \tl_gset:Nn \g_insr_adapter_tl { slides } }
      { handout } { \tl_gset:Nn \g_insr_base_class_tl { beamer } \tl_gset:Nn \g_insr_adapter_tl { slides } \PassOptionsToClass{handout}{beamer} }
      { poster } { \tl_gset:Nn \g_insr_base_class_tl { beamer } \tl_gset:Nn \g_insr_adapter_tl { poster } }
      { letter } { \tl_gset:Nn \g_insr_base_class_tl { scrlttr2 } \tl_gset:Nn \g_insr_adapter_tl { letter } }
    }
    { \msg_warning:nnx { insr } { unknown-document-type } { \tl_use:N \g_insr_document_type_tl } \tl_gset:Nn \g_insr_document_type_tl { paper } \tl_gset:Nn \g_insr_base_class_tl { scrartcl } \tl_gset:Nn \g_insr_adapter_tl { paper } }
}
\insr_resolve_document_type:
\typeout{INSR~v4~bootstrap:~type=\tl_use:N\g_insr_document_type_tl,~base=\tl_use:N\g_insr_base_class_tl,~adapter=\tl_use:N\g_insr_adapter_tl,~theme=\tl_use:N\g_insr_theme_tl,~palette=\tl_use:N\g_insr_palette_tl,~font=\tl_use:N\g_insr_font_tl,~language=\tl_use:N\g_insr_language_tl,~direction=\tl_use:N\g_insr_direction_tl,~profile=\tl_use:N\g_insr_build_profile_tl}
\exp_args:NV \LoadClass \g_insr_base_class_tl
\ExplSyntaxOff

\RequirePackage{ifluatex}
\ifluatex\else\ClassError{insr}{INSR requires LuaLaTeX}{Select LuaLaTeX in Overleaf or run latexmk -lualatex locally.}\fi
\RequirePackage{fontspec}
\RequirePackage[bidi=basic,english,ngerman,arabic,hebrew]{babel}
\babelprovide[import,main]{english}
\babelprovide[import]{ngerman}
\babelprovide[import]{arabic}
\babelprovide[import]{hebrew}
\RequirePackage{xcolor}
\RequirePackage{graphicx}
\RequirePackage{booktabs,tabularx,longtable,array}
\RequirePackage{amsmath,amssymb,mathtools}
\RequirePackage{csquotes}
\RequirePackage{microtype}
\RequirePackage{hyperref}
\RequirePackage[backend=biber,style=apa,sortcites=true]{biblatex}
\RequirePackage[acronym,shortcuts]{glossaries-extra}
\RequirePackage{tikz}
\RequirePackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\@ifclassloaded{beamer}{}{\RequirePackage[a4paper,margin=2.7cm]{geometry}}
\ExplSyntaxOn
\tl_if_blank:VF \g_insr_bibresource_tl { \addbibresource{\g_insr_bibresource_tl} }
\file_if_exist_input:nF { typography/\tl_use:N\g_insr_font_tl.tex } { \msg_warning:nnx { insr } { unknown-font } { \tl_use:N\g_insr_font_tl } \file_input:n { typography/libertinus.tex } }
\file_if_exist_input:nF { palettes/\tl_use:N\g_insr_palette_tl.tex } { \msg_warning:nnx { insr } { unknown-palette } { \tl_use:N\g_insr_palette_tl } \file_input:n { palettes/neuroclinical.tex } }
\bool_if:NT \g_insr_high_contrast_bool { \file_input:n { palettes/high-contrast.tex } }
\file_if_exist_input:nF { themes/\tl_use:N\g_insr_theme_tl.tex } { \msg_warning:nnx { insr } { unknown-theme } { \tl_use:N\g_insr_theme_tl } \file_input:n { themes/insr-default.tex } }
\file_if_exist_input:n { profiles/documents/\tl_use:N\g_insr_document_type_tl.profile.tex }
\file_if_exist_input:n { framework/adapters/\tl_use:N\g_insr_adapter_tl.tex }
\selectlanguage{\g_insr_language_tl}
\hypersetup{unicode=true,colorlinks=true,linkcolor=INSRLink,citecolor=INSRLink,urlcolor=INSRLink,pdftitle={\g_insr_title_tl},pdfauthor={\g_insr_author_tl}}
\ExplSyntaxOff

\newacronym{insr}{INSR}{Integrative Neuro-Somatic Recalibration}
\newacronym{cdss}{CDSS}{Clinical Decision Support System}
\newacronym{hrv}{HRV}{heart-rate variability}
\newacronym{eda}{EDA}{electrodermal activity}

\ExplSyntaxOn
\NewDocumentCommand \INSRShowResolvedConfiguration {} {\par\small\noindent\textbf{INSR configuration:}~type=\tl_use:N\g_insr_document_type_tl;~base=\tl_use:N\g_insr_base_class_tl;~adapter=\tl_use:N\g_insr_adapter_tl;~template=\tl_use:N\g_insr_template_tl;~theme=\tl_use:N\g_insr_theme_tl;~palette=\tl_use:N\g_insr_palette_tl;~typography=\tl_use:N\g_insr_font_tl;~language=\tl_use:N\g_insr_language_tl;~direction=\tl_use:N\g_insr_direction_tl;~build=\tl_use:N\g_insr_build_profile_tl.\par}
\NewDocumentCommand \INSRMakeTitle {} { \insr_adapter_make_title: }
\NewDocumentCommand \INSRRenderDocument {} { \insr_template_render: }
\NewDocumentCommand \INSRPart { m } { \insr_adapter_part:n {#1} }
\NewDocumentCommand \INSRChapter { m } { \insr_adapter_chapter:n {#1} }
\NewDocumentCommand \INSRSection { m } { \insr_adapter_section:n {#1} }
\NewDocumentCommand \INSRSubsection { m } { \insr_adapter_subsection:n {#1} }
\NewDocumentCommand \INSRSubsubsection { m } { \insr_adapter_subsubsection:n {#1} }
\NewDocumentCommand \INSRPrintBibliography { O{} } { \insr_adapter_bibliography:n {#1} }
\cs_new_protected:Npn \insr_semantic_inline:nn #1#2 { \par\noindent\textbf{#1:}~#2\par }
\NewDocumentCommand \ResearchQuestion { m } { \insr_semantic_inline:nn { Research~question } {#1} }
\NewDocumentCommand \Hypothesis { m } { \insr_semantic_inline:nn { Hypothesis } {#1} }
\NewDocumentCommand \Objective { m } { \insr_semantic_inline:nn { Objective } {#1} }
\NewDocumentCommand \Method { m } { \insr_semantic_inline:nn { Method } {#1} }
\NewDocumentCommand \Finding { m } { \insr_semantic_inline:nn { Finding } {#1} }
\NewDocumentCommand \KeyFinding { m } { \begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSRResult,title=Key~finding]#1\end{tcolorbox} }
\NewDocumentCommand \EvidenceStatement { m } { \insr_semantic_inline:nn { Evidence } {#1} }
\NewDocumentCommand \ClinicalImplication { m } { \insr_semantic_inline:nn { Clinical~implication } {#1} }
\NewDocumentCommand \TechnicalImplication { m } { \insr_semantic_inline:nn { Technical~implication } {#1} }
\NewDocumentCommand \Limitation { m } { \insr_semantic_inline:nn { Limitation } {#1} }
\NewDocumentCommand \FutureWork { m } { \insr_semantic_inline:nn { Future~work } {#1} }
\NewDocumentCommand \Recommendation { m } { \insr_semantic_inline:nn { Recommendation } {#1} }
\NewDocumentCommand \SafetyStatement { m } { \begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSRSafety,title=Safety]#1\end{tcolorbox} }
\ExplSyntaxOff
\newenvironment{ResearchNote}{\begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSRResearch,title=Research note]}{\end{tcolorbox}}
\newenvironment{ClinicalNote}{\begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSRClinical,title=Clinical note]}{\end{tcolorbox}}
\newenvironment{EvidenceBlock}{\begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSREvidence,title=Evidence]}{\end{tcolorbox}}
\newenvironment{StudyDesignBlock}{\begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSRMethod,title=Study design]}{\end{tcolorbox}}
\newenvironment{OutcomeBlock}{\begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSRResult,title=Outcome]}{\end{tcolorbox}}
\newenvironment{LimitationBlock}{\begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSRLimitation,title=Limitation]}{\end{tcolorbox}}
\newenvironment{SafetyBox}{\begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSRSafety,title=Safety]}{\end{tcolorbox}}
\newenvironment{KeyPoint}{\begin{tcolorbox}[colback=INSRSurfaceAlt,colframe=INSRAccent,title=Key point]}{\end{tcolorbox}}
\ExplSyntaxOn
\cs_new_protected:Npn \insr_template_render: {
  \@ifclassloaded{beamer}{\insr_template_render_beamer:}{\insr_template_render_text:}
}
\cs_new_protected:Npn \insr_template_render_text: {
  \INSRChapter{Overview}
  \begin{ResearchNote}\ResearchQuestion{How can INSR maintain one source while producing class-safe scientific outputs?}\end{ResearchNote}
  \Objective{Demonstrate the configured document profile, theme, palette and typography preset.}
  \Method{The v4.0 runtime resolves document type before loading a base class, then applies adapters and design tokens.}
  \KeyFinding{Changing \texttt{config/project-config.tex} changes the output without editing \texttt{main.tex}.}
  \begin{EvidenceBlock}Semantic components use design tokens rather than raw theme colours.\end{EvidenceBlock}
  \SafetyStatement{Clinical and protocol documents preserve explicit safety labels in addition to colour.}
  \INSRPrintBibliography
}
\cs_new_protected:Npn \insr_template_render_beamer: {
  \begin{frame}{Overview}\ResearchQuestion{How can INSR maintain one source while producing class-safe scientific outputs?}\Objective{Demonstrate the configured document profile, theme, palette and typography preset.}\end{frame}
  \begin{frame}{Adapter-safe structure}\KeyFinding{\texttt{main.tex} never changes; the selected adapter comes from configuration.}\begin{EvidenceBlock}Beamer receives frames, while paper/report/book receive sectioning commands.\end{EvidenceBlock}\end{frame}
  \begin{frame}{Safety}\SafetyStatement{Status information is labelled and bordered, not represented by colour alone.}\end{frame}
  \INSRPrintBibliography
}
\ExplSyntaxOff

\ExplSyntaxOn
\NewDocumentCommand \INSRAbstract { m } { \@ifclassloaded{beamer}{\begin{frame}{Abstract}#1\end{frame}}{\begin{abstract}#1\end{abstract}} }
\NewDocumentCommand \INSRKeywords { o } { \par\noindent\textbf{Keywords:~}\tl_use:N\g_insr_keywords_tl\par }
\NewDocumentCommand \INSRDeclarations {} { \par\noindent\textbf{Declarations:}~No conflicts declared for the demonstrator.\par }
\NewDocumentCommand \INSRBeginDocument {} { \selectlanguage{\g_insr_language_tl} }
\NewDocumentCommand \INSRContentUnit { m m m m m m } { \@ifclassloaded{beamer}{\begin{frame}{#1}#4\par\medskip\alert{#5}\end{frame}}{#3\par} }
\NewDocumentCommand \INSRKeyMessage { m } { \KeyFinding{#1} }
\NewDocumentCommand \INSRNote { m } { \@ifclassloaded{beamer}{\note{#1}}{\marginpar{\scriptsize #1}} }
\NewDocumentCommand \INSRAltFigure { O{} m m } { \begin{figure}[htbp]\centering #3\caption[#1]{#2}\end{figure} }
\NewDocumentCommand \INSRRTL { m } { \foreignlanguage{arabic}{#1} }
\NewDocumentCommand \INSRLTR { m } { \foreignlanguage{english}{#1} }
\NewDocumentCommand \INSRMixed { m m } { \foreignlanguage{#1}{#2} }
\NewDocumentCommand \INSRLoadPlugin { m } { \InputIfFileExists{plugins/#1.tex}{}{\ClassWarning{insr}{Plugin '#1' not found; continuing}} }
\NewDocumentCommand \INSRClinicalStop { m } { \SafetyStatement{Clinical hard-stop: #1} }
\NewDocumentCommand \INSRSomaticHold { m } { \SafetyStatement{Somatic hold: #1} }
\ExplSyntaxOff
