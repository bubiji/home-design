# -*- coding: utf-8 -*-
"""画墙打印稿：把 F2 哈默修伊、F5 三棵树排成整页 A4（图已按实际尺寸放好，打印时缩放选 100%），
另出一张试印条（暗部三档 + 灰阶）。原图取自 ../名画库，输出到 06_打印稿/，全部转 sRGB。"""
import io, pathlib
import numpy as np
from PIL import Image, ImageCms, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
BASE = pathlib.Path(__file__).resolve().parents[2]          # 客厅设计/
LIB = BASE.parent/"名画库"
OUT = BASE/"06_打印稿"; OUT.mkdir(exist_ok=True)
HAM = LIB/"哈默修伊_Vilhelm.Hammershøi_1864-1916/油画/1903_背影女子的室内/原图.jpg"
TT = LIB/"伦勃朗_Rembrandt_1606-1669/版画/1643_三棵树/原图.jpg"
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
A4 = (21.0, 29.7)
MARGIN = 0.35        # 打印机有边模式四边 3 mm（IPP 自报），留 0.5 mm 余量
PW, PH = A4[0] - 2*MARGIN, A4[1] - 2*MARGIN      # 竖放可印 20.3 × 29.0

# 三棵树：扫描件里纸张边界（全分辨率像素），LOC 记载纸宽约 28 cm → 约 805 ppi
TT_SHEET = (240, 252, 9120, 6588)
TT_SHEET_W_CM = 28.0
LIFTS = (("A", 0), ("B", 8), ("C", 16))          # 哈默修伊暗部三档：把文件里的纯黑抬到 L* 0 / 8 / 16

def px(cm, ppi): return round(cm/2.54*ppi)

def to_srgb(im):
    icc = im.info.get("icc_profile")
    if not icc: return im.convert("RGB")
    return ImageCms.profileToProfile(im.convert("RGB"), ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode="RGB")

M = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]], np.float32)
WHITE = M.sum(1)

def lift(im, lb):
    """L* 线性抬黑位：L' = lb + L·(100−lb)/100，a/b 不动。lb=0 原样返回。"""
    if not lb: return im
    c = np.asarray(im, np.float32)/255
    lin = np.where(c <= 0.04045, c/12.92, ((c + 0.055)/1.055)**2.4)
    f = lin @ M.T / WHITE
    f = np.where(f > 0.008856, np.cbrt(f), 7.787*f + 16/116)
    L, a, b = 116*f[..., 1] - 16, 500*(f[..., 0] - f[..., 1]), 200*(f[..., 1] - f[..., 2])
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

# ---------- F2 哈默修伊：竖放，图宽占满可印宽 ----------
ham = to_srgb(Image.open(HAM))
HW = PW; HH = HW*ham.height/ham.width
ham_p = ham.resize((px(HW, 360), px(HH, 360)), Image.LANCZOS)
for tag, lb in LIFTS:
    pg = page(360)
    pg.paste(lift(ham_p, lb), ((pg.width - ham_p.width)//2, (pg.height - ham_p.height)//2))
    save(pg, f"F2_哈默修伊_A4竖_{tag}_黑位{lb}", 360)
print(f"F2 画面 {HW:.1f}×{HH:.2f} cm，原作 50.5×60.5 的 {HW/50.5*100:.0f}%，源图在此尺寸 {ham.width/HW*2.54:.0f} ppi")

# ---------- F5 三棵树：横放，按原作 1:1 ----------
tt = Image.open(TT)
x1, y1, x2, y2 = TT_SHEET
src_ppi = (x2 - x1)/(TT_SHEET_W_CM/2.54)
cw, ch = PH, PW                                   # 横放可印 29.0 × 20.3
cx, cy = (x1 + x2)/2, (y1 + y2)/2
box = tuple(round(v) for v in (cx - cw/2.54*src_ppi/2, cy - ch/2.54*src_ppi/2, cx + cw/2.54*src_ppi/2, cy + ch/2.54*src_ppi/2))
assert box[0] >= 0 and box[1] >= 0 and box[2] <= tt.width and box[3] <= tt.height, box
tt_c = tt.crop(box); tt_c.info["icc_profile"] = tt.info.get("icc_profile")
tt_p = to_srgb(tt_c).resize((px(cw, 720), px(ch, 720)), Image.LANCZOS)
pg = page(720, landscape=True)
pg.paste(tt_p, ((pg.width - tt_p.width)//2, (pg.height - tt_p.height)//2))
save(pg, "F5_三棵树_A4横_原大", 720)
print(f"F5 源图约 {src_ppi:.0f} ppi；纸张 {TT_SHEET_W_CM:.1f}×{(y2-y1)/src_ppi*2.54:.2f} cm 按 1:1；印出范围 {cw:.1f}×{ch:.1f} cm")

# ---------- 试印条：一张 A4 竖放 ----------
P = 360
pg = page(P); d = ImageDraw.Draw(pg)
f_s, f_m = ImageFont.truetype(FONT, px(.32, P)), ImageFont.truetype(FONT, px(.42, P))
ox, oy = px(MARGIN, P), px(MARGIN, P)
d.text((ox, oy), "试印条 · Velvet Fine Art · 缩放 100% · 画质 高", font=f_m, fill="black")
y = oy + px(.8, P)
# 哈默修伊三档：取裙子 + 桌角一条，与成品同比例
sw, gap = px(6.6, P), px(.25, P)
bx = round(ham_p.width*.42); strip = ham_p.crop((bx, round(ham_p.height*.45), bx + sw, ham_p.height))
for i, (tag, lb) in enumerate(LIFTS):
    x = ox + i*(sw + gap)
    pg.paste(lift(strip, lb), (x, y))
    d.text((x, y + strip.height + px(.1, P)), f"{tag}  黑位 L*{lb}" + ("（原样）" if not lb else ""), font=f_s, fill="black")
y += strip.height + px(.9, P)
# 三棵树：1:1 取中右一条
tt360 = tt_p.resize((px(cw, P), px(ch, P)), Image.LANCZOS)
tw, th = px(PW, P), px(8.2, P)
tx, ty = round(tt360.width*.26), round(tt360.height*.40)
pg.paste(tt360.crop((tx, ty, tx + tw, ty + th)), (ox, y))
d.text((ox, y + th + px(.1, P)), "三棵树  原大 1:1（看线条是否糊、纸色是否偏红或偏绿）", font=f_s, fill="black")
y += th + px(.9, P)
# 暗部灰阶：看从哪一格开始分得开
steps = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 40]
bw, bh = px(PW/len(steps), P), px(1.6, P)
for i, L in enumerate(steps):
    z = np.zeros((bh, bw), np.float32)
    pg.paste(lab_to_img(z + L, z, z), (ox + i*bw, y))
    d.text((ox + i*bw + px(.1, P), y + bh + px(.08, P)), str(L), font=f_s, fill="black")
d.text((ox, y + bh + px(.6, P)), "灰阶 L*：干透后在挂画位置的光线下看，从左数第几格开始能和左邻分开", font=f_s, fill="black")
assert y + bh + px(1.2, P) < pg.height - oy
save(pg, "试印条_A4竖", P)
