#!/bin/sh
set -eu

export PATH="/Users/rainbow/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export TEXINPUTS="vendor-tex-deps//:official-template//:"
export BSTINPUTS="official-template//:"
export BIBINPUTS=".:"
export TFMFONTS="vendor-tex-fonts/fonts/tfm//:"
export VFFONTS="vendor-tex-fonts/fonts/vf//:"
export T1FONTS="vendor-tex-fonts/fonts/type1//:"

latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error frontiers-manuscript.tex
