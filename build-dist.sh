#!/bin/bash
# Build PDF + EPUB for each book via Pandoc + WeasyPrint.
# Chapter order is derived from assets/<slug>/SUMMARY.md.
#
# Usage:
#   bash build-dist.sh                    # build all books
#   bash build-dist.sh network-wealth     # build a single book
#
# Env:
#   WEASYPRINT  Path to weasyprint binary (default: system PATH)
#   PANDOC      Path to pandoc binary (default: system PATH)
set -e

REPO=$(cd "$(dirname "$0")" && pwd)
DIST="$REPO/dist"
mkdir -p "$DIST"

WEASYPRINT="${WEASYPRINT:-weasyprint}"
command -v "$WEASYPRINT" >/dev/null 2>&1 || { echo "weasyprint not found: $WEASYPRINT"; exit 1; }
PANDOC="${PANDOC:-pandoc}"
command -v "$PANDOC" >/dev/null 2>&1 || { echo "pandoc not found: $PANDOC"; exit 1; }


parse_summary_chapters() {
    # Read assets/<slug>/SUMMARY.md and output absolute file paths in order.
    # Only files that actually exist are emitted.
    local summary="$1" src_dir="$2"
    python3 - "$summary" "$src_dir" <<'PYEOF'
import re, sys
summary_path, src_dir = sys.argv[1], sys.argv[2]
with open(summary_path) as f:
    for line in f:
        # Match: * [label](path.md)  OR  5-space indent * [label](path.md)
        m = re.match(r"\s*\*\s*\[(.+?)\]\((.+?)\)", line)
        if m:
            rel = m.group(2).lstrip("./")
            print(f"{src_dir}/{rel}")
PYEOF
}


build_book() {
    local name="$1" slug="$2" title="$3" out="$4"
    echo "=== Building $name ($slug) ==="

    local src_dir="$REPO/content/$slug"
    local summary="$REPO/assets/$slug/SUMMARY.md"
    if [ ! -f "$summary" ]; then
        echo "  SUMMARY.md not found: $summary"; return
    fi

    # Read chapter list in SUMMARY.md order
    local chapters=()
    while IFS= read -r f; do
        if [ -f "$f" ]; then
            chapters+=("$f")
        else
            echo "  ⚠️  Missing chapter: $f (from SUMMARY.md)"
        fi
    done < <(parse_summary_chapters "$summary" "$src_dir")

    if [ ${#chapters[@]} -eq 0 ]; then
        echo "  No chapters found"; return
    fi

    echo "  Chapters: ${#chapters[@]}"

    local html="$DIST/${out}.html"
    local pdf="$DIST/${out}.pdf"
    local epub="$DIST/${out}.epub"

    # Build combined HTML
    "$PANDOC" "${chapters[@]}" \
      -f markdown --standalone \
      --resource-path="$src_dir:$REPO" \
      --metadata title="$title" \
      --metadata author="适兕" \
      -o "$html" \
      --css="$REPO/dist/print.css" \
      --css="$REPO/themes/os-works/static/css/site.css"

    # Build PDF via WeasyPrint
    "$WEASYPRINT" "$html" "$pdf"

    # Build EPUB via Pandoc
    "$PANDOC" "${chapters[@]}" \
      -f markdown -t epub3 \
      --resource-path="$src_dir:$REPO" \
      --metadata title="$title" \
      --metadata author="适兕" \
      -o "$epub"

    echo "  HTML: $html"
    echo "  PDF:  $pdf ($(du -h "$pdf" | cut -f1))"
    echo "  EPUB: $epub ($(du -h "$epub" | cut -f1))"
}


# 定义书籍
BOOKS=(
    "网络财富|network-wealth|网络的财富：社会生产如何改变市场和自由|network-wealth"
    "开源之史|history|开源之史：从思想到运动|history"
)

# 若命令行指定 slug，仅构建该本
if [ -n "$1" ]; then
    TARGET="$1"
    for entry in "${BOOKS[@]}"; do
        IFS='|' read -r name slug title out <<< "$entry"
        if [ "$slug" = "$TARGET" ]; then
            build_book "$name" "$slug" "$title" "$out"
            exit 0
        fi
    done
    echo "未知 book slug: $1"
    echo "可用: ${BOOKS[*]#*|}"; echo "      ${BOOKS[*]%%|*}" | sed 's/[^|]*|/  /'
    exit 1
fi

# 否则全部构建
for entry in "${BOOKS[@]}"; do
    IFS='|' read -r name slug title out <<< "$entry"
    build_book "$name" "$slug" "$title" "$out"
done
