# art_fetch — 名画原图下载与资料整理

skill `/art-fetch`(`.claude/skills/art-fetch/SKILL.md`)调用本脚本来执行,调研部分由 Claude 完成。

## 目录结构说明

| 路径 | 用途 |
|---|---|
| `src/art_fetch/art_fetch.py` | 脚本:`search` 在 Commons 搜候选图,`info` 查尺寸和授权,`build` 按清单建目录、下载原图、写资料、重建索引 |
| `src/art_fetch/README.md` | 本说明 |
| `.claude/skills/art-fetch/SKILL.md` | skill 定义:流程、选图优先级、清单 schema、权限边界 |
| `home design/名画库/` | 名画库根目录(数据,默认值;可用 `--root` 改) |
| `名画库/总目录.md` | 各作者按技法统计的件数(自动生成) |
| `名画库/_manifests/<作者>.json` | 作品清单,也就是调研结果;`build` 以它为输入 |
| `名画库/_trash/` | 索引重建时替换下来的旧版 |
| `名画库/<作者>/README.md` | 作者简介、各技法件数、按年份排列的作品表(自动生成) |
| `名画库/<作者>/作品清单.csv` | 同上的表格版,带 BOM,可以直接用 Excel 打开(自动生成) |
| `名画库/<作者>/<技法>/<年份>_<作品>/原图.*` | 下载到的最大分辨率原图,已存在就不覆盖 |
| `…/预览.jpg` | 原图是 TIFF 或超过 30 MB 时生成的 2000px 预览 |
| `…/资料.md` | 这件作品的资料:馆藏、编号、尺寸、工艺、摘要、故事、过往展出、未来展出、授权、来源 |
| `…/作品.json` | 机器可读的完整字段,另含下载记录(尺寸、SHA-256) |

## 用法

```bash
PY=/opt/homebrew/bin/python3
$PY src/art_fetch/art_fetch.py search "Turner Fighting Temeraire"
$PY src/art_fetch/art_fetch.py info "File:The Fighting Temeraire, JMW Turner, National Gallery.jpg"
$PY src/art_fetch/art_fetch.py build "home design/名画库/_manifests/透纳_J.M.W.Turner_1775-1851.json" --only 1 3 5
```
