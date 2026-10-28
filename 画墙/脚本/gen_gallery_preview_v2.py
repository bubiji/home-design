# -*- coding: utf-8 -*-
"""画墙预览 v2：F1 改为米勒《春》（惠斯勒去掉）；画面上标框号、外框尺寸、水平位置、框缝、到显示器/桌面/桌边的距离、卡纸窗口与边宽。
三个留白候选方案可切换（A 现状 / B 全满框 / C 全留白），都是候选，未写入 room 数据。
位置取自 room_v4.json「画墙_方案1_v4」；输出自包含 HTML。URL 加 #s=b 可直接打开某个方案。"""
import base64, json, math, pathlib, re, subprocess, tempfile

BASE = pathlib.Path(__file__).resolve().parents[2]          # 客厅设计/
ART = BASE/"04_名画素材"
OUT = BASE/"画墙预览_v2.html"
ROOM = json.loads((BASE/"room_v4.json").read_text(encoding="utf-8"))["画墙_方案1_v4"]
F = '-apple-system,"PingFang SC","Hiragino Sans",sans-serif'
TOP, X0, W, H = 212, -125, 250, 156      # 画面上沿离地 cm；viewBox
LIP = 1.5                                # 黑框边宽（假设值）
DESK_L, DESK_R, DESK_TOP, MON_X, MON_TOP, MON_H, BEAM = -80, 80, 72, 35.5, 122, 41, 200
DIM, MUTED, ACC = "#5b554d", "#7a736a", "#2f6f5e"

# 框 → (图, 短名, 全名, 原作 w×h cm, 原作说明)
WORKS = {
    "F1": ("millet_spring.jpg", "米勒《春》", "米勒《春》1868–73", (111, 86), "奥赛，油画"),
    "F2": ("hammershoi.jpg", "哈默修伊", "哈默修伊《室内，年轻女子背影》", (50.5, 61), "Randers，油画"),
    "F3": ("kanbara.jpg", "蒲原夜雪", "广重《蒲原夜雪》", (36.5, 25.2), "大判锦绘，纸张约"),
    "F4": ("wave.jpg", "神奈川冲浪里", "北斋《神奈川冲浪里》", (37.9, 25.7), "大判锦绘，纸张约"),
    "F5": ("threetrees.jpg", "三棵树", "伦勃朗《三棵树》", (27.9, 21.3), "蚀刻，版面"),
}
SLOTS = ["F1", "F2", "F3", "F4", "F5"]

def geom(slot):
    (x1, x2), (h1, h2) = ROOM[slot]["距桌中线"], ROOM[slot]["离地"]
    return x1, x2, h1, h2, x2 - x1, h2 - h1

def fit_window(slot, border):
    """在「框内净尺寸四边各留 border」的范围里，按原作比例取最大窗口，向下取到 0.5。"""
    *_, w, h = geom(slot)
    ow, oh = WORKS[slot][3]
    bw, bh = w - 2*LIP - 2*border, h - 2*LIP - 2*border
    ww, wh = (bw, bw*oh/ow) if bw/bh <= ow/oh else (bh*ow/oh, bh)
    return math.floor(ww*2)/2, math.floor(wh*2)/2

def rule_c(slot):                         # 可见卡纸边 = 外框短边的 1/8，且不小于框边宽的 2 倍
    *_, w, h = geom(slot)
    return max(2*LIP, min(w, h)/8)

SCHEMES = {
    "a": ("A 现状", "沿用旧方案：F1、F2、F5 带卡纸，F3、F4 满框。窗口是按现成框规格和 A4 画芯凑出来的，没有统一规则。",
          {"F1": (36, 28), "F2": (20, 24), "F3": None, "F4": None, "F5": (28, 20)}),
    "b": ("B 全满框", "规则：都不用卡纸，画芯铺满外框，超出框比例的部分裁掉。画面最大，但有裁切。",
          {s: None for s in SLOTS}),
    "c": ("C 全留白", "规则：都用卡纸；可见卡纸边 ≥ 外框短边的 1/8 且 ≥ 3 cm；窗口按原作比例，不裁切。",
          {s: fit_window(s, rule_c(s)) for s in SLOTS}),
}

def prep(name):
    with tempfile.TemporaryDirectory() as d:
        t = pathlib.Path(d)/"t.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78", "-Z", "1000", str(ART/name), "--out", str(t)],
                       check=True, capture_output=True)
        o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(t)], check=True, capture_output=True, text=True).stdout
        pw, ph = (int(v) for v in re.findall(r"pixel(?:Width|Height): (\d+)", o))
        return "data:image/jpeg;base64," + base64.b64encode(t.read_bytes()).decode(), pw, ph

def y(h):
    return TOP - h

def sg(v):                                # 带符号的坐标
    return "0" if v == 0 else f"{'+' if v > 0 else '−'}{abs(v):g}"

def line(x1, y1, x2, y2, col=DIM, sw=.2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}"{d}/>'

def text(x, yy, s, size=2.6, fill=DIM, anchor="middle", extra=""):
    return f'<text x="{x}" y="{yy}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'

def hchain(h, xs, coords=()):
    s = [line(xs[0], y(h), xs[-1], y(h))]
    for x in xs:
        s.append(line(x, y(h)-1, x, y(h)+1))
    for a, b in zip(xs, xs[1:]):
        s.append(text((a+b)/2, y(h)-1, f"{b-a:g}"))
    for x in coords:
        s.append(text(x, y(h)+3.2, sg(x), 2.1, MUTED))
    return "".join(s)

def vchain(x, hs, side, names=None, dy=.8):
    """side=+1：段长写在线右侧、离地高度写在左侧；−1 相反。"""
    s = [line(x, y(hs[0]), x, y(hs[-1]))]
    for h in hs:
        s.append(line(x-1, y(h), x+1, y(h)))
        lab = (names or {}).get(h, f"{h:g}")
        if lab:
            s.append(text(x - side*1.6, y(h)+dy, lab, 2.1, MUTED, "end" if side > 0 else "start"))
    for a, b in zip(hs, hs[1:]):
        s.append(text(x + side*1.4, y((a+b)/2)+.9, f"{b-a:g}", 2.6, DIM, "start" if side > 0 else "end"))
    return "".join(s)

def calc(slot, win):
    """返回绘图与表格用的全部数字；每个都由位置数据和窗口算出。"""
    x1, x2, h1, h2, w, h = geom(slot)
    ow, oh = WORKS[slot][3]
    bw, bh = win if win else (w, h)       # 画芯占的范围：有卡纸 = 窗口；满框 = 外框
    if bw/bh >= ow/oh: scale, crop, cdir = bw/ow, 1 - (ow/oh)/(bw/bh), "上下"
    else:              scale, crop, cdir = bh/oh, 1 - (bw/bh)/(ow/oh), "左右"
    paper = "A4" if max(bw, bh) <= 30 and min(bw, bh) <= 21.3 else "A3" if max(bw, bh) <= 42.3 and min(bw, bh) <= 30 else "A2"
    return dict(x1=x1, x2=x2, h1=h1, h2=h2, w=w, h=h, bw=bw, bh=bh, scale=scale, crop=crop, cdir=cdir, paper=paper,
                mx=(w-2*LIP-bw)/2 if win else 0, my=(h-2*LIP-bh)/2 if win else 0)

def frame(slot, win):
    c = calc(slot, win)
    x1, h2, w, h = c["x1"], c["h2"], c["w"], c["h"]
    cx, cy = (c["x1"]+c["x2"])/2, y((c["h1"]+c["h2"])/2)
    s = [f'<rect x="{x1}" y="{y(h2)}" width="{w}" height="{h}" fill="#141414" filter="url(#sh)"/>']
    if win:
        s.append(f'<rect x="{x1+LIP}" y="{y(h2)+LIP}" width="{w-2*LIP}" height="{h-2*LIP}" fill="#f3f0e9"/>')
        s.append(f'<rect x="{cx-c["bw"]/2-.15}" y="{cy-c["bh"]/2-.15}" width="{c["bw"]+.3}" height="{c["bh"]+.3}" fill="#d8d3c7"/>')
    s.append(f'<use href="#im-{slot}" x="{cx-c["bw"]/2}" y="{cy-c["bh"]/2}" width="{c["bw"]}" height="{c["bh"]}"/>')
    if not win:
        s.append(f'<rect x="{x1+LIP/2}" y="{y(h2)+LIP/2}" width="{w-LIP}" height="{h-LIP}" fill="none" stroke="#141414" stroke-width="{LIP}"/>')
    elif c["my"] >= 2.4:                  # 下方卡纸带里写窗口与可见边宽
        lab = "窗 {bw:g}×{bh:g} · 边 {mx:g}|{my:g}".format(**c)
        size = min(2.1, (w - 2*LIP - 2) / (.58*len(lab) + 1.2))     # 字宽估算：不超出框内净宽
        s.append('<g class="dims">' + text(cx, y(c["h1"])-LIP-c["my"]/2+size*.36, lab, round(size, 2), "#8a8377") + '</g>')
    return "".join(s)

def annotations():
    g = {s: geom(s) for s in SLOTS}
    a = []
    for s in SLOTS:                       # 框号 + 外框尺寸 + 作品，写在各框左上角外侧
        x1, x2, h1, h2, w, h = g[s]
        a.append(f'<text x="{x1+.8}" y="{y(h2)-1.1}" font-size="2.6" fill="#333"><tspan font-weight="700" fill="{ACC}">{s}</tspan> {w:g}×{h:g} {WORKS[s][1]}</text>')
    top = [g["F3"][0], g["F3"][1], g["F1"][0], g["F1"][1], g["F4"][0], g["F4"][1]]
    for x in top:
        a.append(line(x, y(180), x, y(185), MUTED, .12, "1 1"))
    a.append(hchain(190, top, top))
    left = [DESK_L, g["F2"][0], g["F2"][1], -MON_X]
    a.append(line(DESK_L, y(DESK_TOP), DESK_L, y(100), MUTED, .12, "1 1"))
    a.append(hchain(106, left, left[:3]))
    right = [MON_X, g["F5"][0], g["F5"][1]]
    a.append(line(DESK_R, y(DESK_TOP), DESK_R, y(100), MUTED, .12, "1 1"))
    a.append(text(DESK_R-1, y(76), f"桌边 {sg(DESK_R)}", 2.1, MUTED, "end"))
    a.append(hchain(106, right, right[1:]))
    lx, rx = -92, 96
    for h, xe in ((DESK_TOP, DESK_L), (g["F2"][2], g["F2"][0]), (g["F2"][3], g["F2"][0]), (g["F3"][2], g["F3"][0]), (g["F3"][3], g["F3"][0])):
        a.append(line(lx, y(h), xe, y(h), MUTED, .12, "1 1"))
    a.append(vchain(lx, [DESK_TOP, g["F2"][2], g["F2"][3], g["F3"][2], g["F3"][3], BEAM], +1,
                    {DESK_TOP: f"{DESK_TOP} 桌面", g["F3"][3]: f'{g["F3"][3]:g} 顶线', BEAM: f"{BEAM} 梁底"}))
    for h, xe in ((DESK_TOP, DESK_R), (g["F5"][2], g["F5"][1]), (g["F5"][3], g["F5"][1]), (g["F4"][2], g["F4"][1]), (g["F4"][3], g["F4"][1])):
        a.append(line(xe, y(h), rx, y(h), MUTED, .12, "1 1"))
    a.append(vchain(rx, [DESK_TOP, g["F5"][2], g["F5"][3], g["F4"][2], g["F4"][3], BEAM], -1, {BEAM: ""}))
    a.append(vchain(32, [MON_TOP, g["F1"][2], g["F1"][3]], +1, {g["F1"][3]: ""}, dy=-.7))
    a.append(line(g["F1"][1], y(g["F1"][2]), 32, y(g["F1"][2]), MUTED, .12, "1 1"))
    a.append(text(0, y(MON_TOP)+MON_H/2-1, f"显示器 {2*MON_X:g}×{MON_H}", 2.6, "#c9ccd3"))
    a.append(text(0, y(MON_TOP)+MON_H/2+3, f"顶 {MON_TOP} · 左右缘 ±{MON_X:g} · 顶到桌面 {MON_TOP-DESK_TOP}", 2.3, "#c9ccd3"))
    a.append(text(1.2, y(BEAM)-2.5, "中线 0", 2.3, MUTED, "start"))
    return "".join(a)

def scene(imgs):
    s = [f'<svg viewBox="{X0} 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family=\'{F}\'>',
         '<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx=".5" dy="1" stdDeviation="1" flood-color="#000" flood-opacity=".32"/></filter>'
         '<linearGradient id="wl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9e4da"/><stop offset="1" stop-color="#f1ede5"/></linearGradient>']
    for slot, (uri, pw, ph) in imgs.items():
        s.append(f'<symbol id="im-{slot}" viewBox="0 0 {pw} {ph}" preserveAspectRatio="xMidYMid slice"><image href="{uri}" width="{pw}" height="{ph}"/></symbol>')
    s.append('</defs>')
    s.append(f'<rect x="{X0}" y="0" width="{W}" height="{H}" fill="url(#wl)"/><rect x="{X0}" y="0" width="{W}" height="{y(BEAM)}" fill="#dcd6ca"/>')
    s.append(f'<g class="dims">{line(0, y(BEAM)-6, 0, y(195), MUTED, .15, "3 1 .6 1")}{line(0, y(186), 0, y(60), MUTED, .15, "3 1 .6 1")}</g>')
    s.append(f'<rect x="{-MON_X}" y="{y(MON_TOP)}" width="{2*MON_X}" height="{MON_H}" rx=".8" fill="#1d1d1f"/><rect x="{-MON_X+1.2}" y="{y(MON_TOP)+1.2}" width="{2*MON_X-2.4}" height="{MON_H-3.4}" fill="#31343a"/>')
    s.append(f'<rect x="-4" y="{y(MON_TOP-MON_H)}" width="8" height="{MON_TOP-MON_H-DESK_TOP}" fill="#1d1d1f"/>')
    s.append(f'<rect x="{DESK_L}" y="{y(DESK_TOP)}" width="{DESK_R-DESK_L}" height="3.2" fill="#9a6f45"/><rect x="-74" y="{y(DESK_TOP)+3.2}" width="5" height="{H}" fill="#8b633d"/><rect x="69" y="{y(DESK_TOP)+3.2}" width="5" height="{H}" fill="#8b633d"/>')
    for k, (_, _, wins) in SCHEMES.items():
        s.append(f'<g class="s s-{k}">' + "".join(frame(slot, wins[slot]) for slot in SLOTS) + '</g>')
    s.append(f'<g class="dims">{annotations()}</g></svg>')
    return "\n".join(s)

def pos_table():
    r = []
    for s in SLOTS:
        x1, x2, h1, h2, w, h = geom(s)
        dm = h1 - MON_TOP
        mon = f"高 {dm:g}" if dm >= 0 else f"底边低于显示器顶 {-dm:g}，侧距显示器 {min(abs(x1), abs(x2)) - MON_X:g}"
        edge = (x1 - DESK_L) if x1 < 0 and x2 < 0 else (DESK_R - x2) if x1 > 0 else None
        ed = "居中" if edge is None else (f"内缩 {edge:g}" if edge >= 0 else f"超出 {-edge:g}")
        r.append(f'<tr><td><b>{s}</b></td><td>{w:g}×{h:g}</td><td>{sg(x1)} → {sg(x2)}</td><td>{h1:g} → {h2:g}</td><td>{mon}</td><td>{h1-DESK_TOP:g}</td><td>{ed}</td></tr>')
    return "".join(r)

def art_table():
    r = []
    for k, (_, _, wins) in SCHEMES.items():
        for s in SLOTS:
            c = calc(s, wins[s]); ow, oh = WORKS[s][3]
            have = s == "F4" and not wins[s]              # 现有的 35×25 浪，比例以实物为准
            crop = "以实物为准" if have else "无" if c["crop"] < .02 else "{}共裁 {:.0f}%".format(c["cdir"], c["crop"]*100)
            pr = "已有成品，不用印" if have else (c["paper"] + ("（自印）" if c["paper"] == "A4" else "（外送）"))
            if s == "F4" and wins[s]: pr += "，现有的 35×25 用不上"
            core = ("窗口 {bw:g}×{bh:g}" if wins[s] else "满框 {bw:g}×{bh:g}").format(**c)
            mat = "{mx:g} | {my:g}".format(**c) if wins[s] else "—"
            scale = "以实物为准" if have else "{:.0f}%".format(c["scale"]*100)
            r.append(f'<tr class="s s-{k}"><td><b>{s}</b></td><td>{WORKS[s][2]}<br><span class="m">原作 {ow:g}×{oh:g}，{WORKS[s][4]}</span></td>'
                     f'<td>{core}</td><td>{mat}</td><td>{crop}</td><td>{scale}</td><td>{pr}</td></tr>')
    return "".join(r)

imgs = {s: prep(WORKS[s][0]) for s in SLOTS}
btns = "".join(f'<button data-s="{k}" aria-pressed="{"true" if k == "a" else "false"}">{v[0]}</button>' for k, v in SCHEMES.items())
rules = "".join(f'<p class="sub s s-{k}" style="margin:0 0 10px">{v[1]}</p>' for k, v in SCHEMES.items())
hide = "".join(f'body:not([data-s="{k}"]) .s-{k}{{display:none}}' for k in SCHEMES)
html = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>画墙预览 v2</title>
<style>
:root{{--bg:#faf8f4;--fg:#222;--muted:#6b6560;--line:#c9c2b8;--card:#fff;--accent:{ACC}}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#1b1917;--fg:#ece7df;--muted:#a39b91;--line:#4a443e;--card:#221f1c}}}}
:root[data-theme="dark"]{{--bg:#1b1917;--fg:#ece7df;--muted:#a39b91;--line:#4a443e;--card:#221f1c}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 {F}}}main{{max-width:1180px;margin:0 auto;padding:24px 16px 60px}}
h1{{font-size:24px;margin:0 0 4px}}h2{{font-size:16px;margin:0 0 8px}}.sub{{color:var(--muted);margin:0 0 14px}}.m{{color:var(--muted);font-size:12.5px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin:12px 0}}
svg{{width:100%;height:auto;display:block;border-radius:6px}}
.bar{{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;margin:0 0 8px}}
.seg{{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.seg button{{font:inherit;padding:6px 12px;border:0;background:transparent;color:var(--fg);cursor:pointer}}
.seg button[aria-pressed="true"]{{background:var(--accent);color:#fff}}
label{{cursor:pointer;user-select:none}}
.tw{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:13.5px}}th,td{{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}}th{{color:var(--muted);font-weight:600;white-space:nowrap}}
{hide}
body:not(.show-dims) .dims{{display:none}}
</style></head><body data-s="a" class="show-dims"><main>
<h1>画墙预览 v2 · F1 米勒《春》</h1>
<p class="sub">书桌上方，单位 cm，按比例绘制。水平数字 = 距书桌中线（左负右正），垂直数字 = 离地高度。位置取自 room_v4.json；三个留白方案都是候选，尚未写入正式数据。</p>
<div class="card">
<div class="bar"><span>留白方案：</span><span class="seg">{btns}</span><label><input type="checkbox" id="dims" checked> 尺寸标注</label></div>
{rules}
{scene(imgs)}
<p class="m" style="margin:8px 0 0">链上的数字是相邻两点的距离，链下的小字是坐标。卡纸带里的「窗 a×b · 边 c|d」= 窗口宽×高 · 可见卡纸边 左右|上下。黑框边宽按 {LIP:g} cm 画，是假设值。</p></div>
<div class="card tw"><h2>位置与距离（三个方案相同）</h2><table><tr><th>框</th><th>外框</th><th>水平（距中线）</th><th>离地</th><th>底边到显示器顶 {MON_TOP}</th><th>底边到桌面 {DESK_TOP}</th><th>外缘到桌边 ±{DESK_R}</th></tr>{pos_table()}</table>
<p class="m" style="margin:8px 0 0">框缝：F2↔F3 上下 {geom("F3")[2]-geom("F2")[3]:g}；F5↔F4 上下 {geom("F4")[2]-geom("F5")[3]:g}；F1 到左右两列各 {geom("F1")[0]-geom("F3")[1]:g}。F1 顶到梁底 {BEAM-geom("F1")[3]:g}。</p></div>
<div class="card tw"><h2>画芯与卡纸（随方案变化）</h2><table><tr><th>框</th><th>作品</th><th>画芯范围</th><th>可见卡纸边 左右 | 上下</th><th>裁切</th><th>占原作</th><th>打印</th></tr>{art_table()}</table>
<p class="m" style="margin:8px 0 0">占原作 = 画芯相对原作的缩放比例。满框时画芯按外框尺寸算，四边另被框边压住约 {LIP:g} cm。</p></div>
</main><script>
function setS(k){{document.body.dataset.s=k;document.querySelectorAll('.seg button').forEach(function(o){{o.setAttribute('aria-pressed',o.dataset.s===k)}})}}
document.querySelectorAll('.seg button').forEach(function(b){{b.onclick=function(){{setS(b.dataset.s)}}}});
document.getElementById('dims').onchange=function(e){{document.body.classList.toggle('show-dims',e.target.checked)}};
var m=/s=([a-c])/.exec(location.hash);if(m)setS(m[1]);
</script></body></html>'''
OUT.write_text(html, encoding="utf-8"); print("wrote", OUT, f"{OUT.stat().st_size/1e6:.2f} MB")
for k, (name, _, wins) in SCHEMES.items():
    print(name, {s: (wins[s], f'{calc(s, wins[s])["scale"]*100:.0f}%', f'crop {calc(s, wins[s])["crop"]*100:.0f}%', calc(s, wins[s])["paper"]) for s in SLOTS})
