# -*- coding: utf-8 -*-
"""三棵树 大都会藏本 打印稿(2026-10-28):Met 原图(3730×2863,含白色托纸)→ 自动找到纸张(米色)边界裁掉托纸 →
按高铺满可印区 20.3(纸张 21.3×28.3 → 约 27.0×20.3,约原作 95%)→ 左右余量印裁切线(两边裁切版)。
纸色是真实的米色(a*+1.3),不做纸色校正;输出 待印_两边裁切_20261027/F5_三棵树_Met_A4横.jpg(sRGB)。"""
import numpy as np
from PIL import Image
import gen_print_v6_frame as g, gen_print_v8_twoside as v8
src = g.to_srgb(Image.open(g.LIB/"伦勃朗_Rembrandt_1606-1669/版画/1643_三棵树(大都会藏本)/原图.jpg"))
L, a, b = g.to_lab(src)
mount = (L > 88) & (np.abs(b) < 8)                 # 托纸:很亮且不偏黄
rows = np.where((~mount).mean(1) > 0.5)[0]; cols = np.where((~mount).mean(0) > 0.5)[0]
box = (cols[0] + 2, rows[0] + 2, cols[-1] - 1, rows[-1] - 1)
sheet = src.crop(box)
print("纸张像素", sheet.size, f"≈ {sheet.width/3730*28.3:.1f}×{sheet.height/3730*28.3:.1f} cm(按 Met 纸张宽 28.3 换算)")
W, H = v8.fill(sheet.width, sheet.height, True)
tp = sheet.resize((v8.px(W), v8.px(H)), Image.LANCZOS)
g.save(v8.trim_page(tp, True), v8.OUT_T, "F5_三棵树_Met_A4横")
print(f"画面 {W:.1f}×{H:.1f} cm,源图在此尺寸 {sheet.width/W*2.54:.0f} ppi,裁 {'左右' if v8.sides_of(W,H,True)=='lr' else '上下'}")
