# Shared latexmk configuration for local, GitHub Actions and Overleaf builds.
$pdf_mode = 4; # LuaLaTeX
$ENV{'TEXINPUTS'} = '.:./tex/latex/insr//:./examples//:' . ($ENV{'TEXINPUTS'} || '');
$ENV{'BIBINPUTS'} = '.:' . ($ENV{'BIBINPUTS'} || '');
$lualatex = 'lualatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');
sub run_makeglossaries {
  my ($base_name) = @_;
  return system "makeglossaries \"$base_name\"";
}
$clean_ext .= ' acn acr alg aux bbl bcf blg glo gls glg nav snm vrb out ist run.xml synctex.gz toc xdy';
