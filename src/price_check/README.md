# price_check

煤炉商品比价的数据脚本,给 skill `/home-assets:mercari-price-check` 用。只读:不登录、不下单。

| 文件 | 用途 |
|---|---|
| `price_check.py` | 子命令 `item`(煤炉商品详情,匿名 API + DPoP 签名)、`comps`(煤炉同款成交 `--sold` / 在售)、`kakaku`(価格.com 价格历史)、`yahoo`(Yahoo!ショッピング 新品价)、`report`(四项一起,输出 JSON) |

```
uv run -q --script src/price_check/price_check.py report m73648709458 \
  --kw "DJI Mini 4 Pro" --must "Mini 4 Pro|mini4pro" --kakaku K0001576074 --min 40000
```

- `--must`:标题里必须连续出现的短语(`|` 分隔),滤掉搜索混进来的别的商品。
- 楽天 / Amazon 反爬,不抓;由 skill 用 WebSearch 或浏览器补。
- 依赖 `cryptography`(uv 自动装)。
