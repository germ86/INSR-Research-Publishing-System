# Shared latexmk configuration for local, GitHub Actions and Overleaf builds.
$pdf_mode = 4; # LuaLaTeX

# Let latexmk run the bibliography processor whenever the generated .bcf file
# requires it.  The previous value 2 only permitted bibliography processing in
# restricted circumstances and could leave first-build biblatex warnings and an
# unresolved LastPage reference behind even though a PDF was produced.
$bibtex_use = 1;
$biber = 'biber %O %B';

# Resolve INSR packages through the canonical root-level shims. Do not prepend
# tex/latex/insr here: loading implementation paths as package names triggers
# LaTeX package-name mismatch warnings in Overleaf and recent TeX Live releases.
$ENV{'TEXINPUTS'} = '.:./examples//:' . ($ENV{'TEXINPUTS'} || '');
$ENV{'BIBINPUTS'} = './/:' . ($ENV{'BIBINPUTS'} || '');
$lualatex = 'lualatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');
sub run_makeglossaries {
  my ($base_name) = @_;
  return system "makeglossaries \"$base_name\"";
}
$clean_ext .= ' acn acr alg aux bbl bcf blg glo gls glg nav snm vrb out ist run.xml synctex.gz toc xdy';
