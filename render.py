#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page to entry.png.

Original work for make.fun news-image-20261120. Draws a newspaper
front page with PIL from the day's verified stories (see README.md for
sources). Run:  python3 render.py   -> writes entry.png (1024x1024).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)
INK = (17, 17, 17)
MUTED = (70, 70, 70)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
TEAL = (14, 116, 110)
GOLD = (180, 130, 20)
LINE = (200, 192, 175)
CARD = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_TITLE = font("DejaVuSans-Bold.ttf", 30)
F_DATE = font("DejaVuSans-Bold.ttf", 52)
F_SUB = font("DejaVuSans.ttf", 22)
F_KICK = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 34)
F_HEAD2 = font("DejaVuSans-Bold.ttf", 27)
F_HEAD3 = font("DejaVuSans-Bold.ttf", 24)
F_BODY = font("DejaVuSans.ttf", 21)
F_BODY_SM = font("DejaVuSans.ttf", 19)
F_SMALL = font("DejaVuSans-Bold.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading=28, color=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def card(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=LINE, width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=accent)


def icon_scales(d, cx, cy, s, color):
    d.line([cx, cy - s, cx, cy + s], fill=color, width=5)
    d.line([cx - s, cy - s + 8, cx + s, cy - s + 8], fill=color, width=5)
    d.line([cx - s, cy - s + 8, cx - s, cy + s - 6], fill=color, width=3)
    d.line([cx + s, cy - s + 8, cx + s, cy + s - 6], fill=color, width=3)
    d.arc([cx - s - 4, cy + s - 14, cx - s + 16, cy + s + 6], 0, 180, fill=color, width=3)
    d.arc([cx + s - 16, cy + s - 14, cx + s + 4, cy + s + 6], 0, 180, fill=color, width=3)
    d.line([cx - s, cy + s + 8, cx + s, cy + s + 8], fill=color, width=5)


def icon_flags(d, x, y, w, h):
    # Three small flags: US, China, Russia — simple stripes, labelled below.
    fw, fh = (w - 16) // 3, h
    # US
    d.rectangle([x, y, x + fw, y + fh], fill=(255, 255, 255), outline=INK, width=2)
    for i in range(4):
        d.rectangle([x, y + i * fh // 4, x + fw, y + (i + 1) * fh // 4], fill=(185, 28, 28) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + fw // 2, y + fh // 2], fill=NAVY)
    # China
    d.rectangle([x + fw + 8, y, x + 2 * fw + 8, y + fh], fill=(222, 41, 16), outline=INK, width=2)
    d.ellipse([x + fw + 14, y + 6, x + fw + 26, y + 18], fill=(255, 220, 0))
    # Russia
    rx = x + 2 * fw + 16
    d.rectangle([rx, y, rx + fw, y + fh // 3], fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([rx, y + fh // 3, rx + fw, y + 2 * fh // 3], fill=(0, 57, 166))
    d.rectangle([rx, y + 2 * fh // 3, rx + fw, y + fh], fill=(213, 0, 50))


def icon_chart(d, x, y, w, h, color):
    pts = [(x, y + h * 0.2), (x + w * 0.25, y + h * 0.35), (x + w * 0.5, y + h * 0.3),
           (x + w * 0.75, y + h * 0.7), (x + w, y + h * 0.9)]
    d.line(pts, fill=color, width=6, joint="curve")
    d.polygon([(x + w - 14, y + h * 0.9 - 14), (x + w, y + h * 0.9 + 6), (x + w - 2, y + h * 0.9 - 16)], fill=color)


def icon_bridge(d, x, y, w, h, color):
    d.arc([x, y, x + w, y + h * 2], 0, 180, fill=color, width=6)
    d.line([x, y + h, x + w, y + h], fill=color, width=5)
    for fx in (0.25, 0.5, 0.75):
        d.line([x + w * fx, y + h * 0.55, x + w * fx, y + h], fill=color, width=4)


def icon_tower(d, x, y, w, h, color):
    d.rectangle([x + w * 0.3, y, x + w * 0.7, y + h], fill=color)
    d.polygon([(x + w * 0.3, y), (x + w * 0.5, y - 14), (x + w * 0.7, y)], fill=color)
    for r in range(5):
        d.rectangle([x + w * 0.38, y + 12 + r * 14, x + w * 0.62, y + 20 + r * 14], fill=(255, 220, 120))


def icon_leaf(d, x, y, w, h, color):
    d.ellipse([x, y, x + w, y + h], fill=color)
    d.line([x + w * 0.5, y + h, x + w * 0.5, y - 6], fill=(14, 116, 110), width=4)
    d.line([x + w * 0.2, y + h * 0.4, x + w * 0.8, y + h * 0.7], fill=(255, 255, 255), width=3)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 148], fill=INK)
    d.text((32, 18), "THE WORLD IN ONE DAY", font=F_TITLE, fill=(255, 255, 255))
    d.text((32, 56), "FRIDAY 20 NOVEMBER 2026", font=F_DATE, fill=(255, 210, 60))
    d.text((32, 116), "The day's biggest stories — justice, a three-way summit, and a market sell-off",
           font=F_SUB, fill=(220, 220, 220))
    # Lead story
    card(d, 24, 168, 976, 240, RED)
    d.text((48, 186), "JUSTICE  •  THE HAGUE", font=F_KICK, fill=RED)
    icon_scales(d, 905, 250, 34, NAVY)
    y = para(d, 48, 214, "WORLD COURT: MYANMAR COMMITTED GENOCIDE", F_HEAD, 820, 40)
    para(d, 48, y + 4,
         "The International Court of Justice ruled Myanmar committed genocide against the "
         "Rohingya — the first time the court has found a state guilty of genocide. Vote 9–6. "
         "Case brought by The Gambia; the court ordered reparations.",
         F_BODY, 880, 27)
    # Row 2: summit + markets
    card(d, 24, 424, 482, 220, NAVY)
    d.text((48, 442), "POLITICS  •  SHENZHEN, CHINA", font=F_KICK, fill=NAVY)
    para(d, 48, 474, "Trump, Xi and Putin hold first three-way summit", F_HEAD2, 434, 33)
    para(d, 48, 544, "The three leaders signed a 4-point declaration on nuclear risk, UN reform, "
                      "energy supply and the ICC. It does not mention Ukraine or Iran.",
         F_BODY_SM, 434, 25)
    card(d, 518, 424, 482, 220, RED)
    d.text((542, 442), "MARKETS  •  NEW YORK", font=F_KICK, fill=RED)
    para(d, 542, 474, "Anthropic soars as markets slide", F_HEAD2, 434, 33)
    para(d, 542, 544, "Anthropic closed at $97.17, up 17% on its $83 IPO price, raising a record "
                      "$81.3bn. But the S&P 500 fell 2% — a fifth straight loss — and the Nikkei fell 4.8%.",
         F_BODY_SM, 434, 25)
    # Row 3: three stories
    boxes = [
        (24, 660, 314, 196, NAVY, "WAR  •  KYIV", "Russia hits Kyiv bridges — 8 killed",
         "Overnight strikes targeted bridges in Kyiv; 28 injured across nine regions.", icon_bridge),
        (355, 660, 314, 196, RED, "CONFLICT  •  RIYADH", "Houthi missile hits Riyadh tower",
         "A missile damaged the Saudi PIF tower in the financial district. No injuries reported.", icon_tower),
        (686, 660, 314, 196, TEAL, "CLIMATE  •  ANTALYA", "COP31 draft drops fossil-fuel phase-out",
         "The draft deal removed the call to end fossil fuels and net-zero dates.", icon_leaf),
    ]
    for x, y0, w, h, accent, kick, head, body, icon in boxes:
        card(d, x, y0, w, h, accent)
        d.text((x + 20, y0 + 16), kick, font=F_SMALL, fill=accent)
        yy = para(d, x + 20, y0 + 44, head, F_HEAD3, w - 40, 29)
        para(d, x + 20, yy + 4, body, F_BODY_SM, w - 40, 23)
    # Also today strip
    d.rectangle([24, 866, 1000, 972], fill=NAVY)
    d.text((44, 874), "ALSO TODAY", font=F_KICK, fill=(255, 210, 60))
    briefs = [
        "KENYA — Last Ebola patient discharged, 37 days after the first case.",
        "UK–EU — Youth mobility scheme agreed at the Brussels summit.",
        "POLAND — Russia violated its airspace overnight with 3 objects.",
        "GAZA — Israeli troops crossed the Yellow Line, the first incursion since the truce.",
    ]
    yy = 894
    for b in briefs:
        d.text((44, yy), "•  " + b, font=F_BODY_SM, fill=(255, 255, 255))
        yy += 18
    d.text((24, 980), "Stories reported on 20 November 2026  •  Sources: BBC, Reuters, UN News, Wall Street Journal, Human Rights Watch",
           font=F_FOOT, fill=MUTED)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
