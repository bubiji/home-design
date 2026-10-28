#!/bin/zsh
# 等 hd1 挂载 → ①把 画框之外 / 太阳之子 作品标为喜欢 ②_trash 存档到 hd1 并逐个校验,全部一致才从内置盘移除 ③续跑下载+生成资料+同步+索引
I="$(cd "$(dirname "$0")/.." && pwd)"; R=/Volumes/_hd1_22T/名画库; PY=/opt/homebrew/bin/python3
echo "等待 hd1 … $(date)"
for i in {1..1440}; do [ -d "$R/_manifests" ] && break; sleep 60; done
[ -d "$R/_manifests" ] || { echo "24 小时内未等到 hd1,退出"; exit 1; }
echo "hd1 已挂载 $(date)"; sleep 20
# ① 标喜欢
$PY - "$R" <<'PYEOF'
import json,glob,sys
n=0
for f in glob.glob(sys.argv[1]+'/_manifests/*__精选.json'):
    m=json.load(open(f)); ch=False
    for w in m['works']:
        rs=w.get('culture_relation') or []
        why=[t for k,t in (('画框之外','画框之外 The Living Gallery 收录'),('周杰伦《太阳之子》','周杰伦《太阳之子》(2026)MV 名画重现')) if any(r.startswith(k) for r in rs)]
        if why and not w.get('favorite'):
            w['favorite']=True; w['favorite_reason']=';'.join(why); ch=True; n+=1
        elif why and not all(x in (w.get('favorite_reason') or '') for x in why):
            w['favorite_reason']=';'.join([w.get('favorite_reason')]+[x for x in why if x not in (w.get('favorite_reason') or '')]).strip(';'); ch=True
    if ch: json.dump(m,open(f,'w'),ensure_ascii=False,indent=1)
print('① 新标为喜欢:',n)
PYEOF
# ② _trash 存档 + 校验 + 移除
T="$I/_trash"; D="$R/_trash_归档/home_design_trash_20261002"; STAR='20261001-044642__星月夜_原图_超高清(hd1已有).jpg'
if [ -d "$T" ]; then
  mkdir -p "$D"; (cd "$T" && rsync -a --exclude "$STAR" ./ "$D/")
  a=$(cd "$T" && find . -type f ! -name "$STAR" -print0 | sort -z | xargs -0 shasum -a 256)
  b=$(cd "$D" && find . -type f ! -name '_sha256清单.txt' -print0 | sort -z | xargs -0 shasum -a 256)
  h1=$( [ -f "$T/$STAR" ] && shasum -a 256 "$T/$STAR" | cut -d' ' -f1 || echo none)
  h2=$(shasum -a 256 $R/梵高*/油画/1889_星月夜/原图_超高清_44567x35291.jpg | cut -d' ' -f1)
  if [ -n "$a" ] && [ "$a" = "$b" ] && { [ "$h1" = none ] || [ "$h1" = "$h2" ]; }; then
    print -r -- "$b" > "$D/_sha256清单.txt"
    n=$(print -r -- "$b" | wc -l | tr -d ' ')
    rm -rf "$T" && mkdir -p "$T" && echo "② _trash 已存档到 hd1($n 个文件校验一致;星月夜与 hd1 一致)并从内置盘移除"
  else
    echo "② 校验不一致,未删除任何文件"; diff <(print -r -- "$a") <(print -r -- "$b") | head
  fi
fi
# ③ 续跑
zsh $R/_jobs/hk_finish.sh
echo "全部完成 $(date)"
