# -*- coding: utf-8 -*-
"""画墙打印稿 v5(2026-10-27):待印五幅从名画库原图重新生成,图外的可印区不再留白,而是用画面边缘的颜色填满
(每幅各取自己四边一圈像素的中位色),只剩打印机有边模式强制的 3.5 mm 白边。图的尺寸、位置、暗部三档与
v1/v3/v4 完全一样,只是把「白底」换成「画边色底」;三棵树本来就满版,没有填边。
输出到 06_打印稿/待印五幅_填边_20261027/,不碰旧稿。
"""
import io, pathlib
import numpy as np
from PIL import Image, ImageCms

Image.MAX_IMAGE_PIXELS = None
BASE = pathlib.Path(__file__).resolve().parents[2]          # 客厅设计/
LIB = BASE.parent/"名画库"
OUT = BASE/"06_打印稿"/"待印五幅_填边_20261027"; OUT.mkdir(parents=True, exist_ok=True)
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
A4 = (21.0, 29.7)
MARGIN = 0.35
PW, PH = A4[0] - 2*MARGIN, A4[1] - 2*MARGIN      # 竖放可印 20.3 × 29.0
LIFTS = (("A", 0), ("B", 8), ("C", 16))
P = 360
EDGE = 0.02                                       # 取边缘色的带宽:画面短边的 2%

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

def lab_to_img(L, a, b):
    fy = (L + 16)/116; f = np.stack([fy + a/500, fy, fy - b/200], -1)
    xyz = np.where(f > 0.206893, f**3, (f - 16/116)/7.787)*WHITE
    lin = np.clip(xyz @ np.linalg.inv(M).T, 0, 1)
    c = np.where(lin <= 0.0031308, lin*12.92, 1.055*lin**(1/2.4) - 0.055)
    return Image.fromarray((np.clip(c, 0, 1)*255 + .5).astype(np.uint8))

def lift(im, lb):
    if not lb: return im
    L, a, b = to_lab(im)
    return lab_to_img(lb + L*(100 - lb)/100, a, b)

def edge_color(im):
    """四边一圈像素的中位色(sRGB)。"""
    a = np.asarray(im); k = max(2, round(min(a.shape[:2])*EDGE))
    band = np.concatenate([a[:k].reshape(-1, 3), a[-k:].reshape(-1, 3), a[:, :k].reshape(-1, 3), a[:, -k:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(band, 0))

def page(landscape, color):
    w, h = (A4[1], A4[0]) if landscape else A4
    pg = Image.new("RGB", (px(w, P), px(h, P)), "white")
    m = px(MARGIN, P)
    pg.paste(Image.new("RGB", (pg.width - 2*m, pg.height - 2*m), color), (m, m))
    return pg

def save(im, name):
    im.save(OUT/f"{name}.jpg", quality=95, subsampling=0, dpi=(P, P), icc_profile=SRGB.tobytes())
    im.save(OUT/f"{name}.pdf", "PDF", resolution=float(P), quality=95)
    print("wrote", name, im.size)

def fit(src, landscape):
    cw, ch = (PH, PW) if landscape else (PW, PH)
    H = ch; W = H*src.width/src.height
    if W > cw: W = cw; H = W*src.height/src.width
    return W, H

def emit(name, tp, landscape, lifts, orig):
    col = edge_color(tp)
    L, _, _ = to_lab(tp); dark = float((L < 16).mean()*100)
    for tag, lb in lifts:
        pg = page(landscape, col)
        pg.paste(lift(tp, lb), ((pg.width - tp.width)//2, (pg.height - tp.height)//2))
        save(pg, f"{name}_{tag}_黑位{lb}")
    W, H = tp.width/P*2.54, tp.height/P*2.54
    print(f"  画面 {W:.1f}×{H:.1f} cm,原作的 {W/orig[0]*100:.0f}%;填边色 RGB{col};L*<16 暗部 {dark:.0f}%")

# ---------- 按高/宽占满可印区的四幅 ----------
WORKS = [  # (输出名, 原图, 原作 w×h cm, 横放?, 档位)
    ("F1_米勒春_A4横", LIB/"米勒_Jean-François.Millet_1814-1875/油画/1868_春/原图.jpg", (111, 86), True, LIFTS[:1]),
    ("F2_哈默修伊_A4竖", LIB/"哈默修伊_Vilhelm.Hammershøi_1864-1916/油画/1903_背影女子的室内/原图.jpg", (50.5, 60.5), False, LIFTS),
    ("透纳_海上渔夫_A4横", LIB/"透纳_J.M.W.Turner_1775-1851/油画/1796_海上渔夫/原图.jpg", (122.2, 91.4), True, LIFTS),
    ("广重_猿若町夜景_A4竖", LIB/"歌川广重_Utagawa.Hiroshige_1797-1858/版画/1856_名所江户百景·猿若町夜景/原图.jpg", (23.5, 36.2), False, LIFTS[:1]),
]
for name, path, orig, land, lifts in WORKS:
    src = to_srgb(Image.open(path))
    W, H = fit(src, land)
    tp = src.resize((px(W, P), px(H, P)), Image.LANCZOS)
    print(name)
    emit(name, tp, land, lifts, orig)

# ---------- F5 三棵树:与 v1 相同的 1:1 裁切,本来就满版 ----------
TT = LIB/"伦勃朗_Rembrandt_1606-1669/版画/1643_三棵树/原图.jpg"
TT_SHEET, TT_SHEET_W_CM = (240, 252, 9120, 6588), 28.0
tt = Image.open(TT)
x1, y1, x2, y2 = TT_SHEET
src_ppi = (x2 - x1)/(TT_SHEET_W_CM/2.54)
cw, ch = PH, PW
cx, cy = (x1 + x2)/2, (y1 + y2)/2
box = tuple(round(v) for v in (cx - cw/2.54*src_ppi/2, cy - ch/2.54*src_ppi/2, cx + cw/2.54*src_ppi/2, cy + ch/2.54*src_ppi/2))
tt_c = tt.crop(box); tt_c.info["icc_profile"] = tt.info.get("icc_profile")
tt_p = to_srgb(tt_c).resize((px(cw, P), px(ch, P)), Image.LANCZOS)
pg = page(True, "white")
pg.paste(tt_p, ((pg.width - tt_p.width)//2, (pg.height - tt_p.height)//2))
save(pg, "F5_三棵树_A4横_原大")
print("  三棵树满版 1:1,无填边")
