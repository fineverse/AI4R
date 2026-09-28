# 第三十六轮（2026-09-24）· 路线 ② 的起点重估 + `judgments.md` 拆册

**动因**：第三十五轮末尾记着"如果继续，会沿着**从已核验事实里挖推论**这条线走，而不是继续做结构检查"。本轮就查**路线 ② 的起点选得对不对**——[sota-plan.md §5.3](../ideas/sota-plan.md) 与 §7.3 都写"冻结一个有代码的生成器（**DIVER 43.4 / DiffVLA 45.0**）"，但**这两个候选的发布代码从未被核过**：DIVER 只核过"论文 vs 代码"的主张对照（[C003 §G](../code/traces/diffusion_planner_code_traces.md)），DiffVLA 的代码状态**只有一句子代理的转述**（"真实现（36★）"，[sota-plan.md §1](../ideas/sota-plan.md) 是它唯一来源，且**不在 `code/repositories.md` 里**）。

## 做法

对三个候选（DIVER / DiffVLA / DiffusionDrive）用 **L3 取证**（GitHub API + `raw.githubusercontent.com` 逐文件，**不克隆**）核到文件级：仓库元数据 → 根目录 → agent 目录 → 活跃头文件 → 配置 → `forward_test` 的选路逻辑。同时顺带核了 VLA-06/07 两篇笔记的"代码"字段。

## 结论（含更正）

### 1. **最要紧的新发现：DiffVLA 的发布代码里没有论文的那个扩散头**

`sota-plan.md §1` 写"DiffVLA 45.0 = **有代码的纯扩散规划器**"。核完发现**这句话站不住**：

- **仓库自述**：`boschresearch/DiffVLA`（36★ / Apache-2.0 / 44 MB / 最后推送 2025-12-08）README **§5「Notifications」**原文——"The released version has some modifications compared to the paper on arXiv: 1. The trajectory head has been updated from **Diffusion Drive** to a self-developed **Transformer-based Trajectory Head**. 2. A **reward loss** derived from multiple EPDM sub-metrics has been introduced."
- **代码级印证**：`navsim/agents/diffvla/` 下**活跃头是 `trajectory_head_reward.py`**，**该目录里没有任何扩散轨迹头文件**；`modules/` 只剩 `conditional_unet1d.py` 与 `scheduler.py` 两件扩散残件；`diffvla_config.py` 的 `diff_loss_weight = 20.0` 仍在但**不被活跃头使用**；`num_voc = 8192`（论文写 N_anchor = 32）。
- **它其实是一个"选优器"**：`RewardHead` 按 **nc/dac/ddc/tlc/ep/tc/lk/hc 八个 EPDM 子指标**各出一个头，损失 `compute_reward_loss` 是 **BCE against 离线 GT 标签**（监督来自 `pdm_scores_8192`，由仓库脚本 `gen_multi_trajs_pdm_score_ours.py` 生成）；`forward_test` 里 `combined_score = w1·cls + w2·nc + w3·dac + w4·(5tc+2lk) + w5·ddc`（**`w = [1.0, 4.0, 1.2, 0.02, 8.0]` 手调常数**）后 `argmax` 选一条，且 **`ep`/`hc` 算了但没进最终分**。

→ **"45.0 = 有代码的纯扩散规划器 SOTA"不成立**（45.0 是**论文里带扩散头**的竞赛成绩，发布版**未报告任何分数**）；**"有代码的纯扩散规划器"这个子榜在"发布代码"口径下为空**（DIVER 43.4 的代码在 `forward` 里有 **4 处未注释 `pdb.set_trace()`**、且锚点未发布 → 也跑不通）。

→ 这是**第八类"名字≠实际"陷阱**：不是"配置关掉了机制"，不是"机制落在评测没 import 的版本里"（第七类，GuideFlow），而是**发布代码里根本没有论文那个机制**。→ **已写入 [judgments.md §C](../judgments.md) 新增一条**，并给 §B 的"榜上 SOTA ≠ 可复现 SOTA"那条补上 ⚠ 更正。

### 2. **路线 ② 的起点应改为 DiffusionDrive 24.2**

| 候选 | 有真扩散生成器 | 锚点 / 词表 | 代码可跑 | 候选池 | 判定 |
|---|---|---|---|---|---|
| DIVER 43.4 | 是 | **未发布**（0 个 `.npy`，需自建 **(6,6,6,2)** 且依赖 Bench2Drive） | **否**（4 处 `pdb.set_trace()`） | 6 | 排除 |
| DiffVLA 45.0 | **否**（头被换掉） | 已发布（**9 档** 32–8192） | 是 | 8192 | 排除（无可冻结的生成器） |
| **DiffusionDrive 24.2** | **是** | **公开可得**（Release 资产 **(20,8,2)**，与 V2 **逐字节相同**，[C005 §H.3](../code/traces/e2e_trunk_code_traces.md)） | 是（L1 逐文件核验） | **20** | **✅ 建议起点** |

**并指出起点选定后的第一个坑**：DiffusionDrive 候选池只有 **20** 条（vs DriveFuture 100 / DiffVLA 发布版 8192）→ 按 §7.2 条件②，"**上限由候选池决定**"，**从 24.2 出发不能指望 +20.9**；正确顺序是"**先把候选池做大，再做选优**"。

### 3. **正向增益：发布版 DiffVLA 是方向 B 最合适的载体**

它正好是"**离线 GT 打分监督的选择器**"的**第 4 个代码级实例**（前三个：WoTE 的 PDM 子指标 / Drive-OccWorld 的 GT 占据 / World4Drive 的 GT FDE），而且**有代码、可运行、候选池 8192**（比 DriveFuture 的 100 还大）→ 把 §5.3 的"自圆其说"从"三种实例"抬到**四种**，且有了一个**可直接改造的载体**。这条是"从已核验事实里挖推论"的直接产出。

### 4. **顺带更正：VLA 侧两处"未见官方代码"都是错的**

- **VLA-06 DiffVLA**：笔记写"未见官方代码"（第 5 行 + 待核验第 38 行）→ **有官方代码**，并新增「代码核验」节。
- **VLA-07 ReCogDrive**：笔记写"论文未在正文给出仓库"（**论文正文确实没给**，但仓库已发布）→ **[xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive)，611★ / ICLR 2026 / 2026-09-22 仍在更新**，且**研究对象侧早已做过代码级核验**（[C003 §M](../code/traces/diffusion_planner_code_traces-2.md)）。→ 笔记两处 + `vla/papers.md` 两行 + `code/repositories.md §E` 两行。
- **VLA-08 KnowDiffuser**：GitHub 搜索 **0 结果** → "未见"成立。
- **连带更正 [E2E-10](../direction/notes/E2E-10-drivevlm.md) 第 33 行**："VLA-06/07/08 三篇同样'未见官方代码'……**VLA 侧的代码级核验目前整体为空白**"——**2/3 有代码，且 VLA 侧已有 14 篇源码核验** → "整体空白"不成立，**真正空白的是"VLM as Explainer"这一个阶段**。
- **计数同步**：VLA 侧源码核验 **13 → 14 篇**（`vla/papers.md` ×2、`vla/README.md` ×2、`index.md`、`state.md`、`judgments.md §A` 共 7 处；VLA+WM 合计 **27 → 28**）。`vla/verification.md` 新增 **§4.4** 记这一篇（并写明 ReCogDrive 的核验在研究对象侧、**不重复计入**）。

### 5. **顺带查出两处 stale**

- `code/repositories.md` 第 163 行仍写"VADv2 的 4096 词表与 DiffusionDrive 的 20 锚点**都不在公开仓库里**，复现基线前必须先解决词表重建"——**已被 [C005 §H/§H.3](../code/traces/e2e_trunk_code_traces.md) 的实测推翻**（§H 的结论是"这个阻塞被大幅高估"）。→ 就地加 ⚠ 更正并指向待续清单第 10 项。
- `index.md` 写"history.md（索引 + **9 卷**正文）"——**实为 17 卷**（本轮后 18 卷）。→ 已改。

### 6. **`judgments.md` 按既定约定拆册**（关闭待续清单第 15 项）

第三十五轮预警"62.8 KB 即将撞 64 KB"，且 `state.md` 待续清单第 15 项规定"**下次往 A–H 任一组加判断前，先拆册**"。本轮要加判断 → **先拆**：

- 拆点取**章节边界**（非体积均分）：`judgments.md` = **第一册 §A–§D**（30999 B / 63 行 / 28 条），`judgments-2.md` = **第二册 §E–§H**（32604 B / 51 行 / 31 条）。
- **选"§A–§D 留第一册"的用意**：**所有现有 `§A–§D` 引用都不用改**——实测只需改 **3 处**指向 §F/§H 的引用（`preparation.md` S30、`rounds-26.md` ×2）。
- **安全**：改动前 `cp` 到 `/tmp/ai4r/judgments_bak_36.md`；脚本只做机械搬运，**正文一字未动**；拆前后体积 62836 → 30999+32604（增量 = 新表头 + 索引表新增的"册"列）；**自证**：正文 bullet 数 28+31 = **59**（= 拆分前总数）。
- **索引表加"册"列**，并同步 `state.md`（索引表 + 第 44 行）、`index.md`、`AGENTS.md`（入口文件表）、`shared/workspace-design.md`（拆分台账新增"第四次"）。
- **新增判断 1 条**（C 组：第八类陷阱）→ **59 → 60 条**，同步 3 处（`judgments.md` 索引表 C 行、节标题、`state.md` 索引表 C 行）。

## 产出

| 类别 | 文件与章节 |
|---|---|
| 新增分册 | [judgments-2.md](../judgments-2.md)（第二册 §E–§H）；[judgments.md](../judgments.md) 改为第一册（§A–§D）+ 加"册"列索引表 |
| 判断边界 | [judgments.md §C](../judgments.md) 新增"第八类陷阱"条（59→**60** 条）；§B 的"榜上 SOTA ≠ 可复现 SOTA"补 ⚠ 更正 |
| 冲 SOTA 文件 | [sota-plan.md](../ideas/sota-plan.md) **新增 §7.6（含 §7.6.1 / §7.6.2）**；更正 §1 DiffVLA 行、§2 第 4 条、§3 子榜表、§5.1 第①层、§5.3、§7.5 第①层；文件头更新时间 |
| 笔记 | [VLA-06](../topics/vla/notes/VLA-06-diffvla.md) 代码字段 + **新增「代码核验」节** + 待核验重写；[VLA-07](../topics/vla/notes/VLA-07-recogdrive.md) 代码字段 + 待核验作废条；[E2E-10](../direction/notes/E2E-10-drivevlm.md) 第 33 行 |
| 论文表 / 代码清单 | [vla/papers.md](../topics/vla/papers.md)（VLA-06/07 行 + §2 证据边界 ×2）、[vla/verification.md](../topics/vla/verification.md)（**新增 §4.4**）、[code/repositories.md](../code/repositories.md)（§E 新增 2 行 + 节头 + 第 163 行 ⚠ 更正） |
| 状态 / 索引 | [state.md](../state.md)（当前阶段、待续清单第 15 项关闭、索引表加"册"、判断条数、VLA 计数）、[history.md](../history.md)（17→**18** 卷）、[README.md](../../../README.md)、[index.md](../index.md)（+ 修"9 卷"stale） |
| 工作流 / 设计 | [AGENTS.md](../../../AGENTS.md)（`judgments.md` 入口行）、[shared/workspace-design.md](../../../shared/workspace-design.md)（拆分台账"第四次"） |
| 备份 / 中间产物 | `/tmp/ai4r/judgments_bak_36.md`（拆分前备份）、`/tmp/ai4r/split_judgments_36.py`（拆分脚本）→ 已登记 [inbox/cleanup.md](../../../inbox/cleanup.md) |

**验证**：`check_links.py` **七项全绿**（126 个 md、死链 0、表格 0 错、孤儿 0 / 弱引用 0、**分册错册引用 0**、笔记必写节 0 缺、小方向 README 0 缺），退出码 0。

**一句话**：**这轮把路线 ② 的起点从一个"看起来有代码"的名字（DiffVLA 45.0）换成了真正能跑的东西（DiffusionDrive 24.2），同时发现"榜上那个 45.0"在发布代码里根本不存在——而发布版本身恰好是方向 B 想要的那个"离线 GT 打分选择器"。**
