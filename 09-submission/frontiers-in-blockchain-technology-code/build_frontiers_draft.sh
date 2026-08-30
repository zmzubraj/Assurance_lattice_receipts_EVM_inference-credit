#!/bin/sh
set -eu

export PATH="/Users/rainbow/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export LC_ALL=C
export LANG=C
export TZ=UTC
export SOURCE_DATE_EPOCH=1787979600
export FORCE_SOURCE_DATE=1
export TEXINPUTS="vendor-tex-deps//:official-template//:"
export BSTINPUTS="official-template//:"
export BIBINPUTS=".:"
export TFMFONTS="vendor-tex-fonts/fonts/tfm//:"
export VFFONTS="vendor-tex-fonts/fonts/vf//:"
export T1FONTS="vendor-tex-fonts/fonts/type1//:"

latexmk -gg -pdf \
  -pdflatex='pdflatex -no-shell-escape %O %S' \
  -interaction=nonstopmode \
  -halt-on-error \
  -file-line-error \
  frontiers-manuscript.tex
