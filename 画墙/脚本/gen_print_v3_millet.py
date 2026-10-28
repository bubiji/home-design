# -*- coding: utf-8 -*-
"""画墙打印稿 v3：F1 米勒《春》1868–73，改用 A4 自印（原计划外送 A3），整页 A4 横放，暗部三档（黑位 L* 0 / 8 / 16）。
与 gen_print_v1.py / v2_turner 同一套规则（有边 3.5 mm、sRGB、360 ppi、打印缩放 100%），不改旧脚本；
原图取自 ../名画库，输出到 06_打印稿/。试印条沿用 试印条_A4竖（灰阶一样），不另出。

米勒原作 111×86 cm，A4 横放可印 29.0×20.3 → 画面 26.8×20.3 cm，约为原作 24%；源图 2536 px，此尺寸约 240 ppi。
实测 L*<16 的暗部占 0%，A 档（不抬黑位）即可，B/C 只作对照。
"""
import io, pathlib
import numpy as np
from PIL import Image, ImageCms, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
BASE = pathlib.Path(__file__).resolve().parents[2]          # 客厅设计/
LIB = BASE.parent/"名画库"
OUT = BASE/"06_打印稿"; OUT.mkdir(exist_ok=True)
SRC = LIB/"米勒_Jean-François.Millet_1814-1875/油画/1868_春/原图.jpg"
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
A4 = (21.0, 29.7)
MARGIN = 0.35
PW, PH = A4[0] - 2*MARGIN, A4[1] - 2*MARGIN      # 竖放可印 20.3 × 29.0
ORIG_CM = (111, 86)
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

# ---------- 米勒：横放，按高占满可印高 ----------
src = to_srgb(Image.open(SRC))
cw, ch = PH, PW                                   # 横放可印 29.0 × 20.3
H = ch; W = H*src.width/src.height
if W > cw: W = cw; H = W*src.height/src.width
tp = src.resize((px(W, P), px(H, P)), Image.LANCZOS)
L, _, _ = to_lab(tp)
dark = float((L < 16).mean()*100)
for tag, lb in LIFTS:
    pg = page(P, landscape=True)
    pg.paste(lift(tp, lb), ((pg.width - tp.width)//2, (pg.height - tp.height)//2))
    save(pg, f"F1_米勒春_A4横_{tag}_黑位{lb}", P)
print(f"画面 {W:.1f}×{H:.1f} cm，原作 {ORIG_CM[0]}×{ORIG_CM[1]} 的 {W/ORIG_CM[0]*100:.0f}%；源图在此尺寸 {src.width/W*2.54:.0f} ppi；L*<16 的暗部占 {dark:.0f}%")

