"""Mimzi – Little Learners, Big Dreams: characters, picture cards and backgrounds.
Adds to the shared art module (art.CHARS / art.background) so render.py and thumbnail.py can use them."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import art, tts
from art import E, OUT, eye, mouth, cheeks, finish, star_pts

FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
SKIN = (246, 208, 178, 255)
HAIR = (128, 80, 52, 255)
HAIR_HI = (160, 108, 72, 255)
PINK = (255, 132, 182, 255)
PINK_D = (230, 90, 150, 255)
BOW = (255, 105, 170, 255)
WHITE = (255, 255, 255, 255)

# ---------------------------------------------------------------- voices + words
tts.VOICES["mz_narr"] = 0.70 * tts.VOICES["af_heart"] + 0.30 * tts.VOICES["af_bella"]       # warm, smiling teacher-mum voice
tts.VOICES["kid_mimzi"] = 0.60 * tts.VOICES["af_jessica"] + 0.25 * tts.VOICES["af_sky"] + 0.15 * tts.VOICES["af_nicole"]
tts.VOICES["kid_teddy"] = 0.55 * tts.VOICES["am_eric"] + 0.45 * tts.VOICES["af_jessica"]
tts.D.update({"Mimzi": "mˈɪmzi", "Mimzi's": "mˈɪmziz", "yoyo": "jˈOjˌO", "Yoyo": "jˈOjˌO", "ABC": "ˌAbˌisˈi", "ABCs": "ˌAbˌisˈiz",
              "Yippee": "jˈɪpi", "yippee": "jˈɪpi", "Wow": "wˈW", "wow": "wˈW", "broccoli": "bɹˈɑkəli", "Broccoli": "bɹˈɑkəli", "teddies": "tˈɛdiz"})


def brown_eye(d, x, y, r, state):
    """Mimzi's large expressive brown eyes (closed = happy curved lashes)."""
    if state == "closed":
        d.arc([x - r, y - r * 0.7, x + r, y + r * 0.8], 200, 340, fill=OUT, width=10)
        return
    E(d, x, y, r, r * 1.18, WHITE, w=7)
    E(d, x, y + r * 0.12, r * 0.82, r * 0.96, (126, 74, 40, 255), w=0)
    E(d, x, y + r * 0.16, r * 0.46, r * 0.54, (40, 24, 20, 255), w=0)
    E(d, x + r * 0.28, y - r * 0.28, r * 0.26, r * 0.26, WHITE, w=0)
    E(d, x - r * 0.26, y + r * 0.42, r * 0.12, r * 0.12, (255, 255, 255, 220), w=0)
    for k in (-1, 0, 1):  # three little lashes on the outer top
        a = math.radians(-60 + k * 22) if x > 450 else math.radians(-120 - k * 22)
        x0, y0 = x + math.cos(a) * r * 0.95, y + math.sin(a) * r * 1.12
        d.line([x0, y0, x0 + math.cos(a) * r * 0.32, y0 + math.sin(a) * r * 0.32], fill=OUT, width=7)


def hair_bow(d, cx, cy, s=1.0):
    for side in (-1, 1):
        d.polygon([(cx, cy), (cx + side * 95 * s, cy - 58 * s), (cx + side * 105 * s, cy + 52 * s)], fill=BOW, outline=OUT, width=7)
        E(d, cx + side * 62 * s, cy - 4 * s, 14 * s, 14 * s, (255, 190, 220, 255), w=0)
    E(d, cx, cy, 30 * s, 30 * s, (255, 150, 200, 255), w=7)


def curls(d, pts, col=HAIR, r=58):
    for (x, y, rr) in pts:
        E(d, x, y, rr, rr, col, w=7)
    for (x, y, rr) in pts:  # little curl highlights
        d.arc([x - rr * 0.55, y - rr * 0.55, x + rr * 0.55, y + rr * 0.55], 200, 320, fill=HAIR_HI, width=8)


def girl(eyes="open", m=0, h=520, wave=False):
    """Mimzi: toddler girl, brown curly pigtails, pink bows, big brown eyes, pink dress."""
    W, H = 900, 1100
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # legs + pink Mary Jane shoes
    for side in (-1, 1):
        d.rounded_rectangle([450 + side * 70 - 34, 900, 450 + side * 70 + 34, 1045], 30, fill=SKIN, outline=OUT, width=7)
        E(d, 450 + side * 80, 1050, 70, 38, PINK_D)
        d.line([450 + side * 70 - 30, 1030, 450 + side * 70 + 30, 1030], fill=OUT, width=6)
    # arms (behind dress edges)
    for side in (-1, 1):
        if wave and side == 1:
            continue
        else:
            d.line([450 + side * 125, 690, 450 + side * 215, 860], fill=OUT, width=78)
            d.line([450 + side * 125, 690, 450 + side * 215, 860], fill=SKIN, width=62)
            E(d, 450 + side * 222, 872, 44, 44, SKIN)
    # pink dress: puffy sleeves, A-line skirt with a white scalloped hem and a heart
    skirt = [(345, 640), (555, 640), (690, 930), (210, 930)]
    d.polygon(skirt, fill=PINK, outline=OUT, width=8)
    for k in range(9):
        x = 230 + k * 55
        E(d, x, 930, 30, 22, WHITE, w=5)
    d.polygon([(220, 922), (680, 922), (690, 932), (210, 932)], fill=PINK)
    for side in (-1, 1):
        E(d, 450 + side * 120, 680, 62, 52, PINK)
    for (x, y) in ((330, 800), (560, 780), (430, 870), (600, 880), (290, 890), (470, 760)):
        E(d, x, y, 9, 9, (255, 220, 235, 255), w=0)
    hx, hy = 450, 745
    d.polygon([(hx, hy + 34), (hx - 38, hy - 2), (hx + 38, hy - 2)], fill=(255, 230, 240, 255))
    E(d, hx - 19, hy - 6, 20, 18, (255, 230, 240, 255), w=0)
    E(d, hx + 19, hy - 6, 20, 18, (255, 230, 240, 255), w=0)
    # white round collar
    for side in (-1, 1):
        E(d, 450 + side * 46, 650, 58, 34, WHITE, w=6)
    # back hair + pigtails
    E(d, 450, 360, 285, 265, HAIR)
    for side in (-1, 1):
        bx = 450 + side * 300
        curls(d, [(bx, 330, 62), (bx + side * 30, 400, 66), (bx + side * 10, 470, 60), (bx + side * 40, 535, 52),
                  (bx + side * 5, 585, 44)])
        hair_bow(d, 450 + side * 262, 250, 0.9)
    # face
    E(d, 450, 420, 238, 215, SKIN)
    # curly bangs
    curls(d, [(260, 255, 55), (330, 210, 60), (410, 190, 62), (490, 190, 62), (570, 210, 60), (640, 255, 55)])
    E(d, 450, 170, 120, 40, HAIR, w=0)
    # eyes, brows, nose, cheeks, mouth
    for side in (-1, 1):
        brown_eye(d, 450 + side * 100, 425, 52, eyes)
        d.arc([450 + side * 100 - 44, 330, 450 + side * 100 + 44, 370], 205, 335, fill=HAIR, width=9)
    cheeks(im, [(300, 515), (600, 515)], 50, 30)
    d = ImageDraw.Draw(im)
    d.arc([432, 478, 468, 506], 20, 160, fill=(200, 130, 110, 255), width=6)
    if wave:  # waving arm drawn in front of the pigtail
        d.line([450 + 125, 690, 450 + 330, 520], fill=OUT, width=78)
        d.line([450 + 125, 690, 450 + 330, 520], fill=SKIN, width=62)
        E(d, 450 + 125, 690, 62, 52, PINK)
        E(d, 450 + 345, 500, 50, 50, SKIN)
        for k in (-1, 0, 1):
            d.arc([450 + 345 - 70 + k * 6, 500 - 70, 450 + 345 + 70 + k * 6, 500 + 70], 290 + k * 12, 310 + k * 12, fill=(255, 170, 200, 255), width=6)
    if m == 0:
        d.arc([405, 505, 495, 565], 25, 155, fill=OUT, width=9)
    else:  # open happy smile (D shape) with a little tongue
        hh = 30 + 16 * m
        d.chord([400, 520 - hh, 500, 520 + hh], 0, 180, fill=(160, 55, 75, 255), outline=OUT, width=8)
        E(d, 450, 520 + hh * 0.72, 26, hh * 0.25, (250, 140, 160, 255), w=0)
        d.line([406, 520, 494, 520], fill=OUT, width=8)
    return finish(im, (int(h * W / H), h))


def bear(eyes="open", m=0, h=330):
    """Teddy: golden-brown fluffy teddy bear with a red bow tie."""
    W, H = 800, 900
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    F, L = (212, 156, 88, 255), (246, 214, 166, 255)
    for side in (-1, 1):  # feet with paw pads
        E(d, 400 + side * 115, 840, 85, 52, F)
        E(d, 400 + side * 115, 846, 46, 30, L, w=0)
    E(d, 400, 680, 205, 190, F)                      # body
    E(d, 400, 705, 120, 120, L, w=0)                  # tummy
    for side in (-1, 1):                              # arms
        E(d, 400 + side * 200, 690, 62, 100, F)
    for side in (-1, 1):                              # ears
        E(d, 400 + side * 160, 160, 82, 82, F)
        E(d, 400 + side * 160, 166, 44, 44, L, w=0)
    E(d, 400, 330, 235, 205, F)                      # head
    for (x, y) in ((280, 230), (520, 240), (400, 160), (330, 470), (470, 470)):  # fluffy fur tufts
        d.arc([x - 30, y - 18, x + 30, y + 18], 200, 340, fill=(190, 132, 70, 255), width=6)
    E(d, 400, 405, 112, 82, L)                       # muzzle
    E(d, 400, 370, 38, 28, (70, 44, 40, 255), w=0)    # nose
    E(d, 388, 362, 10, 7, (255, 255, 255, 200), w=0)
    for side in (-1, 1):
        eye(d, 400 + side * 92, 300, 30, eyes)
    cheeks(im, [(275, 390), (525, 390)], 40, 24)
    d = ImageDraw.Draw(im)
    mouth(d, 400, 415, 0.6, m)
    by = 545                                          # red bow tie
    for side in (-1, 1):
        d.polygon([(400, by), (400 + side * 82, by - 46), (400 + side * 82, by + 46)], fill=(225, 45, 60, 255), outline=OUT, width=7)
    E(d, 400, by, 24, 24, (245, 80, 90, 255), w=6)
    return finish(im, (int(h * W / H), h))


# ---------------------------------------------------------------- picture-card objects (drawn in a 300x300 box)
def _obj(d, name, cx, cy, s):
    R = 130 * s
    if name == "apple":
        E(d, cx - R * 0.35, cy + R * 0.1, R * 0.6, R * 0.75, (235, 60, 70, 255), w=8)
        E(d, cx + R * 0.35, cy + R * 0.1, R * 0.6, R * 0.75, (235, 60, 70, 255), w=8)
        E(d, cx, cy + R * 0.12, R * 0.62, R * 0.7, (235, 60, 70, 255), w=0)
        d.line([cx, cy - R * 0.55, cx + R * 0.1, cy - R * 0.9], fill=(120, 80, 50, 255), width=int(14 * s))
        d.ellipse([cx + R * 0.1, cy - R * 0.95, cx + R * 0.55, cy - R * 0.65], fill=(110, 190, 90, 255), outline=OUT, width=6)
        E(d, cx - R * 0.45, cy - R * 0.15, R * 0.14, R * 0.2, (255, 255, 255, 200), w=0)
    elif name == "ball":
        E(d, cx, cy, R * 0.9, R * 0.9, (80, 150, 240, 255), w=9)
        d.arc([cx - R * 0.9, cy - R * 0.45, cx + R * 0.9, cy + R * 0.75], 200, 340, fill=WHITE, width=int(24 * s))
        d.arc([cx - R * 0.9, cy - R * 0.65, cx + R * 0.9, cy + R * 0.55], 20, 160, fill=(255, 210, 80, 255), width=int(24 * s))
    elif name == "cat":
        O = (255, 170, 90, 255)
        for side in (-1, 1):
            d.polygon([(cx + side * R * 0.75, cy - R * 0.2), (cx + side * R * 0.7, cy - R * 0.95), (cx + side * R * 0.15, cy - R * 0.6)], fill=O, outline=OUT, width=7)
        E(d, cx, cy, R * 0.85, R * 0.72, O)
        for side in (-1, 1):
            eye(d, cx + side * R * 0.32, cy - R * 0.08, R * 0.13, "open")
            for k in (-1, 1):
                d.line([cx + side * R * 0.3, cy + R * 0.25 + k * 10, cx + side * R * 0.95, cy + R * 0.2 + k * 22], fill=OUT, width=5)
        d.polygon([(cx - 14 * s, cy + R * 0.15), (cx + 14 * s, cy + R * 0.15), (cx, cy + R * 0.27)], fill=(245, 125, 150, 255))
        mouth(d, cx, cy + R * 0.3, 0.5 * s, 0)
    elif name == "duck":
        Y = (255, 215, 70, 255)
        E(d, cx + R * 0.1, cy + R * 0.35, R * 0.85, R * 0.5, Y)
        E(d, cx - R * 0.35, cy - R * 0.35, R * 0.45, R * 0.45, Y)
        d.polygon([(cx - R * 0.75, cy - R * 0.4), (cx - R * 1.15, cy - R * 0.28), (cx - R * 0.75, cy - R * 0.18)], fill=(255, 150, 50, 255), outline=OUT, width=6)
        eye(d, cx - R * 0.42, cy - R * 0.45, R * 0.1, "open")
        d.arc([cx - R * 0.05, cy + R * 0.05, cx + R * 0.6, cy + R * 0.55], 200, 340, fill=(235, 180, 40, 255), width=int(10 * s))
    elif name == "egg":
        E(d, cx, cy + R * 0.05, R * 0.62, R * 0.85, (255, 248, 230, 255), w=9)
        E(d, cx - R * 0.22, cy - R * 0.3, R * 0.12, R * 0.2, WHITE, w=0)
    elif name == "fish":
        O = (255, 140, 60, 255)
        d.polygon([(cx + R * 0.55, cy), (cx + R * 1.05, cy - R * 0.5), (cx + R * 1.05, cy + R * 0.5)], fill=O, outline=OUT, width=7)
        E(d, cx - R * 0.1, cy, R * 0.8, R * 0.52, O)
        for k in range(2):
            d.arc([cx - R * 0.1 + k * 40 * s, cy - R * 0.4, cx + R * 0.5 + k * 40 * s, cy + R * 0.4], 120, 240, fill=(255, 200, 120, 255), width=int(9 * s))
        eye(d, cx - R * 0.5, cy - R * 0.1, R * 0.12, "open")
    elif name == "grapes":
        P = (150, 90, 200, 255)
        for (dx, dy) in ((-0.5, -0.4), (0, -0.4), (0.5, -0.4), (-0.25, 0.05), (0.25, 0.05), (0, 0.5), (-0.5, 0.5) if False else (0, 0.5)):
            E(d, cx + dx * R, cy + dy * R, R * 0.3, R * 0.3, P, w=7)
            E(d, cx + dx * R - R * 0.1, cy + dy * R - R * 0.1, R * 0.07, R * 0.07, (255, 255, 255, 180), w=0)
        d.line([cx, cy - R * 0.7, cx + R * 0.05, cy - R * 1.0], fill=(120, 80, 50, 255), width=int(12 * s))
        d.ellipse([cx + R * 0.05, cy - R * 1.05, cx + R * 0.5, cy - R * 0.75], fill=(110, 190, 90, 255), outline=OUT, width=6)
    elif name == "hat":
        E(d, cx, cy + R * 0.4, R * 1.05, R * 0.3, (255, 215, 120, 255))
        d.chord([cx - R * 0.6, cy - R * 0.6, cx + R * 0.6, cy + R * 0.8], 180, 360, fill=(255, 215, 120, 255), outline=OUT, width=8)
        d.rectangle([cx - R * 0.58, cy + R * 0.0, cx + R * 0.58, cy + R * 0.18], fill=(255, 120, 170, 255))
        hair_bow(d, cx + R * 0.45, cy + R * 0.08, 0.35 * s)
    elif name == "ice cream":
        d.polygon([(cx - R * 0.45, cy), (cx + R * 0.45, cy), (cx, cy + R * 1.0)], fill=(230, 180, 110, 255), outline=OUT, width=7)
        for k in range(3):
            d.line([cx - R * 0.35 + k * R * 0.3, cy + R * 0.05, cx - R * 0.05 + k * R * 0.15, cy + R * 0.7], fill=(200, 140, 80, 255), width=5)
        E(d, cx, cy - R * 0.25, R * 0.55, R * 0.48, (255, 170, 200, 255))
        E(d, cx, cy - R * 0.8, R * 0.14, R * 0.14, (230, 40, 60, 255), w=5)
    elif name == "juice":
        d.rounded_rectangle([cx - R * 0.45, cy - R * 0.55, cx + R * 0.45, cy + R * 0.9], 18, fill=(255, 170, 60, 255), outline=OUT, width=8)
        E(d, cx, cy + R * 0.2, R * 0.28, R * 0.28, (255, 230, 120, 255), w=5)
        d.line([cx + R * 0.15, cy - R * 0.55, cx + R * 0.3, cy - R * 1.05], fill=(255, 100, 140, 255), width=int(16 * s))
    elif name == "kite":
        pts = [(cx, cy - R), (cx + R * 0.7, cy - R * 0.1), (cx, cy + R * 0.8), (cx - R * 0.7, cy - R * 0.1)]
        cols = [(255, 120, 150, 255), (100, 190, 250, 255), (255, 215, 80, 255), (140, 210, 120, 255)]
        c0 = (cx, cy - R * 0.1)
        for i in range(4):
            d.polygon([c0, pts[i], pts[(i + 1) % 4]], fill=cols[i])
        d.polygon(pts, outline=OUT, width=8)
        d.line([pts[2], (cx + R * 0.3, cy + R * 1.05)], fill=OUT, width=5)
        hair_bow(d, cx + R * 0.15, cy + R * 0.95, 0.25 * s)
    elif name == "leaf":
        pts = []
        for k in range(40):
            t = k / 39 * math.pi
            pts.append((cx + math.cos(t) * R * 0.9, cy - math.sin(t) * R * 0.5 * math.sin(t) * 1.4))
        pts += [(cx + math.cos(math.pi - t) * R * 0.9, cy + math.sin(math.pi - t) ** 2 * R * 0.7) for t in [k / 39 * math.pi for k in range(40)]]
        d.polygon(pts, fill=(120, 200, 100, 255), outline=OUT, width=8)
        d.line([cx - R * 0.9, cy, cx + R * 1.1, cy + R * 0.05], fill=(80, 150, 70, 255), width=int(9 * s))
    elif name == "moon":  # true crescent (no white cut-out, so it works on dark night skies too)
        pts = [(cx + math.cos(t) * R * 0.85, cy + math.sin(t) * R * 0.85) for t in [math.radians(a) for a in range(60, 301, 8)]]
        pts += [(cx + R * 0.45 + math.cos(t) * R * 0.75, cy - R * 0.25 + math.sin(t) * R * 0.75) for t in [math.radians(a) for a in range(242, 89, -8)]]
        d.polygon(pts, fill=(255, 225, 110, 255), outline=OUT, width=8)
        eye(d, cx - R * 0.5, cy - R * 0.05, R * 0.1, "closed")
    elif name == "nest":
        for k, col in enumerate(((130, 190, 240, 255), (160, 210, 250, 255), (120, 175, 230, 255))):
            E(d, cx - R * 0.35 + k * R * 0.35, cy - R * 0.1, R * 0.22, R * 0.3, col, w=6)
        d.chord([cx - R * 1.0, cy - R * 0.5, cx + R * 1.0, cy + R * 0.7], 0, 180, fill=(170, 115, 70, 255), outline=OUT, width=8)
        for k in range(5):
            d.arc([cx - R * 0.9, cy - R * 0.2 + k * 14 * s, cx + R * 0.9, cy + R * 0.5 + k * 14 * s], 10, 170, fill=(130, 85, 50, 255), width=5)
    elif name == "orange":
        E(d, cx, cy + R * 0.1, R * 0.85, R * 0.85, (255, 160, 40, 255), w=8)
        for (dx, dy) in ((-0.3, 0.2), (0.25, 0.4), (0.4, -0.1), (-0.1, 0.55), (0, -0.2)):
            E(d, cx + dx * R, cy + dy * R, 4 * s, 4 * s, (235, 130, 30, 255), w=0)
        d.ellipse([cx, cy - R * 0.95, cx + R * 0.5, cy - R * 0.65], fill=(110, 190, 90, 255), outline=OUT, width=6)
        E(d, cx - R * 0.4, cy - R * 0.25, R * 0.14, R * 0.2, (255, 255, 255, 170), w=0)
    elif name == "pig":
        P = (255, 180, 200, 255)
        for side in (-1, 1):
            d.polygon([(cx + side * R * 0.75, cy - R * 0.3), (cx + side * R * 0.8, cy - R * 0.95), (cx + side * R * 0.25, cy - R * 0.65)], fill=P, outline=OUT, width=7)
        E(d, cx, cy, R * 0.88, R * 0.75, P)
        E(d, cx, cy + R * 0.22, R * 0.36, R * 0.25, (255, 150, 175, 255), w=7)
        for side in (-1, 1):
            E(d, cx + side * R * 0.13, cy + R * 0.22, 9 * s, 13 * s, (170, 80, 100, 255), w=0)
            eye(d, cx + side * R * 0.35, cy - R * 0.2, R * 0.11, "open")
    elif name == "quilt":
        cols = [(255, 170, 200, 255), (150, 210, 250, 255), (255, 225, 120, 255), (170, 225, 160, 255)]
        n, w = 3, R * 0.6
        for i in range(n):
            for j in range(n):
                x0, y0 = cx - R * 0.9 + i * w, cy - R * 0.85 + j * w
                d.rectangle([x0, y0, x0 + w, y0 + w], fill=cols[(i + j) % 4], outline=WHITE, width=5)
                if (i + j) % 2 == 0:
                    d.polygon(star_pts(x0 + w / 2, y0 + w / 2, w * 0.28), fill=WHITE)
        d.rounded_rectangle([cx - R * 0.9, cy - R * 0.85, cx + R * 0.9, cy + R * 0.95], 12, outline=OUT, width=8)
    elif name == "rainbow":
        R *= 1.35
        for i, col in enumerate([(255, 110, 120), (255, 170, 80), (255, 225, 90), (120, 210, 120), (100, 170, 250), (170, 130, 240)]):
            rr = R * 1.0 - i * R * 0.13
            d.arc([cx - rr, cy - rr + R * 0.5, cx + rr, cy + rr + R * 0.5], 180, 360, fill=col + (255,), width=int(R * 0.14))
        for side in (-1, 1):
            art.cloud(d, cx + side * R * 0.65 - R * 0.35, cy + R * 0.5, s * 0.55, (255, 255, 255))
    elif name == "sun":
        for k in range(10):
            a = k * math.pi / 5
            d.line([cx + math.cos(a) * R * 0.7, cy + math.sin(a) * R * 0.7, cx + math.cos(a) * R * 1.0, cy + math.sin(a) * R * 1.0], fill=(255, 180, 40, 255), width=int(16 * s))
        E(d, cx, cy, R * 0.6, R * 0.6, (255, 215, 60, 255), w=8)
        for side in (-1, 1):
            eye(d, cx + side * R * 0.22, cy - R * 0.08, R * 0.08, "open")
        mouth(d, cx, cy + R * 0.18, 0.45 * s, 0)
    elif name == "tree":
        d.rectangle([cx - R * 0.15, cy + R * 0.2, cx + R * 0.15, cy + R * 1.0], fill=(150, 100, 65, 255), outline=OUT, width=7)
        for (dx, dy, r) in ((0, -0.35, 0.55), (-0.45, 0.0, 0.45), (0.45, 0.0, 0.45), (0, 0.1, 0.5)):
            E(d, cx + dx * R, cy + dy * R, r * R, r * R, (110, 195, 100, 255), w=0)
        for (dx, dy) in ((-0.3, -0.3), (0.3, 0.05), (-0.1, 0.2)):
            E(d, cx + dx * R, cy + dy * R, R * 0.1, R * 0.1, (235, 70, 80, 255), w=4)
    elif name == "umbrella":
        d.line([cx, cy - R * 0.2, cx, cy + R * 0.8], fill=OUT, width=int(12 * s))
        d.arc([cx, cy + R * 0.6, cx + R * 0.4, cy + R * 1.0], 0, 180, fill=OUT, width=int(12 * s))
        d.chord([cx - R, cy - R * 0.9, cx + R, cy + R * 0.5], 180, 360, fill=(240, 80, 110, 255), outline=OUT, width=8)
        for k in range(4):
            E(d, cx - R * 0.75 + k * R * 0.5, cy - R * 0.2, R * 0.26, R * 0.12, (255, 255, 255, 0) if False else (250, 245, 255, 255), w=0)
        d.line([cx, cy - R * 0.9, cx, cy - R * 1.05], fill=OUT, width=int(10 * s))
    elif name == "van":
        d.rounded_rectangle([cx - R, cy - R * 0.55, cx + R, cy + R * 0.45], 40, fill=(100, 180, 240, 255), outline=OUT, width=8)
        for k in range(3):
            d.rounded_rectangle([cx - R * 0.85 + k * R * 0.6, cy - R * 0.4, cx - R * 0.35 + k * R * 0.6, cy - R * 0.05], 12, fill=(220, 240, 255, 255), outline=OUT, width=5)
        for side in (-1, 1):
            E(d, cx + side * R * 0.55, cy + R * 0.5, R * 0.25, R * 0.25, (70, 60, 80, 255), w=6)
            E(d, cx + side * R * 0.55, cy + R * 0.5, R * 0.1, R * 0.1, (200, 200, 210, 255), w=0)
        E(d, cx + R * 0.92, cy + R * 0.15, R * 0.08, R * 0.08, (255, 230, 100, 255), w=4)
    elif name == "watermelon":
        d.chord([cx - R, cy - R * 0.9, cx + R, cy + R * 0.9], 0, 180, fill=(110, 190, 90, 255), outline=OUT, width=8)
        d.chord([cx - R * 0.85, cy - R * 0.75, cx + R * 0.85, cy + R * 0.75], 0, 180, fill=(250, 245, 230, 255))
        d.chord([cx - R * 0.78, cy - R * 0.68, cx + R * 0.78, cy + R * 0.68], 0, 180, fill=(250, 90, 110, 255))
        d.line([cx - R, cy, cx + R, cy], fill=OUT, width=8)
        for (dx, dy) in ((-0.4, 0.2), (0, 0.35), (0.4, 0.2), (-0.15, 0.5), (0.2, 0.5)):
            E(d, cx + dx * R, cy + dy * R, 7 * s, 11 * s, (60, 40, 40, 255), w=0)
    elif name == "xylophone":
        cols = [(255, 110, 120), (255, 170, 80), (255, 225, 90), (120, 210, 120), (100, 170, 250), (170, 130, 240)]
        for i, col in enumerate(cols):
            x0 = cx - R * 0.95 + i * R * 0.32
            hh = R * (1.3 - i * 0.12)
            d.rounded_rectangle([x0, cy - hh / 2, x0 + R * 0.26, cy + hh / 2], 10, fill=col + (255,), outline=OUT, width=6)
            E(d, x0 + R * 0.13, cy - hh / 2 + 18 * s, 6 * s, 6 * s, WHITE, w=0)
        d.line([cx + R * 0.2, cy + R * 0.95, cx + R * 0.9, cy + R * 0.45], fill=(150, 100, 65, 255), width=int(10 * s))
        E(d, cx + R * 0.92, cy + R * 0.42, R * 0.12, R * 0.12, (255, 120, 170, 255), w=5)
    elif name == "yoyo":
        d.line([cx, cy - R * 1.05, cx, cy - R * 0.4], fill=OUT, width=5)
        E(d, cx, cy + R * 0.15, R * 0.65, R * 0.65, (255, 110, 160, 255), w=8)
        E(d, cx, cy + R * 0.15, R * 0.4, R * 0.4, (255, 200, 225, 255), w=5)
        E(d, cx, cy + R * 0.15, R * 0.12, R * 0.12, (255, 255, 255, 255), w=4)
        E(d, cx, cy - R * 1.08, 12 * s, 12 * s, (255, 215, 80, 255), w=4)
    elif name == "zebra":
        for side in (-1, 1):
            E(d, cx + side * R * 0.5, cy - R * 0.75, R * 0.18, R * 0.3, WHITE)
        E(d, cx, cy - R * 0.1, R * 0.65, R * 0.75, WHITE)
        for k in range(4):
            y = cy - R * 0.7 + k * R * 0.22
            d.arc([cx - R * 0.66, y - R * 0.1, cx - R * 0.2, y + R * 0.15], 300, 60, fill=(50, 40, 50, 255), width=int(13 * s))
            d.arc([cx + R * 0.2, y - R * 0.1, cx + R * 0.66, y + R * 0.15], 120, 240, fill=(50, 40, 50, 255), width=int(13 * s))
        for k in range(4):  # mane
            E(d, cx, cy - R * 0.85 - k * 0 + (k - 1.5) * 0, R * 0.12, R * 0.12, (50, 40, 50, 255), w=0)
        E(d, cx, cy + R * 0.42, R * 0.45, R * 0.32, (120, 110, 120, 255))
        for side in (-1, 1):
            E(d, cx + side * R * 0.15, cy + R * 0.42, 8 * s, 10 * s, (40, 30, 40, 255), w=0)
            eye(d, cx + side * R * 0.28, cy - R * 0.05, R * 0.1, "open")


LETTERS = [("A", "apple"), ("B", "ball"), ("C", "cat"), ("D", "duck"), ("E", "egg"), ("F", "fish"), ("G", "grapes"),
           ("H", "hat"), ("I", "ice cream"), ("J", "juice"), ("K", "kite"), ("L", "leaf"), ("M", "moon"), ("N", "nest"),
           ("O", "orange"), ("P", "pig"), ("Q", "quilt"), ("R", "rainbow"), ("S", "sun"), ("T", "tree"), ("U", "umbrella"),
           ("V", "van"), ("W", "watermelon"), ("X", "xylophone"), ("Y", "yoyo"), ("Z", "zebra")]
CARD_COLS = [(255, 105, 150), (80, 160, 240), (255, 160, 40), (90, 190, 110), (170, 110, 230), (240, 80, 80)]


def card(eyes="open", m=0, h=600, letter="A", word="apple", show_letter=True, show_obj=True):
    """A big white picture card: the letter (upper + lower case) on top, the picture below, the word at the bottom."""
    W, H = 720, 860
    i = ord(letter) - 65
    col = CARD_COLS[i % len(CARD_COLS)] + (255,)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([30, 40, W - 20, H - 10], 60, fill=(60, 30, 60, 90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, W - 30, H - 30], 60, fill=WHITE, outline=col, width=22)
    if show_letter:
        f = ImageFont.truetype(FONT, 250)
        t = letter + letter.lower()
        x = (W - 10 - f.getlength(t)) / 2
        d.text((x + 6, 18 + 6), t, font=f, fill=(60, 30, 60, 60))
        d.text((x, 18), t, font=f, fill=col, stroke_width=10, stroke_fill=(95, 62, 72, 255))
    if show_obj:
        oc = 520 if show_letter else 400
        _obj(d, word, W / 2 - 5, oc, 0.95 if show_letter else 1.5)
        if show_letter:
            f2 = ImageFont.truetype(FONT, 66)
            wt = word.replace("yoyo", "yo-yo")
            d.text(((W - 10 - f2.getlength(wt)) / 2, 700), wt, font=f2, fill=(95, 62, 72, 255))
    return finish(im, (int(h * W / H), h))


def abc_strip(eyes="open", m=0, h=200):
    """All 26 letters in colourful bubbles (for the final 'we did it!' scene)."""
    W, H = 2200, 560
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 110)
    for k in range(26):
        r, c = divmod(k, 13)
        x, y = 90 + c * 166, 140 + r * 270
        col = CARD_COLS[k % len(CARD_COLS)] + (255,)
        E(d, x, y, 76, 76, col, w=8)
        t = chr(65 + k)
        d.text((x - f.getlength(t) / 2, y - 82), t, font=f, fill=WHITE, stroke_width=5, stroke_fill=OUT)
    return finish(im, (int(h * W / H), h))


# ---------------------------------------------------------------- backgrounds
_base_bg = art.background


def background(kind, W, H):
    if kind not in ("mz_playroom", "mz_garden"):
        return _base_bg(kind, W, H)
    rnd = random.Random(11)
    land = W > H
    ground = 0.86 if land else 0.74
    if kind == "mz_playroom":
        im = art.grad(W, H, (255, 228, 236), (255, 243, 232))
        d = ImageDraw.Draw(im)
        for j in range(0, int(H * 0.68), int(H * 0.09)):  # pastel polka-dot wallpaper
            for i in range(0, W + 80, int(H * 0.09)):
                x = i + (H * 0.045 if (j // int(H * 0.09)) % 2 else 0)
                c = [(255, 205, 222), (205, 232, 250), (255, 236, 190)][(i // int(H * 0.09) + j) % 3]
                d.ellipse([x - H * 0.008, j + H * 0.04 - H * 0.008, x + H * 0.008, j + H * 0.04 + H * 0.008], fill=c)
        wy = H * (ground - 0.16)
        d.rectangle([0, wy, W, H], fill=(196, 236, 222))                 # mint wainscot
        d.rectangle([0, wy - H * 0.012, W, wy + H * 0.004], fill=(255, 255, 255))
        fy = H * (ground - 0.06)
        d.rectangle([0, fy, W, H], fill=(240, 205, 160))                 # light wooden floor
        for k in range(0, W, int(H * 0.14)):
            d.line([k, fy, k - H * 0.08, H], fill=(225, 188, 142), width=4)
        # window (left) with sky + cloud + curtains
        wx0, wx1 = (W * 0.05, W * 0.24) if land else (W * 0.08, W * 0.42)
        wy0, wy1 = H * 0.12, H * (0.45 if land else 0.33)
        d.rounded_rectangle([wx0, wy0, wx1, wy1], 30, fill=(170, 220, 255), outline=(255, 255, 255), width=14)
        art.cloud(d, wx0 + (wx1 - wx0) * 0.2, wy0 + (wy1 - wy0) * 0.45, (wx1 - wx0) / 520, (255, 255, 255))
        d.ellipse([wx1 - (wx1 - wx0) * 0.32, wy0 + 20, wx1 - (wx1 - wx0) * 0.08, wy0 + 20 + (wx1 - wx0) * 0.24], fill=(255, 230, 120))
        d.line([(wx0 + wx1) / 2, wy0, (wx0 + wx1) / 2, wy1], fill=(255, 255, 255), width=10)
        for side in (wx0 - 20, wx1 + 20):
            d.polygon([(side - 40, wy0 - 20), (side + 40, wy0 - 20), (side + 25, wy1 + 30), (side - 25, wy1 + 30)], fill=(255, 170, 200))
        d.rectangle([wx0 - 80, wy0 - 34, wx1 + 80, wy0 - 18], fill=(230, 150, 180))
        # bunting across the top
        for k in range(14):
            x = W * (k + 0.5) / 14
            y0 = H * 0.035 + math.sin(k / 13 * math.pi) * H * 0.03
            c = [(255, 120, 170), (120, 190, 250), (255, 210, 80), (140, 210, 130)][k % 4]
            d.polygon([(x - W * 0.025, y0), (x + W * 0.025, y0), (x, y0 + H * 0.06)], fill=c)
        d.arc([-W * 0.1, -H * 0.1, W * 1.1, H * 0.13], 20, 160, fill=(200, 160, 180), width=4)
        # shelf (right) with toy blocks + plant
        sx0, sx1 = (W * 0.76, W * 0.96) if land else (W * 0.6, W * 0.95)
        sy = H * (0.36 if land else 0.27)
        d.rounded_rectangle([sx0, sy, sx1, sy + H * 0.022], 8, fill=(220, 165, 115))
        bw = (sx1 - sx0) / 6
        for k, (c, L) in enumerate(zip([(255, 120, 150), (100, 180, 245), (255, 205, 70)], "ABC")):
            x0 = sx0 + bw * 0.4 + k * bw * 1.15
            d.rounded_rectangle([x0, sy - bw, x0 + bw, sy], 10, fill=c, outline=(255, 255, 255), width=5)
            f = ImageFont.truetype(FONT, int(bw * 0.7))
            d.text((x0 + (bw - f.getlength(L)) / 2, sy - bw * 0.98), L, font=f, fill=(255, 255, 255))
        px = sx1 - bw * 0.9
        d.polygon([(px - bw * 0.4, sy), (px + bw * 0.4, sy), (px + bw * 0.3, sy - bw * 0.7), (px - bw * 0.3, sy - bw * 0.7)], fill=(240, 140, 110))
        for a in (-0.6, 0, 0.6):
            d.ellipse([px + a * bw * 0.6 - bw * 0.25, sy - bw * 1.5, px + a * bw * 0.6 + bw * 0.25, sy - bw * 0.65], fill=(110, 195, 110))
        # round lavender rug
        rx, ry = W * 0.5, H * (ground + 0.02)
        d.ellipse([rx - W * (0.42 if land else 0.48), ry - H * 0.06, rx + W * (0.42 if land else 0.48), ry + H * 0.06], fill=(215, 195, 245))
        d.ellipse([rx - W * (0.36 if land else 0.42), ry - H * 0.045, rx + W * (0.36 if land else 0.42), ry + H * 0.045], outline=(255, 255, 255), width=6)
        return im, None, []
    if kind == "mz_garden":
        im = art.grad(W, H, (160, 215, 252), (238, 248, 255))
        d = ImageDraw.Draw(im)
        d.ellipse([W * 0.82, H * 0.06, W * 0.82 + H * 0.15, H * 0.21], fill=(255, 230, 120))
        for i in range(3):
            art.cloud(d, rnd.uniform(0, W * 0.7), rnd.uniform(H * 0.05, H * 0.25), H / 1000, (255, 255, 255))
        art.hills(d, W, H, ground - 0.12, 0.07, (165, 222, 150), 2)
        art.hills(d, W, H, ground - 0.02, 0.05, (128, 205, 118), 3)
        art.flowers(d, W, H, ground * H, 60, 2)
        return im, None, []


art.background = background
art.CHARS.update({
    "mimzi": dict(fn=girl, kw=dict(), h=0.50),
    "mimzi_wave": dict(fn=girl, kw=dict(wave=True), h=0.50),
    "teddy": dict(fn=bear, kw=dict(), h=0.30),
    "abc_strip": dict(fn=abc_strip, kw=dict(), h=0.26),
})
for L, wd in LETTERS:
    art.CHARS["card_" + L] = dict(fn=card, kw=dict(letter=L, word=wd), h=0.66)
    art.CHARS["obj_" + L] = dict(fn=card, kw=dict(letter=L, word=wd, show_letter=False), h=0.50)
