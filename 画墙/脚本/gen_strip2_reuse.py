# -*- coding: utf-8 -*-
"""试印条 2(2026-10-27):复用已印过的那张 Velvet(试印条_透纳海上渔夫_A4竖,AirPrint 印的),只往它底部还空着的
约 20.3×9 cm 白区里印,其余整页纯白(白 = 不出墨),所以同一张纸同方向再走一遍打印机就行。
内容(自上而下):连续 L* 0→100 渐变条 / L* 0–40 分级色块 / 海上渔夫最暗处 A·B·C 三档小样。
用来在 Epson 驱动路径下看:纸从第几格分得开、暗部三档哪档好、与上半张 AirPrint 的结果直接对比。
输出 06_打印稿/试印条2_复用底部_A4竖.{jpg,pdf}。
"""
import pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import gen_print_v6_frame as g

P, px = g.P, g.px
OUT = g.BASE/"06_打印稿"
TOP = 20.3                     # 旧试印条最后一行字在 19.7 cm 处结束,从这里往下是空白
BOTTOM = g.A4[1] - g.MARGIN    # 29.35
X0 = g.MARGIN; W = g.PW        # 可印宽 20.3

pg = Image.new("RGB", (px(g.A4[0]), px(g.A4[1])), "white")
d = ImageDraw.Draw(pg)
f_s, f_m = ImageFont.truetype(g.FONT, px(.30)), ImageFont.truetype(g.FONT, px(.40))

y = TOP
d.text((px(X0), px(y)), "试印条 2 · Epson 驱动 · Velvet · 最高画质 · 与上方 AirPrint 结果对比", font=f_m, fill="black")
y += 0.65

# 1) 连续渐变 L* 0 → 100
h = 1.0
L = np.tile(np.linspace(0, 100, px(W), dtype=np.float32), (px(h), 1))
z = np.zeros_like(L)
pg.paste(g.lab_to_img(L, z, z), (px(X0), px(y)))
for Lv in (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100):
    x = px(X0) + round(Lv/100*(px(W) - 1))
    d.line((x, px(y + h), x, px(y + h + .12)), fill="black")
    d.text((x - (px(.6) if Lv == 100 else px(.1)), px(y + h + .14)), str(Lv), font=f_s, fill="black")
y += h + 0.75

# 2) L* 0–40 分级(与旧试印条同刻度,多加 1/3/5/7)
steps = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 25, 30, 40]
bw, bh = px(W/len(steps)), px(1.3)
for i, Lv in enumerate(steps):
    z = np.zeros((bh, bw), np.float32)
    pg.paste(g.lab_to_img(z + Lv, z, z), (px(X0) + i*bw, px(y)))
    d.text((px(X0) + i*bw + px(.08), px(y) + bh + px(.06)), str(Lv), font=f_s, fill="black")
d.text((px(X0), px(y) + bh + px(.42)), "L* 分级:干透后在挂画位置看,从左数第几格开始能和左邻分开(上半张是 AirPrint 印的同一刻度)", font=f_s, fill="black")
y += 1.3 + 0.95

# 3) 海上渔夫最暗处 A/B/C 小样(船 + 下方暗浪,与定稿同一缩放)
src = g.to_srgb(Image.open(g.WORKS[2][1]))
Wc, Hc = g.fit(src.width, src.height, True)
tp = src.resize((px(Wc), px(Hc)), Image.LANCZOS)
sw, sh, gap = 6.6, BOTTOM - y - 0.5, 0.25
bx, by = round(tp.width*.24), round(tp.height*.55)
strip = tp.crop((bx, by, bx + px(sw), min(tp.height, by + px(sh))))
for i, (tag, lb) in enumerate(g.LIFTS):
    x = px(X0 + i*(sw + gap))
    pg.paste(g.lift(strip, lb), (x, px(y)))
    d.text((x, px(y) + strip.height + px(.08)), f"{tag}  黑位 L*{lb}" + ("(原样)" if not lb else ""), font=f_s, fill="black")
assert px(y) + strip.height + px(.45) <= px(BOTTOM), "超出可印区"
print(f"小样高 {strip.height/P*2.54:.1f} cm,底边到 {(px(y)+strip.height+px(.45))/P*2.54:.2f} cm(可印到 {BOTTOM:.2f})")

g.save(pg, OUT, "试印条2_复用底部_A4竖")
