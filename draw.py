#!/usr/bin/env python3
"""Draw the news-23 heroes-scene front page (1024x1024, PIL only)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (250, 244, 231)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
NAVY = (24, 48, 96)
BLUE = (31, 78, 160)
TEAL = (0, 110, 110)
ORANGE = (196, 94, 0)
PURPLE = (110, 44, 140)
BROWN = (140, 96, 24)
GREY = (96, 96, 96)
LIGHT = (238, 230, 214)
CARD = (255, 252, 244)
AMBER = (214, 130, 0)
GREEN = (28, 120, 52)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def chip(d, x, y, label, fill):
    font = f(SANS_B, 11)
    w = int(d.textlength(label, font=font)) + 12
    d.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=fill)
    d.text((x + 6, y + 2), label, font=font, fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- top rule + masthead ----
d.rectangle([0, 0, W, 6], fill=RED)
text(d, 14, 12, "THE WORLD TODAY", f(SERIF_B, 52), INK)
text(d, W - 14, 16, "31 STORIES", f(SANS_B, 20), INK, anchor="ra")
text(d, W - 14, 40, "6 REGIONS", f(SANS_B, 20), INK, anchor="ra")
text(d, 14, 70, "MONDAY 23 NOVEMBER 2026", f(SANS_B, 17), RED)
text(d, W - 14, 70, "AI ROUT  ·  AI RULES  ·  POWER SHIFT", f(SANS_B, 13), GREY, anchor="ra")
d.line([14, 92, W - 14, 92], fill=INK, width=2)

# ---- number strip ----
nums = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"), ("11,762", "EBOLA CASES"),
        ("10T WON", "SEOUL FUND"), ("$450M", "SKUBAL DEAL"), ("$107.3B", "ANTHROPIC IPO")]
cw = (W - 28) / 6
for i, (n, lab) in enumerate(nums):
    x0 = 14 + i * cw
    text(d, x0 + cw / 2, 97, n, f(SANS_B, 24), RED, anchor="ma")
    text(d, x0 + cw / 2, 124, lab, f(SANS_B, 11), INK, anchor="ma")
    if i:
        d.line([x0, 97, x0, 138], fill=(200, 190, 170), width=1)
d.line([14, 142, W - 14, 142], fill=INK, width=1)

# ---- region bar ----
regs = [("NORTH AMERICA 8", BLUE), ("EUROPE 6", ORANGE), ("MIDDLE EAST 6", PURPLE),
        ("ASIA-PACIFIC 6", TEAL), ("AFRICA 3", BROWN), ("WORLD 2", GREY)]
rw = (W - 28) / 6
for i, (lab, col) in enumerate(regs):
    x0 = 14 + i * rw
    d.rectangle([x0, 146, x0 + rw - 2, 164], fill=col)
    text(d, x0 + (rw - 2) / 2, 149, lab, f(SANS_B, 11), (255, 255, 255), anchor="ma")

# ---- UTC strip ----
d.rectangle([14, 168, W - 14, 186], fill=NAVY)
text(d, 22, 171, "THE DAY IN UTC", f(SANS_B, 12), (255, 255, 255))
text(d, 150, 171, "~00:00 ASIA OPENS  ·  06:30 KOSPI -3.3%  ·  ~09:00 SEOUL FUND  ·  14:30 WALL ST +3%  ·  ~16:00 GUTERRES  ·  ~21:00 FBI HACK   (~ = APPROX.)",
     f(SANS, 11), (220, 225, 235))

# ---- hero scenes ----
HY, HH = 190, 112          # scene boxes
HT = 306                   # hero title top
hero_w = (W - 28 - 16) / 3


def hero_scene_1(x0):
    d.rectangle([x0, HY, x0 + hero_w, HY + HH], fill=(16, 24, 48))
    # skyline
    import random
    rnd = random.Random(7)
    bx = x0 + 8
    while bx < x0 + hero_w - 12:
        bw = rnd.randint(14, 26)
        bh = rnd.randint(28, 62)
        d.rectangle([bx, HY + HH - bh, bx + bw, HY + HH], fill=(52, 58, 86))
        for wy in range(HY + HH - bh + 5, HY + HH - 4, 9):
            for wx in range(int(bx) + 3, int(bx) + bw - 3, 7):
                if rnd.random() < 0.6:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 205, 90))
        bx += bw + 4
    # falling chart
    pts = [(x0 + 14, HY + 22), (x0 + 70, HY + 34), (x0 + 120, HY + 30),
           (x0 + 170, HY + 52), (x0 + 225, HY + 62), (x0 + 285, HY + 88)]
    d.line(pts, fill=(255, 90, 70), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255), outline=(255, 90, 70))
    text(d, x0 + 8, HY + 4, "intraday -5.8%", f(SANS_B, 12), (255, 255, 255))
    text(d, x0 + hero_w - 8, HY + 4, "-3.3%", f(SANS_B, 26), (255, 90, 70), anchor="ra")


def hero_scene_2(x0):
    d.rectangle([x0, HY, x0 + hero_w, HY + HH], fill=(18, 42, 84))
    # globe
    cx, cy, r = x0 + 62, HY + 56, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 210), outline=(180, 220, 250), width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=(180, 220, 250), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(180, 220, 250), width=1)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=(180, 220, 250), width=1)
    # network
    import random
    rnd = random.Random(11)
    nodes = []
    for _ in range(9):
        nx = x0 + 130 + rnd.random() * (hero_w - 145)
        ny = HY + 10 + rnd.random() * (HH - 24)
        nodes.append((nx, ny))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if ((nodes[i][0] - nodes[j][0]) ** 2 + (nodes[i][1] - nodes[j][1]) ** 2) ** 0.5 < 62:
                d.line([nodes[i], nodes[j]], fill=(140, 190, 240), width=1)
    for nx, ny in nodes:
        d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(255, 205, 90), outline=(255, 255, 255))
    # podium silhouette
    d.rectangle([x0 + hero_w - 34, HY + HH - 26, x0 + hero_w - 8, HY + HH], fill=(10, 20, 40))
    d.ellipse([x0 + hero_w - 28, HY + HH - 40, x0 + hero_w - 14, HY + HH - 26], fill=(10, 20, 40))
    d.rectangle([x0 + 6, HY + 4, x0 + 118, HY + 22], fill=(255, 205, 90))
    text(d, x0 + 10, HY + 6, "150 DELEGATES", f(SANS_B, 12), (26, 26, 26))


def hero_scene_3(x0):
    d.rectangle([x0, HY, x0 + hero_w, HY + HH], fill=(250, 244, 231), outline=(200, 190, 170))
    text(d, x0 + 8, HY + 6, "ASIA POWER INDEX 2026", f(SANS_B, 13), INK)
    # US bar
    text(d, x0 + 8, HY + 30, "US", f(SANS_B, 14), INK)
    d.rectangle([x0 + 64, HY + 30, x0 + 64 + 190, HY + 48], fill=BLUE)
    text(d, x0 + 260, HY + 30, "78.9", f(SANS_B, 14), INK)
    # China bar
    text(d, x0 + 8, HY + 56, "CHINA", f(SANS_B, 14), INK)
    d.rectangle([x0 + 64, HY + 56, x0 + 64 + 176, HY + 74], fill=RED)
    text(d, x0 + 246, HY + 56, "73.6", f(SANS_B, 14), INK)
    # India bar
    text(d, x0 + 8, HY + 82, "INDIA 3rd", f(SANS_B, 12), INK)
    d.rectangle([x0 + 84, HY + 84, x0 + 84 + 96, HY + 98], fill=GREY)
    text(d, x0 + 186, HY + 82, "40.5", f(SANS_B, 12), INK)
    text(d, x0 + hero_w - 8, HY + 6, "GAP 5.3", f(SANS_B, 15), RED, anchor="ra")


heroes = [
    ("#1 ASIA · MARKETS", "AI ROUT HITS ASIA",
     "Kospi closes 4,708.54, sheds 161 pts; Samsung -3.1%, SK Hynix -2.5%.",
     "Source: Yonhap · Korea JoongAng", "REPORTED", GREEN, hero_scene_1),
    ("#2 WORLD · UNITED NATIONS", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules; 150 delegates back a risk framework.",
     "Source: UN News · Reuters", "REPORTED", GREEN, hero_scene_2),
    ("#3 ASIA-PACIFIC · POWER", "US LEAD OVER CHINA AT RECORD LOW",
     "Gap 5.3 narrowest since 2018. US diplomatic influence -6 to 76.7. India third at 40.5.",
     "Source: Lowy Institute", "REPORTED", GREEN, hero_scene_3),
]
for i, (kick, title, body, src, stat, scol, fn) in enumerate(heroes):
    x0 = 14 + i * (hero_w + 8)
    fn(x0)
    text(d, x0, HT, kick, f(SANS_B, 11), RED)
    lines = wrap(d, title, f(SANS_B, 16), hero_w)
    y = HT + 15
    for ln in lines[:2]:
        text(d, x0, y, ln, f(SANS_B, 16), INK)
        y += 18
    blines = wrap(d, body, f(SANS, 12), hero_w)
    y = HT + 15 + 2 * 18 + 2
    for ln in blines[:2]:
        text(d, x0, y, ln, f(SANS, 12), INK)
        y += 14
    text(d, x0, 392, src, f(SANS, 10), GREY)
    chip(d, x0 + hero_w - 74, 390, stat, scol)

# ---- 10 small cards ----
cards = [
    ("#4", "SPORT · US", "Skubal signs $450M Mets deal", "Two-time Cy Young winner, nine years — largest ever for a pitcher.", "ESPN", "REPORTED", GREEN, BLUE),
    ("#5", "TECH · US", "Anthropic IPO: $107.3B, largest ever", "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.", "Bloomberg", "REPORTED", GREEN, BLUE),
    ("#6", "EUROPE · WAR", "Poland: 3 Russian missiles crossed airspace", "Kyiv says three Kh-101 entered Poland on Friday; Tusk: provocation.", "AP", "CLAIM", AMBER, ORANGE),
    ("#7", "EUROPE · SECURITY", "Intel warns of Russian nuclear satellite", "Moscow built a satellite carrying a nuclear warhead; launch next month.", "Bloomberg", "CLAIM", AMBER, ORANGE),
    ("#8", "EUROPE · ECONOMY", "Paris: 100+ back 2% billionaire tax", "Economists, politicians and unions back France's 2% wealth tax.", "AFP", "REPORTED", GREEN, ORANGE),
    ("#9", "EUROPE · UK", "Manchester: 12,000 cleared after scare", "Substance scare empties arena district; no casualties reported.", "AP", "REPORTED", GREEN, ORANGE),
    ("#10", "EUROPE · WAR", "Zelenskyy: 165 Russian missiles in a week", "Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.", "Kyiv", "CLAIM", AMBER, ORANGE),
    ("#11", "WORLD · CLIMATE", "COP31: the day after", "194 nations reject the Antalya pact; Guterres 'profoundly frustrated'.", "CNN", "REPORTED", GREEN, GREY),
    ("#12", "AFRICA · LIBYA", "Benghazi: UN demands probe of port attacks", "Drones hit two Russian ships; UN calls for an investigation.", "UN News", "CLAIM", AMBER, BROWN),
    ("#13", "MIDDLE EAST · ISRAEL", "Israel unity talks resume", "Likud and Gantz's Yesh Atid return to the table after Sunday's stall.", "Reuters", "ONGOING", BLUE, PURPLE),
]
CX0, CY0, CW2, CH2, CG = 14, 414, 193, 96, 7
for idx, (num, kick, title, body, src, stat, scol, kcol) in enumerate(cards):
    r, c = divmod(idx, 5)
    x0 = CX0 + c * (CW2 + CG)
    y0 = CY0 + r * (CH2 + CG)
    d.rectangle([x0, y0, x0 + CW2, y0 + CH2], fill=CARD, outline=(205, 195, 175))
    d.rectangle([x0, y0, x0 + CW2, y0 + 15], fill=kcol)
    text(d, x0 + 4, y0 + 2, num, f(SANS_B, 10), (255, 255, 255))
    text(d, x0 + CW2 - 4, y0 + 2, kick, f(SANS_B, 9), (255, 255, 255), anchor="ra")
    tlines = wrap(d, title, f(SANS_B, 12), CW2 - 8)
    y = y0 + 18
    for ln in tlines[:2]:
        text(d, x0 + 4, y, ln, f(SANS_B, 12), INK)
        y += 13
    blines = wrap(d, body, f(SANS, 10), CW2 - 8)
    y = y0 + 18 + 2 * 13 + 2
    for ln in blines[:2]:
        text(d, x0 + 4, y, ln, f(SANS, 10), INK)
        y += 12
    text(d, x0 + 4, y0 + CH2 - 14, src, f(SANS, 9), GREY)
    chip(d, x0 + CW2 - 66, y0 + CH2 - 15, stat, scol)

# ---- map + ALSO ----
MY0 = 622
text(d, 14, MY0, "THE WORLD — WHERE IT HAPPENED", f(SANS_B, 14), RED)
text(d, 590, MY0, "PIN = STORY NUMBER", f(SANS_B, 10), GREY, anchor="ra")
MAP = (14, 640, 596, 806)
d.rectangle(MAP, fill=(214, 230, 240), outline=(180, 190, 200))
# graticule
for gx in range(MAP[0], MAP[2], 58):
    d.line([gx, MAP[1], gx, MAP[3]], fill=(200, 215, 225), width=1)
for gy in range(MAP[1], MAP[3], 33):
    d.line([MAP[0], gy, MAP[2], gy], fill=(200, 215, 225), width=1)

# simplified continents (lon/lat polygons, equirectangular)
LAND = (232, 216, 178)


def ll2xy(lon, lat):
    x = MAP[0] + (lon + 180) / 360 * (MAP[2] - MAP[0])
    y = MAP[1] + (75 - lat) / 130 * (MAP[3] - MAP[1])
    return (x, y)


CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66), (-76, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-76, 35), (-80, 26), (-86, 21), (-92, 15), (-97, 16), (-105, 20), (-114, 29), (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    # South America
    [(-78, 9), (-72, 12), (-60, 9), (-52, 5), (-44, -3), (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -45), (-70, -54), (-73, -44), (-72, -30), (-77, -18), (-81, -6), (-80, 1)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (28, 60), (30, 70), (40, 68), (45, 60), (40, 55), (30, 50), (28, 45), (23, 40), (19, 42), (12, 44), (3, 43), (-1, 38)],
    # Africa
    [(-17, 15), (-16, 21), (-10, 31), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (39, 21), (43, 12), (51, 11), (48, 2), (40, -5), (36, -18), (32, -29), (26, -34), (19, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8)],
    # Asia
    [(43, 68), (55, 72), (70, 72), (90, 75), (110, 74), (130, 72), (150, 70), (162, 66), (170, 60), (158, 53), (142, 50), (140, 40), (130, 35), (127, 40), (122, 31), (120, 25), (110, 20), (105, 9), (100, 8), (97, 16), (92, 22), (88, 22), (80, 13), (77, 8), (72, 20), (66, 25), (60, 25), (55, 27), (50, 29), (48, 30), (44, 29), (43, 39), (40, 42), (42, 47), (35, 46), (30, 46), (35, 52), (40, 55)],
    # Oceania
    [(113, -22), (122, -14), (132, -12), (142, -11), (147, -19), (153, -27), (150, -37), (140, -38), (130, -32), (120, -34), (114, -30)],
]
for poly in CONTINENTS:
    d.polygon([ll2xy(lon, lat) for lon, lat in poly], fill=LAND, outline=(190, 175, 140))

PINS = [
    (127, 37.5, "1", 0), (127, 37.5, "22", 14), (127, 37.5, "23", -14), (127, 37.5, "25", 0),
    (-59.6, 13.1, "2", 0), (170, -30, "3", 0),
    (-74, 40.7, "4", 0), (-74, 40.7, "29", 12), (-122.4, 37.8, "5", 0),
    (19, 52, "6", 0), (37.6, 55.7, "7", 0), (2.35, 48.85, "8", 0), (-2.24, 53.48, "9", 0),
    (30.5, 50.45, "10", 0), (30.7, 36.9, "11", 0), (20.1, 32.1, "12", 0),
    (35.2, 31.8, "13", 0), (34.5, 31.5, "14", -12), (35.2, 32, "15", 12),
    (51.4, 35.7, "16", 0), (35.5, 33.9, "17", 10), (50.6, 26.2, "18", 0),
    (32.5, 15.6, "19", 0), (25, -2, "20", 0), (90.4, 23.8, "21", 0),
    (116.4, 39.9, "24", 0),
    (-77, 38.9, "26", 0), (-77, 38.9, "27", 13), (-80, 26.7, "28", 0),
    (-105, 39.7, "30", 0), (-97, 25.9, "31", 0),
]
CLAIM_PINS = {"6", "7", "10", "12"}
for lon, lat, num, dx in PINS:
    x, y = ll2xy(lon, lat)
    x += dx
    col = AMBER if num in CLAIM_PINS else RED
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col, outline=(255, 255, 255), width=1)
    tf = f(SANS_B, 8)
    tw = d.textlength(num, font=tf)
    d.text((x - tw / 2, y - 5), num, font=tf, fill=(255, 255, 255))
text(d, MAP[0] + 4, MAP[3] - 14, "N ↑", f(SANS_B, 11), INK)

# ---- ALSO list (flowing paragraphs per region, fits the band) ----
def draw_segments(d, x, y, segs, maxw, lh):
    """segs: list of (text, font, fill); words keep their style; returns next y."""
    f10 = f(SANS, 10)
    # split into word tokens (text, font, fill)
    toks = []
    for s, font, fill in segs:
        for w in s.split(" "):
            toks.append((w, font, fill))
    lines, cur, curw = [], [], 0
    space = d.textlength(" ", font=f10)
    for w, font, fill in toks:
        ww = d.textlength(w, font=font)
        add = ww if not cur else ww + space
        if cur and curw + add > maxw:
            lines.append(cur)
            cur, curw = [(w, font, fill)], ww
        else:
            cur.append((w, font, fill))
            curw += add
    if cur:
        lines.append(cur)
    for line in lines:
        cx = x
        for i, (w, font, fill) in enumerate(line):
            if i:
                cx += space
            d.text((cx, y), w, font=font, fill=fill)
            cx += d.textlength(w, font=font)
        y += lh
    return y


AX0 = 606
text(d, AX0, MY0, "ALSO ON MONDAY — 18 MORE STORIES", f(SANS_B, 14), RED)
also = [
    ("MIDDLE EAST", RED, [("14", "Gaza: two killed in Israeli strike"), ("15", "West Bank: settler attacks hit villages"),
                          ("16", "Iran war: no deal in sight"), ("17", "Lebanon seizes 264 kg of explosives"),
                          ("18", "Bahrain: Iran strike hits plant, 2 hurt")]),
    ("AFRICA", BROWN, [("19", "Sudan: drones downed over Khartoum"), ("20", "DRC: fighting traps Ebola teams")]),
    ("ASIA-PACIFIC", TEAL, [("21", "Bangladesh: Hasina jailed on return"), ("22", "Seoul minister quits in AI exam row"),
                            ("23", "SK Telecom -7.3% as hype cools"), ("24", "China eases margin rules to calm rout"),
                            ("25", "Seoul readies 10T-won fund")]),
    ("NORTH AMERICA", BLUE, [("26", "Bessent demands Nvidia answers"), ("27", "FBI probes police database hack"),
                              ("28", "Trump: Iran strikes may resume"), ("29", "US futures jump 3% holiday week"),
                              ("30", "Tom Jackson dies at 75")]),
    ("WORLD", GREY, [("31", "States sue SpaceX on AI safety")]),
]
ay = 642
for region, col, items in also:
    segs = [(region + "  ", f(SANS_B, 10), col)]
    for i, (num, s) in enumerate(items):
        segs.append((num + " ", f(SANS_B, 10), RED))
        segs.append((s + ("  ·  " if i < len(items) - 1 else ""), f(SANS, 10), INK))
    ay = draw_segments(d, AX0, ay, segs, W - 14 - AX0, 13)
    ay += 3

# ---- DATE CHECK ----
d.rectangle([14, 814, W - 14, 892], outline=RED, width=2, fill=(255, 240, 238))
text(d, 22, 820, "DATE CHECK", f(SANS_B, 13), RED)
text(d, 22, 837, "Every story above happened or was first reported on Monday 23 November 2026.",
     f(SANS_B, 12), INK)
text(d, W - 22, 820, "WIRES READ UP TO 23:00 UTC", f(SANS_B, 11), RED, anchor="ra")
text(d, 22, 854, "LEFT OUT (not 23 Nov): Democrats reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) ·",
     f(SANS, 11), INK)
text(d, 22, 868, "EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov).",
     f(SANS, 11), INK)
text(d, 22, 880, "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff.",
     f(SANS, 11), INK)

# ---- footer ----
text(d, 14, 900, "SOURCES: AP · Reuters · Bloomberg · AFP · CNN · ESPN · UN News · WHO · Kyiv · Lowy Institute · Korea JoongAng · Morningstar",
     f(SANS, 10), GREY)
text(d, 14, 914, "CONFIRMED = 2+ outlets · REPORTED = carried by a wire · CLAIM = one side alleges · ONGOING = developing.  Red pin = reported · Amber pin = claim (unverified).",
     f(SANS, 10), GREY)
text(d, 14, 928, "THE WORLD TODAY · 23 NOV 2026", f(SANS_B, 10), INK)
text(d, W - 14, 928, "Scenes are drawn illustrations, not photographs.", f(SANS, 10), GREY, anchor="ra")
d.line([14, 948, W - 14, 948], fill=RED, width=3)

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
