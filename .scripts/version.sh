#!/usr/bin/env bash
# Write tex/version.tex with the document version (git tag/commit) and date.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
version="$(git -C "$root" describe --tags --always --dirty 2>/dev/null || echo dev)"
printf '\\newcommand{\\wersja}{%s}\n\\newcommand{\\datawersji}{%s}\n' \
  "${version//_/\\_}" "$(date +%Y-%m-%d)" > "$root/tex/version.tex"
cat "$root/tex/version.tex"
