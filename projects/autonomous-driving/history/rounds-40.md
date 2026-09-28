# 第四十轮（2026-09-24）· 传播核查：前四轮的口径结论有多少处还没同步

**动因**：第三十六至三十九轮连续产出四条**承重的口径/代码更正**（DiffVLA 发布版换头、EPDMS 两套实现、EC 不进分、本地 devkit 版本）。按 [ai/workflows.md](../../../ai/workflows.md) §轮次收尾的纪律，这类更正要**逐个同步到所有引用处**——但前几轮都是"就地修发现的那一处"。本轮做一次**系统的传播核查**：把四条结论当成搜索条件，全库找还没改的旧表述。

## 做法

对四条结论各做一次全库检索（排除 `code/repos/` 与 `history/rounds-*`）：① "未找到官方代码 / 未见官方代码"；② `EPDMS` 的引用处（28 个第一方文件）；③ "EC + 权重 2"；④ `36/36`、`§E 在列 6 个` 这类计数。同时检查文件体积是否需要拆册。

## 结论（本轮抓到 4 处 stale，其中 1 处是真错误）

### 1. **⚠ 真错误：`vla/verification.md` 把一句正确的 docstring 判成了"与实现不符"**

原文（第二十四轮写的）：

> **一处 docstring 与实现不符**：`PDM_Reward.rl_pdm_score` 的 docstring 写 "excluding the two_frame_extended_comfort metric"，**代码里没有排除任何指标**（直接取 `result.score`）…

**第三十九轮的发现让这条翻转**：本地 devkit 的 `result.score`（EPDMS）**本身就排除 EC**（`pdm_scorer.py` 原文 "Exclude the two-frame extended comfort metric from the weighted metrics calculation"）→ **排除发生在上游 devkit 里，这个 wrapper 不需要再排除** → **docstring 是对的，原判是误读**。已改为"看起来不符，其实相符"，并保留仍然成立的后半句（`except Exception` 静默返回 0 奖励）。

> **这是本轮最有价值的一处**：它说明"代码级核验"的结论也会因为**上游依赖的口径没核清**而判错——**看一个 wrapper 有没有做 X，必须先知道它调用的底层有没有做 X**。

### 2. **DP-A27（DiffVLA）在研究对象表里仍写"未找到官方代码"**

第三十六轮只修了 **VLA 侧**（`VLA-06` 笔记 + `vla/papers.md`）与 `code/repositories.md §E`，**漏了 `topics/diffusion-planner/papers/diffusion_planner_ad.md` 的 DP-A27 行**——而 DP-A27 正是 DiffVLA 在研究对象侧的编号。→ 已改为"**有官方代码，但发布版与论文不同**"+ L3 核验结论 + 证据状态升级为"元数据 + 摘要 + **代码静态检查（L3）**"。
**连带**：该表文件头的"研究对象侧 L3 共 6 个"→ **7 个**（补 DP-A27）。

### 3. **两处计数 stale**

- `papers/diffusion_planner_ad.md` 的"官方代码快照 **36/36** 已获取" → **37/37**（36 是第二十一轮新增 `OpenDriveVLA` **之前**的旧数；权威计数在 `state.md`）。
- `index.md` 的"**§E VLA 侧在列 6 个**" → **8 个**（第三十六轮补了 DiffVLA 与 recogdrive 两行）。

### 4. **两处口径警告只写在了 `benchmarks.md`，没写到会被人直接引用的表上**

第三十八 / 三十九轮的两条口径结论（EPDMS 两套实现、EC 不进分）此前只落在 `benchmarks.md §2.9/§2.10`、`judgments.md §B`、`sota-plan.md`、`preparation.md` 的 P2c。但**两张"会被直接拿去引用数字"的表还没有警告**：

- `papers/diffusion_planner_ad.md` 的「证据边界」节 → 已加一条并列警告（**v2 EPDMS 一律按"口径未声明"读**；**EC 不进 EPDMS**）。
- `preparation.md §6.1`（跨论文 navtest 对照表）的「读法」→ 已加**第四条读法（口径）**与 EC 那条。

→ **原则**：口径警告必须写进**读者会直接抄数字的那张表**里，不能只写在口径专章（读者抄数时不会先翻 §2.9）。

### 5. 体积检查：**暂不需要拆册**

| 文件 | 体积 |
|---|---|
| `preparation.md` | **58.6 KB**（最大；待续清单第 16 项已预警） |
| `world-model/verification.md` | 55.5 KB |
| `papers/diffusion_planner_ad.md` | 53.4 KB |
| `vla/verification-2.md` | 50.7 KB |
| `benchmarks.md` | 49.6 KB |

→ 全部 < 64 KB；`preparation.md` 与 `world-model/verification.md` 需继续盯（都已过半）。

**本轮未新增判断条目**（判断条数保持 **63**）：本轮的产出全是**传播与更正**，没有新结论——按第三十三轮立的规则（"引用可以重复，计数不能"），这类轮次不应为了凑数而加条目。

## 产出

| 类别 | 文件与章节 |
|---|---|
| 更正（真错误） | [vla/verification.md](../topics/vla/verification.md) §5.1 的 docstring 条（"与实现不符"→"其实相符"） |
| 更正（传播漏） | [papers/diffusion_planner_ad.md](../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A27 行（未找到代码 → 有代码 + L3）+ 文件头 L3 6→7 + 证据边界加两条口径警告 + `36/36`→`37/37` |
| 加口径警告 | [preparation.md](../ideas/preparation.md) §6.1「读法」加第四条（EPDMS 两套实现）与 EC 那条 |
| 计数同步 | [index.md](../index.md) §E VLA 侧 6→8 |
| 状态 / 索引 | [state.md](../state.md)（当前阶段、卷数）、[history.md](../history.md)（21→**22** 卷）、[README.md](../../../README.md) |
| 中间产物 | 本轮**未产生**新中间产物（纯检索与就地更正） |

**验证**：`check_links.py` **七项全绿**，退出码 0。

**一句话**：**前四轮挖出的结论本身是对的，但"结论对"不等于"工作空间里每处都改了"——这轮把四条结论当成搜索条件全库扫了一遍，抓到 1 处真错误（把正确的 docstring 判成了错的）、1 处传播漏（研究对象表还写着"没有代码"）、2 处计数 stale，并把口径警告写到了读者真正会抄数字的那两张表上。**
