%% INSR Scientific Publishing Platform v4.0
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{insr}[2026/07/16 v4.0 INSR Scientific Publishing Platform]
\RequirePackage{expl3}
\RequirePackage{xparse}
\makeatletter
\def\input@path{{tex/latex/insr/}{./tex/latex/insr/}}
\makeatother
\RequirePackage{insr-core}
\RequirePackage{insr-config}
\RequirePackage{insr-metadata}
\ExplSyntaxOff
\makeatletter
\def\insr@loadproject{true}%
\def\insr@skipprojectoption{config/load-project=false}%
\@for\insr@option:=\@classoptionslist\do{%
  \ifx\insr@option\insr@skipprojectoption\def\insr@loadproject{false}\fi
}%
\def\insr@true{true}%
\ifx\insr@loadproject\insr@true
  \InputIfFileExists{config/project-config.tex}{}{\ClassWarning{insr}{Missing config/project-config.tex; using safe defaults}}%
\else
  \ClassInfo{insr}{Skipping config/project-config.tex because config/load-project=false was supplied}%
\fi
\makeatother
\ExplSyntaxOn
\DeclareOption*{\exp_args:Nno \keys_set:nn { insr } { \CurrentOption }}
\ProcessOptions\relax
\insr_resolve_document_type:
\INSRPublicAPIBanner
\typeout{INSR v4 class: root insr.cls version 2026/07/16 v4.0; git commit unavailable without shell escape}
\typeout{INSR v4 bootstrap: type=\tl_use:N\g_insr_document_type_tl, base=\tl_use:N\g_insr_base_class_tl, adapter=\tl_use:N\g_insr_adapter_tl, theme=\tl_use:N\g_insr_theme_tl, palette=\tl_use:N\g_insr_palette_tl, font=\tl_use:N\g_insr_font_tl, language=\tl_use:N\g_insr_language_tl, direction=\tl_use:N\g_insr_direction_tl, profile=\tl_use:N\g_insr_build_profile_tl}
\exp_args:NV \LoadClass \g_insr_base_class_tl
\ExplSyntaxOff
\RequirePackage{insr-utils}
\RequirePackage{insr-localization}
\RequirePackage{insr-bibliography}
\RequirePackage{insr-typography}
\RequirePackage{insr-colors}
\RequirePackage{insr-layout}
\RequirePackage{insr-frontmatter}
\RequirePackage{insr-page-style}
\RequirePackage{insr-boxes}
\RequirePackage{insr-accessibility}
\RequirePackage{insr-neuro}
\RequirePackage{insr-content}
\RequirePackage{insr-adapters}
\endinput
