---
name: drone-msdk
description: DJI 无人机 × MSDK 编程飞行实验的知识卡和流程(本项目专用)。机型 Mini 4 Pro;遥控器必须用 RC-N2;Android MSDK V5;在日本哪里能飞、要办什么手续(桶川、长瀞、箱根、美瑛、埼玉练习场);租赁(ドロサツ 的价格和 Care);飞行任务设计(相对坐标航点、Reveal、环绕、安全闸、日志);先租后决定买不买的判断标准。用户提到无人机编程、MSDK、Mini 4 Pro、RC-N2、DJI 飞行计划、去哪飞无人机、飞行许可、租无人机、长瀞或箱根航拍、无人机航点任务、要不要买无人机时使用。
argument-hint: "[plan|where|mission|dev|rent|preflight|review|issues] 默认先看 ISSUES"
allowed-tools: Bash, Read, Edit, Write, WebSearch, WebFetch, AskUserQuestion
---

# /drone-msdk — DJI 无人机 × MSDK 编程飞行实验

| 文件 | 内容 |
|---|---|
| `knowledge.md`(本目录) | **知识真源**:硬件前提、法规、地点比较、租赁价格、任务设计、安全闸、买不买的标准,每条都附出处和核实日期 |
| `ISSUES.md`(本目录) | 未解决的问题和待验证项(本项目 local-only,不开 GitHub issue,用这个文件代替) |
| `TESTS.md`(本目录) | 测试本 skill 用的提问和期望行为 |
| `调研_DJI选购/MSDK飞行实验计划_v1.md` | 当前这次实验的计划书(knowledge 的具体应用);新版本另存 `_v2`,不覆盖旧版 |
| `调研_DJI选购/Mini_4_Pro/` | DJI 官方用户手册和更新日志(JP,PDF + txt) |
| `TASKS.md` 中「Mini 4 Pro × MSDK」一节 | 任务状态 |

## 规矩

1. **每次先读 `ISSUES.md`**,开头先报告 open 的项。用户的回答或新查到的事实能关掉某项,就当场把它改成 closed,写上日期和依据。
2. **法规、价格、SDK 支持情况都会变**:knowledge 里超过 90 天没核实的条目,用到之前先 WebSearch 或 WebFetch 复核,更新 `核实日期`。查不到的,如实写「未核实」。
3. 判断"能不能飞"要按顺序过四关,缺一关就不算能飞:**航空法**(DID、目视、30m、夜间、150m)→ **小型无人机等飞行禁止法**(重要设施周边)→ **地方或管理者规定**(町、公园、国立公园、机场)→ **土地所有者同意**。
4. **第一次跑自己写的代码,只能在练习场**,不在风景区首飞。
5. 去某个地方要联系谁、要备案、要拿许可的,列成待办交给用户;**不替用户打电话、不替用户提交申请**。咨询表单可以用 `/form-fill` 填,正文先给用户看,用户说发再发。
6. 写代码时,实现代码放 `src/drone_msdk/`(Android 工程),同时给出目录说明;MSDK 的 App Key 不进 git。

## 子命令

- `plan`:读 knowledge、计划书和 ISSUES,报告当前阶段和下一步。
- `where <地点>`:按规矩 3 的四关给出结论表,附出处;结论写回 knowledge 的地点表。
- `mission <地点>`:按 knowledge 第 5 节的模板,用相对坐标设计 M0~M5;练习场版本的距离 ×0.5。
- `dev`:搭或续写 `src/drone_msdk/` 的 MSDK V5 Android 工程(先确认 Android 手机和 App Key 都有了)。
- `rent`:比较租赁选项。核心问题是**能不能拿到 RC-N2**,拿不到的话这套设备就编不了程。
- `preflight`:飞行当天的检查表(knowledge 第 6 节)。
- `review`:飞完后用日志 CSV 画轨迹、写复盘;按第 7 节的标准给出买或不买的结论;新学到的写回 knowledge 和 ISSUES。
- `issues`:只列出 ISSUES 的状态。

## 更新规则

- 新事实写进 knowledge 对应的小节:每条带 `(出处 URL,核实 YYYY-MM-DD)`。
- 新问题加到 ISSUES 末尾,编号接着往下排(`D-xx`),不要重新编号。
- 用 TESTS 测出 skill 的问题后,改 SKILL.md 或 knowledge,并在 ISSUES 里记一条 `skill 修正`。
- 改动后在本项目 git 本地 commit(privacy 项目,不推送)。
