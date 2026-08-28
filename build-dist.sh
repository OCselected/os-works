#!/bin/bash
# Build PDF + EPUB for each book via Pandoc + WeasyPrint
set -e

REPO=$(cd "$(dirname "$0")" && pwd)
DIST="$REPO/dist"
mkdir -p "$DIST"

WEASYPRINT="/home/lee/.hermes/hermes-agent/venv/bin/weasyprint"
PANDOC="pandoc"

build_book() {
    local name="$1" slug="$2" title="$3" out="$4"
    echo "=== Building $name ==="

    local src_dir="$REPO/content/$slug"
    local chapters=()
    while IFS= read -r -d '' f; do
        chapters+=("$f")
    done < <(find "$src_dir" -maxdepth 1 -name "*.md" -print0 | sort -z)

    if [ ${#chapters[@]} -eq 0 ]; then
        echo "  No chapters found"; return
    fi

    local html="$DIST/${out}.html"
    local pdf="$DIST/${out}.pdf"
    local epub="$DIST/${out}.epub"

    # Build combined HTML
    $PANDOC "${chapters[@]}" \
      -f markdown --standalone \
      --resource-path="$src_dir:$REPO" \
      --metadata title="$title" \
      --metadata author="适兕" \
      -o "$html" \
      --css="$REPO/dist/print.css" \
      --css="$REPO/themes/os-works/static/css/site.css"

    # Build PDF via WeasyPrint
    $WEASYPRINT "$html" "$pdf"

    # Build EPUB via Pandoc
    $PANDOC "${chapters[@]}" \
      -f markdown -t epub3 \
      --resource-path="$src_dir:$REPO" \
      --metadata title="$title" \
      --metadata author="适兕" \
      -o "$epub"

    echo "  HTML: $html"
    echo "  PDF:  $pdf ($(du -h "$pdf" | cut -f1))"
    echo "  EPUB: $epub ($(du -h "$epub" | cut -f1))"
}

build_book "网络财富" "network-wealth" "网络的财富：社会生产如何改变市场和自由" "network-wealth"
build_book "开源历史" "history" "开源历史：从思想到运动" "history"