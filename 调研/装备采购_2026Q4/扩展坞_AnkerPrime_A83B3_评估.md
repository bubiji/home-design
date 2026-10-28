# Anker Prime 扩展坞(14 合 1,三屏,DisplayLink)评估

> 2026-09-30,店头照片(Downloads/IMG_5083~5085)+ 官网与评测核对。结论:**对现在的 `_mb1`(M1 Max 14")不推荐**;若 12 月上 Mac Studio,更不需要它。

## 型号与价格

- Anker Prime Charging Docking Station(14-in-1, Triple Display, DisplayLink),型号 **A83B3**,DisplayLink 芯片 DL7400。日本店头 ¥39,990(含税)。
- 同架旁边的 Anker Prime Charger 200W 6 口 GaN 充电器 ¥12,990(单口最大 100W)。

## 接口(官网,已确认)

| 位置 | 接口 | 规格 |
|---|---|---|
| 上行 | USB-C ×1 | 140W 供电,**USB 3.2 10Gbps(不是雷雳)** |
| 前面 | USB-C ×2 | 10Gbps,100W |
| 前面 | USB-C ×1 | 5Gbps,100W |
| 前面 | SD + TF 卡槽、3.5mm 音频、控制旋钮 + 彩色小屏 | 小屏显示各口功率/分辨率;旋钮切换显示与省电模式 |
| 背面 | USB-A ×2 | 5Gbps |
| 背面 | USB-A ×1 | USB 2.0(480Mbps) |
| 背面 | DisplayPort ×1 | **原生**(DP Alt Mode),8K@60Hz |
| 背面 | HDMI ×2 | **DisplayLink 模拟**,8K@30Hz |
| 背面 | 2.5G 网口、AC 电源输入 | 内置风扇 |

电源总输出 160W:给 Mac 140W 后其余口只剩 20W(Macworld 主要批评点)。

## 用户的两个问题

### 1. 能做"双屏幕切换"吗

**同时接两台显示器**——能,但 M1 Max **用不着它**:M1 Max 原生支持 3 台外接显示器,机身 HDMI 口现在空着,第二台屏直接插 Mac,画质延迟都比 DisplayLink 好。坞上只有 1 个原生 DP,2 个 HDMI 都靠 DisplayLink:要装驱动、给「屏幕录制」权限,而且**放不了 Netflix / Prime Video / Apple TV 等受版权保护内容**。

**一台显示器在两台电脑间切换(KVM)**——坞**做不到**,只有一个上行口。但已有的 **Dell U3223QE 自带 KVM**:Mac 走 USB-C,第二台电脑走 HDMI/DP + USB-B 上行线,键鼠接显示器,在 OSD 里切;装 Dell Display Manager 可 Auto KVM 自动切。此功能已经买过,只是没用。

### 2. 接口够不够现在的设备一直连着

现常插:22TB `_hd1`、Passport 1TB `_hd3`、iPad、Redmi Note 10 JE、DJI 麦发射器 ×2、有线网;偶尔:Elements 1TB `_hd2`、SSD `_ss1`、光驱 `_cd1`、安卓测试机。

坞的数据口共 6 个(USB-C ×3 + USB-A ×3),常插 6 台正好填满,偶尔用的没位置。可行的搭配:DJI 发射器只充电,挪到充电器上(空出 2 口);现有 Anker USB-C hub 串在坞的 10Gbps 口上专挂硬盘。这样够用,Mac 还能空出 2 个雷雳口 + HDMI。

短板:所有硬盘共享一条 10Gbps 上行(机械盘无所谓,SSD 会被压到一半);14" M1 Max 最多只吃 96W,140W 供电对它没意义,现有显示器的 90W 已接近上限。

## 结论

这 ¥39,990 买到的是"口多 + 2.5G 网口 + 单线插拔",三屏与 DisplayLink 对用户是用不上的功能。
- 只想多几个口:几千日元的 10Gbps hub + 显示器自带集线器即可。
- 想要真正单线全接管、两台屏原生输出:看同系列 **雷雳 5 版(A83B5)**,40Gbps、不用 DisplayLink,更贵。
- **若 12 月买 Mac Studio**:它自带 6 个雷雳 5 口 + 2 个 USB-A + HDMI + 10G 网口,扩展坞议题自然消失。

## 顺带发现(登记簿)

- 现有 Anker USB-C hub(VIA Labs VL822 桥,10Gbps)与 Redmi Note 10 JE 都**未登记**,待用户告知型号/归属。
- Dell U3223QE 已登记为 `_mon1`(EDID 2023 年第 15 周,机身 Service Tag 待补)。
