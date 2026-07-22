#!/usr/bin/env bash
# build-paper — compile a problem's paper.tex → paper.pdf (the ShouqiaoW/erdos
# layout). Installs a minimal TeX toolchain on first run. Verifies the PDF.
#   usage: bash scripts/build-paper.sh <slug>
set -euo pipefail
dir="${1:?usage: build-paper.sh <problem-folder>}"
tex="$dir/paper.tex"
[ -f "$tex" ] || { echo "no paper.tex in $dir"; exit 1; }

if ! command -v pdflatex >/dev/null 2>&1; then
  echo "[build-paper] installing texlive (first run)…"
  if command -v apt-get >/dev/null 2>&1; then
    (sudo apt-get update -qq && sudo apt-get install -y -qq \
       texlive-latex-base texlive-latex-recommended texlive-latex-extra \
       texlive-science latexmk) \
      || (apt-get update -qq && apt-get install -y -qq \
       texlive-latex-base texlive-latex-recommended texlive-latex-extra \
       texlive-science latexmk) \
      || { echo "[build-paper] texlive install failed"; exit 1; }
  fi
fi

cd "$dir"
# two passes for refs; latexmk if present else raw pdflatex
if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex >/tmp/paper-build.log 2>&1 \
    || { echo "[build-paper] BUILD FAILED — tail:"; tail -25 /tmp/paper-build.log; exit 1; }
  latexmk -c >/dev/null 2>&1 || true
else
  pdflatex -interaction=nonstopmode -halt-on-error paper.tex >/tmp/paper-build.log 2>&1
  pdflatex -interaction=nonstopmode -halt-on-error paper.tex >/tmp/paper-build.log 2>&1 \
    || { echo "[build-paper] BUILD FAILED — tail:"; tail -25 /tmp/paper-build.log; exit 1; }
fi

[ -f paper.pdf ] && [ "$(stat -f%z paper.pdf 2>/dev/null || stat -c%s paper.pdf)" -gt 3000 ] \
  || { echo "[build-paper] paper.pdf missing/too small"; exit 1; }
echo "[build-paper] OK → $dir/paper.pdf"
