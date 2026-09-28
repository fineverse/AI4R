# DP-A16 · DIVER

- **原题**：DIVER: Reinforced Diffusion Breaks Imitation Bottlenecks in End-to-End Autonomous Driving
- **作者/载体**：Ziying Song 等；arXiv [2507.04049](https://arxiv.org/abs/2507.04049) v5（2025-07-05 首发）；IEEE 期刊稿体例（含 Index Terms），未标会议
- **代码**：[adept-thu/diver](https://github.com/adept-thu/diver)（见 [code/repositories.md](../../../code/repositories.md)）
- **证据等级**：全文（arXiv HTML 逐节提取 + 仓库 README 复核）；结果表数值**已从 arXiv HTML 与官方 README 取到**（2026-09-24 更正：此前记"结果表数值未获取"已不成立）
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> Most end-to-end autonomous driving methods rely on imitation learning from single expert demonstrations, often leading to conservative and homogeneous behaviors... At the core of DIVER lies a reinforced diffusion-based generation mechanism. First, the model conditions on map elements and surrounding agents to generate multiple reference trajectories from a single ground-truth trajectory... Second, reinforcement learning is employed to guide the diffusion process...

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 问题陈述 | 单专家模仿学习导致保守、同质行为与模式坍缩；**理论证明**单 GT 监督下 p_θ→δ(τ−τ*) | §III-B、Eq.1–6 |
| 生成机制 | 条件扩散；论文写噪声起点为**标准高斯**（**代码不符**：x₀ 是 GT 命令对应的 plan anchor + 截断噪声，见下方「代码核验」）；PADG（多参考 GT + 6 锚点作生成引导） | §IV-B2、Eq.7–8 |
| 安全/多样性位置 | **GRPO 奖励注入策略**（Eq.13–21），不是生成过程硬约束 | §IV |
| 训练目标 | L_total = λ_match·L_match（匈牙利匹配）+ λ_RL·L_RL（GRPO） | Eq.12 |
| 奖励构成 | 论文：r = λ_div·r_div + λ_safe·r_safe + λ_TC·r_TC + λ_LK·r_LK，并复用 Hydra-MDP 的 PDMS 奖励（NC/DAC/TTC/Comf/EP）（**代码不符**：实际只有 `0.5·div + 0.3·safe + 0.2·map`，其中 `map` 是 dummy 常数，TTC/LK/PDMS 项不存在） | Eq.20、§IV-C2 |
| 评价基准与结果 | **NAVSIM v1 navtest 88.3**（98.5/96.5/94.9/100/82.6；同表 GoalFlow 90.3、DriveSuprim 89.9、DiffRefiner 89.4、DiffusionDrive 88.1，Table 2）；**v2 navtest EPDMS 82.2**（同表 DiffusionDriveV2 85.5、DriveSuprim 83.1、ARTEMIS 83.1，Table 3）；**v2 navhard Stage1 26.8 / Stage2 43.4**（同表 MindDrive 30.5、GuideFlow 27.1、DiffusionDrive 24.2，Table 4）；**Bench2Drive** DIVER(vs DiffAD) DS 68.90 / SR 36.75（Table 1）；**nuScenes 开环** **L2 Avg 0.21 / Col. Avg 0.07**（**同表 UniAD 0.15/0.08、SparseDrive 0.13/0.08**，Table 5——**2026-09-24 用仓库 README 定案：表头是 `L2 (m) Avg` 与 `Col. (%) Avg`，此前误记为 "Div.Avg"**）；**Bench2Drive** 表里另有 `Avg. L2 1.13 / Div.(t) 0.32`（SparseDrive 0.87 / 0.21，Table 6）；**FPS 41**（Table 7） | 各表（PDF 核验）+ 仓库 README |
| 与 DiffusionDrive | **有直接对比**（Table 1、2、4、5） | 各表 |
| 新指标 | 提出 Div. 多样性指标 | Eq.23–24 |

## 作者自述局限

- 正文未设专门局限段（未获取）。

## 对本项目的意义

- 与 DiffusionDriveV2 是同一问题的两种解法：都承认"IL 缺乏约束"，但 DIVER 从**理论**（单 GT 导致分布坍缩）出发，且用 GRPO 同时优化安全与多样性。
- 它提出的 Div. 指标是判断"多样性是否被牺牲"的现成工具（DDV2 的 Table 3 即用类似指标）。
- 对本项目的关键提示：**"安全"目前普遍是软奖励**。若要做生成过程硬约束，DIVER 是必须区分的对照。
- 结果上的一个重要信号：**navhard 上所有方法都掉到 20–45 区间**（DIVER Stage2 43.4、GuideFlow 27.1、DiffusionDrive 24.2），说明长尾/困难场景远未解决；而 v1 navtest 已经挤在 88–90 的窄带里，**继续在 navtest 上刷分的边际价值很低**。

## 代码核验（2026-09-23）

读 `mmdet3d_plugin/models/motion/motion_planning_head_DriveStyle.py`、`decoder.py`、`adzoo/sparsedrive/configs/DIVER_small_b2d_stage2_targetpoint_multiplan.py`、`adzoo/sparsedrive/tools/kmeans/kmeans_plan.py` 与 README。**两处论文主张与代码不符**：

| 项 | 代码证据 |
|---|---|
| **扩散接在 SparseDrive 上** | 规划头换成 `DriveStyleMotionPlanningHead`，**沿用 SparseDrive 的 `operation_order`**，另加 `diff_operation_order` / `diff_noise_operation_order` 两组各 10 步操作；数据集是 **Bench2Drive**（`B2D3DDataset`），不是 NAVSIM |
| **噪声起点不是纯高斯，是"锚点 + 截断噪声"**（与笔记正文相反） | `cmd = metas['gt_ego_fut_cmd'].argmax(dim=-1)` → `cmd_plan_anchor = plan_anchor[bs_indices, cmd]` → 差分 → `odo_info_fut`；`timesteps = torch.randint(0, 40, (bs,))` 加到 `DDIMScheduler(num_train_timesteps=1000, scaled_linear)` 上。→ **x₀ 是 GT 命令对应的 plan anchor，噪声只到 1000 步中的前 40 步**（与 DiffusionDrive 的 t=8 同思路）。**笔记原记"噪声起点为标准高斯"需更正** |
| **"GRPO" 实为"奖励加权损失"**（与论文相反） | `diff_PPO_loss_planning`：**`diffusion_loss = diffusion_loss * (1.0 + total_reward.mean())`**。**全仓无 `log_prob` / `advantage` / PPO clip / 组内基线**（grep 无命中）→ 没有策略梯度的任何要素 |
| **奖励项只剩两项，且 20% 是常数** | `compute_reward`：`safety_reward = 1 - min(1, collision_penalty/num_modes)`（用 **GT 未来智能体轨迹**、`safe_distance=2.0`）、**`map_reward = 1.0`（注释自述 "dummy 值"）**、`diversity_reward` = 模态两两距离均值；`total_reward = 0.5*div + 0.3*safe + 0.2*map`。→ **论文 Eq.20 的 TTC / 车道保持 / Hydra-MDP PDMS 奖励在代码里都不存在** |
| **`check_collision` 语义与名字相反** | `safe = True` 起手；若某智能体 `min_dist >= safe_distance` 则 `safe = False; break` → **只有"所有智能体都在 2 m 内"才返回 True**。`generate_safe_trajectories`（训练时 `num_trajectories=10`）收集的因此是**离 GT 智能体极近**的样本 |
| **发布的代码跑不通** | `motion_planning_head_DriveStyle.py` 有 **4 处未注释的 `pdb.set_trace()` 在 `forward` 里**（`:600/617/655/969`），另有 `:1052` 与 `instance_queue.py:221`。→ **无法直接跑通一次前向** |
| **锚点文件未发布** | 全仓 **0 个 `.npy`**；`kmeans_plan.py` 已改为 **6 命令分组**（`K=6`）→ DIVER 的 `kmeans_plan_6.npy` 应是 **(6,6,6,2)**，与 SparseDrive 的同名文件 **(3,6,6,2)** 不是同一个文件。这是本项目里**第 3 个"锚点文件未发布"的仓库** |
| 一处内部不一致（待运行确认） | 配置声明 `num_cmd=6`、`ego_fut_mode=6`（36 候选），但评测用的 `HierarchicalPlanningDecoder.decode` **硬编码 `reshape(bs, 1, ego_fut_mode)`** → 最终只输出 **6 条**（`num_cmd` 未被使用） |

**另外**：DIVER 的 README 表给出 **nuScenes 开环 L2 Avg 0.21（SparseDrive 0.13、UniAD 0.15）、碰撞 Avg 0.07（SparseDrive 0.08）、Div.(t) 0.32/0.35（SparseDrive 0.21）**——**它自己提供了"用 L2 换多样性"的实测证据**。

> 完整核验见 [diffusion_planner_code_traces.md §G](../../../code/traces/diffusion_planner_code_traces.md)。

## 待核验

- DIVER 的"Stage1/Stage2"在 navhard 上的定义（正文未展开）。
- nuScenes 开环的 Col.Avg 与 DiffusionDrive 几乎持平（0.07 vs 0.08）——RL 带来的多样性提升没有转化为开环碰撞率改善，原因未说明。
