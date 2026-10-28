# -*- coding: utf-8 -*-
"""三棵树 无边距安全版(2026-10-28,用户定的两条规矩):
  ① 作品本身的纸边一毫米都不裁:LOC 扫描件的整个图像区(含作品自己的纸边)原样保留;
  ② A4 尽量不留白:走无边距,作品放在页面中央、四周留 SAFE 的出血余量,余量用作品自己的纸色填,
     打印机出血放大时吃掉的是这圈纸色,不是作品。
全部从 LOC 原扫描件一次生成(裁→转 sRGB→缩放→Met 米色调子→合成页面→存一次 JPG),不在任何中间稿上二次加工。
输出 待印_两边裁切_20261027/F5_三棵树_A4横_无边距安全_Met调子.jpg。"""
import numpy as np
from PIL import Image
import gen_print_v6_frame as g
Image.MAX_IMAGE_PIXELS = None
SAFE = 0.3                       # 四周出血余量 cm(打印机无边距约放大 2–3 mm/边)
T_L, T_A, T_B = 85.7, 1.3, 10.9  # Met 藏本纸面
tt = Image.open(g.TT); x1, y1, x2, y2 = g.TT_SHEET
c = tt.crop((x1, y1, x2, y2)); c.info["icc_profile"] = tt.info.get("icc_profile")
src = g.to_srgb(c)
PW_, PH_ = g.A4[1] - 2*SAFE, g.A4[0] - 2*SAFE            # 可放区 29.1 × 20.4
H = PH_; W = H*src.width/src.height
if W > PW_: W = PW_; H = W*src.height/src.width
tp = src.resize((g.px(W), g.px(H)), Image.LANCZOS)
# Met 调子(同 tone_white:只动纸面,墨线不动,比纸面更亮的扫描底不动)
L, a, b = g.to_lab(tp); m = L > 75
pL, pa, pb = np.median(L[m]), np.median(a[m]), np.median(b[m])
w = np.clip((L - 35)/40, 0, 1) * np.clip((pL + 8 - L)/8, 0, 1)
tp = g.lab_to_img(np.clip(L*T_L/pL, 0, 100), a + w*(T_A - pa), b + w*(T_B - pb))
# 页面底色 = 调子后的纸面中位色
L2, a2, b2 = g.to_lab(tp); m2 = L2 > 75
paper = tuple(int(v) for v in np.median(np.asarray(tp)[m2], 0))
pg = Image.new("RGB", (g.px(g.A4[1]), g.px(g.A4[0])), paper)
pg.paste(tp, ((pg.width - tp.width)//2, (pg.height - tp.height)//2))
g.save(pg, g.BASE/"06_打印稿"/"待印_两边裁切_20261027", "F5_三棵树_A4横_无边距安全_Met调子")
print(f"作品 {W:.1f}×{H:.1f} cm(图像区 28.0×20.0 的 {W/28.0*100:.0f}%),页面 29.7×21.0,四周纸色余量 左右 {(g.A4[1]-W)/2:.2f} / 上下 {(g.A4[0]-H)/2:.2f} cm,底色 RGB{paper}")
