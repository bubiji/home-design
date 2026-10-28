# lyrics_ruby — 日语歌词注音学习 PDF

| 文件 | 用途 |
|---|---|
| `make_lyrics_pdf.py` | 歌词 txt → A4 PDF:汉字上方自动标平假名(fugashi + UniDic),每句下方配中文译文;不给译文则留手写虚线。Chrome 无头打印,输出已存在时自动加 `_v2` 后缀不覆盖 |

```bash
python3 src/lyrics_ruby/make_lyrics_pdf.py 歌词.txt --zh 中文.txt --title "曲名" --sub "歌手"
```

- 歌词.txt:一行一句,空行分段;中文.txt 与之逐行对齐(可省略 → 手写线)
- 数词连读(如 一歩=いっぽ)、当て字等特殊读音会按字面读,打印前请核对

- 手动注音语法:歌词里写 `始{はじ}ま`,该词按指定读音标注(自动读错时用)
- 成品放 `assets/lyrics_ruby/<曲名>/`(歌词 txt、中文 txt、PDF、HTML)
