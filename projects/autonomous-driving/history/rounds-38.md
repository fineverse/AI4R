# 第三十八轮（2026-09-24）· EPDMS 有两套官方实现——53.2 的谜底

**动因**：第三十七轮把"SimScale 的 53.2 出自哪里"记成**待核**（论文与仓库最高都是 48.0，53.2 在其论文全文里查不到）。而 §1 那张 13 行表是**全项目所有门槛的唯一来源**，其中一行对不上就不该放着。本轮先去拿**权威源（官方 navhard 排行榜）**。

## 做法

1. **探权威源**：官方榜在 HF（`AGC2025/e2e-driving-navhard`）。**`huggingface.co` 在本沙箱内不可达**（`http 000`；`opendrivelab.com` / `arxiv.org` / GitHub 均可达）→ **排行榜这条路走不通**，记为环境限制。
2. **改从可达的 arXiv 拿原文**：下载 **DriveFuture（2605.09701）PDF**（9.4 MB）`pdftotext -layout`，逐表核它的 Table 1 题注与正文。

## 结论（含更正）

### 1. **谜底：53.2 与 48.0 是两套官方实现，不是错误**

DriveFuture **§3.3 原文**：

> "We distinguish between **EPDMS\*** and **EPDMS** when reporting NAVSIM-v2 results. **EPDMS\* denotes scores computed with the earlier NAVSIM-v2 evaluation implementation before the human-behavior filtering fix was adopted in the official leaderboard.** It preserves the same extended metric set as Eq. (18), but may penalize the agent for violations that are also present in the human reference behavior. **EPDMS denotes the corrected official implementation** … EPDMS\* is reported only for compatibility with earlier results computed using the legacy code."

修复逻辑（§3.3）："**ignores a rule violation if the same violation is also committed by the human trajectory** in the corresponding scene, reducing **false penalties** caused by annotation noise or contextually necessary maneuvers." → **只减不增扣分 → 修复后系统性偏高。**

→ **SimScale 自报的 48.0 是旧实现（`EPDMS*`）**（2025-11 的论文，早于修复）；**DriveFuture 表里的 53.2 是新实现（`EPDMS`）**。逐阶段子指标显示**两行是同一个 V2-99 模型**（NC 94.5↔94.9、DAC 94.2↔94.3、TLC 99.2↔99.3 几乎相同），差别集中在 **EC 43.2 ↔ 30.9**。

**实测幅度**（DriveFuture Table 2 是唯一同时给两列的地方）：**DriveFuture 自己 86.4 → 89.9（+3.5）**、**DiffusionDriveV2 85.5 → 87.5（+2.0）**。

### 2. **本工作空间其实早已核到"这条修复"，只是不知道它是"修复"**

`benchmarks.md §2.3` 第 4 条**第十一轮就写下了**：

> 4. 加入**假阳性过滤** `filter_m(agent, human)`：若人类驾驶在该指标上也为 0，则该指标对 agent 记 1.0

——代码侧的 `filter_m` 早就在册，**缺的是"它是后来才被官方榜采纳的、因此存在修复前后两套实现"这一层**。→ **这是本轮最典型的"消化"形态：两半证据各自都在，合起来才成结论。**

### 3. 后果（已写入四个文件）

1. **`§1` 的表是一个"口径混装集"**：DriveFuture 的行是 `EPDMS`（新），各论文自报的行多是 `EPDMS*`（旧）→ **列内排序可用，行间分数差不可当精度用**。§1 已加显著标注。
2. **`§3` 子榜里"SimScale 53.2"改回可用**（不是"来源不明"，是"新实现口径"），并与 48.0 并列注明。
3. **P8 实例 ③（DiffusionDrive 的 v2 navtest 88.3 vs 84.5）多了一个候选解释**：两套实现之差（2.0–3.5）与那个 3.8 分差**同量级** → **未必是某家测错，拿到实现版本前不宜归因**。
4. **"DiffusionDriveV2 的 85.5 在两表完全一致 → 最可信跨论文锚点"这条要加限定**：DriveFuture 把 **85.5 列在 `EPDMS*` 一栏**（其 `EPDMS` 是 **87.5**）→ **两表一致的其实是"旧实现"口径**。

### 4. **顺带拿到两条原文事实**

- **EPDMS 的结构**（与我们的代码级核验一致，可交叉验证）：乘性惩罚项 **M_pen = {NC, DAC, DDC, TLC}**、加权平均项 **M_avg = {EP, TTC, LK, HC, EC}**，默认权重 **β_EP = β_TTC = 5、β_LK = β_HC = β_EC = 2**。
- **作者自己写明了"选优压低 EC"这个 trade-off**（§D.1 原文）："**The lower EC value for the scored model indicates a known trade-off in NAVSIM-style planning** … **Since EPDMS uses multiplicative penalties for safety-critical metrics, the safety and compliance improvements dominate the final score.**" → **这给了第三十七轮那条 EC 观察一个作者级的机制解释**（根因是 **EPDMS 的结构本身**，不是某家的实现问题），且 DriveFuture 自己的 Table 7 也是同一形态（加 scorer 使 Stage-2 **EC 75.9 → 45.6**，总分 **30.9 → 55.5**）。

### 5. 环境限制（需记下）

**`huggingface.co` 在本沙箱内不可达** → 官方 navhard 排行榜（`AGC2025/e2e-driving-navhard`）**无法核对**。这影响两件事：① 本轮的"53.2 待核"只能用**论文原文**间接关闭（已关闭）；② **将来若要核对官方榜、或下载 SimScale / GTRS 的 checkpoint（都在 HF），必须由用户协助或调整沙箱设置**。已记入 [state.md](../state.md) 待续清单。

## 产出

| 类别 | 文件与章节 |
|---|---|
| 基准口径 | [benchmarks.md](../direction/benchmarks.md) **新增 §2.9（§2.9.1–§2.9.2）**——第三套"跨论文不可比"机制；§2.3 第 4 条补"这是后来才采纳的修复"；§2.4 末尾加指针 |
| 判断边界 | [judgments.md §B](../judgments.md) 新增 1 条（B 组 8 → **9**，总数 61 → **62**）；§B 旧条里"85.5 最可信锚点"加限定 |
| 冲 SOTA 文件 | [sota-plan.md](../ideas/sota-plan.md) **新增 §7.7.5**；§1 加"口径混装集"显著标注 + SimScale 行改写；§3 子榜；§6 关闭"53.2 待核"；文件头 |
| 笔记 | [DP-A31 DriveFuture](../topics/diffusion-planner/notes/DP-A31-drivefuture.md) 修正 `EPDMS*` 的记法 + **新增「口径与代码核验」节** + 「对本项目的意义」补一条 |
| 设计前提 / 问题 | [preparation.md](../ideas/preparation.md) **P2c 补作者级机制解释**、**P8 实例 ③ 补候选解释** |
| 状态 / 索引 | [state.md](../state.md)（当前阶段、索引表 B 行、条数 62、**待续清单新增第 17 项：HF 不可达**）、[history.md](../history.md)（19→**20** 卷）、[index.md](../index.md)、[README.md](../../../README.md) |
| 中间产物 | `/tmp/ai4r/df.pdf`（9.4 MB）+ `df.txt` → 已登记 [inbox/cleanup.md](../../../inbox/cleanup.md) |

**验证**：`check_links.py` **七项全绿**，退出码 0。

**一句话**：**上一轮发现"榜上那个 53.2 在论文里查不到"；这一轮发现它不是错误，而是"官方榜修了一个假阳性过滤"造成的口径差——而这个过滤，本工作空间第十一轮就从代码里抄下来过，只是当时不知道它是"修复"。**
