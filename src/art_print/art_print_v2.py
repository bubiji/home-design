#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""名画打印 v2:两条队列都能走,默认 AirPrint(零依赖,只用系统自带的 lp / lpstat / ipptool / sips)。
2026-10-28 实测:Epson 驱动队列不论画质 354/355/360、不论纸盒还是背面进纸,都每 25 mm 出一条深线;AirPrint High 没有。
所以正式稿默认走 AirPrint,驱动队列留作实验(--queue driver)。

  check  [--queue]                 打印前体检:队列、纸型、墨量、打印机状态
  calib  [--apply] [--queue]       普通纸校准页:100 mm 标尺 + 可印范围框,用来量缩放、看哪一面出墨
  send <文件> --paper <纸> [--queue]  发打印稿;默认只预演,--apply 才真的发;--hold 发成暂停任务(不出纸)

v1(art_print.py)只认 AirPrint 队列,2026-10-27 用它印 Velvet 出现毛边渗墨、暗部糊,原因是 AirPrint 送图上限
360 dpi、纸型/墨量控制粗、没有色彩管理、关不掉自动校正。v2 改为默认 Epson 驱动队列 EPSON_EW_M873T_Driver
(PPD「EPSON EW-M873T Series」13.50),按纸型选驱动自己的用紙種類、最高画质、驱动色彩校正「EPSON 标准」、
不开 PhotoEnhance、不锐化。稿件仍必须是整页 A4(图已按实际尺寸摆好),一律 100% 发,不缩放。说明见 README.md。
"""
import argparse, datetime, json, pathlib, re, subprocess, sys, tempfile

A4_MM = (210.0, 297.0)
QUEUES = {"driver": "EPSON_EW_M873T_Driver", "airprint": "EPSON_EW_M873T"}   # 队列名;地址由队列自己记,不在这里写 IP

# Epson 驱动(PPD 选项 EPIJ_*)。值来自 PPD 的 *EPIJ_Medi / *EPIJ_Qual / *EPIJ_FdSo 列表。
DRV_PAPERS = {   # 纸 → (EPIJ_Medi, EPIJ_Qual, 说明)
    "velvet": ("53", "360", "Epson Velvet Fine Art Paper(驱动 Velvet Fine Art Paper,最高画质)"),
    "matte": ("67", "355", "フォトマット紙(驱动 EPSON Photo Matte Paper,きれい)"),
    "plain": ("0", "354", "普通纸(演练用,标准)"),
}
DRV_SLOTS = {"rear": "0", "main": "2"}                     # EPIJ_FdSo: 0 = Rear Paper Feeder, 2 = Upper Cassette
DRV_FIXED = {                                              # 每次都带的固定项
    "EPIJ_Size": "1",        # A4
    "EPIJ_PSrc": "2",        # 有边(Standard),不用无边距
    "EPIJ_Mode": "3",        # Advanced:自己定画质,不让驱动按「速度/标准/画质」自动选
    "EPIJ_Ink_": "1",        # 彩色
    "EPIJ_CMat": "0",        # Color Settings = Manual(不用 PhotoEnhance,也不是 Off)
    "EPIJ_CCor": "4",        # 驱动色彩校正 = EPSON 标准(把 sRGB 稿映射到纸),不用 Vivid
    "EPIJ_Gamm": "0",        # Gamma 2.2
    "EPIJ_AFil": "0",        # 不锐化
    "EPIJ_OSColMat": "1",    # Vendor Color Matching(驱动管色;ICC 路径用 Epson Print Layout 做)
}

# AirPrint 队列(备用,与 v1 相同)
AIR_PAPERS = {
    "velvet": ("Com.epsonVelvetFineArt", "High", "Epson Velvet Fine Art Paper"),
    "matte": ("PhotographicMatte", "High", "フォトマット紙"),
    "plain": ("Stationery", "Normal", "普通纸(演练用)"),
}
AIR_SLOTS = {"rear": "Rear", "main": "Main"}


def run(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if check and r.returncode:
        sys.exit(f"命令失败: {' '.join(map(str, cmd))}\n{r.stderr.strip() or r.stdout.strip()}")
    return r


def device_uri(queue):
    out = run(["lpstat", "-v", queue], check=False).stdout
    m = re.search(r"(ipps?://\S+)", out)
    if not m:
        sys.exit(f"找不到打印队列 {queue}(lpstat -v 无结果)。")
    return m.group(1)


def printer_attrs(queue):
    """向打印机要属性(只读)。返回 {属性名: 原始字符串}。"""
    out = run(["ipptool", "-tv", device_uri(queue), "get-printer-attributes.test"], check=False).stdout
    attrs = {}
    for line in out.splitlines():
        m = re.match(r"\s+([\w-]+) \([^)]*\) = (.*)", line)
        if m:
            attrs[m.group(1)] = m.group(2)
    return attrs


def queue_choices(queue, option):
    out = run(["lpoptions", "-p", queue, "-l"]).stdout
    for line in out.splitlines():
        if line.startswith(option + "/"):
            return [c.lstrip("*") for c in line.split(":", 1)[1].split()]
    return []


def cmd_check(args):
    q = QUEUES[args.queue]
    a = printer_attrs(q)
    if not a:
        sys.exit("打印机没应答(ipptool 无输出)。检查电源和网络。")
    ok = True
    print(f"队列 {q}({args.queue})→ {a.get('printer-make-and-model', '?')},状态 {a.get('printer-state', '?')} / {a.get('printer-state-reasons', '?')}")
    names = a.get("marker-names", "").split(",")
    levels = [int(x) for x in a.get("marker-levels", "").split(",") if x.strip().lstrip("-").isdigit()]
    lows = [int(x) for x in a.get("marker-low-levels", "").split(",") if x.strip().isdigit()]
    for n, lv, lo in zip(names, levels, lows):
        flag = "  ← 到低位线" if lv <= lo else ""
        ok &= lv > lo
        print(f"  墨 {n:>2}: {lv:>3}%  (低位线 {lo}%){flag}")
    print("  注:墨量是打印机按用量估的,以墨仓窗口实际液位为准。")
    if args.queue == "driver":
        medi, qual, slots = queue_choices(q, "EPIJ_Medi"), queue_choices(q, "EPIJ_Qual"), queue_choices(q, "EPIJ_FdSo")
        for key, (m, ql, label) in DRV_PAPERS.items():
            have = m in medi and ql in qual
            ok &= have
            print(f"  纸型 {key:<6} {label}: {'有' if have else f'驱动里没有 Medi={m}/Qual={ql}'}")
        have = DRV_SLOTS["rear"] in slots
        ok &= have
        print(f"  背面进纸(EPIJ_FdSo=0): {'有' if have else '没有'};驱动进纸口选项 {slots}")
    else:
        types = queue_choices(q, "MediaType")
        for key, (mt, _, label) in AIR_PAPERS.items():
            have = mt in types
            ok &= have
            print(f"  纸型 {key:<6} {label}: {'有' if have else '队列里没有 ' + mt}")
        print(f"  进纸口: {', '.join(queue_choices(q, 'InputSlot'))}")
    print(f"  打印机有边模式边距(1/100 mm): 上 {a.get('media-top-margin-supported')} 下 {a.get('media-bottom-margin-supported')}")
    print("体检通过。" if ok else "体检有问题,见上。")
    return 0 if ok else 1


def image_mm(path):
    out = run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", "-g", "dpiWidth", "-g", "dpiHeight", str(path)]).stdout
    v = {k: float(x) for k, x in re.findall(r"(pixelWidth|pixelHeight|dpiWidth|dpiHeight): ([\d.]+)", out)}
    if len(v) < 4:
        sys.exit(f"读不到尺寸或分辨率: {path}")
    return v["pixelWidth"]/v["dpiWidth"]*25.4, v["pixelHeight"]/v["dpiHeight"]*25.4


def pdf_mm(path):
    b = pathlib.Path(path).read_bytes()
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", b)
    if not m:
        sys.exit(f"读不到 PDF 页面尺寸: {path}")
    x0, y0, x1, y1 = (float(g) for g in m.groups())
    return (x1 - x0)/72*25.4, (y1 - y0)/72*25.4


def to_a4_pdf(src, tmp):
    """整页 A4 稿 → 竖放 A4 的 PDF(带原图的色彩描述文件)。横稿先无损转 90°,免得打印系统自己转、自己缩。"""
    src = pathlib.Path(src)
    if src.suffix.lower() == ".pdf":
        w, h = pdf_mm(src)
        if abs(w - A4_MM[0]) > 1 or abs(h - A4_MM[1]) > 1:
            sys.exit(f"PDF 页面是 {w:.1f}×{h:.1f} mm,不是竖放 A4。横稿请给 JPG/TIFF,由本工具转。")
        return src, (w, h), False
    w, h = image_mm(src)
    land = w > h
    if abs(min(w, h) - A4_MM[0]) > 1 or abs(max(w, h) - A4_MM[1]) > 1:
        sys.exit(f"稿件是 {w:.1f}×{h:.1f} mm,不是整页 A4。先把图排进 A4 页面(四边留 3.5 mm)再发。")
    work = src
    if land:
        work = tmp/"rot.tif"
        run(["sips", "-r", "90", "-s", "format", "tiff", "-s", "formatOptions", "lzw", str(src), "--out", str(work)])
    pdf = tmp/(src.stem + ".pdf")
    run(["sips", "-s", "format", "pdf", str(work), "--out", str(pdf)])
    pw, ph = pdf_mm(pdf)
    if abs(pw - A4_MM[0]) > 1 or abs(ph - A4_MM[1]) > 1:
        sys.exit(f"转出的 PDF 是 {pw:.1f}×{ph:.1f} mm,不是 A4,停止。")
    return pdf, (pw, ph), land


def lp_opts(queue_key, paper, slot, quality, extra):
    """返回 (-o 选项列表, 记录用的 dict)。"""
    if queue_key == "driver":
        medi, qual, _ = DRV_PAPERS[paper]
        o = dict(DRV_FIXED, EPIJ_Medi=medi, EPIJ_Qual=quality or qual, EPIJ_FdSo=DRV_SLOTS[slot or "rear"])
    else:
        mt, q, _ = AIR_PAPERS[paper]
        o = {"media": "iso_a4_210x297mm", "InputSlot": AIR_SLOTS[slot or "rear"], "MediaType": mt,
             "cupsPrintQuality": quality or q, "print-scaling": "none", "ColorModel": "RGB"}
    for kv in extra or []:
        k, _, v = kv.partition("=")
        o[k] = v
    return o


def lp_cmd(queue_key, pdf, title, opts, hold):
    cmd = ["lp", "-d", QUEUES[queue_key], "-t", title]
    for k, v in opts.items():
        cmd += ["-o", f"{k}={v}"]
    if hold:
        cmd += ["-H", "hold"]
    return cmd + [str(pdf)]


def submit(src, pdf, args, extra=None):
    opts = lp_opts(args.queue, args.paper, args.slot, args.quality, args.opt)
    cmd = lp_cmd(args.queue, pdf, pathlib.Path(src).stem, opts, args.hold)
    print("命令:", " ".join(f"'{c}'" if " " in c else c for c in cmd))
    if not args.apply:
        print("预演,没有发送。加 --apply 才发;加 --hold 发成暂停任务(不出纸)。")
        return 0
    out = run(cmd).stdout.strip()
    print(out)
    m = re.search(rf"({QUEUES[args.queue]}-\d+)", out)
    rec = {"time": datetime.datetime.now().isoformat(timespec="seconds"), "file": str(src), "queue": args.queue,
           "paper": args.paper, "slot": args.slot or "rear", "options": opts, "hold": args.hold, "job": m.group(1) if m else ""}
    rec.update(extra or {})
    log = pathlib.Path(args.log) if args.log else pathlib.Path(src).resolve().parent/"打印记录.jsonl"
    if not args.hold:
        with log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print("已记入", log)
    return 0


def cmd_send(args):
    with tempfile.TemporaryDirectory() as d:
        pdf, (w, h), land = to_a4_pdf(args.file, pathlib.Path(d))
        print(f"稿件 {args.file} → PDF {w:.1f}×{h:.1f} mm" + (",横稿已转成竖页" if land else ""))
        label = DRV_PAPERS[args.paper][2] if args.queue == "driver" else AIR_PAPERS[args.paper][2]
        print(f"队列: {QUEUES[args.queue]}({args.queue});纸: {label}")
        return submit(args.file, pdf, args, {"rotated": land})


def calib_pdf(path):
    """手写一页矢量 PDF:3.5 mm 边框、横竖各 100 mm 标尺、进纸方向与出墨面标记。"""
    mm = 72/25.4
    W, H, m = 210*mm, 297*mm, 3.5*mm
    s = [f"0.5 w {m:.2f} {m:.2f} {W-2*m:.2f} {H-2*m:.2f} re S"]
    x0, y0 = 40*mm, 200*mm
    s.append(f"1 w {x0:.2f} {y0:.2f} m {x0+100*mm:.2f} {y0:.2f} l S")
    s.append(f"{x0:.2f} {y0:.2f} m {x0:.2f} {y0-100*mm:.2f} l S")
    for i in range(11):
        s.append(f"{x0+i*10*mm:.2f} {y0:.2f} m {x0+i*10*mm:.2f} {y0+4*mm:.2f} l S")
        s.append(f"{x0:.2f} {y0-i*10*mm:.2f} m {x0-4*mm:.2f} {y0-i*10*mm:.2f} l S")

    def text(x, y, size, t):
        s.append(f"BT /F1 {size} Tf {x:.2f} {y:.2f} Td ({t}) Tj ET")
    text(x0, y0 + 8*mm, 12, "100 mm  (measure tick 0 to tick 10, both rulers)")
    text(30*mm, 280*mm, 16, "TOP of page (note which paper edge comes out first)")
    text(30*mm, 270*mm, 12, "PRINTED SIDE. Outer box = 3.5 mm from each paper edge.")
    text(30*mm, 262*mm, 12, "Pass: both rulers 100.0 mm (+-0.5), all 4 box sides visible.")
    text(30*mm, 20*mm, 12, "BOTTOM")
    body = "\n".join(s).encode()
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {W:.2f} {H:.2f}] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>".encode(),
            b"<< /Length %d >>\nstream\n" % len(body) + body + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offs = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1) + b"".join(b"%010d 00000 n \n" % o for o in offs)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    pathlib.Path(path).write_bytes(out)


def cmd_calib(args):
    args.paper, args.quality, args.log = "plain", None, None
    with tempfile.TemporaryDirectory() as d:
        pdf = pathlib.Path(d)/"校准页.pdf"
        calib_pdf(pdf)
        if args.out:
            calib_pdf(args.out)
            print("校准页另存到", args.out)
        print(f"校准页:普通纸,队列 {QUEUES[args.queue]}({args.queue});量两条 100 mm 标尺、看四条边框是否都在、记下哪一面出墨。")
        opts = lp_opts(args.queue, "plain", args.slot, None, args.opt)
        cmd = lp_cmd(args.queue, pdf, "art-print 校准页", opts, args.hold)
        print("命令:", " ".join(f"'{c}'" if " " in c else c for c in cmd))
        if not args.apply:
            print("预演,没有发送。加 --apply 才发。")
            return 0
        print(run(cmd).stdout.strip())
    return 0


def main():
    p = argparse.ArgumentParser(description="名画打印 v2:整页 A4 稿按固定设置发给打印机(默认 Epson 驱动队列)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--queue", choices=QUEUES, default="airprint", help="airprint = AirPrint 队列(默认,2026-10-28 起:驱动队列每 25 mm 出一条深线,AirPrint 没有);driver = Epson 驱动队列(做实验用)")
        sp.add_argument("--slot", choices=DRV_SLOTS, help="进纸口,默认 rear(背面)")
        sp.add_argument("--opt", action="append", help="额外 -o 选项 KEY=VAL(可多次),用来做实验,例如 --opt EPIJ_Qual=355")
        sp.add_argument("--apply", action="store_true", help="真的发送(默认只预演)")
        sp.add_argument("--hold", action="store_true", help="发成暂停任务,不出纸,用来核对选项")

    sub.add_parser("check", help="打印前体检").add_argument("--queue", choices=QUEUES, default="airprint")
    sub.choices["check"].set_defaults(fn=cmd_check)
    c = sub.add_parser("calib", help="普通纸校准页")
    common(c)
    c.add_argument("--out", help="把校准页 PDF 另存一份")
    c.set_defaults(fn=cmd_calib)
    s = sub.add_parser("send", help="发打印稿")
    s.add_argument("file")
    s.add_argument("--paper", choices=DRV_PAPERS, required=True)
    common(s)
    s.add_argument("--quality", help="覆盖画质:驱动队列给 EPIJ_Qual 值(354 标准 / 355 きれい / 360 最高),AirPrint 给 Normal/High")
    s.add_argument("--log", help="打印记录 jsonl,默认写在稿件同目录")
    s.set_defaults(fn=cmd_send)
    args = p.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
