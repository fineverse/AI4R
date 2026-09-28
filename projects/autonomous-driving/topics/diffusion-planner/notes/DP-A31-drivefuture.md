# DP-A31 · DriveFuture（当前 navhard 榜首）

- **原题**：DriveFuture: Future-Aware Latent World Models for Autonomous Driving
- **作者/载体**：Yufeng Hong 等；arXiv [2605.09701](https://arxiv.org/abs/2605.09701) v1（2026-05-10）；24 页
- **代码**：未核验
- **证据等级**：全文（PDF + `pdftotext -layout` 表格核验）
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> ...existing latent world models typically treat future latent states as prediction targets or auxiliary signals, rather than directly conditioning trajectory planning. This can entangle current and future features in latent space. In this work, we propose DriveFuture... conditioning the current latent state modeling process on future world states.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 核心主张 | 现有潜世界模型把未来潜状态当作**预测目标或辅助信号**，而非规划条件，导致当前/未来特征在潜空间纠缠 | 摘要 |
| 方法 | 训练时先从当前潜状态 + ego 动作预测未来潜状态，再用 cross-attention 对 GT 未来潜状态精修；结果条件化轨迹规划 | 摘要 |
| NAVSIM v2 **navhard** EPDMS | **55.5，表内最高**（Stage1 各分量 99.8/99.8/100/99.6/85.7/99.8/98.7/97.6/66.2；Stage2 90.6/87.5/94.1/99.1/84.6/88.8/58.3/93.5/45.6） | Table 1（PDF 核验） |
| navhard 同表对比 | DrivoR 54.6、SimScale 53.2、GTRS-E 49.4、ZTRS 48.1、DiffVLA 45.0、DriveSuprim 42.1、World4Drive 34.9、MindDrive 30.9、GuideFlow 27.1、**DiffusionDrive 24.2**、TransFuser 23.1 | Table 1（PDF 核验） |
| NAVSIM v2 navtest EPDMS | **89.9**（同表另有 **`EPDMS*` 86.4**——**两套官方实现**，见下）；同表 Latent-WAM 89.3、DiffusionDriveV2 **87.5**（其 `EPDMS*` 为 **85.5**）、DriveWorld-VLA 86.8 | Table 2（PDF 核验） |
| NAVSIM v1 navtest PDMS | **90.7**（NC 98.8 / DAC 99.1 / TTC 95.4 / Conf 100 / EP 84.2）；同表 DriveWorld-VLA 91.3、GoalFlow 90.3、人类 94.8 | Table 3（PDF 核验） |
| 消融（**navhard，不含 scorer**，第二十四轮核实） | 基线（仅 GT）**30.9** → FF+MSE+KS+GT **32.1** → FF+Impl 32.0 → **FF+Impl+KS+GT 34.6**；Table 5：tf=1.5 / qs=16 / eo=0.83 均为 34.6 | Table 4/5（PDF 核验 + 第二十四轮全文复核） |
| 规划器实现 | **条件扩散（DDPM，Diffusion Transformer，5 层）**，默认**采样 100 条候选 + GTRS-Dense 选优**；**去噪步数论文未给** | §4.2 |
| 接口位 | **②隐状态级条件**：世界模型输出未来感知潜状态 Z̃（**16 个 future query token，d=256**），作为额外上下文喂进去噪器 `ε_θ(a_s, s, C_scene, Z̃)`；训练与推理都接线（推理 bypass adapter 用预测值） | 摘要、§3.3–3.4 |

## 对本项目的意义

- 它代表了"条件来源"这条轴的最新进展：把**未来潜状态**从辅助损失升级为生成条件，与 GoalFlow 的 goal point、VLM 类的语言条件形成对照。论文自己做了"**条件化 vs 辅助损失**"的显式对照：**条件化 34.6 vs 直接 future-latent MSE 32.1（+2.5）**（Table 4）。
- **⚠ 第二十四轮更正（重要）**：本笔记此前写的"navhard 上 DiffusionDrive 24.2 vs DriveFuture 55.5，差距超过 2×"是**误读**——**这两个数字是同一张表（Table 1，navhard SOTA 对比）里的两行不同方法**，且 **55.5 含 GTRS-Dense scorer**，而 **Table 4 的受控消融不含 scorer**。→ **"加未来条件"的受控收益只有约 +3.7（30.9→34.6），不是 +31.3**；"24.2→55.5"混入了**换方法 + 换选优器**两重差异。**修正后仍成立的两条**：
  1. navtest 上的 88–91 分区间已经饱和，**navhard（长尾/困难）才是区分度所在**；
  2. **同表内方法间差距（24.2→55.5）远大于同一方法内改条件带来的差距（+3.7）** → 但前者的归因**不明确**（方法、主干、选优器都在变），**不能用来支持"改条件比改生成机制更重要"**。
- 对 idea 讨论的直接含义（**修正后**）：navhard 上的高分离不开**选优器**（DriveFuture 的 55.5 与 WoTE 的 88.3/87.1 都靠 scorer）→ **"选优器"这一环在困难基准上的权重可能比"条件"更大**；且 **DriveFuture 的"未来条件"与 GT 未来监督纠缠**（训练用 GT 未来 cross-attention + LatentAlign），"纯条件收益"难以完全剥离。
- **⚠ 第三十八轮新增**：**本笔记是"EPDMS 有两套官方实现"这条口径发现的来源**——本工作空间的 v2 EPDMS 数字此前是一个**混装集**，引用前必须问"旧实现还是新实现"（见 [benchmarks.md §2.9](../../../direction/benchmarks.md)）。**且作者自己给了 P2c 的机制解释**：EPDMS 的乘性安全项主导总分，所以**选优 / 合规的收益会盖过 EC 的损失** → 本项目若要"提分"，**舒适性会是被牺牲的那一项**，必须在论文里主动报告，而不是等 reviewer 指出。

## 口径与代码核验（2026-09-24 第三十八轮，PDF 逐表核验）

**最要紧的一条：这篇论文定义了 NAVSIM-v2 的两套官方实现，而本工作空间此前只知其一半。**

- **`EPDMS*`** = **旧实现**（§3.3 原文 "computed with the earlier NAVSIM-v2 evaluation implementation **before the human-behavior filtering fix was adopted in the official leaderboard**"）
- **`EPDMS`** = **修好后的官方实现**（"the corrected official implementation"），本文把它作为**主口径**，`EPDMS*` 只"for compatibility with earlier results"
- 修复逻辑（§3.3 原文）："**ignores a rule violation if the same violation is also committed by the human trajectory** in the corresponding scene, reducing false penalties" → **只减不增扣分，所以修复后系统性偏高**
- **`benchmarks.md §2.3` 第 4 条那个 `filter_m` 就是这条修复**——本工作空间第十一轮从代码里核到了它，但**不知道它是"后来才被官方榜采纳的"**
- 本文 Table 2（navtest）**同时给两列**，是目前唯一能直接量化的地方：**本文自己 86.4 → 89.9（+3.5）**、**DiffusionDriveV2 85.5 → 87.5（+2.0）**
- **navhard 侧的实例**：SimScale 自报 **48.0（旧）** vs 本文表记 **53.2（新）** → 差 **5.2**（见 [sota-plan.md §7.7.5](../../../ideas/sota-plan.md)）

**另外两条本轮补到的原文事实**：

- **EPDMS 的加权结构**（与我们的代码级核验一致，可交叉验证）：乘性惩罚项 **M_pen = {NC, DAC, DDC, TLC}**、加权平均项 **M_avg = {EP, TTC, LK, HC, EC}**，默认权重 **β_EP = β_TTC = 5、β_LK = β_HC = β_EC = 2**；Stage-2 用高斯核按"合成起点 ↔ Stage-1 终点"的距离加权（Eq. 19，与 `benchmarks.md §2.4` 的 `σ²=0.1` 一致）
- **本文自己写明了"选优会压低 EC"这个 trade-off**（§D.1 原文）："**The lower EC value for the scored model indicates a known trade-off in NAVSIM-style planning**: selecting safer and more rule-compliant proposals can reduce the extended comfort metric when the chosen trajectory is more conservative or involves stronger braking. **Since EPDMS uses multiplicative penalties for safety-critical metrics, the safety and compliance improvements dominate the final score.**" → **这是 P2c 的作者级解释**，也直接解释了第三十七轮在 SimScale 表上观察到的 **EC 79.6/72.8 → 59.6/31.9 而总分仍涨 5.1**。**本文自己的 Table 7 也是同一形态**：加 scorer 让 Stage-2 **EC 从 75.9 掉到 45.6**，而总分从 **30.9 升到 55.5**

## 待核验

- **世界模型自身的推理成本未报告**（100 条候选 + 世界模型前向的端到端延迟）。
- 是否有官方代码；world model 预训练成本与数据需求（可能显著高于纯规划器）。**已确认无官方代码**（全文只有 HuggingFace 排行榜链接）。
