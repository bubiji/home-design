# -*- coding: utf-8 -*-
"""画墙定稿·无边距安全版(2026-10-28,用户批准三棵树那版后推广到其余作品):
  · 作品整幅保留,一毫米不裁;等比放到 A4 减去四周 SAFE 出血余量的区域内,居中;
  · 页面底色 = 作品四边一圈像素的中位色(油画是画布边色,版画是纸色),无边距打印时被吃掉的是这圈底色;
  · 全部从名画库原图一次生成,存一次 JPG;不印裁切线、不印字。
用法:python gen_print_v13_safe_all.py            → 米勒、哈默修伊(A/B/C)、猿若町、海上渔夫(A/B/C)
输出 06_打印稿/定稿_无边距安全/。三棵树由 gen_print_v12_trees_safe.py 单独生成(含 Met 调子)。"""
import numpy as np
from PIL import Image
import gen_print_v6_frame as g
Image.MAX_IMAGE_PIXELS = None
SAFE = 0.3
OUT = g.BASE/"06_打印稿"/"定稿_无边距安全"
EDGE = 0.02

def edge_color(im):
    a = np.asarray(im); k = max(2, round(min(a.shape[:2])*EDGE))
    band = np.concatenate([a[:k].reshape(-1, 3), a[-k:].reshape(-1, 3), a[:, :k].reshape(-1, 3), a[:, -k:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(band, 0))

def make(name, path, landscape, lifts):
    src = g.to_srgb(Image.open(path))
    pw, ph = ((g.A4[1], g.A4[0]) if landscape else g.A4)
    aw, ah = pw - 2*SAFE, ph - 2*SAFE
    H = ah; W = H*src.width/src.height
    if W > aw: W = aw; H = W*src.height/src.width
    tp = src.resize((g.px(W), g.px(H)), Image.LANCZOS)
    col = edge_color(tp)
    for tag, lb in lifts:
        im = g.lift(tp, lb)
        pg = Image.new("RGB", (g.px(pw), g.px(ph)), col)
        pg.paste(im, ((pg.width - im.width)//2, (pg.height - im.height)//2))
        g.save(pg, OUT, f"{name}_无边距安全_{tag}_黑位{lb}")
    print(f"{name}: 作品 {W:.1f}×{H:.1f} cm,余量 左右 {(pw-W)/2:.2f} / 上下 {(ph-H)/2:.2f} cm,底色 RGB{col}")

WORKS = [
    ("F1_米勒春_A4横", g.WORKS[0][1], True, g.LIFTS[:1]),
    ("F2_哈默修伊_A4竖", g.WORKS[1][1], False, g.LIFTS),
    ("广重_猿若町夜景_A4竖", g.WORKS[3][1], False, g.LIFTS[:1]),
    ("透纳_海上渔夫_A4横", g.WORKS[2][1], True, g.LIFTS),
]
if __name__ == "__main__":
    for w in WORKS:
        make(*w)
