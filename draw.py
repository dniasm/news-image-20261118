"""Draws entry.png: the world's news of Wednesday 18 November 2026 as one front page.

Run once with Pillow installed: python draw.py  ->  entry.png (1024 x 1024 PNG).
Everything is drawn at 2x and scaled down for clean edges. main.ts only copies the result.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
S = 2  # supersampling factor
FONTS = "C:/Windows/Fonts/"

PAPER = (246, 241, 230)
INK = (24, 26, 33)
MUTED = (92, 92, 100)
RED = (196, 38, 46)
BLUE = (34, 86, 160)
GOLD = (214, 160, 42)
GREEN = (36, 128, 84)
SEA = (120, 170, 205)
SAND = (226, 206, 160)

img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)


def font(name, size):
    return ImageFont.truetype(FONTS + name, int(size * S))


def sc(*v):
    return [int(x * S) for x in v]


def rect(x0, y0, x1, y1, fill=None, outline=None, width=1, r=0):
    d.rounded_rectangle(sc(x0, y0, x1, y1), radius=r * S, fill=fill, outline=outline, width=int(width * S))


def text(x, y, s, f, fill=INK, anchor="la"):
    d.text((x * S, y * S), s, font=f, fill=fill, anchor=anchor)


def wrap(x, y, s, f, maxw, fill=INK, gap=1.18, anchor_center=False):
    """Word-wrap s into lines no wider than maxw; returns the y below the last line."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) / S <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    lh = f.size / S * gap
    for i, ln in enumerate(lines):
        if anchor_center:
            text(x, y + i * lh, ln, f, fill, "ma")
        else:
            text(x, y + i * lh, ln, f, fill)
    return y + len(lines) * lh


def poly(pts, fill=None, outline=None, width=1):
    d.polygon([(px * S, py * S) for px, py in pts], fill=fill, outline=outline, width=int(width * S))


def line(pts, fill=INK, width=2):
    d.line([(px * S, py * S) for px, py in pts], fill=fill, width=int(width * S), joint="curve")


def dot(cx, cy, r, fill, outline=None, width=1):
    d.ellipse(sc(cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=int(width * S))


def arc_path(p0, p1, lift, n=40):
    """Points on a quadratic curve from p0 to p1 bulging upward by lift."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - lift
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * mx + t * t * p1[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * my + t * t * p1[1]) for t in (i / n for i in range(n + 1))]


def arrowhead(p_from, p_to, size, fill):
    ang = math.atan2(p_to[1] - p_from[1], p_to[0] - p_from[0])
    a, b = ang + 2.6, ang - 2.6
    poly([p_to, (p_to[0] + size * math.cos(a), p_to[1] + size * math.sin(a)),
          (p_to[0] + size * math.cos(b), p_to[1] + size * math.sin(b))], fill=fill)


def person(cx, base, h, coat, skin=(232, 196, 160), arm=None, hair=None):
    """A simple standing figure: head, suit body, legs. arm=(dx, dy) reaches one hand out."""
    head_r = h * 0.11
    dot(cx, base - h + head_r, head_r, skin)
    body_top, body_bot = base - h + head_r * 2.2, base - h * 0.42
    poly([(cx - h * 0.17, body_bot), (cx - h * 0.14, body_top), (cx + h * 0.14, body_top), (cx + h * 0.17, body_bot)], fill=coat)
    rect(cx - h * 0.13, body_bot, cx - h * 0.02, base, fill=INK)
    rect(cx + h * 0.02, body_bot, cx + h * 0.13, base, fill=INK)
    poly([(cx - h * 0.03, body_top), (cx + h * 0.03, body_top), (cx, body_top + h * 0.16)], fill=(250, 250, 250))
    if arm:
        sx = cx + (h * 0.13 if arm[0] > 0 else -h * 0.13)
        line([(sx, body_top + h * 0.06), (sx + arm[0], body_top + h * 0.06 + arm[1])], fill=coat, width=h * 0.07)
        dot(sx + arm[0], body_top + h * 0.06 + arm[1], h * 0.04, skin)
    if hair:
        draw_hair(cx, base - h + head_r, head_r, hair, skin)


def draw_hair(cx, cy, r, style, skin):
    """Each leader's hair, drawn over the head circle (centre cx, cy; radius r)."""
    if style == "xi":  # short, dense black hair, combed back with a side part
        black = (28, 28, 32)
        d.pieslice(sc(cx - r * 1.06, cy - r * 1.16, cx + r * 1.06, cy + r * 0.9), 180, 360, fill=black)
        d.ellipse(sc(cx - r * 0.78, cy - r * 0.62, cx + r * 0.78, cy + r * 0.9), fill=skin)  # high, arched hairline
        rect(cx - r * 1.04, cy - r * 0.2, cx - r * 0.8, cy + r * 0.25, fill=black)  # sideburns
        rect(cx + r * 0.8, cy - r * 0.2, cx + r * 1.04, cy + r * 0.25, fill=black)
        line([(cx - r * 0.35, cy - r * 1.05), (cx - r * 0.45, cy - r * 0.5)], fill=(70, 70, 76), width=max(1, r * 0.08))
    elif style == "trump":  # voluminous golden-blond hair swept forward over the brow
        gold, shade = (236, 196, 96), (204, 160, 64)
        d.pieslice(sc(cx - r * 1.12, cy - r * 1.3, cx + r * 1.12, cy + r * 0.8), 180, 360, fill=gold)
        poly([(cx - r * 1.12, cy - r * 0.25), (cx - r * 0.9, cy - r * 0.95), (cx + r * 0.2, cy - r * 1.25),
              (cx + r * 1.0, cy - r * 0.9), (cx + r * 1.35, cy - r * 0.3), (cx + r * 0.75, cy - r * 0.45),
              (cx - r * 0.2, cy - r * 0.5)], fill=gold)  # the forward sweep, past the brow
        line([(cx - r * 0.7, cy - r * 0.8), (cx + r * 0.3, cy - r * 1.0), (cx + r * 1.05, cy - r * 0.45)], fill=shade, width=max(1, r * 0.1))
        rect(cx - r * 1.1, cy - r * 0.3, cx - r * 0.86, cy + r * 0.2, fill=gold)  # sides
        rect(cx + r * 0.86, cy - r * 0.3, cx + r * 1.1, cy + r * 0.2, fill=gold)
    elif style == "putin":  # thin, receding light-brown hair: a fringe at the sides and back, a bare crown
        thin = (176, 150, 112)
        d.pieslice(sc(cx - r * 1.04, cy - r * 1.06, cx + r * 1.04, cy + r * 1.0), 180, 360, fill=thin)
        d.ellipse(sc(cx - r * 0.72, cy - r * 1.02, cx + r * 0.72, cy + r * 0.2), fill=skin)  # receding hairline
        rect(cx - r * 1.03, cy - r * 0.15, cx - r * 0.84, cy + r * 0.2, fill=thin)
        rect(cx + r * 0.84, cy - r * 0.15, cx + r * 1.03, cy + r * 0.2, fill=thin)


def panel(x0, y0, x1, y1, tag, tag_color):
    rect(x0, y0, x1, y1, fill=(255, 253, 248), outline=INK, width=2, r=8)
    tw = d.textlength(tag, font=F_TAG) / S + 16
    rect(x0 + 8, y0 + 8, x0 + 8 + tw, y0 + 34, fill=tag_color, r=4)
    text(x0 + 16, y0 + 12, tag, F_TAG, fill=(255, 255, 255))


F_MAST = font("georgiab.ttf", 64)
F_KICK = font("arialbd.ttf", 19)
F_SUB = font("georgiai.ttf", 21)
F_TAG = font("arialbd.ttf", 17)
F_HEAD = font("arialbd.ttf", 24)
F_BODY = font("arial.ttf", 18)
F_BIG = font("impact.ttf", 56)
F_LBL = font("arialbd.ttf", 16)
F_TICK = font("arialbd.ttf", 15)

# ---------------------------------------------------------------- masthead
text(512, 16, "THE WORLD ON WEDNESDAY", F_KICK, fill=RED, anchor="ma")
text(512, 40, "18 NOVEMBER 2026", F_MAST, anchor="ma")
line([(24, 116), (1000, 116)], width=3)
text(512, 124, "Summits in Shenzhen, missiles over the Gulf, a record AI share sale and a probe one light-day from home",
     F_SUB, fill=MUTED, anchor="ma")
line([(24, 154), (1000, 154)], width=1)

# ---------------------------------------------------------------- hero: APEC Shenzhen tarmac
hx0, hy0, hx1, hy1 = 24, 164, 1000, 470
rect(hx0, hy0, hx1, hy1, fill=(255, 253, 248), outline=INK, width=2, r=8)
# sky and tarmac inside the left art box
ax0, ay0, ax1, ay1 = hx0 + 10, hy0 + 10, 640, hy1 - 10
for i in range(int((ay1 - ay0) * S)):
    t = i / ((ay1 - ay0) * S)
    c = tuple(int(a + (b - a) * t) for a, b in zip((250, 205, 150), (252, 238, 214)))
    d.line([(ax0 * S, ay0 * S + i), (ax1 * S, ay0 * S + i)], fill=c)
ground = ay0 + 205
rect(ax0, ground, ax1, ay1, fill=(150, 150, 156))
# skyline of Shenzhen
x = ax0 + 6
for bw, bh in [(34, 70), (22, 110), (40, 85), (26, 150), (30, 95), (20, 60), (36, 125), (28, 80), (44, 100),
               (24, 140), (32, 75), (22, 55), (38, 115), (26, 90), (30, 65), (20, 105), (34, 70)]:
    rect(x, ground - bh, x + bw, ground, fill=(206, 172, 140))
    x += bw + 3
# airliner (generic) parked at left
px, py = ax0 + 30, ground - 18
poly([(px, py), (px + 300, py - 6), (px + 330, py + 10), (px + 300, py + 22), (px + 10, py + 22)], fill=(250, 250, 252), outline=INK, width=1.5)
poly([(px + 20, py), (px + 6, py - 70), (px + 40, py - 70), (px + 70, py)], fill=BLUE)
poly([(px + 130, py + 14), (px + 210, py + 14), (px + 160, py + 60), (px + 120, py + 60)], fill=(220, 222, 228), outline=INK, width=1)
for k in range(9):
    dot(px + 110 + k * 20, py + 7, 3, BLUE)
line([(px + 60, py + 15), (px + 300, py + 10)], fill=BLUE, width=3)
# airstairs and red carpet
poly([(px + 250, py + 22), (px + 262, py + 22), (px + 300, ground + 18), (px + 284, ground + 18)], fill=(180, 180, 186))
poly([(px + 290, ground + 18), (px + 330, ground + 18), (ax1 - 60, ay1), (px + 300, ay1)], fill=RED)
# Xi greeting Trump
person(470, ground + 70, 120, (40, 44, 56), arm=(26, 14), hair="xi")
person(530, ground + 70, 126, (30, 46, 90), arm=(-26, 14), hair="trump")


def name_tag(cx, y, name):
    """A white name tag with an ink border, legible over sky, skyline or carpet alike."""
    f = font("arialbd.ttf", 17)
    tw = d.textlength(name, font=f) / S
    rect(cx - tw / 2 - 7, y, cx + tw / 2 + 7, y + 24, fill=(255, 255, 255), outline=INK, width=1.5, r=5)
    text(cx, y + 3, name, f, anchor="ma")


name_tag(462, ground - 78, "XI")  # above the heads, in the open sky between the towers
name_tag(538, ground - 83, "TRUMP")
# Putin in a small inset frame: he met Xi first
rect(ax1 - 118, ay0 + 10, ax1 - 10, ay0 + 120, fill=(255, 253, 248), outline=INK, width=1.5, r=6)
person(ax1 - 64, ay0 + 102, 70, (60, 60, 64), hair="putin")
text(ax1 - 64, ay0 + 104, "PUTIN", F_LBL, anchor="ma")
# story text on the right
panel_tag = "ASIA-PACIFIC · APEC SUMMIT"
tw = d.textlength(panel_tag, font=F_TAG) / S + 16
rect(656, hy0 + 14, 656 + tw, hy0 + 40, fill=RED, r=4)
text(664, hy0 + 18, panel_tag, F_TAG, fill=(255, 255, 255))
y = wrap(656, hy0 + 54, "Xi greets Trump on the tarmac in Shenzhen", font("georgiab.ttf", 36), 330, gap=1.1)
y = wrap(656, y + 8, "Breaking protocol, China's leader meets the US president at the plane as APEC opens. "
         "Putin holds talks with Xi first; a Xi-Trump-Putin meeting is set for Thursday.", F_BODY, 330, fill=MUTED)

# ---------------------------------------------------------------- middle row
my0, my1 = 478, 760
cols = [(24, 344), (352, 672), (680, 1000)]

# Gulf
x0, x1 = cols[0]
panel(x0, my0, x1, my1, "GULF · IRAN WAR", RED)
mx0, mmy0, mx1, mmy1 = x0 + 10, my0 + 42, x1 - 10, my0 + 172
rect(mx0, mmy0, mx1, mmy1, fill=SEA, r=4)
poly([(mx0, mmy0), (mx1, mmy0), (mx1, mmy0 + 50), (mx1 - 60, mmy0 + 64), (mx0 + 150, mmy0 + 30), (mx0 + 60, mmy0 + 24), (mx0, mmy0 + 30)], fill=SAND)  # Iran
poly([(mx0, mmy0 + 46), (mx0 + 40, mmy0 + 50), (mx0 + 90, mmy0 + 80), (mx0 + 150, mmy0 + 104), (mx1 - 80, mmy0 + 110), (mx1, mmy0 + 96), (mx1, mmy1), (mx0, mmy1)], fill=SAND)  # Arabia

kw, bh_, qs = (mx0 + 32, mmy0 + 52), (mx0 + 150, mmy0 + 94), (mx1 - 70, mmy0 + 58)
dot(*kw, 6, RED, outline=INK)
dot(*bh_, 6, RED, outline=INK)
d.ellipse(sc(qs[0] - 16, qs[1] - 5, qs[0] + 16, qs[1] + 5), fill=SAND, outline=INK, width=S)
text(kw[0] - 4, kw[1] + 10, "KUWAIT", F_LBL)
text(bh_[0] - 30, bh_[1] + 10, "BAHRAIN", F_LBL)
text(qs[0] - 10, qs[1] + 10, "QESHM", F_LBL)
for tgt, src in [(kw, (mx0 + 120, mmy0 + 20)), (bh_, (mx0 + 200, mmy0 + 30))]:
    pts = arc_path(src, tgt, 34)
    line(pts, fill=RED, width=3)
    arrowhead(pts[-4], pts[-1], 12, RED)
pts = arc_path((mx1 - 10, mmy1 - 6), qs, 20)
line(pts, fill=BLUE, width=3)
arrowhead(pts[-4], pts[-1], 12, BLUE)
text(mx1 - 14, mmy1 - 24, "US STRIKE", F_LBL, fill=BLUE, anchor="ra")
text(mx0 + 8, mmy0 + 6, "IRAN", F_LBL, fill=RED)  # strikes launch from Iran's coast (top)
y = wrap(x0 + 12, my0 + 180, "Iran fires on US base in Kuwait and on Bahrain", F_HEAD, x1 - x0 - 20, gap=1.05)
wrap(x0 + 12, y + 2, "after a US strike on Qeshm Island", F_BODY, x1 - x0 - 24, fill=MUTED)

# Anthropic IPO
x0, x1 = cols[1]
panel(x0, my0, x1, my1, "MARKETS · RECORD IPO", GREEN)
rect(x0 + 10, my0 + 42, x1 - 10, my0 + 172, fill=(20, 30, 28), r=4)
cx0, cy0, cx1, cy1 = x0 + 22, my0 + 54, x1 - 22, my0 + 160
for gx in range(5):
    line([(cx0 + gx * (cx1 - cx0) / 4, cy0), (cx0 + gx * (cx1 - cx0) / 4, cy1)], fill=(40, 60, 54), width=1)
text(cx0, cy0 + 2, "ANT", font("arialbd.ttf", 26), fill=(120, 230, 160))
text(cx1, cy0 - 2, "$83", F_BIG, fill=(120, 230, 160), anchor="ra")
text(cx0, cy0 + 34, "NASDAQ · priced 18 Nov", F_LBL, fill=(170, 200, 185))
stair = [(cx0, cy1 - 6), (cx0 + 50, cy1 - 14), (cx0 + 90, cy1 - 10), (cx0 + 140, cy1 - 30), (cx0 + 190, cy1 - 26), (cx1, cy1 - 52)]
line(stair, fill=(120, 230, 160), width=3)
arrowhead(stair[-2], stair[-1], 12, (120, 230, 160))
y = wrap(x0 + 12, my0 + 180, "Anthropic IPO raises a record $81.3bn", F_HEAD, x1 - x0 - 20, gap=1.05)
wrap(x0 + 12, y + 2, "priced at $83 a share, valuing it near $1.5 trillion", F_BODY, x1 - x0 - 24, fill=MUTED)

# Voyager 1
x0, x1 = cols[2]
panel(x0, my0, x1, my1, "SPACE · NASA", BLUE)
rect(x0 + 10, my0 + 42, x1 - 10, my0 + 172, fill=(10, 14, 34), r=4)
seed = 1811  # fixed star field: a tiny LCG keeps every run byte-identical
for i in range(60):
    seed = (seed * 1103515245 + 12345) % 2147483648
    sx = x0 + 14 + seed % (x1 - x0 - 28)
    seed = (seed * 1103515245 + 12345) % 2147483648
    sy = my0 + 46 + seed % 122
    dot(sx, sy, 0.7 + (i % 3) * 0.4, (220, 225, 255))
ex, ey = x0 + 40, my0 + 128
dot(ex, ey, 11, (70, 140, 230))
dot(ex - 3, ey - 3, 4, (120, 200, 120))
text(ex, ey + 16, "EARTH", F_LBL, fill=(220, 225, 255), anchor="ma")
vx, vy = x1 - 66, my0 + 92
for k in range(18):
    a = ex + 18 + k * (vx - ex - 40) / 18
    line([(a, ey - (ey - vy) * (a - ex) / (vx - ex)), (a + 7, ey - (ey - vy) * (a + 7 - ex) / (vx - ex))], fill=GOLD, width=2)
d.pieslice(sc(vx - 22, vy - 22, vx + 22, vy + 22), 90, 270, fill=(235, 235, 240))  # dish
rect(vx, vy - 6, vx + 26, vy + 6, fill=(190, 160, 90))
line([(vx + 26, vy), (vx + 56, vy - 20)], fill=(235, 235, 240), width=2)
text(vx, vy + 28, "VOYAGER 1", F_LBL, fill=(220, 225, 255), anchor="ma")
text((ex + vx) / 2 + 22, my0 + 134, "1 LIGHT-DAY", font("impact.ttf", 34), fill=GOLD, anchor="ma")
y = wrap(x0 + 12, my0 + 180, "Voyager 1 reaches one light-day from Earth", F_HEAD, x1 - x0 - 20, gap=1.05)
wrap(x0 + 12, y + 2, "25.9bn km away, 49 years after launch", F_BODY, x1 - x0 - 24, fill=MUTED)

# ---------------------------------------------------------------- bottom row
by0, by1 = 768, 978


def hemicycle(cx, cy, r_in, r_out, counts, colors):
    """Seats in rows of a half-circle, filled left to right with each group's colour."""
    total = sum(counts)
    rows = 5
    radii = [r_in + (r_out - r_in) * i / (rows - 1) for i in range(rows)]
    per = [round(total * r / sum(radii)) for r in radii]
    per[-1] += total - sum(per)
    seats = []
    for r, n in zip(radii, per):
        for j in range(n):
            a = math.pi - math.pi * (j + 0.5) / n
            seats.append((a, cx + r * math.cos(a), cy - r * math.sin(a)))
    seats.sort(key=lambda s: -s[0])
    group, left = 0, counts[0]
    for _, sx, sy in seats:
        while left == 0:
            group += 1
            left = counts[group]
        dot(sx, sy, 4.2, colors[group])
        left -= 1


# Knesset
x0, x1 = cols[0]
panel(x0, by0, x1, by1, "ISRAEL · KNESSET", BLUE)
hemicycle((x0 + x1) / 2, by0 + 128, 44, 86, [66, 52], [BLUE, (170, 170, 176)])
text((x0 + x1) / 2, by0 + 100, "66-52", font("impact.ttf", 26), anchor="ma")
y = wrap(x0 + 12, by0 + 140, "Kahana elected speaker in a blow to Netanyahu", F_HEAD, x1 - x0 - 20, gap=1.05)

# Alaska / US Senate
x0, x1 = cols[1]
panel(x0, by0, x1, by1, "USA · SENATE", BLUE)
hemicycle((x0 + x1) / 2, by0 + 128, 44, 86, [56, 44], [BLUE, RED])
text((x0 + x1) / 2, by0 + 100, "56-44", font("impact.ttf", 26), anchor="ma")
y = wrap(x0 + 12, by0 + 140, "Peltola wins Alaska for the Democrats", F_HEAD, x1 - x0 - 20, gap=1.05)

# Streets
x0, x1 = cols[2]
panel(x0, by0, x1, by1, "STREETS · PROTESTS", RED)
signs = [("PARIS", "146,000 march on prices"), ("DHAKA", "garment wage clashes"), ("BRUSSELS", "students vs cuts")]
for i, (city, what) in enumerate(signs):
    sy = by0 + 44 + i * 52
    sx = x0 + 14 + (i % 2) * 16
    line([(sx + 22, sy + 40), (sx + 22, sy + 52)], fill=(120, 90, 60), width=4)
    rect(sx, sy, x1 - 30 + (i % 2) * 10, sy + 40, fill=(255, 255, 255), outline=INK, width=2, r=3)
    text(sx + 10, sy + 6, city, font("impact.ttf", 26), fill=RED)
    text(sx + 18 + d.textlength(city, font=font("impact.ttf", 26)) / S, sy + 12, what, F_LBL, fill=INK)

# ---------------------------------------------------------------- ticker
rect(0, 988, 1024, 1024, fill=INK)
text(512, 997, "ALSO: UK and Australia sanction Israeli settlement firms  ·  NSA network outage: US sees no cyberattack  ·  Germany cuts power tax",
     F_TICK, fill=(250, 245, 230), anchor="ma")

img = img.resize((W, H), Image.LANCZOS)
img = img.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB")
img.save("entry.png", optimize=True)
print("wrote entry.png")
