#!/usr/bin/env python3
"""名画原图下载与资料整理(/art-fetch 的实现)。零依赖,只用标准库 + macOS sips。

子命令:
  search <关键词>          在 Wikimedia Commons 搜图,按分辨率列候选
  info   <File:标题>       看某个 Commons 文件的原图尺寸、授权
  build  <manifest.json>   按清单建目录、下载原图、写 资料.md / 作品.json、重建索引

目录:<root>/<作者>/<技法>/<年份>_<中文名>/{原图.<ext>, 预览.jpg, 资料.md, 作品.json}
规则:已存在的原图/资料一律不覆盖;资料有变化另存 资料_<日期>.md;
     重建的索引文件(作品清单.csv、README.md、总目录.md)若内容变化,旧版先移入 <root>/_trash/。
"""
import argparse, csv, hashlib, io, json, re, shutil, subprocess, sys, time
import urllib.error, urllib.parse, urllib.request
from datetime import date, datetime
from pathlib import Path

UA = {"User-Agent": "art-fetch/0.1 (personal non-commercial art archive; low volume) python-urllib"}
API = "https://commons.wikimedia.org/w/api.php"
DEFAULT_ROOT = Path(__file__).resolve().parents[2] / "home design" / "名画库"
TECH_ORDER = ["油画", "水彩", "素描", "版画", "其他"]


def _get(url, timeout=60, tries=5):
    """带退避的 GET:Wikimedia 限流(429/503)时按 Retry-After 或指数退避重试。"""
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or i == tries - 1:
                raise
            wait = int(e.headers.get("Retry-After") or 0) or 5 * 2 ** i
            print(f"   限流 {e.code},{wait}s 后重试", file=sys.stderr); time.sleep(min(wait, 120))
    raise RuntimeError("unreachable")


def api(**p):
    p["format"] = "json"
    with _get(API + "?" + urllib.parse.urlencode(p)) as r:
        return json.load(r)


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def commons_info(title):
    title = title if title.startswith("File:") else "File:" + title
    r = api(action="query", titles=title, prop="imageinfo", iiprop="url|size|mime|extmetadata")
    page = next(iter(r["query"]["pages"].values()))
    if "imageinfo" not in page:
        raise LookupError(f"Commons 上没有这个文件: {title}")
    ii = page["imageinfo"][0]
    md = ii.get("extmetadata", {})
    return {
        "title": page["title"], "url": ii["url"], "page": ii.get("descriptionurl", ""),
        "width": ii["width"], "height": ii["height"], "bytes": ii.get("size", 0), "mime": ii.get("mime", ""),
        "license": strip_html(md.get("LicenseShortName", {}).get("value", "")),
        "license_url": md.get("LicenseUrl", {}).get("value", ""),
    }


def cmd_search(a):
    r = api(action="query", generator="search", gsrsearch=a.query + " filetype:bitmap",
            gsrnamespace=6, gsrlimit=a.limit, prop="imageinfo", iiprop="size")
    pages = sorted(r.get("query", {}).get("pages", {}).values(), key=lambda p: -p["imageinfo"][0]["width"])
    for p in pages:
        ii = p["imageinfo"][0]
        print(f"{ii['width']:>6}x{ii['height']:<6} {ii.get('size', 0) // 1024:>7}KB  {p['title']}")


def cmd_info(a):
    print(json.dumps(commons_info(a.title), ensure_ascii=False, indent=2))


def safe(name, n=60):
    name = re.sub(r'[\\/:*?"<>|\n\r\t]', "", name).strip()
    return name[:n]


def download(url, dest):
    """下到 .part 再改名;已存在则跳过。返回 (是否新下载, sha256)。"""
    if dest.exists():
        return False, sha256(dest)
    part = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(3):
        try:
            with _get(url, timeout=300) as r, open(part, "wb") as f:
                shutil.copyfileobj(r, f, 1 << 20)
            break
        except Exception as e:  # 网络抖动重试
            if attempt == 2:
                raise
            print(f"   重试({e})"); time.sleep(3)
    part.rename(dest)
    time.sleep(3)  # 对 upload.wikimedia.org 保持低频,避免触发批量限流
    return True, sha256(dest)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def make_preview(src, dest, px=2000):
    if dest.exists():
        return
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85", "-Z", str(px),
                    str(src), "--out", str(dest)], check=True, capture_output=True)


def write_versioned(path, text, trash):
    """资料类:不存在就写;内容相同跳过;不同则另存 <名>_<日期>.md,原文件不动。"""
    if not path.exists():
        path.write_text(text, encoding="utf-8"); return path
    if path.read_text(encoding="utf-8") == text:
        return None
    alt = path.with_name(f"{path.stem}_{date.today():%Y%m%d}{path.suffix}")
    alt.write_text(text, encoding="utf-8"); return alt


def write_index(path, text, trash):
    """索引类(可重生成):内容变化时旧版移入 _trash/ 再写新版。"""
    if path.exists():
        if path.read_text(encoding="utf-8") == text:
            return
        trash.mkdir(parents=True, exist_ok=True)
        rel = str(path.relative_to(trash.parent)).replace("/", "__")
        shutil.move(str(path), trash / f"{datetime.now():%Y%m%d-%H%M%S}__{rel}")
    path.write_text(text, encoding="utf-8")


def bullets(xs):
    return "\n".join(f"- {x}" for x in xs) if xs else "- 未查到"


def render_md(w, author, img, article):
    v = lambda k: w.get(k) or "未查到"
    star = " ★" if w.get("favorite") else ""
    if img:
        img_block = (f"- 文件:`{img['file']}`({img['width']}×{img['height']} px,{img['bytes'] / 1e6:.1f} MB)\n"
                     f"- 来源:{img['source_page'] or img['url']}\n- 授权:{img['license'] or '未查到'}"
                     f"{(' — ' + img['license_url']) if img.get('license_url') else ''}\n- SHA-256:`{img['sha256']}`")
    else:
        img_block = f"- 未下载:{w.get('image', {}).get('note') or '没有找到公有领域的高清原图'}"
    return f"""# {v('title_zh')}{star}

**{v('title_en')}**　/　日文:{v('title_ja')}

| 项目 | 内容 |
|---|---|
| 作者 | {author.get('name_zh', author.get('dir', ''))}({author.get('name_en', '')},{author.get('life', '')}) |
| 创作年份 | {v('year')} |
| 技法 | {v('technique')}　/　{v('medium')} |
| 尺寸 | {v('dimensions')} |
| 现藏 | {v('museum')}({v('museum_city')}) |
| 馆藏编号 | {v('accession')} |
| 馆藏页面 | {v('museum_url')} |
| 是否有高清图 | {v('hd_available')} |
| 流行文化关联 | {'<br>'.join(w.get('culture_relation') or []) or '—'} |
| 我喜欢 | {('★ ' + (w.get('favorite_reason') or '')) if w.get('favorite') else '—'} |
| 《The Story of Art》 | {w.get('book_relation') or '未收录(按 1951 年英文初版插图目录核对)'} |
| 收录来源 | {(article + f"(文中第 {w['no']} 号)") if w.get('no') and article else ('Wikidata ' + w['qid'] + ' 全集收录' if w.get('qid') else (article or '—'))} |

## 摘要
{v('summary')}

## 作品故事
{v('story')}

## 工艺与技法
{v('technique_note')}

## 展出记录(过去)
{bullets(w.get('exhibited_history'))}

## 未来可能的展出
{bullets(w.get('exhibited_future'))}
{('> ' + w['future_note']) if w.get('future_note') else ''}

## 原图
{img_block}

## 权威链接(实测)
{chr(10).join(f"- {x['label']}:{x['url']}" + {200: '', 403: '(脚本访问被网站拦截,浏览器可打开)', 404: '(⚠ 实测 404,链接可能失效)'}.get(x['status'], f"(⚠ 实测连接失败:{x['status']})") + f"  _{x['checked']}_" for x in w.get('links') or []) or '- 未查'}

## 资料来源
{bullets(w.get('sources'))}

_整理于 {date.today():%Y-%m-%d},由 /art-fetch 生成。查不到的字段写「未查到」,不编造。_
"""


def cmd_build(a):
    m = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    root = Path(a.root).expanduser(); trash = root / "_trash"
    author = m["author"]; adir = root / safe(author["dir"], 80)
    rows = []
    # 全集清单:跳过同作者「__精选.json」里已有的作品(同一原图文件,或同名同年)
    norm = lambda s: re.sub(r"\W+", "", (s or "").lower())[:40]
    cur_files, cur_keys = set(), set()
    sel = Path(a.manifest).with_name(f"{author['dir']}__精选.json")
    if sel.exists() and Path(a.manifest).resolve() != sel.resolve():
        sm = json.loads(sel.read_text(encoding="utf-8"))
        author = {**sm["author"], **{k: v for k, v in author.items() if v}}  # 作者中文名/生卒/简介取精选清单
        for c in sm["works"]:
            cur_files.add((c.get("image") or {}).get("commons_file", "")); cur_keys.add((norm(c.get("title_en")), c.get("year_sort")))
    skipped = 0
    for w in sorted(m["works"], key=lambda w: (w.get("year_sort") or 0, w.get("no", 0))):
        if a.only and w.get("no") not in a.only:
            continue
        tech = w.get("technique") if w.get("technique") in TECH_ORDER else "其他"
        name = f"{w.get('year_sort') or '年代不详'}_{w.get('title_zh') or w.get('title_ja') or w.get('title_en') or w.get('qid')}"
        wdir = adir / tech / (safe(name, 70) + (f"_{w['qid']}" if w.get("qid") and not w.get("no") else ""))
        if not w.get("no") and ((w.get("image") or {}).get("commons_file") in cur_files
                                or (norm(w.get("title_en")) and (norm(w.get("title_en")), w.get("year_sort")) in cur_keys)):
            skipped += 1; continue  # 已被精选条目(文章/画墙/书)收录,不重复
        if a.skip_done and (wdir / "作品.json").exists() and not w.get("favorite"):
            continue
        wdir.mkdir(parents=True, exist_ok=True)
        im, img = w.get("image") or {}, None
        im = {k: ("" if v in ("未查到", "none", None) else v) for k, v in im.items()}
        print(f"[{w.get('no')}] {wdir.relative_to(root)}")
        url = src_page = lic = lic_url = ""
        try:
            if im.get("url"):  # harvest 已预取好 imageinfo,不再逐个查
                url, src_page, lic, lic_url = im["url"], im.get("page", ""), im.get("license", ""), im.get("license_url", "")
            elif im.get("commons_file"):
                ci = commons_info(im["commons_file"])
                if ci["bytes"] > 300e6 and not (wdir / "原图.jpg").exists():
                    raise RuntimeError(f"原图 {ci['bytes'] / 1e6:.0f} MB 超过 300 MB,需用户确认后再下(换较小版本或确认后重跑)")
                url, src_page, lic, lic_url = ci["url"], ci["page"], ci["license"], ci["license_url"]
            elif im.get("direct_url"):
                url, src_page, lic, lic_url = im["direct_url"], im.get("page", ""), im.get("license", ""), im.get("license_url", "")
            if url:
                ext = Path(urllib.parse.urlparse(url).path).suffix.lower() or ".jpg"
                dest = wdir / f"原图{ext}"
                new, digest = download(url, dest)
                print(f"   {'下载' if new else '已存在,跳过'} {dest.name} {dest.stat().st_size / 1e6:.1f} MB")
                out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(dest)],
                                     capture_output=True, text=True).stdout
                wpx, hpx = (int(x) for x in re.findall(r"pixel\w+: (\d+)", out))
                if ext not in (".jpg", ".jpeg") or dest.stat().st_size > 30e6:
                    make_preview(dest, wdir / "预览.jpg")
                img = {"file": dest.name, "url": url, "source_page": src_page, "license": lic, "license_url": lic_url,
                       "width": wpx, "height": hpx, "bytes": dest.stat().st_size, "sha256": digest}
        except Exception as e:
            print(f"   ✗ 原图失败:{e}")
            im["note"] = f"下载失败:{e}"
        md = wdir / "资料.md"; before = md.read_text(encoding="utf-8") if md.exists() else None
        write_index(md, render_md(w, author, img, m.get("source_article")), trash)  # 资料由清单生成:变化时旧版移入 _trash
        md = md if md.read_text(encoding="utf-8") != before else None
        if md:
            print(f"   写入 {md.name}")
        write_index(wdir / "作品.json", json.dumps({**w, "downloaded": img}, ensure_ascii=False, indent=2), trash)
        rows.append({"编号": w.get("no"), "喜欢": "★" if w.get("favorite") else "", "Story of Art": w.get("book_relation") or "", "年份": w.get("year"),
                     "中文名": w.get("title_zh"), "原名": w.get("title_en"), "技法": tech, "材质": w.get("medium"),
                     "现藏": w.get("museum"), "馆藏编号": w.get("accession"),
                     "原图": f"{img['width']}x{img['height']}" if img else "无", "授权": img["license"] if img else "",
                     "目录": str(wdir.relative_to(adir))})
    if skipped:
        print(f"跳过 {skipped} 件(精选里已有)")
    if not rows:
        return
    rebuild_author_index(adir, author, m, trash, rows)
    rebuild_root_index(root, trash)


def rebuild_author_index(adir, author, m, trash, new_rows):
    # 合并:目录里已有作品(作品.json)+ 本次清单
    rows = {}
    for j in adir.glob("*/*/作品.json"):
        w = json.loads(j.read_text(encoding="utf-8")); img = w.get("downloaded")
        rows[str(j.parent.relative_to(adir))] = {
            "编号": w.get("no"), "喜欢": "★" if w.get("favorite") else "", "Story of Art": w.get("book_relation") or "", "年份": w.get("year"),
            "中文名": w.get("title_zh"), "原名": w.get("title_en"), "技法": j.parent.parent.name,
            "材质": w.get("medium"), "现藏": w.get("museum"), "馆藏编号": w.get("accession"),
            "原图": f"{img['width']}x{img['height']}" if img else "无", "授权": img["license"] if img else "",
            "目录": str(j.parent.relative_to(adir))}
    for r in new_rows:
        rows[r["目录"]] = r
    rows = sorted(rows.values(), key=lambda r: r["目录"])
    buf = io.StringIO(); wr = csv.DictWriter(buf, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    write_index(adir / "作品清单.csv", "﻿" + buf.getvalue(), trash)
    count = {t: sum(r["技法"] == t for r in rows) for t in TECH_ORDER if any(r["技法"] == t for r in rows)}
    lines = [f"# {author.get('name_zh', author.get('dir', ''))}({author.get('name_en', '')},{author.get('life', '')})", "",
             author.get("bio", ""), "", "## 数量", "",
             "| 技法 | 件数 |", "|---|---|", *[f"| {t} | {n} |" for t, n in count.items()], f"| **合计** | **{len(rows)}** |",
             "", "## 作品(按年份)", "", "| 年份 | 作品 | 技法 | 现藏 | 原图 |", "|---|---|---|---|---|",
             *[f"| {r['年份']} | {r['喜欢']}[{r['中文名']}]({urllib.parse.quote(r['目录'])}/资料.md) | {r['技法']} | {r['现藏']} | {r['原图']} |" for r in sorted(rows, key=lambda r: r['目录'].split('/')[-1])],
             "", f"来源:{m.get('source_article', '')}", ""]
    write_index(adir / "README.md", "\n".join(lines), trash)


def rebuild_root_index(root, trash):
    lines = ["# 名画库总目录", "", "目录规则:`作者/技法/年份_作品名/`,每件作品含 原图、资料.md、作品.json。",
             "", "| 作者 | " + " | ".join(TECH_ORDER) + " | 合计 |", "|---|" + "---|" * (len(TECH_ORDER) + 1)]
    for adir in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("_")):
        c = [len(list((adir / t).glob("*/作品.json"))) for t in TECH_ORDER]
        lines.append(f"| [{adir.name}]({urllib.parse.quote(adir.name)}/README.md) | " + " | ".join(str(x or "") for x in c) + f" | {sum(c)} |")
    write_index(root / "总目录.md", "\n".join(lines) + "\n", trash)


SPARQL = "https://query.wikidata.org/sparql"
HARVEST_Q = """SELECT ?w ?img ?inc ?en ?ja ?zh ?col ?inv ?h ?wd
 (GROUP_CONCAT(DISTINCT ?tl;separator="|") AS ?types) (GROUP_CONCAT(DISTINCT ?ml;separator="|") AS ?mats) WHERE {
 ?w wdt:P170 wd:%s .
 OPTIONAL{?w wdt:P18 ?img} OPTIONAL{?w wdt:P571 ?inc}
 OPTIONAL{?w rdfs:label ?en FILTER(lang(?en)="en")} OPTIONAL{?w rdfs:label ?ja FILTER(lang(?ja)="ja")}
 OPTIONAL{?w rdfs:label ?zh FILTER(lang(?zh)="zh")}
 OPTIONAL{?w wdt:P195 ?c. ?c rdfs:label ?col FILTER(lang(?col)="en")} OPTIONAL{?w wdt:P217 ?inv}
 OPTIONAL{?w wdt:P2048 ?h} OPTIONAL{?w wdt:P2049 ?wd}
 OPTIONAL{?w wdt:P31 ?t. ?t rdfs:label ?tl FILTER(lang(?tl)="en")}
 OPTIONAL{?w wdt:P186 ?m. ?m rdfs:label ?ml FILTER(lang(?ml)="en")}
} GROUP BY ?w ?img ?inc ?en ?ja ?zh ?col ?inv ?h ?wd"""


def sparql(q):
    u = SPARQL + "?" + urllib.parse.urlencode({"query": q})
    req = urllib.request.Request(u, headers={**UA, "Accept": "application/sparql-results+json"})
    for i in range(8):  # WDQS 限流时每分钟只放 1 次
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.load(r)["results"]["bindings"]
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == 7:
                raise
            print("   WDQS 限流,65s 后重试", file=sys.stderr); time.sleep(65)
    return []


def classify(types, mats):
    t, m = types.lower(), mats.lower()
    if any(k in t for k in ("print", "woodcut", "etching", "engraving", "mezzotint", "lithograph", "ukiyo-e", "surimono")):
        return "版画"
    if "watercolor" in t or "watercolour" in t or "watercolor" in m or "gouache" in m:
        return "水彩"
    if "drawing" in t or "sketch" in t:
        return "素描"
    if "painting" in t or "oil paint" in m:
        return "油画" if ("oil" in m or not m) else "其他"
    return "其他"


def cmd_harvest(a):
    """按作者 QID 从 Wikidata 拉全部作品 → Commons 批量取原图信息 → 写全集清单。"""
    rows = sparql(HARVEST_Q % a.qid)
    items = {}
    for r in rows:  # 同一作品多行(多个标签/尺寸),合并成一条
        g = lambda k: r.get(k, {}).get("value", "")
        q = g("w").rsplit("/", 1)[-1]; it = items.setdefault(q, {"qid": q})
        for k in ("img", "inc", "en", "ja", "zh", "col", "inv", "h", "wd", "types", "mats"):
            if g(k) and not it.get(k):
                it[k] = g(k)
    with_img = [i for i in items.values() if i.get("img")]
    print(f"Wikidata:{len(items)} 件,有图 {len(with_img)} 件", file=sys.stderr)
    # Commons 批量 imageinfo(每次 50 个)
    title_of = lambda i: "File:" + urllib.parse.unquote(i["img"].rsplit("/", 1)[-1]).replace("_", " ")
    info = {}
    for k in range(0, len(with_img), 50):
        batch = [title_of(i) for i in with_img[k:k + 50]]
        r = api(action="query", titles="|".join(batch), prop="imageinfo", iiprop="url|size|extmetadata",
                iiextmetadatafilter="LicenseShortName|LicenseUrl")
        norm = {n["to"]: n["from"] for n in r["query"].get("normalized", [])}
        for p in r["query"]["pages"].values():
            if "imageinfo" in p:
                ii = p["imageinfo"][0]; md = ii.get("extmetadata", {})
                info[norm.get(p["title"], p["title"])] = {
                    "url": ii["url"], "page": ii.get("descriptionurl", ""), "width": ii["width"], "height": ii["height"],
                    "bytes": ii.get("size", 0), "license": strip_html(md.get("LicenseShortName", {}).get("value", "")),
                    "license_url": md.get("LicenseUrl", {}).get("value", "")}
        time.sleep(0.5)
    works, noimg = [], []
    for i in items.values():
        y = (re.match(r"[+-]?(\d{4})", i.get("inc", "")) or [None, None])[1]
        tech = classify(i.get("types", ""), i.get("mats", ""))
        w = {"qid": i["qid"], "title_en": i.get("en", ""), "title_ja": i.get("ja", ""), "title_zh": i.get("zh", ""),
             "year": y or "", "year_sort": int(y) if y else 0, "technique": tech,
             "medium": i.get("mats", "").replace("|", ", "), "types": i.get("types", ""),
             "dimensions": f"{i['h']} × {i['wd']} cm" if i.get("h") and i.get("wd") else "",
             "museum": i.get("col", ""), "accession": i.get("inv", ""),
             "museum_url": f"https://www.wikidata.org/wiki/{i['qid']}",
             "summary": "", "story": "", "technique_note": "", "exhibited_history": [], "exhibited_future": [],
             "sources": [f"https://www.wikidata.org/wiki/{i['qid']}"]}
        ii = info.get(title_of(i)) if i.get("img") else None
        if ii:
            w["image"] = {"source": "commons", "commons_file": title_of(i), **ii}; works.append(w)
        else:
            noimg.append(w)
    # 版画去重:同名同年多个馆藏印本只留像素最大的
    best = {}
    for w in works:
        key = (w["technique"], re.sub(r"\W+", "", (w["title_en"] or w["title_ja"] or w["qid"]).lower()), w["year"]) \
            if w["technique"] == "版画" else w["qid"]
        cur = best.get(key)
        if not cur or w["image"]["width"] * w["image"]["height"] > cur["image"]["width"] * cur["image"]["height"]:
            best[key] = w
    works = sorted(best.values(), key=lambda w: (w["year_sort"], w["title_en"]))
    total = sum(w["image"]["bytes"] for w in works)
    print(f"去重后有图 {len(works)} 件,约 {total / 1e9:.1f} GB;无图 {len(noimg)} 件", file=sys.stderr)
    out = Path(a.out)
    m = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {"author": {}, "works": []}
    m["author"].update({k: v for k, v in json.loads(a.author).items()} if a.author else {})
    m["source_article"] = m.get("source_article") or f"Wikidata 作者 {a.qid}"
    m["works"], m["no_image"] = works, noimg
    write_index(out, json.dumps(m, ensure_ascii=False, indent=1), out.parent / "_trash")


def cmd_favorites(a):
    """把 作品.json 里 favorite=true 的作品文件夹复制到另一个库(不覆盖已存在)。"""
    src, dst = Path(a.root).expanduser(), Path(a.to).expanduser(); n = 0
    for j in src.glob("*/*/*/作品.json"):
        w = json.loads(j.read_text(encoding="utf-8"))
        if not w.get("favorite"):
            continue
        rel = j.parent.relative_to(src); t = dst / rel
        t.mkdir(parents=True, exist_ok=True)
        for f in j.parent.iterdir():
            if not f.is_file() or f.name.startswith("原图_超高清"):  # 超大文件只留主库
                continue
            g = t / f.name
            if g.exists():
                same = g.stat().st_size == f.stat().st_size and (f.stat().st_size > 5e6 or g.read_bytes() == f.read_bytes())
                if same:
                    continue
                (dst / "_trash").mkdir(exist_ok=True)  # 内容变了:旧版移入 _trash 再复制
                shutil.move(str(g), dst / "_trash" / f"{datetime.now():%Y%m%d-%H%M%S}__{str(rel).replace('/', '__')}__{f.name}")
            shutil.copy2(f, g); n += 1
    print(f"复制 {n} 个文件到 {dst}")
    rebuild_root_index(dst, dst / "_trash")


def cmd_timeline(a):
    """所有 favorite 作品按年份排成一张表,写到主库和每个 --to 库的 喜欢作品年表.md。"""
    root = Path(a.root).expanduser(); rows = []
    for mf in root.glob("_manifests/*__精选.json"):
        m = json.loads(mf.read_text(encoding="utf-8")); au = m["author"]; adir = root / au["dir"]
        done = {}
        for j in adir.glob("*/*/作品.json"):
            d = json.loads(j.read_text(encoding="utf-8")); done[(d.get("no"), d.get("title_en"))] = (j.parent.relative_to(root), d.get("downloaded"))
        for w in m["works"]:
            if not w.get("favorite"):
                continue
            rel, dl = done.get((w.get("no"), w.get("title_en")), ("", None))
            soa = (w.get("book_relation") or "").replace("《The Story of Art》1951 英文初版 ", "").replace("——16 版编号未核对", "")
            song = "; ".join(r.split("——")[0] for r in w.get("culture_relation") or [])
            fut = "; ".join(x.split("(来源")[0] for x in w.get("exhibited_future") or [])
            link = f"[{w.get('title_zh') or w.get('title_en')}]({urllib.parse.quote(str(rel))}/资料.md)" if rel else w.get("title_zh", "")
            rows.append((w.get("year_sort") or 9999, f"| {w.get('year') or '?'} | {au.get('name_zh', au['dir'])} | {link} | {w.get('technique', '')} | "
                         f"{w.get('favorite_reason', '')} | {soa} | {song} | {w.get('museum', '')} | {'✓' if dl else '✗ 无图'} | {fut} |", bool(dl)))
    rows.sort(key=lambda r: r[0])
    text = "\n".join(["# 我喜欢的作品·年表", "",
                      "按创作年份排列,方便对照《The Story of Art》阅读(图号为 1951 英文初版,16 版未核对)。", "",
                      "| 年份 | 作者 | 作品 | 技法 | 为什么喜欢 | The Story of Art | 流行文化 | 现藏 | 原图 | 即将展出 |",
                      "|---|---|---|---|---|---|---|---|---|---|", *[r[1] for r in rows], "",
                      f"共 {len(rows)} 件,有原图 {sum(r[2] for r in rows)} 件。", ""])
    for d in [root, *[Path(t).expanduser() for t in a.to]]:
        write_index(d / "喜欢作品年表.md", text, d / "_trash")
    print(f"年表 {len(rows)} 件")


def cmd_culture(a):
    """按 culture_relation 汇总「流行文化里的名画」,每首歌/作品一节;_manifests/<名>_其他致敬.json 为非画作引用。"""
    root = Path(a.root).expanduser(); groups = {}
    for mf in root.glob("_manifests/*__精选.json"):
        m = json.loads(mf.read_text(encoding="utf-8")); au = m["author"]; done = {}
        for j in (root / au["dir"]).glob("*/*/作品.json"):
            d = json.loads(j.read_text(encoding="utf-8")); done[(d.get("no"), d.get("title_en"))] = (j.parent.relative_to(root), d.get("downloaded"))
        for w in m["works"]:
            rels = [r for r in w.get("culture_relation") or [] if r.startswith(a.prefix)]
            first = {}
            for r in rels:  # 同一首歌多条关联合并成一行
                song = r.split(":")[0].split("MV")[0].strip()
                first.setdefault(song, []).append(r.split(":", 1)[1] if ":" in r else r)
            for song, hows in first.items():
                rel, dl = done.get((w.get("no"), w.get("title_en")), ("", None))
                soa = (w.get("book_relation") or "").replace("《The Story of Art》1951 英文初版 ", "").split("——")[0]
                groups.setdefault(song, []).append((w.get("year_sort") or 9999, w.get("year") or "?", au.get("name_zh", au["dir"]),
                    w.get("title_zh") or w.get("title_en"), str(rel), "✓" if dl else "✗ " + ((w.get("image") or {}).get("note") or "")[:24],
                    ";".join(hows), w.get("museum", ""), soa))
    others = {}
    for of in root.glob(f"_manifests/{a.prefix}*_其他致敬.json"):
        others.update(json.loads(of.read_text(encoding="utf-8")))
    for d in [root, *[Path(t).expanduser() for t in a.to]]:
        L = [f"# {a.title}", "", "按歌曲分组、创作年份排序。「出现方式」里的置信度 = 有几篇解析提到;只描述画面,不引用歌词。", ""]
        for song, rows in sorted(groups.items()):
            L += [f"## {song}(共 {len(rows)} 件,有原图 {sum(r[5] == '✓' for r in rows)} 件,《The Story of Art》收录 {sum(bool(r[8]) for r in rows)} 件)", "",
                  "| 年份 | 作者 | 作品 | 出现方式 | 现藏 | The Story of Art | 原图 |", "|---|---|---|---|---|---|---|"]
            for r in sorted(rows):
                link = f"[{r[3]}]({urllib.parse.quote(r[4])}/资料.md)" if r[4] and (d / r[4]).exists() else r[3]
                L.append(f"| {r[1]} | {r[2]} | {link} | {r[6]} | {r[7]} | {r[8]} | {r[5]} |")
            if others.get(song):
                L += ["", f"### {song}:画作以外的致敬", "", "| 类型 | 名称 | 怎么出现 | 来源 |", "|---|---|---|---|",
                      *[f"| {o['type']} | {o['name']} | {o['how']} | {o.get('source', '')} |" for o in others[song]]]
            L.append("")
        write_index(d / f"{a.title}.md", "\n".join(L), d / "_trash")
    print({k: len(v) for k, v in groups.items()})


WD_API = "https://www.wikidata.org/w/api.php"
MUSEUM_HOSTS = ("louvre.fr", "musee-orsay.fr", "rijksmuseum.nl", "mauritshuis.nl", "nationalgallery.org.uk", "tate.org.uk", "moma.org",
                "metmuseum.org", "artic.edu", "nga.gov", "uffizi.it", "khm.at", "hermitagemuseum.org", "belvedere.at", "nasjonalmuseet.no",
                "smb.museum", "hamburger-kunsthalle.de", "philamuseum.org", "mfa.org", "skd.museum", "clevelandart.org", "vangoghmuseum.nl",
                "krollermuller.nl", "kunstmuseum.nl", "kunsthaus.ch", "phillipscollection.org", "nationalgalleries.org", "buffaloakg.org",
                "famsf.org", "neuegalerie.org", "mak.at", "arthermitage.org", "pushkinmuseum", "britishmuseum.org", "english-heritage.org.uk",
                "gallerieaccademia.it", "barberinicorsini.org", "museivaticani.va", "mczk.pl", "marmottan.fr", "courtauld.ac.uk", "nationalmuseum",
                "museoreinasofia", "museodelprado", "centrepompidou.fr", "guggenheim.org", "moca.org", "artsandculture.google.com")


def wd(**p):
    p["format"] = "json"
    with _get(WD_API + "?" + urllib.parse.urlencode(p)) as r:
        return json.load(r)


def check_url(u):
    """真实打开一次,返回 HTTP 状态码或错误类型。"""
    try:
        u = urllib.parse.quote(u, safe=":/?=&%#+,;@~")  # 非 ASCII 字符先编码
        req = urllib.request.Request(u, headers={**UA, "Accept": "text/html"}, method="GET")
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return type(e).__name__


_fmt_cache = {}


def ext_urls(claims):
    """外部 ID → 用属性的格式化 URL(P1630)拼出链接。"""
    out = []
    props = [p for p, cs in claims.items() if cs and cs[0]["mainsnak"].get("datatype") == "external-id"]
    need = [p for p in props if p not in _fmt_cache]
    for k in range(0, len(need), 50):
        ents = wd(action="wbgetentities", ids="|".join(need[k:k + 50]), props="claims|labels", languages="en")["entities"]
        for pid, e in ents.items():
            f = [c["mainsnak"].get("datavalue", {}).get("value") for c in e.get("claims", {}).get("P1630", [])]
            _fmt_cache[pid] = (f[0] if f else None, e.get("labels", {}).get("en", {}).get("value", pid))
    for p in props:
        fmt, label = _fmt_cache.get(p, (None, p))
        v = claims[p][0]["mainsnak"].get("datavalue", {}).get("value")
        if fmt and v:
            out.append((label, fmt.replace("$1", urllib.parse.quote(str(v), safe="/:"))))
    return out


def item_from_commons(cf):
    """Commons 文件的结构化数据:P6243(数字化再现于)/ P180(描绘)指向的 Wikidata 条目。"""
    try:
        r = api(action="query", titles=cf, prop="info")
        pid = next(iter(r["query"]["pages"].values())).get("pageid")
        if not pid:
            return None
        ent = api(action="wbgetentities", ids=f"M{pid}").get("entities", {}).get(f"M{pid}", {})
        for p in ("P6243", "P180"):
            for c in (ent.get("statements") or {}).get(p, []):
                q = c["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
                if q:
                    return q
    except Exception:
        return None
    return None


def find_item(w, artist_qid):
    """先看 Commons 原图的结构化数据;再按 英文名 / 英文名+作者 / 中文名 在 Wikidata 搜,取创作者对得上的条目。"""
    cf = (w.get("image") or {}).get("commons_file")
    q0 = item_from_commons(cf) if cf else None
    if q0:
        e = wd(action="wbgetentities", ids=q0, props="claims|sitelinks/urls", sitefilter="enwiki|zhwiki")["entities"].get(q0, {})
        if artist_qid in [c["mainsnak"].get("datavalue", {}).get("value", {}).get("id") for c in e.get("claims", {}).get("P170", [])]:
            return q0, e
    t = w.get("title_en") or ""
    for q in [t, t.split("(")[0].strip(), f"{t.split('(')[0].strip()} {w.get('_artist', '')}".strip(), w.get("title_zh")]:
        if not q:
            continue
        hits = wd(action="wbsearchentities", search=q, language="en", limit=10, type="item").get("search", [])
        if not hits:
            continue
        ents = wd(action="wbgetentities", ids="|".join(h["id"] for h in hits), props="claims|sitelinks/urls", sitefilter="enwiki|zhwiki")["entities"]
        for h in hits:
            e = ents.get(h["id"], {}); cl = e.get("claims", {})
            creators = [c["mainsnak"].get("datavalue", {}).get("value", {}).get("id") for c in cl.get("P170", [])]
            if artist_qid in creators:
                return h["id"], e
    return None, None


def cmd_links(a):
    """为作品找真实权威链接(馆方藏品页 / Wikidata / Wikipedia / Commons),逐个实测,写入清单 links 字段。"""
    root = Path(a.root).expanduser(); artist_cache = {}
    for mf in sorted(root.glob("_manifests/*__精选.json")):
        m = json.loads(mf.read_text(encoding="utf-8")); au = m["author"]; changed = False
        for w in m["works"]:
            if a.prefix and not any(r.startswith(a.prefix) for r in w.get("culture_relation") or []):
                continue
            if w.get("wikidata") and not a.refresh:  # 已匹配过的跳过;未匹配的每次重试
                continue
            name = au.get("name_en") or au["dir"]
            if name not in artist_cache:  # 作者 QID:清单里写了就用,否则按名字搜
                hs = [] if au.get("wikidata") else wd(action="wbsearchentities", search=name, language="en", limit=1, type="item").get("search", [])
                artist_cache[name] = au.get("wikidata") or (hs[0]["id"] if hs else None)
            qid, e = find_item({**w, "_artist": name}, artist_cache[name])
            links = []
            if qid and e:
                cl = e.get("claims", {})
                links.append(("Wikidata", f"https://www.wikidata.org/wiki/{qid}"))
                for c in cl.get("P973", []):  # described at URL
                    u = c["mainsnak"].get("datavalue", {}).get("value")
                    if u:
                        links.append(("描述页(P973)", u))
                for label, u in ext_urls(cl):
                    if any(h in u for h in MUSEUM_HOSTS):
                        links.append((label, u))
                for site, sl in (e.get("sitelinks") or {}).items():
                    links.append(({"enwiki": "Wikipedia(英)", "zhwiki": "维基百科(中)"}.get(site, site), sl["url"]))
            cf = (w.get("image") or {}).get("commons_file")
            if cf:
                links.append(("Commons 原图页", "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(cf.replace(" ", "_"))))
            seen, checked = set(), []
            for label, u in links:
                if u in seen:
                    continue
                seen.add(u); st = check_url(u); time.sleep(0.3)
                checked.append({"label": label, "url": u, "status": st, "checked": f"{date.today():%Y-%m-%d}"})
            w["links"] = checked; w["wikidata"] = qid or ""
            museum = [x for x in checked if any(h in x["url"] for h in MUSEUM_HOSTS) and x["status"] == 200]
            if museum and ("未核对" in (w.get("museum_url") or "") or w.get("museum_url") in ("", "未查到")):
                w["museum_url"] = museum[0]["url"]
            changed = True
            ok = sum(x["status"] == 200 for x in checked)
            print(f"{au['dir'][:12]} {w.get('no')} {w.get('title_zh')}: {qid or '未匹配'} 链接 {len(checked)} 条,可打开 {ok}", flush=True)
        if changed:
            mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--limit", type=int, default=10); s.set_defaults(f=cmd_search)
    s = sub.add_parser("info"); s.add_argument("title"); s.set_defaults(f=cmd_info)
    s = sub.add_parser("build"); s.add_argument("manifest"); s.add_argument("--root", default=str(DEFAULT_ROOT))
    s.add_argument("--only", type=int, nargs="*", help="只处理这些编号")
    s.add_argument("--skip-done", action="store_true", help="已有 作品.json 的非喜欢作品整条跳过(断点续跑)"); s.set_defaults(f=cmd_build)
    s = sub.add_parser("harvest"); s.add_argument("qid", help="作者的 Wikidata QID,如 Q159758")
    s.add_argument("--out", required=True); s.add_argument("--author", help="JSON:dir/name_zh/name_en/life/bio"); s.set_defaults(f=cmd_harvest)
    s = sub.add_parser("favorites"); s.add_argument("--root", default=str(DEFAULT_ROOT)); s.add_argument("--to", required=True)
    s.set_defaults(f=cmd_favorites)
    s = sub.add_parser("timeline"); s.add_argument("--root", default=str(DEFAULT_ROOT)); s.add_argument("--to", nargs="*", default=[])
    s.set_defaults(f=cmd_timeline)
    s = sub.add_parser("culture"); s.add_argument("--root", default=str(DEFAULT_ROOT)); s.add_argument("--to", nargs="*", default=[])
    s.add_argument("--prefix", required=True, help="culture_relation 前缀,如 周杰伦"); s.add_argument("--title", required=True)
    s.set_defaults(f=cmd_culture)
    s = sub.add_parser("links"); s.add_argument("--root", default=str(DEFAULT_ROOT)); s.add_argument("--prefix", default="", help="只处理 culture_relation 以此开头的作品")
    s.add_argument("--refresh", action="store_true"); s.set_defaults(f=cmd_links)
    a = ap.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
