#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""名画打印:把排好的整页 A4 稿按固定设置发给打印机(零依赖,只用系统自带的 lp / lpstat / ipptool / sips)。

  check                      打印前体检:队列、纸型、墨量、打印机状态
  calib [--apply]            普通纸校准页:100 mm 标尺 + 可印范围框,用来量缩放、看哪一面出墨
  send <文件> --paper <纸>   发打印稿;默认只预演,--apply 才真的发;--hold 发成暂停任务(不出纸)

稿件必须是整页 A4(图已按实际尺寸摆在页面里),这里一律按 100% 发,不缩放。说明见 README.md。
"""
import argparse, datetime, json, pathlib, re, subprocess, sys, tempfile

QUEUE = "EPSON_EW_M873T"          # CUPS 队列名;地址由队列自己记,不在这里写 IP
A4_MM = (210.0, 297.0)
# 纸 → (MediaType, cupsPrintQuality, 默认进纸口, 说明)
PAPERS = {
    "velvet": ("Com.epsonVelvetFineArt", "High", "Rear", "Epson Velvet Fine Art Paper"),
    "matte": ("PhotographicMatte", "High", "Rear", "フォトマット紙"),
    "plain": ("Stationery", "Normal", "Rear", "普通纸(演练用)"),
}
SLOTS = {"rear": "Rear", "main": "Main", "manual": "Manual"}


def run(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if check and r.returncode:
        sys.exit(f"命令失败: {' '.join(map(str, cmd))}\n{r.stderr.strip() or r.stdout.strip()}")
    return r


def device_uri():
    out = run(["lpstat", "-v", QUEUE], check=False).stdout
    m = re.search(r"(ipps?://\S+)", out)
    if not m:
        sys.exit(f"找不到打印队列 {QUEUE}(lpstat -v 无结果)。先在「系统设置 → 打印机」里加上。")
    return m.group(1)


def printer_attrs():
    """向打印机要属性(只读)。返回 {属性名: 原始字符串}。"""
    out = run(["ipptool", "-tv", device_uri(), "get-printer-attributes.test"], check=False).stdout
    attrs = {}
    for line in out.splitlines():
        m = re.match(r"\s+([\w-]+) \([^)]*\) = (.*)", line)
        if m:
            attrs[m.group(1)] = m.group(2)
    return attrs


def queue_choices(option):
    out = run(["lpoptions", "-p", QUEUE, "-l"]).stdout
    for line in out.splitlines():
        if line.startswith(option + "/"):
            return [c.lstrip("*") for c in line.split(":", 1)[1].split()]
    return []


def cmd_check(_):
    a = printer_attrs()
    if not a:
        sys.exit("打印机没应答(ipptool 无输出)。检查电源和网络。")
    ok = True
    print(f"队列 {QUEUE} → {a.get('printer-make-and-model', '?')},状态 {a.get('printer-state', '?')} / {a.get('printer-state-reasons', '?')}")
    names = a.get("marker-names", "").split(",")
    levels = [int(x) for x in a.get("marker-levels", "").split(",") if x.strip().lstrip("-").isdigit()]
    lows = [int(x) for x in a.get("marker-low-levels", "").split(",") if x.strip().isdigit()]
    for n, lv, lo in zip(names, levels, lows):
        flag = "  ← 到低位线" if lv <= lo else ""
        ok &= lv > lo
        print(f"  墨 {n:>2}: {lv:>3}%  (低位线 {lo}%){flag}")
    print("  注:墨量是打印机按用量估的,以墨仓窗口实际液位为准。")
    types = queue_choices("MediaType")
    for key, (mt, _, _, label) in PAPERS.items():
        have = mt in types
        ok &= have
        print(f"  纸型 {key:<6} {label}: {'有' if have else '队列里没有 ' + mt}")
    print(f"  进纸口: {', '.join(queue_choices('InputSlot'))}")
    print(f"  有边模式边距(1/100 mm): 上 {a.get('media-top-margin-supported')} 下 {a.get('media-bottom-margin-supported')}")
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


def lp_cmd(pdf, paper, slot, quality, title, hold):
    mt, q, default_slot, _ = PAPERS[paper]
    cmd = ["lp", "-d", QUEUE, "-t", title,
           "-o", "media=iso_a4_210x297mm", "-o", f"InputSlot={SLOTS[slot] if slot else default_slot}",
           "-o", f"MediaType={mt}", "-o", f"cupsPrintQuality={quality or q}",
           "-o", "print-scaling=none", "-o", "ColorModel=RGB"]
    if hold:
        cmd += ["-H", "hold"]
    return cmd + [str(pdf)]


def submit(src, pdf, args, extra=None):
    cmd = lp_cmd(pdf, args.paper, args.slot, args.quality, pathlib.Path(src).stem, args.hold)
    print("命令:", " ".join(f"'{c}'" if " " in c else c for c in cmd))
    if not args.apply:
        print("预演,没有发送。加 --apply 才发;加 --hold 发成暂停任务(不出纸)。")
        return 0
    out = run(cmd).stdout.strip()
    print(out)
    m = re.search(rf"({QUEUE}-\d+)", out)
    rec = {"time": datetime.datetime.now().isoformat(timespec="seconds"), "file": str(src), "paper": args.paper,
           "media_type": PAPERS[args.paper][0], "slot": args.slot or PAPERS[args.paper][2].lower(),
           "quality": args.quality or PAPERS[args.paper][1], "hold": args.hold, "job": m.group(1) if m else ""}
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
        print(f"纸: {PAPERS[args.paper][3]}")
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
        print("校准页:普通纸,量两条 100 mm 标尺、看四条边框是否都在、记下哪一面出墨。")
        args.hold = getattr(args, "hold", False)
        cmd = lp_cmd(pdf, "plain", args.slot, None, "art-print 校准页", args.hold)
        print("命令:", " ".join(f"'{c}'" if " " in c else c for c in cmd))
        if not args.apply:
            print("预演,没有发送。加 --apply 才发。")
            return 0
        print(run(cmd).stdout.strip())
    return 0


def main():
    p = argparse.ArgumentParser(description="名画打印:整页 A4 稿按固定设置发给打印机")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="打印前体检").set_defaults(fn=cmd_check)
    c = sub.add_parser("calib", help="普通纸校准页")
    c.add_argument("--slot", choices=SLOTS, default="rear")
    c.add_argument("--apply", action="store_true")
    c.add_argument("--hold", action="store_true")
    c.add_argument("--out", help="把校准页 PDF 另存一份")
    c.set_defaults(fn=cmd_calib)
    s = sub.add_parser("send", help="发打印稿")
    s.add_argument("file")
    s.add_argument("--paper", choices=PAPERS, required=True)
    s.add_argument("--slot", choices=SLOTS)
    s.add_argument("--quality", choices=["Normal", "High"])
    s.add_argument("--apply", action="store_true", help="真的发送(默认只预演)")
    s.add_argument("--hold", action="store_true", help="发成暂停任务,不出纸,用来核对选项")
    s.add_argument("--log", help="打印记录 jsonl,默认写在稿件同目录")
    s.set_defaults(fn=cmd_send)
    args = p.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
