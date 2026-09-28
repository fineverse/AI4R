# 自动驾驶基准与评价协议

更新时间：2026-09-23  
性质：**大方向公共资产**。本文件只汇总"用哪个基准、怎么算分、能不能比"，不重复各小方向的实验结果。  
来源编号见 [sources.md](../sources.md)（B 系列＝基准与数据集）。  
证据等级：基准清单与论文口径来自**官方 README 与论文自述**；**§2 的 NAVSIM 指标定义与 Agent/评测接口、§2.6 的 nuPlan 闭环分数、§2.7 的 Bench2Drive 四项指标、§2.8 的 nuScenes 开环规划指标均已做代码级静态核验**（NAVSIM 读 `navsim` 仓库 `main` 分支 commit `0a380a9063d7162ec93d0f51e9990ebac585f720`，即 v2 版 devkit，见 [code/repos/navsim](../code/repos/navsim)；nuPlan 读**已 vendored 到本地的 nuplan-devkit**，见 [code/repos/WAM-Flow/nuplan-devkit](../code/repos/WAM-Flow/nuplan-devkit)；Bench2Drive 读**已 vendored 到本地的官方评测栈**，见 [code/repos/diver](../code/repos/diver)，并已与官方 `0.0.4` 分支逐字节比对；nuScenes 开环读本地已克隆的 `UniAD` / `VAD` / `SparseDrive` / `GenAD`）；**未在本地运行任何评测**。

## 1. 基准清单

| 编号 | 基准 | 类型 | 输入权限 | 指标 | 关键限制 |
|---|---|---|---|---|---|
| B001 | NAVSIM v1 | **非反应式**伪闭环 | devkit 提供 8 相机 + 1 路合并点云；"纯相机"是 **agent 自己选的子集** | PDMS | navtest 已饱和（前沿方法挤在 88–91） |
| B012 | NAVSIM v2 / Pseudo-Simulation | 两阶段伪闭环，**两阶段默认用反应式 IDM 交通**（2026-09-23 代码级更正） | 同上 | EPDMS（代码里叫 `extended_pdm_score_*`） | 划分是 `navtest` / **`navhard_two_stage`**（官方 HF 榜标题写作 "navhard"，是同一划分的简称；devkit 配置名才是 `navhard_two_stage`）；navhard 才有区分度 |
| B002 | Bench2Drive | CARLA 闭环（反应式） | 传感器 | **四个指标**：DS = RC × IS、SR、5 项 Ability、Effi、Comf（**§2.7 已代码级核验**） | CARLA 版本与模型适配需固定；**DS/SR 的分母硬编码 220**（不足即静默按 0 计）；**Effi 是"速度比"、Comf 是"时间占比"**，且两者取自 **agent 自己 dump 的 `metric_info.json`**；**0.0.4 改过口径（2024-08-19 移除低速惩罚 + TickRunTime 2000→4000）→ 前后数字不可混用** |
| B003 | nuPlan | 闭环规划（结构化输入） | 矢量化特权输入 | closed-loop score = **`(4 项乘性连乘) × [Σw·m / Σw]`**（**§2.6 已代码级核验**） | 与 NAVSIM 不是同一件事；IDM 仿真；**加权平均的分母依赖配置的 metric 列表** |
| B004 | nuScenes | 开环 | 传感器 | L2、碰撞率（**§2.8 已代码级核验**） | 开环，不测交互与误差恢复；**同名 L2/碰撞在 UniAD / VAD / VADv2 / SparseDrive 里是四套不同实现**（碰撞判定：栅格占据 vs shapely 精确相交；L2 归约：逐时刻 vs 前缀平均；GT 碰撞时刻是否剔除也不同）→ **跨仓库横比不予采信** |
| B005 | Waymax | 状态级仿真 | 状态级 | 自定 | 不等于传感器渲染 |
| B006 | MetaDrive | 程序化场景 | 传感器 | 自定 | 反应式交通可配置 |
| B007 | Waymo Open Dataset | 数据集 | 传感器 | 分 Perception / Motion / E2E 子集 | 子集不能混用描述 |
| B008 | Argoverse 2 | 数据集 | 传感器 | 分 Sensor / Motion Forecasting | 同上 |
| B013 | 跨榜统一复评（IROS 2026 workshop） | 方法学研究 | — | — | 用于判断不同 leaderboard 数字的可比性 |

## 2. NAVSIM 口径（代码级核验，最易混，禁止互比）

### 2.1 三套划分

| 口径 | 含义 | 状态 |
|---|---|---|
| v1 navtest（PDMS） | 单阶段，**非反应式**（`default_common.yaml:22` `traffic_agents: non_reactive`；`log_replay_traffic_agents.py:15` 类注释原文 "Replayed (**non-reactive**) background traffic agents class."） | 已饱和（前沿挤在 88–91） |
| v2 navtest（EPDMS） | 两阶段伪闭环，**默认反应式 IDM 交通** | 与 v1 分数**接近但不系统性更高**（同一方法实测：DriveFuture v1 PDMS 90.7 / v2 EPDMS 89.9） |
| v2 **`navhard_two_stage`**（EPDMS） | 困难划分；**`include_synthetic_scenes: true`**（含合成场景） | **同一方法差距可达 3.6×**（DiffusionDrive：v1 navtest PDMS 88.1 → navhard EPDMS 24.2） |

> **划分的代码定义方式（2026-09-23 核验）**：不是数据集版本，而是 **SceneFilter 配置里的 log_name 列表**——`navsim/planning/script/config/common/train_test_split/scene_filter/*.yaml`，`_target_: navsim.common.dataclasses.SceneFilter`。该目录共 **11 个 split**（`navtest` / `navtest_two_stage` / `navhard_two_stage` / `navsafe_two_stage` / `warmup_two_stage` / `warmup_navsafe_two_stage_extended` / `private_test_hard_two_stage` / `competition_private_tokens` / `navtrain` / `navmini` / `all_scenes`）——**注意 `navtest` 与 `navtest_two_stage` 是两个不同文件**。规模：`navtest` **136 log_names / 12,146 tokens**；`navtrain` **1,192 log_names / 103,288 tokens**；`navhard_two_stage` **76 log_names / 5,912 tokens**。→ **引用配置时写 `navhard_two_stage`**（官方 HF leaderboard 标题写作 "navhard"，是同一划分的简称；`README.md` 的 changelog 里也混用两者）。
>
> **存储规模（`docs/splits.md`）**：`navtrain` **14 GB**（log）+ **445 GB**（传感器）；`navtest` **983 MB** + **223 GB**；`navhard_two_stage` **892 MB** + **31 GB**（合成帧另需下载）。→ 全量三套约 **700 GB**，与实验环境规划的容量需求一致。
>
> SceneFilter 不只有 token 列表，还带**加载参数**，三个 split 并不一致：`navtest` / `navtrain` 是 `num_history_frames: 4` + **`num_future_frames: 10`**；`navtest_two_stage` 是 **`num_future_frames: 16`**；`navhard_two_stage` 是 **`num_future_frames: 8` + `include_synthetic_scenes: true`**。→ **"同一份数据换个划分"不成立**，历史帧数、未来帧数、是否含合成场景都随 split 变。

### 2.2 分数是怎么算出来的（PDMS）

来源：`navsim/planning/simulation/planner/pdm_planner/scoring/pdm_scorer.py`、[docs/metrics.md](../code/repos/navsim/docs/metrics.md)。

```
PDMS = (NC × DAC) × [ (5·EP + 5·TTC + 2·C) / 12 ]
```

- **乘法项**（任一为 0 → 总分 0）：NC（无自车责任碰撞）、DAC（可行驶区域合规）
- **加权项**：EP 进度权重 **5**、TTC 权重 **5**、C 舒适权重 **2**（分母 12）
- **NC 不是二值**：碰撞对象属 `AGENT_TYPES` 记 **0.0**，否则记 **0.5**（`_calculate_no_at_fault_collision`）
- **"自车责任"有判定规则**：只有 `ACTIVE_FRONT` / `STOPPED_TRACK` 碰撞，或（横向碰撞 且 自车处于多车道/非可行驶区）才算；否则记入 `collided_track_ids` 后**不再重复扣分**
- **TTC 只在 1 s 窗口内、每 0.3 s 采一次**（`np.arange(0, 10, 3)`），且自车速度低于 `5e-3` m/s 时跳过

### 2.3 EPDMS 相对 PDMS 的四处改动

来源：`docs/metrics.md`、`run_pdm_score.py`、`scene_aggregator.py`、`pdm_scorer.py`。

1. 乘法项 **+DDC**（驾驶方向合规，取值 {0, 0.5, 1}：逆行累计位移 <2 m 记 1.0、<6 m 记 0.5、否则 0）与 **+TLC**（红绿灯合规，{0,1}）
2. 加权项 **+LK**（车道保持，权重 2；**偏离中心线 >0.5 m 且连续 ≥2.0 s** 才判失败，且**路口内跳过**）与 **+HC**（历史舒适，权重 2）
3. v1 的 Comfort 被替换为 **HC + EC（extended comfort）**；EC 比较**相邻两帧输出轨迹**的加速度/加加速度差异。**⚠ 第三十九轮更正：EC 在本地 devkit 里不进分**——配置写 `two_frame_extended_comfort_weight: 2.0`，但 `pdm_scorer.py` 里被显式 mask 掉（原文注释 "Exclude the two-frame extended comfort metric from the weighted metrics calculation"，`mask[WeightedMetricIndex.TWO_FRAME_EXTENDED_COMFORT] = False`）→ **EC 只作为一列被报告，不参与 EPDMS 的加权和**；**配置里那个 2.0 是死权重**。→ **实际参与加权和的只有 4 项**（见下方公式）。**⚠ 注意这与 DriveFuture 论文的 `M_avg = {EP, TTC, LK, HC, EC}`（β_EC = 2）冲突**——以本地代码为准，但需注明可能是版本差异（见 §2.10）
4. 加入**假阳性过滤** `filter_m(agent, human)`：若人类驾驶在该指标上也为 0，则该指标对 agent 记 1.0（不因"违规是必要的"而扣分）。**⚠ 这条过滤是后来才被官方榜采纳的**（2026-09-24 第三十八轮由 DriveFuture §3.3 确认）→ **采纳前后的分数分属两套官方实现（EPDMS\* / EPDMS），见 §2.9**；**本地 devkit 已含此修复**（且 2025-09-29 又修了它的一处 bug，见 §2.10）

```
EPDMS = (∏ filter_m) × [ Σ w_m · filter_m / Σ w_m ],  m ∈ {EP, TTC, LK, HC}   # EC 被 mask 掉，不进此和
```

### 2.4 两条使跨论文数字不可比的机制（本次代码核验新发现）

1. **EP 是批内相对分，不是绝对分**：`_aggregate_pdm_scores` 里 `norm_constant_progress = np.max(masked_progress)`，即进度按**本批候选轨迹中的最大值**归一化；若该最大值 ≤ 5.0 m 阈值，则所有候选的 EP 直接给 **1.0**。→ **同一场景、不同候选集，EP 不同**，PDMS 因此依赖"提了多少条候选、候选有多好"。**不同论文的候选集不同，PDMS 严格来说不可横比。**
2. **EPDMS 的两阶段聚合以"本方法自己的终点"为权重中心**：`SceneAggregator.calculate_pseudo_closed_loop_weights` 用高斯核 `exp(-d²/(2σ²))`、**`σ² = 0.1`（σ ≈ 0.32 m）**，距离是第一阶段的**本方法输出终点**与第二阶段各跟进场景**起点**之间的欧氏距离。σ 这么小意味着：只有起点落在终点约 0.5 m 内的跟进场景才有非零权重。→ **换一个方法，权重分布就变**，第二阶段不是固定题目。最终 `EPDMS = (stage1 × stage2)`，再对场景取平均。

> 结论：把 PDMS/EPDMS 当作"绝对能力分"跨论文比较是**方法上的错误**；可行的做法是**在同一候选集、同一划分、同一输入权限下自己复现基线**（与 §3 第 6 条一致）。
>
> **第三套机制见 [§2.9](#29-epdms-有两套官方实现epdms-vs-epdms--第三套跨论文不可比机制2026-09-24-第三十八轮新增)**（2026-09-24 第三十八轮新增）：**EPDMS 有"修复前 / 修复后"两套官方实现**（`filter_m` 是后来才被官方榜采纳的），同一方法差 **2.0–5.2** 分。本节标题的"两条"指代码侧已核到的两条；**引用 v2 数字时必须同时问"哪一套实现"**。

### 2.5 Agent 与评测接口（代码级，2026-09-23 新增）

来源：`navsim/agents/abstract_agent.py`、`navsim/common/dataclasses.py`、`navsim/evaluate/pdm_score.py`、`navsim/planning/script/run_create_submission_pickle.py`、`navsim/planning/script/run_pdm_score_from_submission.py`。

**agent 契约（`abstract_agent.py`）**

| 类别 | 方法 | 位置 |
|---|---|---|
| 必须实现（`@abstractmethod`，共 3 个） | `name()` / `get_sensor_config()` / `initialize()` | `:25` / `:31` / `:37` |
| 可选（默认 `raise NotImplementedError`） | `forward` / `get_feature_builders` / `get_target_builders` / `compute_loss` / `get_optimizers` | `:43` / `:51` / `:57` / `:86` / `:97` |
| 可选（默认返回 `[]`） | `get_training_callbacks` | `:106` |

→ **只做评测的 agent 只需实现 3 个方法**；训练侧接口（feature/target builder、loss、optimizer）全部可选，**没有 `initialize_training()`**。

**推理入口只有一个，且一次只处理一个 token**

- `compute_trajectory(agent_input: AgentInput) -> Trajectory`（`:63`）：`get_feature_builders()` → 建 feature → `unsqueeze(0)` 加 batch 维 → `torch.no_grad()` → `predictions["trajectory"].squeeze(0)` → 包成 `Trajectory`
- **没有 batch 版本**；评测脚本逐 token 调用（`run_create_submission_pickle.py:63` 一阶段、`:77` 二阶段），产出即 `Dict[token, Trajectory]` 的 pickle（`:59` / `:73`）
- **评测禁止读标注场景**：`agent.requires_scene == True` 在评测入口直接 `raise ValueError`（`run_create_submission_pickle.py:41-46`，原文 "In evaluation, no access to the annotated scene is provided, but only to the AgentInput"）→ **这是"输入权限"在代码里的硬边界**

**输出形状被断言：训练口径 8 poses 与打分口径 40 poses 不是一回事**

- `Trajectory`（`dataclasses.py:277-289`）：`poses` 末维 (x, y, heading)，`trajectory_sampling` 默认 `TrajectorySampling(time_horizon=4, interval_length=0.5)`；`__post_init__` 断言 `poses.shape[0] == trajectory_sampling.num_poses`、`ndim == 2`、末维 3
- **输出/训练 = 8 poses @2 Hz（4 s）**；**PDM 打分 = 40 poses @10 Hz**（`config/common/default_common.yaml:29-33` `proposal_sampling: num_poses: 40 / interval_length: 0.1`）
- 打分前先 `transform_trajectory`（`pdm_score.py:26-54`）把 8 点轨迹按固定时间步转成 `InterpolatedTrajectory`，**速度与加速度被显式丢弃**（`:41` 注释 "velocity and acceleration ignored by LQR + bicycle model"），再由 LQR + 自行车模型**重新仿真**（`:146` `simulator.simulate_proposals`）→ **被评分的不是模型输出的那 8 个点，而是被动力学模型"开过一遍"的轨迹**

**agent 能看到什么**

- `AgentInput`（`:148-154`）只有 3 个字段：`ego_statuses` / `cameras` / `lidars`；驾驶命令在 `EgoStatus.driving_command`（`:144`），不在 `AgentInput` 顶层
- `SensorConfig`（`:782-837`）字段固定为 8 路相机（`cam_f0/l0/l1/l2/r0/r1/r2/b0`）+ 1 路 `lidar_pc`；**预置只有 `build_all_sensors()` 与 `build_no_sensors()`**，**没有相机-only / LiDAR-only 预置** → "纯相机"是**各 agent 自己填的子集**（如 TransFuser 只开相机）

**命名：代码里没有 "EPDMS"**

- `EPDMS` 只出现在 `README.md` 与 `docs/metrics.md`；代码里的命名是 `extended_pdm_score_stage_one` / `_stage_two` / `_combined`（`run_pdm_score_from_submission.py:389/398/407`）
- 两阶段循环在 `run_create_submission_pickle.py:58` / `:69` 与 `run_pdm_score_from_submission.py:58` / `:100`；**二阶段场景取自 `input_loader.reactive_tokens_stage_two`**
- 一阶段终点被显式记录（`run_pdm_score_from_submission.py:79-88`：`end_pose = trajectory.poses[-1]` → `relative_to_absolute_poses` → `endpoint_x/y`）→ **这正是 §2.4 第 2 条"权重中心是本方法自己的终点"的实现位置**

## 2.6 nuPlan 的闭环分数口径（代码级核验，第二十四轮新增）

**动因**：研究对象侧（DP-A01 Diffusion Planner、DP-A06 HDP、DP-A11 Flow Planner）**都以 nuPlan 为主基准**，但本表 §1 对它的描述只有"各类闭环分数"一句，**没有任何代码级口径**。nuplan-devkit **已随多个仓库 vendored 到本地**（`WAM-Flow/nuplan-devkit`、`PC-Diffuser/nuplan-devkit`、`GoalFlow/nuplan-devkit`），故本轮直接读代码核验（**未运行**）。

### 2.6.1 分数是怎么算出来的

`nuplan/planning/metrics/aggregator/weighted_average_metric_aggregator.py:99-124` 的 `_compute_scenario_score` 给出**每个场景**的分数：

```
final_score = multiple_factor × weighted_average_score
其中：
  multiple_factor        = Π（4 个乘性项，见下）
  weighted_average_score = Σ(weight_i × metric_i) / Σ(weight_i)      # 只对"非 None 的列"求和
```

**乘性项（`multiple_metrics`，连乘）** 与 **加权项（`metric_weights`）** 都在配置里（`nuplan/planning/script/config/simulation/metric_aggregator/closed_loop_{reactive,nonreactive}_agents_weighted_average.yaml`）：

| 项 | 权重 / 取值 | 说明（配置里的注释原文） |
|---|---|---|
| `ego_progress_along_expert_route` | **加权 5.0** | "base score can take a value in [0,1] depending on the **ratio of ego to expert progress**" |
| `time_to_collision_within_bound` | **加权 5.0** | "base score can be 0 or 1 depending on the minimum time to collision threshold" |
| `speed_limit_compliance` | **加权 4.0** | "can take a value in [0,1] depending on the amount and duration of over-speeding" |
| `ego_is_comfortable` | **加权 2.0** | "can be 0 or 1 depending on the comfort thresholds on acceleration, jerk and yaw" |
| 其余列 | **default 1.0** | 未在 `metric_weights` 里列出的列一律取 **1.0** |
| **`no_ego_at_fault_collisions`** | **乘性，0 / 0.5 / 1** | "0, 0.5 or 1 depending on whether there is an at fault collision with **VRUs, vehicles or objects**" |
| **`drivable_area_compliance`** | **乘性，0 / 1** | "whether ego drives outside the drivable area" |
| **`ego_is_making_progress`** | **乘性，0 / 1** | "whether ego makes progress more than a minimum threshold compared to expert's progress" |
| **`driving_direction_compliance`** | **乘性，0 / 0.5 / 1** | "depending on how much ego drives in the opposite direction if any" |

**参与打分的 metric 列表**（`simulation_closed_loop_{reactive,nonreactive}_agents.yaml`）：低层 8 项（`ego_lane_change` / `ego_jerk` / `ego_lat_acceleration` / `ego_lon_acceleration` / `ego_lon_jerk` / `ego_yaw_acceleration` / `ego_yaw_rate` / `ego_progress_along_expert_route`）+ 高层 7 项（`drivable_area_compliance` / `no_ego_at_fault_collisions` / `time_to_collision_within_bound` / `speed_limit_compliance` / `ego_is_comfortable` / `ego_is_making_progress` / `driving_direction_compliance`）。

**跨场景聚合**（同文件 `_group_scenario_type_metric:145-172` 与 `_group_final_score_metric:174-220`）：
1. **场景类型分数** = `Σ(场景 final_score) / 该类型的场景数`（注释原文 "scenario_type_score = sum(scenario_final_score) / total number of scenarios"）
2. **最终分数** = `Σ(类型分数 × 该类型场景数) / 总场景数`（`available_values.append(value * num_scenario)` → `total_values = Σ / total_scenarios`）→ **按场景数加权，不是按场景类型等权**

### 2.6.2 与 NAVSIM PDMS 的结构差异（**两者不可互比，且"不可比"的机制不同**）

| 维度 | **NAVSIM PDMS**（见 §2.2） | **nuPlan closed-loop score**（本节） |
|---|---|---|
| 结构 | **乘法链**：`(NC × DAC) × [(5·EP + 5·TTC + 2·C)/12]` | **加权平均 × 乘性连乘**：`(4 项连乘) × [Σw·m / Σw]` |
| 乘性硬门槛项数 | **2**（NC、DAC） | **4**（碰撞、可行驶区、进度、方向） |
| **碰撞项的粒度** | **0 / 1** | **0 / 0.5 / 1**（按 VRU / vehicle / object 分档） |
| 进度项是"跟谁比" | **批内相对分**（按本批候选最大进度归一化 → 候选集变则分数变，§2.4） | **跟专家比**（`ratio of ego to expert progress`，`score_progress_threshold: 2 [m]`） |
| 加权平均的**分母** | 固定 12（5+5+2） | **`Σ(参与列权重)`——参与列由配置的 metric 列表决定** → **换一套 metric 列表，分母就变** |
| 反应式与否影响什么 | v1 非反应式 / v2 两阶段默认反应式（**口径本身也变**，§2.1） | **两套配置的 metric 列表与权重完全相同**，差别只在仿真环境是否反应式 |

**三条口径事实（引用 nuPlan 数字时必须知道）**：
1. **nuPlan 的分数不是"纯乘法链"**——它比 PDMS"温和"：乘性项只有 4 个，且**不含 progress / TTC / comfort**（这三项是加权项）。→ 一个"进度很好但轻微越界"的方案在 nuPlan 上会被乘性项打到 0，而在 PDMS 上 DAC=0 同样归零；但"TTC 差"在 nuPlan 只是掉权，在 PDMS 里是掉 5/12 的权重。
2. **加权平均的分母依赖配置**（`Σ(参与列权重)`），与 NAVSIM 的"EP 是批内相对分"是**同类的口径脆弱性**——**分数不是绝对量，而是相对于"你配了哪些 metric"**。
3. **跨场景聚合是按场景数加权**（不是按场景类型等权）→ **同一批配置下，改场景分布会改总分**；引用 nuPlan 总分时须同时说明场景划分（nuPlan 官方用 `val14` / `test14-random` / `test14-hard`）。

### 2.6.3 与 Bench2Drive 的对照

| 维度 | nuPlan（本节，代码级） | **Bench2Drive**（§2.7，**已代码级核验**） |
|---|---|---|
| 分数结构 | 乘性 4 项 × 加权平均（分母随配置变） | **RC（0–100）× IS（乘性连乘，起手 1.0）** |
| 聚合 | 按场景数加权 | **220 条 route 等权算术平均（分母硬编码）** |
| 额外指标 | 无 | **SR + 5 项 Ability + Efficiency + Smoothness**（另 3 个脚本） |

→ 两者**都不含"批内相对分"这种脆弱性**（那是 NAVSIM 独有的），但 **Bench2Drive 的"分母硬编码 220"是同类的口径脆弱性**，详见 §2.7。

## 2.7 Bench2Drive 的指标口径（代码级核验，第二十四轮追加）

**核验路径**：仓库仍未克隆，但**官方评测栈已被 DIVER 逐字节 vendored 到本地**（`code/repos/diver/`）。本轮用 `raw.githubusercontent.com` 取官方 `0.0.4` 分支的对应文件**逐字节比对，全部 IDENTICAL**：`leaderboard/leaderboard/utils/statistics_manager.py`、`tools/merge_route_json.py`、`tools/ability_benchmark.py`、`tools/efficiency_smoothness_benchmark.py`、`scenario_runner/srunner/scenariomanager/scenarioatomics/atomic_criteria.py`、`scenario_runner/srunner/scenarios/route_scenario.py`；唯一差异是 DIVER 在 `leaderboard/leaderboard/autoagents/autonomous_agent.py:118` 多一行被注释掉的 `pdb.set_trace()`。→ **可把本地 `diver/` 当作 Bench2Drive 官方评测栈来读**（**未运行**）。

**关键前提**：Bench2Drive **一共 4 组指标**（DS / SR / Ability / Effi+Comf），由**三个互不相干的脚本**产出——leaderboard 只出 DS 与 SR 的原料，`merge_route_json.py` 汇总出 DS 与 SR，另两个脚本分别算 Ability 与 Effi/Comf。**报 Bench2Drive 数字时只说"DS"是不完整的。**

### 2.7.1 DS = RC × IS（唯一在 leaderboard 内算出来的量）

`statistics_manager.py`：每条 route 算三个数——`score_route`（该 route 的 `route_completed`，0–100，来自 `ROUTE_COMPLETION` 事件，`:407`）、`score_penalty`（违规乘性折扣，**起手 1.0**，`:369`），然后

```
score_composed = max(score_route × score_penalty, 0)          # :413
DS             = Σ(220 条 route 的 score_composed) / 220      # merge_route_json.py:38
```

**IS 的乘性扣分表**（`PENALTY_VALUE_DICT`，`:21-30`）——**同类事件重复发生会连乘**（两次撞车 → `0.6² = 0.36`）：

| 事件 | 折扣 |
|---|---|
| 撞行人 `COLLISION_PEDESTRIAN` | **0.5** |
| 撞车辆 `COLLISION_VEHICLE` | **0.6** |
| 撞静态物 `COLLISION_STATIC` | **0.65** |
| 闯红灯 `TRAFFIC_LIGHT_INFRACTION` | **0.7** |
| 场景超时 `SCENARIO_TIMEOUT` | **0.7** |
| 未让行紧急车辆 `YIELD_TO_EMERGENCY_VEHICLE` | **0.7** |
| 停车标志 `STOP_INFRACTION` | **0.8** |
| 越出 route 车道 `OUTSIDE_ROUTE_LANES_INFRACTION` | **唯一按比例扣分**（`[0, 'increases']`，`:35`） |
| **低速 `MIN_SPEED_INFRACTION`** | **`'unused'`**（`:37`）→ `set_score_penalty` 里 `elif penalty_type == "unused": pass`（`:359-360`） |

→ **2024-08-19 起"低速"不再影响 DS**（官方 README 原文 "we remove the penalty for minimum speed in calculating the Drive Score"），改列为独立指标 Efficiency（见 §2.7.3）。**`ROUTE_DEVIATION` / `VEHICLE_BLOCKED` 不扣 IS**（`:398-404` 只记 `failure_message`），但它们由两个 `terminate_on_failure=True` 的判据抛出——`InRouteTest(offroad_max=30)` 与 `ActorBlockedTest(min_speed=0.1, max_time=180.0)`（`route_scenario.py:310-315`，代码注释原文 "These stop the route early to save computational time"）→ **提前终止 route ⇒ RC < 100，间接压低 DS**。**route 的 status 只由 `target_reached`（`route_completed >= 100`）决定**（`:418-423`）。

**SR**（`merge_route_json.py:20-28`）：一条 route 记为成功需**同时**满足 ① `status ∈ {Completed, Perfect}` ② **`infractions` 里除 `min_speed_infractions` 外全部为空** → `SR = success_num / 220`（`:39`）。→ **SR 是"零违规完成"的比例，比"跑完"严格得多**。

### 2.7.2 Ability：5 项能力，且 Traffic_Signs 被**双重计数**

`ability_benchmark.py` 的 `Ability` 字典（`:12-18`）把 44 个场景映射到 **Overtaking / Merging / Emergency_Brake / Give_Way / Traffic_Signs** 五类，**一个场景可同时属于多类**（代码注释原文 "Only these three 'Ability's intersect"）。每类 = 该类场景中"零违规完成"的比例（`get_infraction_status:20-26` 与 SR 同一判据）；`Ability_Res['mean'] = sum(...) / 5`（`:158`，**硬编码 /5**）。

- **Traffic_Signs 被算两遍**（`:116-147`）：先由 `update_Ability` 按通用判据 +1，再由专门分支按**路口进度**判据再 +1（`junction_completion = (count+8)/len(waypoint_route)`；成功条件 `record_completion > junction_completion and not stop_infraction and not red_light_infraction`）→ **该项的分母是该类场景数的 2 倍**，且**这一支需要启动 CARLA + `GlobalRoutePlanner` 才能算**（`:88-99`）。
- 该脚本末尾 `assert len(crash_route_list) == 220 - Route_num`（`:170`）→ **220 这个常数被硬编码进断言**。

### 2.7.3 Driving Efficiency 的真实语义（**与名字不符**）

名字像"通行效率 / 完成效率"，代码里实际是**自车均速占周围背景车均速的百分比**：

- 数据源是 `MIN_SPEED_INFRACTION` 事件的 `percentage`，**从事件消息文本里正则抠出来**（`efficiency_smoothness_benchmark.py:268` `re.search(r"\b\d+\.?\d*%", ...)`），消息由 `atomic_criteria.py:2064` 生成：`f"Average speed is {checkpoint_value}% of the surrounding traffic's one"`
- `checkpoint_value = round(actor_speed / (RATIO × mean_speed) × 100, 2)`（`:2054`），且 **`RATIO = 1`**（`:1968`）→ **就是"自车均速 / 背景车均速 × 100"**
- 检查点：`route_scenario.py:308` 传 **`checkpoints=4`** → 每 1/4 路程一个；`terminate` 时若进度 > 95% 再补一个（`:2071-2072`）；**该路段没有背景车时该检查点直接记 100**（`:2056-2057`）
- 聚合：**只对"有 `min_speed_infractions` 的 route"求平均**（`:263-273`：无记录则 `continue`），并**丢弃 > 1000% 的检查点**（`:269-270`）

→ **"Efficiency 251.72"（Simlingo，官方 0.0.4 表）的意思是"平均开得比周围车流快 1.5 倍"，不是"完成了 251% 的路线"**；**高 Effi 与高 DS 不必然同向**（同表 UniAD 120.16 / VAD 163.74，而 DS 只有 38.69 / 38.65）。**引用 Effi 必须声明它是速度比，且只统计有低速事件的 route。**

### 2.7.4 Driving Smoothness（Comfort）：6 项硬编码界 + 20 步分段

`compute_comfort_metric`（`efficiency_smoothness_benchmark.py:65-166`）：先对时序做 **Savitzky–Golay 滤波**（`window=7`、`poly=2`、`deriv=1`、`dt=0.1 s`），再要求 **6 个量同时落在界内**（`_within_bound:196-212`，**严格不等号**）：

| 量 | 界（硬编码于 `:9-26`） |
|---|---|
| 纵向加速度 `lon_acc` | **( −4.05, 2.40 )** m/s² |
| 横向加速度 `lat_acc` | ( −4.89, 4.89 ) m/s² |
| 加速度模长加加速度 `magnitude_jerk` | ( −8.37, 8.37 ) m/s³ |
| 纵向加加速度 `lon_jerk` | ( −4.13, 4.13 ) m/s³ |
| 偏航角加速度 `yaw_acc` | ( −1.93, 1.93 ) rad/s² |
| 偏航角速度 `yaw_rate` | ( −0.95, 0.95 ) rad/s |

- **偏航角速度先做相位展开**（`_phase_unwrap:214-234`，按 `round(Δ/2π)` 累积修正 ±π 跳变）——否则朝向在 ±π 附近抖动会算出巨大的角速度
- **分段评分**：route 按 **20 步（= 2 s @10 Hz）** 切块（`per_step=20`，`:50`），**每块独立判"6 项是否全部在界内"**，route 分数 = 合规块数 / 总块数（`:62`）；**不足 20 步的尾巴被丢弃**（`:59-60`），route 总长 ≤ 20 步时退化为整条一个 0/1 分（`:52-54`）
- 最终 Comfort = 各 route 分数的平均（`:283-286`）→ **它是"合规时间占比"，不是"平均加速度"**

**两处代码级问题（第六类陷阱"命名与实现语义不符"的第 9、10 例）**：
1. **`yaw_acc` 与 `yaw_rate` 在代码里是同一个数组**——`:91-103` 两处都是 `savgol_filter(_z_yaw_rate, polyorder=2, window_length=7)`，**`yaw_acc` 那一处漏了 `deriv=1`**（`lon_jerk`/`magnitude_jerk` 都带了）。→ 因 ±0.95 严格紧于 ±1.93，**`yaw_acc` 这一项恒不生效**，6 项实际只有 5 项在起作用。
2. **`_approximate_derivatives`（`:168-194`）全文件从未被调用**（死代码）。

→ **6 个界来自哪个分布、是哪个百分位，仓库里没有任何说明**（无注释、无生成脚本）→ **引用时必须注明是"Bench2Drive 0.0.4 的硬编码界"**。

### 2.7.5 三个口径陷阱 + 与 NAVSIM / nuPlan 的对照

| 维度 | NAVSIM PDMS（§2.2） | nuPlan（§2.6） | **Bench2Drive（本节）** |
|---|---|---|---|
| 分数结构 | 纯乘法链 × 加权平均（**分母固定 12**） | 乘性 4 项 × 加权平均（**分母随配置变**） | **RC（0–100）× IS（乘性连乘，起手 1.0）** |
| 乘性扣分粒度 | NC 0/1、DAC 0/1 | 0 / 0.5 / 1（碰撞、方向） | **每类违规一个固定折扣（0.5–0.8），同类重复连乘** |
| 聚合 | 场景平均 | 按场景数加权 | **220 条 route 等权算术平均** |
| 口径脆弱性 | **EP 是批内相对分** | **分母随配置变** | **分母硬编码 220** |
| 额外指标 | 无 | 无 | **SR / 5 项 Ability / Efficiency / Smoothness（另 3 个脚本）** |
| 评测入口 | devkit 单入口 | devkit 单入口 | **leaderboard 出原料 → `merge_route_json` → `ability_benchmark` + `efficiency_smoothness_benchmark`**（后两个需要 CARLA 或 agent 产物） |

**三个陷阱**：
1. **分母硬编码 220**：`merge_route_json.py:38-39` 与 `ability_benchmark.py:170` 都把 220 写死；官方 README 原文 "This script will assume the total number of routes with results is 220. **If there is not enough, the missed ones will be treated as 0 score.**" → **部分评测会静默给出偏低的 DS/SR**（脚本只在 `len != 220` 时打印 warning，不报错）。官方建议改用 10 条的 `drivetransformer_bench2drive_dev10.xml` 做消融，但那**不是** 220 条口径。
2. **Effi / Comf 的输入是 agent 自己 dump 的 `metric_info.json`**：`efficiency_smoothness_benchmark.py:243` 逐 route 读 `<metric_dir>/<save_name>/metric_info.json`，该文件由 **agent 侧**写盘——`autonomous_agent.py:146-161` 的 `get_metric_info()` 从 CARLA `hero_actor` 取加速度/角速度/前向向量/右向向量/位置/旋转，`team_code/sparsedrive_b2d_agent.py:524-525` 每 tick 记录、`:577-578` 写 JSON。→ **不 dump 这个文件的提交拿不到 Effi/Comf**，且这两项的数值**依赖 agent 自己的记录方式**（不在 leaderboard 的强制契约里）。
3. **0.0.4 改过口径**：2024-08-19 移除低速惩罚并**把 TickRunTime 从 2000 延长到 4000**；2024-10-14 修了 Ability 计算的 typo（官方声明"不影响 DS 与 SR"）→ **引用 2024-08 之前的 Bench2Drive 数字与之后的不可混用**。


## 2.8 nuScenes 开环规划口径（代码级核验，第二十四轮追加）

**动因**：§1 的 B004 行只有"L2、碰撞率"四个字，而**研究对象侧的四个"非生成式基线"（UniAD / VAD / VADv2 / SparseDrive）与 GenAD 的主表数字全是 nuScenes 开环 L2 / 碰撞**。**四个仓库都在本地**（`UniAD` / `VAD` / `SparseDrive` / `GenAD`），零网络成本。

**一句话结论**：**"nuScenes 开环规划指标"这个名字下至少有四套不同实现，且其中两套是同一份代码里的可切换分支。**

### 2.8.1 四套实现（同名不同义）

| 维度 | **UniAD** | **VAD** | **VADv2** | **SparseDrive** |
|---|---|---|---|---|
| 文件 | `uniad/dense_heads/planning_head_plugin/planning_metrics.py` | `VAD/planner/metric_stp3.py`（**文件名叫 `metric_stp3`**，docstring 原文 "calculate planner metric same as stp3"） | `VAD/VADv2/VADv2_head.py:2710`（内联类） | `datasets/evaluation/planning/planning_eval.py:55`（内联类） |
| 碰撞判定 | **栅格占据**（GT 框 `cv2.fillPoly` 画进 200×200 BEV，再查自车中心格 / 框格） | 同（栅格） | 同（栅格） | **`shapely.Polygon.intersects` 精确多边形相交**（对数据集给的 GT 未来框 `fut_boxes`） |
| 障碍物集合 | 由外部传入的 `segmentation` | `human=[2..8]` / `vehicle=[14..23]`（nuScenes 类 id），**碰撞时把两者合并** | `human=[0,1,2,3]` / `vehicle=[0,1,2,3]`（**两个集合完全相同**） | GT 未来框（无类别过滤） |
| 自车框 | W **1.85** / H **4.084**，**+0.5 m 前向偏移**（`pts = ±H/2 + 0.5`） | 同 | 同 | 同（`ego_box[3:6] = [4.084, 1.85, 1.56]`；`:21` 注释原文 "**follow uniad, add a 0.5m offset**"） |
| L2 归约 | **逐时刻向量**（`compute()` 返回 6 维） | **标量前缀平均**（`compute_L2` 直接 `return ade`） | 无 `update`/`compute`（聚合内联在 head 里） | **逐时刻向量**，但**打印时做前缀累积平均**（`:162`） |
| GT 碰撞时刻 | **剔除**（`m1 &= ~gt_box_coll`，`:108`/`:114`） | **剔除**（`:279`） | **不剔除**——`m2 = torch.ones_like(gt_box_coll)`（`:2934`），**上一行原本的 `m2 = ~gt_box_coll` 被注释掉** | **剔除**（`:100`） |
| 无效样本 | 用 `gt_trajs_mask` 逐坐标乘进 L2 | — | — | **整样本丢弃**（`:144` `if not sdc_planning_mask.all(): continue`） |
| 批大小 | 支持 B | **`assert shape[0]==1`** | — | **`assert B == 1, 'only supprt bs=1'`**（`:96`） |

### 2.8.2 最硬的一条证据：**同一份代码里显式提供两套 L2 定义**

`UniAD/projects/mmdet3d_plugin/datasets/nuscenes_e2e_dataset.py:1033-1047` 打印时按配置项分支：

```python
planning_tab.title = f"{planning_evaluation_strategy}'s definition planning metrics"
...
if planning_evaluation_strategy == "stp3":
    row_value.append("%.4f" % float(value[: i + 1].mean()))   # 前缀累积平均（ADE 式）
elif planning_evaluation_strategy == "uniad":
    row_value.append("%.4f" % float(value[i]))                 # 单步值
else:
    raise ValueError("planning_evaluation_strategy should be uniad or spt3")
```

配置在 `projects/configs/stage2_e2e/base_e2e.py:61`：**`planning_evaluation_strategy = "uniad"  # uniad or stp3`**。

→ **同一个表头 "L2 1s / 2s / 3s"，在 `stp3` 口径下是"0→1s / 0→2s / 0→3s 的累积平均"，在 `uniad` 口径下是"第 1s / 2s / 3s 那一刻的单步值"**。**SparseDrive 的打印（`planning_eval.py:159-165`）走的是 `stp3` 那一支**（`np.array(value[:i+1]).mean()`，且 `avg = mean(value[1], value[3], value[5])`），**VAD 的 `compute_L2` 也返回前缀平均**。→ **三个仓库的同名列，两种不同的量。**

### 2.8.3 四处需要收窄或标注的记录

1. **SparseDrive 的 `obj_col` 累加的是"GT 的碰撞"，不是自车的**（`:102`）：
   ```python
   obj_coll_sum += gt_box_coll.long()      # ← GT 自车轨迹的碰撞
   obj_box_coll_sum += box_coll.long()     # ← 预测轨迹的碰撞（已剔除 GT 碰撞时刻）
   ```
   在 UniAD 里 `obj_col` / `obj_box_col` **都是自车的**（中心格 / 框格两档，`:112`/`:116`）；在 SparseDrive 里 **`obj_col` 变成"GT 碰撞率"**。→ **报 SparseDrive 的 "Collision" 时必须说明取自哪一列**；此条**需与论文表格对照确认是有意为之还是复制粘贴遗留**（此前记的"评测侧用 shapely 精确相交 + 车身 4.084×1.85 + UniAD 式 +0.5 m 偏移"成立，**列语义这一层是本轮新发现**）。
2. **VAD 的 `metric_stp3.py` 里 `update` / `compute` 整段被注释掉**（`:310-336`）→ 该类没有累加器，聚合写在 `VAD.py:616-637`：**按 1s / 2s / 3s 三个前缀各算一次**，`compute_L2` 每次返回一个标量。→ **VAD 的 "L2 1s/2s/3s" 是三次前缀平均，不是三个时刻的值。**
3. **VAD / VADv2 会把行人栅格并进占据栅格**（`VAD.py:618` `occupancy = torch.logical_or(segmentation, pedestrian)`，VADv2 同）→ **其"碰撞"含行人**；而 UniAD 的 `segmentation` 由外部传入（该文件内没有 `pedestrian` 通道）。→ 引用"碰撞率"必须说明**是否含行人**。
4. **两处坐标映射不一致（需运行确认）**：VAD 的 `evaluate_single_coll` 用 `r = bev_dimension[0] − traj`（`:200`）把自车**框**放到栅格行，而同一文件 `evaluate_coll` 里自车**中心点**用的是 `xi = (−bx[0]/2 − yy)/dx[0]`（`:272`）——**两者不是同一个映射**（UniAD 两处都用 `(yy − bx[0])/dx[0]`）。→ **同一批轨迹在 VAD 的"中心格"与"框格"两路判定下落到不同格子**；VAD / VADv2 里原本的 `trajs * [−1, 1]` 两行**被注释掉**，而 UniAD 里是活的。**这一条只有运行才能判定影响量级**，故只作标注，不作结论。

### 2.8.4 与本项目的关系

- **四个基线报的 "L2 / Collision" 不是同一个量** → 与 §2.4（PDMS 的 EP 是批内相对分）、§2.6（nuPlan 分母随配置变）、§2.7（Bench2Drive 分母硬编码 220）并列，是**第四类"口径脆弱性"**：**这次的问题不是分母，而是"同名列的定义本身不同"**。
- **这条给"不用 nuScenes 开环"提供了代码级依据**——Bench2Drive 官方 README（2025-02-05 条目）与 CARLA_GARAGE 都公开呼吁停止报告 nuScenes 开环规划结果；本节的代码证据说明**该呼吁不只是"指标无意义"，还包括"同名指标在各家实现里根本不同义"**。
- **对研究对象的直接后果**：引用 UniAD / VAD / SparseDrive 的 nuScenes 数字做对比时，**必须同时声明取自哪份代码、哪个 `planning_evaluation_strategy`、哪一列**；跨仓库横比这三家的 L2/碰撞在本项目里**不予采信**。

## 2.9 EPDMS 有两套官方实现（EPDMS vs EPDMS\*）——**第三套"跨论文不可比"机制**（2026-09-24 第三十八轮新增）

来源：**DriveFuture（arXiv 2605.09701）§3.3 原文**（PDF + `pdftotext -layout` 逐表核验）。这是**论文侧的独立确认**，与 §2.3 第 4 条（代码侧早已核到的 `filter_m`）拼成完整证据链——**此前只知道"有这个过滤"，不知道"它是后来才被官方榜采用的"**。

**原文（§3.3）**：

> "We distinguish between **EPDMS\*** and **EPDMS** when reporting NAVSIM-v2 results. **EPDMS\* denotes scores computed with the earlier NAVSIM-v2 evaluation implementation before the human-behavior filtering fix was adopted in the official leaderboard.** It preserves the same extended metric set as Eq. (18), but may penalize the agent for violations that are also present in the human reference behavior. **EPDMS denotes the corrected official implementation**, where the human-filtered subscores `f_m(·)` are used consistently. Therefore, **EPDMS is the primary metric** for final comparison, while **EPDMS\* is reported only for compatibility with earlier results computed using the legacy code**."

也就是说：**§2.3 第 4 条那个 `filter_m` 是后来才被官方榜采纳的**，采纳前后的分数**不可混用**。DriveFuture 另外给出了 EPDMS 的加权结构（与 §2.2/§2.3 一致，可交叉验证）：乘性惩罚项 **M_pen = {NC, DAC, DDC, TLC}**、加权平均项 **M_avg = {EP, TTC, LK, HC, EC}**，默认权重 **β_EP = β_TTC = 5、β_LK = β_HC = β_EC = 2**。

### 2.9.1 修复的方向与实测幅度（**不是小差**）

修复逻辑（§3.3 原文）："This filtering mechanism **ignores a rule violation if the same violation is also committed by the human trajectory** in the corresponding scene, reducing **false penalties** caused by annotation noise or contextually necessary maneuvers." → **它只减不增扣分，所以修复后分数系统性偏高。**

DriveFuture 的 **Table 2（navtest）同时给了两列**，是目前唯一能直接量化这个修复的地方：

| 方法 | EPDMS\*（旧实现） | EPDMS（新实现） | 差 |
|---|---|---|---|
| **DriveFuture**（自己） | **86.4** | **89.9** | **+3.5** |
| **DiffusionDriveV2** | **85.5** | **87.5** | **+2.0** |
| TransFuser / Hydra-MDP++ / DriveSuprim / ARTEMIS | 76.7 / 81.4 / 83.1 / 83.1 | —（未给） | — |
| DiffusionDrive / DriveWorld-VLA / DriveVLA-W0 / Recogdrive / Latent-WAM | —（未给） | 84.5 / 86.8 / 86.1 / 83.6 / 89.3 | — |

**navhard 侧同一效应的一个直接实例**（第三十七轮留的"53.2 待核"由此关闭）：**SimScale 论文自报的 navhard 最高分是 48.0**（2025-11，旧实现，原文 "establishing a new SOTA on navhard"），而 **DriveFuture Table 1 里 SimScale 那一行是 53.2**（2026-05，新实现）→ **差 5.2**。逐阶段子指标对照显示两行**是同一个模型**（都是 V2-99；NC 94.5↔94.9、DAC 94.2↔94.3、TLC 99.2↔99.3 几乎相同），差别集中在 **EC 43.2 ↔ 30.9** 与 **HC 96.1 ↔ 93.4**。→ **53.2 不是错误，是口径差。**

### 2.9.2 对本项目的三条约束

1. **现有表里的 v2 数字是一个"混装集"**：`papers/diffusion_planner_ad.md` 与 `preparation.md §6.1` 里的 EPDMS 值**来自不同论文，可能分属两套实现**，而**多数论文不声明用的是哪一套**（DriveFuture 是少数明确区分的）。→ 引用任何 v2 EPDMS 时**必须问一句"旧实现还是新实现"**；答不出来就只能标注"**口径未声明**"。
2. **"DiffusionDriveV2 的 85.5 在两表完全一致"这条"最可信跨论文锚点"要加限定**（见 [judgments.md §B](../judgments.md)）：DriveFuture Table 2 把 **85.5 列在 EPDMS\* 一栏**，它的 EPDMS 是 **87.5**。→ **两表一致的其实是"旧实现"口径**；两个来源若一个用旧一个用新，一致性会**假性成立或假性破裂**。
3. **P8 实例 ③（DiffusionDrive 的 v2 navtest 88.3 vs 84.5）多了一个候选解释**：两套实现之间的差（2.0–3.5）与那个 3.8 分差**同量级**。→ 该分歧**未必是"某家测错"**，可能只是口径不同；**在拿到两边的实现版本前不宜归因**。

> **一句话**：**NAVSIM-v2 的 EPDMS 有"修复前 / 修复后"两套官方实现，同一方法差 2.0–5.2 分，且多数论文不声明用哪套。** 这是继 §2.4 的"EP 是批内相对分"与"两阶段权重以本方法终点为中心"之后的**第三套机制**，也是三套里**最容易在引用时被忽略**的一套——因为它有一个明确的"修复"叙事，看起来像改进，而**不是像口径变更**。

## 2.10 我们手上这份 devkit 是哪一套口径（2026-09-24 第三十九轮新增）

**动因**：§2.9 确立了"EPDMS 有修复前 / 修复后两套实现"，但**没回答我们自己的实验该用哪套**。本地 `code/repos/navsim/` 就在盘上，可以直接核。

### 2.10.1 版本与身份（实测）

| 项 | 值 |
|---|---|
| 版本 | `setup.py` 写 **`version="2.0.0"`** |
| commit | **`0a380a9`**（`Revise highlights and changelog in README.md`），**2025-10-27** |
| 克隆方式 | **shallow**（`git rev-parse --is-shallow-repository` = `true`）→ **本地拿不到历史**，时间线只能用 README 的 changelog |
| 同源的 vendored 副本 | `DiffusionDrive/`、`DiffusionDriveV2/`、`GoalFlow/`、`FeaXMeanFuser`、`WAM-Flow`、`Policy-World-Model`、`FeaXDrive` 各带一份 `navsim/evaluate/`（第二十四轮已核 DIVER 逐字节 vendored） |

### 2.10.2 README changelog 给出的口径时间线（**这是本项目此前缺的**）

| 日期 | 事件 |
|---|---|
| **2024/02/20** | v0.1（初始 demo） |
| 2024/04/21 | v1.0（AGC 2024 官方 devkit） |
| 2024/09/03 | v1.1（navtest 榜） |
| **2025/02/28** | **v2.0** — **EPDMS 首次引入**（"Extends the PDM Score with more metrics and penalties" + 两阶段伪闭环 + 反应式交通） |
| **2025/04/08** | v2.1 — 两阶段反应式交通 agent 支持 |
| 2025/04/13 | v2.1.1 — warmup 数据集小修 |
| **2025/04/24** | **v2.1.2** — 发布 `navhard_two_stage`；**"Updated Extended Predictive Driver Model Score (EPDMS)"** ⚠ **这是 EPDMS 的第一次口径变更** |
| **2025/04/28** | **v2.2** — **AGC 2025 官方 devkit**；发布 `private_test_hard`；**提交截止 2025-05-11** |
| 2025/07/16 | ICCV warmup 榜 + 注册系统 |
| **2025/09/29** | **Bugfix** — "Fixed a bug in **metric filtering** where `multiplicative_metrics_prod` and `weighted_metrics` were not correctly excluded by the **human filter**"（[Issue #151](https://github.com/autonomousvision/navsim/issues/151#issue-3379282167)）⚠ **这就是 DriveFuture 说的 "human-behavior filtering fix" 的最可能对应** |
| **2025/10/27** | 本仓 HEAD（`0a380a9`） |

→ **可操作的推断**（**标为推断**，DriveFuture 未给日期）：**`EPDMS*` ↔ 2025-09-29 之前**、**`EPDMS` ↔ 之后**。按这个界线：
- **SimScale 的 48.0**：其提交对应 **AGC 2025（截止 2025-05-11）** → **旧实现** ✓ 与 §2.9 的结论一致；
- **DriveFuture 的 53.2 / 55.5**（2026-05）→ **新实现** ✓；
- **GTRS-E 的 49.4**（2025-06 论文）→ 按日期应是**旧实现**，**但它与 DriveFuture 表逐字一致** → **说明 DriveFuture 是照抄 GTRS 论文的数字，而不是重测**（这条反过来印证了 §7.7.1 的"混装集"判断）。

### 2.10.3 本地这份是**修复后**的版本（三条实测）

1. **filter 存在且默认开**：`pdm_scorer.yaml:27 human_penalty_filter: True`（类型 `Optional[bool] = None`，注释原文 "ensuring that the ego is not penalized when the human agent makes mistakes"）。
2. **含 2025-09-29 的 bugfix**：`pdm_score.py` 的 `skip_columns = {"multiplicative_metrics_prod", "weighted_metrics", "weighted_metrics_array", "pdm_score"}` ✓，且其后有**重建块**（重算 `multiplicative_metrics_prod` 与 `weighted_metrics`）✓。
3. **⚠ 但 filter 只对 Stage-1 生效**：门控条件是 `scorer._config.human_penalty_filter and metric_cache.scene_type == SceneFrameType.ORIGINAL` → **Stage-2（合成场景）不做人类过滤**。→ DriveFuture 说的 "the human-filtered subscores f_m(·) are used **consistently**" 与代码**不完全一致**（代码是 **Stage-1 only**）。**这一层两家论文都没提。**

### 2.10.4 两处"注释 / 论文 与代码不一致"（本项目的老类别，这里又添两例）

1. **配置注释与代码不一致**：`pdm_scorer.yaml` 注释写 "**now only for driving_direction_compliance**"，但 `pdm_score.py` 的循环是**遍历所有列**（只跳过那 4 个聚合列）→ **注释严重低估了实际作用范围**。→ **以代码为准**。
2. **论文与代码不一致**：DriveFuture 写 `M_avg = {EP, TTC, LK, HC, EC}`、`β_EC = 2`；本地代码**把 EC mask 掉**（见 §2.3 第 3 条）→ **EC 不进 EPDMS**。

### 2.10.5 对本项目的直接结论

1. **实验协议里必须固定 devkit 版本**：写明 **commit `0a380a9`（2025-10-27）**，它**含 2025-09-29 的 human-filter bugfix** → **用它跑出的分数是 `EPDMS`（新实现），与官方榜可比**。**这是路线 ②③ 的第一步（用 SimScale 的 ckpt 跑评测）必须先钉死的一件事。**
2. **报告 EC 时必须说明它不进分**（只作诊断列）；**"涨分牺牲舒适性"这个说法要改写**——EC 的下降**根本不影响分数**（HC 才进分），所以那不是"权衡"，而是"**指标没测这一项**"（见 [sota-plan.md §5.4](../ideas/sota-plan.md) 与 [preparation.md](../ideas/preparation.md) P2c 的第三十九轮更正）。
3. **changelog 时间线是"按日期给已有数字分类"的唯一依据**（因为多数论文不声明口径）→ 已在 §2.10.2 给出界线与三个实例。

## 3. 比较前必须固定的条件

来自 [context.md](../context.md) 的领域约束，逐条可核：

1. **输入权限**：纯相机 / 相机+LiDAR / 矢量化特权输入 / 额外先验（锚点、goal、VLM、未来潜状态）必须分别标注。
2. **backbone**：不同 backbone（ResNet-34 / V2-99）的 PDMS 不可横比。**2026-09-23 已把它落成可核对的清单**（见 [C003 §F](../code/traces/diffusion_planner_code_traces.md)）：四个 NAVSIM 扩散规划器里，**只有 DiffusionDrive 与 V2 的 `transfuser_config.py` 逐字节相同**（真正对齐）；MeanFuser 的 `tf_d_model` 是 128、`lidar_seq_len` 是 4，GoalFlow 的 `tf_d_model` 是 512、轨迹是 11 点/5.5 s。→ **"都用 TransFuser"不等于对齐**，必须逐项核对 `tf_d_model`、`lidar_seq_len`、轨迹视野。
3. **协议与划分**：v1 navtest / v2 navtest / v2 `navhard_two_stage` / Bench2Drive / nuPlan 之间禁止混用。
4. **区分三类信息**：推理输入、训练监督、评价真值——数据里不存在的信息不能靠格式转换补足。
5. **区分三类评价**：开环指标、伪闭环指标、真实闭环驾驶能力不是同一件事。
6. **自己复现基线**：不直接引用他人表格（已发现同一方法在不同论文中相差 4.6 分，GoalFlow 90.3 vs 85.7）。

## 4. 评价层的已知开放问题

四篇 2024–2026 综述在"评价协议未解"上收敛一致（见 [preparation.md](../ideas/preparation.md) 第 2b 节）：跨协议排名反转、子指标饱和、NAVSIM 只是代理证据、闭环下生成式方法常输给更简单方法、推理成本普遍漏报。
