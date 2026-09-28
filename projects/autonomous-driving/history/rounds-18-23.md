# 自动驾驶项目 · 逐轮工作记录 · 第十八至第二十三轮

本卷范围：**第十八至第二十三轮**。内容：特权信息输入权限、GenAD 生成机制、具身迁移机制 + NAVSIM Agent/评测接口、VLA 侧三轮（4 篇全文 + 2 篇核验、4 篇全文 + SimLingo、ORION / MindDrive / Drive My Way）。
索引见 [../history.md](../history.md)；当前状态见 [../state.md](../state.md)。

---

## 第十八轮（「特权信息三段式」的输入权限核验，2026-09-23）

**动因**：[direction/lineage.md](../direction/lineage.md) 里有一条**领域级结构观察**——"**特权信息的三段式**"（① 输入即特权 → ② 输入侧去特权 → ③ 特权作为可选辅助）。该条自己就标注了"**AI 归纳，依据上表的'输入'列**"，即**只有论文级依据**；同时 [preparation.md](../ideas/preparation.md) 第 6 节要求"输入权限必须分别标注"，却一直缺代码级清单。本节把两件事一起补：**逐个读各仓库推理期声明的 `sensors()` / 数据管线实际读取的字段**。

**逐仓库实测（六家）**：

| 仓库 | 相机 | LiDAR | 地图 | ego 运动学 | 路由/命令 |
|---|---|---|---|---|---|
| **ST-P3**（CARLA） | **4 视角** rgb | **无** | 无 HD 地图（只用 GPS 路径点） | IMU + GNSS + speedometer | `RoutePlanner`（GPS） |
| **TCP**（CARLA） | rgb（+第二视角） | **无**——`base_agent.py:170` 的 `sensor.lidar.ray_cast` **整段被注释掉** | 无 | IMU + GNSS + speedometer | 无（用 GPS） |
| **TransFuser**（CARLA） | rgb ×3（+1） | **有** | 无 | IMU + GNSS + speedometer | 无 |
| **UniAD**（nuScenes） | 6 视角 | `use_lidar=False` | **`use_map=False`** | **未发现 `ego_status` 类消费** | `command`（`get_sdc_planning_label`） |
| **VAD v1 / v2**（nuScenes） | 6 视角 | `use_lidar=False` | **`use_map=False`** | **`ego_lcf_feat`**（`gt_ego_lcf_feat`；VADv2 取 idx `[0,1,4]`） | `ego_fut_cmd` |
| **SparseDrive**（nuScenes） | 6 视角 | `use_lidar=False` | **`use_map=False`** | **`ego_status` = CAN bus `pose.accel` + `steeranglefeedback`** | `num_cmd=3` 命令组 |

**三条判断**：

1. **三段式成立，但第 2 段的"相机（+LiDAR）"必须收紧**——代码层**三个工作里只有 TransFuser 吃 LiDAR**：**ST-P3 是 4 视角纯相机**，**TCP 也是纯相机**（LiDAR 行被整段注释）。准确表述是"**只见相机，LiDAR 仅 TransFuser 有**"。
2. **`use_external` 这个 config flag 不可信，而且两个方向都错**：**UniAD 声明 `True` 却全仓未消费**（grep 只命中配置本身，数据集只读 `modality['use_camera']`）；**SparseDrive 声明 `False` 却实际消费 CAN bus 的 `ego_status`**（`instance_queue.py` 的 `ego_feature_encoder` / `prev_ego_status`）。→ **判断"输入权限"必须看数据管线实测字段，不能看 config flag**——这直接改写 [preparation.md](../ideas/preparation.md) 第 6 节的标注方法。
3. **nuScenes 四家在感知侧是彻底去特权的**：UniAD / VAD v1 / VAD v2 / SparseDrive **一致** `use_lidar=False` + `use_map=False`（只有 6 视角相机）。"特权"残留三处：`gt_sdc_*`（UniAD 训练侧标签）、**路由命令**（四家都用）、**ego 运动学**（VAD `ego_lcf_feat` / SparseDrive CAN `ego_status`）。→ 后两者不是网络输入特权，**但跨基准比较时必须声明**：CARLA 系用 GPS + route planner、nuScenes 系用 `command` + CAN bus、NAVSIM 系用 `driving_command` + 矢量化自车状态，**三者可得性不同**。

**产出**：[C005](../code/traces/e2e_trunk_code_traces.md) 新增 **§I**（I.1 输入清单表 / I.2 三条判断），文件头同步；[direction/lineage.md](../direction/lineage.md) 的"特权信息三段式"补**代码级修正**引用块（并注明"标注要按实测字段而非配置文件"）；[preparation.md](../ideas/preparation.md) 第 6.2 节的"输入权限"规则改写；state.md 新增三条判断 + 轮次更新；README / sources / index 同步。

## 第十九轮（GenAD 的生成机制核验：本领域第一条"生成式"路线，2026-09-23）

**动因**：GenAD（[2402.11502](https://arxiv.org/abs/2402.11502)，CVPR'24）是 13 个主干仓库里**规模最大（848 个 `.py`）却一直只做过完整性扫描**的一个。它在 [direction/lineage.md](../direction/lineage.md) 阶段 III 里与"回归/分类"并列，而 README 首句自称 "**GenAD casts autonomous driving as a generative modeling problem**"。本轮把它读完，结论是**这条"生成式"与扩散完全无关，且应被单独归类**。

**核到的四组事实**：

1. **组合关系：基于 VAD 的代码库**。数据集文件就叫 `nuscenes_vad_dataset.py`（类 `GenADCustomNuScenesDataset`）；闭环配置路径是 `closed-loop/adzoo/genad/configs/**VAD**/GenAD_config_b2d.py`；继承了 VAD v1 的 `self.ego_query = nn.Embedding(1, self.embed_dims)`。**但改掉了一处 VAD 的 ego 输入**：`ego_lcf_feat_idx=None`（VAD 用 `[0,1,4]`）。README 自带与 VAD 的对照表：VAD(Paper) 39.42 / VAD(Github) 42.35 / VAD(Reproduction) 38.16 / **GenAD 44.81**。
2. **生成机制：对角高斯隐变量（CVAE 式）+ spatial GRU，不是扩散**。`DistributionModule` 的 docstring 原文 "A convolutional net that parametrises a **diagonal Gaussian** distribution"，`log_sigma` 被 clamp 到 `[-5.0, 5.0]`；`self.latent_dim = 32`、`self.probabilistic = True`（head 内**硬编码**）；`FuturePrediction` 的 docstring 是 "future prediction with **grus**"（`SpatialGRU` × 3 + `Bottleneck`）。**核心是 `GenAD_head.py:1962-1976` 的三行**：
   ```python
   if self.training:  mu, sigma = future_mu, exp(future_log_sigma)    # 后验（当前特征 + 未来 GT）
   else:              mu, sigma = present_mu, exp(present_log_sigma)  # 先验（只用当前特征）
   sample = mu + sigma * noise                                        # 重参数化采样
   ```
   两个分布由 `ProbabilisticLoss`（`@LOSSES.register_module()`，docstring "kl-loss for present distribution and future distribution"）对齐——算的是**两个对角高斯之间的解析 KL** `log σ_p − log σ_f − 1/2 + (σ_f² + (μ_f − μ_p)²)/(2σ_p²)` = KL(N_future ‖ N_present)，配置 `loss_vae_gen` **权重 1.0 启用**。**全仓无任何扩散日程/去噪步/噪声调度**。
3. **规划输出与损失**：`fut_ts=valid_fut_ts=6`（3 s @2 Hz，与 UniAD/SparseDrive/VAD 同视野）；`ego_fut_mode` 默认 3、**闭环 config 覆盖为 6**；逐帧解码后 `torch.stack(..., dim=2)` → **`(B, ego_fut_mode, fut_ts, 2)`**（**只有 (x,y)，没有朝向**）；规划损失**四项全开**（`loss_plan_reg` L1 1.0、`loss_plan_bound` 1.0、`loss_plan_col` 1.0、`loss_plan_dir` 0.5）。
4. **对 §C「轨迹词表/锚点」谱系的补正**：**GenAD 的 ego 规划器没有任何词表/锚点**（`projects/` 全仓 grep `vocabulary|plan_anchor|kmeans` 零命中）；闭环目录里的 `kmeans_anchors` **只在智能体运动预测头**，是给其他交通参与者的。

**三条判断**：① **GenAD 是扩散规划器之前"生成式规划"的代表，且其生成机制与扩散无关** → 做"生成式 vs 非生成式"对照时**必须把 GenAD 作为独立的第四类**（既非单模回归、也非离散词表分类、也非扩散）；② **GenAD 与 VAD 同库、两代、范式相反**（VAD 只留 `loss_plan_cls_expert=200`、其余全 0；GenAD 用回归 + 三项几何约束损失）→ **"VAD 家族"不能当整体引用**；③ **"生成式"不等于"多模态"，且多模态的来源分两类**——GenAD 是**一个 32 维连续高斯**，VADv2 是**4096 离散词表**，这与 C003 §H.4 的"起点先验 5 类"是**不同维度**的分类，两者都要在比较表里标。

**产出**：[C005](../code/traces/e2e_trunk_code_traces.md) 新增 **§J**（J.1 组合关系 / J.2 生成机制 / J.3 规划输出与损失 / J.4 对谱系的补正 / J.5 三条判断），§A 的 GenAD 行与文件头同步；[direction/lineage.md](../direction/lineage.md) 阶段 III 补入"**第一条生成式路线（隐变量）**"并加代码级更正；[preparation.md](../ideas/preparation.md) 新增"生成式有两条路线"一条；[repositories.md](../code/repositories.md) GenAD 行补核验结论；state / README / sources / index 同步。

## 第二十轮（具身侧迁移机制的代码级核验，2026-09-23）

**动因**：[transfer.md](../topics/diffusion-planner/transfer.md) 的 §1（具身侧机制）是**全表唯一没有代码级补充的一节**——§2（VLA）与 §3（世界模型）都已有"代码级补充"块，只有 §1 的 13 条机制停在论文级；而其中 **4 个来源的仓库就在工作空间里**（`diffusion_policy`、`3D-Diffusion-Policy`、`visualnav-transformer`、`diffuser`，见 [repositories.md](../code/repositories.md) §C）。本轮把能核的逐条核掉。

**核到的 4 条（能核的全核）**：

| 机制（§1 原文） | 论文级数字 | 代码级实测 | 判定 |
|---|---|---|---|
| receding horizon action chunk（DP-E09 "Ta=8 最优"；DP-E17） | Ta=8 | Diffusion Policy 22 个 workspace 配置里 `n_action_steps` **14 个取 8 / 8 个取 1**；`horizon` **13 个取 16**；NoMaD `len_traj_pred: 8` | **一致且更强**：主流但**非唯一**；且**两个独立来源都落在 8** |
| 引导式约束（DP-E01，"跨任务差 3 个数量级"） | 3 个数量级 | 函数签名默认 `scale=0.001`；`release-run.sh` 只扫 **`scale ∈ {0.1, 0.001}`（2 个数量级）且单任务** | **需收窄**：已发布脚本只演示 2 个数量级、单任务 |
| 目标掩码（DP-E17，"p=0.5"） | p=0.5 | `nomad.yaml:39` **`goal_mask_prob: 0.5`** ✅；`goal_mask[:, -1] = True`、`all_masks = cat([no_mask, goal_mask])`，**平均时用 `(context_size+2)/(context_size+1)` 重加权** | **一致**，并补上论文未写的重加权系数 |
| 3D 表示条件化（DP-E10，"3 层 MLP 已足够"） | 3 层 MLP | `PointNetEncoderXYZ` 是 **4 层 Linear**（`in→64→128→256→512`）+ 全局 max-pool，`encoder_output_dim: 64`；**"simple" 变体改的是 U-Net 宽度**（`down_dims` 512/1024/2048 → 128/256/384） | **需更正**：编码器 4 层非 3 层；"简单"指 U-Net 变小 |

**代码比论文多出的四条工程细节（§1.2）**，其中第一条最有价值：

1. **引导梯度按后验方差缩放**：`if scale_grad_by_std: grad = model_var * grad`（`functions.py:21-22`，默认开启）→ **`scale` 的绝对意义依赖任务的方差尺度，不能跨任务复用同一个 α**。这**解释了"跨任务差几个数量级"的成因**，也正好补上本项目缺的一环——驾驶侧 DP-A01 的引导强度是**硬编码 1.5**。
2. **引导只在 `t ≥ t_stopgrad` 生效**：`grad[t < t_stopgrad] = 0`，release-run.sh 取 `t_stopgrad=4`（总 20 步）→ 与 DP-A01 的"引导只在扩散末段（t∈(0.005,0.1)）生效"**是同一类做法，两个域独立收敛到"晚引导"**。
3. **每步引导后立刻硬投影条件**：引导循环**内**每步都调 `x = apply_conditioning(x, cond, model.action_dim)` → 与 PC-Diffuser 的"约束投影"同类，**软引导 + 硬投影叠加**而非二选一。
4. **每步可多次引导**：`for _ in range(n_guide_steps)`，release-run.sh 扫 `n_guide_steps ∈ {2,1}`。

**两条判断**：① **§1 的数字必须逐条看代码**（能核的 4 条里 2 条需收窄/更正），与 C003/C005 的结论同构；② **"按方差归一化"应作为本项目引导设计的默认**，而不是沿用硬编码常数。

**产出**：[transfer.md](../topics/diffusion-planner/transfer.md) §1 新增**代码级补充**（1.1 逐条核验 / 1.2 四条新增可搬机制 / 1.3 两条判断 / **1.4 π0/π0.5 核验**），4 行「证据等级」升级为 `全文 + 代码静态检查`，文件头的证据等级定义补 `代码静态检查`；[repositories.md](../code/repositories.md) §C 五行补核验结论并加「代码核验」列；[具身论文表](../../embodied-ai/topics/diffusion-policy/papers/diffusion_planner_embodied.md) DP-E19 行升级为代码静态检查并补明细；state / README / sources 同步。

**π0 / π0.5 的核验（§1.4，同日完成）**：`openpi` 是具身侧最后一个未核验的仓库（**子代理盘点结论：36 个仓库里只剩 `openpi` 与 `navsim` 的 Agent 侧未核**）。核验结果——**论文表四条声称里 3 条代码级一致、1 条需标注**：`pi0.py` 的 `compute_loss` 实测 `x_t = t·noise + (1−t)·actions`、`u_t = noise − actions`、损失 `mean((v_t−u_t)²)`、`sample_actions(num_steps=10)` → **条件流匹配/线性路径/Euler 10 步完全一致**；`action_horizon=50`、`action_expert_variant=gemma_300m` 一致；**但"总 3.3B"在配置里读不到**（配置是 `gemma_2b` + `gemma_300m` = 2.3B，全仓 grep 不到 3.3）。**代码另给四条未记录细节**：① **时间采样是 `Beta(1.5,1)` 而非均匀**（偏向噪声端；**驾驶侧是均匀采样**，如 HDP 的 `torch.rand`）→ 一条未记录的可搬细节；② **代码时间约定与论文相反，作者自承**（`pi0.py:226-227` 原文 "t=1 is noise… yes, this is the opposite of the pi0 paper, and I'm sorry."）；③ **π0.5 的核心改动是"状态从连续输入变成离散语言 token"**（`pi0_config.py:29` 注释原文）+ `max_token_len` 48→200 + 动作专家启用 adaRMS；④ `action_dim=32` 是统一动作空间的 padding。

### 第二十轮·续：NAVSIM 的 Agent / 评测接口核验（2026-09-23）

**动因**：子代理盘点给出的结论是"36 个仓库只剩 `navsim` 的 Agent/规划接口侧未核"（其 PDMS/EPDMS **指标实现**已在第十一轮核过）。这是最后一个角落，且它是**本项目实验协议的落地对象**，接口细节直接决定实验怎么写。

**核到的接口事实（全部有 `文件:行号`）**：

| 事实 | 证据 | 为什么重要 |
|---|---|---|
| agent 契约：**只需实现 3 个抽象方法**（`name` / `get_sensor_config` / `initialize`），训练侧 6 个方法全部可选 | `abstract_agent.py:25/31/37`（`@abstractmethod`）、`:43/51/57/86/97/106` | 评测与训练是**两套可选接口**；**没有 `initialize_training()`** |
| **唯一推理入口** `compute_trajectory(agent_input)`，**无 batch 版本** | 定义 `abstract_agent.py:63`；调用 `run_create_submission_pickle.py:63/77`、`pdm_score` 路径 `run_pdm_score.py:95` | 逐 token 调用，产出 `Dict[token, Trajectory]` pickle；**做吞吐/延迟对比时没有批量通道** |
| **评测禁止读标注场景** | `run_create_submission_pickle.py:41-46`：`requires_scene=True` → `raise ValueError`，原文 "In evaluation, no access to the annotated scene is provided, but only to the AgentInput" | 这是"输入权限"在代码里的**硬边界**，比论文里的口径声明更硬 |
| 输出形状被硬断言：8 poses @2 Hz；**打分口径是 40 poses @10 Hz** | `dataclasses.py:284-289`；`config/common/default_common.yaml:29-33` | **训练/输出口径与打分口径不同**，不能拿"输出 8 点"去反推打分方式 |
| 打分前轨迹被**重新仿真**：速度/加速度被显式丢弃，走 LQR + 自行车模型 | `pdm_score.py:26-54`（`:41` 注释 "velocity and acceleration ignored by LQR + bicycle model"）、`:146` `simulator.simulate_proposals` | **被评分的不是模型输出的点，而是被动力学模型"开过一遍"的轨迹** → 模型输出速度无用、平滑性由 LQR 兜底 |
| `AgentInput` 只有 3 字段（`ego_statuses`/`cameras`/`lidars`），命令在 `EgoStatus.driving_command` | `dataclasses.py:148-154`、`:144` | 引用"输入权限"时要写清命令来自自车状态而非独立输入 |
| `SensorConfig` 预置只有 `build_all_sensors()` / `build_no_sensors()` | `dataclasses.py:782-837` | **没有相机-only / LiDAR-only 预置** → "纯相机"是 **agent 自己填的子集** |
| **代码里没有 "EPDMS" 字样** | `EPDMS` 仅出现在 `README.md` / `docs/metrics.md`；代码命名 `extended_pdm_score_stage_one/_stage_two/_combined`（`run_pdm_score_from_submission.py:389/398/407`） | 检索/复现时按 `extended_pdm_score` 找 |
| 一阶段终点被显式记录并转成全局坐标 | `run_pdm_score_from_submission.py:79-88` | **这正是 §2.4 第 2 条"EPDMS 权重中心是本方法自己的终点"的实现位置** |

**三处口径更正**（写回 [benchmarks.md](../direction/benchmarks.md)）：

1. **"NAVSIM 是非反应式伪闭环"需收窄**——v1/单阶段确为非反应式（`default_common.yaml:22 traffic_agents: non_reactive`；`log_replay_traffic_agents.py:15` 类注释原文 "Replayed (non-reactive) background traffic agents class."），但 **v2 两阶段默认用反应式 IDM 交通**（`navsim_IDM_traffic_agents.py:61`；`docs/traffic_agents.md:28` 原文 "In two-stage simulations … reactive traffic agents are used by default"）。→ **准确表述：v1 及单阶段默认非反应式，v2 两阶段默认反应式**
2. **"navhard" 不是 devkit 的配置名**——devkit 里是 **`navhard_two_stage`**（`train_test_split=navhard_two_stage`）；"navhard" 是**官方 HF leaderboard 的标题简称**（`README.md:6` "Public Leaderboard v2 (navhard)"），changelog 里两者混用。→ 引用**配置**时写 `navhard_two_stage`
3. **划分不是"数据集版本"，而是 SceneFilter 配置**——`config/common/train_test_split/scene_filter/` 下共 **11 个 split**（含容易混淆的 `navtest` 与 `navtest_two_stage`）；且**加载参数不一致**：`navtest`/`navtrain` `num_future_frames: 10`、`navtest_two_stage` **16**、`navhard_two_stage` **8** + `include_synthetic_scenes: true`。→ **"同一份数据换个划分"不成立**

**顺带补齐的可用数字**：`docs/splits.md` 的存储规模——`navtrain` 14 GB log + **445 GB** 传感器；`navtest` 983 MB + **223 GB**；`navhard_two_stage` 892 MB + **31 GB**（合成帧另下）。→ 三套全量约 **700 GB**，与实验环境容量规划一致。

**产出**：[benchmarks.md](../direction/benchmarks.md) 新增 **§2.5 Agent 与评测接口**、§2.1 补 SceneFilter 定义方式与存储规模、§1 的 B001/B012 行更正、§3 第 3 条改为 `navhard_two_stage`、文件头证据等级扩到"指标 + 接口两侧"；[repositories.md](../code/repositories.md) `navsim` 行补代码核验结论；[lineage.md](../direction/lineage.md) 与 [preparation.md](../ideas/preparation.md) 第 6.2 节同步该口径。

**本轮结论**：**36 个仓库的静态核验至此全部结账**（含 4 个零代码/代码不全的负面结论）。→ 静态核验的边际收益已近零，下一阶段的实质推进只有两条：**运行验证**（需算力与数据）或**与用户收敛研究方向**。

## 第二十一轮（VLA 侧代表工作：4 篇全文 + 2 篇代码级核验，2026-09-23）

**动因**：第二十轮末尾的结论是"研究对象侧与 36 个仓库的静态核验已结账"。但 [state.md](../state.md) 待续清单第 3 项早已写明下一步优先级是 **OpenDriveVLA / DriveMoE / AutoVLA**——**VLA 侧是唯一一个完全没有做过代码核验的借鉴来源**。本轮把这一块补上，并用子代理并行取全文（按新目标的授权）。

**第一步：4 篇全文（子代理并行取证 + 主线程复核）**

| 编号 | 论文 | 全文核验到的关键事实 |
|---|---|---|
| VLA-03 | OpenDriveVLA | **自回归离散 token**；nuScenes 开环 3 s / 6 waypoint @0.5 s；纯视觉无 LiDAR；**无词表/锚点、无候选、无 selector**。Table I 显示**同一模型两套口径差一倍**：ST-P3 口径 L2 Avg **0.33 m** / 碰撞 0.10%，UniAD 口径 **0.66 m** / 0.25% |
| VLA-04 | DriveMoE | **底座就是 π0**（§3.1 标题 "Drive-π0 Baseline"）；输出 flow matching 连续轨迹 **10 waypoint**；Action MoE = **1 共享 + 6 非共享、top-3 激活**，门控用**技能标签交叉熵**监督；Bench2Drive **DS 74.22 / SR 48.64%**（对比 DiffAD 67.92、VAD 42.35）；**论文与项目页均无 GitHub 仓库** |
| VLA-11 | AutoVLA | 自回归**离散 action token**，5 s = **10 token** @0.5 s；**K-disk codebook K=2048**；**best-of-N（N=6）+ oracle scorer**；**NAVSIM PDMS 92.12（best-of-N）/ 89.11（RFT）/ 80.54（one-shot）**；Bench2Drive DS 78.84；**真 GRPO（r = r_Driving − λ·r_CoT，β=0.04）**；延迟 fast 1.072 s / slow 10.518 s；**官方代码已发布** |
| VLA-18 | ExploreVLA | 生成与回归**解耦**（自回归生成未来 RGB/深度，MAGVIT-v2 码本 K=8192 **只用于图像 token 化**；轨迹由轻量 MLP head 回归）；**单前视相机**；best-of-N N=6；GRPO G=8 + **世界模型不确定性作内在奖励** + **PDMS 安全门控**；**NAVSIM v1 PDMS 93.7 / v2 EPDMS 88.8**；**论文与项目页均无 GitHub 仓库**（原表"有代码"是误记，`comments` 的 code 链接指向项目页本身） |

**第二步：两篇代码级核验**（写入 [vla/verification.md §5](../topics/vla/verification.md)，仓库登记在 [repositories.md §E](../code/repositories.md)）

**AutoVLA（完整发布）**——`git clone` 连续 5 次 TLS 失败、codeload tarball 停滞在约 1.5 MB，改用 **GitHub API + raw 逐文件取证**：

- **K=2048 实测成立**：`agent_vocab.pkl` 形状 **`(2048, 6, 4, 2)` × 3 类（`veh`/`ped`/`cyc`）**；聚类脚本 `--num_cluster` 默认 2048、`--n_trajs` 2048000、`--tol_dist` 0.05（论文未给后两个）
- **"GRPO"需三处限定**：① **"组"是跨 GPU 的 batch**（`all_gather(reward)`；`batch_size=1` + `devices: [0,1]` → **组大小 2**），不是"同 prompt 采 G 次"；② **无 PPO clip**（`exp(logp − logp.detach())` 比值恒为 1）；③ RFT 时 `limit_val_batches=0` 关掉验证。→ 实质是 **REINFORCE + 组归一化优势 + KL**（KL 用标准 k3 估计量，`kl_beta=0.04` 与论文一致）
- **奖励是本工作空间最强的"真奖励"**：`PDM_Reward.rl_pdm_score` **真跑 NAVSIM 的 `pdm_score`**（40 poses @0.1 s + `PDMScorer`）——对比 DIVER 的 dummy 项、HDP 的 RWR
- **四条论文未写的实现细节**：① 码本的 6 步结构**只在聚类时有用**，解码时只取**末步包围盒 4 角点均值**；② **非 action token 静默映射到索引 0**（零位移）；③ 码本是**三类智能体共用**的（ego 只用 `veh` 分支）；④ `submission = False` **硬编码** → `upsample_trajectory`（5 s → 4 s @10 Hz）**不可达**，实际输出 10 poses @0.5 s（5 s）而 **NAVSIM 按 4 s 打分 → 最后 1 s 不打分**
- **两处论文与代码不符（本轮最强的负面发现）**：论文 Eq.3 写"每 query 采 **G 个候选** `O={o₁…o_G}`"、Eq.4 写**标准 PPO-clipped 目标** `J_i^R = min(ratio·A_i, clip(ratio,1−ε,1+ε)·A_i)`；代码里**每 prompt 只采 1 次**（组由 `all_gather` 跨 GPU 组成）、`per_policy_loss = exp(logp − logp.detach())·A`，**全文件无 `clip`/`epsilon`/`ratio`/old policy**（唯一的 `clip` 是 `clip_grad_value_` 梯度裁剪）→ **引述"AutoVLA 用带 clip 的 GRPO"必须限定为"REINFORCE + 组归一化优势 + KL"**。可信的部分是 Eq. S3：`r_Driving = NC × DAC × ((5·TTC+2·C+5·EP)/12)` **与 NAVSIM 的 PDMS 公式完全一致** ✓
- **best-of-N 的口径限定**：论文 §4.2 原文 "we use an **oracle scorer** to select the optimal trajectory from **six generated candidates**" → **92.12 是"6 选 1 + 真值侧打分选优"**，与已记录的 UniAD 测试时优化、DiffusionDriveV2 的 scorer 选优同类，**引用时必须与 one-shot 的 80.54 并列**。另发现**正文与自身表格不一致**：正文称 best-of-N "achieving the highest PDMS"，但 **Table 1 里 TrajHF 93.95 > AutoVLA 92.12 > Centaur 92.10**（Hydra-MDP 91.26）；且 Table 1 列名（Collision/Area/Direction/Progress/TTC/Comfort）**与 devkit 的 v1 五项、v2 九项都不完全对应** → 引用其 PDMS 前必须自行核对口径
- **一处 docstring 与实现不符**：`rl_pdm_score` 声称 "excluding the two_frame_extended_comfort metric"，代码**未排除任何指标**，且异常时**静默返回 0 奖励**

**OpenDriveVLA（部分发布）**：README TODO 里 **`Release training scripts` 未勾选** → 四阶段训练**只有论文自述级**；**只发布 0.5B 权重**（论文头条是 7B）；无词表/锚点（grep 零命中）；**轨迹是从自由文本里用多步正则清洗流水线抠出来的**——`retrieve_traj` 去字母/中文、修连续小数点、补逗号、修中缀负号、去 z 分量，**不足 6 点用最后一点补齐、多于 6 点截断**，且推理侧是 `do_sample=False` 单样本。→ 这是 **WAM-Flow"轨迹即文本"** 同类做法的**脆弱性直接证据**。

**本轮最有价值的三点**：

1. **具身 → 驾驶的迁移已经有人做了**：DriveMoE 的底座就是 **π0**（工作空间有 `openpi` 官方代码且已核验）→ 本项目的问题应从"能不能搬"变成"**搬到哪一层**"。
2. **NAVSIM v2 有了第一份第三方全子指标复评表**（ExploreVLA Table 2）：**DiffusionDrive 的 v2 navtest EPDMS 是 88.3（MeanFuser 表）还是 84.5（ExploreVLA 表）？差 3.8 分** → **P8 的第三个实例**；而 **DiffusionDriveV2 的 85.5 在两表完全一致** → **目前可信度最高的跨论文锚点**。另：单前视相机的 ExploreVLA（88.8）**已超过**相机+LiDAR 的 DiffusionDrive 系（84.5/85.5）→ **"输入权限"这一维的差距已比"生成机制"更大**。
3. **"RL"的词义清单扩到四种**：DIVER（奖励加权损失）< HDP（RWR）< **AutoVLA（REINFORCE + 组归一化优势 + k3 KL，无 clip）** < FeaXDrive（完整 GRPO）。**只有 FeaXDrive 是完整 PPO 式策略梯度。**

**第三步：顺手清掉两个"限流阻塞"的待续项**（首轮失败是因为 **arXiv API 走 HTTP 会 301、`urllib` 默认 UA 会 406**，改用 **HTTPS + `curl`** 即通）

- **世界模型 arXiv ID 补录：5/7 解决**——**DriveDreamer `2309.09777`、GenAD `2402.11502`、Imagine-2-Drive `2411.10171`、WoTE `2504.01941`（"End-to-End Driving with Online Trajectory Evaluation via BEV World Model"）、RenderWorld `2409.11356`**。**venue 大多仍未获独立确认**：只有 RenderWorld 的 `comments` 明确 **ICRA 2025 录用**；**Imagine-2-Drive 的 `comments` 是 "Submitted to IROS 2025"——是投稿不是录用**；DriveDreamer/WoTE/GenAD 的会议版本在 OpenAlex 查不到（按 DOI 只返回 arXiv 存根，必须按标题查）。**两个同名陷阱**：GenAD `2402.11502`（本项目已代码核验的那篇）≠ `2403.09630`（OpenDriveLab 的数据集论文）。**剩 2 项无解**：**NeMo**（arXiv 按标题找不到，需回综述核对全称）、**OccVAR**（arXiv 无此标题）
- **VLA 边界外清单：4 条复检，SimLingo 升为收录**——**SimLingo（`2503.09594`）的 `comments` 明确 "CVPR 2025. 1st Place @ CARLA Challenge 2024"** → **T1，补入为 VLA-19**（纯相机、Bench2Drive SOTA、三任务含**语言-动作对齐**）；**意外查清 CarLLaVA（`2406.10165`）就是 SimLingo 的 preliminary 挑战赛技术报告**（SimLingo 的 `comments` 原文指向），故**不单列、作指针**；**LMDrive（`2312.07488`）与 RAG-Driver（`2402.10828`）的 venue 仍不可核**（comments 只给项目页/篇幅）→ 留在边界外

**产出**：[vla/papers.md](../topics/vla/papers.md) 新增 §4.2（4 篇全文事实）与 §5（代码级核验，含 5.1 AutoVLA / 5.2 OpenDriveVLA / 5.3 结论）、**VLA-19 SimLingo 行**，§2 证据边界重写，§1 的 VLA-18「有代码」更正，§3 边界外清单改为"复检结果"；[world-model/papers.md §3](../topics/world-model/papers.md) 重写为"补录进度"（含可复用的 arXiv API 用法）；[preparation.md §6.1](../ideas/preparation.md) 新增**第三方复评表 + 三条读数**；[repositories.md](../code/repositories.md) 新增 **§E VLA 侧（2 个）**并更新总数 36→**37**；[state.md](../state.md) / [sources.md](../sources.md) / [index.md](../index.md) / [README.md](../../../README.md) 同步。**仓库新增 `OpenDriveVLA`（38M，commit `10e8095`）**；`AutoVLA` 因网络阻塞未落盘全仓（clone 5 次 TLS 失败、tarball 在 9.6 MB 处截断）。

## 第二十二轮（VLA 侧续做：再加 4 篇全文 + SimLingo 代码级核验，2026-09-23）

**动因**：第二十一轮把 VLA 侧从"零代码核验"推到"2 篇代码核验 + 9 篇全文"。state.md 待续清单第 3 项已写明下一批是 **VLA-15 ORION / VLA-16 MindDrive / VLA-17 Drive My Way**，本轮补上这三篇并追加 **VLA-19 SimLingo**（第二十一轮刚从边界外补入、且是 Drive My Way 的基座）。

**第一步：4 篇全文**（子代理并行取证，主线程复核）

| 编号 | 论文 | 全文核验到的关键事实 |
|---|---|---|
| VLA-15 | ORION（ICCV'25） | **非自回归**：LLM 只出 **1 个 planning token**（§3.2 Eq.3）→ **VAE + GRU** 解码（§3.3 Eq.4–5）；**anchor-free**，**6 条模态**（对应 6 个导航命令）。multi-view、**不用 LiDAR**、**HD map-free**；额外用 **memory bank + history queries**（Tab.5 最优 `N_h=16`）。**无词表**（仅扩散消融版用 K-means 20 锚点）；**无 selector、无 RL**。Bench2Drive base **DS 77.74 / SR 54.62%**；nuScenes L2 **0.34 m** / 碰撞 0.37%。**未报 FPS**；**只自比 diffusion 71.97/46.54 vs VAE 77.74/54.62**（Tab.3）。训练 **32×A800**。**代码已发布**（`xiaomi-mlab/Orion`，667 stars） |
| VLA-16 | MindDrive（ECCV'26） | **两段式**：Decision Expert 出**离散 meta-action（7 速度 + 6 路径）**→ Action Expert 取 logits → **VAE + GRU** 解码（§3.2 Eq.6–7）。speed **6 点/3 s/2 Hz**、path **20 点/1 m/20 m**。**无 LiDAR**、**无轨迹码本**（决策空间 13 个）。**有学到的选择器 π_d** + **RL**：稀疏奖励 **±1**、**用仿真事件而非真值**。Bench2Drive 3B **DS 80.59 / SR 58.26%**。**有延迟**：A100 约 **540 ms**（视觉编码器 ~400 ms），对比 ORION ~1106 ms、ReCogDrive ~750 ms（Tab.7）。**代码已发布**（`xiaomi-mlab/Minddrive`，270 stars） |
| VLA-17 | Drive My Way（CVPR'26） | **基座 + 残差**：**基座就是 SimLingo**，残差解码器（MLP + categorical head）出速度/转向两个离散残差 → **PID**（§5.1–5.2）。**单前视相机**、无 LiDAR/地图；输入含语言指令、路线目标点、**用户 profile**；**特权 PDM-Lite 仅作训练监督**。**训练期 GRPO 每输入采 4 条**，奖励 = 行为相似度，**风格权重由 GPT-5 推断 + 专家复核**（§5.4）。Bench2Drive **Neutral DS 82.03 / SR 70.95**（SimLingo 78.15/65.85）。**未报 FPS**。**代码已发布**（`tasl-lab/DMW`，HF 数据集 `tasl-lab/PDD`） |
| VLA-19 | SimLingo（CVPR'25） | 见下"第二步" |

**第二步：SimLingo 的代码级核验**（写入 [vla/verification.md §6](../topics/vla/verification.md)）

仓库 [`RenzKa/simlingo`](https://github.com/RenzKa/simlingo)（**453 stars**，98.6 MB）。**未克隆全仓**（4 个仓库合计约 1.2 GB，会让工作空间接近翻倍），改用 **GitHub API 逐文件取证**，核了 7 个文件：

- **8 条论文声称全部一致**（语言自回归 + 动作非自回归、单前视相机、0.25 s / 1 m 双表示、LoRA r=32、无词表、Action Dreaming）
- **补上论文未给的两个关键数字**：`pred_len=11`（含当前）→ **N_w = 10 个未来点 / 2.5 s**；`num_route_points=20` + `equal_spacing_route` 里 `np.arange(0, 20, 1)` + `future_waypoints = 20` → **N_p = 20 个点 / 20 m**
- **动作头是"非自回归 + 无词表"的最硬证据**：`route_head`/`speed_wps_head` **都是纯 MLP**（`Linear→SiLU→Linear(→2, bias=False)`），查询是**可学习参数**（`query_embeds_wps (1,20,h)` / `query_embeds_speed (1,10,h)`）——**没有分类头、没有码本、没有 argmax**
- **3 处工程细节不一致**：`future_speed_waypoints = 10 #TODO: read from config`（硬编码）、**`cross_track_error` 的调用被整段注释掉**、`DrivingLabel` 注释写 "0.2s apart" 而配置是 4 Hz（**过期注释**）——**均不影响机制主张的可信度**
- **README 的两条硬事实**：① 官方原文写 "SimLingo-Base (**previously CarLLaVA** - without language capabilities)" → **CarLLaVA = SimLingo-Base 由官方 README 直接确认**（比从 `comments` 推断更硬）；② 数据由 **PDM-Lite（来自 DriveLM 论文）** 生成
- **发布史**：2025/05/08 代码 → 05/26 完整数据集 → **06/25 权重 + 推理代码** → **代码与权重都已发布**

**本轮最有价值的三点**：

1. **"1 个 token → VAE + GRU"成了 VLA 侧的主流解码范式，且与 GenAD 同源**：ORION（1 个 planning token）与 MindDrive（13 个 meta-action）**独立收敛到同一结构**，且 MindDrive 的 VAE 损失类型名 **`ProbabilisticLoss` 与 GenAD 完全相同**、其仓内有 `mmcv/models/vad_utils/` → **三者都长在 VAD 系代码库上**。→ **"隐变量生成"在 VLA 侧也被复用了**，"生成式 vs 非生成式"对照必须把它算进来。
2. **VLA 侧的 RL 有三种形态**：ORION **无 RL**；MindDrive 把 RL 的探索空间压到 **13 个 meta-action**（奖励来自**仿真事件**）；Drive My Way 用 **GRPO 对齐人类风格**（奖励 = 行为相似度，**风格权重由 GPT-5 推断 + 专家复核**）。→ 与研究对象侧的"RL 词义核验"清单并列，**VLA 侧只有 DMW 用 GRPO，且奖励不是 PDM 而是行为相似度**。
3. **SimLingo 是这一轮的"锚"**：CVPR'25 Highlight + CARLA Challenge 2024 冠军，**又是 Drive My Way 的基座**——同一基座被"加语言"（SimLingo 自身）与"加风格对齐"（DMW）各推一步。→ **若本项目要做"生成式规划器 + 下游对齐"，这是一条已有完整对照的实验线。**

**产出**：[vla/papers.md](../topics/vla/papers.md) 新增 **§4.3（4 篇全文事实）+ §6（SimLingo 代码级核验）**，§2 证据边界与 §5.3 计数更新；[repositories.md §E](../code/repositories.md) 扩为**在列 6 个仓库**（新增 SimLingo / Minddrive / Orion / DMW 四行，并说明"未落盘、改用 API 取证"的理由）；[state.md](../state.md) / [sources.md](../sources.md) / [index.md](../index.md) / [README.md](../../../README.md) 同步。**本轮未新增本地仓库**（4 个仓库合计约 1.2 GB，故只做 API 取证），本地快照仍为 **37 个 / 1.65 GB**。

## 第二十三轮（ORION / MindDrive / Drive My Way 的源码核验，2026-09-23）

**动因**：第二十二轮末尾把"三个已发布仓库仍未逐文件核"列为下一步候选 ①。这三个仓库合计约 1.14 GB，**仍不克隆**（沿用 API/raw 逐文件取证；ORION 的 tarball 被完整解出后本地 grep）。

**核到的三组结论**（写入 [vla/verification.md §7](../topics/vla/verification.md)）：

### 1. ORION（VLA-15）：机制成立，但扩散消融在配置层被全量关闭

- **逐条一致**：`constants.py:18` 只注册 **1 个** `EGO_WAYPOINT_TOKEN = "<waypoint_ego>"`（`llava_llama.py:143` 用掩码取它的 hidden state）；`orion.py:215-239` **VAE + GRU**（`latent_dim = 32`、`N_GRU_BLOCKS = 3`、`DistributionModule` + `PredictModel`）；VAE 分支 `ego_fut_mode = 6`；`orion_head.py:104` **`num_memory = 16`**、`memory_len=600`
- **需限定**：`diffusions.py:41/104` 里 20 模态扩散分支确实存在，但 **7 个 stage 配置全部 `use_diff_decoder = False`**，且**没有任何配置传 `plan_anchor_path`** → **论文的扩散对照（Tab.3）不可由已发布配置复现**

### 2. MindDrive（VLA-16）：**教科书式 PPO**，但 π_d 的"路径"分支不是学到的

- **是完整 PPO**（论文未写算法细节，代码给出）：`iter_based_runner.py:314` `RLIterBasedRunner`，`:323-331` `gamma=0.99, clip_range=0.2, vf_coef=0.5, kl_coef=0.5, normalize_advantage=True`；`:465-470` **真 clip**（`clamp(ratio, 1±clip_range)` 取 min）；`:481-482` **value loss** + 独立 `value_net`；`buffers.py:273` **GAE**（`gae_lambda=1.0`）
- **π_d 只对了一半**：速度分支是学到的（`action_distribution` → `sample()`/`argmax`），**路径分支是 `path_idx = torch.argmax(data['ego_fut_cmd'][:,0,0])`——直接取导航命令**
- **其余一致**：7+6 meta-action（`command2hot(..., max_dim=7/6)`）、**双 LoRA**（`action_expert`/`decision_expert`，**RL 只训决策侧 + value head，生成器冻结**）、**VAE+GRU**（`latent_dim=32`）、`ProbabilisticLoss` 权重 3.0、奖励 **±1 来自 CARLA 事件**
- **三处"声明未接线"**：`no_use_kl_and_entro = True` 但接线被注释 → **KL 实际按 0.5 开**；`workflow=[('ppo_train',1)]` 与 `type='EpochBasedRunner'` 并存；`carla_env_scenario.py:505` 的 `_compute_reward` **未被 `step` 调用**

### 3. Drive My Way（VLA-17）：**GRPO 代码未发布**

- README 目录树原文：**`├── grpo/ # GRPO post-training (to be released)`**、**`├── checkpoints/ # Checkpoints (to be released)`**；README 又让用户 `cd grpo` —— **但全仓 14,508 个文件里没有 `grpo/`**
- **全仓无 reward / advantage / GRPO 源文件**；推理侧只读 `.hydra/config_grpo_human.yaml` 并加载别人训好的 checkpoint → **论文的"每输入采 4 条 + 行为相似度奖励 + GPT-5 推断风格权重"完全不可核验**（仓库里唯一的 GPT 产物是 **`gpt-4o`** 的 QA 评分脚本）
- **成立的部分**：**50 个联合离散残差动作**（`speed_list` 7 档 × `steer_list` 7 档 + 1 个 zero，`Categorical` 头 + **可学习温度**）；speed **乘性**（`clip(...,0.5,1.5)`）/ steer **加性**（`clip(...,-0.3,0.3)`）；下游确为 **PID**；基座确为 **SimLingo**（`DrivingAdaptor` 同名同构）

**本轮最有价值的三点**：

1. **"RL 词义核验"清单扩到五种，并出现第一个完整 PPO**：DIVER（奖励加权损失）< HDP（RWR）< AutoVLA（REINFORCE + 组归一化优势 + KL，无 clip）< FeaXDrive（GRPO：clip + log-prob + BC）< **MindDrive（完整 PPO：clip + 独立 critic + GAE）**。→ **只有 MindDrive 同时有 critic 与 GAE**，其奖励是**仿真事件稀疏 ±1**（既不是 PDM 也不是行为相似度）。
2. **"论文声称 vs 代码实测"出现三种新形态**：① **机制在代码里但被配置全量关闭**（ORION 的 20 模态扩散消融）；② **机制只实现了一半**（MindDrive 的 π_d 只有速度是策略）；③ **机制根本没发布**（DMW 的 GRPO）。→ 前两种只有**读代码**才能发现，第三种只有**查目录树**才会发现。
3. **"有代码"分档要再细一档**：**完整**（AutoVLA / SimLingo / ORION / MindDrive）/ **关键部分未发布**（DMW）/ **训练脚本未发布**（OpenDriveVLA）/ **只有项目页**（ExploreVLA、DriveMoE）。→ **VLA 侧在列 6 个仓库至此全部核完**（5 个未落盘，走 API/raw 取证）。

**产出**：[vla/papers.md](../topics/vla/papers.md) 新增 **§7（含 7.1 ORION / 7.2 MindDrive / 7.3 DMW / 7.4 结论）**，§2 证据边界、§4.3 三行、文件头更新；[repositories.md §E](../code/repositories.md) 三行改为"已源码核验"并补实测结论；[state.md](../state.md) / [sources.md](../sources.md) / [index.md](../index.md) / [README.md](../../../README.md) 同步。**本轮仍未新增本地仓库**，本地快照 **37 个 / 1.65 GB**。
