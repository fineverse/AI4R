# DP-A18 · FeaXDrive（可行性违规的可测证据）

- **原题**：FeaXDrive: Feasibility-aware Trajectory-Centric Diffusion Planning for End-to-End Autonomous Driving
- **作者/载体**：Baoyun Wang 等；arXiv [2604.12656](https://arxiv.org/abs/2604.12656) v2（2026-04 首发，2026-04-30 更新）
- **代码**：[BaoyunWang/FeaXDrive](https://github.com/BaoyunWang/FeaXDrive)（已克隆；**代码核验见下**）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> ...the physical feasibility of generated trajectories remains insufficiently addressed. In particular, generated trajectories may exhibit local geometric irregularities, violate trajectory-level kinematic constraints, or deviate from the drivable area, indicating that the commonly used noise-centric formulation in diffusion planning is not yet well aligned with the trajectory space where feasibility is more naturally characterized.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 机制 (a) 训练期 | 曲率惩罚 L_cur = (1/H)Σ max(\|κ_i\|−κ_i^adp, 0)²，自适应阈值 κ^adp = min(κ_geo, a_max/v²) | Eq.14–15 |
| 机制 (b) 推理期 | 可行驶区 SDF + footprint 软障碍 L_drv = (1/4H)ΣΣ softplus(m_safe − d_ij)（Eq.22）+ **触发式**梯度校正（Eq.23），每步作用于干净估计 | Eq.22–23 |
| 机制 (c) 后训练 | FA-GRPO：R = R_task + λ_fea·R_fea，作用于整条去噪链 | Eq.26/28 |
| 约束范围 | 曲率/运动学 + 可行驶区；**无碰撞项** | §III |
| 主结果（NAVSIM） | IL **PDMS 88.7 > DiffusionDrive 88.1**（Table 2）；FA-GRPO **90.0** | Table 2 |
| **违规率（关键）** | 曲率违规 **0.88% vs DiffusionDrive 8.59%**、ReCogDrive 8.05%/15.5% | Table 3 |
| 延迟构成 | 总 348.73 ms：**VLM 245.33 ms（70.3%）**、planner 82.96 ms、SDF 16.03 ms、guidance 4.41 ms | Fig.5 |
| 消融 | 轨迹中心式 85.32→86.56 PDMS、曲率违规 11.36%→7.51%；+曲率正则 →0.13%；+可行驶引导 86.57→88.75、DAC 94.94→97.46、可行驶违规 5.06%→2.54%（曲率违规回升到 0.88%） | Table 4 |
| 消融（RL） | 普通 GRPO **90.56 但曲率违规 →5.79%**；FA-GRPO 90.00 / 2.40% | Table 5 |
| 自述局限 | GRPO 奖励只含几何/运动学；可行驶引导依赖局部地图先验 | §V |
| 理论 | 无 | — |

## 判定（AI 判断）

**生成内软引导**：训练期惩罚 + 推理期触发式 softplus 梯度，无投影/证书。强于事后筛选，但不是硬约束。

## 对本项目的意义（关键）

1. **它给出了"问题真实存在"的量化证据**：DiffusionDrive 的曲率违规率是 **8.59%**，ReCogDrive 8.05%/15.5%。这说明"生成轨迹不满足运动学/几何可行性"不是假想问题，而是可测的现状——这是做"可行性/约束"方向最有力的动机证据。
2. **它同时给出了两个反直觉的权衡**：
   - 加可行驶引导后 PDMS 上升（86.57→88.75），但曲率违规从 0.13% 回升到 0.88%——**约束之间会互相干扰**。
   - 普通 GRPO 分数更高（90.56 vs 90.00）但曲率违规高 2.4 倍——**分数与可行性不一致**，直接用 PDMS 做奖励会把可行性搞坏。
3. **延迟构成值得注意**：VLM 占 70.3%，planner 只占 82.96 ms。如果目标是实时性，瓶颈不在扩散采样。

## 代码核验（2026-09-23）

读 `navsim/agents/feaxdrive/{feaxdrive_diffusion_planner.py, trajectory_projector.py, feaxdrive_diffusion_planner_fagrpo.py}`、`navsim/agents/recogdrive/utils/drivable_sdf.py`、`scripts/repro/slurm/*.slurm`、`README.md`、`docs/`。**结论：两个核心机制都是真实实现，但论文的"约束一致性训练"项未启用。**

| 项 | 代码证据 |
|---|---|
| 它的身份 | 规划器类名是 **`ReCogDriveDiffusionPlanner`**——**FeaXDrive = ReCogDrive 的扩散规划器 + 可行性模块**，仓库内同时保留 `navsim/agents/recogdrive/` 全套 |
| **曲率正则（Eq.14–15）逐字实现** | `_kappa_max_adapt`：`min(kappa_geo_max, a_lat_max/(v²+eps))`；惩罚为 **hinge-squared**：`relu(\|κ\|−bound)² + relu(\|a_lat\|−a_lat_max)²`。官方 `dyn` 档超参：**`proj_kappa_geo_max=0.166`、`proj_a_lat_max=6.0`、`proj_use_kappa_adapt=true`、`lambda_dyn=0.01`**（与论文的 κ_geo=0.166、a_max 量级一致） |
| **但"约束一致性训练"项在官方链路里全为 0** | `lambda_proj=0.0`、`lambda_proj_supervise=0.0`；代码注释明写 `use_constraint_projection` **is deprecated in the current official chain**。→ 论文的 `‖x₀−Π(x₀)‖²`、`‖Π(x₀)−x_gt‖²` **未启用**；`project_dynamics` / `project_drivable` 是保留但未接入的代码 |
| x0 是统一对象 | `pred_type='x0'` → `F.mse_loss(x0_pred, gt_actions)`；`lambda_dyn>0` 时 `total_loss += 0.01 · violation(denorm(x0_pred))`——**惩罚施加在干净轨迹上** |
| **推理引导（Eq.22–23）逐条实现** | **只在最后 3 / 共 5 步生效**；`step = 0.05·progress`；障碍项 `softplus((0.30 − sdf)/0.20)`；梯度对 **x0 估计** 求，XY 归一化为单位向量、heading 用符号归一化 ×0.1；`x0 ← x0 − step·grad` |
| SDF 来源 | ego 系 ROI x∈[−10,80]、y∈[−30,30] m，分辨率 0.2 m；可行驶层 = ROADBLOCK/INTERSECTION/DRIVABLE_AREA/CARPARK_AREA；`distance_transform_edt` 后 clip ±50。官方链路固定 **`DRIVABLE_SDF_SOURCE=data_map`**（从 map_api 重建，不用 MetricCache） |
| **FA-GRPO 是真 GRPO** | `G=8` 条/样本 → `advantages=(R−mean)/std` **组内归一化** → 分位裁剪 → 折扣 `0.6^(剩余去噪步)` → 对去噪链取 `Normal(mean,std).log_prob` → `policy_loss = −mean(logp·adv)`；另加 **BC 项** `+0.1·(−logp(old_policy 采样链))`。奖励 = **真 PDM 分数**（`PDMSimulator`+`PDMScorer` 逐条仿真） |
| 奖励权重非标准 | `progress_weight=10.0`（navsim 标准 5.0）、`comfortable_weight=10.0`（标准 2.0）；脚本含断言：标准评测 scorer 若被 FA-GRPO comfort 指标污染则 `exit 3` |
| **违规率判据（解决原「待核验」）** | 先对 xy 做**二项式核平滑（ksize=5）**，再按弧长参数化用变步长中心差分算 κ，`a_lat=v²·κ`（dt=0.5），**两端点补 0**；违规率 = `(\|val\|>bound).float().mean()`，**同时输出固定界与自适应界两套**。→ 是"**逐时间步超限比例**"，依赖平滑核与端点补零；**DiffusionDrive 的 8.59% 是用同一套判据测的**（论文内可比，跨论文不可比） |
| 发布状态 | **无未注释断点、无缺失 `.npy`**（本就不需要锚点），带 3 个 slurm 复现脚本 + 4 篇 `docs/`。→ **本项目核验过的扩散规划器里可复现性最好的一个** |

**三条判断**：

1. **两个核心机制（自适应曲率正则、softplus SDF 引导）经代码确认成立**，超参与论文对得上。这是本工作空间里**第一篇"约束类主张"被代码证实**的工作。
2. **但"约束一致性训练/投影"在发布配置里未启用** → 引用时只能说"**训练期软违规惩罚 + 推理期软引导**"，不能说"投影/一致性训练"。
3. **它自己的 README 给出两条对本题最不利的数字**：① **ReCogDrive w/GRPO 的 PDMS 90.5 > FeaXDrive 的 90.0**；② **FA-GRPO 把曲率违规从 0.88% 抬到 2.40%**（普通 GRPO 更差 15.5%）。→ **"RL 提分"与"RL 破坏可行性"在同一张表里同时成立**。

> 完整核验见 [diffusion_planner_code_traces.md §H.1](../../../code/traces/diffusion_planner_code_traces.md)。

## 待核验

- 表 4 中"曲率违规回升"的原因未解释（代码侧只能看到引导作用于 x0 估计、XY 单位化步长，未涉及曲率项）。
- 论文的违规率数字由哪个脚本产出：仓库里**只有训练期的 `violation()` 统计**（输出三个 rate），未见独立的评测分析脚本——需运行确认论文数字取自哪一列。
