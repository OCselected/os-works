#!/usr/bin/env python3
"""
gen_covers.py — 用 PIL 生成 os-works 新作品封面

风格：与现有 wealth-cover / history-cover 统一（深蓝 + 古铜金 + 中式装饰）
输出：static/book-list-cover.jpeg / static/economics-cover.jpeg /
      static/way-cover.jpeg / static/thinking-cover.jpeg
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("/home/lee/developing/os-works/static")
OUT.mkdir(parents=True, exist_ok=True)

FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

# 颜色（与 wealth/history 统一）
PRUSSIAN = (27, 59, 107)         # 深蓝
BRONZE = (180, 160, 120)         # 古铜金
CREAM = (245, 240, 225)          # 米白
INK = (30, 30, 40)               # 墨黑
BRONZE_DARK = (140, 120, 80)     # 深古铜

W, H = 1200, 1800


def load_font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_PATH
    return ImageFont.truetype(path, size, index=0)


def gradient_bg(color_top, color_bot, w=W, h=H):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(color_top[0] * (1-t) + color_bot[0] * t)
        g = int(color_top[1] * (1-t) + color_bot[1] * t)
        b = int(color_top[2] * (1-t) + color_bot[2] * t)
        d.line([(0, y), (w, y)], fill=(r, g, b))
    return img


def draw_corner_frame(img, color=BRONZE, thickness=4, margin=80, corner_len=120):
    """古铜金四角边框（与 history-cover 风格一致）"""
    d = ImageDraw.Draw(img)
    w, h = img.size
    corners = [
        # 左上
        [(margin, margin), (margin + corner_len, margin), (margin, margin + corner_len)],
        # 右上
        [(w-margin-corner_len, margin), (w-margin, margin), (w-margin, margin + corner_len)],
        # 左下
        [(margin, h-margin-corner_len), (margin, h-margin), (margin + corner_len, h-margin)],
        # 右上
        [(w-margin-corner_len, h-margin), (w-margin, h-margin), (w-margin, h-margin-corner_len)],
    ]
    for c in corners:
        d.line(c, fill=color, width=thickness)


def draw_center_decor(img, color=BRONZE, y_center=None):
    """中部装饰（小点 + 短线）"""
    d = ImageDraw.Draw(img)
    w, h = img.size
    y = y_center or h // 2
    # 中央 6 点装饰
    cx = w // 2
    for dx, dy in [(-80, 0), (-50, 0), (-20, 0), (20, 0), (50, 0), (80, 0)]:
        d.ellipse([cx+dx-3, y-3, cx+dx+3, y+3], fill=color)
    # 中央横线
    d.line([(cx-200, y), (cx-100, y)], fill=color, width=2)
    d.line([(cx+100, y), (cx+200, y)], fill=color, width=2)


def draw_text_centered(d, text, y, font, fill, w=W):
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (w - tw) // 2
    d.text((x, y), text, font=font, fill=fill)


def gen_booklist():
    """开源之书·书单 — 米白底 + 深蓝文字 + 古铜金装饰（书本堆叠意象）"""
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # 顶部深蓝窄条
    d.rectangle([0, 0, W, 140], fill=PRUSSIAN)
    # 底部深蓝窄条
    d.rectangle([0, H-140, W, H], fill=PRUSSIAN)
    # 古铜金四角边框（在米白区域）
    draw_corner_frame(img, BRONZE, thickness=3, margin=120, corner_len=100)
    # 中央书本堆叠意象（3 本竖立的书）
    book_x = W // 2 - 150
    book_y = H // 2 - 180
    for i, color in enumerate([PRUSSIAN, BRONZE_DARK, BRONZE]):
        x = book_x + i * 100
        d.rectangle([x, book_y + i*15, x+70, book_y + 280 + i*15], fill=color)
        d.rectangle([x+10, book_y + 30 + i*15, x+60, book_y + 60 + i*15], outline=CREAM, width=2)
    # 标题（中文大字）
    font_title = load_font(72, bold=True)
    draw_text_centered(d, "开源之书", H - 400, font_title, PRUSSIAN)
    # 副标题
    font_sub = load_font(48)
    draw_text_centered(d, "· 书单 ·", H - 310, font_sub, BRONZE_DARK)
    # 顶部英文
    font_en = load_font(36)
    draw_text_centered(d, "THE OPEN SOURCE WAY", 70, font_en, CREAM)
    # 底部作者
    font_author = load_font(30)
    draw_text_centered(d, "「开源之道」· 适兕", H - 70, font_author, CREAM)
    img.save(OUT / "book-list-cover.jpeg", "JPEG", quality=92)
    print("  ✅ book-list-cover.jpeg")


def gen_economics():
    """开源的经济学 — 深蓝底 + 古铜金网络节点 + 米白标题（网络节点意象）"""
    img = gradient_bg((40, 70, 130), (20, 40, 80))
    d = ImageDraw.Draw(img)
    draw_corner_frame(img, BRONZE, thickness=4, margin=80, corner_len=120)
    draw_center_decor(img, BRONZE, y_center=H//2 - 200)
    # 网络节点意象（12 个节点 + 连线）
    import random
    random.seed(42)
    nodes = []
    for _ in range(15):
        nx = random.randint(200, W-200)
        ny = random.randint(500, H-350)
        nodes.append((nx, ny))
    # 连线（节点距离 < 280）
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes[i+1:], i+1):
            dist = ((x1-x2)**2 + (y1-y2)**2) ** 0.5
            if dist < 280:
                d.line([(x1, y1), (x2, y2)], fill=BRONZE, width=1)
    # 节点（古铜金圆点）
    for (x, y) in nodes:
        d.ellipse([x-8, y-8, x+8, y+8], fill=BRONZE)
    # 标题
    font_title = load_font(72, bold=True)
    draw_text_centered(d, "开源的经济学", H - 400, font_title, CREAM)
    font_sub = load_font(42)
    draw_text_centered(d, "The Economics of Open Source", H - 310, font_sub, BRONZE)
    font_author = load_font(30)
    draw_text_centered(d, "「开源之道」· 适兕", H - 220, font_author, BRONZE)
    font_type = load_font(28)
    draw_text_centered(d, "讲义 · 在线阅读", H - 140, font_type, CREAM)
    img.save(OUT / "economics-cover.jpeg", "JPEG", quality=92)
    print("  ✅ economics-cover.jpeg")


def gen_way():
    """开源之道 — 米白底 + 深蓝标题 + 古铜金路/桥意象"""
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_corner_frame(img, BRONZE, thickness=3, margin=80, corner_len=110)
    # 中央桥/路意象（横向曲线 + 节点）
    cx = W // 2
    cy = H // 2 - 100
    # 主路径（贝塞尔近似）
    import math
    for x in range(200, W-200, 3):
        t = (x - 200) / (W - 400)
        y = cy + int(80 * math.sin(t * math.pi))
        d.point((x, y), fill=BRONZE)
        d.point((x, y+1), fill=BRONZE)
    # 路径两端圆点
    d.ellipse([190, cy-10, 210, cy+10], fill=PRUSSIAN)
    d.ellipse([W-210, cy-10, W-190, cy+10], fill=PRUSSIAN)
    # 标题
    font_title = load_font(88, bold=True)
    draw_text_centered(d, "开源之道", H - 480, font_title, PRUSSIAN)
    font_en = load_font(36)
    draw_text_centered(d, "THE OPEN SOURCE WAY", H - 380, font_en, BRONZE_DARK)
    font_author = load_font(30)
    draw_text_centered(d, "「开源之道」· 适兕", H - 280, font_author, INK)
    # 底部装饰
    d.line([(300, H - 180), (900, H - 180)], fill=BRONZE, width=2)
    font_type = load_font(28)
    draw_text_centered(d, "博客 · 思想长文", H - 230, font_type, BRONZE_DARK)
    img.save(OUT / "way-cover.jpeg", "JPEG", quality=92)
    print("  ✅ way-cover.jpeg")


def gen_thinking():
    """开源之思 — 深蓝底 + 古铜金星点 + 米白标题（思想碎片意象）"""
    img = gradient_bg((30, 50, 95), (15, 25, 55))
    d = ImageDraw.Draw(img)
    draw_corner_frame(img, BRONZE, thickness=4, margin=80, corner_len=110)
    # 中央星点（思想碎片意象）
    import random
    random.seed(13)
    cx, cy = W // 2, H // 2 - 150
    for _ in range(40):
        r = random.uniform(50, 280)
        angle = random.uniform(0, 2 * math.pi)
        x = int(cx + r * math.cos(angle))
        y = int(cy + r * math.sin(angle))
        size = random.randint(2, 6)
        d.ellipse([x-size, y-size, x+size, y+size], fill=BRONZE)
    # 中央亮点
    d.ellipse([cx-15, cy-15, cx+15, cy+15], fill=BRONZE)
    d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=CREAM)
    # 标题
    font_title = load_font(88, bold=True)
    draw_text_centered(d, "开源之思", H - 480, font_title, CREAM)
    font_sub = load_font(42)
    draw_text_centered(d, "21 篇思想札记", H - 370, font_sub, BRONZE)
    font_author = load_font(30)
    draw_text_centered(d, "「开源之道」· 适兕", H - 270, font_author, BRONZE)
    font_type = load_font(28)
    draw_text_centered(d, "在线阅读 · 无 PDF/EPUB", H - 180, font_type, CREAM)
    img.save(OUT / "thinking-cover.jpeg", "JPEG", quality=92)
    print("  ✅ thinking-cover.jpeg")


if __name__ == "__main__":
    import math  # noqa
    gen_booklist()
    gen_economics()
    gen_way()
    gen_thinking()
    print("\n全部封面生成完成")