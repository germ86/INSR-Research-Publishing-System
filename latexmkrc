# Shared latexmk configuration for local, GitHub Actions and Overleaf builds.
$pdf_mode = 4; # LuaLaTeX

# In latexmk, value 2 permits bibliography generation on a clean build even when
# no .bbl file exists yet.  This is required for biblatex/Biber CI builds after
# latexmk -C.  Value 1 only processes the bibliography when a .bbl is already
# present and therefore leaves fresh builds with a Biber rerun request.
$bibtex_use = 2;
$biber = 'biber %O %B';

# Allow enough convergence passes for Biber, cross-references and LastPage.
$max_repeat = 6;

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
