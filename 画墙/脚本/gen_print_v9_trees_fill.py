# -*- coding: utf-8 -*-
"""三棵树 放大版(2026-10-28):扫描件的图像区是 28.0×20.0 cm,v1 的 1:1 稿把它居中放进 29.0×20.3 的可印区,
左右各多出 0.5 cm 扫描底色(白)。这里把图像区等比放大到 29.0 宽(约 104%),高度多出的 0.4 cm 上下各裁 0.2,
画面铺满可印区,只剩 3.5 mm 打印边。输出 待印_两边裁切_20261027/F5_三棵树_A4横_放大104.jpg(sRGB)。"""
from PIL import Image
import gen_print_v6_frame as g, gen_print_v8_twoside as v8
Image.MAX_IMAGE_PIXELS = None
tt = Image.open(g.TT); x1, y1, x2, y2 = g.TT_SHEET
w, h = x2 - x1, y2 - y1
scale = g.PH / g.TT_SHEET_W_CM                     # 29.0/28.0
need_h = h * (g.PW / g.PH) * (w / h) / (w / h)     # 占位
need_h = round(w * g.PW / g.PH)                    # 目标比例 29.0:20.3 下需要的源高
cy = (y1 + y2) / 2
box = (x1, round(cy - need_h/2), x2, round(cy + need_h/2))
c = tt.crop(box); c.info["icc_profile"] = tt.info.get("icc_profile")
tp = g.to_srgb(c).resize((g.px(g.PH), g.px(g.PW)), Image.LANCZOS)
pg = v8.trim_page(tp, True)
g.save(pg, v8.OUT_T, "F5_三棵树_A4横_放大104")
print(f"放大 {scale*100:.1f}%,源区 {w/805*2.54:.1f}×{need_h/805*2.54:.1f} cm → 29.0×20.3;上下各裁 {(h-need_h)/2/805*2.54:.2f} cm")
