# 扩散规划器代码脉络（第二册：§I–§P）

更新时间：2026-09-23  
证据等级：**代码静态检查**。  
**核验级别（定义见 [ai/rules.md §代码静态检查](../../../../ai/rules.md)）**：本册 §I–§P 的 **6 个新仓库全部为 L3**——走 GitHub trees API + `raw.githubusercontent.com` 逐文件取证，**未克隆**（体积 98–452 MB，会让工作空间接近翻倍）。**级别与第一册的 L1 同级可支持"机制是否实现"的结论**，但不支持"性能与延迟"类结论。  
**⚠ 本册为重建版**：原 `diffusion_planner_code_traces.md` 的 §I–§P 在一次机械拆分中因脚本 bug 被丢弃（该文件为 103 KB、超 Read 工具 64 KB 上限，拆分时后半部分未写入）。本册内容**逐节取自同一批证据的轮次记录**（`history/rounds-09-17.md` 第十四~十六轮、`history/rounds-24a/b/c.md` 的 §9/§21/§22/§23/§24），**事实、`文件:行号` 与数字完整保留**，措辞与原文不完全一致。  
本册承接 [diffusion_planner_code_traces.md](diffusion_planner_code_traces.md)（§A–§H）。

---

## I. PC-Diffuser（DP-A21）——"生成过程内硬约束"到底硬在哪（第十四轮）

（PC-Diffuser 的"硬约束"逐项核验，2026-09-23）

- **动因**：PC-Diffuser（DP-A21）是**驾驶域内唯一声称"认证级硬约束"**的工作，也是 [preparation.md](../../ideas/preparation.md) 方向 A 的决定性对照。§A 只到结构级，§D 第 3 项还留着"QP 求解器实现细节与 1.14 ms 是否可复现"
- **新增产出**：[C003](../../code/traces/diffusion_planner_code_traces.md) 新增 **§I**（I.1 逐项核对 + I.2 三条判断），并把 §D 第 3 项标记为"已解决一半"
### I.1 逐项核对

- **先厘清的一件事：这个仓库里有三个方法、两套 QP**：
  - `safety/pc_diffuser/` = **PC-Diffuser 主方法**，QP 用 **CasADi `ca.qpsol('qp','qpoases')`**，决策变量是**加速度级** `[a, a_nbr(M=10), slack(M=10)]`
  - `safety/safe_diffuser/` = SafeDiffuser 基线，用 **cvxpy + OSQP**（`safety/utils.py::solve_QP`），决策变量是 **ego 位置增量 `[H,2]`**（yaw 被注释掉）
  - `safety/mpc_cbf/` = MPC-CBF 基线，CasADi NLP（N=80），调用时 `safety_mode='direct'`（非 CBF 衰减）
  - → 原 §A 记的"**自带 QP 求解器（未调 cvxpy）**"**对 PC-Diffuser 主路径成立，但不能当作整个仓库的结论**（仓库里确有 cvxpy+OSQP 路径）
- **机制逐项确认（原笔记记载准确，无需更正）**：注入点在 `dpm_solver_pytorch.data_prediction_fn`，滤在**干净估计 x0** 上；QP 目标 `(a−a_des)² + 1e4·Σ(slack+slack²)`，约束含**速度非负**与**逐邻居 degree-1 CBF**；**"只调速度、固定转向"完全一致**（ego 唯一决策量是标量加速度，转向率由 LQR 直写）；胶囊障碍 `h = sqrt(d_seg²) − (r_e+r_n)`，**docstring 原文 "linear gap distance, no bias towards far and fast vehicles"**——§A 记的"线性间距"就是它
### I.2 三条判断

- **但有三处需要限定**：
  1. **"逐去噪步"要看去哪个脚本**：yaml 默认 `shield_every_step: false`，**`scripts/methods/pc_diffuser.sh` 覆盖为 `true`**（并设 `selective_CBF=true`）→ 主方法确实逐去噪步；而 `mpc_cbf.sh` 没覆盖 → **MPC-CBF 基线只在最后一步滤**
  2. **"硬约束"是带松弛的**：每条邻居约束带 `slack`（权重 **1e4**），且 **QP 失败时回退到 nominal（不安全）轨迹** → "certified" 只在 QP 可行且**活跃松弛为 0** 时成立；仓库恰好**记录 `n_slack_total`** 作为诊断量
  3. **QP 次数被严重低估**：`n_steps = 1 if one_step else H − 1`，`for k in range(n_steps)` 里**每个航路点解一次**（被注释的计时打印写 `slack: {n_slack_total}/{H-1}`）→ 配 `steps=10` + `num_poses=80`，**单次规划解 QP 数百次**。→ **"1.14 ms" 是单次 QP 的口径**，不能与端到端延迟混用
- **顺带记录两条易漏的复现前提**：① README 明说为 mpc-cbf / pc-diffuser **改写了 nuplan-devkit 的 tracker**（`action_replay_tracker.py` + `set_latest_action`），否则 **CBF 输出会被 nuPlan 控制器覆盖**；② `distance_functions.py` 实现了 **5 种**距离表示（capsule / sat / sat_euclidean / circles / euclidean）
- **对方向 A 的直接影响**：障碍从"选哪一层"改成"**能不能把 QP 次数从数百降到个位数**"——更硬也更可测；同时更正 preparation 里"**FeaXDrive 未开源，违规率需自行定义**"这句（**FeaXDrive 已开源且判据已核验**）
- **回填**：[DP-A21 笔记](../../topics/diffusion-planner/notes/DP-A21-pc-diffuser.md) 新增「代码核验」、venue 补 **IROS 2026**、"代码：未核验"改为已核验；[论文表](../../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A21 行补代码级补充与 venue；[preparation.md](../../ideas/preparation.md) 方向 A 补代码级补充并更正"FeaXDrive 未开源"

## J. Hyper-Diffusion-Planner（DP-A06）——"无锚点纯扩散"在两个生态里各长什么样（第十五轮）

**目标**：核验 [Hyper-Diffusion-Planner](https://github.com/ZhengYinan-AIR/Hyper-Diffusion-Planner)（DP-A06 / HDP）——它是**唯一同时提供 NAVSIM 与 nuPlan 两套实现**的仓库，也是 preparation.md 里"纯扩散不靠锚点"这条设计前提的唯一代码级候选证据；此前只做到结构级（"同仓含两套实现"）。

**读的文件**：`HDP-nuplan/` 的 `model/module/{decoder,dit}.py`、`model/diffusion_utils/{sde,sampling}.py`、`loss.py`、`train_epoch.py`、`train_predictor.py`、`planner/planner.py`、`normalization.json`、`config/planner/hyper_diffusion_planner.yaml`；`HDP-navsim/` 的 `agent/dp_vla/{dp_vla_agent,dp_vla_rl_agent}.py`、`model/{modeling_dp_vla,decoder,configuration_dp_vla}.py`、`model/diffusion_utils/diffusion_sde.py`、`agent/dp_vla/{scoring,rl_utils}.py`、`config/agent/*.yaml`、`config/agent/_shared/*.yaml`；两份 README。**并逐行对照上游 `Diffusion-Planner/diffusion_planner/model/module/decoder.py`。**

### J.1 "无锚点纯扩散"成立（代码级）

全仓 grep `anchor|kmeans|vocab|cluster` 在模型与配置路径上**零命中**（唯一命中是 nuPlan 数据处理的 `anchor_ego_state` 坐标系，与轨迹锚点无关）；nuPlan 侧 DiT 输入就是**完整 80 步轨迹**，位置编码是 `nn.Embedding(future_length=80)`（逐时间步，**不是可学习的模式 query 集**），推理从单条 `randn(80,4)*0.1` 一次去噪出整条；NAVSIM 侧 `CustomDiT(num_actions=8, dim_action=4)`（8 = 4s@2Hz 路点）同样一次出整条。NAVSIM README 自述 base 模型 88.6 PDMS 是 **"one trajectory per scene, without multi-sample selection, goal conditioning, or anchor-based decoding"**。
### J.2 "扩散损失空间 + 轨迹表示"的受控对照成立（本轮最有价值的一条）

nuPlan 侧 `--diffusion_model_type` × `--diffusion_supervision_type` 各 4 选（`x_start`/`noise`/`v`/`score`，默认均 `x_start`），转换逻辑是 `sde.py::VPSDE_linear.transform` 的四表示互转；**真正的受控证据是两份同主干配置**——`dp_vla_agent_base.yaml` 与 `dp_vla_agent_hdp.yaml` 共用同一 `_shared/model.yaml`（同一 `DpVlaModel`），**只差四个字段**：`model_type`（noise→x_start）、`supervision_type`（null→x_start）、`kinematic_type`（waypoint→diff）、`hybrid_loss_weight`（0→0.05）。NAVSIM 侧 `model_type` **只有 3 选、没有 `v`**（`DpVlaConfig` 校验）。
### J.3 "数据规模"这条主张不可复现（证据边界）

`train_predictor.py` 全部 45 个参数里数据相关只有 `--train_set` / `--train_set_list`（路径），**没有任何规模/子采样参数**；NAVSIM 侧只有三个固定 split；仓库**不含实车数据集**。→ 引用时必须**单独降级为"仅论文自述"**，不能与前两条并列声称"代码级已核验"。
### J.4 HDP-RL 不是 GRPO，是优势加权回归（RWR）

`DpVlaRlAgent._rl_train_step` 的三行是 `rewards=(R−mean)/std`（**组内归一化优势**）→ `weights=exp(rewards)` → `reward_weighted_mse=(per_sample_mse*weights).mean()`。有正确的优势估计，但**没有对数概率、没有概率比、没有 PPO clip、没有 KL**。→ 本项目的"RL 词义核验"清单现在覆盖三种实现：**DIVER 最弱（`(1+r̄)` 乘性、无组内基线）< HDP（RWR）< FeaXDrive（真 GRPO）**，只有 FeaXDrive 是策略梯度。

### J.5 意外发现：相对上游 Diffusion Planner 的四处 README 未声明差异

逐行对照 `decoder.py` 后确认：

- **删掉联合预测**：上游 `xT = cat([current_states, randn(B,P,future_len,4)*0.5])` 是 **ego + 近邻一起生成**；HDP 是 `randn(B,80,4)*0.1`，**只生成 ego**。（README 未提，但 `train_predictor.py` 参数帮助里写了 **"[Warning] Neighbor prediction is deprecated in HDP"**）
- **删掉当前状态锚定 token**：上游把 current state 放序列首位并用 `initial_state_constraint` 每步钉死；HDP **没有首位 token**，当前状态改由 `DiT.ego_state_proj` 注入 ego 速度。
- **删掉引导模块**：上游有 `model/guidance/`（`collision_guidance_fn`、`guidance_wrapper.py`、`diffusion_planner_guidance.yaml`）且 `_guidance_fn` 非空时用 `guidance_type="classifier"`；HDP **`guidance_fn: null` 且根本没有 `guidance/` 目录**，`HyperDiffusionPlanner` 直接返回模型输出（**无引导、无 refine、无后处理**）。
- **初始噪声尺度 0.5→0.1**（NAVSIM 侧 `sample_temperature=0.5`）。
- → **判断**：引用 HDP 时**不能把它当作"Diffusion Planner + 损失空间消融"**——它是一个**退化为 ego-only 的 planner**。

### J.6 另外两处"声明未接线"

（与 DIVER 的 dummy reward、FeaXDrive 的零权重投影项同类）

- `DpVlaModel` 声明了**双 LoRA 适配器（positive/negative）+ CFG**（`generate()` 里 `(1+cfg_scale)·pos − cfg_scale·neg`），但**全仓没有任何地方调用 `init_lora_adapter()`** → `generate()` 永远走 base 分支，**CFG 与 LoRA 不可达**。
- `DpVlaRlAgent` 的 `self.only_ep` **被赋值两次但全仓从未被读取**——"only_ep 模式"是死变量。

### J.7 还核到两条细节

① hybrid loss 的 README 表述（`L_velocity + ω·L_waypoints`）与代码不完全一致——`train_epoch.py:105` 的第一项是**所选空间下的扩散损失**（默认 `x_start` 时不是 velocity），第二项是**预测干净轨迹的路点 MSE**（`detached_integral(..., detach_window_size=10)`，nuPlan 硬编码 10、NAVSIM 走 config 默认 1）；系数默认值两生态不一致（nuPlan **0.01**、NAVSIM base **0.0** / HDP **0.05**）。② `detached_integral` 的机制是"cumsum 的滑窗去梯度"——只保留最近 `window_size` 步的梯度。

### J.8 产出

[C003](../../code/traces/diffusion_planner_code_traces.md) 新增 **§J**（J.1–J.8，含三张对照表）；[论文表](../../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A06 行升级为代码静态检查并补六条代码级补充，**并按核验结果把 DP-A06 从 C 节（截断扩散 + 锚点先验）移入 B 节（无锚点先验：纯高斯起点）**（C 节保留明细行并加反向指针，CSV 的 `分组` 同步）；[preparation.md](../../ideas/preparation.md) 把"HDP 摘要称…"这条**拆成三条**（成立 / 成立 / 仅论文自述）；[topics/lineage.md](../../topics/diffusion-planner/lineage.md) 与 [direction/lineage.md](../../direction/lineage.md) 的"跨生态已打通"补上"两套实现不是同一模型的移植"这一限定；state / index / sources / repositories / README 同步。**核验覆盖度：逐文件核验 12 个扩散规划器仓库，只剩 DriveFine（DP-A29）为结构级。**



## K. DriveFine（DP-A29）——仓库零代码，研究对象侧 13 个仓库全部结账（第十六轮）

**目标**：核验 DriveFine（DP-A29）——第十五轮结束时它是研究对象侧**唯一还没逐文件核验**的仓库（此前只到"确认 README 明写基于 ReCogDrive + LaViDa"的结构级）。

**结论：仓库零代码，核验到此为止。** 三重独立证据：

| 证据 | 结果 |
|---|---|
| 本地快照 `find` 全量列举（含隐藏文件，排除 `.git`） | **共 2 个文件**：`README.md`（3,135 B）+ `images/overview.png`。按扩展名统计只有 `md` × 1、`png` × 1。**零个 `.py`、零个配置、零个脚本** |
| `git log --oneline --all` | **仅 1 个 commit**（`f44f86e update`），本地只有 `main` 分支 |
| GitHub API `GET /repos/MSunDYY/DriveFine/branches` | **只有 `main` 一个分支**，SHA = `f44f86e5e9e48645acbffef340d9b3df90e60654`，**与本地快照完全一致** → **排除"代码在别的分支上"** |
| GitHub API 仓库元数据 | `size` = 227 KB、`created_at` = **2026-02-16**、`pushed_at` = **2026-02-17**（**创建后第二天起再无推送**）、30 stars、**无 tag、无 license** |

**README 全文只有**：标题、arXiv 徽章（2602.14577）、作者与单位（华中科技大学 / **小米 EV** / 清华 AIR）、Abstract、一张框架图、News（**仅一条**：`2026/2.17` 论文放上 arXiv）、Acknowledgement（ReCogDrive + LaViDa）、Citation。

**判断**：

1. **DriveFine 是"论文发布当天建的占位仓库"，从未发布代码**——News 里**没有**任何"code will be released"条目，创建与最后推送就是论文上 arXiv 的那两天，此后 7 个月无更新。
2. → 其**可插拔 block-MoE、生成/精修双专家、梯度阻断、hybrid RL 策略**全部只能停留在**论文自述级**，与 [E2E-05 Hydra-MDP](../../direction/notes/E2E-05-hydra-mdp.md)、[E2E-10 DriveVLM](../../direction/notes/E2E-10-drivevlm.md)、WM-18 WorldRFT 同类。
3. **`repositories.md` 的 DriveFine 行由"有代码"改为"零代码"**，它是本项目查出的**第 3 个零代码仓库**（研究对象侧第 2 个，与 WorldRFT 并列）。累计口径（**当时 36 个在列仓库**，第二十一轮起为 37 个；此后第二十四轮复查把"无代码/代码不全"进一步扩到 **11 条**，见 [sources.md C002](../../sources.md)）：36 个里 **7 个实际无代码或代码不全**（sources.md C002 行、state.md、README.md 的计数同步从 6 改 7）。
4. **研究对象侧的代码级证据由此穷尽**：13 个仓库 = **12 个逐文件核验 + 1 个零代码**。→ 这条边界比"还剩 1 个没做"更有用：**扩散规划器这条线的代码级工作已经结账**，再往下推进只有两条路——**换领域做代码核验**（E2E 主干 13 个 / 世界模型 4 个 / VLA 3 篇仍有未核验项），或**进入运行验证阶段**（需算力与数据，见 state.md 待续清单第 9 项）。

**产出**：[C003](../../code/traces/diffusion_planner_code_traces.md) 新增 **§K**（含三重证据表与四条判断），§A 的 DriveFine 行改为"组合关系无法核验"、§H.4 与文件头改为"13 个仓库全部结账"；[论文表](../../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A29 行与 CSV 标注**零代码**；[repositories.md](../../code/repositories.md) DriveFine 行改为零代码并把它加进"实际无代码/代码不全"清单（7→8 条，其中"论文声称有代码但实际没有"由 4 条改 5 条）；[topics/lineage.md](../../topics/diffusion-planner/lineage.md) 组合关系表补注；sources / state / README 同步。

## L. Flow Planner（DP-A11）——"无锚点 + 无选优"的纯流匹配（第二十四轮）

DP-A11 Flow Planner 的代码级核验（研究对象侧最后一个"代码未获取"缺口关闭）

**动因**：DP-A11 是研究对象侧**唯一"代码本体未获取"**的仓库（`git clone` 与 codeload tarball 都在约 4.5 MB 处稳定截断）。本轮改用**逐文件取证**（GitHub trees API 1 次 + `raw.githubusercontent.com`），把**全部 72 个非图片文件**抓到本地并逐一核对字节数（与树接口 blob size 完全对齐，`truncated=false`）→ **该仓库的静态核验不再有缺口**，结论写入 [C003 §L](../../code/traces/diffusion_planner_code_traces-2.md)。

**仓库元数据**：`main` / `size` 69669 KB / `pushed_at 2026-04-03` / **271 stars** / MIT / `created 2025-10-11`；84 blobs = 49 `.py` + 18 `.yaml` + 2 `.sh` + README + requirements + LICENSE + 12 图片。代码全在 `flow_planner/` 下。

**核心结论**：

- **零锚点、零词表、零选优**：全量 grep `kmeans｜vocabulary｜codebook｜cluster｜topk｜nms｜scorer｜select` **零命中**（仅地图/智能体预处理的无关语义），**仓库内不存在任何 `.npy`/`.pkl`/`.pt`/`.bin`**。
- **候选轨迹的构造**：`traj_chunking(future, action_len=20, action_overlap=10)` 重叠滑窗 → **7 个 action token**（`(80-10)/(20-10)`）；推理 `x_init = randn(...)` → **4 步 midpoint ODE**（`sample_steps=4, sample_method=midpoint, sample_temperature=1.0`）→ `assemble_actions(method='average')` 计数平均拼接 → `planner.py:131` **直接取 `outputs[0, 0]`**。
- **流匹配本体**：`AffineProbPath` + `CondOTScheduler`；`model_type: x_start` → **回归终点而非速度场**；损失 = **普通 MSE**（`ego_planning_loss 1.0` + `consistency_loss 0.5`）。
- **CFG 的无条件分支是"抹掉邻居"**：`cfg_type: neighbors`、`cfg_prob: 0.3`、`cfg_weight: 1.8`、`cfg_neighbor_num: 10`（`mask_flags[:, 10:, :] = 1`）→ 引导方向 = "假如没有其他车"，**比论文表述更具体**。
- **`class FlowPlanner(DiffusionADPlanner)`**：继承 `model/model_base.py` 的抽象基类（含 `forward_train`/`forward_inference`/`encoder`/`decoder` 钩子与 `Scheduler` 基类）。
- **编码器不吃自车历史**：`with_ego_history: false`。
- **README 的 "w/ refine" 是外部评测协议**：仓库内 `refine` 只出现在 `data/augmentation/state_aug.py`（`NUM_REFINE=20`、`REFINE_HORIZON=2.0`），是**数据增广的五次样条**，不是推理期选优 → 引用 94.31 时必须与 w/o refine 的 90.43 分开。
- **两处"配置声明但未生效"**：① `time_sampler` 的 `alpha: 1.0 / beta: 1.5`（注释还写 "beta distribution shifts to early steps"）在 `sample_method: uniform` 下**不生效**（对照：具身侧 π0 真用 `Beta(1.5,1)`）；② `assemble_method` 的类默认 `linear` 被配置覆盖为 `average`。

**判断**：**"无锚点纯生成"在研究对象侧有了第二个代码级实例**（前一个是 DP-A06 HDP）→ **"生成式规划器必须靠锚点/词表"在 nuPlan 与 NAVSIM 两个生态里各被证伪一次**；且 **Flow Planner 是"纯生成、无选择"的最干净基线**，对"生成 vs 选择"的对照实验有直接价值。

## M. ReCogDrive（DP-A28）——"DiffGRPO"是第六种"RL"（第二十四轮）

ReCogDrive（DP-A28）的代码级核验——"DiffGRPO"是第六种"RL"

**动因**：上一节（§20）的全表核验发现 **DP-A28 此前记为"未见官方"是错的**——[xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive) 代码与权重都已公开。它有两个不可替代的位置：① 是 **WM-11 DriveLaW 的 `ReCogDriveDiffusionPlanner` 的上游**；② 它的 RL 阶段自称 **Diffusion Group Relative Policy Optimization（DiffGRPO）**，而本项目已维护一份"RL 词义核验"清单（五种）。→ 补做代码级核验（**未克隆**，走 `raw` 逐文件取证；全仓 359 个 blob）。

**逐项核对（实现全在 `navsim/agents/recogdrive/recogdrive_diffusion_planner.py`，全仓无任何文件名含 `grpo`/`ppo`）**：

| 要素 | 有无 | 证据 |
|---|---|---|
| 对数概率 | ✅ **真** | `:754 get_logprobs`；`:813-815` `std = exp(0.5·logvar).clamp(min=min_logprob_denoising_std)` → `Normal(mean, std)` → `dist.log_prob(x_t_minus_1)`；`mean/logvar` 来自**带梯度的** `p_mean_variance`（`:805`），采样链 `.detach()` |
| 组内归一化优势 | ✅ | `:852-854` `advantages = ((rewards_matrix − mean_r) / std_r).view(-1).detach()` |
| 去噪步折扣 | ✅ | `:862` `discount = gamma_denoising ** (num_denoising_steps − denoising_indices − 1)`，`gamma_denoising = 0.6` |
| 策略梯度项 | ✅ | `:872` `policy_loss = -torch.mean(log_probs * adv_weighted_flat)` |
| **重要性比率 `ratio`** | ❌ **全仓无** | grep `ratio` 只命中 `:233` 的 DDIM `step_ratio` |
| **比率裁剪** | ❌ | `eps_clip_value`（`:80`/`:266`）**是采样时对 `pred_noise` 的裁剪**（`:426-428`），**不是 PPO 裁剪** |
| **KL** | ❌ | `:26` `from torch.distributions import ... kl_divergence` —— **import 了却全文件零次调用** |
| **critic / GAE** | ❌ | grep 零命中 |
| BC 正则 | ✅ | `:876-886` `teacher_chains = self.old_policy.sample_chain(...)` → `bc_loss = -bc_logp.mean()` → `total_loss = policy_loss + bc_coeff·bc_loss`，`bc_coeff = 0.1`。**`old_policy` 只当 BC 教师**（`:296-298`），不参与比率或 KL |
| 奖励 | ✅ **真 PDM 分数** | `:904 reward_fn` → `:916-923` `pdm_score(..., scorer=self.train_scorer)` → `asdict(pdm_result)["score"]` → `.detach()`；权重 `progress 10.0 / ttc 5.0 / comfortable 2.0` |
| 优势裁剪 | 有开关但**默认空操作** | `:84-85` `clip_advantage_lower_quantile = 0.0` / `upper = 1.0`（全分位 = 不裁） |

**开关链**：`recogdrive_agent.yaml:21` **`grpo: False`**（`GRPOConfig` 与工厂默认也都 False）；`recogdrive_agent.py:200-205` 是三路分支；**4 个 RL 脚本显式覆盖 `agent.grpo=True`** 并配 `metric_cache_path` / `reference_policy_checkpoint`。→ **与 ORION 的"机制在代码里但被配置全量关闭"不同，这里 RL 脚本确实打开了它。**

**三条判断**：① **"DiffGRPO" = REINFORCE + 组内相对优势 + BC 正则**，不是 PPO/GRPO 完整形态 → **"RL 词义核验"清单扩到六种**：DIVER < HDP(RWR) < AutoVLA < **ReCogDrive** < FeaXDrive(GRPO) < MindDrive(完整 PPO)；**只有 MindDrive 有 critic 与 GAE，只有 FeaXDrive 与 MindDrive 有比率裁剪**。② **奖励是真的**（逐条跑 NAVSIM `PDMScorer`），与 AutoVLA 同级，远强于 DIVER 的 `0.2·map(dummy=1.0)`。③ **RL 收益可量化且两个规模一致**：Base 2B **84.1 →(IL) 86.5 →(RL) 90.8**（**+4.3**）、Large 8B **86.4 → 86.5 → 90.4**（**+3.9**）→ **这是本项目方向 A/B 的正向证据**；**但口径冲突**：ReCogDrive 自报 **90.8**，FeaXDrive 对比表记 **90.5**（本项目此前采用 90.5）→ **"同一方法跨论文数字不一致"的又一实例**。

**产出**：[C003 §M](../../code/traces/diffusion_planner_code_traces-2.md) 新增一节（逐项核对表 + 开关链 + 三条判断），文件头同步；[papers/diffusion_planner_ad.md](../../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A28 行补代码级结论与 README 数字；[state.md](../../state.md) 的"RL 词义核验"清单扩到六种、待续第 13 项状态更新；[preparation.md §2](../../ideas/preparation.md) 新增"RL 阶段净收益 ~4 PDMS"这条事实；[repositories.md §F](../../code/repositories.md) / [README.md](../../../../README.md) 同步。**本轮未克隆任何仓库**（ReCogDrive 走 `raw` 取证）。

## N. GuideFlow（DP-A12）——navhard SOTA 的三条机制，发布代码里两条不在评测路径上（第二十四轮）

GuideFlow（DP-A12）的代码级核验——navhard SOTA 的三条机制，**两条不在评测路径上**

**动因**：GuideFlow 是**与本项目研究对象同基准（NAVSIM v2 `navhard_two_stage`）的当前 SOTA**（EPDMS **43.0**，同表 DiffusionDrive 只有 24.2），论文卖点"受约束流匹配"正对**方向 A（约束注入层级）**。它的代码此前只被记为"arXiv 指向的仓库是占位"——本轮按 §20 的指向链找到真仓库 **[adept-thu/GuideFlow](https://github.com/adept-thu/GuideFlow)**（`main`，1513 个 blob），走 `raw` 逐文件取证（**未克隆**，缓存 57 个文件）。

**论文三条机制与代码的对应**：

| 论文主张 | 代码实况 |
|---|---|
| **CVF**（Eq.14）：速度场朝约束方向**投影**，λ=0.1，每步 | 只在 `navsim_train/agents/flowdrive_unet/transfuser_model_v8.py`：`:556 limited_v_pred = limited_anchors − zt`（**在采样循环之外算一次**）→ `:579 zt = zt + (v_pred + 0.11*limited_v_pred) * dt`，紧跟注释 **`# 0.05 ,0.08 ,0.15, 0.10, 0.12 , 0.11 best`**。→ **不是投影**（全库无 `v − (v·n)n` 之类算子），是**朝初始锚点方向的常数速度偏置**；**λ 实取 0.11 且是调参选出的**；"约束"= **GTRS 给的整条专家轨迹**，不是可行驶区/车道/障碍物梯度 |
| **CF**（Eq.16）：第 `k_c=50` 步替换为 anchor，只做一次 | `navsim_test/agents/flowdrive/transfuser_model_v6.py:505-506` `if i_step < k_num: zt = limited_anchors` —— **`k_num` 全仓只此一处引用、无定义** → **按此文件运行会立即 `NameError`**；语义也变成"前 `k_num` 步都替换"。`k_c=50` 的唯一痕迹是**死代码**（各版本 `self.num_inference_steps = 50` 从未被读取） |
| **RFE**（Eq.17–18）：**训练期**能量项 | **训练损失里没有能量项**：`transfuser_loss.py:30-35` 只有 `trajectory/agent_class/agent_box/bev_semantic` 四项。v10 的 "rfe Module" 是**推理期**：`:203-207` 从**网络预测的 BEV 语义图**算 `distance_transform_edt` 双向 SDF → `:290 ESDFEncoder` → `:558-560` 作为**条件**喂进模型，`v_pred = v_pred_no_cond + 2.5·(v_pred_cond − v_pred_no_cond)`（**这是 CFG**） |
| **K = 100** | ✅ 成立且未被覆盖（`dp_config.py:43 denoising_timesteps = 100`；代码写死 `range(0,100)`、`dt = 1/100`） |

**本轮最重要的一条**：仓库里是**两套并列代码树**（`navsim_test/` 与 `navsim_train/`），**版本切换靠注释 import 行**。**评测侧 `navsim_test/agents/flowdrive/transfuser_agent.py:12` import 的是 `v6`**，而 **`navsim_test/agents/flowdrive/` 只发布到 v6，没有 v8/v9/v10**；**CVF 只在 v8、RFE 模块只在 v10**（训练侧 import v10）→ **按仓库给的评测脚本（`scripts/testing/test_flow.sh`）直接跑，命中 v6：既无 CVF 也无 RFE，且会撞上未定义的 `k_num`**。三条机制的开关全是模型 `__init__` 里的 Python 常量（`use_guidance_limit` / `use_condition_limit`），**没有任何 yaml/sh 字段** → **"配置覆盖链"这条老陷阱在这里不适用，真正的坑在 import 层**。

**其余硬发现**：① **`flow_matching.py` 是三处 11 字节占位文件**（全文 `# step = 50`）——**该放流匹配实现的位置是空的**；② **100 条候选默认取 `proposals[0]`**（`agent_lightning_module.py` 注释写 `# randomly choose a dp proposal`，**实际不是随机**），**学到的 scorer 只在 `combined_inference=True`（默认 False）时启用**，全仓无 `no_scorer` 字面量；③ **代码真正依赖的两个资产都不在仓库内**（`transfuser_config.py:17 plan_anchor_path = /nas/.../fps_navsim_traj_768_3.npy` 与 CF 的 GTRS `navhard_two_stage.pkl`，都是**硬编码作者本机绝对路径**），而仓库里反而有 2 个**零引用**的词表（`traj_final/16384.npy` / `8192.npy`）；④ **v10 推理时把 `EP SCORE` 写死为常数 `1.0`**（`:513`），README 自称的 "v10 = command + EP SCORE as condition + rfe Module" 里 **EP 条件并未真正注入**；⑤ README 的 Model Zoo 表里链接名与实际文件名不符。

**四条判断**：① **GuideFlow 的 43.0 目前无法从发布代码复现**（评测路径与论文机制不在同一文件，且 v6 有未定义变量）→ **引用时必须标"仅论文自述 + 发布代码不可直接复现"**；② **"受约束流匹配"要打折扣**：**没有投影算子、没有约束梯度、没有训练期能量项**，实际是"朝一条 GTRS 专家轨迹做常数速度偏置 + 推理期 ESDF 条件 CFG"；③ **λ 与 `k_c` 两个论文超参都无法从发布代码复现**；④ **同类陷阱的第三种形态**——此前记过"配置覆盖链"（TransFuser 的 `n_layer`）与"配置全量关闭"（ORION 的扩散消融），**GuideFlow 是"两套并列代码树 + 靠注释切换 import，而论文机制落在未被评测路径 import 的版本里"** → **读这类仓库必须先确认"评测入口 import 的是哪个文件"**。

**产出**：[C003 §N](../../code/traces/diffusion_planner_code_traces-2.md) 新增一节（对照表 + N.1–N.4），文件头同步；[papers/diffusion_planner_ad.md](../../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A12 行补代码级结论；[state.md](../../state.md) 新增**第七类陷阱**（判断边界）与待续第 13 项状态更新；[preparation.md 方向 A](../../ideas/preparation.md) 新增一条"把最像投影的那一篇也打掉了"的补充；[repositories.md §F](../../code/repositories.md) / [README.md](../../../../README.md) 同步。**未克隆任何仓库**（走 `raw` 取证）。

## O. LCS（DP-A26）与 BridgeDrive（DP-A08）（第二十四轮）

LCS（DP-A26）与 BridgeDrive（DP-A08）的代码级核验

**动因**：上一节（§20）的全表核验新发现 6 个仓库；§21、§22 已核完 ReCogDrive 与 GuideFlow。本轮把**与研究对象接点最紧的两个**也补上：**LCS**（"引导成本"——单次前向替代两次前向的 CFG）与 **BridgeDrive**（扩散桥，且同时报 NAVSIM 与 Bench2Drive）。两篇都走 `raw` 逐文件取证（**未克隆**）。

### O.1 LCS（DP-A26）——"单次前向"是真的，但"省算力"没有代码证据

- **确实少跑一次模型调用**：标准 CFG 路径 `agent_lcs.py:941` 跑 cond、`:962` 跑 uncond、`:969` `pred_route = pred_route_uncond + cfg_scale*(cond − uncond)`；**LCS 默认路径 `:929-931` 只调用一次**（注释原文 "Standard forward pass with conditional prompt - LCS is applied inside model"）。**关键确认：全仓无 `torch.cat([cond, uncond])` 式的 CFG 批拼接**（`driving.py` 里三处 `torch.cat` 分别是 token 拼接、跨样本累积、loss 拼接）→ **省掉的确实是第二次前向**，代之以**离线预计算的隐空间方向向量**（`driving.py:194-198` `driving_features + lmsi_scale * shift`；`mean_shift_scale = 0.1`；`data/mean_shift_deltas_cfg03.pt` **在仓库内，1.4 MB**，键为 6 个导航命令各自的质心 − 全局质心）。
- **但代码里没有任何 FPS / FLOPs / latency 数字**（全仓 grep 只命中 `agent_lcs.py:1104-1106` 一处 `print("[TIMING] ...")`，**只打印、不落盘、也不对比单/双前向**）→ **"省一半算力"只有机制推论，无代码证据**。
- **四处陷阱**：① `use_cfg_latent`（`config_lcs.py:11`）**全仓只此一处出现、从未被读取**（声明未接线）；② `use_mean_shift_cfg` 的环境变量**只能置 True、无法关**（要关得改源码）；③ **`mean_shift_deltas_path` 是相对路径**，而评测脚本从不 `cd` 到仓库根 → **cwd 不对时只打印 `Prior file not found, steering disabled` + 一个 WARNING，评测照常跑完** → **引导被静默关闭、分数照出**（最隐蔽的一条）；④ `cfg_scale = 3.0` 在 LCS 模式下是**死参数**。
- 附带查明：**`dropout03` = 训练期命令丢弃概率 0.30**（`train_lcs.yaml:41-42` + `dataset_driving.py:235-240`）；生成质心文件的 `extract_mean_shift_centers.py` **不在仓库内** → 质心如何统计不可核验。

### O.2 BridgeDrive（DP-A08）——桥是真的，但步数与锚点路径都硬编码

- **桥核与论文一致**：`model_diffusion_head_ddbm_v5.py:204-223` 注释原文 `# 1. add truncated noise to the plan anchor`，`x_T = plan_anchor`、`x_0 = targets["trajectory"]`；`get_abc:38-49` 是 **DDBM 的 VP-SDE 桥核**（`a_t = exp(logsnr_T − logsnr_t + logs_t − logs_T)` 等），合成 `samples = a_t·xT + b_t·x0 + c_t·noise`。→ **但代码里没有任何 "Doob" / "h-transform" 字样**，也没有独立 SDE 求解器。
- **论文的"PF-ODE / 一阶 DDIM 足够"在代码里没有对应命名**：`sample_step`（`:59-76`）里是**一个未命名的确定性一阶更新式**（只在首步 t=T 注入噪声）。**全仓无 `PF-ODE` / `Euler` / `Heun` 字面量**。
- **三处硬编码/失效**：① **NAVSIM 侧 `step_num = 20` 是硬编码**（`:272-273`，**任何 yaml/sh 都改不了**；LEAD 侧是配置项但脚本覆盖值与默认值相同，等于没覆盖）；② **锚点 yaml 指向作者机器绝对路径**（`bridgedrive_agent_k80_beta10.yaml:17` = `/data/workspace/shuliu/...`），类默认又指向**不存在**的 `kmeans_navsim_traj_20.npy`，而**仓库内实际提供的是 `kmeans_navsim/navsim_anchor_k80.npy`（10368 B）** → 需手改；③ **`ddbm_training`**（`config_training.py:262 = True`）被 `planning_decoder_bridgedrive.py:182/196` 依 `'route' in data` **强制改写**；④ `beta_d` **三套值**（类默认 2.0 / `DDBMScheduler` 里 19.9 死默认 / yaml 1.0）。
- **无任何引导/约束项**（全仓 `cbf|guidance|reinforce|penalty` 只命中 README 叙述文字）→ 与论文"约束只来自锚点先验"一致。
- **两个数字本仓都不可闭环复现**：**Bench2Drive 87.99/74.99** 需外部 Bench2Drive 指标模块（本仓只 vendor 了 `leaderboard_evaluator_v2.py`，依赖 `3rd_party/Bench2Drive/scenario_runner` 等外部目录）；**NAVSIM 88.0** 的权重不在仓内（`run_main_testing_...sh:11` 是占位符 `CKPT=/change/to/your/ckpt/path`）。**"补丁式发布"**：README 要求先 clone DiffusionDrive / LEAD 再覆盖文件；仓内还残留 `model_diffusion_head_ddbm{,_v8,_v8v5}.cpython-310.pyc` —— **v8/v8v5 的 `.py` 源文件不在仓库里**。

### O.3 两条判断

① **LCS 的 single-pass CFG 是目前看到的"省算力"里最干净的实现**（真的少一次前向），但**没有算力实测** → 若本项目要做"引导的成本"这条线，LCS 可作对照实现，**延迟必须自己测**；② **BridgeDrive 是"理论叙述 > 代码实现"的又一例**（桥核真、但 PF-ODE 无对应命名、步数与锚点硬编码、两个基准数字都不可闭环复现）→ **引用其 88.0 / 87.99 时必须加限定**。

**产出**：[C003 §O](../../code/traces/diffusion_planner_code_traces-2.md) 新增一节（O.1 LCS / O.2 BridgeDrive / O.3 两条判断），文件头同步；[papers/diffusion_planner_ad.md](../../topics/diffusion-planner/papers/diffusion_planner_ad.md) 的 **DP-A26 与 DP-A08 两行**补代码级结论；[state.md](../../state.md) 待续第 13 项更新（6 个新仓库已核 4 个）；[repositories.md §F](../../code/repositories.md) / [README.md](../../../../README.md) 同步。**未克隆任何仓库**。

## P. MPDiffuser（DP-A23）与 DIPOLE（DP-A17）——6 个新仓库全部核完（第二十四轮）

MPDiffuser（DP-A23）与 DIPOLE（DP-A17）的代码级核验——6 个新仓库全部核完

**动因**：§20 新发现的 6 个仓库已核 4 个（§21–§23）。本轮补最后两个，**把"研究对象侧代码可用性"这条线彻底结账**。两篇都走 `raw` 逐文件取证（**未克隆**）。

### P.1 MPDiffuser（DP-A23）——"非梯度可行性注入"是真的，但仓库是 JAX 且两个入口是坏的

- **动力学模型是"学出来的扩散转移模型"**（不是解析式、也不是环境真值）：`mpdiffuser/model/dyn_model.py:8-30`，条件 `(x_t, t, x0, u, conds)`，目标是预测噪声；**训练入口在仓库内**（`scripts/train.py model=dynamics`）。
- **"参与去噪"发生在每一个去噪步，方式是替换状态子块**：`mpdiffuser/policy/mpdiffuser.py:65-73` —— 动力学预测噪声 → 用**动力学自己的扩散后验** `p_mean_variance` 推进一步 → **替换状态块（动作块不变）** → 规划器再做自己的后验去噪；且 `:75` 的 **`use_pmean_var=False` 是硬编码**（`diff_utils.py:135` 默认是 True）→ 这是机制成立的前提。动力学那一步**也走 CFG**。
- **"非梯度"成立，但理由要写清**：全程只有 `apply`（前向），**没有显式 `no_grad`/`detach`**（JAX，压根没构造计算图）；全仓 `jax.grad` 只有两处，**都不在 MPDiffuser 路径上**。
- **三处硬问题**：① **`Planner` 类自身是坏的**——`model/planner.py:125` 的**嵌套** `sample_step` 在 `:127/:129` 调用 **`self.sample_step`，而该类里没有这个方法**（全文件只有 `:125` 一处 `def sample_step`）→ **`--method planner` 必 `AttributeError`**；② **`GuidedSampler`（`diff_utils.py:183`）只有 `__init__` 与 `__call__`**，而 `diffuser_policy.py:58` 取 `sampler.sample_step` → **`--method guided` 也坏**；③ `sample_cond` 是死代码。**好消息：论文方法主路径不受影响。**
- **权重与数据都不可得**：树清单**无任何 `.pt/.ckpt`**；README `:157` "coming soon" **仍成立**、`:3` Project Page 仍是 `TODO`；**无数据下载入口**；**README 无结果表**。

### P.2 DIPOLE（DP-A17）——不是策略梯度，是 IQL + 有界优势加权 flow 回归

- 主仓 `LRMbbj/DIPOLE` 确为**占位**；实现在 **git submodule** → `Whiterrrrr/dipole-rl`（**默认分支是 `master`**）。
- **RL 形态**：**无 `log_prob`、无重要性比率、无比率裁剪、无 KL**；**有 critic 与 value**；优势是 **IQL 型逐样本 `q − v`**（`dipole.py:122`）；总损失 `v_loss + c_loss + pos_loss + neg_loss`。→ **IQL + 优势加权 flow-matching 回归（RWR 型）+ 正/负对偶 actor + CFG 推理**。
- **与 DIVER 的"名实不符"不同**：DIPOLE **从不自称 GRPO**（它声称"KL 正则 RL 的 greedified 重构"）→ **自称与代码自洽**。→ "RL 词义核验"清单补一条注记。
- **"稳定训练"的机制可核**（论文关键主张）：核心是**有界 sigmoid 权重** `sigmoid(beta·value + k)`（`dipole.py:14-19`）替代 IQL 的 `exp(α·adv)`——**权重恒在 (0,1)，指数项才是 loss explosion 的源头**；配套 **Q 集成取 min（悲观）**、**Polyak 目标网 `tau=0.005`**、**IQL expectile 值**。
- **奖励全部来自离线数据集**（`:64`），**无奖励模型**。
- **三处接线缺陷**：① **`q_agg` 半接线**（`value_loss` 遵守 `:39`，但 **actor 加权处硬编码 `min`** `:121`，而 README 要求两个域用 `mean`）；② **`seed`（`get_config():331`）声明后从未被读取**；③ **`encoder` 是未回填的 `placeholder(str)`**（`:332`），而 `create():250` 直接访问它。
- **可跑性最干净的一篇**（无未定义变量、无硬编码本机路径、无 pdb 残留），代价是依赖栈老（`mujoco-py` + `d4rl==1.1` + `gym==0.23.1`）且**不含权重与数据**。
- **一处缺口**：主 README `:74-88` 有 **NavSim 结果表（`DP-VLA w/ DIPOLE navtest` EPDMS 94.8）**，但 submodule **只含 ExORL 与 OGBench，没有任何 NavSim/驾驶代码** → **该表对应配置在发布物中不存在**。

### P.3 三条判断

① **MPDiffuser 是"生成过程内注入可行性"的第四条实现路线**（前三条：PC-Diffuser 逐去噪步 CBF-QP、FeaXDrive SDF 软引导、GuideFlow 常数速度偏置）→ **只能作机制参考，不能作可复现基线**；② **DIPOLE 给"RL 稳定训练扩散策略"提供了一个可核的具体机制**，且**自称与代码自洽**；③ **两个仓库都不适合直接跑**（一个坏入口 + 无资产，一个老依赖 + 无驾驶代码）→ **静态核验的边际收益已接近零**。

**产出**：[C003 §P](../../code/traces/diffusion_planner_code_traces-2.md) 新增一节（P.1 / P.2 / P.3），文件头与"6 个全部已核"的注记同步；[papers/diffusion_planner_ad.md](../../topics/diffusion-planner/papers/diffusion_planner_ad.md) 的 **DP-A23 与 DP-A17 两行**补代码级结论；[state.md](../../state.md) **待续第 13 项标记为可关闭**；[repositories.md §F](../../code/repositories.md) / [README.md](../../../../README.md) / [inbox/cleanup.md](../../../../inbox/cleanup.md) 同步。**未克隆任何仓库**。→ **研究对象侧"代码可用性 + 代码级核验"这条线至此全部结账：34 篇论文表 + 18 个有代码的仓库（13 已克隆逐文件 + 5 走 raw）。**
