$ENV{'LC_ALL'} = 'C';   # TeX Live needs an installed locale
$pdf_mode = 4;          # use lualatex
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -synctex=1 %O %S';
$biber = 'biber %O %B';
