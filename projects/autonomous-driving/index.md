# 自动驾驶项目索引

> **大方向**：端到端自动驾驶。**小方向**见 `topics/`：`diffusion-planner`（研究对象）、`vla`、`world-model`（借鉴来源）。
> **具身智能**是平级领域，独立成项目，见 [embodied-ai/index.md](../embodied-ai/index.md)。

## 项目入口

- [项目定义](project.md)
- [研究上下文与约束](context.md)
- [当前状态](state.md)（当前阶段 / 待续清单 / 判断边界**索引**）
- [判断边界（详细）](judgments.md)（每条判断的完整论证、出处与代码事实；**第一册 §A–§D**）+ [judgments-2.md](judgments-2.md)（**第二册 §E–§H**）
- [逐轮工作记录](history.md)（**索引 + 60 卷正文**：每轮做了什么、更正了什么、产出在哪）+ [CURRENT.md](history/CURRENT.md)（**并行会话同步（软通道，单写者）**：本轮在改文件清单；投递物登记表就是 `inbox/` 本身）
- [工作空间设计](../../shared/workspace-design.md)

## 大方向层 `direction/`

| 文件 | 内容 |
|---|---|
| [lineage.md](direction/lineage.md) | 端到端自动驾驶发展脉络（1989→2026，四阶段 + 三条轴 + **继承关系（代码层面已核验，S1–S4 分级）**） |
| [benchmarks.md](direction/benchmarks.md) | 基准与评价协议（NAVSIM v1/v2、Bench2Drive、nuPlan、nuScenes 等）+ **PDMS/EPDMS 的代码级口径**（§2）+ **§2.5 Agent 与评测接口** + **§2.6 nuPlan 闭环分数的代码级口径**（`final_score = (4 项乘性连乘) × [Σw·m / Σw]`；与 PDMS 结构不同、且分母依赖配置） + **§2.7 Bench2Drive 四项指标的代码级口径**（DS = `max(RC × IS, 0)` 且分母硬编码 220；SR = 零违规完成率；5 项 Ability；**Effi 是速度比、Comf 是时间占比**） + **§2.8 nuScenes 开环的代码级口径**（**同名 L2/碰撞在 UniAD / VAD / VADv2 / SparseDrive 里是四套不同实现**；UniAD 代码里有 `uniad` / `stp3` 两套 L2 定义） |
| [surveys/](direction/surveys) | E2E 综述大表（S001–S045）+ CSV |
| [notes/](direction/notes) | 领域级笔记 **16 篇**（E2E 代表工作 11 + 综述 S001/S002/S031/S032/S033） |

## 小方向层 `topics/`

### diffusion-planner —— 研究对象

| 文件 | 内容 |
|---|---|
| [README.md](topics/diffusion-planner/README.md) | 角色、边界、进度 |
| [lineage.md](topics/diffusion-planner/lineage.md) | 扩散规划器发展脉络（2022→2026，五阶段 + 三次转移 + **继承关系（S1–S4 分级）**） |
| [transfer.md](topics/diffusion-planner/transfer.md) | 来源 → 对象 的可借鉴机制表（待验证假设） |
| [papers/](topics/diffusion-planner/papers) | AD 扩散规划器论文表（DP-A01–A34）+ CSV；**[navhard 竞品登记表](topics/diffusion-planner/papers/navhard_competitors.md)**（DP-C01–C07：非扩散 / 选择式**对手**，含逐行代码状态；**第七十轮更正 DP-C01 并新增 C06/C07**）；**[选优器 / 候选池专线](topics/diffusion-planner/papers/scoring_line.md)**（方向 B 的文献地基：4 条**摘要级**已核 + 15 条线索级，含 TOAD / Vault 两篇强对手） |
| [surveys/](topics/diffusion-planner/surveys) | 扩散规划器综述表（DP-S01–S15）+ CSV |
| [notes/](topics/diffusion-planner/notes) | 单篇笔记 **14 篇**（DP-A×12 + DP-S11/DP-S15） |

### 借鉴来源

| 小方向 | 状态 |
|---|---|
| [vla/](topics/vla) | [README.md](topics/vla/README.md) — [论文表 **28 篇**](topics/vla/papers.md)（表 + 证据边界 + 边界外清单，**轻量入口**）+ [脉络](topics/vla/lineage.md)（四阶段 + **继承关系（论文级）**）+ 3 篇 [notes/](topics/vla/notes)；**逐篇全文与代码核验结论拆到两册**：[verification.md](topics/vla/verification.md)（§4–§8）、[verification-2.md](topics/vla/verification-2.md)（§9–§14）→ **28/28 已读全文、14 篇已源码核验、28 篇全部核过代码可用性** |
| [world-model/](topics/world-model) | [README.md](topics/world-model/README.md) — [论文表 **24 篇**](topics/world-model/papers.md)（表 + 证据边界 + 补录 + 代码可用性全表）+ [脉络](topics/world-model/lineage.md)（五类空间 + **五条接口路线** + **继承关系（代码层面已核验）**）+ 5 篇 [notes/](topics/world-model/notes)；**§4 逐篇全文核验结论拆到** [verification.md](topics/world-model/verification.md) → **24/24 已读全文、14 篇已源码核验** |

> 两个借鉴来源的可迁移机制汇总在 [transfer.md](topics/diffusion-planner/transfer.md) 第 2、3 节。质量筛选口径见 [shared/literature-quality.md](../../shared/literature-quality.md)。

## 代码（跨专题，位于项目根）

| 位置 | 内容 |
|---|---|
| [code/repositories.md](code/repositories.md) | 官方代码快照清单（**37 个仓库 + commit**，约 1.65 GB，未安装未运行）；**§D/§D.1 世界模型侧在列 12 个**（4 个已落盘 + 8 个未落盘走 raw 取证；其中 **WoTE / DriveLaW / Drive-OccWorld / World4Drive / LAW 已逐文件核验**）、**§E VLA 侧在列 8 个**（`OpenDriveVLA` 已落盘 / 其余 7 个走 API 取证；**第三十六轮补 DiffVLA 与 recogdrive 两行**） |
| [code/traces/](code/traces) | 三份代码脉络（**两份已拆册**，因单文件超 Read 工具 64 KB 上限）：[扩散规划器侧](code/traces/diffusion_planner_code_traces.md)（§A–§H）+ [第二册](code/traces/diffusion_planner_code_traces-2.md)（§I–§P：PC-Diffuser / HDP / DriveFine / Flow Planner / ReCogDrive / GuideFlow / LCS+BridgeDrive / MPDiffuser+DIPOLE）→ **研究对象侧 13 个仓库全部结账：12 逐文件核验 + 1 零代码**；[世界模型→规划器接口](code/traces/world_model_code_traces.md)（§E WoTE / §G DriveLaW / §H 判断 / §I Drive-OccWorld·World4Drive·LAW / §J DrivingGen）；[E2E 主干](code/traces/e2e_trunk_code_traces.md)（§A–§J）+ [第二册](code/traces/e2e_trunk_code_traces-2.md)（§K–§M：CARLA 系 6 基线 / TransFuser·TCP·ST-P3 / LBC·CIL·NEAT·DriveLM） |
| `code/repos/` | 仓库快照本体（约 1.65 GB，按需读取，**勿全量扫描**） |

> 注：`code/` 含 13 个研究对象仓库、13 个领域级 E2E 主干仓库、6 个具身侧仓库、4 个世界模型侧仓库、**1 个 VLA 侧仓库**，**跨三层**，故放项目根而非某个小方向下。

## 跨专题

- [sources.md](sources.md) — 来源索引（论文、仓库、基准，编号 L/C/B/P）
- [pdfs_pending.md](pdfs_pending.md) — 付费墙 PDF 8 条（需你下载）
- [raw/](raw) — 检索日志
- [ideas/sota-plan.md](ideas/sota-plan.md) — **冲 SOTA 作战文件**（navhard 分数格局（**§1.0 官方公开榜 20 行** + §1 论文口径 13 行）与逐行代码状态、子榜门槛、七方向重排、四条推荐路线；**2026-09-24 从 `preparation.md §5.1` 拆出**）
- [ideas/preparation.md](ideas/preparation.md) — idea 讨论准备材料（研究地图、9 个未解决问题、7 个潜在方向 + **§5.0 七方向横向比较** + **§7 四项待拍板、已给默认值**）；`candidates.md` / `rejected.md` 在正式形成候选后创建
- [ideas/recombination-map.md](ideas/recombination-map.md) — **重组地图：结构（代码血统）× 因果（受控增益）**（**只做连接、不复制论证**：结构指各 `lineage §继承关系`、因果指 `sota-plan §7–§9` / `judgments` / `transfer`；含"结构相邻但因果未测"的 idea 候选区）
- 阅读顺序：综述 S001 → S019 → S032；论文 DP-A02 → DP-A01 → DP-A09 → DP-A14 → DP-A31

## 实验与写作

| 目录 | 内容 |
|---|---|
| [experiments/protocol.md](experiments/protocol.md) | **路线 B 第一阶段预注册协议**：冻结 DiffusionDrive，测 floor / selected / oracle ceiling / 扩池 ceiling；尚未运行 |
| `experiments/records/`、`experiments/results/`、`writing/outline.md` | **尚未建立**——协议已就绪、实验未运行，这三个位置待实验启动后再创建。**注**：`experiments/records` 与 `results` 在文件系统里是**有意空目录占位**（git 不跟踪空目录，clone 恢复后需重建；`writing/` 未建），见 [inbox/cleanup.md](../../inbox/cleanup.md) §不在清理范围 |
