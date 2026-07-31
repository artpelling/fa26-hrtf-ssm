$ENV{'LC_ALL'} = 'C';   # TeX Live needs an installed locale
$pdf_mode = 4;          # use lualatex
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode %O %S';
$out_dir = 'build';

# Build nomenclature output in the configured output directory.
add_cus_dep('nlo', 'nls', 0, 'makenomenclature');
sub makenomenclature {
  return system('makeindex', '-s', 'nomencl.ist', '-o', "$_[0].nls", "$_[0].nlo");
}

# Biber runs from the manuscript directory, alongside references.bib.
$biber = 'biber --debug %O %B';
