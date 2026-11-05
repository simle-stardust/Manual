#!/usr/bin/env bash
# Build the manual PDF from LaTeX sources in tex/.
#
# Prerequisites: TeX Live with latexmk (see .scripts/shell.nix), e.g. on Debian/Ubuntu:
#   sudo apt install latexmk texlive-latex-extra texlive-pictures texlive-science \
#                    texlive-lang-polish texlive-fonts-recommended lmodern tex-gyre
# Optional (regenerate figures from data/ and assets/): python3 with matplotlib, Pillow, geopandas<1.0
#   python3 .scripts/plots.py && python3 .scripts/photos.py
#
# Output: pdf/Stardust-NEXT-Manual.pdf

set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
"$root/.scripts/version.sh"
mkdir -p "$root/pdf"
cd "$root/tex"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf "$root/pdf/Stardust-NEXT-Manual.pdf"
echo "PDF: $root/pdf/Stardust-NEXT-Manual.pdf"
