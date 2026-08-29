#!/usr/bin/env python3
"""Fix SUMMARY.md paths to match flat content/ layout."""
import re
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).parent.parent
CONTENT = REPO / "content"

def get_existing_flat_names(section):
    """Return set of existing flat md basenames (lowercased) in content/<section>/."""
    names = set()
    d = CONTENT / section
    if not d.exists(): return names
    for f in d.iterdir():
        if f.suffix == ".md":
            names.add(f.stem.lower())
    return names

def fix_summary(section, fix_case=True, verbose=True):
    path = REPO / "assets" / section / "SUMMARY.md"
    if not path.exists():
        print(f"  ⚠️  {path} not found")
        return
    with open(path) as f:
        content = f.read()
    existing = get_existing_flat_names(section)

    # 大小写映射
    case_map = defaultdict(list)
    for name in existing:
        case_map[name].append(name)
    # 找真实文件名（用 content/<section>/ 里的原始大小写）
    real_names = {}
    for f in (CONTENT / section).iterdir():
        if f.suffix == ".md":
            real_names[f.stem.lower()] = f.stem

    def fix_one_line(line):
        m = re.match(r"(\s*)\*\s*\[(.+?)\]\((.+?)\)", line)
        if not m: return line, False
        prefix, label, rel = m.group(1), m.group(2), m.group(3)
        # 处理 dir/.md → 用 dir 作为 basename
        # 处理 dir/ 或 dir → 用 dir 作为 basename
        # 处理 xxx.md → xxx
        # 处理 xxx → xxx
        rel_stripped = rel.rstrip("/")
        if rel_stripped.endswith("/.md"):
            # dir/.md → 用 dir 部分
            rel_stripped = rel_stripped[:-4]  # 去掉 /.md
        # 现在 rel_stripped 是相对路径的最后一段（无 .md）
        if "/" in rel_stripped:
            rel_stripped = rel_stripped.split("/")[-1]
        # 去掉可能残留的 .md
        if rel_stripped.endswith(".md"):
            rel_stripped = rel_stripped[:-3]
        # 大小写匹配
        stem = rel_clean[:-3].lower()
        if stem in real_names:
            rel_clean = real_names[stem] + ".md"
        elif stem not in existing:
            if verbose:
                print(f"    ⚠️  NOT FOUND: {rel_clean}")
        return f"{prefix}* [{label}]({rel_clean})", True

    lines = content.split("\n")
    fixed = 0
    for i, line in enumerate(lines):
        new_line, changed = fix_one_line(line)
        if changed:
            lines[i] = new_line
            fixed += 1
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  ✅ {section}: fixed {fixed} paths")

if __name__ == "__main__":
    for s in ["network-wealth", "history"]:
        print(f"Fixing {s}...")
        fix_summary(s)
