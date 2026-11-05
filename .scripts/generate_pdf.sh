#!/usr/bin/env bash
# Build one PDF from all chapter files (NN_*.md) in the repository root.
#
# Prerequisites (Debian/Ubuntu):
#   sudo apt install pandoc texlive-xetex texlive-latex-extra texlive-lang-polish fonts-dejavu imagemagick
# or: nix-shell .scripts/shell.nix
#
# Output: pdf/Stardust-NEXT-Manual.pdf

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
out_dir="$root/pdf"
out_file="$out_dir/Stardust-NEXT-Manual.pdf"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT

mkdir -p "$out_dir"

# Copy chapters and downscale images, so the PDF stays small.
cp "$root"/[0-9][0-9]_*.md "$build/"
mkdir -p "$build/assets"
for img in "$root"/assets/*; do
  name="$(basename "$img")"
  if command -v convert >/dev/null 2>&1; then
    case "${name,,}" in
      *.jpg|*.jpeg) convert "$img" -auto-orient -resize '1600x1600>' -quality 80 "$build/assets/$name" ;;
      *.png)        convert "$img" -resize '1600x1600>' "$build/assets/$name" ;;
      *)            cp "$img" "$build/assets/$name" ;;
    esac
  else
    cp "$img" "$build/assets/$name"
  fi
done

version="$(git -C "$root" describe --tags --always --dirty 2>/dev/null || echo dev)"

cd "$build"
export LC_ALL=C.UTF-8
pandoc "$root/.scripts/metadata.yaml" [0-9][0-9]_*.md \
  --from markdown+lists_without_preceding_blankline \
  --pdf-engine=xelatex \
  --toc --toc-depth=2 \
  --number-sections \
  --top-level-division=chapter \
  --resource-path="$build" \
  --metadata date="Wersja $version, $(date +%Y-%m-%d)" \
  --output "$out_file"

echo "PDF: $out_file"
