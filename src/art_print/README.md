# src/art_print — 名画打印

把排好的整页 A4 稿按固定设置发给打印机 `_prt1`(EPSON EW-M873T)。零依赖,只用系统自带的 `lp`、`lpstat`、`lpoptions`、`ipptool`、`sips`。对应 skill:`/art-print`。

| 文件 | 用途 |
|---|---|
| `art_print_v2.py` | **现行**。三个子命令:`check` 体检、`calib` 普通纸校准页、`send` 发打印稿;默认走 Epson 驱动队列 `EPSON_EW_M873T_Driver`,`--queue airprint` 退回 AirPrint 队列 `EPSON_EW_M873T` |
| `art_print.py` | v1,只认 AirPrint 队列。2026-10-27 用它印 Velvet 出现毛边渗墨、暗部糊,留作对照 |
| `README.md` | 本文件 |

## 用法

```bash
python3 src/art_print/art_print_v2.py check
python3 src/art_print/art_print_v2.py calib --apply                      # 普通纸,背面进纸
python3 src/art_print/art_print_v2.py send <稿件> --paper velvet          # 预演
python3 src/art_print/art_print_v2.py send <稿件> --paper velvet --apply  # 真的发
python3 src/art_print/art_print_v2.py send <稿件> --paper velvet --opt EPIJ_Qual=355   # 临时改某个驱动选项
```

- `send` 默认只预演,`--apply` 才发;`--hold` 发成暂停任务,不出纸,用来核对选项。
- 发出去的任务记在稿件同目录的 `打印记录.jsonl`(暂停任务不记),含完整选项。
- 背面进纸:**先发任务,等打印机屏幕提示再插纸**,一次 1 张。先插纸再发会卡(10/27 实测)。

## 驱动队列的纸型预设(v2 默认)

| `--paper` | 纸 | `EPIJ_Medi` | `EPIJ_Qual` | `EPIJ_FdSo` |
|---|---|---|---|---|
| `velvet` | Epson Velvet Fine Art Paper | 53 | 360 最高 | 0 背面 |
| `matte` | フォトマット紙 | 67 | 355 きれい | 0 背面 |
| `plain` | 普通纸(演练) | 0 | 354 标准 | 0 背面 |

每次固定带上:`EPIJ_Size=1`(A4)、`EPIJ_PSrc=2`(有边)、`EPIJ_Mode=3`(Advanced)、`EPIJ_Ink_=1`(彩色)、`EPIJ_CMat=0` + `EPIJ_CCor=4`(手动、EPSON 标准色彩校正)、`EPIJ_Gamm=0`(2.2)、`EPIJ_AFil=0`(不锐化)、`EPIJ_OSColMat=1`(驱动管色)。选项值来自 PPD `/Library/Printers/PPDs/Contents/Resources/EPSON EW-M873T Series.gz`,全表用 `lpoptions -p EPSON_EW_M873T_Driver -l` 看。

队列建法(一次性,地址用 `device_resolve("打印机")` 取):`lpadmin -p EPSON_EW_M873T_Driver -E -v ipps://<打印机>:631/ipp/print -P "/Library/Printers/PPDs/Contents/Resources/EPSON EW-M873T Series.gz"`。打印机接受 `application/vnd.epson.escpr`,所以驱动输出能走 ipps 631;9100 口关着,LPD 已关。

## AirPrint 队列的纸型预设(`--queue airprint`,备用)

| `--paper` | MediaType | 画质 | 进纸口 |
|---|---|---|---|
| `velvet` | `Com.epsonVelvetFineArt` | High | Rear |
| `matte` | `PhotographicMatte` | High | Rear |
| `plain` | `Stationery` | Normal | Rear |

## 稿件要求

- 整页 A4(210×297 mm,横竖都行),图已按实际尺寸摆在页面里,四边留 3.5 mm。
- JPG / TIFF / PNG 带分辨率和色彩描述文件,或竖放 A4 的 PDF。
- 工具把稿件转成竖放 A4 的 PDF(横稿先转 90°),按 100% 发,不缩放。尺寸不是 A4 就拒发。
- 客厅画墙的稿件由 `home design/客厅设计/05_脚本与中间文件/_ids/gen_print_v1.py` 生成,在 `home design/客厅设计/06_打印稿/`。

## 已核实与未核实(2026-10-27)

- 已核实(AirPrint 队列):接受上表的选项;有边模式四边 3 mm;送图上限 360 dpi;`calib` 实印:两条标尺 100 mm、四边框都在、背面进纸印在朝上那面。
- 已核实(驱动队列):PPD 含 Velvet(53)/Photo Matte(67)纸型、背面进纸(FdSo=0)、7 个纸张 ICC;`check` 通过。
- 未核实(驱动队列):实际出纸的缩放与边距、Velvet 配 `EPIJ_Qual=360` 是否被驱动接受——要靠 `calib` 和第一张真印才知道。`cupsfilter` 在 cupsd 之外跑 Epson 滤镜会崩,不能用它预检。
