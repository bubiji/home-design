# /// script
# requires-python = ">=3.10"
# dependencies = ["cryptography"]
# ///
"""煤炉商品比价:目标商品详情 + 煤炉同款成交/在售 + 価格.com 价格历史 + Yahoo!ショッピング 新品价。

只读,不登录、不下单。skill /home-assets:mercari-price-check 调用它取数据,判断与租赁比较由模型完成。

用法:
  uv run -q --script src/price_check/price_check.py item m73648709458
  uv run -q --script src/price_check/price_check.py comps "DJI Mini 4 Pro" --sold --min 40000 --exclude "ジャンク ケース"
  uv run -q --script src/price_check/price_check.py kakaku K0001576074
  uv run -q --script src/price_check/price_check.py yahoo "DJI Mini 4 Pro" --min 60000
  uv run -q --script src/price_check/price_check.py report <煤炉URL或ID> --kw "DJI Mini 4 Pro" [--kakaku K...] [--min 40000] [--exclude "..."]
"""
import argparse
import base64
import html
import json
import re
import statistics
import sys
import time
import urllib.parse
import urllib.request
import unicodedata
import uuid

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
COND = {1: "新品未使用", 2: "未使用に近い", 3: "目立った傷なし", 4: "やや傷", 5: "傷汚れあり", 6: "全体的に悪い"}


# ---------- 煤炉 API(网页版同款 DPoP 签名,匿名) ----------

_KEY = ec.generate_private_key(ec.SECP256R1())


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _dpop(url: str, method: str) -> str:
    pn = _KEY.public_key().public_numbers()
    jwk = {"crv": "P-256", "kty": "EC", "x": _b64(pn.x.to_bytes(32, "big")), "y": _b64(pn.y.to_bytes(32, "big"))}
    head = {"typ": "dpop+jwt", "alg": "ES256", "jwk": jwk}
    body = {"iat": int(time.time()), "jti": str(uuid.uuid4()), "htu": url, "htm": method, "uuid": str(uuid.uuid4())}
    si = _b64(json.dumps(head, separators=(",", ":")).encode()) + "." + _b64(json.dumps(body, separators=(",", ":")).encode())
    r, s = decode_dss_signature(_KEY.sign(si.encode(), ec.ECDSA(hashes.SHA256())))
    return si + "." + _b64(r.to_bytes(32, "big") + s.to_bytes(32, "big"))


def _mercari(url: str, method: str = "GET", body=None):
    req = urllib.request.Request(
        url, method=method, data=json.dumps(body).encode() if body else None,
        headers={"DPoP": _dpop(url, method), "X-Platform": "web", "Accept": "application/json",
                 "Content-Type": "application/json; charset=utf-8", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def item_id(s: str) -> str:
    m = re.search(r"(m\d{8,})", s)
    if not m:
        sys.exit(f"认不出煤炉商品 ID: {s}")
    return m.group(1)


def item(iid: str) -> dict:
    d = _mercari("https://api.mercari.jp/items/get?id=" + iid)["data"]
    sel = d.get("seller") or {}
    return {
        "id": iid, "url": f"https://jp.mercari.com/item/{iid}", "name": d.get("name"), "price": d.get("price"),
        "status": d.get("status"), "condition": (d.get("item_condition") or {}).get("name"),
        "shipping_payer": (d.get("shipping_payer") or {}).get("name"),
        "ship_from": (d.get("shipping_from_area") or {}).get("name"),
        "likes": d.get("num_likes"),
        "created": time.strftime("%Y-%m-%d", time.localtime(d.get("created", 0))),
        "photos": len(d.get("photos") or []),
        "description": d.get("description"),
        "seller": {"id": sel.get("id"), "name": sel.get("name"), "ratings": sel.get("num_ratings"),
                   "good": (sel.get("ratings") or {}).get("good"), "bad": (sel.get("ratings") or {}).get("bad"),
                   "listings": sel.get("num_sell_items"), "official_shop": sel.get("is_official"),
                   "since": time.strftime("%Y-%m", time.localtime(sel.get("created", 0)))},
    }


def comps(kw: str, sold: bool, min_price: int = 0, max_price: int = 0, exclude: str = "", must: str = "") -> list:
    body = {"pageSize": 120, "searchSessionId": uuid.uuid4().hex,
            "searchCondition": {"keyword": kw, "excludeKeyword": exclude,
                                "status": ["STATUS_SOLD_OUT" if sold else "STATUS_ON_SALE"],
                                "sort": "SORT_CREATED_TIME", "order": "ORDER_DESC",
                                "priceMin": min_price or 0, "priceMax": max_price or 0},
            "defaultDatasets": ["DATASET_TYPE_MERCARI", "DATASET_TYPE_BEYOND"], "serviceFrom": "suruga",
            "withItemBrand": False, "withItemSize": False, "withItemPromotions": False,
            "withItemSizes": False, "withShopname": False}
    r = _mercari("https://api.mercari.jp/v2/entities:search", "POST", body)
    out = []
    for it in r.get("items", []):
        name = it.get("name", "")
        if not _match(name, must or kw):
            continue  # 搜索会混入别的商品,标题里必须连续含关键词短语
        p = int(it["price"])
        if min_price and p < min_price:
            continue
        iid = it["id"]
        out.append({"price": p, "cond": COND.get(int(it.get("itemConditionId") or 0), "?"),
                    "date": time.strftime("%Y-%m-%d", time.localtime(int(it.get("updated") or 0))),
                    "shop": not iid.startswith("m"), "name": name[:70],
                    "url": f"https://jp.mercari.com/item/{iid}" if iid.startswith("m") else f"https://jp.mercari.com/shops/product/{iid}"})
    return out


def _squash(s: str) -> str:
    return re.sub(r"[\s\-_・]", "", unicodedata.normalize("NFKC", s or "").lower())


def _match(name: str, must: str) -> bool:
    """must 用 | 分隔多个短语,任一短语(去空格后)连续出现在标题里即算命中。"""
    t = _squash(name)
    return any(_squash(p) in t for p in must.split("|") if p.strip())


def stats(rows: list) -> dict:
    ps = [r["price"] for r in rows]
    if not ps:
        return {"n": 0}
    return {"n": len(ps), "min": min(ps), "median": int(statistics.median(ps)), "max": max(ps)}


# ---------- 価格.com ----------

def _get(url: str, enc: str = "utf-8") -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode(enc, "ignore")


def _text(s: str) -> str:
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))


def kakaku(code: str) -> dict:
    t = _text(_get(f"https://kakaku.com/item/{code}/pricehistory/", "cp932"))
    title = re.search(r"価格\.com - (.+?) 価格推移グラフ", t)
    first = re.search(r"初値 現在の最安値 差額 値下がり率 (¥[\d,]+|‐) （(.+?)） (¥[\d,]+|‐)", t)
    days = re.findall(r"(\d{4}年\s*\d+月\s*\d+日) (¥[\d,]+)", t)
    return {"code": code, "url": f"https://kakaku.com/item/{code}/pricehistory/",
            "title": title.group(1) if title else None,
            "first_price": first.group(1) if first else None, "first_month": first.group(2) if first else None,
            "current_min": first.group(3) if first else None,
            "recent_daily": days[:10],
            "note": "current_min 为 ‐ 表示现在没有店铺报价(多半新品已断货/停售);Amazon 不计入価格.com 历史"}


# ---------- Yahoo!ショッピング ----------

def yahoo(kw: str, min_price: int = 0, max_price: int = 0, must: str = "") -> list:
    q = {"p": kw, "X": "2"}
    if min_price:
        q["pf"] = str(min_price)
    if max_price:
        q["pt"] = str(max_price)
    s = _get("https://shopping.yahoo.co.jp/search?" + urllib.parse.urlencode(q))
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', s, re.S)
    if not m:
        return []
    found, seen = [], set()

    def walk(o):
        if isinstance(o, dict):
            if "name" in o and isinstance(o.get("price"), (int, float)):
                found.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(json.loads(m.group(1)))
    out = []
    for o in found:
        name = str(o["name"])
        if not _match(name, must or kw):
            continue
        key = (o["price"], name)
        if key in seen:
            continue
        seen.add(key)
        store = o.get("store") if isinstance(o.get("store"), dict) else {}
        out.append({"price": int(o["price"]), "store": store.get("name"), "name": name[:80],
                    "url": (o.get("url") or "").split("?")[0]})
    return sorted(out, key=lambda r: r["price"])


# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("item"); a.add_argument("id")
    a = sub.add_parser("comps"); a.add_argument("kw"); a.add_argument("--sold", action="store_true")
    a.add_argument("--min", type=int, default=0); a.add_argument("--max", type=int, default=0)
    a.add_argument("--exclude", default=""); a.add_argument("--must", default="")
    a = sub.add_parser("kakaku"); a.add_argument("code")
    a = sub.add_parser("yahoo"); a.add_argument("kw"); a.add_argument("--min", type=int, default=0)
    a.add_argument("--max", type=int, default=0); a.add_argument("--must", default="")
    a = sub.add_parser("report"); a.add_argument("id"); a.add_argument("--kw", required=True)
    a.add_argument("--kakaku", default=""); a.add_argument("--min", type=int, default=0)
    a.add_argument("--exclude", default="ジャンク 部品 ケース プロペラ フィルター バッテリーのみ")
    a.add_argument("--must", default="")
    x = ap.parse_args()

    if x.cmd == "item":
        res = item(item_id(x.id))
    elif x.cmd == "comps":
        rows = comps(x.kw, x.sold, x.min, x.max, x.exclude, x.must)
        res = {"stats": stats(rows), "items": rows}
    elif x.cmd == "kakaku":
        res = kakaku(x.code)
    elif x.cmd == "yahoo":
        res = yahoo(x.kw, x.min, x.max, x.must)
    else:
        sold = comps(x.kw, True, x.min, 0, x.exclude, x.must)
        on = comps(x.kw, False, x.min, 0, x.exclude, x.must)
        res = {"target": item(item_id(x.id)),
               "mercari_sold": {"stats": stats(sold), "items": sold[:30]},
               "mercari_on_sale": {"stats": stats(on), "items": on[:30]},
               "kakaku": kakaku(x.kakaku) if x.kakaku else None,
               "yahoo_new": yahoo(x.kw, x.min, 0, x.must)[:15]}
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
