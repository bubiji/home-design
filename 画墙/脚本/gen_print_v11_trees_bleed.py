# -*- coding: utf-8 -*-
"""三棵树 满版出血稿(2026-10-28):给无边距打印用。图像区(LOC 扫描件 28.0×20.0 cm)等比放大到铺满整张 A4
(29.7×21.0,约 106%),高度多出的部分上下各裁一点;页面上没有任何白边、文字、裁切线。
打印机无边距模式自己还会再放大一点点出血。输出 待印_两边裁切_20261027/F5_三棵树_A4横_满版出血.jpg(sRGB,未调色),
之后用 tone_white.py 85.7 1.3 10.9 得到 Met 米色调子版。"""
from PIL import Image
import gen_print_v6_frame as g
Image.MAX_IMAGE_PIXELS = None
tt = Image.open(g.TT); x1, y1, x2, y2 = g.TT_SHEET
w, h = x2 - x1, y2 - y1
PW_, PH_ = g.A4[1], g.A4[0]                       # 横放整页 29.7 × 21.0
need_h = round(w * PH_ / PW_)
cy = (y1 + y2) / 2
box = (x1, round(cy - need_h/2), x2, round(cy + need_h/2))
c = tt.crop(box); c.info["icc_profile"] = tt.info.get("icc_profile")
tp = g.to_srgb(c).resize((g.px(PW_), g.px(PH_)), Image.LANCZOS)
g.save(tp, g.BASE/"06_打印稿"/"待印_两边裁切_20261027", "F5_三棵树_A4横_满版出血")
print(f"放大 {PW_/g.TT_SHEET_W_CM*100:.1f}%,上下各裁 {(h-need_h)/2/805*2.54:.2f} cm,页面 {tp.width}×{tp.height} px = 29.7×21.0")
