# -*- coding: utf-8 -*-
"""画墙打印稿 v8(2026-10-27):两套,都不改原画比例,都只在一个方向留裁切(上下 或 左右),另一方向顶到打印边。
  A 两边裁切版(trim):画按一个方向铺满可印区,余量只在另一方向,余量里印裁切线;印完只裁两刀。
  B 画框版(frame):画外加一圈等宽的印刷画框(深色框条 1.0 cm + 米色内衬 0.15 cm),框的外沿在铺满方向顶到打印边,
    另一方向余量里印裁切线;同样只裁两刀。三棵树保持 1:1,为装进框只好再裁一点版面。
输出 06_打印稿/待印_两边裁切_20261027/ 与 06_打印稿/待印_画框版_20261027/。海上渔夫已放弃,不出。
"""
from PIL import Image, ImageDraw
import gen_print_v6_frame as g

P, px = g.P, g.px
FRAME_W, LIP_W = 1.0, 0.15
FRAME_COL, LIP_COL = (30, 28, 26), (222, 214, 200)
MARK, GAP = 0.6, 0.1

def page(landscape):
    w, h = (g.A4[1], g.A4[0]) if landscape else g.A4
    return Image.new("RGB", (px(w), px(h)), "white")

def marks(pg, x0, y0, w, h, sides):
    """只在 sides('lr' 或 'tb')方向的余量里印裁切线:延长画(或框)的边线,离边 GAP,长 MARK。"""
    d = ImageDraw.Draw(pg); gp, mk, lw = px(GAP), px(MARK), max(1, px(0.02))
    if sides == "lr":
        for x in (x0, x0 + w):
            for y, s in ((y0, -1), (y0 + h, 1)):
                pass
            for yy in (y0, y0 + h):          # 横线:从画边向左右延伸
                for xx, s in ((x0, -1), (x0 + w, 1)):
                    d.line((xx + s*gp, yy, xx + s*(gp + mk), yy), fill=(40, 40, 40), width=lw)
    else:
        for xx in (x0, x0 + w):              # 竖线:从画边向上下延伸
            for yy, s in ((y0, -1), (y0 + h, 1)):
                d.line((xx, yy + s*gp, xx, yy + s*(gp + mk)), fill=(40, 40, 40), width=lw)

def fill(w, h, landscape, pad=0.0):
    cw, ch = (g.PH, g.PW) if landscape else (g.PW, g.PH)
    cw, ch = cw - 2*pad, ch - 2*pad
    H = ch; W = H*w/h
    if W > cw: W = cw; H = W*h/w
    return W, H

def sides_of(W, H, landscape):
    cw, ch = (g.PH, g.PW) if landscape else (g.PW, g.PH)
    return "lr" if cw - W > ch - H else "tb"

def trim_page(tp, landscape):
    pg = page(landscape)
    x0, y0 = (pg.width - tp.width)//2, (pg.height - tp.height)//2
    pg.paste(tp, (x0, y0))
    W, H = tp.width/P*2.54, tp.height/P*2.54
    cw, ch = (g.PH, g.PW) if landscape else (g.PW, g.PH)
    if max(cw - W, ch - H) > 2*GAP:
        marks(pg, x0, y0, tp.width, tp.height, sides_of(W, H, landscape))
    return pg

def frame_page(tp, landscape):
    pg = page(landscape); d = ImageDraw.Draw(pg)
    fw, lw = px(FRAME_W), px(LIP_W)
    ow, oh = tp.width + 2*(fw + lw), tp.height + 2*(fw + lw)
    x0, y0 = (pg.width - ow)//2, (pg.height - oh)//2
    d.rectangle((x0, y0, x0 + ow - 1, y0 + oh - 1), fill=FRAME_COL)
    d.rectangle((x0 + fw, y0 + fw, x0 + ow - fw - 1, y0 + oh - fw - 1), fill=LIP_COL)
    pg.paste(tp, (x0 + fw + lw, y0 + fw + lw))
    W, H = ow/P*2.54, oh/P*2.54
    cw, ch = (g.PH, g.PW) if landscape else (g.PW, g.PH)
    if max(cw - W, ch - H) > 2*GAP:
        marks(pg, x0, y0, ow, oh, sides_of(W, H, landscape))
    return pg

OUT_T = g.BASE/"06_打印稿"/"待印_两边裁切_20261027"
OUT_F = g.BASE/"06_打印稿"/"待印_画框版_20261027"
WORKS = [(g.WORKS[0][0], g.WORKS[0][1], True, g.LIFTS[:1]),
         (g.WORKS[1][0], g.WORKS[1][1], False, g.LIFTS),
         (g.WORKS[3][0], g.WORKS[3][1], False, g.LIFTS[:1])]
for name, path, land, lifts in WORKS:
    src = g.to_srgb(Image.open(path))
    W, H = fill(src.width, src.height, land)
    tp = src.resize((px(W), px(H)), Image.LANCZOS)
    for tag, lb in lifts:
        g.save(trim_page(g.lift(tp, lb), land), OUT_T, f"{name}_{tag}_黑位{lb}")
    print(f"[裁切版] {name}: 画面 {W:.1f}×{H:.1f},裁 {'左右' if sides_of(W, H, land) == 'lr' else '上下'}")
    Wf, Hf = fill(src.width, src.height, land, pad=FRAME_W + LIP_W)
    tpf = src.resize((px(Wf), px(Hf)), Image.LANCZOS)
    for tag, lb in lifts:
        g.save(frame_page(g.lift(tpf, lb), land), OUT_F, f"{name}_画框_{tag}_黑位{lb}")
    ow, oh = Wf + 2*(FRAME_W + LIP_W), Hf + 2*(FRAME_W + LIP_W)
    print(f"[画框版] {name}: 画面 {Wf:.1f}×{Hf:.1f},连框 {ow:.1f}×{oh:.1f},裁 {'左右' if sides_of(ow, oh, land) == 'lr' else '上下'}")

# F5 三棵树:裁切版 = v1 满版 1:1;画框版 = 1:1 再裁到框内(29.0-2.3)×(20.3-2.3)
tt = Image.open(g.TT); x1, y1, x2, y2 = g.TT_SHEET
src_ppi = (x2 - x1)/(g.TT_SHEET_W_CM/2.54); cx, cy = (x1 + x2)/2, (y1 + y2)/2
def tt_crop(cw, ch):
    box = tuple(round(v) for v in (cx - cw/2.54*src_ppi/2, cy - ch/2.54*src_ppi/2, cx + cw/2.54*src_ppi/2, cy + ch/2.54*src_ppi/2))
    c = tt.crop(box); c.info["icc_profile"] = tt.info.get("icc_profile")
    return g.to_srgb(c).resize((px(cw), px(ch)), Image.LANCZOS)
g.save(trim_page(tt_crop(g.PH, g.PW), True), OUT_T, "F5_三棵树_A4横_满版原大")
g.save(frame_page(tt_crop(g.PH - 2*(FRAME_W + LIP_W), g.PW - 2*(FRAME_W + LIP_W)), True), OUT_F, "F5_三棵树_A4横_画框_原大")
print(f"[F5] 裁切版 1:1 满版 29.0×20.3;画框版 1:1 版面 {g.PH-2.3:.1f}×{g.PW-2.3:.1f},连框顶满,不用裁")
