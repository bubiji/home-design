# -*- coding: utf-8 -*-
"""画墙打印稿 v6(2026-10-27):给五幅加「画框感」的版式,三种候选,全部从名画库原图重新生成。
每幅四边都留至少 BORDER 的边(画面按此略缩,四边才匀),边里再画线、填色或加题签:
  museum  博物馆式:纸白留边 + 画外 3 mm 处一条 0.4 mm 石墨色细线 + 左下角小字题签
  dark    深色卡纸:炭黑填满留边 + 画外 2 mm 处一条暖灰细线,像深色卡纸配黑框
  cream   暖卡纸双线:米白填满留边 + 双线(近画一条深、外一条赭)+ 题签,法式卡纸
用法:python gen_print_v6_frame.py [museum|dark|cream|all] [--full]
  默认只出预览档(每幅一档),--full 出全部黑位档。输出 06_打印稿/待印五幅_画框版_20261027/<版式>/,不碰旧稿。
  python gen_print_v6_frame.py final  → 定稿(2026-10-27 用户定):一律不印题签;哈默修伊、海上渔夫用 dark 且黑底铺满整页
  (含 3.5 mm 打印边,若走无边距就能出血到纸边),其余三幅 museum;全部黑位档;输出 待印五幅_定稿_20261027/。
"""
import io, pathlib, sys
import numpy as np
from PIL import Image, ImageCms, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
BASE = pathlib.Path(__file__).resolve().parents[2]          # 客厅设计/
LIB = BASE.parent/"名画库"
OUTROOT = BASE/"06_打印稿"/"待印五幅_画框版_20261027"
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
A4 = (21.0, 29.7)
MARGIN = 0.35
PW, PH = A4[0] - 2*MARGIN, A4[1] - 2*MARGIN      # 竖放可印 20.3 × 29.0
BORDER = 0.9                                      # 画四边至少留这么宽(cm)
LIFTS = (("A", 0), ("B", 8), ("C", 16))
P = 360

STYLES = {
    "museum": dict(bg="white", line=((0.3, 0.04, (70, 70, 72)),), caption=(60, 60, 62)),
    "dark": dict(bg=(32, 32, 34), line=((0.2, 0.06, (168, 160, 150)),), caption=None),
    "cream": dict(bg=(236, 230, 218), line=((0.3, 0.04, (70, 62, 55)), (0.5, 0.03, (165, 125, 70))), caption=(80, 72, 64)),
}

def px(cm, ppi=P): return round(cm/2.54*ppi)

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

def fit(w, h, landscape):
    cw, ch = (PH, PW) if landscape else (PW, PH)
    cw, ch = cw - 2*BORDER, ch - 2*BORDER
    H = ch; W = H*w/h
    if W > cw: W = cw; H = W*h/w
    return W, H

def compose(tp, landscape, style, caption, bleed=False):
    st = STYLES[style]
    w, h = (A4[1], A4[0]) if landscape else A4
    pg = Image.new("RGB", (px(w), px(h)), st["bg"] if bleed else "white")
    m = px(MARGIN)
    d = ImageDraw.Draw(pg)
    d.rectangle((m, m, pg.width - m - 1, pg.height - m - 1), fill=st["bg"])
    x0, y0 = (pg.width - tp.width)//2, (pg.height - tp.height)//2
    pg.paste(tp, (x0, y0))
    for gap, wid, col in st["line"]:
        g, lw = px(gap), max(1, px(wid))
        d.rectangle((x0 - g, y0 - g, x0 + tp.width + g - 1, y0 + tp.height + g - 1), outline=col, width=lw)
    if st["caption"] and caption:
        f = ImageFont.truetype(FONT, px(0.26))
        gap_last = px(st["line"][-1][0])
        d.text((x0, y0 + tp.height + gap_last + px(0.25)), caption, font=f, fill=st["caption"])
    return pg

def save(im, out, name):
    out.mkdir(parents=True, exist_ok=True)
    im.save(out/f"{name}.jpg", quality=95, subsampling=0, dpi=(P, P), icc_profile=SRGB.tobytes())
    im.save(out/f"{name}.pdf", "PDF", resolution=float(P), quality=95)
    print("wrote", out.name, name)

# (输出名, 原图, 原作 w×h cm, 横放?, 预览档, 题签)
WORKS = [
    ("F1_米勒春_A4横", LIB/"米勒_Jean-François.Millet_1814-1875/油画/1868_春/原图.jpg", (111, 86), True, "A",
     "Jean-François Millet · Le Printemps · 1868–73 · Musée d'Orsay"),
    ("F2_哈默修伊_A4竖", LIB/"哈默修伊_Vilhelm.Hammershøi_1864-1916/油画/1903_背影女子的室内/原图.jpg", (50.5, 60.5), False, "B",
     "Vilhelm Hammershøi · Interior with Young Woman from Behind · 1903–04 · Randers Kunstmuseum"),
    ("透纳_海上渔夫_A4横", LIB/"透纳_J.M.W.Turner_1775-1851/油画/1796_海上渔夫/原图.jpg", (122.2, 91.4), True, "B",
     "J. M. W. Turner · Fishermen at Sea · 1796 · Tate"),
    ("广重_猿若町夜景_A4竖", LIB/"歌川广重_Utagawa.Hiroshige_1797-1858/版画/1856_名所江户百景·猿若町夜景/原图.jpg", (23.5, 36.2), False, "A",
     "歌川広重 · 名所江戸百景 猿わか町よるの景 · 1856"),
]
TT = LIB/"伦勃朗_Rembrandt_1606-1669/版画/1643_三棵树/原图.jpg"
TT_SHEET, TT_SHEET_W_CM = (240, 252, 9120, 6588), 28.0
TT_CAPTION = "Rembrandt · The Three Trees · 1643 · etching, Library of Congress"

def three_trees():
    """三棵树:纸边内 1:1,裁到留边后的可印区(比 v1 的满版四边各少 BORDER)。"""
    tt = Image.open(TT)
    x1, y1, x2, y2 = TT_SHEET
    src_ppi = (x2 - x1)/(TT_SHEET_W_CM/2.54)
    cw, ch = PH - 2*BORDER, PW - 2*BORDER
    cx, cy = (x1 + x2)/2, (y1 + y2)/2
    box = tuple(round(v) for v in (cx - cw/2.54*src_ppi/2, cy - ch/2.54*src_ppi/2, cx + cw/2.54*src_ppi/2, cy + ch/2.54*src_ppi/2))
    c = tt.crop(box); c.info["icc_profile"] = tt.info.get("icc_profile")
    return to_srgb(c).resize((px(cw), px(ch)), Image.LANCZOS)

FINAL = {"F1_米勒春_A4横": "museum", "F2_哈默修伊_A4竖": "dark", "透纳_海上渔夫_A4横": "dark",
         "广重_猿若町夜景_A4竖": "museum", "F5_三棵树_A4横": "museum"}

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args and args[0] == "final":
        out = BASE/"06_打印稿"/"待印五幅_定稿_20261027"
        for name, path, orig, land, _, _ in WORKS:
            src = to_srgb(Image.open(path))
            W, H = fit(src.width, src.height, land)
            tp = src.resize((px(W), px(H)), Image.LANCZOS)
            st = FINAL[name]
            print(f"{name}: {st},画面 {W:.1f}×{H:.1f} cm,原作的 {W/orig[0]*100:.0f}%")
            for tag, lb in (LIFTS if st == "dark" else LIFTS[:1]):
                save(compose(lift(tp, lb), land, st, None, bleed=(st == "dark")), out, f"{name}_{st}_{tag}_黑位{lb}")
        save(compose(three_trees(), True, "museum", None), out, "F5_三棵树_A4横_museum_原大")
        return
    styles = list(STYLES) if not args or args[0] == "all" else [args[0]]
    full = "--full" in sys.argv
    tts = three_trees()
    for name, path, orig, land, pre, cap in WORKS:
        src = to_srgb(Image.open(path))
        W, H = fit(src.width, src.height, land)
        tp = src.resize((px(W), px(H)), Image.LANCZOS)
        print(f"{name}: 画面 {W:.1f}×{H:.1f} cm,原作的 {W/orig[0]*100:.0f}%")
        for style in styles:
            for tag, lb in (LIFTS if full else [l for l in LIFTS if l[0] == pre]):
                save(compose(lift(tp, lb), land, style, cap), OUTROOT/style, f"{name}_{tag}_黑位{lb}")
    for style in styles:
        save(compose(tts, True, style, TT_CAPTION), OUTROOT/style, "F5_三棵树_A4横_原大")
    print(f"三棵树 1:1,画面 {PH-2*BORDER:.1f}×{PW-2*BORDER:.1f} cm")

if __name__ == "__main__":
    main()
