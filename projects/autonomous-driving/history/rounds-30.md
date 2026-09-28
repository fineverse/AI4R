# 第三十轮（S1–S30 量化依据溯源 + 分册错册引用清账，2026-09-24）

**动因**：`ideas/preparation.md` §2 的 **S1–S30「设计前提清单」** 与 §6.1 的同基准对照表，是**即将进行的 idea 讨论的地基**——讨论时每条前提的"量化依据"会被直接引用。但这份清单的数字**从未被系统溯源核验**：第二十七至二十九轮改过论文表、`sota-plan.md`、`benchmarks.md`、具身表，`preparation.md` 未必跟着更新；前几轮只抽查改过 S9 / S19 / S30 三处。

## 1. 做法

派 **1 个只读子代理**做逐条溯源：把 S1–S30 的「量化依据」列里**每个数字**回溯到权威源（论文表 / 两册 `verification` / 三份代码脉络 / `benchmarks.md` / `judgments.md` / `sota-plan.md` / 具身表），判定四类：**一致 / 矛盾 / 找不到 / 口径错标**。同标准覆盖 §6.1（两张表）与 §2b；`judgments.md` 58 条另抽 21 条（覆盖 A–H 各组）核对数字与章节号。

## 2. 结论：数字本身已经对齐，问题全在"口径 / 名称 / 指针"

| 范围 | 一致 | 矛盾 | 找不到 | 口径错标 |
|---|---|---|---|---|
| S1–S30（30 条） | **29** | 0 | 0 | 1（S12） |
| §6.1（两张表） | 全部数字一致 | 0 | 1（"6 个"计数） | 1（名称拼写） |
| §2b | — | 0 | 0 | 1（出处列错标） |
| `judgments.md` 抽查 21 条 | **21** | 0 | 0 | 1 类 3 处（章节号指错册） |

→ **第二十八轮修的 S19 箭头方向、S9 的 navtest/navhard 混记、S30 的"八→九种"，以及第二十九轮修的 navhard 12→13 行，均已生效**。

## 3. 本轮最要紧的发现：**C005 的分册错册引用（13 处）**

第二十八轮修了 **C003** 的 §I–§P 错册引用 **52 处**，但**同一类坑在 C005（E2E 主干脉络）上被整批漏掉**——`e2e_trunk_code_traces.md` 只含 §A–§J，§K–§M 在拆出的 `-2.md`，而引用它们的链接**全部指向第一册**：

| 文件 | 处数 |
|---|---|
| `judgments.md` | 3 |
| `direction/lineage.md` | 2 |
| `code/traces/e2e_trunk_code_traces-2.md`（自指） | 3 |
| `ideas/preparation.md` | 2（其中 1 处是 §G/§K 混指，已拆成两个链接） |
| `history/rounds-24a.md` | 3 |

另修 **2 处 C003 第一册的内部散文引用**（`（见 §K）`、`加上 … §K`）——它们不是链接，死链检查抓不到。

**死链检查为什么抓不到**：文件确实存在，错的只是"**章节在哪一册**"。→ **把这项加进 [shared/scripts/check_links.py](../../../shared/scripts/check_links.py) 作为第五项「分册引用归属」**：对每组 `X.md` / `X-2.md`，解析两册的 `## §X` 标题，凡"链接文字里的 `§X` 只存在于另一册"即报错（第一册↔第二册双向都查）。这类坑**已踩两次**（C003 52 处、C005 13 处），自动化后不会再漏。

## 4. `preparation.md` 与源文件的内容修正（5 处 + 2 处源间不一致）

| # | 位置 | 问题 | 处理 |
|---|---|---|---|
| 1 | S12（`preparation.md` §2.3） | 把 **GuideFlow** 归入"**有硬约束**的方案"，但同文件 §2b 的四立场表明确把它列为"**生成内软引导（非硬约束）**"（DP-A12 无 QP/投影证书）——**自相矛盾** | 改为"**硬约束** PC-Diffuser 约 2 fps；**软引导** GuideFlow 3.6 FPS"，并就地标 ⚠ |
| 2 | §6.2（固定规则） | "UniAD 的 `uniad` / `stp3` 两套 L2 定义（**前缀累积平均 vs 单步值**）"——**顺序反**，且与 S29、[benchmarks.md §2.8.2](../direction/benchmarks.md) 矛盾（`stp3` = 前缀累积平均、`uniad` = 单步值） | 改为"**单步值 vs 前缀累积平均**"并补出处 |
| 3 | §2b（收敛结论表） | "安全保证未解"行的 **S031 列**写"无形式化安全保证（S001 §4.7）"，但 **S031 笔记通篇未涉及安全保证**（全文只有"交通安全"作为应用域） | 该格改为"**—（本综述未涉及）**"，并把 S001 §4.7 的出处保留在同一格里说明 |
| 4 | §6.1（第三方复评表） | 方法名写成 "**DriveSuprem**" | 改为 **DriveSuprim**，并注明"原文拼作 DriveSuprem"（该表转录自 ExploreVLA Table 2） |
| 5 | §6.1 表下注 | "上表只列了我们收集过的方法（**6 个**）"，但 navhard 列实际只有 **5** 个有值 | 改为 **5 个**并逐一列出 |

**两处"两个权威源本身不一致"（已就地收敛）**：

1. **GenAD 的类序**：`judgments.md §C` 与 S4 写"**第四类**"，C005 §J.5 写"**第三类**"——但 §J.5 紧接着的三个否定（单模回归 / 离散词表+分类 / 扩散）已占 1–3 位 → **第四类才对**，C005 §J.5 已改并标 ⚠。
2. **GoalFlow 的末步是"均值化"还是"选 1 条"**：S6 / `judgments.md` / C003 §F 都记"**对候选取均值**"（代码原文 `pred_trajs[:,:,1:1+8,:].mean(1)`），而 **DP-A09 行**写"生成 128/256 条**选 1 条**" → **论文表行是错的**，已改为"论文自述'选 1 条'；**代码实测为对候选维取均值**"，并指出这决定它属于"均值化"而非"选优"。

## 5. 产出与状态

- **改动文件**：`shared/scripts/check_links.py`（四项 → **五项**）、`ai/workflows.md` §轮次收尾、`shared/index.md`、`projects/autonomous-driving/ideas/preparation.md`、`judgments.md`、`direction/lineage.md`、`direction/benchmarks.md`（只读引用）、`topics/diffusion-planner/papers/diffusion_planner_ad.md`（DP-A09 行）、`code/traces/e2e_trunk_code_traces.md` + `-2.md`、`code/traces/diffusion_planner_code_traces.md`、`history/rounds-24a.md`、`history.md`、`state.md`、`README.md`
- **验证**：`check_links.py` **死链 0 / 行数超限 0 / 表格不匹配 0 / 孤儿 0 / 弱引用 0 / 错册引用 0 / 退出码 0**；所有 `index.md` / `state.md` ≤100 行；无第一方文档超 64 KB
- **待用户**（未变）：① **7.1 可用 GPU 与预算** ② **7.2 是否把"扩散规划器"升级为正式课题**
