# 扩散规划器代码脉络（主张 → 代码）

更新时间：2026-09-23  
证据等级：**代码静态检查**（已克隆仓库，读文件与配置，**未安装依赖、未运行**）。仓库清单与 commit 见 [repositories.md](../repositories.md)。  
**核验级别（定义见 [ai/rules.md §代码静态检查](../../../../ai/rules.md)）**：**§A–§H 覆盖的 13 个仓库中 12 个为 L1 逐文件核验**（已克隆、逐项对齐 `文件:行号`）；**DriveFine（DP-A29）为 L2**（仓库存在但零代码，只有 `README.md`）。**第二册 §I–§P 的 6 个新仓库为 L3**（`raw` 逐文件取证、**未克隆**，见 [diffusion_planner_code_traces-2.md](diffusion_planner_code_traces-2.md)）。  
读法：本文件回答研究脉络三关系中的两条——**组合关系**（模块来自哪篇论文）与**主张—代码关系**（论文卖点对应哪些文件）。继承关系见 [diffusion_planner_lineage.md](../../topics/diffusion-planner/lineage.md)。  
本文件规模：主张—代码对照 **12 项**、组合关系 **7 项**、实现细节 **13 项**、待核验 5 项（§D3 已解一半）、判断 4 条，另有 **§F 同基准可比性核验**（四个 NAVSIM 扩散规划器的主干/输入/视野逐项对照）、**§G DIVER**（扩散接在 SparseDrive 上、噪声起点是锚点、"GRPO" 实为奖励加权损失）、**§H 三个"非锚点"规划器**（FeaXDrive 的可行性与真 GRPO、WAM-Flow 的文本数字 token、FlowDrive 的采样中段调制与规则 PDM 选优）、**§I PC-Diffuser**（逐去噪步 CBF-QP 的求解器、决策变量、slack 与 QP 次数）、**§J Hyper-Diffusion-Planner**（跨两生态的"无锚点纯扩散"、损失空间受控对照、"数据规模"不可复现、HDP-RL 实为优势加权回归）与 **§K DriveFine**（仓库零代码，研究对象侧 13 个仓库至此全部结账：12 逐文件 + 1 零代码）、**§L Flow Planner**（无锚点无词表无选优的纯流匹配）、**§M ReCogDrive**（**全表核验代码可用性后新发现的仓库**；其 "DiffGRPO" 是**第六种"RL"**：有真 log-prob 与组内归一化优势、**无 ratio / 无比率裁剪 / 无 KL / 无 critic**）、**§N GuideFlow**（**同基准 navhard SOTA**；论文三条机制里 **CVF 只在 v8、RFE 只在 v10，而评测路径 import 的是 v6** → **默认评测路径既无 CVF 也无 RFE，且 v6 有未定义的 `k_num`**；`flow_matching.py` 是 11 字节占位）、**§O LCS + BridgeDrive**（LCS 的"single-pass CFG"**真的少一次前向**但**无算力实测**；BridgeDrive 的桥核是真的但**步数与锚点路径硬编码、Bench2Drive 数字本仓不可复现**）、**§P MPDiffuser + DIPOLE**（MPDiffuser 的"非梯度可行性注入"是真的但是 **JAX 仓库、三个入口两个坏、无权重无数据**；DIPOLE 的 RL 是 **IQL + 有界优势加权 flow 回归（RWR）**、**自称与代码自洽**）。**注（第二十四轮）**：研究对象侧"代码可用性"已**全表 34/34 核完**（18 有代码 / 1 占位 / 1 只有项目页 / 14 未找到），**其中 6 个此前记为"未见官方"的仓库其实有代码，且 6 个全部已做代码级核验**（走 `raw` 逐文件取证，**未克隆**），见 [repositories.md §F](../repositories.md)。世界模型侧见 [world_model_code_traces.md](world_model_code_traces.md)，E2E 主干侧见 [e2e_trunk_code_traces.md](e2e_trunk_code_traces.md)，NAVSIM 指标口径见 [benchmarks.md](../../direction/benchmarks.md) §2。


## A. 主张—代码对照（逐个核验）

| 论文 | 论文主张 | 代码证据（文件 / 类 / 配置） | 一致性判断 |
|---|---|---|---|
| **DiffusionDrive**（DP-A02） | 截断扩散 + 多模态锚点先验 + 级联扩散解码器，2 步去噪 | `navsim/agents/diffusiondrive/transfuser_model_v2.py`：`from diffusers.schedulers import DDIMScheduler`、`ConditionalUnet1D`、`self.diffusion_scheduler = DDIMScheduler(...)`；`transfuser_config.py`：`plan_anchor_path = ".../kmeans_navsim_traj_20.npy"`；`modules/multimodal_loss.py: LossComputer` | **一致**：锚点先验是 K-means 得到的 **20 条锚点轨迹**（文件 `kmeans_navsim_traj_20.npy`）；采样器用 diffusers 的 DDIM |
| **DiffusionDriveV2**（DP-A03） | 两阶段（RL 约束 + mode selector）；乘性噪声探索；锚内/锚间 GRPO | 文件级：`diffusiondrivev2_rl_agent.py`、`diffusiondrivev2_model_rl.py`、`diffusiondrivev2_rl_config.py`、`diffusiondrivev2_model_sel.py` | **一致**：两阶段与 selector 均有独立文件；配置 `plan_anchor_path = kmeans_navsim_traj_20.npy`、`TrajectorySampling(time_horizon=4, interval_length=0.5)`（4s @2Hz） |
| **DiffusionDriveV2**（附加发现） | 论文只强调 20 个锚点的高斯混合 | 仓库另有 `gtrs_traj/16384.npy`，shape **(16384, 40, 3)**（x,y,heading） | **论文未展开**：仓库同时带一套 **16384 条轨迹词表**（与 Hydra-MDP 的 4096/8192 词表同源），用途需进一步读代码确认 |
| **MeanFuser**（DP-A14） | MeanFlow 一步采样 + 高斯混合噪声（GMN, K=8）+ 自适应重建（ARM） | `navsim/agents/meanfuser/meanfuser_model.py`：`class MeanFlowHead`、`meanflow_loss = F.l1_loss(v_pred, v_hat)`；`meanfuser_config.py`：`num_sample_steps: int = 1`、`num_proposals: int = 8`、`meanflow_loss_weight: float = 7.0`；`arm_model.py`；`tools/gaussian_mixed_noise/get_GMN_anchors.py` | **完全一致**：一步采样、K=8 提案、ARM、GMN 生成脚本都在代码里 |
| **PC-Diffuser**（DP-A21） | 逐去噪步 CBF-QP、路径一致、速度级约束 | 主仓 `PC-Diffuser` 是**子模块壳**；子模块 `diffusion-planner-cbf`（= Eugene29/Diffusion_Planner，分支 `public`）内含：`diffusion_planner/safety/pc_diffuser/lqr_tracker_cbf_modular.py`、`lqr_tracker.py`、`safety/mpc_cbf/mpc.py`、`distance_functions.py`、`vehicle_params.py`、`safety/safe_diffuser/safe_diffuser.py` | **一致**：CBF/MPC 与车辆参数是独立模块，且仓库内**同时保留 `safe_diffuser` 基线**（对应论文的对比）。**逐项核验见 §I**（三个方法、两套 QP：PC-Diffuser 用 CasADi qpOASES 加速度级 QP，SafeDiffuser 基线用 cvxpy+OSQP 位置级 QP） |
| **PC-Diffuser**（组合关系） | 基座为 Diffusion Planner | 子模块 URL = `Eugene29/Diffusion_Planner.git`；另有 `Eugene29/nuplan-devkit` 子模块 | **一致**：确实是 fork 自 Diffusion Planner + vendored nuPlan devkit |
| **GoalFlow**（DP-A09） | Rectified flow，K=100 步，goal point 两级评分 | `navsim/agents/goalflow/`：`goalflow_model_traj.py`（`def denoise(self, ego_trajectory, sigma, ...)`，sigma 编码 + `sigma / infer_steps`）、`goalflow_config.py`：`infer_steps: int = 100`、`goalflow_loss.py`（含 `train goalpoint construction`）、`diffusion_es.py`、`goalflow_agent_navi.py` / `goalflow_model_navi.py`（导航分支） | **一致**：sigma 条件化的 flow 去噪器 + 100 步 + 独立的 goal 构造损失 |
| **Hyper-Diffusion-Planner**（DP-A06 / HDP） | 扩散损失空间、轨迹表示、数据规模的系统研究 + RL 后训练 | 仓库顶层同时含 **`HDP-navsim/`** 与 **`HDP-nuplan/`** 两套完整实现（各带 `setup.py`、脚本、配置） | **一致且更强**：同一篇论文提供两个生态的实现，**跨生态在代码层已打通**。**逐项核验见 §J**（前两条主张有代码落点；**"数据规模"无对应开关、不可复现**；"RL 后训练"实为**优势加权回归**而非 GRPO） |
| **FlowDrive**（DP-A10） | nuPlan 流匹配 + 数据重平衡 | 仓库基于 `nuplan-devkit`，README 提及 PLUTO | 组合关系一致；**逐文件核验见 §H.3** |
| **DriveFine**（DP-A29） | 掩码扩散 VLA + 精修专家 | README 明写 "developed based of" → **ReCogDrive + LaViDa**；但**仓库零代码**（见[第二册 §K](diffusion_planner_code_traces-2.md)） | **组合关系无法核验**：只有 README 可读 |
| **DiffusionVeteran**（DP-S14，ICLR'25 Spotlight） | 实证研究："无引导采样 + 选择可优于引导采样"、"Transformer 优于 U-Net"；训练并评估 6000+ 个扩散模型 | `pipelines/veteran_d4rl_{maze2d,antmaze,kitchen,mujoco}.py`：`guidance_type` 三选一 **MCSS / cfg / cg**；`planner_net` 二选一 **transformer / unet**；`configs/veteran/**/*.yaml` 为完整的消融网格 | **一致且更具体**：三条引导路线**在同一份代码里并列实现**（见下方 C 节） |
| **Diffusion Planner**（DP-A01） | 训练无关的 classifier guidance，能量函数含**目标车速 / 舒适 / 避碰 / 可行驶区域**四项（Eq.8、§4.3） | `model/guidance/guidance_wrapper.py`：**`self._guidance_fns = [collision_guidance_fn]`——只有避碰一项**；`model/guidance/` 目录下只有 `collision.py`（+ 一篇 `documentation_guidance.md` 教用户自己加） | **需更正**：已发布代码里**只有避碰引导**；目标车速/舒适/可行驶区域**未发布**。该框架设计为插件式，作者只给了 1/4 |

## B. 组合关系（模块来自哪里）

| 模块 | 来源 | 证据 |
|---|---|---|
| 锚点词表（20 条） | K-means 聚类 NAVSIM 轨迹 | `kmeans_navsim_traj_20.npy`（V1/V2 共用同一文件） |
| 大词表（16384 条） | 与 Hydra-MDP 同源的轨迹词表思路 | `gtrs_traj/16384.npy`（V2 仓库内） |
| 扩散采样器 | HuggingFace `diffusers` 的 `DDIMScheduler` | DiffusionDrive `transfuser_model_v2.py` |
| 感知主干 | TransFuser（resnet34 图像 + LiDAR） | DiffusionDrive/V2/GoalFlow 均为 transfuser 系目录结构 |
| 安全模块 | 自研 `pc_diffuser` + `mpc_cbf`，并 vendored nuplan-devkit | PC-Diffuser 子模块 |
| 车辆几何参数 | 独立 `vehicle_params.py` | PC-Diffuser 子模块 |
| 扩散与引导算法库 | **CleanDiffuser**（模块化扩散决策库） | DiffusionVeteran 顶层即 `cleandiffuser/`；README 致谢段称 "officially supported by CleanDiffuser" |

## C. 关键实现细节（本轮静态核验已解决）

| 问题 | 结论 | 证据 |
|---|---|---|
| DiffusionDrive 的"2 步去噪"如何实现 | **`forward_test` 中 `step_num = 2`**；`step_ratio = 20 / step_num`；关键在截断——**噪声加在 `t=8`（总 1000 步）**：`trunc_timesteps = torch.ones(...) * 8`，再 `scheduler.add_noise(..., timesteps=trunc_timesteps)`。即反过程从"锚点 + 极低噪声"起步，而不是从纯噪声起步 | `transfuser_model_v2.py:forward_test`（`step_num = 2`、`trunc_timesteps = ... * 8`、`add_noise`） |
| V2 的 16384 词表用途 | 模型输出含 **`reward` 与 `sub_rewards`**（`predictions['reward']`、`predictions.get('sub_rewards')`），说明 16384 轨迹词表用于**奖励/子分数计算**（与 Hydra-MDP 的多目标子分数同源），不是扩散采样的先验 | `diffusiondrivev2_rl_agent.py`（reward / sub_rewards 字段） |
| V2 的 GRPO 如何实现 | 反链中逐步记录 **`log_prob`**（`log_prob.sum(dim=(-2,-1))`），并堆叠成 **`all_log_probs = torch.stack(..., dim=-1)`，形状注释为 `[B, G*N, step_num]`**——即"每个锚点 × 每个采样"的分组对数概率，与论文的**锚内（Intra-Anchor）/锚间（Inter-Anchor）GRPO** 分组一致 | `diffusiondrivev2_model_rl.py`（`log_prob`、`all_log_probs`、`roll_timesteps`） |
| PC-Diffuser 的 QP 是闭式还是调库 | 该文件**未调用 cvxpy/qpsolvers**，而是自带 `_build_qp_solver()`；屏障函数为**线性间距** `h = D − (r_e + r_n)`，并带类-K 项 `alpha * h_k1_nom`（`cbf_alpha` 默认 0.7，另一处 0.3）——与论文"速度级 CBF、闭式平均 1.14 ms"的描述一致 | `safety/pc_diffuser/lqr_tracker_cbf_modular.py`（`_build_qp_solver`、`_compute_barrier`、`cbf_alpha`） |
| MeanFuser 的 ARM 是否与论文一致 | 存在独立模块 **`class ARMModel(nn.Module)`**，含 `get_arm_loss(predictions, targets)` 与 `forward(outputs_dict, encoder_outputs)`——与论文"自适应重建模块（注意力选/重建）"一致 | `navsim/agents/meanfuser/arm_model.py` |
| **三条引导路线在代码里到底怎么分工**（DiffusionVeteran，直接回答"CFG vs Q 引导"之争） | 同一 planner、三种推理路径：<br>① **MCSS**：**无引导**采样 `num_envs × 50` 条（`condition_cfg=None, w_cfg=1.0`），再用 **horizon critic 的 `argmax`** 选一条 → "无引导采样 + 值函数选优"<br>② **cfg**：按目标回报做 **classifier-free guidance** 采样 `num_envs` 条（`condition_cfg=condition, w_cfg=planner_w_cfg`），**不重采样**<br>③ **cg**：带 **classifier guidance** 采样 `num_envs × 50` 条，再用 **`log["log_p"]` 的 `argmax`**（分类器累计回报对数概率）选一条 | `pipelines/veteran_d4rl_maze2d.py:357-408`；critic 为 `DVHorizonCritic`（112-120）、分类器为 `CumRewClassifier`（130-138） |
| DiffusionVeteran 的消融维度有哪些 | 配置即消融网格：`guidance_type`（MCSS/cfg/cg）、`planner_net`（transformer/unet）、`pipeline_type`（separate/joint，状态与动作是否分离）、`rebase_policy`（是否把 next_obs 平移到当前坐标系）、`use_diffusion_invdyn`（动作由扩散逆动力学还是普通逆动力学出）、`planner_solver`（ddim）、`planner_sampling_steps`（20）、`policy_diffusion_steps`（10）、`planner_num_candidates`（50） | `configs/veteran/maze2d/maze2d.yaml` |
| **V2 的 16384 轨迹词表到底做什么用**（原 §D 待核验项，已解决） | 它是**一张预计算的 PDM 子分数查找表**，并被当作**扩大后的候选池**送进选优器：<br>① `self.vocab_pdm_gt_path = 'gtrs_traj/navtrain_16384.pkl'`（每个 token 对应每个词表轨迹的 PDM 子分数）、`self.vocab_path = 'gtrs_traj/16384.npy'`（轨迹本体）；<br>② `get_vocab_pdm_subscores` 用与 NAVSIM 相同的权重拼出词表级 PDM 分：`no_collision × drivable_area × (5·ttc + 5·progress + 2·comfort)`；<br>③ 按 `dropout_ratio` 随机保留一部分词表（训练 0.5、推理 **0.99** → 只留约 1%）；<br>④ **把词表轨迹本体拼到候选集后面**：`diffusion_output = torch.cat((diffusion_output, vocab), dim=1)`，随后由 coarse scorer → **top-32** → fine scorer 统一选优 | `diffusiondrivev2_model_sel.py:929-932`、`1202-1266`、`1346-1380` |
| **DP-A01 的引导只在扩散的哪一段生效** | **只在末段**。`collision_guidance_fn` 里 `mask_diffusion_time = (t < 0.1 and t > 0.005)`，随后 `x = torch.where(mask_diffusion_time, x, x.detach())`——**t 不在 (0.005, 0.1) 时梯度被切断**，即引导只作用于 VP-SDE 时间轴的最后约 10% | `model/guidance/collision.py:70-71` |
| **DP-A01 的引导强度** | **硬编码**，不在配置里：`collision.py` 末尾 `return 3.0 * reward`；同时 `decoder.py` 传 `guidance_scale=0.5` → 有效强度 **1.5** | `collision.py:126`、`decoder.py:136` |
| **DP-A01 的噪声起点与硬约束** | 起点 = **当前状态 + 未来帧 `torch.randn(...) * 0.5`**（噪声尺度 0.5，非标准 1.0）；并把 `initial_state_constraint` 作为 `correcting_xt_fn` 传入采样器——**每一步都把第 0 帧强制重置为当前状态** | `decoder.py:105-110, 120-122` |
| **DP-A01 的去噪步数**（原笔记待核验项，已解决） | **默认 10 步**：`dpm_sampler(..., diffusion_steps=10, ...)`，采样器为 DPM-Solver++、`order=2`、`skip_type="logSNR"`、`method="multistep"`、`denoise_to_zero=True`；代码注释写 "Steps in [10, 20] can generate quite good samples. And steps = 20 can almost converge." | `model/diffusion_utils/sampling.py:10, 32-43` |
| **DP-A01 的避碰能量怎么算** | 用**有向矩形距离**（对两个矩形的 4 条法向做投影，即 SAT 思路）`batch_signed_distance_rect`；障碍物**膨胀 `INFLATION = 1.0` m**、`CLIP_DISTANCE = 1.0`；距离按 >1 与 ≤1 分两组各取均值后相加再 `.exp()`；梯度经 **21 点高斯核 `exp(-linspace(-2,2,21)²/4)` 的 conv1d 做时间维平滑**；自车几何硬编码 `COG_TO_REAR = 1.67` + nuPlan `get_pacifica_parameters()` | `model/guidance/collision.py:13-14, 60-126` |
| **README 表里的 "refine" 指什么**（原笔记待核验项，已澄清） | **是 nuPlan 闭环评测的口径，不是本仓库的功能**。README 表把对手标为 "w/o refine."、自己标为 "w/ refine (ours)"；仓库内 `data_augmentation.py` 的 `refine_horizon` / `num_refine` 是**数据增强用的五次样条插值**（`quintic spline interpolation`），与评测口径无关——两者**不可混为一谈** | `README.md:56-79`、`utils/data_augmentation.py:68-69, 240-252` |

## D. 仍然待核验（需要运行环境或更多阅读）

1. `roll_timesteps` 与 `trunc_timesteps=8` 的**数值配合关系**（前者由 `step_ratio=10` 推出 `[10, 0]`，与噪声起点 8 不完全对齐），需要实际跑一次才能确认采样是否按预期执行。
2. V2 的选优器**最终选出的轨迹有多少来自词表、多少来自扩散采样**——代码已确认两者被拼进同一个候选池（见 §C），但**各自的胜出比例未报告**，需要运行才能统计。这直接决定"V2 的 91.2 分有多少是扩散生成器的贡献"。
3. ~~PC-Diffuser 的 QP **求解器实现细节**（`_build_qp_solver` 内部）与论文的 1.14 ms 是否可复现。~~ → **已解决一半（见 §I）**：求解器已确定为 **CasADi `qpsol('qp','qpoases')`**（不是 cvxpy），QP 结构、决策变量、slack 与回退路径都已核清；**剩下的只有"1.14 ms 单次 QP 是否可复现"这一条数值验证**，需要运行（仓库有细粒度计时但汇总打印被注释）。
4. DiffusionVeteran 的**结论表**（6000+ 模型的实证排序）**未在本次核验范围内**——本次只确认"三条引导路线都有可运行实现"，**不确认**"无引导 + 选择确实优于引导"这一结论。
5. 所有论文的**指标数字**都必须实际运行才能验证——静态检查只能确认"代码里有对应实现"，不能确认"实现了论文声称的效果"。

## E. 由本轮代码核验得出的四条判断

1. **"CFG vs Q 引导"不是二选一，而是三个并列的可实现选项**。DiffusionVeteran 的代码把三者放在同一 planner 上：`MCSS`（无引导采样 + critic 选优）、`cfg`（条件引导）、`cg`（分类器引导 + 按分类器分数选优）。研究对象的 transfer.md 第 1 节里那条"CFG 优于 Q 引导（DP-E02 附录 K）与 DiffusionDriveV2/DIVER 的 RL 引导做法相反"的**矛盾**，因此有了一个可执行的对齐口径：**把"引导"与"选优"拆开**——DP-E02 批评的是"用离线 Q 做引导"，而 MCSS 用的是"无引导 + 用 critic 选优"，两者不是同一件事。
2. **研究对象已有的消融维度可以在同一份配置网格上对齐**。DiffusionVeteran 的 `configs/veteran/**/*.yaml` 给出了 9 个维度的默认值（引导方式、网络结构、状态-动作是否分离、坐标系重定基、动作生成方式、采样器、采样步数等），这些维度与驾驶侧扩散规划器**大部分同构**，可直接作为实验设计的起点（对应 [preparation.md](../../ideas/preparation.md) 的实验协议）。
3. **V2 的"扩散规划器"标签需要打折**：16384 条词表轨迹**与**扩散采样结果被拼进同一个候选池，再由 scorer 选优（coarse → top-32 → fine）。也就是说 **V2 的最终输出可以是一条词表轨迹而非扩散样本**。这既解释了它为何能到 91.2，也说明**它的分数不能当作"扩散生成机制本身"的能力证明**——引用时必须区分"生成器贡献"与"选优器贡献"。
4. **DP-A01 的"引导"在代码里只剩 1/4，且是个插件骨架**。论文写能量函数含**目标车速 / 舒适 / 避碰 / 可行驶区域**四项，而 `model/guidance/` 下**只有 `collision.py`**，`_guidance_fns` 里也只挂了一个；同目录的 `documentation_guidance.md` 是"教你自己加引导函数"的教程。→ 这说明 **DP-A01 的引导框架是设计成可扩展的，但作者自己只交付了避碰一项**。引用"DP-A01 用引导替代规则后处理"时必须限定为"**避碰引导**"，否则是把未发布的实现当成已验证结论。

## F. 同基准可比性的代码级核验（四个 NAVSIM 扩散规划器的主干/输入/视野）

**动因**：本工作空间反复把"backbone 与输入权限不同 → 不可横比"作为障碍，但从没有给出**具体的差异清单**。本节用四个仓库自己的配置文件把它列出来。

| 项 | DiffusionDrive（DP-A02） | DiffusionDriveV2（DP-A03） | MeanFuser（DP-A14） | GoalFlow（DP-A09） |
|---|---|---|---|---|
| 配置类 | `transfuser_config.TransfuserConfig` | `diffusiondrivev2_sel_config.TransfuserConfig` | **`meanfuser_config.MeanfuserConfig`（自有）** | `goalflow_config.GoalFlowConfig`（**TransfuserConfig 的逐字段克隆**） |
| 配置文件同源性 | 基准 | **与 DD 的 `transfuser_config.py` 逐字节完全相同**（`diff` 无输出） | 其 `navsim/agents/transfuser/transfuser_config.py` 是 **vendored 的 TransFuser 基线，不被 MeanfuserAgent 使用** | 无独立 `transfuser_config.py`；**主干字段与 navsim 的 `transfuser_config.py` 逐字段相同**（差异仅为 GoalFlow 新增的流匹配字段） |
| **`tf_d_model`** | **256** | 256 | **128** | **512**（agent yaml 覆盖） |
| `tf_num_layers` / `tf_num_head` | 3 / 8 | 3 / 8 | `decoder_layers=1` / `decoder_nhead=8` | 3 / 8 |
| 图像 / LiDAR 主干 | resnet34 / resnet34 | 同 | resnet34 / resnet34 | resnet34 / resnet34（另有 `v99_pretrained_path` 选项） |
| LiDAR 几何 | ±32 m，256×256 | 同 | 同 | 同 |
| **`lidar_seq_len`** | **1** | 1 | **4**（agent yaml 覆盖） | 1 |
| **训练轨迹视野** | 4 s / 0.5 s → **8 点** | 同 | 同 | **5.5 s / 0.5 s → 11 点**（`trajectory_generation_len=11`） |
| **实际输出点数** | 8 点（4.0 s） | 同 | 同 | **8 点（4.0 s）**：`pred_trajs[:,:,1:1+8,:].mean(1)`，11 点被**模型侧切前 8 点** |
| 锚点 / 词表字段 | `plan_anchor_path`（20 条 K-means） | 同 + `gtrs_traj/16384.npy` | **无任何锚点字段**；改为 `noise_type='multi_gaussian'` + `navtrain_8_mean_std.pkl` | `voc_path: ''`（未启用） |
| 规划损失项 | `trajectory_weight 12.0` + `trajectory_cls_weight 10.0` + `trajectory_reg_weight 8.0` + `diff_loss_weight 20.0` | 同 | `trajectory_weight 10.0`（**仅一项**） | 见 `goalflow_loss.py`（本次未展开） |
| **评测视野**（scorer/simulator） | 40 poses @ 0.1 s = **4.0 s** | 同 | 同 | **同（也是 4.0 s）** |

**证据位置**：`DiffusionDrive|DiffusionDriveV2/navsim/agents/diffusiondrive{v2}/transfuser_config.py`、`MeanFuser/navsim/agents/meanfuser/meanfuser_config.py`、`GoalFlow/navsim/agents/goalflow/goalflow_config.py`、各仓 `navsim/planning/script/config/common/agent/*.yaml`、`navsim/planning/script/config/pdm_scoring/default_scoring_parameters.yaml`、`navsim/planning/simulation/planner/pdm_planner/simulation/pdm_simulator.py`。

**五条由本节得出的结论**：

1. **DD 与 V2 是真正对齐的一对**。两个仓库的 `transfuser_config.py` **逐字节相同**，agent yaml 也都只覆盖 `trajectory_sampling`（4 s / 0.5 s）与 `latent: False`。→ **V2 的 91.2 vs DD 的 88.1 可以直接归因于"RL 后训练 + mode selector"**，不必担心主干差异。这是本工作空间**第一条"可横比"的代码级结论**，也是全表里唯一一对。
2. **MeanFuser 与 GoalFlow 都与 DD 不齐，且差异是量化的**。MeanFuser 的 `tf_d_model` 是 DD 的 **1/2**（128 vs 256）、`lidar_seq_len` 是 DD 的 **4 倍**（4 vs 1）；GoalFlow 的 `tf_d_model` 是 DD 的 **2 倍**（512 vs 256）、训练轨迹是 **11 点/5.5 s**（DD 为 8 点/4 s）。→ **"GoalFlow 自报 90.3 vs MeanFuser 表记 85.7"的矛盾，除 backbone 口径外，还有 `tf_d_model`（512 vs 128，差 4 倍）与训练视野（11 vs 8 点）两重差异。**
3. **评测视野四个仓库统一为 4.0 s，但训练视野不统一**。scorer 与 simulator 的 `proposal_sampling` 都是 `40 poses @ 0.1 s`；GoalFlow 的**训练目标是 5.5 s / 11 点**，但**模型在输出前就把 11 点切成前 8 点**（`goalflow_model_traj.py:407-410` 的 `pred_trajs[:,:,1:1+8,:]` / `[:,:,:8,:]`），`Trajectory` 的 `__post_init__` 也断言必须是 8 点（`dataclasses.py:215-225` 默认 `time_horizon=4, interval_length=0.5`）。→ **口径差异真实存在，但机制是模型侧截断，不是 simulator 截断**（`PDMSimulator.simulate_proposals` 的 `states[:, :num_poses+1]` 只取前 41 个状态，是因为它按 scorer 的 0.1 s 网格工作，与 GoalFlow 的 0.5 s 输出无关）。**结论不变：GoalFlow 生成的第 9–11 点（4.0–5.5 s）参与训练却不参与打分。**
4. **MeanFuser 的"去词表"主张得到代码确认**。其配置类里**没有任何锚点/词表字段**，取而代之是 `noise_type='multi_gaussian'` 与 `navtrain_8_mean_std.pkl`（K=8 高斯混合统计量），`num_proposals=8`、`num_sample_steps=1`。→ 与 [lineage.md](../../topics/diffusion-planner/lineage.md) 转移 1 的"连续混合替代离散词表"一致。
5. **GoalFlow 的主干与 DD 同族，只是宽度不同**（新增）。`GoalFlow/navsim/agents/goalflow/resnet_backbone.py` 首行 docstring 原文 **"Implements the TransFuser vision backbone."**；其 `goalflow_config.py` 与 navsim 的 `transfuser_config.py` **逐字段相同**（`resnet34/resnet34`、±32 m、`pixels_per_meter=4.0`、`hist_max_per_pixel=5`、相机 1024×256、LiDAR 256×256、anchors 8/32/8/8、`n_layer=2/n_head=4/n_scale=4`、`bev_features_channels=64`、`num_bev_classes=7`）。→ 上一版把它写成"自有配置类"**过于保守**：它不是另起一套主干，而是**沿 navsim 的 TransFuser 适配版**（注意与 CARLA 原版不同：原版 `pixels_per_meter=8.0`、`n_layer=8`、相机 960×480），差异集中在 `tf_d_model` 宽度（512 vs 256）。

> 使用方式：本节的表**可以直接作为实验协议的"对齐清单"**——要在同一张表里比较，必须把 `tf_d_model`、`lidar_seq_len`、轨迹视野三项逐一对齐，而不只是说"都用 TransFuser"。

## G. DIVER（DP-A16）的代码级核验

**动因**：DIVER 是本工作空间里"**RL 约束生成质量**"这一路线的代表（与 DiffusionDriveV2 并列），且它是**唯一一个明确基于 SparseDrive 的扩散规划器**——[C005 §G](e2e_trunk_code_traces.md) 已核验 SparseDrive 的规划头，正好可以看扩散是**接在哪里**。读 `mmdet3d_plugin/models/motion/motion_planning_head_DriveStyle.py`（约 1400 行）、`decoder.py`、`diff_motion_blocks.py`、`adzoo/sparsedrive/configs/DIVER_small_b2d_stage2_targetpoint_multiplan.py`、`adzoo/sparsedrive/tools/kmeans/kmeans_plan.py`、README。

| 项 | 代码证据 |
|---|---|
| 代码规模与载体 | `diver` 仓库 **256 个 `.py`**；配置 `DIVER_small_b2d_stage2_targetpoint_multiplan.py`，数据集是 **Bench2Drive**（`B2D3DDataset`、`data/bench2drive/`），不是 NAVSIM |
| 扩散接在哪 | 规划头换成 `DriveStyleMotionPlanningHead`，**沿用 SparseDrive 的 `operation_order`**（`temp_gnn/gnn/cross_gnn/ffn/refine`），另加两组 10 步操作序列：`diff_operation_order`（`traj_pooler/self_attn/agent_cross_gnn/anchor_cross_gnn/ffn/diff_refine`）与 `diff_noise_operation_order`（末项换 `diff_refine_noise`） |
| **噪声起点不是纯高斯，是"GT 命令的锚点轨迹 + 截断噪声"** | `cmd = metas['gt_ego_fut_cmd'].argmax(dim=-1)` → `cmd_plan_anchor = plan_anchor[bs_indices, cmd]` → 差分 → `odo_info_fut`；`timesteps = torch.randint(0, 40, (bs,))`，`self.diffusion_scheduler.add_noise(original_samples=odo_info_fut, noise=noise, timesteps=repeat_timesteps)`，随后 `clamp(-1,1)`。→ **x₀ 是锚点、噪声只加到 DDIM 1000 步中的前 40 步**（与 DiffusionDrive 的 t=8 同思路） |
| DDIM scheduler 只用于加噪 | `DDIMScheduler(num_train_timesteps=1000, beta_schedule="scaled_linear", prediction_type="sample")`——**全仓只调用 `add_noise` 一处**；反向过程是**手写循环**（`reverse_process_sample`，`self.diff_T=10` 步），且**起点是 `reg_target.squeeze(1) + torch.randn(...)`（GT + 噪声）** → **该函数只能训练时用**（推理没有 GT） |
| 扩散维度 | `diff_input_dim=13` = 6 步 × 2 维 + 1 维时间正弦嵌入（`diffusion_reverse_process` 里 `torch.cat([flattened_traj, t_embed])`）；`diff_hidden_dim=256` |
| **"GRPO" 在代码里是"奖励加权损失"** | `diff_PPO_loss_planning` 里：**`diffusion_loss = diffusion_loss * (1.0 + total_reward.mean())`**；`total_reward = 0.5*diversity + 0.3*safety + 0.2*map`。**全仓无 `log_prob` / `advantage` / PPO clip / 组内基线**（grep 无命中）→ 论文写 "employ Group Relative Policy Optimization (GRPO) objectives"，代码里**没有策略梯度的任何要素** |
| 奖励项的实测构成 | `compute_reward`：`safety_reward = 1 - min(1, collision_penalty/num_modes)`，碰撞用 **GT 未来智能体轨迹**（`data['gt_agent_fut_trajs']`）与 `safe_distance = 2.0`；**`map_reward = 1.0`（代码注释自述 "dummy 值"）**；`diversity_reward` = 模态两两距离均值。→ 论文 Eq.20 的 **TTC / 车道保持 / Hydra-MDP PDMS 奖励在代码里都不存在**，且 20% 的奖励是常数 |
| 训练总损失 | `loss()` 里挂的是 `diff_PPO_loss_planning`，**`diff_loss_planning` 被注释掉**；回归项 `reg_loss = reg_loss_target*0.9 + reg_loss_multi_safe_target*0.1`，后者来自下面的 `generate_safe_trajectories` |
| **`check_collision` 的语义与名字相反** | `safe = True` 起手；对每个智能体若 `min_dist >= safe_distance` 则 `safe = False; break` → **只有当"所有智能体都落在 2.0 m 内"时才返回 True**。`generate_safe_trajectories` 因此收集的是**离 GT 智能体极近**的样本（训练时 `num_trajectories=10`），而非"安全"样本 |
| **仓库里有 6 处未注释的调试断点，4 处在 `forward` 里** | `motion_planning_head_DriveStyle.py:600 / 617 / 655 / 969`（均在 `forward`）、`:1052`、`instance_queue.py:221`。→ **发布的代码无法直接跑通一次前向**，必须手动清掉断点 |
| 锚点文件未随仓库发布 | 全仓 **0 个 `.npy`**。`adzoo/sparsedrive/tools/kmeans/kmeans_plan.py` 已改为 **6 命令分组**（`navi_trajs = [[], [], [], [], [], []]`，`K=6`）→ DIVER 的 `kmeans_plan_6.npy` 应是 **(6,6,6,2)**，与 SparseDrive 的同名文件 **(3,6,6,2)** **不是同一个文件** |
| **`num_cmd` 的口径（原记"内部不一致"，**已解决**，见 [C005 §H.3](e2e_trunk_code_traces.md)）** | 原记"配置声明 `num_cmd=6`、`ego_fut_mode=6`（36 候选），但 `HierarchicalPlanningDecoder.decode` 硬编码 `classification.reshape(bs, 1, self.ego_fut_mode)` → 只输出 6 条"是**误读**。更正：**`num_cmd` 是"命令组数"不是候选数**——8 个配置里 3 个 `num_cmd=6`、5 个 `num_cmd=1`，**唯一实例化扩散头**（`DriveStyleMotionPlanningHead`）的是 `DIVER_small_b2d_stage2_targetpoint_multiplan.py`（`num_cmd=6`、`plan_anchor=kmeans_plan_6.npy` **生效**）；而**输出候选数恒为 `ego_fut_mode = 6`**。→ 不再需要运行确认 |

**四条由本节得出的判断**：

1. **DIVER 的"起点先验"被归类错了**。[lineage.md](../../topics/diffusion-planner/lineage.md) 把 DP-A16 与 DP-A20 一起归为"起点先验 = 纯高斯"，但代码里 **x₀ 是 GT 命令对应的 plan anchor**（再叠加 ≤40/1000 步的噪声）。→ 应归入 **"锚点词表"** 一路，与 DP-A02/A03 同类；论文正文写"标准高斯"与代码不符。
2. **DIVER 的"RL"不是策略梯度，而是"把 reward 当损失乘子"**。`diffusion_loss * (1 + reward.mean())` 既没有组内相对基线，也没有对数概率与 clip。→ 引用"DIVER 用 GRPO"时**必须降级为"用奖励加权扩散损失"**；同时 `map_reward` 是 dummy 常数、TTC/LK/PDMS 项缺失，**"多目标奖励"这一卖点在实际发布的配置里只剩多样性与安全两项**。
3. **DIVER 的"安全"奖励用 GT 未来轨迹，且判定函数语义反转**。奖励与"safe trajectory"生成都直接读 `gt_agent_fut_trajs`，`check_collision` 在"全部智能体都在 2 m 内"时返回 True。→ 这条**同时影响它的安全性主张与可复现性**：奖励依赖特权未来信息，且命名与行为不一致，需要运行才能确定实际收集的是哪一类样本。
4. **DIVER 的发布状态与 SparseDrive 同类：锚点文件缺失 + 代码不可直接运行**。全仓无 `.npy`（`kmeans_plan_6.npy` / `kmeans_motion_6.npy` 都要自建），且 `forward` 里有 4 处未清断点。→ 这是本项目里**第 3 个"词表/锚点文件未发布"的仓库**（前两个：VADv2、DiffusionDrive），进一步印证 [§F](#f-同基准可比性的代码级核验四个-navsim-扩散规划器的主干输入视野) 与 [C005](e2e_trunk_code_traces.md) §F3 的判断：**复现基线前必须先解决锚点重建**。

> 另：DIVER 的 README 表里 **nuScenes 开环 L2 Avg 0.21 差于 SparseDrive 0.13 / UniAD 0.15**，碰撞 Avg 0.07 略优于 0.08，多样性 Div.(t) 0.32/0.35 高于 SparseDrive 0.21——**它自己给出了"用 L2 换多样性"的实测证据**，这比任何论证都直接。

## H. 三个"非锚点"扩散规划器的代码级核验（FeaXDrive / WAM-Flow / FlowDrive）

**动因**：§A–§G 覆盖的工作都建立在**轨迹锚点/词表**之上。本节核验三个**不依赖 K-means 轨迹锚点**的代表，看它们各自用什么替代方案——这直接对应 [lineage.md](../../topics/diffusion-planner/lineage.md) 转移 1 的"起点先验"维度。

### H.1 FeaXDrive（DP-A18）——可行性约束与 FA-GRPO 都真实存在

读 `navsim/agents/feaxdrive/{feaxdrive_diffusion_planner.py, trajectory_projector.py, feaxdrive_diffusion_planner_fagrpo.py}`、`navsim/agents/recogdrive/utils/drivable_sdf.py`、`scripts/repro/slurm/*.slurm`、`README.md`、`docs/`。

| 项 | 代码证据 |
|---|---|
| 它是什么 | 规划器类名是 **`ReCogDriveDiffusionPlanner`**（`feaxdrive_diffusion_planner.py:184`）——**FeaXDrive = ReCogDrive 的扩散规划器 + 可行性模块**；仓库里同时保留 `navsim/agents/recogdrive/` 全套 |
| **训练期曲率正则（论文 Eq.14–15）逐字实现** | `_kappa_max_adapt`：`kappa_max_adapt(t) = min(kappa_geo_max, a_lat_max/(v²+eps))`（`trajectory_projector.py:289-320`）；`violation()` 的惩罚是 **hinge-squared**：`relu(\|κ\| − bound)² + relu(\|a_lat\| − a_lat_max)²`（`:336-356`）。官方 `dyn` 档超参：**`proj_kappa_geo_max=0.166`、`proj_a_lat_max=6.0`、`proj_use_kappa_adapt=true`、`lambda_dyn=0.01`**（`submit_train_feaxdrive.slurm:314-332`） |
| **但"约束一致性训练"项在官方链路里全为 0** | 同处超参：**`lambda_proj=0.0`、`lambda_proj_supervise=0.0`**；代码注释明写 `use_constraint_projection` **is deprecated in the current official chain**。→ **论文的 `‖x₀−Π(x₀)‖²` 与 `‖Π(x₀)−x_gt‖²` 两项在发布版里没有启用**，投影机制（`project_dynamics` / `project_drivable`）是保留但未接入的代码 |
| x0 预测是统一对象 | `pred_type='x0'` → `base_loss = F.mse_loss(x0_pred, gt_actions)`（`:902-903`）；`lambda_dyn>0` 时 `total_loss += lambda_dyn * violation(denorm(x0_pred))`（`:928-930`）——**惩罚施加在干净轨迹上**，与论文"把可行性建模移入 clean trajectory space"一致 |
| **推理期引导（Eq.22–23）逐条实现** | `_apply_drivable_guidance`（`:376-487`）：**只在最后 `last_k=3` / 共 5 步生效**；`step = 0.05 · progress^1.0`；障碍项 `softplus((margin_m − sdf)/beta_m)`，**`margin_m=0.30`、`beta_m=0.20`**；梯度对 **x0 估计** 求（`x0_g.requires_grad_(True)`），**XY 按样本归一化为单位向量**、heading 用**符号归一化**×`heading_scale=0.1`，`x0_new = x0 − step·grad` |
| SDF 怎么来的 | `recogdrive/utils/drivable_sdf.py`：ego 系 ROI **x∈[−10, 80] m、y∈[−30, 30] m、分辨率 0.2 m**；可行驶层 = ROADBLOCK / INTERSECTION / DRIVABLE_AREA / CARPARK_AREA；`distance_transform_edt` 后 `clip(din−dout, ±50)`。**官方链路固定 `DRIVABLE_SDF_SOURCE=data_map`**（从 scene map_api 重建，不用 MetricCache；脚本对其它取值直接报错退出） |
| **FA-GRPO 是真 GRPO**（与 DIVER 相反） | `forward_grpo`（`:1275-1344`）：`G=sample_time=8` 条/样本 → `advantages = (R − mean)/std` **组内归一化** → 分位裁剪 → `discount = 0.6^(剩余去噪步)` → `get_logprobs`（对去噪链的 `Normal(mean, std).log_prob`）→ `policy_loss = −mean(logp · adv_weighted)`；另加 **BC 项**：`total_loss = policy_loss + 0.1 · (−logp(old_policy 采样链))`。奖励 = **真 PDM 分数**（`PDMSimulator` + `PDMScorer` 逐条仿真打分） |
| FA-GRPO 的奖励权重与标准不同 | `progress_weight=10.0`（navsim 标准 5.0）、`ttc_weight=5.0`、`comfortable_weight=10.0`（标准 2.0）；脚本里有**安全断言**：若标准评测 scorer 被 FA-GRPO 的 comfort 指标污染则直接 `exit 3` |
| **违规率的判据（解决原笔记待核验项）** | `_curvature_and_alat`（`:203-259`）：先对 xy 做**二项式核平滑**（`smooth_ksize=5`），再按**弧长参数化**用变步长中心差分算 κ，`a_lat = v²·κ`（`v` = 弧长/dt，`dt=0.5`），**两端点补 0**。违规率 = `(\|val\| > bound).float().mean()`（`:364-368`），同时输出 **`kappa_violation_rate`（固定界）与 `kappa_adapt_violation_rate`（自适应界）两套**。→ **判据是"逐时间步超限比例"，且依赖平滑核与端点补零**；DiffusionDrive 的 8.59% 是用**同一套 FeaXDrive 判据**测的，故论文内可比，**跨论文不可比** |
| 发布状态 | 全仓**无未注释断点**、**无缺失 `.npy`**（本就不需要锚点），带 `scripts/repro/slurm/` 三个复现脚本 + 4 篇 `docs/` 说明。→ **是本项目目前核验过的扩散规划器里可复现性最好的一个** |

**三条判断**：

1. **FeaXDrive 的两个核心机制（自适应曲率正则、softplus SDF 引导）都是真实实现**，且超参与论文数字对得上（0.166 / 6.0 / margin 0.30）。这是本工作空间里**第一篇"约束类主张"经代码确认成立**的工作。
2. **但论文的"约束一致性训练"（Π 投影监督）在发布配置里未启用**（`lambda_proj = lambda_proj_supervise = 0`，且 `use_constraint_projection` 被标注弃用）。→ 引用时**只能说"训练期软违规惩罚 + 推理期软引导"**，不能说"投影/一致性训练"。
3. **它自己的 README 给出了两条对本题最不利的数字**：① **ReCogDrive w/GRPO 的 PDMS 是 90.5，高于 FeaXDrive 的 90.0**；② **FA-GRPO 把曲率违规从 0.88% 抬到 2.40%**（普通 GRPO 更差，15.5%）。→ **"RL 提升分数"与"RL 破坏可行性"在同一张表里同时成立**，这正是 [preparation.md](../../ideas/preparation.md) 方向 A 要处理的核心张力。

### H.2 WAM-Flow（DP-A13）——"轨迹 token 词表"其实是文本数字

读 `navsim/agents/wam_flow_agent.py`、`flow_matching/solver/discrete_solver.py`、`flow_matching/data/navsim.py`、`config/sft_navsim.yaml`。

| 项 | 代码证据 |
|---|---|
| 轨迹怎么生成 | `initialize()` 里 **`num_tokens = [f"{x:.2f}" for x in np.linspace(-100, 100, 20001)]`**，再 `tokenizer.add_tokens(num_tokens)`（`:197-199`）→ **把"−100.00 到 100.00、步长 0.01"的 20001 个数字字符串加进 VLM 词表**，轨迹以**文本数字**形式被生成 |
| 词表规模 | `vocab_size=102400`（VLM 原词表）+ 上述 20001 个数字 token；`vocabulary_size_txt = max(len(tokenizer), embedding 行数)` |
| 生成机制 | **联合离散流匹配**：`MixtureDiscreteSoftmaxEulerSolver`，`path_txt = MixtureDiscreteSoftmaxProbPath(mode='text')`、`path_img = ...(mode='image')`；`source_distribution="uniform"`、`use_quantize=True`、`discrete_fm_steps=50`；`data_info` 里带 `text_token_mask` / `image_token_mask` |
| 输出与视野 | `extract_num_list` 从生成文本里解析 **恰好 16 个数字 = 8 waypoints × 2（x,y）**；`trajectory_sampling = 4.0 s / 0.5 s` → 8 点。**heading 不由流匹配生成**，另加载 `TrajectoryHeadingMLP`（`heading_mlp_path`） |
| 输入权限 | `SensorConfig(cam_f0=[3], ...)` —— **只用前视相机一帧，无 LiDAR、无环视** |

**判断**：lineage 表里把 DP-A13 记为"轨迹 token 词表"是对的，但**机制要写清楚**：它不是学出来的轨迹码本，而是**把连续坐标按 0.01 m 量化为文本数字 token，借 VLM 的词表与自回归/流匹配生成能力输出轨迹**。→ 这条路线的"词表"是**分词器层面**的，与 VADv2/DiffusionDrive 的"轨迹码本"**不是同一类东西**，两者不可混谈。

### H.3 FlowDrive（DP-A10）——"moderated"是采样中段的几何注入，选优靠规则 PDM

读 `flow_drive/model/flow_drive_planner.py`、`flow_drive/utils/{infer_utils,dataset}.py`、`flow_drive/planner/planner.py`、`flow_drive/config/config.yaml`。

| 项 | 代码证据 |
|---|---|
| 源分布与步数 | `sample_action_with_speed_and_lateral_offsets`：`x_t = torch.randn(...)`（**纯高斯**）；`sampler.set_timesteps(flow_inference_iter)`，配置里 **`flow_inference_iter=8`**、`flow_train_iter=2000`、`pred_horizon=40`（4 s @10 Hz） |
| **"moderated" 是什么** | 生成 **`S = len(speed_offsets) × len(lateral_offsets)` = 20** 条；在**去噪中段**（`applied_index = len(int_ts)//2 − 1`）调用 `_apply_speed_and_lateral_adjustments`，沿**自车航向**做纵向拉伸、沿**法向**做横向平移（`:193-198`）——**这是把显式几何扰动注入采样轨迹中点**，不是 guidance、也不是条件 |
| 后处理 | `smooth_trajectories_preset(..., preset="strong")` + `bound_speed_and_acceleration(actions, ego_state, speed_limit)`（`:146-152`）；每步还把第 0 帧钉死为当前自车状态 |
| **选优用的是规则 PDM，不是学到的 scorer** | `planner.py`：`_post_process == 1` 时 → `self._trajectory_scorer.score_plans(outputs)` → `index = np.argmax(scores)`；`TrajectoryScorer` 内部就是 **navsim/nuPlan 的 `PDMSimulator` + `PDMScorer` + `PDMEmergencyBrake`**，`TrajectorySampling(num_poses=40, interval_length=0.1)` → **4.0 s** |
| **20 簇文件确实随仓库发布，但只用于数据平衡** | `flow_drive/config/ego_future_clusters.pkl`（787 KB）实测内容：**`cluster_centers` (20, 80) float32**（80 = 40 步 × 2）、**`cluster_labels` (100200,) int32**、`n_clusters=20`。用法：`_compute_weights_for_balanced_clusters` 用 `argmin` 距离给每个场景定簇，再按簇频率**反比加权**（`balance_mode: "cluster"`、`weighted_sampling: True`）。**`ClusterStatsRetriever` 全仓只被这一处调用** → **簇中心不参与流匹配的初始化** |
| 附带的一条 PDM 修正 | README 要求把 tuplan_garage 的 `pdm_object_manager.py` 换成仓库内版本，理由是"恒速预测的物体应沿**速度方向**而非**朝向**运动"，并自述 **"This fix improves the performance of PDM and FlowDrive* significantly."** |

**判断**：FlowDrive 的 20 簇是本项目见到的**第 5 种"轨迹簇"用法**——**只做数据平衡，不做生成先验**。① VADv2 = 输出答案集；② DiffusionDrive = 扩散起点；③ DiffusionDriveV2 = 候选池成员；④ SparseDrive = query 初始化；⑤ **FlowDrive = 训练样本权重**。→ 引用"用 K-means 轨迹簇"时必须说明是**哪一类用法**，否则会把数据平衡的收益误读成先验质量。

### H.4 本节对"起点先验"维度的更新

| 工作 | 源分布 | 候选/选优 | 代码依据 |
|---|---|---|---|
| FeaXDrive（DP-A18） | **纯高斯**（`pred_type='x0'`，DiT 直出干净轨迹） | 单条；无候选选择 | `sample` / `get_action` 只出一条轨迹 |
| WAM-Flow（DP-A13） | **文本数字 token 上的均匀分布** | 单条（文本贪心/采样） | `source_distribution="uniform"` |
| FlowDrive（DP-A10） | **纯高斯** | **20 条（speed×lateral 调制）→ 规则 PDM argmax** | `plan_multiple_trajectories_with_moderated_offset` |

→ 加上 §A–§G、**§J**（本册）与 **§K**（[第二册](diffusion_planner_code_traces-2.md)），**研究对象侧的 13 个仓库已全部核验完毕**：**逐文件核验 12 个**（DD、DDV2、Diffusion-Planner、DiffusionVeteran、MeanFuser、GoalFlow、PC-Diffuser、DIVER、FeaXDrive、WAM-Flow、FlowDrive、HDP）+ **1 个零代码**（**DriveFine**，DP-A29）。**"起点先验"这一维现在有 5 类实测值**：纯高斯、锚点词表、高斯混合、文本数字 token、20 簇（仅数据平衡，不参与生成）。

---

**§I 及以后见 [diffusion_planner_code_traces-2.md](diffusion_planner_code_traces-2.md)**（本册为 §A–§H；§I–§P 含 PC-Diffuser / HDP / DriveFine / Flow Planner / ReCogDrive / GuideFlow / LCS / BridgeDrive / MPDiffuser / DIPOLE）。拆分原因：原文 103 KB，超 Read 工具 64 KB 上限。
