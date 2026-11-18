#!/usr/bin/env python3
"""Render the 18 November 2026 world-news infographic to entry.png.

Pure Pillow drawing: no network, no wall-clock input, no randomness.
Running it twice produces byte-identical output (PNG encoder is
deterministic for fixed pixels). The entrypoint main.py copies the
rendered entry.png to the output directory.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 234)
INK = (20, 24, 31)
NAVY = (27, 42, 74)
NAVY_DARK = (18, 30, 56)
RED = (192, 57, 43)
RED_DARK = (150, 40, 30)
GOLD = (183, 121, 31)
GRAY = (107, 114, 128)
LIGHT = (233, 228, 216)
BLUE = (37, 99, 235)
TEAL = (13, 148, 136)
MAROON = (136, 19, 55)
AMBER = (217, 119, 6)
OLIVE = (101, 90, 40)
WHITE = (255, 255, 255)
GREEN = (22, 163, 74)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
REG = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, f, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, s, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(f.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def letterspaced(draw, x, y, s, f, fill, tracking=3):
    cx = x
    for ch in s:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += draw.textlength(ch, font=f) + tracking
    return cx


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- icons
def icon_bridge(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(52, 94, 140))
    # water
    for i, yy in enumerate((y + s - 26, y + s - 16)):
        draw.line([x + 10, yy, x + s - 10, yy], fill=(147, 197, 253), width=3)
    # deck + arch
    draw.line([x + 10, y + s - 40, x + s - 10, y + s - 40], fill=WHITE, width=5)
    draw.arc([x + 14, y + 22, x + s - 14, y + s - 28], 180, 360, fill=WHITE, width=5)
    draw.line([x + s // 2, y + 18, x + s // 2, y + s - 40], fill=WHITE, width=4)
    # strike flash on the arch
    star(draw, x + s - 26, y + 26, 10, RED)


def icon_summit(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=TEAL)
    # sun
    draw.ellipse([x + s - 34, y + 12, x + s - 12, y + 34], fill=(253, 224, 71))
    # skyline
    base = y + s - 14
    for bx, bw, bh in ((12, 16, 34), (32, 14, 48), (50, 18, 28), (72, 14, 40)):
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=WHITE)
    draw.line([x + 10, base, x + s - 10, base], fill=WHITE, width=3)


def icon_virus(draw, x, y, s):
    import math
    draw.rectangle([x, y, x + s, y + s], fill=MAROON)
    cx, cy = x + s // 2, y + s // 2
    for i in range(10):
        ang = i * math.pi / 5
        x1 = cx + 20 * math.cos(ang)
        y1 = cy + 20 * math.sin(ang)
        x2 = cx + 34 * math.cos(ang)
        y2 = cy + 34 * math.sin(ang)
        draw.line([x1, y1, x2, y2], fill=(251, 113, 133), width=4)
        draw.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=(251, 113, 133))
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(251, 113, 133))
    draw.ellipse([cx - 8, cy - 10, cx + 2, cy], fill=MAROON)
    draw.ellipse([cx + 4, cy + 4, cx + 12, cy + 12], fill=MAROON)


def icon_measles(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(254, 243, 199))
    import math
    cx, cy = x + s // 2, y + s // 2
    draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(253, 224, 171))
    for dx, dy, r in ((-16, -12, 7), (8, -18, 6), (18, 2, 8), (-6, 8, 6),
                      (2, 20, 5), (-20, 12, 5), (14, -6, 4)):
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=(220, 38, 38))


def icon_quake(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=OLIVE)
    pts = [(x + 8, y + s // 2), (x + 24, y + s // 2), (x + 32, y + 18),
           (x + 42, y + s - 18), (x + 52, y + 24), (x + 62, y + s - 22),
           (x + 70, y + s // 2), (x + s - 8, y + s // 2)]
    draw.line(pts, fill=WHITE, width=4, joint="curve")


def gulf_map(draw, x, y, w, h):
    """Stylised Persian Gulf: sand land, blue gulf, strike + drone paths."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 228, 200))
    draw.rectangle([x, y, x + w, y + h], outline=(200, 186, 150), width=2)
    # gulf water: diagonal band
    water = [(x + 30, y + h), (x + w * 0.42, y + 8), (x + w * 0.66, y + 8),
             (x + w - 8, y + h * 0.55), (x + w - 8, y + h), (x + 30, y + h)]
    draw.polygon(water, fill=(147, 197, 253))
    draw.line([(x + 30, y + h), (x + w * 0.42, y + 8)], fill=(96, 165, 250), width=2)
    # land labels
    draw.text((x + 14, y + 12), "IRAN", font=BOLD(15), fill=(120, 105, 70))
    draw.text((x + w - 62, y + h - 26), "GULF", font=BOLD(15), fill=(37, 99, 235))
    # Qeshm star (top of gulf)
    qx, qy = x + int(w * 0.52), y + 52
    star(draw, qx, qy, 13, RED)
    draw.text((qx + 16, qy - 9), "QESHM", font=BOLD(15), fill=RED_DARK)
    # Bahrain + Kuwait dots with dashed drone paths
    for (dx, dy, lab) in ((x + int(w * 0.72), y + 108, "BAHRAIN"),
                          (x + int(w * 0.60), y + 158, "KUWAIT")):
        for i in range(5):
            t0 = i / 5
            px = qx + (dx - qx) * t0
            py = qy + (dy - qy) * t0
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED_DARK)
        draw.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=RED_DARK)
        draw.text((dx + 10, dy - 8), lab, font=BOLD(14), fill=INK)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header band
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 116], fill=GOLD)
    letterspaced(d, 36, 18, "THE WORLD IN ONE DAY", BOLD(20), GOLD, tracking=4)
    d.text((36, 44), "WEDNESDAY, 18 NOVEMBER 2026", font=BOLD(50), fill=WHITE)

    # ---- hero: Gulf escalation
    hy = 132
    d.text((36, hy), "TOP STORY  —  THE GULF", font=BOLD(20), fill=RED)
    y = hy + 30
    y = draw_wrapped(d, 36, y, "U.S. strikes Iran's Qeshm Island",
                     BOLD(46), 600, INK, leading=52, max_lines=2)
    y += 6
    y = draw_wrapped(
        d, 36, y,
        "U.S. jets hit a Revolutionary Guard missile site on Qeshm Island. "
        "Iran answered with drone attacks on a U.S. radar site in Bahrain "
        "and Patriot batteries in Kuwait.",
        REG(21), 600, (55, 65, 81), leading=27, max_lines=3)
    gulf_map(d, 668, 132, 320, 236)
    d.line([36, 392, W - 36, 392], fill=(200, 190, 168), width=2)

    # ---- story grid 2x2
    d.text((36, 408), "ALSO TODAY", font=BOLD(20), fill=NAVY)
    stories = [
        (icon_bridge, "UKRAINE", "Kerch Bridge hit again",
         "Ukrainian drones and missiles struck the bridge to Crimea for a "
         "second day; part of its road span fell into the strait."),
        (icon_summit, "ASIA", "Trump, Xi and Putin to meet in Shenzhen",
         "APEC opens in Shenzhen as Trump wraps QUAD talks in Manila; the "
         "first trilateral summit is set for Thursday."),
        (icon_virus, "HEALTH", "Ebola cases more than double in Congo",
         "Over 11,000 cases and 5,400 deaths in three months; nearly three "
         "in four infected children under five die."),
        (icon_measles, "AMERICAS", "U.S. loses measles-free status",
         "After 26 years, more than 5,400 cases and 10 deaths end the "
         "elimination status the U.S. had held since 2000."),
    ]
    gx, gy = 36, 440
    cw, chh, gap = 468, 196, 16
    for i, (icon, kicker, head, body) in enumerate(stories):
        x = gx + (i % 2) * (cw + gap)
        yy = gy + (i // 2) * (chh + gap)
        d.rectangle([x, yy, x + cw, yy + chh], fill=WHITE,
                    outline=(214, 205, 188), width=2)
        icon(d, x + 14, yy + 14, 92)
        tx = x + 120
        d.text((tx, yy + 14), kicker, font=BOLD(16), fill=RED)
        ty = draw_wrapped(d, tx, yy + 36, head, BOLD(24), cw - 134, INK,
                          leading=28, max_lines=2)
        draw_wrapped(d, tx, ty + 4, body, REG(16), cw - 134, (55, 65, 81),
                     leading=20, max_lines=3)

    # ---- quake strip
    qy = gy + 2 * chh + gap + 14  # 868
    d.rectangle([36, qy, W - 36, qy + 64], fill=WHITE,
                outline=(214, 205, 188), width=2)
    icon_quake(d, 48, qy + 8, 48)
    d.text((112, qy + 8), "DISASTER", font=BOLD(16), fill=RED)
    d.text((112, qy + 28), "Magnitude 6.0 quake strikes Papua New Guinea",
           font=BOLD(22), fill=INK)

    # ---- markets ticker
    my = qy + 64 + 10  # 942
    d.rectangle([0, my, W, my + 46], fill=NAVY_DARK)
    d.text((36, my + 12), "MARKETS", font=BOLD(18), fill=GOLD)
    marks = [("S&P 500", "7,340.53", "-1.03%"), ("Nasdaq", "24,328.38", "-0.74%"),
             ("Gold", "$3,775", "-2.31%"), ("Brent", "$91.55", "-1.71%"),
             ("VIX", "25.46", "+11.13%")]
    # shrink the ticker font until the whole strip fits the band
    tsize = 18
    while tsize > 13:
        tw = 170
        for name, val, chg in marks:
            tw += (d.textlength(name + " ", font=REG(tsize))
                   + d.textlength(val + " ", font=BOLD(tsize))
                   + d.textlength(chg + "  ", font=BOLD(tsize)))
        if tw <= W - 36:
            break
        tsize -= 1
    mx = 170
    for name, val, chg in marks:
        d.text((mx, my + 12), name + " ", font=REG(tsize), fill=(203, 213, 225))
        mx += d.textlength(name + " ", font=REG(tsize))
        d.text((mx, my + 12), val + " ", font=BOLD(tsize), fill=WHITE)
        mx += d.textlength(val + " ", font=BOLD(tsize))
        col = GREEN if chg.startswith("+") else (248, 113, 113)
        d.text((mx, my + 12), chg + "  ", font=BOLD(tsize), fill=col)
        mx += d.textlength(chg + "  ", font=BOLD(tsize))

    # ---- footer
    d.text((36, H - 26),
           "Compiled from wire reports  ·  18 November 2026  ·  Drawn by program, no photos",
           font=REG(15), fill=GRAY)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
