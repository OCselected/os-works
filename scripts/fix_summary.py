#!/usr/bin/env python3
"""Fix broken links in SUMMARY.md files."""
import re
from pathlib import Path

REPO = Path(__file__).parent.parent
CONTENT = REPO / "content"

# 断链映射：SUMMARY.md 里写错的路径 → 实际文件名
HISTORY_FIXES = {
    "00-review-of-os-history-book-and-pape": "00-review-of-os-history-book-and-paper",
    "01-let-us-talk-os-in-high-school": "00-the-power-of-open-source",
    "03-software-solution-stack-evolve-and-os-growth": "06-the-evolution-of-open-collaboration",
    "03-01-software-solution-stack-evolve-and-os-growth": "06-03-other-open-collaboration-based-source",
    "04-03-counter-culture": "04-02-hacker-culture",
    "04-05-the-world-without-open-sourc": "04-01-free-software-and-os-movement",
    "05-00-the-economic-structure-of-intellectual-property-law": "05-business-from-freedom-to-subscription",
    "posts/history-of-open-source/06-00-hacker-culture-and-origin-collabration": "06-00-hacker-culture-and-origin-collabration",
    "07-000-free-software-foundation-introduction": "07-01-the-rise-of-linux-foundataion",
}

NETWORK_FIXES = {
    "README": "readme",  # Hugo slugifies to lowercase
}


def fix_summary(slug: str, fixes: dict):
    """Fix broken paths in assets/<slug>/SUMMARY.md."""
    path = REPO / "assets" / slug / "SUMMARY.md"
    if not path.exists():
        print(f"  skip {slug}: no SUMMARY.md")
        return
    with open(path) as f:
        content = f.read()
    original = content
    for broken, fixed in fixes.items():
        # 匹配 (path/) 或 (path.md) 或 (path.md/)
        pattern = re.compile(r"\(([^)]*" + re.escape(broken) + r"(?:\.md)?(?:/)?)(?:\)|\)*)")
        # 简单替换：直接把 broken 替换成 fixed（保留扩展名/斜杠）
        content = content.replace(broken, fixed)
    if content != original:
        with open(path, "w") as f:
            f.write(content)
        print(f"  ✅ {slug}: 修复 {len(fixes)} 处断链")
    else:
        print(f"  ⚠️  {slug}: 无变化")


def fix_draft_flags():
    """Remove draft: true from chapters referenced by SUMMARY.md."""
    for slug in ["network-wealth", "history"]:
        summary = REPO / "assets" / slug / "SUMMARY.md"
        if not summary.exists():
            continue
        # 提取所有引用的文件
        refs = set()
        with open(summary) as f:
            for line in f:
                m = re.search(r"\((\S+?)\)", line)
                if m:
                    refs.add(m.group(1).lstrip("./"))
        for ref in refs:
            md = ref if ref.endswith(".md") else ref + ".md"
            md = md.rstrip("/")
            path = CONTENT / slug / md
            if path.exists():
                with open(path) as f:
                    c = f.read()
                if "draft: true" in c:
                    c2 = c.replace("draft: true", "draft: false")
                    with open(path, "w") as f:
                        f.write(c2)
                    print(f"  📝 {slug}/{md}: draft: true → false")


if __name__ == "__main__":
    fix_summary("network-wealth", NETWORK_FIXES)
    fix_summary("history", HISTORY_FIXES)
    fix_draft_flags()
