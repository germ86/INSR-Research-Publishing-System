$pdf_mode = 4; # LuaLaTeX, no shell escape for core ISPP builds.
$bibtex_use = 2;
$lualatex = 'lualatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
$clean_ext .= ' acn acr alg aux bbl bcf blg glg glo gls ist run.xml synctex.gz toc xdy';
