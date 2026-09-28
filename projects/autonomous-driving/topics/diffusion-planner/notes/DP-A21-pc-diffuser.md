# DP-A21 · PC-Diffuser（驾驶域内的认证级硬约束）

- **原题**：PC-Diffuser: Path-Consistent Capsule CBF Safety Filtering for Diffusion-Based Trajectory Planner
- **作者/载体**：Eugene Ku 等；arXiv [2603.10330](https://arxiv.org/abs/2603.10330) v2（2026-03 首发，2026-07 更新）；官方 README 写明 **IROS 2026**
- **代码**：[Eugene29/PC-Diffuser](https://github.com/Eugene29/PC-Diffuser)（已克隆，含两个子模块；**代码核验见下**）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对；关键论断已由本线程 grep 复核）
- **笔记日期**：2026-09-22
- **重要性**：这是**驾驶域内**目前最接近"生成过程内硬约束"的工作，直接决定了"约束注入"这个 idea 方向还剩多少空间。

## 摘要原文（节选）

> Diffusion-based trajectory planners have recently shown strong closed-loop performance by iteratively denoising a full-horizon plan, but they remain difficult to certify and can fail catastrophically in rare or out-of-distribution scenarios. ... we present PC-Diffuser, a safety augmentation framework that embeds a certifiable, path-consistent barrier-function structure directly into the denoising loop of diffusion planning.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 问题陈述 | 扩散规划器"no formal mechanism to prevent unsafe outcomes"；要求安全成为"intrinsic part of trajectory generation rather than a post-hoc fix" | 摘要、§I |
| 约束定义 | 胶囊距离 CBF：h_j = d_cap(S_ego, S_j) − d_safe（Eq.7），配单车模型（Eq.1）；覆盖碰撞 + 运动学 + 路径几何 | Eq.1/7 |
| 注入方式 | **路径一致 CBF-QP**（Eq.11/16）：固定转向、只调速度 v_k*=argmin‖v_k−v_nom‖² s.t. (∂h_j/∂v)v_k ≥ −α(h_j)；**每个去噪步**对干净估计 τ̂₀(t) 施 CBF 后 **re-noise 回注**（Eq.17） | §III–IV、Eq.11–17 |
| 理论保证 | Prop.1（光滑性）、**Thm.1（速度级胶囊 CBF 可行性）**、**Cor.1（前向不变性）**——证书作用在**将被执行的 rollout 时间轴**上，而非中间隐状态 | §III–IV |
| 推理成本 | 迭代式：**5× vanilla，约 2 fps**；若只做单次 post-hoc 则为 1.5× | §V-D |
| 主结果（nuPlan） | all-collision 挑战集 **碰撞率 100% → 10.29%**，composite 0.59（Table I）；Val14 0.83→0.88、Test14-hard 0.69→0.78 | Table I |
| 基座 | Diffusion Planner（**不与 DiffusionDrive 对比**，不同基准） | §V |
| 消融（Table II） | 去迭代 → 16.91%/0.47；去选择性过滤 → 11.76%/0.47；去动态可行性 → 21.32%/0.30 | Table II |
| 自述局限 | 仍属 reactive；nuPlan 的 IDM 仿真不真实，约 10% 碰撞不可避免 | §VI |

## 代码核验（2026-09-23）

读 `safety/pc_diffuser/lqr_tracker_cbf_modular.py`（906 行）、`safety/utils.py`、`safety/mpc_cbf/{distance_functions,mpc}.py`、`model/diffusion_utils/dpm_solver_pytorch.py`、`config/planner/*.yaml`、`scripts/methods/*.sh`。**机制描述与笔记原先的记载一致，但"硬约束"这个标签要加限定。**

**先厘清：这个仓库里其实有三个方法、两套 QP**

| 目录 | 方法 | 求解器 | 决策变量 | 障碍函数 |
|---|---|---|---|---|
| `safety/pc_diffuser/` | **PC-Diffuser**（主方法） | **CasADi `ca.qpsol('qp','qpoases')`** | **加速度级** `[a, a_nbr(M=10), slack(M)]` | **胶囊** `h = sqrt(d_seg²) − (r_e+r_n)` |
| `safety/safe_diffuser/` | SafeDiffuser 基线 | **cvxpy + OSQP** | ego **位置增量** `[H,2]`（yaw 被注释掉） | 矩形有符号距离 `distance − R` |
| `safety/mpc_cbf/` | MPC-CBF 基线 | CasADi NLP（N=80） | 全状态/控制序列 | 胶囊，但 `safety_mode='direct'`（非 CBF 衰减） |

| 项 | 代码证据 |
|---|---|
| **注入点** | `dpm_solver_pytorch.py::data_prediction_fn`：先算干净估计 `x0`，再 `if cbf.enabled and (cbf.shield_every_step or is_last): x0 = apply_cbf(x0, t)` → **滤在 x0 上**，与 Eq.17 一致 |
| **是否真的逐去噪步** | yaml 默认 `shield_every_step: false`，但 **`scripts/methods/pc_diffuser.sh` 覆盖为 `true`**（并设 `lqr_cbf=true`、`selective_CBF=true`）→ **主方法确实逐去噪步滤**；而 `mpc_cbf.sh` 没覆盖 → **MPC-CBF 基线只在最后一步滤** |
| **QP 结构** | 决策变量 `[a, a_nbr(M), slack(M)]`；目标 `(a − a_des)² + 1e4·Σ(slack + slack²)`；约束 ① `a·dt + v_k ≥ 0` ② 逐邻居 degree-1 CBF `coeff_a_ego·a + coeff_a_nbr·a_nbr + bias + slack ≥ 0` ③ `slack ≥ 0` |
| **"只调速度、固定转向"** | **完全一致**：ego 的唯一决策量是标量加速度；转向率由 LQR 给出并直写 `u_hist[0,k,1] = sr_des` |
| **胶囊障碍** | `h_expr = ca.sqrt(D2) − (r_e + r_n)`，**docstring 原文 "linear gap distance, no bias towards far and fast vehicles"**；二次形式被注释掉。ego 位置先由后轴平移到 COG |
| **实际生效的 α** | `_compute_barrier` 返回 `h − safety_margin`；**`dpm_solver` 显式传 `cbf_alpha=0.9`**（类默认 0.7/0.3，代码带 TODO "Make this cbf_alpha configurable"） |
| **每次规划解多少次 QP** | `n_steps = 1 if one_step else H − 1`，`for k in range(n_steps)` 里**每个航路点解一次**；被注释的计时打印写 `slack: {n_slack_total}/{H-1}`。配 `sampler.steps=10` + `num_poses=80` → **单次规划数百次 QP**。→ **"1.14 ms" 是单次 QP 的口径**，不能与端到端延迟混用 |
| **"硬"吗** | **不是严格硬**：每条邻居约束带 **slack（权重 1e4）**，QP 失败时**回退到 nominal（不安全）轨迹**；仓库**记录 `n_slack_total`（活跃松弛数）** 作为诊断 → **"certified" 只在 QP 可行且 slack 全 0 时成立** |
| **选择性过滤** | `predict_collision` 按 `reachability_threshold` 扫描全部时间步的胶囊距离标记"会碰撞"的邻居；`selective_cbf=True` 时未标记者 `bias = 1e6`（平凡满足） |
| **复现前提（易漏）** | README 明说为 mpc-cbf 与 pc-diffuser **改写了 nuplan-devkit 的 tracker**（`action_replay_tracker.py` + `set_latest_action`），否则 **CBF 输出的动作会被 nuPlan 控制器覆盖** |
| 距离表示 | `distance_functions.py` 实现 **5 种**：`capsule` / `sat` / `sat_euclidean` / `circles`（3 圆）/ `euclidean`（圆盘） |

**三条判断**：

1. **机制描述经代码确认，原笔记准确**（"只调速度、固定转向、逐去噪步"）；§A 里"线性间距 `h = D − (r_e+r_n)`"也对——它正是胶囊函数的 docstring 原文。→ **无需更正机制，只需补"哪套 QP 属于哪个方法"**。
2. **"认证级硬约束"要加限定**：带 slack + 失败回退 → 应写成"**带松弛的逐去噪步 CBF-QP，可行性由 QP 是否成功与活跃松弛数决定**"。
3. **成本门槛比"约束写在哪一层"更硬**：`n_steps = H−1` × `steps=10` → 单次规划数百次 QP。方向 A 若要做"生成内硬约束 + 实时"，**必须先回答"能否把 QP 次数从数百降到个位数"**。

> 完整核验见 [diffusion_planner_code_traces.md §I](../../../code/traces/diffusion_planner_code_traces-2.md)。

## 对本项目的意义（关键）

1. **推翻了"驾驶域无硬约束"的初判**：此前基于摘要级信息，我把它记为"与 DP-A20 同思路但未逐项核验"。逐表核对后确认：它有可行性定理 + 前向不变性推论，且约束作用在**执行 rollout** 上，不是中间隐状态。**方向 A 的空白比原先判断的小得多**。
2. **剩下的空间在哪**（AI 判断，待验证）：
   - **代价**：5× 延迟、约 2 fps，离实时（≥10 Hz）差一个量级；"硬约束 + 实时"目前没人同时做到。
   - **约束类型**：只做碰撞/运动学/路径几何，**没有交通规则、舒适性、交互式反应**；且只在 nuPlan（IDM 仿真）验证。
   - **只调速度不调转向**（路径一致性的代价）：横向避让能力被结构性限制。
3. **与 DP-A22 的技术路线冲突**：G2SD 明确反对在去噪内注入安全力（流形破裂），主张把约束前移到图规划。这两篇构成一个可直接讨论的对立。

## 待核验

- 是否有官方代码（未核验）。
- "约 10% 碰撞不可避免"是在什么条件下（IDM 仿真局限还是方法局限）。
- 若把该框架移到 NAVSIM 类相机端到端规划器上，SDF/胶囊几何的输入从哪来（nuPlan 有特权状态，NAVSIM 没有）。
