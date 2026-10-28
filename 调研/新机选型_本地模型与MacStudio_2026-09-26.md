# 调研:新机选型——本地模型要多大内存?MacBook、Mac Studio、NVIDIA 怎么选?

> 2026-09-23 ~ 09-26 会话整理。隐私项目,本地保存。结论先行,依据与出处在后。
> 数据可信度标签:**已确认**＝Apple/厂商官方或在售价;**传闻**＝媒体爆料;**推测**＝按历代规律外推,无来源。

## 0. 一句话结论

**旧 M1 Max 64GB 留家里当模型服务器;新机若为本地模型买,首选 Mac Studio M5 Max 128GB(约 ¥75 万),而不是 ¥199 万的 M5 Ultra 256GB——除非明确要跑 235B 以上模型或做视频生成。本地模型用来做转写、OCR、隐私批量任务,替代不了 Claude/ChatGPT 干活。**

## 1. 现状与需求

| 项目 | 内容 |
|---|---|
| 现主力机 `_mb1` | MacBook Pro 14" 2021,MacBookPro18,4,M1 Max 10C CPU / 32C GPU,64GB,2TB,国行 CH/A;电池最大容量 80%、442 次循环 |
| 处置决定 | **不卖**,换机后留家当备用机 / 模型服务器(已开 macOS 26 充电上限 80%,插电常驻) |
| 实际负载 | mlx-whisper large-v3 转写(`transcribe` 技能)、本地 Qwen 第二引擎、OCR、Parallels 虚拟机 |
| 便携性 | 不需要再多一台笔记本(用户确认) |

## 2. 选型原理(不变的框架)

Apple Silicon **没有独立显卡**,也不支持外接显卡;CPU/GPU 共用统一内存,**选内存＝选显存**。尺寸只决定能选哪档芯片(Air 只有基础芯片;Pro 14/16 寸上限相同)。Intel 时代"13 寸核显、15/16 寸独显"的区分已不存在。

| 变量 | 决定什么 |
|---|---|
| **内存容量** | 能不能跑。4-bit 量化约:8B≈5GB、14B≈9GB、32B≈20GB、70B≈40GB、120B 级≈65–70GB、235B≈130GB、405B≈230GB |
| **内存带宽**(芯片档位决定) | 生成速度。经验式:**字/秒 ≈ 带宽 ÷ 模型大小** |
| GPU 核数 / 神经加速器 | 提示处理、长文档、批量任务速度 |
| 散热 | 能否持续满速(Air 无风扇会降频) |

优先级:**容量 > 带宽 > 芯片代际**。代际每年只涨 15–25%,带宽跟档位走(M1→M3 Max 都是 400 GB/s)。

**「70B Q4」是尺子,不是某个模型**:700 亿参数、4-bit 量化(约 40GB),卡在"家用机能不能跑"的分界线上;所有 70B 级模型(Llama 3.3 70B、Qwen2.5-72B 等)速度近似相同。MoE 模型(如 gpt-oss-120b 每次只激活 5B)速度远快于同体积稠密模型。体感:<5 字/秒像打字机,>10 字/秒可流畅阅读。

## 3. 已确认的 2026 年 Apple 新机

### 3.1 MacBook Pro M5 Pro / M5 Max——2026-03-03 发布(**已确认**)

| 芯片 | 带宽 | 最大内存 | 70B Q4 约 |
|---|---|---|---|
| 旧 M1 Max(对照) | 400 GB/s | 64GB | 8–10 字/秒 |
| M5 Pro | **307 GB/s** | 64GB | **比 M1 Max 还慢** |
| M5 Max | 614 GB/s | 128GB | 13–15 字/秒 |

美元价:14" M5 Pro 24GB/1TB $2,199;14" M5 Max 36GB/2TB $3,599;48GB/2TB $4,099;16" M5 Pro $2,699、M5 Max $3,899。苹果宣称 LLM 提示处理比 M4 Pro/Max 快 4 倍(每个 GPU 核加了 Neural Accelerator)。
→ **跑大模型不退步只能选 Max。**

### 3.2 Mac Studio M5 Max / M5 Ultra——2026-08-25 发布、09-22 发售(**已确认**)

| 项目 | M5 Max | M5 Ultra |
|---|---|---|
| CPU / GPU | 18C / 最高 40C | 最高 36C / 80C,32 核 Neural Engine |
| 带宽 | **低配 460 / 高配 614 GB/s** | 1.2 TB/s(**是否低配 Ultra 也是 1.2TB/s 待确认**) |
| 内存档位 | 36 / 48 / 64 / 128GB | 96 / 256 / 512GB(512GB 版 10 月下旬出货) |
| 日本起价 | ¥419,800 | ¥949,800 |
| 美国起价 | $2,499 | $5,499 |

用户保存的官网配置(2026-09-26):**M5 Ultra 36C CPU / 80C GPU、256GB、2TB = ¥1,993,800**。拆分:起价 949,800 + 高配芯片约 234,000(倒推)+ 内存 96→256GB 720,000 + 存储 1→2TB 90,000。

苹果宣称:M5 Ultra 比 M3 Ultra AI 峰值算力高 4.3 倍;4 台 Studio 组集群推理最高快 3 倍。

> 注:本人 6 月知识截止时 M5 Ultra 仅是传闻,当时推测价 ¥90–110 万**严重偏低**(实为约 2 倍);推测带宽 2×614≈1.2TB/s 与官方一致。

### 3.3 传闻中(未发布)

| 机型 | 时间 | 备注 |
|---|---|---|
| OLED MacBook Pro 大改款(可能 M6,触屏、更薄) | 2026 年底或 2027 初(**传闻**,9to5Mac) | 芯片、价格全未知;第一代新设计 |
| 廉价 MacBook(A18 Pro,13 寸,约 $699) | 下半年(**传闻**) | 支持 Apple Intelligence,**适合给母亲 `_mb2` 换机** |
| Mac mini 刷新(可能 M6) | 下半年(**传闻**) | 可做家用模型服务器 |

## 4. 候选对比

| 方案 | 日本价 | 可用内存 / 带宽 | 70B Q4 | 强项 | 弱项 |
|---|---|---|---|---|---|
| **Mac Studio M5 Max 128GB(高配芯片)** | 约 ¥75 万(**推测**,起价 419,800 + 升级;以配置器为准) | 128GB / 614 | 约 15 字/秒;120B 级可跑 | 安静(满载约 200W)、Parallels 与 macOS 虚拟机、保值 | 训练、视频生成弱 |
| Mac Studio M5 Ultra 96GB | ¥949,800 | 96GB / 1.2T? | 约 25–30 | 快 | 容量反比上面小,**性价比最差** |
| Mac Studio M5 Ultra 256GB(用户所选) | ¥1,993,800 | 256GB / 1.2T | 约 25–30;235B、405B Q4 可装 | 大模型、集群 | 贵;超出当前需求 |
| MacBook Pro M5 Max 14" 64–128GB | 约 $4,500–5,000+(**推测**) | 64–128GB / 614 | 约 15 | 可随身 | 笔记本内存溢价高 |
| **NVIDIA DGX Spark**(GB10,2025-10 上市) | $3,999,日本约 ¥60 万(**推测**,未核实) | 128GB / **273 GB/s** | 约 5–7(比 M1 Max 还慢) | CUDA、微调、提示处理、视频生成 | 生成慢;2 台联机只加容量不加速 |
| 自组 PC 单 RTX 5090 + Linux | ¥60–70 万(5090 单卡约 ¥40 万,**记忆值**) | 显存 32GB / 1.8 TB/s | **装不下**,溢出到 CPU 降至 3–5 | 32B 以内最快、Whisper CUDA 最快、可升级 | 700W+ 吵;无 macOS 虚拟机 |
| 自组 PC 双 5090 | 约 ¥110 万 | 64GB | 约 25–30 | 70B 速度冠军 | 1200W+,很吵 |
| 自组 PC 四张二手 3090 | ¥60–80 万 | 96GB | 约 15–20 | 每万日元显存最多 | 1400W、占地、二手风险 |
| NVIDIA DGX Station(GB300) | 未公布,数百万日元级(**推测**) | 784GB | 快 | 企业级 | 价格不适用 |

PC 明显赢:训练/微调、图像视频生成、Whisper 大批量、所有能塞进显存的模型。Mac 明显赢:每万日元可用容量、功耗噪音、macOS 虚拟机与现有工作流。

判断口诀:**模型大多在 32B 以内 → 单 5090 PC;70B 以上 + 要安静 + 要 macOS 虚拟机 → Mac Studio;70B 以上 + 不在乎电费噪音 → 多卡二手 3090。**

## 5. 端侧开源模型 Top 3(截至 2026-06 知识,需复查最新榜单)

| 模型 | 内存(Q4) | 强项 |
|---|---|---|
| OpenAI gpt-oss-120b(Apache 2.0)/ 20b | 约 65GB / 16GB | 推理、工具调用;MoE 速度快 |
| 阿里 Qwen3 系列(30B-A3B、32B、235B-A22B、Coder) | 18GB / 20GB / 130GB | **中日文最好**,代码强 |
| Google Gemma 3 27B | 约 17GB | 多模态看图、140 种语言、128K 上下文 |

分工建议:中日文问答 Qwen3-30B-A3B;复杂推理 gpt-oss;看图/OCR 类 Gemma 3;转写继续 Whisper large-v3。以上 M1 Max 64GB 现在都能跑(gpt-oss-120b 需关掉其他软件)。

**第三方实测反馈**(他人经历,非用户本人):在 DGX Spark 上部署 Qwen3.5-27B 4-bit,"很笨、响应慢、有时答非所问、修 bug 修很久"。解读:27B 规模天花板 + 4-bit 精度 + Spark 带宽低 + 部署方式可能不对。**结论成立的部分:本地模型代替不了云端模型写代码。**

## 6. Whisper / OCR / Apple Intelligence 的要求

| 负载 | 要求 |
|---|---|
| Whisper large-v3 | 任何 M 芯片约 3–4GB 内存;NVIDIA 上 `faster-whisper` / `whisperX` 比 MLX 快数倍 |
| OCR | 系统 Live Text 即可,几乎不占资源 |
| Apple Intelligence | M1 及以后的 Mac(端侧约 3B 模型);**Intel Mac(如 `_mb2`)不可用** |

## 7. 旧机 M1 Max 的市场价(2026-09-24 查)

| 渠道 | 金额 |
|---|---|
| 煤炉 14" M1 Max 64GB/2TB 成交 | ¥239,000、¥239,800、¥290,000;同店批量"本体のみ"¥219,800 |
| 预计可卖 | ¥210,000–240,000,扣 10% 手续费到手约 ¥190,000–215,000 |
| Apple 日本 Trade In(Likewize) | **¥124,000 Apple 礼品卡**(估价题不问内存,64GB 不计价;首次误答水浸题得 ¥0) |
| Apple 中国 Trade In | MacBook Pro 最高 RMB 8,300(最新机型上限) |

已决定不卖,留作服务器。

## 8. 推荐与反转条件

- **首选**:Mac Studio M5 Max 128GB(高配芯片 614 GB/s),约 ¥75 万。
- **要上 Ultra**:只选 256GB 以上(96GB Ultra 无意义);**先在配置器确认低配 Ultra 的带宽**,若同为 1.2TB/s 则省下约 ¥23 万的高配芯片费(80C GPU 只对图像/视频生成有用)。
- **反转条件**:
  - 预算 < ¥50 万 → 不换,M1 Max 继续主力;
  - 明确要跑 235B+ 或做视频生成 → M5 Ultra 256GB 或 NVIDIA 方案;
  - 需要微调/训练 → DGX Spark 或 NVIDIA PC;
  - 必须随身带大模型 → MacBook Pro M5 Max 128GB;
  - 不急且想要 OLED → 等年底 M6 改款发布后按本框架重算。
- **分工**:M1 Max 家用常驻(Ollama 局域网服务、Whisper、OCR、备份);新机跑 70B+ 与虚拟机。

## 9. 待办

- [ ] 在 Apple 配置器确认 M5 Ultra 低配(芯片档位)的内存带宽
- [ ] 查 Mac Studio M5 Max 128GB 高配芯片的确切日元价
- [ ] 复查 2026-09 最新端侧模型榜单(LMArena / Artificial Analysis)
- [ ] 母亲 `_mb2`:关注廉价 MacBook(A18 Pro)发布,或考虑 M1 Air 二手(煤炉 8GB/256GB 成交 ¥42,000–66,000,集中 ¥50,000–57,000)

## 出处

- Apple 新闻稿:MacBook Pro M5 Pro/M5 Max(2026-03)https://www.apple.com/newsroom/2026/03/apple-introduces-macbook-pro-with-all-new-m5-pro-and-m5-max/
- Apple 新闻稿:Mac Studio M5 Max/M5 Ultra(2026-08)https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/
- AAPL Ch. 日本价格与出货:https://applech2.com/archives/20260825-mac-studio-m5-max-and-ultra.html
- ITmedia 4 台 M5 Ultra 集群:https://www.itmedia.co.jp/aiplus/article/2608/26/2000000786/
- Macworld MacBook Pro M5 价格表:https://www.macworld.com/article/2942089/macbook-pro-m5-pro-max-release-specs-price.html
- 9to5Mac 2026 Mac 产品线展望:https://9to5mac.com/2026/01/25/apple-mac-lineup-2026-plans-macbook-pro-overhaul-new-m6-chips/
- MacRumors 产品指南:https://www.macrumors.com/guide/upcoming-apple-products/
- Apple Tahoe 兼容机型:https://support.apple.com/en-us/122867
- 用户保存的官网配置页:`~/Downloads/Mac Studio、M5 Ultraチップ、36コアCPU、80コアGPU、256GBのメモリ、2TBのストレージを購入 - Apple（日本） (9_26_2026 1：31：32 AM).html`
