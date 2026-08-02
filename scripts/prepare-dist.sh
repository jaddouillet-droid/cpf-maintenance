#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Pages are committed as unified HTML; rebuild only when legacy sources exist locally.
if ls _legacy_*.html >/dev/null 2>&1; then
  python3 build.py
fi

rm -rf dist
mkdir -p dist

for f in index.html entretien-pac.html installation-pac.html isolation.html contact.html about.html mentions-legales.html; do
  cp "$f" dist/
done
cp -r css js dist/

echo "Dist ready: $(find dist -type f | wc -l | tr -d ' ') files"
