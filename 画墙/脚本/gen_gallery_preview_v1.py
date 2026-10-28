# -*- coding: utf-8 -*-
"""画墙预览页：把 04_名画素材 里的真图按 cm 比例放进方案 1 的 5 个框，F1 可在惠斯勒 / 米勒《春》之间切换。
位置取自 room_v4.json 的「画墙_方案1_v4」；输出自包含 HTML（图片缩到 1000px 后内嵌）。"""
import base64, json, pathlib, subprocess, tempfile

BASE = pathlib.Path(__file__).resolve().parents[2]          # 客厅设计/
ART = BASE/"04_名画素材"
OUT = BASE/"画墙预览_v1.html"
ROOM = json.loads((BASE/"room_v4.json").read_text(encoding="utf-8"))["画墙_方案1_v4"]
F = '-apple-system,"PingFang SC","Hiragino Sans",sans-serif'
TOP = 205            # 画面上沿离地 cm（梁底 200）
X0, W, H = -100, 200, 150
LIP = 1.5            # 黑框边宽 cm

# 框号 → (图, 作品名, 窗口 w×h 或 None=无卡纸满框, 原作 w×h cm, 原作说明)
WORKS = {
    "F1a": ("whistler.jpg", "惠斯勒《夜曲：蓝与银—切尔西》", (36, 29), (60.8, 50.2), "Tate，油画"),
    "F1b": ("millet_spring.jpg", "米勒《春》1868–73", (36, 28), (111, 86), "奥赛美术馆，油画"),
    "F2": ("hammershoi.jpg", "哈默修伊《室内，年轻女子背影》", (20, 24), (50.5, 61), "Randers 美术馆，油画"),
    "F3": ("kanbara.jpg", "广重《蒲原夜雪》", None, (35, 22.5), "大判锦绘，画面约"),
    "F4": ("wave.jpg", "北斋《神奈川冲浪里》（已有成品）", None, (37.9, 25.7), "大判锦绘，纸张约"),
    "F5": ("threetrees.jpg", "伦勃朗《三棵树》", (28, 20), (27.9, 21.3), "蚀刻，版面"),
}

def b64(name):
    with tempfile.TemporaryDirectory() as d:
        t = pathlib.Path(d)/"t.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78", "-Z", "1000", str(ART/name), "--out", str(t)],
                       check=True, capture_output=True)
        return "data:image/jpeg;base64," + base64.b64encode(t.read_bytes()).decode()

def y(h):            # 离地高度 → svg y
    return TOP - h

def frame(key, slot):
    img, title, win, orig, _ = WORKS[key]
    (x1, x2), (h1, h2) = ROOM[slot]["距桌中线"], ROOM[slot]["离地"]
    w, h = x2 - x1, h2 - h1
    cx, cy = (x1 + x2)/2, y((h1 + h2)/2)
    s = [f'<rect x="{x1}" y="{y(h2)}" width="{w}" height="{h}" fill="#141414" filter="url(#sh)"/>']
    if win:
        ww, wh = win
        s.append(f'<rect x="{x1+LIP}" y="{y(h2)+LIP}" width="{w-2*LIP}" height="{h-2*LIP}" fill="#f3f0e9"/>')
        s.append(f'<rect x="{cx-ww/2-.15}" y="{cy-wh/2-.15}" width="{ww+.3}" height="{wh+.3}" fill="#d8d3c7"/>')
    else:
        ww, wh = w, h        # 无卡纸：画芯按外框尺寸满铺，四边被框边压住
    s.append(f'<image href="{b64(img)}" x="{cx-ww/2}" y="{cy-wh/2}" width="{ww}" height="{wh}" preserveAspectRatio="xMidYMid slice"/>')
    if not win:
        s.append(f'<rect x="{x1+LIP/2}" y="{y(h2)+LIP/2}" width="{w-LIP}" height="{h-LIP}" fill="none" stroke="#141414" stroke-width="{LIP}"/>')
    ow, oh = orig
    ghost = (f'<g class="ghost"><rect x="{cx-ow/2}" y="{cy-oh/2}" width="{ow}" height="{oh}" fill="none" stroke="#b5533c" stroke-width=".5" stroke-dasharray="2 1.5"/>'
             f'<text x="{cx-ow/2+1}" y="{max(cy-oh/2-1.2, 9)}" font-size="3" fill="#b5533c" stroke="#efeae1" stroke-width=".9" paint-order="stroke">原作 {ow:g}×{oh:g}</text></g>')
    return "".join(s), ghost, (ww, wh)

def dim_h(h, label):
    return (f'<line x1="{X0+6}" y1="{y(h)}" x2="{X0+W}" y2="{y(h)}" stroke="#7a736a" stroke-width=".15" stroke-dasharray="1 1"/>'
            f'<text x="{X0+1}" y="{y(h)+1}" font-size="3" fill="#6b6560">{label}</text>')

def scene():
    g = [f'<svg viewBox="{X0} 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family=\'{F}\'>',
         '<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx=".5" dy="1" stdDeviation="1" flood-color="#000" flood-opacity=".32"/></filter>'
         '<linearGradient id="wl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9e4da"/><stop offset="1" stop-color="#f1ede5"/></linearGradient></defs>',
         f'<rect x="{X0}" y="0" width="{W}" height="{H}" fill="url(#wl)"/>',
         f'<rect x="{X0}" y="0" width="{W}" height="{y(200)}" fill="#dcd6ca"/>',                       # 梁
         f'<rect x="-35.5" y="{y(122)}" width="71" height="41" rx=".8" fill="#1d1d1f"/><rect x="-34.3" y="{y(122)+1.2}" width="68.6" height="37.6" fill="#31343a"/>',
         f'<rect x="-4" y="{y(81)}" width="8" height="9" fill="#1d1d1f"/>',
         f'<rect x="-80" y="{y(72)}" width="160" height="3.2" fill="#9a6f45"/><rect x="-74" y="{y(68.8)}" width="5" height="20" fill="#8b633d"/><rect x="69" y="{y(68.8)}" width="5" height="20" fill="#8b633d"/>']
    ghosts, sizes = [], {}
    for slot, key in (("F2", "F2"), ("F3", "F3"), ("F4", "F4"), ("F5", "F5")):
        s, gh, sizes[key] = frame(key, slot); g.append(s); ghosts.append(gh)
    for key, cls in (("F1a", "f1 f1a"), ("F1b", "f1 f1b")):
        s, gh, sizes[key] = frame(key, "F1")
        g.append(f'<g class="{cls}">{s}</g>'); ghosts.append(f'<g class="{cls}">{gh}</g>')
    g.append('<g class="dims">' + dim_h(180, "顶线 180") + dim_h(140, "F1 底 140") + dim_h(122, "显示器顶 122") + dim_h(112, "底线 112") + dim_h(72, "桌面 72")
             + f'<text x="{X0+1}" y="{y(200)-1}" font-size="3" fill="#6b6560">梁底 200</text></g>')
    g += ghosts
    g.append('</svg>')
    return "\n".join(g), sizes

def rows(sizes):
    r = []
    for key, slot in (("F1a", "F1"), ("F1b", "F1"), ("F2", "F2"), ("F3", "F3"), ("F4", "F4"), ("F5", "F5")):
        _, title, win, (ow, oh), note = WORKS[key]
        ww, wh = sizes[key]
        cls = ' class="f1 %s"' % key.lower() if slot == "F1" else ""
        r.append(f'<tr{cls}><td>{slot}</td><td>{title}</td><td>{ROOM[slot]["框"]}</td><td>{f"窗口 {ww:g}×{wh:g}" if win else "满框，无卡纸"}</td>'
                 f'<td>{ow:g}×{oh:g}<br><span class="m">{note}</span></td><td>{"" if win else "约 "}{round(ww/ow*100)}%</td></tr>')
    return "".join(r)

svg, sizes = scene()
html = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>画墙预览</title>
<style>
:root{{--bg:#faf8f4;--fg:#222;--muted:#6b6560;--line:#c9c2b8;--card:#fff;--accent:#2f6f5e}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#1b1917;--fg:#ece7df;--muted:#a39b91;--line:#4a443e;--card:#221f1c}}}}
:root[data-theme="dark"]{{--bg:#1b1917;--fg:#ece7df;--muted:#a39b91;--line:#4a443e;--card:#221f1c}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 {F}}}main{{max-width:1040px;margin:0 auto;padding:24px 16px 60px}}
h1{{font-size:24px;margin:0 0 4px}}.sub{{color:var(--muted);margin:0 0 14px}}.m{{color:var(--muted);font-size:12.5px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin:12px 0}}
svg{{width:100%;height:auto;display:block;border-radius:6px}}
.bar{{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;margin:0 0 10px}}
.seg{{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.seg button{{font:inherit;padding:6px 12px;border:0;background:transparent;color:var(--fg);cursor:pointer}}
.seg button[aria-pressed="true"]{{background:var(--accent);color:#fff}}
label{{cursor:pointer;user-select:none}}
.tw{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:13.5px}}th,td{{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}}th{{color:var(--muted);font-weight:600}}
body[data-f1="a"] .f1b,body[data-f1="b"] .f1a{{display:none}}
body:not(.show-ghost) .ghost,body:not(.show-dims) .dims{{display:none}}
</style></head><body data-f1="a" class="show-dims"><main>
<h1>画墙预览 · 方案 1 错落式</h1>
<p class="sub">书桌上方，单位 cm，按真实比例；位置取自 room_v4.json。屏幕颜色只作参考，哑光纸打印后暗部会更浅。</p>
<div class="card">
<div class="bar"><span>F1：</span><span class="seg"><button data-f1="a" aria-pressed="true">惠斯勒《夜曲》</button><button data-f1="b" aria-pressed="false">米勒《春》</button></span>
<label><input type="checkbox" id="ghost"> 原作尺寸轮廓</label><label><input type="checkbox" id="dims" checked> 高度标注</label></div>
{svg}</div>
<div class="card tw"><table><tr><th>框</th><th>作品</th><th>外框</th><th>可见画面</th><th>原作</th><th>比例</th></tr>{rows(sizes)}</table>
<p class="m" style="margin:8px 0 0">比例 = 画面宽 ÷ 原作宽。F3、F4 无卡纸，按画芯铺满外框尺寸估算，四边被框边压住约 {LIP:g} cm。</p></div>
</main><script>
document.querySelectorAll('.seg button').forEach(function(b){{b.onclick=function(){{document.body.dataset.f1=b.dataset.f1;
document.querySelectorAll('.seg button').forEach(function(o){{o.setAttribute('aria-pressed',o===b)}})}}}});
document.getElementById('ghost').onchange=function(e){{document.body.classList.toggle('show-ghost',e.target.checked)}};
document.getElementById('dims').onchange=function(e){{document.body.classList.toggle('show-dims',e.target.checked)}};
</script></body></html>'''
OUT.write_text(html, encoding="utf-8"); print("wrote", OUT, f"{OUT.stat().st_size/1e6:.2f} MB")
