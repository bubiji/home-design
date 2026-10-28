# 调研_装备采购_2026Q4 —— 12 月采购议题的资料汇总

> 建于 2026-09-30。隐私项目,本地保存。总计划在上一层的 `装备采购与软件计划.md`,本目录放各议题的调研正文与资料出处。
> 数据可信度:**已确认**＝厂商官网/在售价;**推测**＝按规律外推。价格为日本含税价,12 月下单前必须重核。

| 议题 | 文件 | 状态 |
|---|---|---|
| 双显示器选型(12 月想买;Mac 显示器 vs Dell vs 护眼型) | `双显示器选型_评估.md` | 初评完成,12 月复核清单在文末 |
| Mac Studio 要不要买 | `../doc/调研_新机选型_本地模型与MacStudio_2026-09-26.md`(正文)+ `../doc/调研_新机选型_附件/`(Apple 配置页、Likewize 报价页存档) | 9/26 已评估;本目录只做索引,见下 |
| Anker Prime 扩展坞 A83B3 | `扩展坞_AnkerPrime_A83B3_评估.md` | 已评估:**对 M1 Max 不推荐** |
| 22TB 硬盘 `_hd1` 太吵,想接远一点 | `hd1_22T_远离桌面方案.md` | 方案列出,待选 |

## Mac Studio 已有评估(索引)

- **结论(2026-09-26)**:旧 M1 Max 64GB 留家当模型服务器;新机若为本地模型买,首选 **Mac Studio M5 Max 128GB(约 ¥75 万)**,不是 ¥199 万的 M5 Ultra 256GB,除非明确要跑 235B 以上模型或做视频生成。
- **日本起价(2026-09-22 上市,已确认)**:Mac Studio M5 Max ¥419,800、M5 Ultra ¥949,800;同日 Mac mini M6 ¥149,800、M5 Pro ¥299,800。512GB 内存版 10 月起。
- **待办(正文第 8 节)**:在官网配置器确认低配 M5 Ultra 的内存带宽是否也是 1.2TB/s——若是,可省约 ¥23 万高配芯片费。
- **相关会话**(本项目,`claude --resume <id>` 可续):
  - `0b4b3776-1e4a-4804-bc46-d037e1b0caea`(2026-09-23 ~ 09-29,提及 Mac Studio 158 次,评估主会话,产出上述正文)
  - `7f213a26-eaf8-40a7-a293-185397d34b33`(2026-09-28,顺带提及)
- 与显示器议题的交叉点:Mac Studio 只有雷雳口没有内置屏,**买它就必然要配显示器**;新 Studio Display 是雷雳 5,可菊花链最多 4 台。两个议题应一起定。

## 资料出处(2026-09-30 查)

| 主题 | 出处 |
|---|---|
| Apple 新 Studio Display / XDR 发布(2026-03-04 预订,03-11 发售) | https://www.apple.com/jp/newsroom/2026/03/apple-introduces-stunning-studio-display-xdr/ |
| Apple 官网购买页 | https://www.apple.com/jp/shop/buy-mac/studio-display |
| Dell U2725QE / U3225QE(IPS Black、120Hz、雷雳 4 集线器) | https://pc.watch.impress.co.jp/docs/news/1650530.html · https://www.dell.com/ja-jp/blog/digital-highend-monitor-u2725qe-u3225qe/ · Dell 日本商店 U3225QE 页 |
| EIZO FlexScan EV2740X / EV3240X(护眼、Auto EcoView) | https://www.eizo.co.jp/products/lcd/ev2740x/ · https://www.eizo.co.jp/products/lcd/ev3240x/ · https://direct.eizo.co.jp/shop/g/gEV3240X-WT/ |
| Mac mini / Mac Studio 2026-09-22 发售与价格 | https://www.smartwatchlife.jp/81267/ |
| Anker Prime 扩展坞 A83B3 官方页 | https://www.anker.com/products/a83b3-anker-prime-charging-docking-station-14-in-1-triple-display-140w |
| Macworld 评测(电源预算不足是主要批评) | https://www.macworld.com/article/2992468/anker-prime-14-in-1-displaylink-usb-c-dock-review.html |
| Dell 显示器 KVM 设置指南 | https://www.dell.com/support/contents/en-us/article/product-support/self-support-knowledgebase/monitor-screen-video/kvm-setup-guide-dell-monitors |
| USB 3.0 光纤/有源延长线 | https://www.fibermall.com/ja/sale-424894-usb-3-0-type-a-aoc-10m.htm · https://www.buffalo.jp/product/detail/bsuambsu315bk.html |

现有设备参数见登记簿(`device_resolve 显示器` / `_hd1` / `_mb1`)。
