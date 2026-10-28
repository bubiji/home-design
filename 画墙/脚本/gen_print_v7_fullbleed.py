# -*- coding: utf-8 -*-
"""画墙打印稿 v7(2026-10-27):不要留白。两招并用——
  1. 画按可印区铺满:至少一个方向顶到 3.5 mm 打印边,另一方向的余量尽量小;比例差得多的画裁一点
     (裁的位置按画定,不是机械居中);
  2. 余量里只印裁切标记(四角短线),印完沿线裁纸,纸就是画的尺寸,一点白边都没有。
     装卡纸的(F1/F2/F5)裁完正好压在窗口下;不装卡纸的按裁后尺寸配框。
每幅的做法:
  F1 米勒《春》   横放,裁高 10%(上 3%、下 7%,保住彩虹),铺满 28.0×19.3;余量 0.5 cm 四边均匀,裁切后 28.0×19.3
  F2 哈默修伊     竖放,不裁,按宽铺满 20.3×24.3;上下各 2.35 cm 余量印裁切线,裁后 20.3×24.3(窗口 20×24 正好)
  F5 三棵树       横放,1:1 满版 29.0×20.3(同 v1),无余量
  广重 猿若町     竖放,不裁,按高铺满 19.1×29.0;左右各 0.6 cm 余量印裁切线,裁后 19.1×29.0
  海上渔夫        用户 2026-10-27 放弃,不出
输出 06_打印稿/待印五幅_满版裁切_20261027/,全部黑位档。
"""
import io, pathlib
import numpy as np
from PIL import Image, ImageCms, ImageDraw
import gen_print_v6_frame as g

P, px = g.P, g.px
OUT = g.BASE/"06_打印稿"/"待印五幅_满版裁切_20261027"
MARK = 0.6      # 裁切标记长度 cm
GAP = 0.1       # 标记离画边的距离 cm(刀口留在画外)

def page(landscape):
    w, h = (g.A4[1], g.A4[0]) if landscape else g.A4
    return Image.new("RGB", (px(w), px(h)), "white")

def marks(pg, x0, y0, w, h):
    """画四角的裁切标记(画外 GAP 处起,长 MARK),画内不画。"""
    d = ImageDraw.Draw(pg); gp, mk, lw = px(GAP), px(MARK), max(1, px(0.02))
    for x in (x0, x0 + w):
        for y, s in ((y0, -1), (y0 + h, 1)):
            d.line((x, y + s*gp, x, y + s*(gp + mk)), fill=(40, 40, 40), width=lw)
    for y in (y0, y0 + h):
        for x, s in ((x0, -1), (x0 + w, 1)):
            d.line((x + s*gp, y, x + s*(gp + mk), y), fill=(40, 40, 40), width=lw)

def place(tp, landscape):
    pg = page(landscape)
    x0, y0 = (pg.width - tp.width)//2, (pg.height - tp.height)//2
    pg.paste(tp, (x0, y0))
    m = px(g.MARGIN)
    if x0 - m > px(GAP) or y0 - m > px(GAP):
        marks(pg, x0, y0, tp.width, tp.height)
    return pg

def fitfull(w, h, landscape, pad=0.0):
    cw, ch = (g.PH, g.PW) if landscape else (g.PW, g.PH)
    cw, ch = cw - 2*pad, ch - 2*pad
    H = ch; W = H*w/h
    if W > cw: W = cw; H = W*h/w
    return W, H

def emit(name, tp, landscape, lifts):
    W, H = tp.width/P*2.54, tp.height/P*2.54
    for tag, lb in lifts:
        g.save(place(g.lift(tp, lb), landscape), OUT, f"{name}_{tag}_黑位{lb}")
    print(f"{name}: 画面 {W:.1f}×{H:.1f} cm")

# F1 米勒:裁高 10%(上 3%、下 7%),余量 0.5
src = g.to_srgb(Image.open(g.WORKS[0][1]))
top, bot = round(src.height*0.03), round(src.height*0.07)
im = src.crop((0, top, src.width, src.height - bot))
W, H = fitfull(im.width, im.height, True, pad=0.5)
emit("F1_米勒春_A4横_裁高10", im.resize((px(W), px(H)), Image.LANCZOS), True, g.LIFTS[:1])

# F2 哈默修伊:不裁,按宽铺满
src = g.to_srgb(Image.open(g.WORKS[1][1]))
W, H = fitfull(src.width, src.height, False)
emit("F2_哈默修伊_A4竖_满宽", src.resize((px(W), px(H)), Image.LANCZOS), False, g.LIFTS)

# 广重 猿若町:不裁,按高铺满
src = g.to_srgb(Image.open(g.WORKS[3][1]))
W, H = fitfull(src.width, src.height, False)
emit("广重_猿若町夜景_A4竖_满高", src.resize((px(W), px(H)), Image.LANCZOS), False, g.LIFTS[:1])

# F5 三棵树:1:1 满版(与 v1 相同)
tt = Image.open(g.TT)
x1, y1, x2, y2 = g.TT_SHEET
src_ppi = (x2 - x1)/(g.TT_SHEET_W_CM/2.54)
cw, ch = g.PH, g.PW
cx, cy = (x1 + x2)/2, (y1 + y2)/2
box = tuple(round(v) for v in (cx - cw/2.54*src_ppi/2, cy - ch/2.54*src_ppi/2, cx + cw/2.54*src_ppi/2, cy + ch/2.54*src_ppi/2))
c = tt.crop(box); c.info["icc_profile"] = tt.info.get("icc_profile")
tp = g.to_srgb(c).resize((px(cw), px(ch)), Image.LANCZOS)
g.save(place(tp, True), OUT, "F5_三棵树_A4横_满版原大")
print(f"F5_三棵树: 画面 {cw:.1f}×{ch:.1f} cm,1:1")
