# 官方代码仓库快照

更新时间：2026-09-23  
存放位置：本文件同目录的 `repos/`（`--depth 1 --single-branch`，保留 `.git`；少数因 git 传输失败改用 codeload tarball）。共 **37 个仓库、约 1.65 GB**（2026-09-23 第二十一轮新增 `OpenDriveVLA`；`AutoVLA` 因网络阻塞未落盘全仓，见 §E）。**§D/§E 另有 3 个"在列但未落盘"的条目**（`WoTE`、`DriveDreamer`、`AutoVLA` 已落盘部分），不计入上述快照数。  
**状态说明**：全部仅完成克隆，**未安装依赖、未下载数据、未运行任何代码**；结论只到"静态检查 / 目录结构"级别。  
选择标准：**论文声称有官方代码，且已克隆核验代码存在**（2026-09-23 修正——原标准只写"论文有官方代码"，核验后发现在列仓库里有 4 个实际无代码或代码不全，见「已确认无官方代码」表与 [traces/e2e_trunk_code_traces.md](traces/e2e_trunk_code_traces.md) §A）。  
**跨项目共用**：C 节的 6 个具身侧仓库供 [embodied-ai](../../embodied-ai/index.md) 引用。2026-09-23 决定**不按项目拆分**（仓库交叉引用 + 避免 1.65 GB 重复），理由见 [workspace-design.md](../../../shared/workspace-design.md)「当前落地状态」。

## A. 扩散规划器与评测基准（13 个）

| 目录 | 论文 / 编号 | 仓库 | commit | 体积 | 为什么保留 |
|---|---|---|---|---|---|
| `DiffusionDrive` | DiffusionDrive（DP-A02） | [hustvl/DiffusionDrive](https://github.com/hustvl/DiffusionDrive) | `9b52ed0ec06b073d82d6f392ab084c7b301c8681` | 16M | 本项目基线案例；与前序会话记录一致 |
| `DiffusionDriveV2` | DiffusionDriveV2（DP-A03） | [hustvl/DiffusionDriveV2](https://github.com/hustvl/DiffusionDriveV2) | tarball（master） | 16M | 同家族后续版本；NAVSIM v1 91.2 |
| `Diffusion-Planner` | Diffusion Planner（DP-A01） | [ZhengYinan-AIR/Diffusion-Planner](https://github.com/ZhengYinan-AIR/Diffusion-Planner) | `a3a621f0b724c5fa6447f7a2fbaf9e0387bd35df` | 32M | nuPlan 闭环 + classifier guidance 的参考实现 |
| `Hyper-Diffusion-Planner` | HDP（DP-A06） | [ZhengYinan-AIR/Hyper-Diffusion-Planner](https://github.com/ZhengYinan-AIR/Hyper-Diffusion-Planner) | `f37cb9ffc36986510691155126a1fe7a0ea89c32` | 87M | **同仓含 `HDP-navsim` 与 `HDP-nuplan` 两套实现**——跨生态代码级证据。**已逐文件核验（[C003 §J](traces/diffusion_planner_code_traces-2.md)）**：无锚点纯扩散成立；损失空间有同主干受控对照；"数据规模"不可复现；HDP-RL 为**优势加权回归**；相对上游 Diffusion Planner **退化为 ego-only 并删掉 `guidance/` 模块** |
| `GoalFlow` | GoalFlow（DP-A09） | [YvanYin/GoalFlow](https://github.com/YvanYin/GoalFlow) | `411fdbda4e7b77874dbd38776de2b8b9408fbeaf` | 147M | 流匹配路线的事实基准 |
| `MeanFuser` | MeanFuser（DP-A14） | [wjl2244/MeanFuser](https://github.com/wjl2244/MeanFuser) | `8de8ba6244834645192e318dcc437d124cfd6872` | 6.3M | 一步生成 + 高斯混合噪声 |
| `WAM-Flow` | WAM-Flow（DP-A13） | [fudan-generative-vision/WAM-Flow](https://github.com/fudan-generative-vision/WAM-Flow) | `747dad929a419e11c7fb2fcbd57fec90e9e31a55` | 33M | 离散流匹配；README 致谢 WAM-Diff/Janus/ReCogDrive |
| `diver` | DIVER（DP-A16） | [adept-thu/diver](https://github.com/adept-thu/diver) | `351530aca4903c24a9e42f137cd899f183451c07` | 41M | RL 约束生成质量；README 显示基于 SparseDrive。**额外价值（第二十四轮）：本仓逐字节 vendored 了官方 Bench2Drive 的整套评测栈**（`leaderboard/` + `scenario_runner/` + `tools/ability_benchmark.py` / `efficiency_smoothness_benchmark.py` / `merge_route_json.py`），**已与官方 `0.0.4` 分支逐字节比对确认 IDENTICAL**（唯一差异是 `autoagents/autonomous_agent.py:118` 多一行注释掉的 `pdb`）→ **Bench2Drive 的代码级口径就靠它核验，无需克隆官方仓库**，详见 [benchmarks.md §2.7](../direction/benchmarks.md) |
| `PC-Diffuser` | PC-Diffuser（DP-A21） | [Eugene29/PC-Diffuser](https://github.com/Eugene29/PC-Diffuser) | `f4b08a15450e2446afa533965536690b7e8b3162` | 1020K | 驾驶域认证级硬约束；内含 `diffusion-planner-cbf` + vendored nuplan-devkit |
| `FeaXDrive` | FeaXDrive（DP-A18） | [BaoyunWang/FeaXDrive](https://github.com/BaoyunWang/FeaXDrive) | `31669441221cdc80d61a08f7e5eae96a579e479d` | 11M | 可行性建模与违规率判据 |
| `DriveFine` | DriveFine（DP-A29） | [MSunDYY/DriveFine](https://github.com/MSunDYY/DriveFine) | `f44f86e5e9e48645acbffef340d9b3df90e60654` | 648K | **零代码**：全仓仅 `README.md` + `images/overview.png`（GitHub 上只有 `main` 一个分支、单次提交，`created 2026-02-16` / `pushed 2026-02-17`，此后无更新）。README 明写基于 ReCogDrive + LaViDa，但**机制主张只能停留在论文自述级**（见 [C003 §K](traces/diffusion_planner_code_traces-2.md)） |
| `flow_drive_planner` | FlowDrive（DP-A10） | [einsteinguang/flow_drive_planner](https://github.com/einsteinguang/flow_drive_planner) | `06f941e3681a6a508b3e0e09ec35e2256ac26771` | 94M | nuPlan/PLUTO 血统 + 数据重加权 |
| `navsim` | NAVSIM（B001） | [autonomousvision/navsim](https://github.com/autonomousvision/navsim) | `0a380a9063d7162ec93d0f51e9990ebac585f720` | 66M | 主评价基准实现。**已代码级核验**（指标 + Agent/评测接口两侧，见 [benchmarks.md §2](../direction/benchmarks.md)）：指标侧 EP 为批内相对分、EPDMS 权重中心是**本方法自己的终点**（跨论文不可比）；接口侧只需实现 3 个抽象方法、`compute_trajectory` 无 batch 版、评测**禁止读标注场景**（`requires_scene=True` 直接报错）、输出 8 poses 但打分 40 poses 且**轨迹会被 LQR 重新仿真**；`EPDMS` 一词**代码里不存在**（叫 `extended_pdm_score_*`） |

## B. 端到端主干（13 个）

**2026-09-23 全扫核验**：本节 13 个仓库逐个统计了 `.py` 文件数，**发现 2 个零代码**（`Hydra-MDP`、`DriveVLM`）。逐仓库结论与谱系见 [traces/e2e_trunk_code_traces.md](traces/e2e_trunk_code_traces.md) §A。**研究对象侧 13 个仓库同期核验完毕**（12 逐文件 + `DriveFine` 零代码，见 [C003 §K](traces/diffusion_planner_code_traces-2.md)）。

| 目录 | 论文 / 编号 | 仓库 | commit | 体积 | 代码核验 |
|---|---|---|---|---|---|
| `UniAD` | UniAD（[E2E-01](../direction/notes/E2E-01-uniad.md)） | [OpenDriveLab/UniAD](https://github.com/OpenDriveLab/UniAD) | `609ee083ea51c3521c323f1279dfc4cee0e60467` | 17M | 122 个 `.py`，完整 |
| `VAD` | VAD / VADv2（[E2E-02](../direction/notes/E2E-02-vad.md)、[E2E-03](../direction/notes/E2E-03-vadv2.md)） | [hustvl/VAD](https://github.com/hustvl/VAD) | `1688c4b1c3a9e2e7873ca9700ff8058170c0e3c8` | 2.8M | v1 完整（172 个 `.py`）；**VADv2 仅 config + head 两个文件**，且 `carla_plan_vocabulary_4096.npy` 未发布 |
| `SparseDrive` | SparseDrive（[E2E-04](../direction/notes/E2E-04-sparsedrive.md)） | [swc-17/SparseDrive](https://github.com/swc-17/SparseDrive) | `fbadea693cbef3f3daea7705e521c0dd3321605c` | 2.9M | 75 个 `.py`，完整 |
| `Hydra-MDP` | Hydra-MDP（[E2E-05](../direction/notes/E2E-05-hydra-mdp.md)） | [NVlabs/Hydra-MDP](https://github.com/NVlabs/Hydra-MDP) | `16f195c20f336c4590474dd2f0c711375b4d7a6a` | 2.5M | **零代码**：仅 `README.md` + 一张图。README 自述 "Delay in code and model release due to company policy" |
| `TCP` | TCP（[E2E-08](../direction/notes/E2E-08-tcp.md)，NeurIPS'22） | [OpenDriveLab/TCP](https://github.com/OpenDriveLab/TCP) | `73cc1ddfb615439b3f035c0285f5c9ffce350418` | 181M | 140 个 `.py`，完整（含 CARLA 侧） |
| `ST-P3` | ST-P3（[E2E-09](../direction/notes/E2E-09-st-p3.md)，ECCV'22） | [OpenDriveLab/ST-P3](https://github.com/OpenDriveLab/ST-P3) | `69aabefd2610951d9e34238142776ed2228673be` | 7.4M | 27 个 `.py`，完整 |
| `neat` | NEAT（ICCV'21） | [autonomousvision/neat](https://github.com/autonomousvision/neat) | tarball（main） | 65M | 140 个 `.py`，完整 |
| `imitation-learning` | CIL（CoRL'18） | [carla-simulator/imitation-learning](https://github.com/carla-simulator/imitation-learning) | `62f93c2785a2452ca67eebf40de6bf33cea6cbce` | 157M | 仅 5 个 `.py`，`.gitmodules` 为空，子模块未接入 |
| `LearningByCheating` | LBC（CoRL'19） | [dotchen/LearningByCheating](https://github.com/dotchen/LearningByCheating) | `4145d33f74c9a8f27061a0f94840f3e458ecc60e` | 3.7M | 63 个 `.py`，完整 |
| `DriveVLM` | DriveVLM（CoRL'24） | [Tsinghua-MARS-Lab/DriveVLM](https://github.com/Tsinghua-MARS-Lab/DriveVLM) | `c040a178bc1add47e460cc867f466995a402a276` | 52M | **零代码**：仅 `index.html` + `images/` + `DriveVLM.pdf`，**这是项目主页不是代码仓库** |
| `transfuser` | TransFuser（[E2E-07](../direction/notes/E2E-07-transfuser.md)，CVPR'21） | [autonomousvision/transfuser](https://github.com/autonomousvision/transfuser) | tarball（2022） | 84M | 133 个 `.py`，完整 |
| `GenAD` | GenAD（生成式 E2E） | [wzzheng/GenAD](https://github.com/wzzheng/GenAD) | tarball（main） | 79M | 848 个 `.py`，完整（规模最大）。**已逐文件核验（[C005 §J](traces/e2e_trunk_code_traces.md)）**：基于 VAD 代码库；生成机制是 **32 维对角高斯隐变量 + spatial GRU + 解析 KL**（CVAE 式，**非扩散、无词表**） |
| `DriveLM` | DriveLM（ECCV'24） | [OpenDriveLab/DriveLM](https://github.com/OpenDriveLab/DriveLM) | tarball（main） | 49M | 23 个 `.py`，以数据/文档与挑战赛工具为主 |

## C. 具身侧（6 个）

| 目录 | 论文 / 编号 | 仓库 | commit | 体积 | 代码核验 |
|---|---|---|---|---|---|
| `diffusion_policy` | Diffusion Policy（DP-E09） | [real-stanford/diffusion_policy](https://github.com/real-stanford/diffusion_policy) | `5ba07ac6661db573af695b419a7947ecb704690f` | 32M | **已代码核验**：22 个 workspace 配置里 `n_action_steps` **14 个取 8 / 8 个取 1**、`horizon` **13 个取 16**（[transfer.md §1.1](../topics/diffusion-planner/transfer.md)） |
| `3D-Diffusion-Policy` | DP3（DP-E10） | [YanjieZe/3D-Diffusion-Policy](https://github.com/YanjieZe/3D-Diffusion-Policy) | `47385d9d6f5bde3f2ebdf2400ecb8261cc9e6b97` | 137M | **已代码核验**：编码器是 **4 层 Linear**（`in→64→128→256→512`）+ 全局 max-pool，输出 **64 维**；"simple" 变体改的是 U-Net 宽度（`down_dims` 512/1024/2048 → 128/256/384） |
| `visualnav-transformer` | NoMaD（DP-E17） | [robodhruv/visualnav-transformer](https://github.com/robodhruv/visualnav-transformer) | `dca79815b704e5aa9c6bdc3082351f9e3b2848c2` | 724K | **已代码核验**：`goal_mask_prob: 0.5` 确认；`len_traj_pred: 8`；`num_diffusion_iters: 10`；掩码平均带 `(context_size+2)/(context_size+1)` 重加权 |
| `diffuser` | Diffuser（DP-E01） | [jannerm/diffuser](https://github.com/jannerm/diffuser) | `7ea422860cc0106e5ca5949d980f04b799d5462c` | 1.7M | **已代码核验**：引导实现 `n_step_guided_p_sample`（`scale` 默认 0.001、`scale_grad_by_std=True` → **梯度乘后验方差**、`t_stopgrad` 晚引导、每步引导后 `apply_conditioning` 硬投影）；`release-run.sh` 只扫 `scale ∈ {0.1, 0.001}` 且**单任务** |
| `DiffusionVeteran` | 扩散规划设计选择实证（DP-S14） | [Josh00-Lu/DiffusionVeteran](https://github.com/Josh00-Lu/DiffusionVeteran) | `8d60e3c2b60a99136a82d8e719917d4fec56a878` | 30M | **已代码核验**：三条引导路线并列（`MCSS` 无引导 + critic 选优 / `cfg` 条件引导 / `cg` 分类器引导 + 选优）与 9 维消融网格，见 [C003 §C/E](traces/diffusion_planner_code_traces.md) |
| `openpi` | π0 / π0.5（DP-E19/E20） | [Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) | `215abfb217dbac7d5f1273282331b9b1866c0479` | 2.7M | **已代码核验**：`pi0.py` 确认**条件流匹配**（`x_t = t·noise + (1−t)·actions`、`u_t = noise − actions`、速度场 MSE、Euler 10 步）；`action_horizon=50`；**时间采样是 `Beta(1.5,1)` 而非均匀**；作者自承**代码时间约定与论文相反**；π0.5 的核心改动是**状态离散化进语言 token**（[transfer.md §1.4](../topics/diffusion-planner/transfer.md)） |

## D. 世界模型侧（在列 6 个，其中 **4 个已落盘**；2026-09-23 新增）

| 目录 | 论文 / 编号 | 仓库 | commit | 体积 | 代码范围核实 |
|---|---|---|---|---|---|
| `OccWorld` | OccWorld（[WM-03](../topics/world-model/notes/WM-03-occworld.md)） | [wzzheng/OccWorld](https://github.com/wzzheng/OccWorld) | tarball（main） | 42M | **世界模型 + 规划器齐全**，含 `PlanUAutoRegTransformer` 与 `PlanRegLossLidar` |
| `Policy-World-Model` | Policy World Model（[WM-17](../topics/world-model/notes/WM-17-policy-world-model.md)） | [6550Zhao/Policy-World-Model](https://github.com/6550Zhao/Policy-World-Model) | `c67e4b90364d8e94ff54fba4905ea2550c8ea138` | 29M | **世界模型 + 规划头齐全**（Show-o 主干 + MAGVIT-v2 tokenizer） |
| `Drive-WM` | Drive-WM（[WM-01](../topics/world-model/notes/WM-01-drive-wm.md)） | [BraveGroup/Drive-WM](https://github.com/BraveGroup/Drive-WM) | `eabe3c63bf362a2edf0fb6cbcb908424d2e18980` | 22M | **仅图像生成侧**（vendored `diffusers` + 转换脚本）；**论文的 tree-based planner 与 image reward 不在仓库内** |
| `WorldRFT` | WorldRFT（[WM-18](../topics/world-model/notes/WM-18-worldrft.md)） | [pengxuanyang/WorldRFT](https://github.com/pengxuanyang/WorldRFT) | `e59a4b991559c9fe301a0e3da4b5bc6e4b1942e7` | 208K | **仓库为空**，仅 `LICENSE` + `readme.md`；readme 称代码"soon"上传 |
| `WoTE`（**未落盘**） | WoTE（[WM-24](../topics/world-model/papers.md)） | [liyingyanUCAS/WoTE](https://github.com/liyingyanUCAS/WoTE) | 未取（main，10 次提交） | — | **世界模型 + 规划器 + 奖励模型齐全，已源码核验**（[C004 §E](traces/world_model_code_traces.md)）：`navsim/agents/WoTE/`（`WoTE_model.py` 41,430 B + `WoTE_agent.py` + `WoTE_targets.py` + `configs/default.py`）。实测 **256 锚 + `argmax` 选优 + 8 poses@2 Hz** 成立；**默认配置只跑 1 步世界模型**（`num_fut_timestep = 1`）；`use_wm` 参数**声明未接线**。**未克隆**：走 `raw.githubusercontent.com` 逐文件取证（270 stars，Apache-2.0） |
| `DriveDreamer`（**未落盘**） | DriveDreamer（[WM-21](../topics/world-model/papers.md)） | [JeffWang987/DriveDreamer](https://github.com/JeffWang987/DriveDreamer) | 未取 | — | **代码范围不符**：仓库为图像/视频生成侧（Auto-DM + ActionFormer），**论文的"未来动作"规划脚本未见** → 与 Drive-WM 同类 |

### D.1 第二十四轮新核实的世界模型侧仓库（**全部未落盘**，走 raw/API 取证）

来源：世界模型侧"代码可用性全表"（见 [world-model/verification.md §5](../topics/world-model/verification.md)）。**这 6 个是"有官方代码且含规划器/接口代码"的**。**WM-05（IR-WM）的专属实现已确认在同仓的 `ir-wm` 分支**（main 分支 README 直链该分支，main 全树对 `residual｜implicit` 零命中）。

| 目录 | 论文 / 编号 | 仓库 | 最后推送 | 体积 / 文件数 | 代码范围核实 |
|---|---|---|---|---|---|
| `Drive-OccWorld` | Drive-OccWorld（[WM-04](../topics/world-model/papers.md)） | [yuyang-cloud/Drive-OccWorld](https://github.com/yuyang-cloud/Drive-OccWorld) | 2026-02-10 | ~116 MB / 177 | **世界模型 + 显式规划头，已逐文件核验**（[C004 §I.1](traces/world_model_code_traces.md)）：未来占据 → `argmax` → `instance_occupancy`/`drivable_area` → **`Cost_Function` → cost volume → `topk(largest=False)` 选优**；`planning_steps=1` 逐帧；**规划损失抄自 UniAD** |
| `LAW` | LAW（[WM-06](../topics/world-model/notes/WM-06-law-latent-world-model.md)） | [BraveGroup/LAW](https://github.com/BraveGroup/LAW) | 2025-06-29 | ~0.86 MB / 180 | **世界模型损失 + VAD 规划头，已逐文件核验**（[C004 §I.3](traces/world_model_code_traces.md)）：`wm_prediction(view_query_feat, cur_waypoint)` **以显式 waypoint 为动作条件**预测下一帧潜状态；重建目标是 **view query 特征**；`CD_loss.py` 是**轨迹点损失集合**（非对比蒸馏） |
| `World4Drive` | World4Drive（[WM-07](../topics/world-model/papers.md)） | [ucaszyp/World4Drive](https://github.com/ucaszyp/World4Drive) | 2025-12-31 | ~292 MB / 450 | **世界模型损失 + waypoint 解码，已逐文件核验**（[C004 §I.2](traces/world_model_code_traces.md)）：**`class W4D(VAD)` 继承 VAD**；**`select_optimal_modality` 用"重建+KL+余弦"当模态分配准则**（但 FDE 项用 GT）；锚点同名 `kmeans_plan_6.npy` |
| `TrafficBots` | TrafficBots（[WM-10](../topics/world-model/papers.md)） | [zhejz/TrafficBots](https://github.com/zhejz/TrafficBots) | 2023-09-29 | ~0.37 MB / 62 | **多智能体运动预测/动作头**，**不是轨迹规划** |
| `DriveLaW` | DriveLaW（[WM-11](../topics/world-model/papers.md)） | [xiaomi-research/drivelaw](https://github.com/xiaomi-research/drivelaw) | 2026-08-24 | ~32 MB / 2376 | **重点：世界模型 + 扩散规划器同仓**（已逐文件核验，[C004 §G](traces/world_model_code_traces.md)）——LTX 视频世界模型（`action_expert: true`，动作专家内嵌）+ **`ReCogDriveDiffusionPlanner`** + **DiffusionDrive 基线**；**`recogdrive_agent.yaml` 的 `_target_` 是死引用**（`navsim/agents/` 下无 `recogdrive/`） |
| `DrivingGen` | DrivingGen（[WM-20](../topics/world-model/papers.md)） | [youngzhou1999/DrivingGen](https://github.com/youngzhou1999/DrivingGen) | 2026-03-13 | ~61 MB / 1274 | **评测基准**（含轨迹提取 agent），非规划器 |

## E. VLA 侧（在列 **8** 个，其中 **1 个已落盘**；2026-09-23 新增，第三十六轮补 2 个）

来源：第二十一 / 二十二轮 VLA 代表工作的源码级核验（结论见 [vla/verification.md §5、§6](../topics/vla/verification.md)），**第三十六轮补入 `DiffVLA` 与 `recogdrive`**（结论见 [VLA-06 笔记](../topics/vla/notes/VLA-06-diffvla.md) 与 [C003 §M](traces/diffusion_planner_code_traces-2.md)）。

> **本节的特殊性**：除 `OpenDriveVLA` 外，**其余 7 个都未克隆到本地**——第二十二轮的 4 个仓库体积在 **98–452 MB**（合计约 1.2 GB，会让工作空间接近翻倍），故改用 **GitHub API 逐文件取证 + 目录清单核验**（方法见文末「下载方法」第 6 条）。因此本节不计入上文"37 个仓库、约 1.65 GB"的本地快照数。

| 目录 | 论文 / 编号 | 仓库 | commit | 体积 | 代码范围核实 |
|---|---|---|---|---|---|
| `OpenDriveVLA` | OpenDriveVLA（[VLA-03](../topics/vla/papers.md)） | [DriveVLA/OpenDriveVLA](https://github.com/DriveVLA/OpenDriveVLA) | `10e8095bc618d508cb70cca37b6956ac4db6e9f3`（2026-02-16） | 38M | **部分发布**：环境 + 推理代码 + **0.5B 权重**已发布，**README TODO 里 `Release training scripts` 未勾选** → 四阶段训练不可核验；`scripts/` 只有 `eval_drivevla.sh` |
| `AutoVLA` | AutoVLA（[VLA-11](../topics/vla/papers.md)） | [ucla-mobility/AutoVLA](https://github.com/ucla-mobility/AutoVLA) | 见下注 | ~39M | **完整发布**：`models/`（`autovla.py` 含 GRPO、`action_tokenizer.py`）+ `codebook_cache/agent_vocab.pkl`（实测 **`(2048,6,4,2)`×3 类**）+ `config/` + `tools/run_rft.py` + vendored `navsim`。**未落盘全仓**：`git clone` 连续 5 次 TLS 失败（`gnutls_handshake() failed`），codeload tarball 两次尝试分别**稳定截断在 9,605,125 / 9,175,408 字节**（`gzip -t` 失败）→ 与 Flow Planner 同类判定为**网络阻塞**，核验改用 **GitHub API + raw 逐文件取证** |
| `SimLingo` | SimLingo（[VLA-19](../topics/vla/papers.md)） | [RenzKa/simlingo](https://github.com/RenzKa/simlingo) | 未落盘（main，2025-08-25 最后推送） | 98.6M | **完整发布**：`simlingo_training/`（训练）+ `simlingo_base_training/`（**基础版 = 原 CarLLaVA**）+ `team_code/`（CARLA agent）+ 数据采集与 **dreaming 生成** + vendored `Bench2Drive`/`leaderboard`/`scenario_runner`。**已 API 逐文件核验 7 个文件**（[vla/verification.md §6](../topics/vla/verification.md)）：8 条论文声称**全部一致**，并补上论文未给的 **N_w=10 / N_p=20**。发布史：2025/05/08 代码 → 05/26 数据集 → 06/25 权重+推理。453 stars |
| `Minddrive` | MindDrive（[VLA-16](../topics/vla/papers.md)） | [xiaomi-mlab/Minddrive](https://github.com/xiaomi-mlab/Minddrive) | 未落盘（main，2026-06-23 最后推送） | 335M | **完整发布 + 已源码核验**（[vla/verification.md §7.2](../topics/vla/verification.md)）：`adzoo/minddrive/`（`train.py` + 5 套 config + PPO 脚本）+ `mmcv/`（**VAD 系** mmdet3d 框架，含 `vad_utils/`）+ `rl_projects/`（CARLA 闭环 RL 基建）。实测：**完整 PPO**（`RLIterBasedRunner`，`clip_range=0.2` + 独立 `value_net` + GAE λ=1 + `kl_coef=0.5`）、**双 LoRA**（`action_expert`/`decision_expert`，RL 只训前者之外的决策侧）、**VAE+GRU**（`latent_dim=32`）、**7+6 meta-action**、奖励 **±1 来自 CARLA 事件**。270 stars |
| `Orion` | ORION（[VLA-15](../topics/vla/papers.md)） | [xiaomi-mlab/Orion](https://github.com/xiaomi-mlab/Orion) | 未落盘（main，2026-06-22 最后推送） | 452M | **完整发布 + 已源码核验**（[vla/verification.md §7.1](../topics/vla/verification.md)）：1 个 `EGO_WAYPOINT_TOKEN` → **VAE+GRU**（`latent_dim=32`、`N_GRU_BLOCKS=3`）→ **6 模态**；`num_memory=16`、`memory_len=600`。**但 7 个 stage 配置全部 `use_diff_decoder = False`** → 论文的 20 模态扩散消融**不可由已发布配置启用**。667 stars |
| `DMW` | Drive My Way（[VLA-17](../topics/vla/papers.md)） | [tasl-lab/DMW](https://github.com/tasl-lab/DMW) | 未落盘（main，2026-08-01 最后推送） | 353M | **关键部分未发布 + 已源码核验**（[vla/verification.md §7.3](../topics/vla/verification.md)）：README 目录树里 **`grpo/` 与 `checkpoints/` 都标 "to be released"，且全仓 14,508 个文件里确实没有 `grpo/`** → **论文的 GRPO 与奖励函数不可核验**。成立的部分：**50 个联合离散残差动作**（7 speed × 7 steer + 1 zero，`Categorical` 头 + 可学习温度）、speed 乘性 / steer 加性、下游 **PID**、基座 **SimLingo**。23 stars |
| `DiffVLA` | DiffVLA（[VLA-06](../topics/vla/papers.md) / DP-A27） | [boschresearch/DiffVLA](https://github.com/boschresearch/DiffVLA) | 未落盘（main，2025-12-08 最后推送） | ~44M | **⚠ 发布版与论文不同 + 已源码核验（第三十六轮 L3）**（[VLA-06 笔记 §代码核验](../topics/vla/notes/VLA-06-diffvla.md)、[sota-plan.md §7.6](../ideas/sota-plan.md)）：**README §5 自述"轨迹头已从 Diffusion Drive 换成自研 Transformer 头 + 引入 EPDM 子指标 reward loss"**，代码里活跃头是 `trajectory_head_reward.py`（**该目录内无任何扩散轨迹头文件**）；`RewardHead` 按 8 个 EPDM 子指标出 **BCE 头**（监督 = 离线 GT `pdm_scores_8192`），**推理期用手调权重 `argmax` 选一条** → **论文的 45.0 不可由发布代码复现**。`num_voc = 8192`（论文写 N_anchor = 32）；**`diffvla_data_exp/planning_vb/` 下 9 档锚点（32–8192）全部已发布**。36 stars / Apache-2.0；⚠ `DiffVLA/DiffVLA` 是**空壳**（0 KB） |
| `recogdrive` | ReCogDrive（[VLA-07](../topics/vla/papers.md) / DP-A28） | [xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive) | 未落盘（main，2026-09-22 最后推送） | — | **完整发布 + 已在研究对象侧源码核验**（[C003 §M](traces/diffusion_planner_code_traces-2.md)）：**611 stars / ICLR 2026**。**第三十六轮更正**：VLA-07 笔记此前记"论文未给仓库"，实际**仓库已发布**（论文正文确未给链接）→ 代码结论见 C003 §M（其 "DiffGRPO" 是**第六种"RL"**：有真 log-prob 与组内归一化优势、**无 ratio / 无 clip / 无 KL / 无 critic**；RL 阶段 **+4.3 PDMS**） |

> 注：`AutoVLA` 的 **commit 未取到**（clone/tarball 均被网络阻塞）。已核验的关键文件：`models/autovla.py`(30,526 B)、`models/action_tokenizer.py`(4,630 B)、`models/utils/score.py`(2,595 B)、`tools/run_rft.py`(7,058 B)、`tools/action_token/action_token_cluster.py`(8,519 B)、`dataset_utils/rft_dataset.py`(3,041 B)、`config/training/qwen2.5-vl-3B-nuplan-grpo-cot.yaml`(1,982 B)、`navsim/navsim/agents/autovla_agent.py`(19,707 B)、`codebook_cache/agent_vocab.pkl`(1,179,952 B)。**仓库元数据**：`created 2025-06-14` / `pushed 2026-05-29`，654 stars，默认分支 `main`。

## 已确认无官方代码（不下载）

| 论文 | 仓库 | 核实方式 |
|---|---|---|
| DiMA（DP-A33） | dotchen/DiMA | GitHub API 404 |
| PARA-Drive（CVPR'24） | OpenDriveLab/PARA-Drive | GitHub API 404 |
| GuideFlow（DP-A12） | — | 论文称 "code will be released"，GitHub 检索无结果 |
| RenderWorld（WM-22） | — | 2026-09-23 读全文并检索，**未见官方仓库**（第二十四轮） |
| Imagine-2-Drive（WM-23） | — | 论文与项目页均无代码入口（README 原文 "**Code coming soon!**"，第二十四轮） |
| [ChauffeurNet](../direction/notes/E2E-06-chauffeurnet.md)（2018）、PilotNet（2016）、ALVINN（1989） | — | 均无官方开源（时间早或工业界未开源） |

## 在列但**实际无代码 / 代码不全**（2026-09-23 克隆后核验）

| 目录 | 论文 | 实际情况 |
|---|---|---|
| `WorldRFT` | WorldRFT（WM-18） | **仓库为空**：仅 `LICENSE` + `readme.md`，readme 称代码 "soon" 上传 |
| `Hydra-MDP` | Hydra-MDP（E2E-05） | **零代码**：仅 `README.md` + 一张图；README 自述 "Delay in code and model release due to company policy" |
| `DriveVLM` | DriveVLM（E2E-10） | **零代码**：仅 `index.html` + `images/` + `DriveVLM.pdf`——**这是项目主页，不是代码仓库** |
| `Drive-WM` | Drive-WM（WM-01） | **代码范围不符**：仓库是 vendored `diffusers`，**不含论文的 tree-based planner 与 image reward** |
| `VAD`（`VADv2/`） | VADv2（E2E-03） | **部分发布**：只有 `VADv2_config_voca4096.py` + `VADv2_head.py`；README 明说要自行集成进 VADv1；`v116ADTRHead` 全仓未注册；**词表 `carla_plan_vocabulary_4096.npy` 未发布** |
| `imitation-learning` | CIL（CoRL'18） | 仅 5 个 `.py`，`.gitmodules` 为空，子模块未接入 |
| `Flow-Planner`（DP-A11，**未落盘**） | Flow Planner（NeurIPS 2025） | **网络阻塞但已用逐文件取证解决**：`git clone` 与 codeload tarball 均在约 4.5 MB 处稳定截断，**第二十四轮改用 GitHub trees API（1 次）+ `raw.githubusercontent.com`，把 72 个非图片文件全部取得**（字节数与树接口逐一对齐，`truncated=false`），**代码静态核验已完成**（[C003 §L](traces/diffusion_planner_code_traces-2.md)）。仓库 `size` 69669 KB / 271 stars / MIT / `pushed_at 2026-04-03`；代码全在 `flow_planner/` 下 |
| `DriveFine`（DP-A29） | DriveFine（arXiv 2602.14577） | **零代码**：全仓仅 `README.md` + `images/overview.png`；**GitHub API 确认只有 `main` 一个分支、单次提交**（`f44f86e`，`created 2026-02-16` / `pushed 2026-02-17`，此后无更新），README 的 News 里**没有任何"将发布代码"的条目** → **论文发布当天建的占位仓库**（见 [C003 §K](traces/diffusion_planner_code_traces-2.md)） |
| `DriveDreamer`（WM-21，未落盘） | DriveDreamer（ECCV'24） | **代码范围不符**：仓库只有图像/视频生成侧（Auto-DM + ActionFormer），**论文的"未来动作"规划脚本未见** → 与 Drive-WM 同类（第二十四轮读全文 + 检索后判定） |
| `DrivingGPT`（WM-12） | DrivingGPT（ICCV'25） | **宣称有码但未公开**：项目页指向 `RogerChern/DrivingGPT`，**该仓库不存在**（HTTP 000，作者仓库列表无此项）（第二十四轮） |
| `UniDrive-WM`（WM-13） | UniDrive-WM（ECCV'26） | **只有项目页**：仓库仅 `index.html` + `static/` 全静态资源，无代码（与 DriveVLM 同类）（第二十四轮） |
| `Raw2Drive`（WM-16） | Raw2Drive（NeurIPS'25） | **仅 `README.md`**：仓库 0 KB / 1 文件（与 WorldRFT 同类）（第二十四轮） |

> 这 **12 条**里，**前 9 条属于"论文声称有代码但实际没有、范围不符或未公开"**（WorldRFT、Hydra-MDP、DriveVLM、DriveFine、**Raw2Drive** 零代码或仅 README；Drive-WM、**DriveDreamer** 范围不符；**DrivingGPT 宣称有码但仓库不存在**；**UniDrive-WM 只有项目页**）——引用其机制主张时**必须标注"无代码可核验"**。另注：`DiffusionDrive`（v1）仓库内**没有** `kmeans_navsim_traj_20.npy`（配置里只有作者本机绝对路径）；`DiffusionDriveV2` 有 `16384.npy` 但缺 `gtrs_traj/navtrain_16384.pkl`。

## 下载方法（本轮生效的做法）

`git clone` 在本机对 GitHub 经常报 `gnutls_handshake() failed`，**多次重试可成功**。生效的组合是：

1. 每个仓库最多 8–10 次 `git clone --depth 1 --single-branch`，失败后 `sleep 6–8` 再试；**中途不删除**——失败就换个名字重试（`<name>.try2`）或跳过并记录，删除统一留到收尾（见 [inbox/cleanup.md](../../../inbox/cleanup.md)）；
2. 仍失败则用 `git ls-remote --symref <repo> HEAD` 取默认分支（不走 GitHub API，避免未认证额度耗尽），再 `curl https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/<branch>` 解压（tarball 无 commit，已在表中标注）；
3. **不存在的仓库会白耗时间**（每仓库约 2 分钟），务必先核实仓库存在再排队；
4. 注意：`pkill -f <脚本名>` 会误杀自己所在的 shell（命令行里含同一字符串），应用 PID 精确 kill。
5. **新发现（2026-09-23）**：`codeload` 在本机可能**在中途截断**——Flow Planner 的 tarball 稳定停在 4,493,317 字节（`gzip -t` 失败，重试 3 次同样大小）；**AutoVLA 同类**（两次尝试截断在 9,605,125 / 9,175,408 字节）。**判断方法**：下载后必须跑 `gzip -t` 校验，不能只看文件非空。此类截断不是重试能解决的，应记录为"网络阻塞"并停止。
6. **替代取证法（第二十一轮新增，网络阻塞时的兜底）**：`git clone` 与 tarball 都失败时，**用 GitHub API + raw 逐文件取证仍可完成代码级核验**——`curl https://api.github.com/repos/<owner>/<repo>/contents/<path>` 返回 base64，本地解码即可；同时用 `.../git/trees/<branch>?recursive=1` 拿全仓文件清单与体积（AutoVLA 就是这样核完 9 个关键文件的，含 1.18 MB 的 `agent_vocab.pkl`）。**代价**：拿不到 commit hash，需在表中注明。
   - **额度警告（第二十三轮实测）**：未认证的 GitHub API 只有 **60 次/小时**，**一轮多仓库核验很容易打满**（第二十三轮三个仓库核完即 60/60 用尽，之后连 `contents` 都返回失败）。→ **对策**：① 让每个子代理在本地缓存它抓到的文件（`/tmp/ai4r/<name>_probe/`），**主线程复核时直接读缓存、不再调 API**；② 需要重复读时改用 `raw.githubusercontent.com`（不计 API 额度）；③ 一次 `git/trees?recursive=1` 拿全清单，比逐目录列举省得多。

## F. 研究对象侧"代码可用性"全表核验后新发现、**尚未获取**的 6 个仓库（2026-09-23）

**动因**：此前只对**已克隆的 13 个仓库**做过逐文件核验，论文表里 34 篇 DP-A 中**未克隆的 21 篇从未查过代码可用性**。2026-09-23 用 3 个并行子代理补齐（**未克隆**，只查 arXiv 摘要页 / HTML 全文外链 / `raw`），结果 **34/34 核完**：**18 篇有代码 / 1 篇占位仓库 / 1 篇只有项目页 / 14 篇未找到官方代码**。下表是**此前记为"未见官方"或空白、实际有代码**的 6 个（按优先级排）。

| 目录名（建议） | 论文 / 编号 | 仓库 | 为什么值得拿 | 获取状态 |
|---|---|---|---|---|
| `recogdrive` | ReCogDrive（**DP-A28**） | [xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive) | **优先级最高，且已完成代码级核验**：NAVSIM 系自回归 VLM + 扩散规划器框架；**"DiffGRPO" 已核**（[C003 §M](traces/diffusion_planner_code_traces-2.md)）：有真 log-prob + 组内归一化优势 + 去噪步折扣 `0.6^k` + 真 PDM 奖励，**无 ratio/比率裁剪/KL/critic** → **第六种"RL"**；**RL 阶段净收益 +4.3 PDMS（Base 2B IL 86.5→RL 90.8）**；它是 **WM-11 DriveLaW 的 `ReCogDriveDiffusionPlanner` 的上游**。**口径冲突**：自报 90.8，FeaXDrive 表记 90.5。注意 README TODO 里 Bench2Drive/DriveLM/NAVSIM2.0/Drivebench 评测框架**未勾选** | **走 `raw` 逐文件取证，未克隆**（如需运行再克隆） |
| `GuideFlow` | GuideFlow（**DP-A12**） | [adept-thu/GuideFlow](https://github.com/adept-thu/GuideFlow) | **同基准 SOTA，且已完成代码级核验**（[C003 §N](traces/diffusion_planner_code_traces-2.md)）：navhard EPDMS **43.0**（同表 DiffusionDrive 24.2）；1513 个 blob。**三条机制里两条不在评测路径上**——评测侧 import `v6`（`navsim_test/` 只发布到 v6），而 **CVF 只在 v8、RFE 模块只在 v10** → 按仓库脚本直接跑会命中"无 CVF、无 RFE"的版本并撞上未定义的 `k_num`；`flow_matching.py` 是 11 字节占位文件。**陷阱**：arXiv 摘要指向的 `liulin815/GuideFlow` 是**占位**（README 原文 "We are currently organizing the code, coming soon"），真代码在此仓 | **走 `raw` 逐文件取证，未克隆** |
| `BridgeDrive` | BridgeDrive（**DP-A08**） | [shuliu-ethz/BridgeDrive](https://github.com/shuliu-ethz/BridgeDrive) | 扩散桥路线，Bench2Drive **DS 87.99 / SR 74.99**；README News 2026-03-09 已释放代码与训练/评测脚本，权重在 HuggingFace。**已代码级核验**（[C003 §O.2](traces/diffusion_planner_code_traces-2.md)）：桥核是真的（`x_T=anchor`/`x_0=traj` + DDBM VP-SDE 桥核），但**无 "Doob"/"PF-ODE" 字样**；**NAVSIM 侧 `step_num=20` 硬编码**、**锚点 yaml 指向作者机器绝对路径**（仓库内有同名文件需手改）、`ddbm_training` **声明了却被强制改写**；**两个数字本仓都不可闭环复现**（Bench2Drive 需外部指标模块、NAVSIM 权重不在仓内）。**"补丁式发布"**：需先 clone DiffusionDrive / LEAD | **走 `raw` 逐文件取证，未克隆** |
| `LCS` | Latent-Centroid Steering（**DP-A26**） | [codingmlinprocess/LCS](https://github.com/codingmlinprocess/LCS) | 单次前向的潜质心引导（替代两次前向的 CFG）；约 495 个 `.py`，含 **Bench2Drive leaderboard + SimLingo 训练/评测脚本**，README 给 HuggingFace checkpoint。**已代码级核验**（[C003 §O.1](traces/diffusion_planner_code_traces-2.md)）：**"单次前向"是真的少一次模型调用**（无 `torch.cat([cond,uncond])` 式批拼接），代之以**离线方向向量**（`mean_shift_scale=0.1`）；**但代码里无任何 FPS/FLOPs**；`use_cfg_latent` **声明未接线**、`use_mean_shift_cfg` **无法关**、`mean_shift_deltas_path` 是**相对路径**（cwd 不对时引导静默关闭） | **走 `raw` 逐文件取证，未克隆** |
| `MPDiffuser` | MPDiffuser（**DP-A23**，通用离线控制域） | [haldunbalim/MPDiffuser](https://github.com/haldunbalim/MPDiffuser) | 让动力学模型参与去噪（非梯度）把可行性注入生成过程；`mpdiffuser/` 包 + `scripts/train.py` + `scripts/test.py`。**已代码级核验**（[C003 §P.1](traces/diffusion_planner_code_traces-2.md)）：**机制是真的**（学出来的扩散动力学 + 每一步替换状态子块，`use_pmean_var=False` 硬编码），**但仓库是 JAX/Flax、三个入口里两个坏**（`Planner` 的嵌套 `sample_step` 调不存在的 `self.sample_step`；`GuidedSampler` 无 `sample_step`）、**无权重无数据无结果表** | **走 `raw` 逐文件取证，未克隆** |
| `dipole-rl` | DIPOLE（**DP-A17**，通用决策域） | [Whiterrrrr/dipole-rl](https://github.com/Whiterrrrr/dipole-rl) | "扩散策略如何被 RL 稳定训练"的算法层结论；**注意主仓 [LRMbbj/DIPOLE](https://github.com/LRMbbj/DIPOLE) 是占位**（README "Quick Start Comming soon."），真代码在本仓（主仓的 git submodule；**默认分支 `master`**）。**已代码级核验**（[C003 §P.2](traces/diffusion_planner_code_traces-2.md)）：**RL 实为 IQL + 有界优势加权 flow 回归（RWR）**，**无 log_prob / 无比率 / 无 clip / 无 KL**，但**有 critic 与 value**；"稳定训练"靠**有界 sigmoid 权重**替代 `exp(α·adv)` + Q 集成取 min + Polyak 目标网；**自称与代码自洽**（从不称 GRPO）。**NavSim 结果表在 README 里但无对应代码** | **走 `raw` 逐文件取证，未克隆** |

**另有 2 条"有仓库但无代码"的负面确认**（避免重复踩坑）：**DP-A29 DriveFine** 是占位仓库（只有 `README.md` + 一张图）；**DP-A15** 的 `MarcelloCeresini/DirectControlFlowMatching` 里只有 GitHub Pages 站点源码 `docs/index.html`（无 `.py`、无 README）。

## 下一步（尚未执行）

1. 确认运行前置条件：Python/CUDA 版本、数据与权重下载入口、单卡显存需求。
2. 代码脉络分析已完成，见同目录三份文件：
   - [traces/diffusion_planner_code_traces.md](traces/diffusion_planner_code_traces.md)（扩散规划器侧：主张—代码对照 11 项 + 组合关系 7 项 + 实现细节 8 项 + 判断 3 条）；
   - [traces/world_model_code_traces.md](traces/world_model_code_traces.md)（世界模型→规划器接口：对照 9 项 + 组合关系 8 项 + 实现细节 7 项 + 负面发现 2 项）；
   - [traces/e2e_trunk_code_traces.md](traces/e2e_trunk_code_traces.md)（E2E 主干：完整性核验 13 个 + 主张对照 5 项 + **「轨迹词表/锚点」谱系 5 环** + 实现细节 7 项）。
3. **词表重建**：**⚠ 本条已于 2026-09-24 第三十六轮更正**——原文写"VADv2 的 4096 词表与 DiffusionDrive 的 20 锚点**都不在公开仓库里**，复现基线前必须先解决词表重建"，但 [C005 §H/§H.3](traces/e2e_trunk_code_traces.md) 的实测（GitHub Releases API + 实际下载 + 内容实测）**已推翻这句话**：**DiffusionDrive 的 20 锚点公开可得**（Release 资产，实测形状 **(20,8,2)**，与 V2 仓库内同名文件**逐字节相同**）、SparseDrive 的四个 `kmeans_*.npy` 与 UniAD 的 `motion_anchor_infos_mode6.pkl` 也都能下载；**唯一真不可得的只剩 VADv2 的 `carla_plan_vocabulary_4096.npy`**（构造线索已明确）。→ 资源估算请用 [state.md](../state.md) 待续清单第 10 项的口径，**不要再用本条原文**。
4. **navhard 侧的两个"对手 / 工具"仓库**（**第三十七轮新增**，均为 L3 核验、**未克隆**；结论见 [sota-plan.md §7.7](../ideas/sota-plan.md)）：
   - **[OpenDriveLab/SimScale](https://github.com/OpenDriveLab/SimScale)**（327★ / Apache-2.0 / 2026-09-18 最后推送 / ~22 MB）——**不是规划器，是模型无关的 sim-real co-training 框架**。**路线 ③ 的载体**：仓库里**已有 `navsim/planning/script/config/common/agent/diffusiondrive_agent.yaml`**，且 HF 上发布了 **`diffusiondrive_sim_navhard.ckpt`**（navhard **32.6**；**第五十六轮定位到精确路径**：在 **HF `datasets`** 仓库 `datasets/OpenDriveLab/SimScale` 的 `SimScale_ckpts/DiffusionDrive/` 下，**不在 `models` 仓库**，**243.6 MB 可下载**，实测 HTTP 200；同数据集共 **12 个 ckpt**）→ **用我们选定的起点（DiffusionDrive）跑它的 ckpt 只需推理、不需训练**。⚠ **它自己报告的最高分是 48.0**（论文原文 "establishing a new SOTA on navhard"），**DriveFuture 表里的 53.2 在它论文全文里查不到**。
   - **[NVlabs/GTRS](https://github.com/NVlabs/GTRS)**（288★ / Apache-2.0 / 2026-02-09 最后推送 / ~13 MB）——**四个 checkpoint 全部在 HF**（`gtrs_dp.ckpt` 25.6 / `gtrs_dense_vov.ckpt` **41.7** / `gtrs_aug_vov.ckpt` **42.1** / `hydra_mdp_vov.ckpt` 37.5，**都是 V2-99 骨干**）。⚠ **它的 49.4（GTRS-E）是"六个模型的集成"，而六个里只发布了 2 个**（即上面两个 V2-99 的）→ **49.4 不可复现**；**可复现单模最高 42.1**，**最佳单模 45.3（GTRS-Dense + ViT-L）未发布**。
