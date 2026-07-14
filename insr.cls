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
\msg_new:nnn { insr } { unknown-key } { Unknown~configuration~key~'#1'.~Ignoring~it. }
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
\tl_new:N \l_insr_author_id_tl
\tl_new:N \l_insr_author_name_tl
\tl_new:N \l_insr_author_orcid_tl
\tl_new:N \l_insr_author_roles_tl
\tl_new:N \l_insr_institution_id_tl
\tl_new:N \l_insr_institution_name_tl
\tl_new:N \l_insr_unit_id_tl
\tl_new:N \l_insr_unit_title_tl
\tl_new:N \l_insr_unit_outputs_tl
\tl_new:N \l_insr_unit_full_tl
\tl_new:N \l_insr_unit_summary_tl
\tl_new:N \l_insr_unit_key_tl
\tl_new:N \l_insr_unit_notes_tl
\seq_new:N \g_insr_author_seq
\seq_new:N \g_insr_institution_seq
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
    unknown .code:n = { \msg_warning:nnx { insr } { unknown-key } { \l_keys_key_str } }
  }
\keys_define:nn { insr/author }
  {
    id .tl_set:N = \l_insr_author_id_tl,
    name .tl_set:N = \l_insr_author_name_tl,
    short-name .code:n = {},
    orcid .tl_set:N = \l_insr_author_orcid_tl,
    email .code:n = {},
    affiliations .code:n = {},
    corresponding .code:n = {},
    equal-first .code:n = {},
    equal-senior .code:n = {},
    roles .tl_set:N = \l_insr_author_roles_tl,
    unknown .code:n = { \msg_warning:nnn { insr } { unknown-key } { author/#1 } }
  }
\keys_define:nn { insr/institution }
  {
    id .tl_set:N = \l_insr_institution_id_tl,
    name .tl_set:N = \l_insr_institution_name_tl,
    short-name .code:n = {},
    department .code:n = {},
    city .code:n = {},
    country .code:n = {},
    type .code:n = {},
    logo .code:n = {},
    logo-dark .code:n = {},
    url .code:n = {},
    unknown .code:n = { \msg_warning:nnn { insr } { unknown-key } { institution/#1 } }
  }
\keys_define:nn { insr/content-unit }
  {
    id .tl_set:N = \l_insr_unit_id_tl,
    title .tl_set:N = \l_insr_unit_title_tl,
    outputs .tl_set:N = \l_insr_unit_outputs_tl,
    unknown .code:n = { \msg_warning:nnn { insr } { unknown-key } { content-unit/#1 } }
  }
\NewDocumentCommand \INSRConfigure { m } { \keys_set:nn { insr } { #1 } }
\NewDocumentCommand \INSRSetup { m } { \keys_set:nn { insr } { #1 } }
\NewDocumentCommand \INSRAddAuthor { m } { \tl_clear:N \l_insr_author_name_tl \tl_clear:N \l_insr_author_orcid_tl \tl_clear:N \l_insr_author_roles_tl \keys_set:nn { insr/author } { #1 } \seq_gput_right:Nx \g_insr_author_seq { \tl_use:N \l_insr_author_name_tl } }
\NewDocumentCommand \INSRAddInstitution { m } { \tl_clear:N \l_insr_institution_name_tl \keys_set:nn { insr/institution } { #1 } \seq_gput_right:Nx \g_insr_institution_seq { \tl_use:N \l_insr_institution_name_tl } }
\NewDocumentCommand \INSRAuthor { O{} m m O{} O{} } { \tl_gset:Nn \g_insr_author_tl { #2 } \tl_gset:Nn \g_insr_institution_tl { #3 } \seq_gput_right:Nn \g_insr_author_seq { #2 } }
\NewDocumentCommand \INSRInstitution { O{} m O{} } { \tl_gset:Nn \g_insr_institution_tl { #2 } \seq_gput_right:Nn \g_insr_institution_seq { #2 } }
\NewDocumentCommand \INSRLogo { O{} m m } { }
\cs_new:Npn \insr_author_block: { \seq_if_empty:NTF \g_insr_author_seq { \tl_use:N \g_insr_author_tl } { \seq_use:Nn \g_insr_author_seq {,~} } }
\cs_new:Npn \insr_institution_block: { \seq_if_empty:NTF \g_insr_institution_seq { \tl_use:N \g_insr_institution_tl } { \seq_use:Nn \g_insr_institution_seq {;~} } }
\DeclareRobustCommand{\INSRMakeTitle}{%
  \ifcsname __insr_adapter_make_title:\endcsname
    \csname __insr_adapter_make_title:\endcsname
  \else
    \ClassError{insr}{Mandatory adapter title renderer missing}{The selected adapter did not define \string\__insr_adapter_make_title:.}%
  \fi}
\DeclareRobustCommand{\INSRRenderDocument}{%
  \ifcsname __insr_template_render:\endcsname
    \csname __insr_template_render:\endcsname
  \else
    \ClassWarning{insr}{INSRRenderDocument called before template finalisation; using emergency renderer}%
    \par\noindent INSR template renderer unavailable. Check the class banner for the loaded insr.cls version.\par
  \fi}
\DeclareRobustCommand{\INSRPublicAPIBanner}{%
  \typeout{INSR v4 public API exports: \\INSRMakeTitle, \\INSRRenderDocument, \\INSRShowResolvedConfiguration}%
}
\InputIfFileExists{config/project-config.tex}{}{\msg_warning:nn { insr } { missing-config }}
\DeclareOption*{\exp_args:Nno \keys_set:nn { insr } { \CurrentOption }}
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
\INSRPublicAPIBanner
\typeout{INSR~v4~class: root insr.cls version 2026/07/14 v4.0; git commit unavailable without shell escape}
\typeout{INSR~v4~bootstrap:~type=\tl_use:N\g_insr_document_type_tl,~base=\tl_use:N\g_insr_base_class_tl,~adapter=\tl_use:N\g_insr_adapter_tl,~theme=\tl_use:N\g_insr_theme_tl,~palette=\tl_use:N\g_insr_palette_tl,~font=\tl_use:N\g_insr_font_tl,~language=\tl_use:N\g_insr_language_tl,~direction=\tl_use:N\g_insr_direction_tl,~profile=\tl_use:N\g_insr_build_profile_tl}
\exp_args:NV \LoadClass \g_insr_base_class_tl
\ExplSyntaxOff
\RequirePackage{ifluatex}
\ifluatex\else\ClassError{insr}{INSR requires LuaLaTeX}{Select LuaLaTeX in Overleaf or run latexmk -lualatex locally.}\fi
\RequirePackage{fontspec}
\RequirePackage[english]{babel}
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
\cs_generate_variant:Nn \file_if_exist:nTF { V }
\cs_generate_variant:Nn \file_input:n { V }
\cs_generate_variant:Nn \tl_if_blank:nTF { V }
\cs_generate_variant:Nn \tl_if_blank:nF { V }
\cs_generate_variant:Nn \clist_if_in:nnTF { VV }
\bool_new:N \g__insr_adapter_ready_bool
\tl_new:N \l__insr_runtime_file_tl
\tl_new:N \l__insr_pdf_title_tl
\tl_new:N \l__insr_pdf_author_tl
\tl_new:N \l__insr_pdf_keywords_tl
\cs_new_protected:Npn \__insr_load_file_with_fallback:nnn #1#2#3
  {
    \tl_set:Nx \l__insr_runtime_file_tl { #1 }
    \typeout{INSR~#2:~\tl_use:N \l__insr_runtime_file_tl}
    \file_if_exist:VTF \l__insr_runtime_file_tl
      { \file_input:V \l__insr_runtime_file_tl \ExplSyntaxOn }
      { #3 \ExplSyntaxOn }
  }
\cs_new_protected:Npn \__insr_load_typography:
  { \__insr_load_file_with_fallback:nnn { typography/\tl_use:N\g_insr_font_tl.tex } { typography } { \msg_warning:nnx { insr } { unknown-font } { \tl_use:N\g_insr_font_tl } \file_input:n { typography/libertinus.tex } } }
\cs_new_protected:Npn \__insr_load_palette:
  { \__insr_load_file_with_fallback:nnn { palettes/\tl_use:N\g_insr_palette_tl.tex } { palette } { \msg_warning:nnx { insr } { unknown-palette } { \tl_use:N\g_insr_palette_tl } \file_input:n { palettes/neuroclinical.tex } } }
\cs_new_protected:Npn \__insr_load_theme:
  { \__insr_load_file_with_fallback:nnn { themes/\tl_use:N\g_insr_theme_tl.tex } { theme } { \msg_warning:nnx { insr } { unknown-theme } { \tl_use:N\g_insr_theme_tl } \file_input:n { themes/insr-default.tex } } }
\cs_new_protected:Npn \__insr_load_profile:
  { \__insr_load_file_with_fallback:nnn { profiles/documents/\tl_use:N\g_insr_document_type_tl.profile.tex } { profile } { \msg_warning:nnn { insr } { missing-slot } { profile } } }
\cs_new_protected:Npn \__insr_load_adapter:
  { \__insr_load_file_with_fallback:nnn { framework/adapters/\tl_use:N\g_insr_adapter_tl.tex } { adapter } { \msg_warning:nnn { insr } { missing-slot } { adapter } } }
\cs_new_protected:Npn \__insr_define_default_adapters:
  {
    \cs_set_protected:Npn \__insr_adapter_make_title:
      { \title{\tl_use:N\g_insr_title_tl} \author{\insr_author_block:} \date{\tl_use:N\g_insr_date_tl} \maketitle \INSRShowResolvedConfiguration }
    \cs_set_protected:Npn \__insr_adapter_part:n ##1 { \part{##1} }
    \cs_set_protected:Npn \__insr_adapter_chapter:n ##1 { \section{##1} }
    \cs_set_protected:Npn \__insr_adapter_section:n ##1 { \section{##1} }
    \cs_set_protected:Npn \__insr_adapter_subsection:n ##1 { \subsection{##1} }
    \cs_set_protected:Npn \__insr_adapter_subsubsection:n ##1 { \subsubsection{##1} }
    \cs_set_protected:Npn \__insr_adapter_bibliography:n ##1
      { \__insr_print_bibliography:n {##1} }
  }
\cs_new_protected:Npn \__insr_assert_adapter_ready:
  {
    \bool_gset_true:N \g__insr_adapter_ready_bool
    \clist_map_inline:nn
      { make_title:, part:n, chapter:n, section:n, subsection:n, subsubsection:n, bibliography:n }
      {
        \cs_if_exist:cF { __insr_adapter_##1 }
          { \bool_gset_false:N \g__insr_adapter_ready_bool \ClassError{insr}{Mandatory adapter function missing: \c_backslash_str __insr_adapter_##1}{The selected adapter is incomplete.} }
      }
  }
\cs_new_protected:Npn \__insr_select_language:
  { \exp_args:NV \selectlanguage \g_insr_language_tl }
\cs_new_protected:Npn \__insr_setup_bibliography:
  { \tl_if_blank:VF \g_insr_bibresource_tl { \exp_args:NV \addbibresource \g_insr_bibresource_tl } }
\cs_new_protected:Npn \__insr_print_bibliography:n #1
  { \tl_if_blank:VF \g_insr_bibresource_tl { \@ifpackageloaded{biblatex}{\printbibliography[#1]}{} } }
\cs_new_protected:Npn \__insr_setup_pdf_metadata:
  {
    \tl_set_eq:NN \l__insr_pdf_title_tl \g_insr_title_tl
    \tl_set_eq:NN \l__insr_pdf_author_tl \g_insr_author_tl
    \tl_set_eq:NN \l__insr_pdf_keywords_tl \g_insr_keywords_tl
    \exp_args:Nx \hypersetup { unicode=true,colorlinks=true,linkcolor=INSRLink,citecolor=INSRLink,urlcolor=INSRLink,pdftitle={\tl_use:N \l__insr_pdf_title_tl},pdfauthor={\tl_use:N \l__insr_pdf_author_tl},pdfkeywords={\tl_use:N \l__insr_pdf_keywords_tl} }
  }
\__insr_define_default_adapters:
\__insr_setup_bibliography:
\__insr_load_typography:
\__insr_load_palette:
\bool_if:NT \g_insr_high_contrast_bool { \file_input:n { palettes/high-contrast.tex } }
\__insr_load_theme:
\__insr_load_profile:
\__insr_load_adapter:
\__insr_assert_adapter_ready:
\__insr_select_language:
\__insr_setup_pdf_metadata:
\ExplSyntaxOff
\newacronym{insr}{INSR}{Integrative Neuro-Somatic Recalibration}
\newacronym{cdss}{CDSS}{Clinical Decision Support System}
\newacronym{hrv}{HRV}{heart-rate variability}
\newacronym{eda}{EDA}{electrodermal activity}
\ExplSyntaxOn
\NewDocumentCommand \INSRShowResolvedConfiguration {} {\par\small\noindent\textbf{INSR configuration:}~type=\tl_use:N\g_insr_document_type_tl;~base=\tl_use:N\g_insr_base_class_tl;~adapter=\tl_use:N\g_insr_adapter_tl;~template=\tl_use:N\g_insr_template_tl;~theme=\tl_use:N\g_insr_theme_tl;~palette=\tl_use:N\g_insr_palette_tl;~typography=\tl_use:N\g_insr_font_tl;~language=\tl_use:N\g_insr_language_tl;~direction=\tl_use:N\g_insr_direction_tl;~build=\tl_use:N\g_insr_build_profile_tl.\par}
\NewDocumentCommand \INSRPart { m } { \__insr_adapter_part:n {#1} }
\NewDocumentCommand \INSRChapter { m } { \__insr_adapter_chapter:n {#1} }
\NewDocumentCommand \INSRSection { m } { \__insr_adapter_section:n {#1} }
\NewDocumentCommand \INSRSubsection { m } { \__insr_adapter_subsection:n {#1} }
\NewDocumentCommand \INSRSubsubsection { m } { \__insr_adapter_subsubsection:n {#1} }
\NewDocumentCommand \INSRPrintBibliography { O{} } { \__insr_adapter_bibliography:n {#1} }
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
\cs_generate_variant:Nn \clist_if_in:NnTF { NV }
\cs_generate_variant:Nn \clist_if_in:nnT { nV }
\cs_generate_variant:Nn \clist_if_in:nnF { nV }
\cs_new_protected:Npn \__insr_template_render: {
  \InputIfFileExists{content/manifest.tex}{}{\ClassWarning{insr}{content/manifest.tex missing; no content rendered}}
  \INSRPrintBibliography
}
\NewDocumentCommand \INSROnlyFor { m +m } { \clist_if_in:nVT {#1} \g_insr_document_type_tl {#2} }
\NewDocumentCommand \INSRExceptFor { m +m } { \clist_if_in:nVF {#1} \g_insr_document_type_tl {#2} }
\NewDocumentCommand \INSRFullText { +m } { \tl_set:Nn \l_insr_unit_full_tl {#1} }
\NewDocumentCommand \INSRSummary { +m } { \tl_set:Nn \l_insr_unit_summary_tl {#1} }
\NewDocumentCommand \INSRKeyMessage { +m } { \tl_set:Nn \l_insr_unit_key_tl {#1} }
\NewDocumentCommand \INSRSpeakerNotes { +m } { \tl_set:Nn \l_insr_unit_notes_tl {#1} }
\NewDocumentEnvironment { INSRContentUnit } { O{} +b }
  {
    \tl_clear:N \l_insr_unit_id_tl \tl_clear:N \l_insr_unit_title_tl \tl_clear:N \l_insr_unit_outputs_tl
    \tl_clear:N \l_insr_unit_full_tl \tl_clear:N \l_insr_unit_summary_tl \tl_clear:N \l_insr_unit_key_tl \tl_clear:N \l_insr_unit_notes_tl
    \keys_set:nn { insr/content-unit } { #1 } #2 \insr_content_unit_render:
  }
  { }
\cs_new_protected:Npn \insr_content_unit_render: {
  \tl_if_blank:VTF \l_insr_unit_outputs_tl { \insr_content_unit_render_selected: } { \clist_if_in:VVTF \l_insr_unit_outputs_tl \g_insr_document_type_tl { \insr_content_unit_render_selected: } { } }
}
\cs_new_protected:Npn \insr_content_unit_render_selected: {
  \@ifclassloaded{beamer}{
    \begin{frame}{\tl_use:N \l_insr_unit_title_tl}
      \tl_if_blank:VTF \l_insr_unit_summary_tl { \tl_if_blank:VF \l_insr_unit_key_tl { \textbf{Key~message:}~\tl_use:N \l_insr_unit_key_tl } } { \tl_use:N \l_insr_unit_summary_tl }
      \tl_if_blank:VF \l_insr_unit_key_tl { \par\medskip\alert{\tl_use:N \l_insr_unit_key_tl} }
    \end{frame}
  }{
    \INSRSection{\tl_use:N \l_insr_unit_title_tl}
    \tl_if_blank:VTF \l_insr_unit_full_tl { \tl_use:N \l_insr_unit_summary_tl } { \tl_use:N \l_insr_unit_full_tl }
  }
}
\ExplSyntaxOff
\ExplSyntaxOn
\NewDocumentCommand \INSRAbstract { m } { \@ifclassloaded{beamer}{\begin{frame}{Abstract}#1\end{frame}}{\begin{abstract}#1\end{abstract}} }
\NewDocumentCommand \INSRKeywords { o } { \par\noindent\textbf{Keywords:~}\tl_use:N\g_insr_keywords_tl\par }
\NewDocumentCommand \INSRDeclarations {} { \par\noindent\textbf{Declarations:}~No conflicts declared for the demonstrator.\par }
\NewDocumentCommand \INSRBeginDocument {} { \csname __insr_select_language:\endcsname }
\NewDocumentCommand \INSRNote { m } { \@ifclassloaded{beamer}{\note{#1}}{\marginpar{\scriptsize #1}} }
\NewDocumentCommand \INSRAltFigure { O{} m m } { \begin{figure}[htbp]\centering #3\caption[#1]{#2}\end{figure} }
\NewDocumentCommand \INSRRTL { m } { \foreignlanguage{arabic}{#1} }
\NewDocumentCommand \INSRLTR { m } { \foreignlanguage{english}{#1} }
\NewDocumentCommand \INSRMixed { m m } { \foreignlanguage{#1}{#2} }
\NewDocumentCommand \INSRLoadPlugin { m } { \InputIfFileExists{plugins/#1.tex}{}{\ClassWarning{insr}{Plugin '#1' not found; continuing}} }
\NewDocumentCommand \INSRClinicalStop { m } { \SafetyStatement{Clinical hard-stop: #1} }
\NewDocumentCommand \INSRSomaticHold { m } { \SafetyStatement{Somatic hold: #1} }
\ExplSyntaxOff
