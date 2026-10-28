# -*- coding: utf-8 -*-
"""画墙打印稿 v4：用户 2026-10-27 选定替换 F3/F4 的两幅（具体进哪个框未定，文件名不带框号）：
  · 透纳《海上渔夫》1796（油画，原作 91.4×122.2 cm）—— A4 横放，按高占满；夜景很暗，出暗部三档 + 专用试印条
  · 广重《名所江户百景·猿若町夜景》1856（大判锦绘，约 36.2×23.5 cm）—— A4 竖放，连纸边整张按高占满（原作放不下 1:1）
与 gen_print_v1.py / v2_turner 同一套规则（有边 3.5 mm、sRGB、360 ppi、打印缩放 100%），不改旧脚本；
原图取自 ../名画库，输出到 06_打印稿/。暗部占比低于 2% 的只出 A 档。
"""
import io, pathlib
import numpy as np
from PIL import Image, ImageCms, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
BASE = pathlib.Path(__file__).resolve().parents[2]          # 客厅设计/
LIB = BASE.parent/"名画库"
OUT = BASE/"06_打印稿"; OUT.mkdir(exist_ok=True)
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
A4 = (21.0, 29.7)
MARGIN = 0.35
PW, PH = A4[0] - 2*MARGIN, A4[1] - 2*MARGIN      # 竖放可印 20.3 × 29.0
LIFTS = (("A", 0), ("B", 8), ("C", 16))
P = 360

def px(cm, ppi): return round(cm/2.54*ppi)

def to_srgb(im):
    icc = im.info.get("icc_profile")
    if not icc: return im.convert("RGB")
    return ImageCms.profileToProfile(im.convert("RGB"), ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode="RGB")

M = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]], np.float32)
WHITE = M.sum(1)

def to_lab(im):
    c = np.asarray(im, np.float32)/255
    lin = np.where(c <= 0.04045, c/12.92, ((c + 0.055)/1.055)**2.4)
    f = lin @ M.T / WHITE
    f = np.where(f > 0.008856, np.cbrt(f), 7.787*f + 16/116)
    return 116*f[..., 1] - 16, 500*(f[..., 0] - f[..., 1]), 200*(f[..., 1] - f[..., 2])

def lift(im, lb):
    """L* 线性抬黑位：L' = lb + L·(100−lb)/100，a/b 不动。"""
    if not lb: return im
    L, a, b = to_lab(im)
    return lab_to_img(lb + L*(100 - lb)/100, a, b)

def lab_to_img(L, a, b):
    fy = (L + 16)/116; f = np.stack([fy + a/500, fy, fy - b/200], -1)
    xyz = np.where(f > 0.206893, f**3, (f - 16/116)/7.787)*WHITE
    lin = np.clip(xyz @ np.linalg.inv(M).T, 0, 1)
    c = np.where(lin <= 0.0031308, lin*12.92, 1.055*lin**(1/2.4) - 0.055)
    return Image.fromarray((np.clip(c, 0, 1)*255 + .5).astype(np.uint8))

def page(ppi, landscape=False):
    w, h = (A4[1], A4[0]) if landscape else A4
    return Image.new("RGB", (px(w, ppi), px(h, ppi)), "white")

def save(im, name, ppi):
    im.save(OUT/f"{name}.jpg", quality=95, subsampling=0, dpi=(ppi, ppi), icc_profile=SRGB.tobytes())
    im.save(OUT/f"{name}.pdf", "PDF", resolution=float(ppi), quality=95)
    print("wrote", name, im.size, f"{ppi} ppi")


WORKS = [  # (输出名, 原图, 原作 w×h cm, 横放?)
    ("透纳_海上渔夫_A4横", LIB/"透纳_J.M.W.Turner_1775-1851/油画/1796_海上渔夫/原图.jpg", (122.2, 91.4), True),
    ("广重_猿若町夜景_A4竖", LIB/"歌川广重_Utagawa.Hiroshige_1797-1858/版画/1856_名所江户百景·猿若町夜景/原图.jpg", (23.5, 36.2), False),
]

def fit(src, landscape):
    cw, ch = (PH, PW) if landscape else (PW, PH)
    H = ch; W = H*src.width/src.height
    if W > cw: W = cw; H = W*src.height/src.width
    return W, H

fisher = None
for name, path, orig, land in WORKS:
    src = to_srgb(Image.open(path))
    W, H = fit(src, land)
    tp = src.resize((px(W, P), px(H, P)), Image.LANCZOS)
    L, _, _ = to_lab(tp)
    dark = float((L < 16).mean()*100)
    for tag, lb in (LIFTS if dark >= 2 else LIFTS[:1]):
        pg = page(P, landscape=land)
        pg.paste(lift(tp, lb), ((pg.width - tp.width)//2, (pg.height - tp.height)//2))
        save(pg, f"{name}_{tag}_黑位{lb}", P)
    print(f"{name}: 画面 {W:.1f}×{H:.1f} cm，原作的 {W/orig[0]*100:.0f}%；源图在此尺寸 {src.width/W*2.54:.0f} ppi；L*<16 的暗部占 {dark:.0f}%")
    if name.startswith("透纳"): fisher = tp

# ---------- 试印条（海上渔夫）：竖放 A4，暗部三档（渔船与浪）+ 亮部（月光云）+ 灰阶 ----------
tp = fisher
pg = page(P); d = ImageDraw.Draw(pg)
f_s, f_m = ImageFont.truetype(FONT, px(.32, P)), ImageFont.truetype(FONT, px(.42, P))
ox, oy = px(MARGIN, P), px(MARGIN, P)
d.text((ox, oy), "试印条 · 透纳 海上渔夫 · 缩放 100% · 画质 高", font=f_m, fill="black")
y = oy + px(.8, P)
sw, gap = px(6.6, P), px(.25, P)
bx, by = round(tp.width*.24), round(tp.height*.55)          # 左侧渔船、船灯与下方暗浪
strip = tp.crop((bx, by, bx + sw, min(tp.height, by + px(8.5, P))))
for i, (tag, lb) in enumerate(LIFTS):
    x = ox + i*(sw + gap)
    pg.paste(lift(strip, lb), (x, y))
    d.text((x, y + strip.height + px(.1, P)), f"{tag}  黑位 L*{lb}" + ("（原样）" if not lb else ""), font=f_s, fill="black")
y += strip.height + px(.9, P)
tw, th = px(PW, P), px(6.0, P)
tx, ty = round(tp.width*.10), round(tp.height*.08)          # 月亮与被照亮的云
pg.paste(tp.crop((tx, ty, min(tp.width, tx + tw), ty + th)), (ox, y))
d.text((ox, y + th + px(.1, P)), "亮部原样（看月光与云边的层次是否还在）", font=f_s, fill="black")
y += th + px(.9, P)
steps = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 40]
bw, bh = px(PW/len(steps), P), px(1.6, P)
for i, Lv in enumerate(steps):
    z = np.zeros((bh, bw), np.float32)
    pg.paste(lab_to_img(z + Lv, z, z), (ox + i*bw, y))
    d.text((ox + i*bw + px(.1, P), y + bh + px(.08, P)), str(Lv), font=f_s, fill="black")
d.text((ox, y + bh + px(.6, P)), "灰阶 L*：干透后在挂画位置的光线下看，从左数第几格开始能和左邻分开", font=f_s, fill="black")
assert y + bh + px(1.2, P) < pg.height - oy
save(pg, "试印条_透纳海上渔夫_A4竖", P)
