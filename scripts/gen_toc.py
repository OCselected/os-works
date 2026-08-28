#!/usr/bin/env python3
"""Generate Hugo partial templates from SUMMARY.md files.

Reads assets/<slug>/SUMMARY.md and generates
data/<slug>/toc.md containing TOC HTML that Hugo template can inline.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
ASSETS = REPO / "assets"
DATA = REPO / "data"


def parse_summary(path: Path) -> list[dict]:
    """Parse SUMMARY.md into a list of {type, label, file} entries.

    type: 'part' | 'chapter' | 'section'
    """
    entries = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            # Part heading: ## xxx  OR  ## [xxx](file.md)
            if line.startswith("## "):
                m = re.match(r"##\s+\[(.+?)\]\((.+?)\)", line)
                if m:
                    # 链接式 part：既作为 part 标题，也作为独立页面
                    entries.append({"type": "part", "label": m.group(1)})
                else:
                    entries.append({"type": "part", "label": line[3:].strip()})
                continue
            # Chapter: * [label](path.md)
            if line.startswith("* ["):
                m = re.match(r"\*\s*\[(.+?)\]\((.+?)\)", line)
                if m:
                    entries.append({
                        "type": "chapter",
                        "label": m.group(1),
                        "file": m.group(2).lstrip("./"),
                    })
                continue
            # Section: 5-space indent * [label](path.md)
            if line.startswith("     * ["):
                m = re.match(r"\s+\*\s*\[(.+?)\]\((.+?)\)", line)
                if m:
                    entries.append({
                        "type": "section",
                        "label": m.group(1),
                        "file": m.group(2).lstrip("./"),
                    })
                continue
    return entries


def render_html(entries: list[dict], section: str) -> str:
    """Render TOC entries as HTML."""
    html = []
    for e in entries:
        if e["type"] == "part":
            html.append(f'<h2 class="toc-part">{e["label"]}</h2>')
        elif e["type"] == "chapter":
            file_path = e["file"].replace(".md", "").rstrip("/")
            html.append(
                f'<div class="toc-chapter">'
                f'<a class="toc-chapter-title" href="/{section}/{file_path}/">'
                f'{e["label"]}</a></div>'
            )
        elif e["type"] == "section":
            file_path = e["file"].replace(".md", "").rstrip("/")
            html.append(
                f'<a class="toc-section" href="/{section}/{file_path}/">'
                f'{e["label"]}</a>'
            )
    return "\n".join(html)


def main():
    DATA.mkdir(exist_ok=True)
    for summary_path in sorted(ASSETS.glob("*/SUMMARY.md")):
        slug = summary_path.parent.name
        entries = parse_summary(summary_path)
        if not entries:
            print(f"⚠️  {slug}: 空 SUMMARY.md", file=sys.stderr)
            continue
        html = render_html(entries, slug)
        out_path = DATA / slug / "toc.html"
        out_path.parent.mkdir(exist_ok=True)
        out_path.write_text(html)
        print(f"✅ {slug}: {len(entries)} entries → {out_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
