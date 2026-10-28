#!/usr/bin/env python3
"""日语歌词 → A4 学习用 PDF:汉字上方自动标平假名(ruby),每行下方配中文(或留手写线)。

用法:
  python3 src/lyrics_ruby/make_lyrics_pdf.py 歌词.txt [--zh 中文.txt] [--title 标题] [--sub 副标题] [-o 输出.pdf]

输入约定:
  歌词.txt  一行一句,空行 = 段落分隔(UTF-8);读错的词可手动指定:始{はじ}ま
  中文.txt  可选,与歌词.txt 逐行对齐(空行位置一致);不给则每句下方留手写横线
注音用 fugashi + UniDic 自动生成,歌词里的特殊读法(当て字)需人工核对。
"""
import argparse, html, re, subprocess, sys
from pathlib import Path

import fugashi

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
KANJI = re.compile(r"[㐀-鿿々〆ヶ]")  # 含 々 〆 ヶ
_tagger = fugashi.Tagger()


def kata2hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def ruby_token(surface, reading):
    """把一个词拆成 [(文字, 读音或None)],读音只挂在汉字段上(送假名不注)。"""
    if not KANJI.search(surface) or not reading or reading == "*":
        return [(surface, None)]
    reading = kata2hira(reading)
    # 按 汉字段/假名段 切分,假名段作字面量,汉字段作捕获组去匹配读音
    parts = re.findall(r"[㐀-鿿々〆ヶ]+|[^㐀-鿿々〆ヶ]+", surface)
    pattern = "".join("(.+?)" if KANJI.match(p) else "(" + re.escape(kata2hira(p)) + ")" for p in parts)
    m = re.fullmatch(pattern, reading)
    if not m:
        return [(surface, reading)]
    return [(p, g if KANJI.match(p) else None) for p, g in zip(parts, m.groups())]


MANUAL = re.compile(r"([㐀-鿿々〆ヶ]+)\{([^}]+)\}")  # 手动注音:始{はじ}ま


def line_html(text):
    if MANUAL.search(text):
        out, pos = [], 0
        for m in MANUAL.finditer(text):
            out.append(line_html(text[pos:m.start()]))
            out.append(f"<ruby>{html.escape(m.group(1))}<rt>{html.escape(m.group(2))}</rt></ruby>")
            pos = m.end()
        out.append(line_html(text[pos:]))
        return "".join(out)
    out = []
    for w in _tagger(text):
        sp = " " * len(getattr(w, "white_space", "") or "")
        if sp:
            out.append("&ensp;")
        kana = getattr(w.feature, "kana", None)
        for seg, rd in ruby_token(w.surface, kana):
            if rd:
                out.append(f"<ruby>{html.escape(seg)}<rt>{html.escape(rd)}</rt></ruby>")
            else:
                out.append(html.escape(seg))
    return "".join(out)


CSS = """
@page { size: A4; margin: 12mm 16mm 12mm 16mm; }
* { box-sizing: border-box; }
body { margin: 0; color: #222; background: #fff;
  font-family: "Hiragino Mincho ProN", "Yu Mincho", serif; }
header { text-align: center; margin-bottom: 4mm; padding-bottom: 2mm; border-bottom: 0.6pt solid #b9a27a; }
h1 { font-size: 19pt; margin: 0; letter-spacing: 0.15em; font-weight: 600; }
.sub { font-size: 10pt; color: #8a7350; margin-top: 2mm; letter-spacing: 0.1em; }
.stanza { break-inside: avoid; margin: 0 0 3.5mm 0; padding-left: 4mm; border-left: 1.4pt solid #e3d6bd; }
.line { margin: 0 0 1.4mm 0; }
.jp { font-size: 12.5pt; line-height: 1.95; }
rt { font-size: 7pt; color: #9a6b2f; font-family: "Hiragino Kaku Gothic ProN", sans-serif; letter-spacing: 0; }
.zh { font-family: "Songti SC", "STSong", serif; font-size: 9.5pt; color: #4f5f73; line-height: 1.3; margin-top: -0.8mm; }
.blank { height: 6mm; border-bottom: 0.5pt dashed #c9c9c9; margin: -0.5mm 0 0 0; }
footer { margin-top: 6mm; font-size: 8pt; color: #aaa; text-align: right; }
"""


def build(lyrics, zh, title, sub):
    jp_lines = lyrics.splitlines()
    zh_lines = zh.splitlines() if zh is not None else None
    stanzas, cur = [], []
    for i, ln in enumerate(jp_lines):
        if not ln.strip():
            if cur:
                stanzas.append(cur); cur = []
            continue
        cn = zh_lines[i].strip() if zh_lines and i < len(zh_lines) else None
        cur.append((ln.strip(), cn))
    if cur:
        stanzas.append(cur)
    body = []
    for st in stanzas:
        rows = []
        for jp, cn in st:
            under = f'<div class="zh">{html.escape(cn)}</div>' if cn else ('<div class="blank"></div>' if zh_lines is None else "")
            rows.append(f'<div class="line"><div class="jp">{line_html(jp)}</div>{under}</div>')
        body.append('<section class="stanza">' + "".join(rows) + "</section>")
    sub_html = f'<div class="sub">{html.escape(sub)}</div>' if sub else ""
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>{html.escape(title)}</title>'
            f"<style>{CSS}</style></head><body><header><h1>{html.escape(title)}</h1>{sub_html}</header>"
            + "".join(body) + "<footer>振り仮名は自動生成 · 特殊な読みは要確認</footer></body></html>")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lyrics")
    ap.add_argument("--zh", help="逐行对齐的中文译文文件")
    ap.add_argument("--title", default=None)
    ap.add_argument("--sub", default="")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    src = Path(a.lyrics)
    title = a.title or src.stem
    zh = Path(a.zh).read_text(encoding="utf-8") if a.zh else None
    out = Path(a.out) if a.out else src.with_suffix(".pdf")
    if out.exists():  # 不覆盖已有文件,自动加版本后缀
        n = 2
        while (alt := out.with_name(f"{out.stem}_v{n}{out.suffix}")).exists():
            n += 1
        out = alt
    page = out.with_suffix(".html")
    page.write_text(build(src.read_text(encoding="utf-8"), zh, title, a.sub), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out.resolve()}", page.resolve().as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"PDF: {out}\nHTML: {page}")
    if not a.no_open:
        subprocess.run(["open", str(out)])


if __name__ == "__main__":
    sys.exit(main())
