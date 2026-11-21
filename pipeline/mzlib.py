"""Mimzi picture library: ~80 icons, pattern cards (picture / number / colour / shape / opposites / question /
missing-letter / speech) and extra backgrounds. Cards are looked up by pattern id, e.g. "w:banana", "n:3:duck",
"c:red:apple", "s:circle", "o:hot:cold", "q", "seq:A,B,_", "t:Hello!:wave", "i:balloon"."""
import math, random, zlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import art, mzart
from art import E, OUT, eye, mouth, finish, star_pts

FONT = mzart.FONT
WHITE = (255, 255, 255, 255)
DARK = (95, 62, 72, 255)


def C(r, g, b, a=255):
    return (r, g, b, a)


def poly(d, pts, col, w=8):
    d.polygon(pts, fill=col, outline=OUT, width=w)


def rr(d, box, r, col, w=8):
    d.rounded_rectangle(box, r, fill=col, outline=OUT, width=w)


def face(d, cx, cy, R, smile=True, sleepy=False):
    for side in (-1, 1):
        eye(d, cx + side * R * 0.3, cy - R * 0.05, R * 0.11, "closed" if sleepy else "open")
    if smile:
        d.arc([cx - R * 0.2, cy + R * 0.05, cx + R * 0.2, cy + R * 0.35], 20, 160, fill=OUT, width=max(4, int(R * 0.05)))
    else:
        d.arc([cx - R * 0.2, cy + R * 0.22, cx + R * 0.2, cy + R * 0.5], 200, 340, fill=OUT, width=max(4, int(R * 0.05)))


# ---------------------------------------------------------------- icons
def icon(d, name, cx, cy, s):
    R = 130 * s
    w = max(4, int(8 * s))
    n = name
    if n == "book":
        poly(d, [(cx - R, cy - R * 0.6), (cx, cy - R * 0.45), (cx, cy + R * 0.7), (cx - R, cy + R * 0.55)], C(100, 170, 240), w)
        poly(d, [(cx + R, cy - R * 0.6), (cx, cy - R * 0.45), (cx, cy + R * 0.7), (cx + R, cy + R * 0.55)], C(255, 120, 160), w)
        for k in range(3):
            y = cy - R * 0.2 + k * R * 0.25
            d.line([cx - R * 0.8, y, cx - R * 0.2, y + R * 0.06], fill=WHITE, width=w)
            d.line([cx + R * 0.2, y + R * 0.06, cx + R * 0.8, y], fill=WHITE, width=w)
    elif n == "cup":
        d.arc([cx + R * 0.3, cy - R * 0.3, cx + R * 0.9, cy + R * 0.4], 270, 90, fill=OUT, width=int(R * 0.18))
        d.arc([cx + R * 0.3, cy - R * 0.3, cx + R * 0.9, cy + R * 0.4], 270, 90, fill=C(255, 160, 80), width=int(R * 0.1))
        poly(d, [(cx - R * 0.6, cy - R * 0.6), (cx + R * 0.6, cy - R * 0.6), (cx + R * 0.45, cy + R * 0.7), (cx - R * 0.45, cy + R * 0.7)], C(255, 160, 80), w)
        E(d, cx, cy + R * 0.05, R * 0.18, R * 0.18, C(255, 230, 150), w=0)
    elif n == "car":
        rr(d, [cx - R, cy - R * 0.15, cx + R, cy + R * 0.45], 30, C(240, 80, 90), w)
        poly(d, [(cx - R * 0.55, cy - R * 0.15), (cx - R * 0.3, cy - R * 0.6), (cx + R * 0.35, cy - R * 0.6), (cx + R * 0.6, cy - R * 0.15)], C(240, 80, 90), w)
        poly(d, [(cx - R * 0.4, cy - R * 0.2), (cx - R * 0.22, cy - R * 0.5), (cx + R * 0.02, cy - R * 0.5), (cx + R * 0.02, cy - R * 0.2)], C(210, 235, 255), max(3, w // 2))
        poly(d, [(cx + R * 0.1, cy - R * 0.2), (cx + R * 0.1, cy - R * 0.5), (cx + R * 0.3, cy - R * 0.5), (cx + R * 0.45, cy - R * 0.2)], C(210, 235, 255), max(3, w // 2))
        for side in (-1, 1):
            E(d, cx + side * R * 0.55, cy + R * 0.45, R * 0.24, R * 0.24, C(70, 60, 80), w=w)
            E(d, cx + side * R * 0.55, cy + R * 0.45, R * 0.09, R * 0.09, C(210, 210, 220), w=0)
    elif n == "dog":
        B = C(200, 150, 100)
        for side in (-1, 1):
            E(d, cx + side * R * 0.7, cy - R * 0.05, R * 0.25, R * 0.5, C(140, 95, 60), w=w)
        E(d, cx, cy, R * 0.72, R * 0.68, B, w=w)
        E(d, cx, cy + R * 0.28, R * 0.35, R * 0.26, C(245, 220, 190), w=0)
        E(d, cx, cy + R * 0.15, R * 0.13, R * 0.09, C(60, 40, 40), w=0)
        for side in (-1, 1):
            eye(d, cx + side * R * 0.28, cy - R * 0.15, R * 0.11, "open")
        d.arc([cx - R * 0.18, cy + R * 0.2, cx + R * 0.18, cy + R * 0.42], 20, 160, fill=OUT, width=w)
        E(d, cx, cy + R * 0.48, R * 0.09, R * 0.1, C(250, 120, 140), w=0)
    elif n == "shoe":
        poly(d, [(cx - R * 0.9, cy + R * 0.4), (cx - R * 0.8, cy - R * 0.4), (cx - R * 0.2, cy - R * 0.4), (cx + R * 0.1, cy), (cx + R * 0.9, cy + R * 0.1), (cx + R * 0.95, cy + R * 0.4)], C(100, 180, 240), w)
        d.rectangle([cx - R * 0.9, cy + R * 0.32, cx + R * 0.95, cy + R * 0.5], fill=WHITE, outline=OUT, width=w)
        for k in range(3):
            d.line([cx - R * 0.55 + k * R * 0.18, cy - R * 0.25 + k * R * 0.1, cx - R * 0.25 + k * R * 0.18, cy - R * 0.3 + k * R * 0.1], fill=WHITE, width=w)
    elif n == "spoon":
        d.line([cx - R * 0.1, cy - R * 0.1, cx + R * 0.7, cy + R * 0.9], fill=OUT, width=int(R * 0.24))
        d.line([cx - R * 0.1, cy - R * 0.1, cx + R * 0.7, cy + R * 0.9], fill=C(200, 205, 220), width=int(R * 0.14))
        E(d, cx - R * 0.35, cy - R * 0.45, R * 0.38, R * 0.5, C(200, 205, 220), w=w)
        E(d, cx - R * 0.45, cy - R * 0.55, R * 0.1, R * 0.16, WHITE, w=0)
    elif n == "banana":
        pts = [(cx + math.cos(a) * R * 0.9, cy - R * 0.4 + math.sin(a) * R * 0.9) for a in [math.radians(t) for t in range(20, 161, 10)]]
        pts += [(cx + math.cos(a) * R * 0.95, cy - R * 0.85 + math.sin(a) * R * 0.95) for a in [math.radians(t) for t in range(160, 19, -10)]]
        poly(d, pts, C(255, 220, 70), w)
        d.line([pts[0], (pts[0][0] + R * 0.1, pts[0][1] - R * 0.2)], fill=C(120, 90, 50), width=int(R * 0.12))
    elif n == "strawberry":
        poly(d, [(cx - R * 0.7, cy - R * 0.4), (cx + R * 0.7, cy - R * 0.4), (cx + R * 0.4, cy + R * 0.5), (cx, cy + R * 0.9), (cx - R * 0.4, cy + R * 0.5)], C(240, 60, 80), w)
        E(d, cx, cy - R * 0.35, R * 0.7, R * 0.3, C(240, 60, 80), w=0)
        for (dx, dy) in ((-0.3, -0.1), (0.1, -0.05), (0.4, -0.15), (-0.15, 0.25), (0.2, 0.3), (0, 0.6)):
            E(d, cx + dx * R, cy + dy * R, 6 * s, 9 * s, C(255, 230, 120), w=0)
        for k in range(5):
            a = math.radians(200 + k * 35)
            poly(d, [(cx, cy - R * 0.55), (cx + math.cos(a) * R * 0.5, cy - R * 0.55 + math.sin(a) * R * 0.3 + R * 0.15), (cx + math.cos(a + 0.3) * R * 0.3, cy - R * 0.5)], C(100, 190, 90), max(3, w // 2))
    elif n == "pear":
        E(d, cx, cy + R * 0.3, R * 0.62, R * 0.58, C(180, 220, 90), w=w)
        E(d, cx, cy - R * 0.25, R * 0.38, R * 0.45, C(180, 220, 90), w=w)
        E(d, cx, cy + R * 0.1, R * 0.4, R * 0.5, C(180, 220, 90), w=0)
        d.line([cx, cy - R * 0.68, cx + R * 0.08, cy - R * 0.95], fill=C(120, 80, 50), width=int(12 * s))
    elif n == "carrot":
        poly(d, [(cx - R * 0.35, cy - R * 0.5), (cx + R * 0.35, cy - R * 0.5), (cx, cy + R * 1.0)], C(255, 140, 40), w)
        for k in range(3):
            y = cy - R * 0.25 + k * R * 0.3
            d.line([cx - R * 0.2 + k * R * 0.05, y, cx - R * 0.02, y + R * 0.04], fill=C(220, 110, 30), width=w)
        for a in (-0.5, 0, 0.5):
            E(d, cx + a * R * 0.5, cy - R * 0.75, R * 0.14, R * 0.32, C(110, 190, 90), w=max(3, w // 2))
    elif n == "potato":
        E(d, cx, cy, R * 0.85, R * 0.6, C(210, 165, 110), w=w)
        for (dx, dy) in ((-0.4, -0.1), (0.2, -0.25), (0.45, 0.2), (-0.1, 0.3)):
            E(d, cx + dx * R, cy + dy * R, 6 * s, 5 * s, C(160, 115, 70), w=0)
    elif n == "tomato":
        E(d, cx, cy + R * 0.1, R * 0.85, R * 0.75, C(240, 70, 60), w=w)
        for k in range(5):
            a = math.radians(180 + k * 45)
            poly(d, [(cx, cy - R * 0.62), (cx + math.cos(a) * R * 0.45, cy - R * 0.62 + math.sin(a) * R * 0.2 + R * 0.12), (cx + math.cos(a + 0.4) * R * 0.2, cy - R * 0.55)], C(100, 180, 80), max(3, w // 2))
        E(d, cx - R * 0.4, cy - R * 0.1, R * 0.13, R * 0.18, (255, 255, 255, 170), w=0)
    elif n == "broccoli":
        poly(d, [(cx - R * 0.25, cy + R * 0.1), (cx + R * 0.25, cy + R * 0.1), (cx + R * 0.2, cy + R * 0.95), (cx - R * 0.2, cy + R * 0.95)], C(160, 210, 120), w)
        for (dx, dy, r) in ((-0.5, -0.1, 0.35), (0.5, -0.1, 0.35), (0, -0.4, 0.42), (-0.25, 0.05, 0.3), (0.25, 0.05, 0.3)):
            E(d, cx + dx * R, cy + dy * R, r * R, r * R, C(80, 170, 80), w=w)
    elif n == "corn":
        E(d, cx, cy, R * 0.38, R * 0.85, C(255, 215, 70), w=w)
        for j in range(6):
            for i in range(3):
                E(d, cx - R * 0.18 + i * R * 0.18, cy - R * 0.6 + j * R * 0.24, R * 0.07, R * 0.08, C(255, 240, 150), w=0)
        for side in (-1, 1):
            poly(d, [(cx, cy + R * 0.95), (cx + side * R * 0.65, cy - R * 0.2), (cx + side * R * 0.2, cy + R * 0.2)], C(120, 190, 90), w)
    elif n == "peas":
        poly(d, [(cx - R, cy), (cx - R * 0.6, cy - R * 0.4), (cx + R * 0.6, cy - R * 0.4), (cx + R, cy), (cx + R * 0.6, cy + R * 0.35), (cx - R * 0.6, cy + R * 0.35)], C(110, 190, 90), w)
        for k in range(4):
            E(d, cx - R * 0.6 + k * R * 0.4, cy - R * 0.02, R * 0.2, R * 0.2, C(160, 225, 110), w=max(3, w // 2))
    elif n == "chair":
        rr(d, [cx - R * 0.5, cy - R * 0.95, cx + R * 0.5, cy - R * 0.05], 14, C(240, 150, 90), w)
        rr(d, [cx - R * 0.65, cy - R * 0.1, cx + R * 0.65, cy + R * 0.12], 8, C(240, 150, 90), w)
        for side in (-1, 1):
            d.rectangle([cx + side * R * 0.55 - R * 0.07, cy + R * 0.1, cx + side * R * 0.55 + R * 0.07, cy + R * 0.95], fill=C(200, 115, 70), outline=OUT, width=w)
        E(d, cx, cy - R * 0.5, R * 0.12, R * 0.12, C(255, 200, 150), w=0)
    elif n == "table":
        rr(d, [cx - R, cy - R * 0.35, cx + R, cy - R * 0.1], 10, C(200, 140, 90), w)
        for side in (-1, 1):
            d.rectangle([cx + side * R * 0.8 - R * 0.08, cy - R * 0.1, cx + side * R * 0.8 + R * 0.08, cy + R * 0.85], fill=C(170, 115, 70), outline=OUT, width=w)
        E(d, cx, cy - R * 0.55, R * 0.22, R * 0.2, C(255, 120, 150), w=w)
    elif n == "bed":
        rr(d, [cx - R, cy - R * 0.7, cx - R * 0.78, cy + R * 0.7], 10, C(200, 140, 90), w)
        rr(d, [cx - R * 0.85, cy - R * 0.05, cx + R, cy + R * 0.4], 16, C(255, 170, 200), w)
        rr(d, [cx - R * 0.75, cy - R * 0.3, cx - R * 0.3, cy], 20, WHITE, w)
        d.rectangle([cx + R * 0.85, cy + R * 0.3, cx + R, cy + R * 0.7], fill=C(200, 140, 90), outline=OUT, width=w)
    elif n == "door":
        rr(d, [cx - R * 0.55, cy - R, cx + R * 0.55, cy + R], 16, C(150, 200, 250), w)
        for j in range(2):
            rr(d, [cx - R * 0.38, cy - R * 0.8 + j * R * 0.85, cx + R * 0.38, cy - R * 0.1 + j * R * 0.85], 10, C(180, 220, 255), max(3, w // 2))
        E(d, cx + R * 0.35, cy + R * 0.05, R * 0.08, R * 0.08, C(255, 210, 80), w=max(3, w // 2))
    elif n == "window":
        rr(d, [cx - R * 0.85, cy - R * 0.8, cx + R * 0.85, cy + R * 0.8], 16, C(170, 220, 255), w)
        d.line([cx, cy - R * 0.8, cx, cy + R * 0.8], fill=WHITE, width=int(R * 0.12))
        d.line([cx - R * 0.85, cy, cx + R * 0.85, cy], fill=WHITE, width=int(R * 0.12))
        art.cloud(d, cx - R * 0.75, cy - R * 0.45, s * 0.45, (255, 255, 255))
        E(d, cx + R * 0.45, cy - R * 0.45, R * 0.2, R * 0.2, C(255, 225, 110), w=0)
    elif n == "lamp":
        poly(d, [(cx - R * 0.6, cy - R * 0.1), (cx + R * 0.6, cy - R * 0.1), (cx + R * 0.35, cy - R * 0.8), (cx - R * 0.35, cy - R * 0.8)], C(255, 215, 110), w)
        d.rectangle([cx - R * 0.07, cy - R * 0.1, cx + R * 0.07, cy + R * 0.75], fill=C(200, 140, 90), outline=OUT, width=w)
        E(d, cx, cy + R * 0.85, R * 0.45, R * 0.14, C(200, 140, 90), w=w)
    elif n == "sofa":
        rr(d, [cx - R * 0.85, cy - R * 0.55, cx + R * 0.85, cy + R * 0.1], 30, C(150, 120, 220), w)
        rr(d, [cx - R, cy - R * 0.1, cx + R, cy + R * 0.45], 24, C(170, 140, 235), w)
        for side in (-1, 1):
            rr(d, [cx + side * R - R * 0.18, cy - R * 0.25, cx + side * R + R * 0.18, cy + R * 0.45], 20, C(150, 120, 220), w)
            d.rectangle([cx + side * R * 0.8 - R * 0.06, cy + R * 0.45, cx + side * R * 0.8 + R * 0.06, cy + R * 0.65], fill=C(120, 85, 60))
    elif n == "clock":
        E(d, cx, cy, R * 0.85, R * 0.85, C(255, 170, 200), w=w)
        E(d, cx, cy, R * 0.68, R * 0.68, WHITE, w=max(3, w // 2))
        for k in range(12):
            a = k * math.pi / 6
            E(d, cx + math.cos(a) * R * 0.55, cy + math.sin(a) * R * 0.55, 4 * s, 4 * s, OUT, w=0)
        d.line([cx, cy, cx, cy - R * 0.45], fill=OUT, width=w)
        d.line([cx, cy, cx + R * 0.3, cy + R * 0.1], fill=OUT, width=w)
    elif n == "eye":
        E(d, cx, cy, R * 0.9, R * 0.55, WHITE, w=w)
        E(d, cx, cy, R * 0.42, R * 0.42, C(110, 160, 220), w=0)
        E(d, cx, cy, R * 0.2, R * 0.2, C(40, 30, 40), w=0)
        E(d, cx + R * 0.12, cy - R * 0.12, R * 0.09, R * 0.09, WHITE, w=0)
        for k in range(5):
            a = math.radians(-150 + k * 30)
            d.line([cx + math.cos(a) * R * 0.85, cy + math.sin(a) * R * 0.5, cx + math.cos(a) * R * 1.05, cy + math.sin(a) * R * 0.75], fill=OUT, width=w)
    elif n == "nose":
        sk = mzart.SKIN
        E(d, cx, cy, R * 0.85, R * 0.85, C(255, 236, 222), w=0)
        poly(d, [(cx, cy - R * 0.6), (cx + R * 0.35, cy + R * 0.35), (cx - R * 0.35, cy + R * 0.35)], sk, w)
        for side in (-1, 1):
            E(d, cx + side * R * 0.32, cy + R * 0.35, R * 0.22, R * 0.18, sk, w=w)
            E(d, cx + side * R * 0.16, cy + R * 0.42, R * 0.07, R * 0.05, C(180, 120, 100), w=0)
        E(d, cx, cy + R * 0.36, R * 0.25, R * 0.12, sk, w=0)
    elif n == "mouth":
        d.chord([cx - R * 0.8, cy - R * 0.5, cx + R * 0.8, cy + R * 0.6], 0, 180, fill=C(240, 90, 120), outline=OUT, width=w)
        d.chord([cx - R * 0.6, cy - R * 0.25, cx + R * 0.6, cy + R * 0.35], 0, 180, fill=WHITE)
        E(d, cx, cy + R * 0.38, R * 0.3, R * 0.12, C(255, 150, 170), w=0)
        d.line([cx - R * 0.8, cy + R * 0.05, cx + R * 0.8, cy + R * 0.05], fill=OUT, width=w)
    elif n == "ear":
        sk = mzart.SKIN
        E(d, cx, cy, R * 0.55, R * 0.85, sk, w=w)
        d.arc([cx - R * 0.3, cy - R * 0.55, cx + R * 0.35, cy + R * 0.5], 270, 100, fill=C(210, 150, 130), width=int(R * 0.1))
    elif n in ("hand", "wave"):
        sk = mzart.SKIN
        E(d, cx, cy + R * 0.25, R * 0.5, R * 0.5, sk, w=w)
        for k in range(4):
            x = cx - R * 0.38 + k * R * 0.25
            rr(d, [x - R * 0.1, cy - R * 0.75 + abs(k - 1.5) * R * 0.1, x + R * 0.1, cy + R * 0.1], 20, sk, w)
        rr(d, [cx - R * 0.85, cy - R * 0.05, cx - R * 0.35, cy + R * 0.2], 20, sk, w)
        E(d, cx, cy + R * 0.25, R * 0.42, R * 0.4, sk, w=0)
        if n == "wave":
            for k in range(2):
                d.arc([cx - R * (1.0 + k * 0.2), cy - R * (0.9 + k * 0.2), cx + R * (1.0 + k * 0.2), cy + R * (0.9 + k * 0.2)], 290, 330, fill=C(255, 150, 190), width=w)
                d.arc([cx - R * (1.0 + k * 0.2), cy - R * (0.9 + k * 0.2), cx + R * (1.0 + k * 0.2), cy + R * (0.9 + k * 0.2)], 210, 250, fill=C(255, 150, 190), width=w)
    elif n == "foot":
        sk = mzart.SKIN
        E(d, cx, cy + R * 0.2, R * 0.5, R * 0.7, sk, w=w)
        for k, rr_ in enumerate((0.2, 0.15, 0.13, 0.11, 0.1)):
            E(d, cx - R * 0.35 + k * R * 0.18, cy - R * 0.62 + k * R * 0.05, rr_ * R, rr_ * R, sk, w=max(3, w // 2))
    elif n == "heart":
        poly(d, star_pts(0, 0, 1)[:0] or [(cx, cy + R * 0.85), (cx - R * 0.9, cy - R * 0.05), (cx + R * 0.9, cy - R * 0.05)], C(255, 100, 150), w)
        for side in (-1, 1):
            E(d, cx + side * R * 0.45, cy - R * 0.25, R * 0.5, R * 0.48, C(255, 100, 150), w=w)
        poly(d, [(cx, cy + R * 0.8), (cx - R * 0.82, cy - R * 0.08), (cx + R * 0.82, cy - R * 0.08)], C(255, 100, 150), 0)
        E(d, cx, cy - R * 0.1, R * 0.5, R * 0.3, C(255, 100, 150), w=0)
        E(d, cx - R * 0.5, cy - R * 0.35, R * 0.12, R * 0.15, (255, 255, 255, 180), w=0)
    elif n == "gift":
        rr(d, [cx - R * 0.75, cy - R * 0.3, cx + R * 0.75, cy + R * 0.85], 10, C(120, 190, 250), w)
        rr(d, [cx - R * 0.85, cy - R * 0.55, cx + R * 0.85, cy - R * 0.25], 10, C(100, 170, 240), w)
        d.rectangle([cx - R * 0.12, cy - R * 0.55, cx + R * 0.12, cy + R * 0.85], fill=C(255, 110, 160))
        mzart.hair_bow(d, cx, cy - R * 0.6, 0.6 * s)
    elif n in ("star", "star_s"):
        poly(d, star_pts(cx, cy, R * 0.95), C(255, 215, 60), w)
    elif n == "cloud":
        art.cloud(d, cx - R * 0.95, cy, s * 0.95, (190, 220, 250))
    elif n == "cow":
        for side in (-1, 1):
            E(d, cx + side * R * 0.85, cy - R * 0.35, R * 0.25, R * 0.14, WHITE, w=w)
            d.line([cx + side * R * 0.4, cy - R * 0.62, cx + side * R * 0.55, cy - R * 0.9], fill=C(220, 190, 140), width=int(R * 0.12))
        E(d, cx, cy - R * 0.1, R * 0.65, R * 0.62, WHITE, w=w)
        E(d, cx - R * 0.3, cy - R * 0.35, R * 0.2, R * 0.18, C(60, 50, 60), w=0)
        E(d, cx, cy + R * 0.38, R * 0.5, R * 0.32, C(255, 185, 200), w=w)
        for side in (-1, 1):
            E(d, cx + side * R * 0.18, cy + R * 0.38, 8 * s, 10 * s, C(170, 90, 110), w=0)
            eye(d, cx + side * R * 0.25, cy - R * 0.1, R * 0.1, "open")
    elif n == "sheep":
        for k in range(10):
            a = k * math.pi / 5
            E(d, cx + math.cos(a) * R * 0.6, cy + math.sin(a) * R * 0.5, R * 0.3, R * 0.3, WHITE, w=w)
        E(d, cx, cy, R * 0.65, R * 0.55, WHITE, w=0)
        E(d, cx, cy + R * 0.05, R * 0.38, R * 0.42, C(80, 70, 80), w=w)
        for side in (-1, 1):
            E(d, cx + side * R * 0.45, cy - R * 0.05, R * 0.18, R * 0.09, C(80, 70, 80), w=0)
            E(d, cx + side * R * 0.14, cy - R * 0.02, R * 0.07, R * 0.07, WHITE, w=0)
            E(d, cx + side * R * 0.14, cy, R * 0.035, R * 0.035, OUT, w=0)
        E(d, cx, cy - R * 0.42, R * 0.25, R * 0.15, WHITE, w=0)
    elif n == "horse":
        Hc = C(180, 120, 80)
        poly(d, [(cx - R * 0.4, cy - R * 0.9), (cx - R * 0.25, cy - R * 0.55), (cx - R * 0.55, cy - R * 0.55)], Hc, w)
        poly(d, [(cx + R * 0.4, cy - R * 0.9), (cx + R * 0.25, cy - R * 0.55), (cx + R * 0.55, cy - R * 0.55)], Hc, w)
        E(d, cx, cy - R * 0.1, R * 0.5, R * 0.55, Hc, w=w)
        E(d, cx, cy + R * 0.5, R * 0.4, R * 0.35, C(230, 190, 150), w=w)
        for side in (-1, 1):
            E(d, cx + side * R * 0.15, cy + R * 0.55, 8 * s, 10 * s, C(120, 70, 50), w=0)
            eye(d, cx + side * R * 0.25, cy - R * 0.1, R * 0.1, "open")
        for k in range(3):
            E(d, cx - R * 0.15 + k * R * 0.15, cy - R * 0.62, R * 0.12, R * 0.16, C(110, 70, 50), w=0)
    elif n == "hen":
        E(d, cx, cy + R * 0.2, R * 0.75, R * 0.6, WHITE, w=w)
        E(d, cx - R * 0.35, cy - R * 0.4, R * 0.38, R * 0.38, WHITE, w=w)
        for k in range(3):
            E(d, cx - R * 0.5 + k * R * 0.14, cy - R * 0.78, R * 0.1, R * 0.12, C(240, 60, 70), w=0)
        poly(d, [(cx - R * 0.7, cy - R * 0.45), (cx - R * 0.95, cy - R * 0.35), (cx - R * 0.7, cy - R * 0.28)], C(255, 170, 50), max(3, w // 2))
        eye(d, cx - R * 0.42, cy - R * 0.45, R * 0.08, "open")
        d.arc([cx - R * 0.1, cy, cx + R * 0.6, cy + R * 0.5], 200, 340, fill=C(220, 220, 220), width=w)
        for k in range(3):
            E(d, cx + R * 0.7 + k * 0, cy - R * 0.1 + k * R * 0.15, R * 0.15, R * 0.08, WHITE, w=max(3, w // 2))
    elif n == "chick":
        E(d, cx, cy + R * 0.2, R * 0.7, R * 0.6, C(255, 225, 80), w=w)
        E(d, cx, cy - R * 0.35, R * 0.45, R * 0.42, C(255, 225, 80), w=w)
        E(d, cx, cy - R * 0.1, R * 0.4, R * 0.3, C(255, 225, 80), w=0)
        poly(d, [(cx - R * 0.12, cy - R * 0.25), (cx + R * 0.12, cy - R * 0.25), (cx, cy - R * 0.1)], C(255, 150, 50), max(3, w // 2))
        for side in (-1, 1):
            eye(d, cx + side * R * 0.18, cy - R * 0.42, R * 0.08, "open")
        d.line([cx - R * 0.05, cy - R * 0.77, cx + R * 0.05, cy - R * 0.95], fill=OUT, width=w)
    elif n == "lion":
        for k in range(12):
            a = k * math.pi / 6
            E(d, cx + math.cos(a) * R * 0.68, cy + math.sin(a) * R * 0.68, R * 0.3, R * 0.3, C(220, 130, 50), w=w)
        E(d, cx, cy, R * 0.7, R * 0.7, C(220, 130, 50), w=0)
        E(d, cx, cy, R * 0.55, R * 0.52, C(255, 200, 100), w=w)
        E(d, cx, cy + R * 0.22, R * 0.25, R * 0.17, C(255, 230, 180), w=0)
        poly(d, [(cx - R * 0.1, cy + R * 0.08), (cx + R * 0.1, cy + R * 0.08), (cx, cy + R * 0.18)], C(140, 80, 60), max(3, w // 2))
        for side in (-1, 1):
            eye(d, cx + side * R * 0.22, cy - R * 0.12, R * 0.09, "open")
        d.arc([cx - R * 0.15, cy + R * 0.12, cx + R * 0.15, cy + R * 0.35], 20, 160, fill=OUT, width=w)
    elif n == "elephant":
        G = C(170, 180, 210)
        for side in (-1, 1):
            E(d, cx + side * R * 0.62, cy - R * 0.1, R * 0.42, R * 0.55, G, w=w)
            E(d, cx + side * R * 0.62, cy - R * 0.1, R * 0.25, R * 0.36, C(255, 190, 210), w=0)
        E(d, cx, cy - R * 0.15, R * 0.5, R * 0.55, G, w=w)
        d.line([cx, cy + R * 0.2, cx, cy + R * 0.75], fill=OUT, width=int(R * 0.32))
        d.line([cx, cy + R * 0.2, cx, cy + R * 0.75], fill=G, width=int(R * 0.22))
        d.arc([cx, cy + R * 0.55, cx + R * 0.4, cy + R * 0.95], 90, 200, fill=OUT, width=int(R * 0.1))
        for side in (-1, 1):
            eye(d, cx + side * R * 0.2, cy - R * 0.2, R * 0.09, "open")
    elif n == "giraffe":
        Y = C(255, 200, 90)
        d.rectangle([cx - R * 0.18, cy - R * 0.25, cx + R * 0.18, cy + R * 1.0], fill=Y, outline=OUT, width=w)
        E(d, cx, cy - R * 0.5, R * 0.42, R * 0.32, Y, w=w)
        E(d, cx + R * 0.05, cy - R * 0.35, R * 0.3, R * 0.2, C(240, 180, 120), w=0)
        for side in (-1, 1):
            d.line([cx + side * R * 0.15, cy - R * 0.75, cx + side * R * 0.2, cy - R * 0.98], fill=OUT, width=w)
            E(d, cx + side * R * 0.2, cy - R * 1.0, R * 0.07, R * 0.07, C(170, 110, 60), w=0)
            eye(d, cx + side * R * 0.17, cy - R * 0.58, R * 0.07, "open")
        for (dx, dy) in ((-0.05, 0.05), (0.06, 0.35), (-0.07, 0.65), (0.05, 0.9)):
            E(d, cx + dx * R, cy + dy * R, R * 0.08, R * 0.07, C(200, 130, 60), w=0)
    elif n == "monkey":
        Bc = C(160, 110, 75)
        for side in (-1, 1):
            E(d, cx + side * R * 0.68, cy - R * 0.05, R * 0.22, R * 0.22, Bc, w=w)
            E(d, cx + side * R * 0.68, cy - R * 0.05, R * 0.12, R * 0.12, C(245, 210, 175), w=0)
        E(d, cx, cy, R * 0.6, R * 0.6, Bc, w=w)
        E(d, cx, cy + R * 0.12, R * 0.42, R * 0.38, C(245, 210, 175), w=0)
        for side in (-1, 1):
            E(d, cx + side * R * 0.18, cy - R * 0.12, R * 0.2, R * 0.2, C(245, 210, 175), w=0)
            eye(d, cx + side * R * 0.18, cy - R * 0.1, R * 0.08, "open")
        d.arc([cx - R * 0.18, cy + R * 0.1, cx + R * 0.18, cy + R * 0.35], 20, 160, fill=OUT, width=w)
    elif n == "dolphin":
        Bl = C(120, 180, 240)
        poly(d, [(cx - R * 0.1, cy - R * 0.35), (cx + R * 0.15, cy - R * 0.75), (cx + R * 0.25, cy - R * 0.3)], Bl, w)
        poly(d, [(cx + R * 0.75, cy - R * 0.05), (cx + R * 1.05, cy - R * 0.35), (cx + R * 1.05, cy + R * 0.25)], Bl, w)
        E(d, cx, cy, R * 0.85, R * 0.38, Bl, w=w)
        E(d, cx - R * 0.1, cy + R * 0.12, R * 0.6, R * 0.18, C(220, 240, 255), w=0)
        poly(d, [(cx - R * 0.8, cy - R * 0.02), (cx - R * 1.08, cy + R * 0.08), (cx - R * 0.8, cy + R * 0.14)], Bl, max(3, w // 2))
        eye(d, cx - R * 0.5, cy - R * 0.1, R * 0.08, "open")
    elif n == "turtle":
        Gr = C(110, 190, 110)
        for (dx, dy) in ((-0.55, 0.35), (0.55, 0.35), (-0.45, -0.25), (0.45, -0.25)):
            E(d, cx + dx * R, cy + dy * R + R * 0.1, R * 0.18, R * 0.13, C(170, 220, 140), w=w)
        E(d, cx - R * 0.85, cy + R * 0.05, R * 0.22, R * 0.2, C(170, 220, 140), w=w)
        eye(d, cx - R * 0.9, cy, R * 0.06, "open")
        d.chord([cx - R * 0.7, cy - R * 0.6, cx + R * 0.7, cy + R * 0.6], 180, 360, fill=Gr, outline=OUT, width=w)
        d.rectangle([cx - R * 0.7, cy - R * 0.02, cx + R * 0.7, cy + R * 0.08], fill=C(170, 220, 140), outline=OUT, width=max(3, w // 2))
        for (dx, dy) in ((-0.3, -0.25), (0.3, -0.25), (0, -0.4)):
            E(d, cx + dx * R, cy + dy * R, R * 0.14, R * 0.11, C(80, 160, 90), w=0)
    elif n == "whale":
        Bl = C(90, 140, 220)
        poly(d, [(cx + R * 0.7, cy + R * 0.05), (cx + R * 1.05, cy - R * 0.4), (cx + R * 1.05, cy + R * 0.3)], Bl, w)
        E(d, cx - R * 0.05, cy + R * 0.1, R * 0.85, R * 0.55, Bl, w=w)
        d.chord([cx - R * 0.85, cy - R * 0.1, cx + R * 0.75, cy + R * 0.65], 0, 180, fill=C(200, 225, 250))
        eye(d, cx - R * 0.45, cy - R * 0.05, R * 0.08, "open")
        for a in (-0.4, 0, 0.4):
            d.line([cx - R * 0.1, cy - R * 0.45, cx - R * 0.1 + a * R * 0.5, cy - R * 0.85], fill=C(120, 190, 250), width=w)
    elif n == "crab":
        Rd = C(240, 90, 80)
        for side in (-1, 1):
            for k in range(3):
                d.line([cx + side * R * 0.5, cy + R * 0.1 + k * R * 0.12, cx + side * R * 0.95, cy + R * 0.3 + k * R * 0.18], fill=OUT, width=w)
            E(d, cx + side * R * 0.75, cy - R * 0.45, R * 0.22, R * 0.2, Rd, w=w)
            d.line([cx + side * R * 0.2, cy - R * 0.4, cx + side * R * 0.25, cy - R * 0.65], fill=OUT, width=w)
            E(d, cx + side * R * 0.25, cy - R * 0.68, R * 0.1, R * 0.1, WHITE, w=max(3, w // 2))
            E(d, cx + side * R * 0.25, cy - R * 0.68, R * 0.04, R * 0.04, OUT, w=0)
        E(d, cx, cy, R * 0.6, R * 0.42, Rd, w=w)
        d.arc([cx - R * 0.15, cy - R * 0.05, cx + R * 0.15, cy + R * 0.15], 20, 160, fill=OUT, width=w)
    elif n == "octopus":
        Pu = C(190, 130, 230)
        for k in range(6):
            x = cx - R * 0.6 + k * R * 0.24
            d.line([x, cy + R * 0.1, x + (k - 2.5) * R * 0.08, cy + R * 0.85], fill=OUT, width=int(R * 0.2))
            d.line([x, cy + R * 0.1, x + (k - 2.5) * R * 0.08, cy + R * 0.85], fill=Pu, width=int(R * 0.12))
        E(d, cx, cy - R * 0.2, R * 0.65, R * 0.6, Pu, w=w)
        face(d, cx, cy - R * 0.15, R * 0.8)
    elif n == "ladybug":
        E(d, cx, cy - R * 0.55, R * 0.35, R * 0.3, C(60, 50, 60), w=w)
        E(d, cx, cy + R * 0.1, R * 0.75, R * 0.7, C(240, 60, 60), w=w)
        d.line([cx, cy - R * 0.6, cx, cy + R * 0.8], fill=OUT, width=w)
        for (dx, dy) in ((-0.4, -0.1), (0.4, -0.1), (-0.35, 0.35), (0.35, 0.35)):
            E(d, cx + dx * R, cy + dy * R, R * 0.13, R * 0.13, C(60, 50, 60), w=0)
    elif n == "bee":
        for side in (-1, 1):
            E(d, cx + side * R * 0.25, cy - R * 0.55, R * 0.3, R * 0.25, C(230, 245, 255), w=w)
        E(d, cx, cy + R * 0.05, R * 0.75, R * 0.5, C(255, 210, 60), w=w)
        for k in (-1, 1):
            d.line([cx + k * R * 0.2, cy - R * 0.4, cx + k * R * 0.2, cy + R * 0.5], fill=OUT, width=int(R * 0.15))
        eye(d, cx - R * 0.5, cy - R * 0.05, R * 0.08, "open")
    elif n == "butterfly":
        for side in (-1, 1):
            E(d, cx + side * R * 0.5, cy - R * 0.3, R * 0.45, R * 0.4, C(255, 140, 190), w=w)
            E(d, cx + side * R * 0.42, cy + R * 0.35, R * 0.32, R * 0.3, C(140, 190, 250), w=w)
            E(d, cx + side * R * 0.5, cy - R * 0.3, R * 0.15, R * 0.15, C(255, 230, 120), w=0)
        E(d, cx, cy, R * 0.12, R * 0.6, C(90, 70, 80), w=w)
    elif n == "block":
        rr(d, [cx - R * 0.75, cy - R * 0.75, cx + R * 0.75, cy + R * 0.75], 18, C(255, 120, 160), w)
        f = ImageFont.truetype(FONT, int(R * 1.0))
        d.text((cx - f.getlength("A") / 2, cy - R * 0.68), "A", font=f, fill=WHITE, stroke_width=max(2, w // 2), stroke_fill=OUT)
    elif n == "teddy_i":
        F = C(212, 156, 88)
        for side in (-1, 1):
            E(d, cx + side * R * 0.55, cy - R * 0.6, R * 0.25, R * 0.25, F, w=w)
        E(d, cx, cy - R * 0.1, R * 0.7, R * 0.62, F, w=w)
        E(d, cx, cy + R * 0.12, R * 0.3, R * 0.22, C(246, 214, 166), w=0)
        E(d, cx, cy + R * 0.03, R * 0.1, R * 0.07, C(70, 44, 40), w=0)
        for side in (-1, 1):
            eye(d, cx + side * R * 0.28, cy - R * 0.2, R * 0.09, "open")
        for side in (-1, 1):
            poly(d, [(cx, cy + R * 0.6), (cx + side * R * 0.3, cy + R * 0.45), (cx + side * R * 0.3, cy + R * 0.75)], C(225, 45, 60), max(3, w // 2))
    elif n == "balloon":
        d.line([cx, cy + R * 0.45, cx + R * 0.1, cy + R * 1.0], fill=OUT, width=max(3, w // 2))
        E(d, cx, cy - R * 0.2, R * 0.55, R * 0.68, C(255, 100, 140), w=w)
        poly(d, [(cx - R * 0.1, cy + R * 0.55), (cx + R * 0.1, cy + R * 0.55), (cx, cy + R * 0.45)], C(255, 100, 140), max(3, w // 2))
        E(d, cx - R * 0.22, cy - R * 0.45, R * 0.1, R * 0.18, (255, 255, 255, 180), w=0)
    elif n == "snowman":
        E(d, cx, cy + R * 0.45, R * 0.55, R * 0.5, WHITE, w=w)
        E(d, cx, cy - R * 0.35, R * 0.38, R * 0.36, WHITE, w=w)
        poly(d, [(cx, cy - R * 0.32), (cx + R * 0.35, cy - R * 0.25), (cx, cy - R * 0.2)], C(255, 150, 50), max(3, w // 2))
        for side in (-1, 1):
            E(d, cx + side * R * 0.13, cy - R * 0.45, R * 0.05, R * 0.05, OUT, w=0)
        d.rectangle([cx - R * 0.4, cy - R * 0.05, cx + R * 0.4, cy + R * 0.05], fill=C(100, 170, 240))
        rr(d, [cx - R * 0.3, cy - R * 0.95, cx + R * 0.3, cy - R * 0.65], 6, C(80, 70, 90), max(3, w // 2))
    elif n == "cocoa":
        d.arc([cx + R * 0.35, cy - R * 0.2, cx + R * 0.9, cy + R * 0.45], 270, 90, fill=OUT, width=int(R * 0.15))
        rr(d, [cx - R * 0.55, cy - R * 0.35, cx + R * 0.55, cy + R * 0.75], 22, C(240, 90, 90), w)
        for k in (-1, 0, 1):
            x = cx + k * R * 0.3
            d.arc([x - R * 0.1, cy - R * 0.95, x + R * 0.1, cy - R * 0.65], 90, 270, fill=C(200, 200, 210), width=w)
            d.arc([x - R * 0.1, cy - R * 0.7, x + R * 0.1, cy - R * 0.45], 270, 90, fill=C(200, 200, 210), width=w)
    elif n == "snail":
        E(d, cx - R * 0.1, cy + R * 0.55, R * 0.85, R * 0.18, C(190, 230, 160), w=w)
        E(d, cx, cy + R * 0.05, R * 0.5, R * 0.5, C(255, 170, 90), w=w)
        for k in range(3):
            d.arc([cx - R * (0.4 - k * 0.12), cy + R * 0.05 - R * (0.4 - k * 0.12), cx + R * (0.4 - k * 0.12), cy + R * 0.05 + R * (0.4 - k * 0.12)], 0, 270, fill=C(220, 120, 60), width=w)
        d.line([cx - R * 0.75, cy + R * 0.4, cx - R * 0.8, cy + R * 0.05], fill=OUT, width=w)
        E(d, cx - R * 0.8, cy + R * 0.02, R * 0.07, R * 0.07, OUT, w=0)
    elif n == "rabbit":
        for side in (-1, 1):
            E(d, cx + side * R * 0.22, cy - R * 0.6, R * 0.16, R * 0.42, WHITE, w=w)
            E(d, cx + side * R * 0.22, cy - R * 0.6, R * 0.07, R * 0.3, C(255, 190, 210), w=0)
        E(d, cx, cy + R * 0.15, R * 0.55, R * 0.5, WHITE, w=w)
        face(d, cx, cy + R * 0.15, R * 0.8)
    elif n in ("happy", "sad", "sleepy_f"):
        E(d, cx, cy, R * 0.85, R * 0.85, C(255, 215, 80), w=w)
        for side in (-1, 1):
            eye(d, cx + side * R * 0.3, cy - R * 0.2, R * 0.12, "closed" if n == "sleepy_f" else "open")
        if n == "happy":
            d.chord([cx - R * 0.45, cy - R * 0.1, cx + R * 0.45, cy + R * 0.6], 0, 180, fill=C(160, 55, 75), outline=OUT, width=w)
        elif n == "sad":
            d.arc([cx - R * 0.35, cy + R * 0.25, cx + R * 0.35, cy + R * 0.65], 200, 340, fill=OUT, width=w)
            E(d, cx + R * 0.32, cy + R * 0.05, R * 0.07, R * 0.12, C(120, 180, 250), w=0)
        else:
            d.arc([cx - R * 0.15, cy + R * 0.2, cx + R * 0.15, cy + R * 0.4], 20, 160, fill=OUT, width=w)
        for side in (-1, 1):
            E(d, cx + side * R * 0.55, cy + R * 0.15, R * 0.14, R * 0.09, (255, 150, 150, 160), w=0)
    elif n in ("box_open", "box_closed"):
        rr(d, [cx - R * 0.8, cy - R * 0.2, cx + R * 0.8, cy + R * 0.8], 8, C(230, 180, 120), w)
        if n == "box_open":
            poly(d, [(cx - R * 0.8, cy - R * 0.2), (cx - R * 1.05, cy - R * 0.65), (cx - R * 0.25, cy - R * 0.6), (cx, cy - R * 0.2)], C(240, 200, 145), w)
            poly(d, [(cx + R * 0.8, cy - R * 0.2), (cx + R * 1.05, cy - R * 0.65), (cx + R * 0.25, cy - R * 0.6), (cx, cy - R * 0.2)], C(240, 200, 145), w)
            E(d, cx - R * 0.25, cy - R * 0.25, R * 0.22, R * 0.22, C(80, 150, 240), w=w)
            poly(d, star_pts(cx + R * 0.3, cy - R * 0.3, R * 0.22), C(255, 215, 60), max(3, w // 2))
        else:
            rr(d, [cx - R * 0.88, cy - R * 0.38, cx + R * 0.88, cy - R * 0.15], 6, C(240, 200, 145), w)
            d.rectangle([cx - R * 0.08, cy - R * 0.38, cx + R * 0.08, cy + R * 0.8], fill=C(255, 120, 160))
    elif n in ("cup_full", "cup_empty"):
        poly(d, [(cx - R * 0.5, cy - R * 0.7), (cx + R * 0.5, cy - R * 0.7), (cx + R * 0.4, cy + R * 0.8), (cx - R * 0.4, cy + R * 0.8)], C(220, 240, 255, 200), w)
        if n == "cup_full":
            poly(d, [(cx - R * 0.47, cy - R * 0.45), (cx + R * 0.47, cy - R * 0.45), (cx + R * 0.38, cy + R * 0.75), (cx - R * 0.38, cy + R * 0.75)], C(255, 170, 60), 0)
        d.line([cx - R * 0.35, cy - R * 0.55, cx - R * 0.3, cy + R * 0.6], fill=(255, 255, 255, 200), width=w)
    elif n == "toothbrush":
        d.line([cx - R * 0.9, cy + R * 0.6, cx + R * 0.5, cy - R * 0.4], fill=OUT, width=int(R * 0.26))
        d.line([cx - R * 0.9, cy + R * 0.6, cx + R * 0.5, cy - R * 0.4], fill=C(100, 180, 240), width=int(R * 0.16))
        poly(d, [(cx + R * 0.35, cy - R * 0.55), (cx + R * 0.75, cy - R * 0.85), (cx + R * 0.9, cy - R * 0.65), (cx + R * 0.5, cy - R * 0.35)], WHITE, w)
        for k in range(4):
            d.line([cx + R * (0.42 + k * 0.1), cy - R * (0.55 + k * 0.07), cx + R * (0.32 + k * 0.1), cy - R * (0.7 + k * 0.07)], fill=C(150, 210, 250), width=max(3, w // 2))
        E(d, cx + R * 0.75, cy - R * 0.95, R * 0.16, R * 0.1, C(200, 240, 255), w=max(3, w // 2))
    elif n == "toothpaste":
        poly(d, [(cx - R * 0.9, cy - R * 0.3), (cx + R * 0.5, cy - R * 0.35), (cx + R * 0.6, cy + R * 0.35), (cx - R * 0.9, cy + R * 0.3)], WHITE, w)
        d.rectangle([cx - R * 0.6, cy - R * 0.3, cx + R * 0.1, cy + R * 0.3], fill=C(120, 200, 240))
        rr(d, [cx + R * 0.55, cy - R * 0.18, cx + R * 0.85, cy + R * 0.18], 6, C(255, 120, 160), w)
    elif n == "soap":
        rr(d, [cx - R * 0.8, cy - R * 0.35, cx + R * 0.8, cy + R * 0.45], 40, C(255, 180, 210), w)
        for (dx, dy, r) in ((-0.4, -0.65, 0.2), (0.15, -0.8, 0.14), (0.55, -0.55, 0.22), (-0.05, -0.5, 0.1)):
            E(d, cx + dx * R, cy + dy * R, r * R, r * R, C(220, 240, 255, 230), w=max(3, w // 2))
    elif n == "towel":
        rr(d, [cx - R * 0.6, cy - R * 0.8, cx + R * 0.6, cy + R * 0.85], 14, C(120, 200, 200), w)
        for k in range(2):
            d.line([cx - R * 0.6, cy + R * (0.5 + k * 0.15), cx + R * 0.6, cy + R * (0.5 + k * 0.15)], fill=WHITE, width=w)
        d.line([cx - R * 0.8, cy - R * 0.8, cx + R * 0.8, cy - R * 0.8], fill=C(200, 140, 90), width=int(R * 0.12))
    elif n == "water":
        for (dx, dy, r) in ((0, -0.2, 0.55), (-0.5, 0.45, 0.3), (0.5, 0.45, 0.3)):
            yy = cy + dy * R
            E(d, cx + dx * R, yy, r * R, r * R, C(110, 180, 250), w=w)
            poly(d, [(cx + dx * R - r * R * 0.75, yy - r * R * 0.6), (cx + dx * R + r * R * 0.75, yy - r * R * 0.6), (cx + dx * R, yy - r * R * 1.8)], C(110, 180, 250), 0)
            E(d, cx + dx * R - r * R * 0.3, yy - r * R * 0.1, r * R * 0.2, r * R * 0.3, (255, 255, 255, 200), w=0)
    elif n == "pajamas":
        P = C(170, 200, 255)
        poly(d, [(cx - R * 0.45, cy - R * 0.85), (cx + R * 0.45, cy - R * 0.85), (cx + R, cy - R * 0.45), (cx + R * 0.75, cy - R * 0.2), (cx + R * 0.5, cy - R * 0.35), (cx + R * 0.5, cy + R * 0.1),
                 (cx - R * 0.5, cy + R * 0.1), (cx - R * 0.5, cy - R * 0.35), (cx - R * 0.75, cy - R * 0.2), (cx - R, cy - R * 0.45)], P, w)
        poly(d, [(cx - R * 0.45, cy + R * 0.15), (cx + R * 0.45, cy + R * 0.15), (cx + R * 0.5, cy + R * 0.95), (cx + R * 0.05, cy + R * 0.95), (cx, cy + R * 0.4), (cx - R * 0.05, cy + R * 0.95), (cx - R * 0.5, cy + R * 0.95)], P, w)
        for (dx, dy) in ((-0.2, -0.5), (0.25, -0.25), (-0.25, 0.5), (0.25, 0.7)):
            poly(d, star_pts(cx + dx * R, cy + dy * R, R * 0.1), C(255, 230, 120), 0)
    elif n == "toybox":
        rr(d, [cx - R * 0.9, cy - R * 0.2, cx + R * 0.9, cy + R * 0.85], 14, C(255, 160, 190), w)
        E(d, cx - R * 0.45, cy - R * 0.25, R * 0.3, R * 0.3, C(80, 150, 240), w=w)
        rr(d, [cx - R * 0.05, cy - R * 0.6, cx + R * 0.4, cy - R * 0.15], 6, C(255, 215, 80), w)
        poly(d, star_pts(cx + R * 0.65, cy - R * 0.35, R * 0.25), C(140, 210, 130), max(3, w // 2))
        f = ImageFont.truetype(FONT, int(R * 0.4))
        d.text((cx - f.getlength("TOYS") / 2, cy + R * 0.12), "TOYS", font=f, fill=WHITE, stroke_width=3, stroke_fill=OUT)
    elif n == "bubbles":
        for (dx, dy, r) in ((-0.4, 0.2, 0.4), (0.35, -0.3, 0.35), (0.4, 0.45, 0.25), (-0.3, -0.55, 0.22), (0.0, 0.0, 0.15)):
            E(d, cx + dx * R, cy + dy * R, r * R, r * R, C(210, 235, 255, 220), w=max(3, w // 2))
            E(d, cx + dx * R - r * R * 0.35, cy + dy * R - r * R * 0.35, r * R * 0.18, r * R * 0.18, WHITE, w=0)
    elif n == "drum":
        E(d, cx, cy + R * 0.5, R * 0.8, R * 0.3, C(240, 80, 90), w=w)
        d.rectangle([cx - R * 0.8, cy - R * 0.3, cx + R * 0.8, cy + R * 0.5], fill=C(240, 80, 90), outline=None)
        d.line([cx - R * 0.8, cy - R * 0.3, cx - R * 0.8, cy + R * 0.5], fill=OUT, width=w)
        d.line([cx + R * 0.8, cy - R * 0.3, cx + R * 0.8, cy + R * 0.5], fill=OUT, width=w)
        for k in range(5):
            x = cx - R * 0.8 + k * R * 0.4
            d.line([x, cy - R * 0.25, x + R * 0.2, cy + R * 0.45], fill=C(255, 220, 100), width=w)
        E(d, cx, cy - R * 0.3, R * 0.8, R * 0.3, C(250, 245, 235), w=w)
        for side in (-1, 1):
            d.line([cx + side * R * 0.2, cy - R * 0.4, cx + side * R * 0.7, cy - R * 0.95], fill=C(200, 140, 90), width=int(R * 0.09))
    elif n == "ant":
        Bk = C(90, 60, 70)
        for k in range(3):
            for side in (-1, 1):
                d.line([cx - R * 0.3 + k * R * 0.35, cy + R * 0.1, cx - R * 0.3 + k * R * 0.35 + side * R * 0.15, cy + R * 0.6], fill=OUT, width=w)
        for (dx, r) in ((-0.6, 0.28), (0, 0.24), (0.55, 0.36)):
            E(d, cx + dx * R, cy, r * R, r * R * 0.85, Bk, w=w)
        for side in (-1, 1):
            d.line([cx - R * 0.7, cy - R * 0.2, cx - R * 0.8 + side * R * 0.15, cy - R * 0.65], fill=OUT, width=w)
        E(d, cx - R * 0.68, cy - R * 0.05, R * 0.07, R * 0.07, WHITE, w=0)
    elif n == "sun_up":
        icon(d, "sun", cx, cy, s)
    elif n.startswith("shape_"):
        shape(d, n[6:], cx, cy, R, (255, 150, 190), w)
    else:
        mzart._obj(d, n, cx, cy, s)


SHAPE_COL = {"circle": (255, 105, 150), "square": (80, 160, 240), "triangle": (255, 175, 50), "star": (255, 210, 60),
             "heart": (240, 80, 120), "rectangle": (90, 190, 110), "oval": (170, 110, 230), "diamond": (80, 200, 210)}


def shape(d, kind, cx, cy, R, col, w):
    col = tuple(col[:3]) + (255,)
    if kind == "circle":
        E(d, cx, cy, R * 0.85, R * 0.85, col, w=w)
    elif kind == "square":
        rr(d, [cx - R * 0.8, cy - R * 0.8, cx + R * 0.8, cy + R * 0.8], 12, col, w)
    elif kind == "triangle":
        poly(d, [(cx, cy - R * 0.9), (cx + R * 0.95, cy + R * 0.75), (cx - R * 0.95, cy + R * 0.75)], col, w)
    elif kind == "star":
        poly(d, star_pts(cx, cy, R * 0.98), col, w)
    elif kind == "heart":
        for side in (-1, 1):
            E(d, cx + side * R * 0.45, cy - R * 0.25, R * 0.5, R * 0.48, col, w=w)
        poly(d, [(cx, cy + R * 0.85), (cx - R * 0.9, cy - R * 0.08), (cx + R * 0.9, cy - R * 0.08)], col, w)
        poly(d, [(cx, cy + R * 0.75), (cx - R * 0.82, cy - R * 0.1), (cx + R * 0.82, cy - R * 0.1)], col, 0)
        E(d, cx, cy - R * 0.12, R * 0.55, R * 0.3, col, w=0)
    elif kind == "rectangle":
        rr(d, [cx - R * 1.0, cy - R * 0.55, cx + R * 1.0, cy + R * 0.55], 12, col, w)
    elif kind == "oval":
        E(d, cx, cy, R * 1.0, R * 0.62, col, w=w)
    elif kind == "diamond":
        poly(d, [(cx, cy - R * 0.95), (cx + R * 0.7, cy), (cx, cy + R * 0.95), (cx - R * 0.7, cy)], col, w)


# ---------------------------------------------------------------- cards
BORDER = [(255, 105, 150), (80, 160, 240), (255, 160, 40), (90, 190, 110), (170, 110, 230), (240, 80, 80)]
COLORS = {"red": (235, 60, 70), "blue": (70, 140, 240), "yellow": (255, 200, 40), "green": (80, 185, 90), "orange": (255, 145, 30),
          "purple": (160, 95, 220), "pink": (255, 120, 180), "brown": (160, 105, 65), "white": (250, 250, 250), "black": (50, 45, 55)}
NUMW = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()


def _bcol(key):
    return BORDER[zlib.crc32(key.encode()) % len(BORDER)] + (255,)


def _canvas(W, H, col):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([30, 40, W - 20, H - 10], 60, fill=(60, 30, 60, 90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, W - 30, H - 30], 60, fill=WHITE, outline=col, width=22)
    return im, d


def _ctext(d, W, y, text, size, fill, stroke=8):
    f = ImageFont.truetype(FONT, size)
    while f.getlength(text) > W - 110 and size > 30:
        size -= 6
        f = ImageFont.truetype(FONT, size)
    x = (W - 10 - f.getlength(text)) / 2
    if stroke:
        d.text((x + 5, y + 5), text, font=f, fill=(60, 30, 60, 50))
        d.text((x, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=DARK)
    else:
        d.text((x, y), text, font=f, fill=fill)


def _label(name):
    return name.replace("_", " ").replace("yoyo", "yo-yo").replace("teddy i", "teddy").replace(" i", "")


def make_card(pid, h):
    p = pid.split(":")
    k = p[0]
    W, H = 720, 860
    if k == "w":  # picture + word
        obj = p[1]
        lab = p[2] if len(p) > 2 else _label(obj)
        im, d = _canvas(W, H, _bcol(obj))
        icon(d, obj, W / 2 - 5, 380, 1.75)
        _ctext(d, W, 690, lab, 90, DARK, 0)
    elif k == "t":  # speech words + icon (greetings)
        text, obj = p[1], p[2]
        im, d = _canvas(W, H, _bcol(text))
        icon(d, obj, W / 2 - 5, 470, 1.45)
        _ctext(d, W, 50, text, 120, _bcol(text), 8)
    elif k == "n":  # number + that many things
        N, obj = int(p[1]), p[2]
        im, d = _canvas(W, H, BORDER[N % 6] + (255,))
        _ctext(d, W, 0, str(N), 230, BORDER[N % 6] + (255,), 10)
        cols = 1 if N == 1 else 2 if N <= 4 else 3 if N <= 9 else 4 if N <= 12 else 5
        rows = math.ceil(N / cols)
        cell = min(560 / cols, 360 / rows)
        sc = cell / 300 * (1.5 if N == 1 else 1.0)
        for i in range(N):
            r, c = divmod(i, cols)
            nin = cols if r < rows - 1 else N - cols * (rows - 1)
            x = W / 2 - 5 + (c - (nin - 1) / 2) * cell
            y = 470 + (r - (rows - 1) / 2) * cell
            icon(d, obj, x, y, sc * 0.95)
        _ctext(d, W, 712, NUMW[N] if N < len(NUMW) else str(N), 74, DARK, 0)
    elif k == "nn":  # just the big number
        N = int(p[1])
        im, d = _canvas(W, H, BORDER[N % 6] + (255,))
        _ctext(d, W, 150, str(N), 400, BORDER[N % 6] + (255,), 14)
        _ctext(d, W, 690, NUMW[N], 90, DARK, 0)
    elif k == "c":  # colour
        cname, obj = p[1], p[2]
        col = COLORS[cname] + (255,)
        im, d = _canvas(W, H, col if cname != "white" else (200, 200, 210, 255))
        for a in range(10):
            ang = a * math.pi / 5
            E(d, 230 + math.cos(ang) * 120, 300 + math.sin(ang) * 120, 50, 50, col, w=0)
        E(d, 230, 300, 140, 140, col, w=8)
        icon(d, obj, 470, 450, 1.25)
        _ctext(d, W, 680, cname, 110, col, 8)
    elif k == "s":  # shape
        sname = p[1]
        col = SHAPE_COL.get(sname, (255, 150, 190))
        im, d = _canvas(W, H, col + (255,))
        shape(d, sname, W / 2 - 5, 360, 230, col, 10)
        _ctext(d, W, 680, sname, 100, col + (255,), 8)
    elif k == "o":  # opposites / comparison: o:wordA:wordB:iconA:iconB[:size]
        a, b, ia, ib = p[1], p[2], p[3], p[4]
        size = len(p) > 5 and p[5] == "size"
        W = 1300
        im, d = _canvas(W, H, _bcol(a + b))
        d.line([W / 2 - 5, 90, W / 2 - 5, H - 110], fill=(230, 220, 235, 255), width=8)
        for side, (wd, ic) in ((-1, (a, ia)), (1, (b, ib))):
            cx = W / 2 - 5 + side * W / 4
            sc = (1.75 if side < 0 else 0.75) if size else 1.45
            cy = 400 if not size else (380 if side < 0 else 500)
            icon(d, ic, cx, cy, sc)
            f = ImageFont.truetype(FONT, 90)
            d.text((cx - f.getlength(wd) / 2, 680), wd, font=f, fill=_bcol(wd), stroke_width=6, stroke_fill=DARK)
    elif k == "q":
        im, d = _canvas(W, H, (255, 170, 60, 255))
        _ctext(d, W, 140, "?", 520, (255, 170, 60, 255), 14)
    elif k == "seq":  # missing letter / number:  seq:A,B,_
        items = p[1].split(",")
        W = 1300
        im, d = _canvas(W, H, (120, 170, 250, 255))
        n = len(items)
        bw = min(330, (W - 160) / n)
        f = ImageFont.truetype(FONT, int(bw * 0.8))
        for i, t in enumerate(items):
            x0 = W / 2 - 5 - n * bw / 2 + i * bw + 12
            col = BORDER[(ord(t[0]) if t != "_" else 0) % 6] + (255,)
            if t == "_":
                d.rounded_rectangle([x0, 250, x0 + bw - 24, 250 + bw - 24], 30, fill=(255, 245, 200, 255), outline=DARK, width=8)
                q = "?"
                d.text((x0 + (bw - 24 - f.getlength(q)) / 2, 250 - bw * 0.06), q, font=f, fill=(255, 170, 60, 255), stroke_width=6, stroke_fill=DARK)
            else:
                d.rounded_rectangle([x0, 250, x0 + bw - 24, 250 + bw - 24], 30, fill=col, outline=DARK, width=8)
                d.text((x0 + (bw - 24 - f.getlength(t)) / 2, 250 - bw * 0.06), t, font=f, fill=WHITE, stroke_width=6, stroke_fill=DARK)
    else:
        raise KeyError(pid)
    return finish(im, (int(h * W / H), h))


class Chars(dict):
    """art.CHARS that also understands pattern ids for cards and bare icons."""

    def __missing__(self, cid):
        k = cid.split(":")[0]
        if k in ("w", "t", "n", "nn", "c", "s", "o", "q", "seq"):
            hh = 0.66 if k not in ("o", "seq") else 0.62
            v = dict(fn=lambda eyes="open", m=0, h=600, _p=cid: make_card(_p, h), kw={}, h=hh, static=True)
        elif k == "i":  # bare icon prop: i:name[:size]
            name = cid.split(":")[1]
            sz = float(cid.split(":")[2]) if len(cid.split(":")) > 2 else 0.26

            def fn(eyes="open", m=0, h=300, _n=name):
                im = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
                icon(ImageDraw.Draw(im), _n, 180, 180, 1.2)
                return finish(im, (h, h))
            v = dict(fn=fn, kw={}, h=sz, static=True)
        else:
            raise KeyError(cid)
        self[cid] = v
        return v


art.CHARS = Chars(art.CHARS)
_orig_sprites = art.sprites


def sprites(cid, H, scale=1.0):
    c = art.CHARS[cid]
    if c.get("static"):
        one = c["fn"](h=int(H * c["h"] * scale), **c["kw"])
        return {(e, m): one for e in ("open", "closed") for m in (0, 1, 2)}
    return _orig_sprites(cid, H, scale)


art.sprites = sprites


# ---------------------------------------------------------------- more backgrounds
_prev_bg = art.background


def background(kind, W, H):
    land = W > H
    ground = 0.86 if land else 0.74
    rnd = random.Random(7)
    if kind in ("mz_bedroom", "mz_bedroom_night"):
        night = kind.endswith("night")
        im = art.grad(W, H, (70, 80, 150) if night else (215, 225, 255), (120, 110, 180) if night else (250, 240, 255))
        d = ImageDraw.Draw(im)
        wy = H * (ground - 0.16)
        d.rectangle([0, wy, W, H], fill=(95, 105, 170) if night else (225, 215, 250))
        fy = H * (ground - 0.06)
        d.rectangle([0, fy, W, H], fill=(120, 95, 120) if night else (240, 205, 160))
        wx0, wx1 = (W * 0.06, W * 0.26) if land else (W * 0.08, W * 0.45)
        wy0, wy1 = H * 0.1, H * (0.42 if land else 0.3)
        d.rounded_rectangle([wx0, wy0, wx1, wy1], 30, fill=(30, 40, 100) if night else (170, 220, 255), outline=(255, 255, 255), width=14)
        if night:
            mx, my = wx0 + (wx1 - wx0) * 0.7, wy0 + (wy1 - wy0) * 0.32
            d.ellipse([mx - 45, my - 45, mx + 45, my + 45], fill=(255, 235, 150))
            d.ellipse([mx - 20, my - 60, mx + 65, my + 25], fill=(30, 40, 100))
            for _ in range(8):
                x, y = rnd.uniform(wx0 + 20, wx1 - 20), rnd.uniform(wy0 + 20, wy1 - 20)
                d.polygon(star_pts(x, y, 10), fill=(255, 240, 170))
        else:
            art.cloud(d, wx0 + 30, wy0 + (wy1 - wy0) * 0.5, (wx1 - wx0) / 520, (255, 255, 255))
        d.line([(wx0 + wx1) / 2, wy0, (wx0 + wx1) / 2, wy1], fill=(255, 255, 255), width=10)
        for side in (wx0 - 20, wx1 + 20):
            d.polygon([(side - 40, wy0 - 20), (side + 40, wy0 - 20), (side + 25, wy1 + 30), (side - 25, wy1 + 30)], fill=(170, 150, 230) if night else (200, 180, 250))
        # little bed on the right
        bx0, bx1 = (W * 0.68, W * 0.97) if land else (W * 0.45, W * 0.98)
        by = H * (ground - 0.02)
        d.rounded_rectangle([bx1 - (bx1 - bx0) * 0.1, by - H * 0.3, bx1, by + H * 0.04], 20, fill=(220, 165, 115))
        d.rounded_rectangle([bx0, by - H * 0.14, bx1 - (bx1 - bx0) * 0.08, by - H * 0.02], 26, fill=(255, 170, 200))
        d.rounded_rectangle([bx1 - (bx1 - bx0) * 0.32, by - H * 0.2, bx1 - (bx1 - bx0) * 0.1, by - H * 0.12], 30, fill=(255, 255, 255))
        for k in range(5):
            x = bx0 + (bx1 - bx0) * (0.1 + k * 0.15)
            d.polygon(star_pts(x, by - H * 0.08, H * 0.012), fill=(255, 235, 150))
        d.rectangle([bx0, by - H * 0.02, bx0 + 20, by + H * 0.04], fill=(220, 165, 115))
        # stars wall decals / bunting
        for k in range(10):
            x = W * (k + 0.5) / 10
            d.polygon(star_pts(x, H * 0.05 + (k % 2) * H * 0.03, H * 0.015), fill=(255, 235, 150) if night else (255, 200, 225))
        return im, None, []
    if kind == "mz_bathroom":
        im = art.grad(W, H, (210, 240, 250), (235, 250, 255))
        d = ImageDraw.Draw(im)
        t = int(H * 0.07)
        for y in range(int(H * 0.3), int(H * ground), t):
            for x in range(0, W, t):
                d.rectangle([x + 3, y + 3, x + t - 3, y + t - 3], fill=(190, 230, 240) if (x // t + y // t) % 2 else (220, 245, 250))
        fy = H * (ground - 0.06)
        d.rectangle([0, fy, W, H], fill=(200, 215, 235))
        sx = W * (0.5 if land else 0.5)
        d.rounded_rectangle([sx - W * 0.09, H * 0.08, sx + W * 0.09, H * 0.3], 40, fill=(240, 250, 255), outline=(255, 255, 255), width=12)
        d.rounded_rectangle([sx - W * 0.12, H * 0.42, sx + W * 0.12, H * 0.5], 30, fill=(255, 255, 255))
        d.rectangle([sx - W * 0.03, H * 0.5, sx + W * 0.03, fy], fill=(255, 255, 255))
        d.rounded_rectangle([sx - W * 0.015, H * 0.37, sx + W * 0.015, H * 0.43], 8, fill=(190, 200, 215))
        for k in range(5):
            x, y, r = rnd.uniform(0, W), rnd.uniform(H * 0.1, H * 0.6), rnd.uniform(H * 0.015, H * 0.035)
            d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255), width=4)
        d.rounded_rectangle([W * 0.04, H * 0.42, W * 0.12, H * 0.62], 20, fill=(255, 170, 200))
        d.line([W * 0.02, H * 0.42, W * 0.14, H * 0.42], fill=(200, 160, 120), width=10)
        return im, None, []
    if kind == "mz_ocean":
        im = art.grad(W, H, (90, 190, 240), (30, 100, 180))
        d = ImageDraw.Draw(im)
        for k in range(6):
            x = W * (k + 0.3) / 6
            d.polygon([(x - W * 0.03, 0), (x + W * 0.01, 0), (x + W * 0.08, H * 0.6), (x + W * 0.05, H * 0.6)], fill=(105, 200, 245))
        sy = H * (ground - 0.06)
        d.ellipse([-W * 0.2, sy, W * 1.2, sy + H * 0.5], fill=(250, 220, 160))
        for k in range(9):
            x = rnd.uniform(0, W)
            hh = rnd.uniform(H * 0.12, H * 0.3)
            for j in range(6):
                y = sy + H * 0.04 - j * hh / 6
                d.ellipse([x - H * 0.02 + (j % 2) * 10, y - hh / 10, x + H * 0.02 + (j % 2) * 10, y + hh / 10], fill=(80, 190, 120))
        for k in range(18):
            x, y, r = rnd.uniform(0, W), rnd.uniform(H * 0.05, H * 0.7), rnd.uniform(5, 18)
            d.ellipse([x - r, y - r, x + r, y + r], outline=(220, 245, 255), width=3)
        for k in range(5):
            x = rnd.uniform(0, W)
            d.ellipse([x - 30, sy + H * 0.05 - 15, x + 30, sy + H * 0.05 + 15], fill=(255, 180, 200))
        return im, None, []
    if kind == "mz_farm":
        im, fg, st = mzart.background("mz_garden", W, H)
        d = ImageDraw.Draw(im)
        bx = W * (0.8 if land else 0.75)
        by = H * (ground - 0.1)
        bw = W * (0.14 if land else 0.3)
        d.rectangle([bx - bw / 2, by - bw * 0.7, bx + bw / 2, by], fill=(225, 80, 80))
        d.polygon([(bx - bw * 0.6, by - bw * 0.7), (bx + bw * 0.6, by - bw * 0.7), (bx, by - bw * 1.15)], fill=(180, 60, 70))
        d.rectangle([bx - bw * 0.18, by - bw * 0.38, bx + bw * 0.18, by], fill=(255, 255, 255))
        d.line([bx - bw * 0.18, by - bw * 0.38, bx + bw * 0.18, by], fill=(225, 80, 80), width=8)
        d.line([bx + bw * 0.18, by - bw * 0.38, bx - bw * 0.18, by], fill=(225, 80, 80), width=8)
        fy = H * (ground - 0.03)
        for x in range(0, int(W * 0.65), int(H * 0.06)):
            d.rectangle([x, fy - H * 0.08, x + H * 0.02, fy], fill=(255, 250, 240))
        for yy in (fy - H * 0.065, fy - H * 0.03):
            d.rectangle([0, yy, W * 0.65, yy + H * 0.012], fill=(255, 250, 240))
        return im, fg, st
    if kind == "mz_savanna":
        im = art.grad(W, H, (255, 215, 160), (255, 240, 210))
        d = ImageDraw.Draw(im)
        d.ellipse([W * 0.7, H * 0.08, W * 0.7 + H * 0.2, H * 0.28], fill=(255, 190, 90))
        art.hills(d, W, H, ground - 0.12, 0.05, (225, 205, 120), 2)
        art.hills(d, W, H, ground - 0.03, 0.04, (200, 190, 95), 3)
        tx = W * 0.12
        ty = H * (ground - 0.1)
        d.rectangle([tx - 12, ty - H * 0.25, tx + 12, ty], fill=(140, 100, 70))
        d.ellipse([tx - W * 0.1, ty - H * 0.34, tx + W * 0.1, ty - H * 0.22], fill=(120, 170, 80))
        return im, None, []
    if kind == "mz_kitchen":
        im = art.grad(W, H, (255, 240, 220), (255, 248, 236))
        d = ImageDraw.Draw(im)
        for x in range(0, W, int(H * 0.06)):  # soft striped wallpaper
            d.rectangle([x, 0, x + H * 0.03, H], fill=(255, 233, 214))
        cy = H * (ground - 0.22)
        # window with curtains in the middle
        wx0, wx1 = W * 0.38, W * 0.62
        d.rounded_rectangle([wx0, H * 0.1, wx1, cy - H * 0.04], 24, fill=(170, 220, 255), outline=(255, 255, 255), width=14)
        art.cloud(d, wx0 + 30, H * 0.22, (wx1 - wx0) / 600, (255, 255, 255))
        d.line([(wx0 + wx1) / 2, H * 0.1, (wx0 + wx1) / 2, cy - H * 0.04], fill=(255, 255, 255), width=10)
        for k in range(8):
            x = wx0 - 60 + k * ((wx1 - wx0) + 120) / 7
            d.polygon([(x - 26, H * 0.07), (x + 26, H * 0.07), (x, H * 0.07 + 34)], fill=[(255, 150, 180), (255, 210, 120)][k % 2])
        # upper cabinets
        for x0 in (W * 0.03, W * 0.17, W * 0.68, W * 0.82):
            d.rounded_rectangle([x0, H * 0.06, x0 + W * 0.13, H * 0.3], 14, fill=(150, 210, 190), outline=(120, 185, 165), width=5)
            d.ellipse([x0 + W * 0.11 - 8, H * 0.18 - 8, x0 + W * 0.11 + 8, H * 0.18 + 8], fill=(255, 215, 120))
        # counter + lower cabinets
        d.rectangle([0, cy, W, H], fill=(150, 210, 190))
        d.rectangle([0, cy - H * 0.03, W, cy + H * 0.01], fill=(250, 245, 240))
        for k in range(0, W, int(W * 0.12)):
            d.rounded_rectangle([k + 10, cy + H * 0.04, k + W * 0.12 - 10, H * (ground - 0.07)], 14, outline=(120, 185, 165), width=5)
            d.ellipse([k + W * 0.06 - 8, cy + H * 0.07 - 8, k + W * 0.06 + 8, cy + H * 0.07 + 8], fill=(255, 215, 120))
        # fruit bowl + plant on the counter
        bx = W * 0.14
        for (dx, col) in ((-40, (235, 60, 70)), (0, (255, 160, 40)), (40, (255, 215, 70)), (-18, (120, 200, 90)), (22, (235, 60, 70))):
            d.ellipse([bx + dx - 30, cy - H * 0.085 - (20 if dx in (-18, 22) else 0), bx + dx + 30, cy - H * 0.085 + 55 - (20 if dx in (-18, 22) else 0)], fill=col)
        d.chord([bx - 90, cy - H * 0.11, bx + 90, cy - H * 0.01], 0, 180, fill=(120, 170, 240))
        px = W * 0.86
        d.polygon([(px - 40, cy - H * 0.03), (px + 40, cy - H * 0.03), (px + 30, cy - H * 0.1), (px - 30, cy - H * 0.1)], fill=(240, 140, 110))
        for a in (-1, 0, 1):
            d.ellipse([px + a * 34 - 22, cy - H * 0.2, px + a * 34 + 22, cy - H * 0.09], fill=(110, 195, 110))
        fy = H * (ground - 0.06)
        d.rectangle([0, fy, W, H], fill=(240, 205, 160))
        for k in range(0, W, int(H * 0.14)):
            d.line([k, fy, k - H * 0.08, H], fill=(225, 188, 142), width=4)
        return im, None, []
    return _prev_bg(kind, W, H)


art.background = background
