# 选优器 / 候选池专线（方向 B 的文献地基）

更新时间：2026-09-30
**为什么单独成表**：方向 B（选优器）是本项目**主攻路线**（[sota-plan.md §8](../../../ideas/sota-plan.md)），此前这条线的直接先行工作**只有 [DP-A34](diffusion_planner_ad.md) 一篇**。2026-09-30 做了一次定向检索，发现**这条线并不空**，且有两篇强对手。为不把 idea 判断建在漏检的地基上，单独登记。

**证据等级**：
- **§一 = 摘要级（已独立复核）**：4 条的 **arXiv ID / 标题 / 关键数字**已于 2026-09-30（**第六十八轮**）由主线程 `WebFetch` 逐条读 arXiv abs 页**复核，逐字吻合**；**第六十九轮**又把 **TOAD 的 split 归属**核到**论文正文（全文级）**——**NAVSIM-v2 侧就是 `navhard-two-stage`**。其余仍为摘要级（方法细节、venue、有无代码未核，见各条 ⚠）；
- **§二 = 线索级**（子代理 `WebSearch/WebFetch` 检索所得，**arXiv ID / venue / 代码状态均未逐条核验**，引用前必须核）。

## 一、已核验（4 条，最可能重合；**摘要级**）

| 标题 | arXiv | 年 | venue | 官方代码 | 关键数字 | 与选优器的关系 |
|---|---|---|---|---|---|---|
| **TOAD** | [2606.07170](https://arxiv.org/abs/2606.07170) | 2026 | 预印本（valeo.ai） | 摘要称 "will be made publicly available"（**至第六十九轮仍未发布**） | **v1 94.7 PDMS / v2 56.3 EPDMS** | **把冻结 scorer 当轨迹级 reward，用 CEM 在测试时搜索**；plug-and-play、**无需重训**，跨 6 个 base planner 生效（Hydra-MDP / GTRS / ZTRS / iPad / RAP / DrivoR，**全用公开 ckpt**）。**✅ 第六十九轮已核（论文 §4.1 全文）**：**56.3 就是 navhard-two-stage** → **navhard 榜一由 DriveFuture 55.5 变为 TOAD+DrivoR 56.3**（只比 GT 感知的 PDM-Closed 56.6 低 0.3）；且**头部被压平**（六者原 34.7–54.6 → 搜后全落 49.0–56.3） |
| **Vault** | [2606.06219](https://arxiv.org/abs/2606.06219) | 2026 | 预印本（投 **ICLR 2027**，v2 = 2026-09-28） | 未提 | **v1 94.6 PDMS / v2 91.2 EPDMS** | one-step latent 生成 + **reward-gated 正样本池**（用官方评测器筛自身成功样本锚定）+ **学到的 scorer 预测官方分及其子指标**选一条。**"无策略梯度、无学到的奖励模型"** |
| **DriveVer** | [2607.00399](https://arxiv.org/abs/2607.00399) | 2026 | 预印本 | 未提 | 34M 验证器 | NAVSIM 上按**ego 状态 + 导航命令做条件聚类与均衡采样**造候选数据集，双头（安全置信分 + 几何精修向量），plug-and-play 测试时验证 |
| **BeyondDrive** | [2605.19771](https://arxiv.org/abs/2605.19771) | 2026 | 预印本（Junli Wang） | **未核**（摘要未提代码；"MeanFuser 同组"亦**未核**） | **v1 89.7 PDMS** | flow matching 生成**硬负样本** + Repulsive Distance Loss；"近专家但危险"的候选显式建模。**基线 = Latent Transfuser（单模）** |

## 二、线索级（**未核验**，引用前必核）

**A. learned scoring / scorer**
- FLoRA（`2502.11352`，2025）：propose-selection 里学**时序逻辑评分规则**，只用正样本
- DA-WAM（`2608.19085`，2026，代码 `LeapWM/da-wam`）：每候选一条未来 latent，因子化 scorer 打分
- TrajMoE（`2512.07135`，2025）：MoE 场景自适应先验 + GRPO 微调打分
- MindDrive（`2512.04441`，2025）：逐候选 what-if rollout + VLM-Critic 打分
- MeanFuser（`2602.20060`）：注意力权重在采样集内**隐式选优**（= DP-A14）

**B. 候选 / 提案生成与选择**
- PLUTO（`2404.14327`，2024，`jchengai/pluto`）：多提案 + 规则打分，nuPlan 原型
- Aligning Multi-Trajectory Supervision（`2608.30122`，2026）：指出"**高分候选 ≠ 好监督**"
- CarPlanner（`2502.19908`，2025）：generate-selection + 专家引导奖励 RL
- INTERACT（`2609.31137`，2026）：锚点=驾驶意图，CEM 精修后再打分

**C. ranking / reranking / verifier / reward model**
- DEFT-RLVR（`2608.01755`，2026，`hzx122/DEFT-RLVR`）：规划改成 AD-MCQ 候选选择题
- DriveReward（`2606.08525`，2026）：VLM 生成式奖励模型 + 反事实标注
- DriveCritic（`2510.13108`，2025）：人类成对偏好训 VLM 评测器，论证 EPDMS 缺语境
- CritiqueDriveVLM（`2607.04179`，2026，`MICLAB-BUPT/CritiqueDriveVLM`）：多维 verifier 引导 RL

**D. 监督信号来源**
- VL-DPO（`2605.20082`，2026，**ICRA 2026**）：VLM 零样本造偏好对做 DPO 重排
- HGRL（DOI `10.1109/TIV.2024.3406679`，2024，IEEE TIV）：人驾数据引导 RL，采样候选 + 离线偏好学奖励

## 三、对本项目的直接影响（三条）

1. **"选优器是最高杠杆"这个判断已被他人做**（TOAD 明确把 scorer 当 reward 搜索、Vault 明确学官方分子指标）→ **方向 B 的卖点必须从"做选优"移到"用什么监督信号"**（见 [sota-plan.md §9.6](../../../ideas/sota-plan.md)）；
2. **TOAD 已核实是 navhard（第六十九轮），且它"无需重训"** → **榜一易主为 TOAD+DrivoR 56.3**，且**它把头部压平**（六个 base planner 搜后全落 49.0–56.3）→ **子榜辩护的前提要从"比 55.5 高"改成"比 56.3 高"，且"base planner 好坏"这条叙事被削弱**；
3. **重合风险最高的是 DriveVer**（"条件聚类 + 均衡采样造候选"）——它几乎就是"候选池构造 × 监督"的同一命题 → 方向 B 的**差异化必须写清楚**（工作空间此前已记"候选池已被部分占据"，本轮再添一例）。

## 四、下一步（未做）

- 把 §二 的线索级条目**逐条核验**（arXiv ID / venue / 代码），合格的并入本表 §一或 DP-A 表；
- ~~核实 TOAD 的 56.3 split~~ **✅ 已完成（第六十九轮：是 navhard-two-stage）**；**待办**：Vault 的 venue（是否已中稿）与有无代码、**TOAD 代码是否/何时发布**；
- 把 §三 第 1、3 条写进 [sota-plan.md](../../../ideas/sota-plan.md) 的"重合风险"与 [judgments.md](../../../judgments.md) D 组。
