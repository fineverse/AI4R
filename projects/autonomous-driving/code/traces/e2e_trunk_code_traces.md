# E2E 主干代码脉络（主张 → 代码）

更新时间：2026-09-23  
证据等级：**代码静态检查**（已克隆仓库，读文件与配置，**未安装依赖、未运行**）。仓库清单与 commit 见 [repositories.md](../repositories.md)。  
**核验级别（定义见 [ai/rules.md §代码静态检查](../../../../ai/rules.md)）**：本册 §A–§J 覆盖的 **13 个主干仓库全部为 L1 逐文件核验**（已克隆）；其中 **Hydra-MDP 与 DriveVLM 为 L2**（仓库存在但零 `.py`）。第二册 §K–§M 为重建版（内容取自同一批 L1 记录）。  
读法：本文件回答三关系中的两条——**组合关系**（模块来自哪篇论文）与**主张—代码关系**（论文卖点对应哪些文件）。本文件只覆盖**领域级 E2E 主干**（13 个仓库）；研究对象侧见 [diffusion_planner_code_traces.md](diffusion_planner_code_traces.md)，世界模型侧见 [world_model_code_traces.md](world_model_code_traces.md)。  
本文件规模：仓库完整性核验 **13 个**、主张—代码对照 **5 项**、谱系 **1 条 5 环**、实现细节 **7 项**、待核验 5 项（原第 3 项已由 §H 解决）、判断 3 条，另有 **§G 非生成式基线的规划头对照**（UniAD / SparseDrive / VAD v1 / VADv2 的输出模态数与选优机制）、**§H 锚点/词表文件的公开渠道核验**（逐文件实测下载与形状比对；顺带更正 DIVER 的候选数口径；**§H.4 第二十四轮复查把"两个空洞"改成"一个 30.5 GB 的成本问题 + 一个 CARLA 数据问题"**）、**§I 「特权信息三段式」的代码级核验**（六家的推理期输入权限清单）、**§J GenAD**（"生成式但非扩散"的第二条路线：32 维对角高斯隐变量 + spatial GRU + 解析 KL，无词表）与 **§K CARLA 系 6 个基线的规划/控制输出**（把 §G 的对照表补全到 13 个仓库；发现 **ST-P3 早在 ECCV'22 就用"预测占据 → cost → `topk` 选优"**）、**§L TransFuser / TCP / ST-P3 的主张—代码对照**（补 §B：发现 **TransFuser 的 `loss_velocity`/`loss_brake` 权重为 0**、**`n_layer` 两套默认值冲突**、**ST-P3 的 "dual attention" 实为双 GRU 门控混合**、**ST-P3 官方配置关掉两个头**）、**§M LBC / CIL / NEAT / DriveLM 的主张—代码对照**（发现 **NEAT 的 attention 是真 QKV（与 ST-P3 形成正反对照）**、**LBC 的蒸馏是输出级 L1 而非特征回归**、**CIL 的 `input_control` 定义后从未被喂入**、**DriveLM 仓库内无 FPS 代码且 `lineage.md` 的 0.16 FPS 与本仓数字不一致**）。


**本文件的核心问题**：这些"有官方代码"的主干工作，代码**真的在**吗？以及——**"轨迹词表 + 选优"这条机制线在代码层是怎么传下来的**？

## A. 仓库完整性核验（13 个 E2E 主干全扫）

方法：统计每个仓库的 `.py` 文件数与顶层内容（排除 `.git`）。

| 目录 | `.py` 数 | 实际内容 | 结论 |
|---|---|---|---|
| `UniAD` | 122 | `projects/`、`tools/`、`docs/`、`docker/` | **代码完整** |
| `VAD` | 172 | v1 完整（`projects/mmdet3d_plugin/{bevformer,core,datasets,models,VAD}`）；`VADv2/` **只有 2 个文件** | **v1 完整；v2 部分发布**（见 §B） |
| `SparseDrive` | 75 | `projects/`、`tools/`、`scripts/`、`resources/` | **代码完整** |
| `Hydra-MDP` | **0** | 仅 `README.md` + `asset/hydra-mdp.png`（2.5 M 几乎全是图） | **零代码**：README 原文 "Delay in code and model release due to company policy. Stay tuned for updates." |
| `TCP` | 140 | `TCP/`、`roach/`、`scenario_runner/`、`leaderboard/` | **代码完整**（含 CARLA 侧） |
| `ST-P3` | 27 | `stp3/`、`carla_agent.py`、`evaluate.py`、`scripts/` | **代码完整**（规模本就较小） |
| `neat` | 140 | `aim_mt_2d/`、`aim_mt_bev/`、`aim_va/`、`neat/` | **代码完整** |
| `imitation-learning` | 5 | `run_CIL.py`、`agents/imitation/`；`.gitmodules` **为空** | **代码偏少**，子模块未接入 |
| `LearningByCheating` | 63 | `bird_view/`、`data_collector.py`、`benchmark*/` | **代码完整** |
| `DriveVLM` | **0** | 仅 `index.html`、`index_old.html`、`images/`、`DriveVLM.pdf` | **零代码**：这是**项目主页**，不是代码仓库（52 M 全是图片与 PDF） |
| `transfuser` | 133 | `team_code_transfuser/`、`leaderboard/`、`results/` | **代码完整** |
| `GenAD` | 848 | `projects/`、`tools/`、`closed-loop/`、`docs/` | **代码完整**（规模最大）。**已逐文件核验，见 §J**：基于 VAD 代码库；生成机制是 **32 维对角高斯隐变量 + spatial GRU + 解析 KL**（CVAE 式，**非扩散、无词表**） |
| `DriveLM` | 23 | `challenge/`、`docs/`、`assets/`、`environment.yml` | **以数据/文档为主**，代码为挑战赛工具 |

**两处必须更正的记录**：

1. **Hydra-MDP 的官方仓库零代码**。它是"多教师多目标蒸馏 + 轨迹词表"这一机制线的**命名来源**，但 `README` 自述因公司政策延迟发布，截至 2026-09-23 仍只有 README。
2. **DriveVLM 的官方仓库是项目主页**（HTML + 图片 + PDF），**无任何实现代码**。原先把它列在"官方代码仓库快照"里是错的。

> 影响：这两条都是**引用链上的关键节点**。Hydra-MDP 是 NAVSIM 挑战赛第 1 名、被反复对比；DriveVLM 是 VLA 支线的早期代表。二者都**无法做代码级核验**，其机制主张只能停留在"论文自述"级。

## B. 主张—代码对照

| 论文 | 论文主张 | 代码证据（文件 / 类 / 配置） | 一致性判断 |
|---|---|---|---|
| **VAD**（E2E-02） | 全向量化表征；**单模态**规划输出 | `projects/mmdet3d_plugin/VAD/VAD_head.py:405`：**`self.ego_query = nn.Embedding(1, self.embed_dims)`**（1 条 ego query）；`loss_plan_reg` 为 `L1Loss`（`VAD_base_e2e.py:287` 权重 **1.0**，head 默认 0.25） | **一致**：VAD v1 是**单模轨迹回归**，无词表、无锚点 |
| **VADv2**（E2E-03） | 规划输出为**动作词表上的概率分布**，默认 **N=4096**，推理取最高概率动作；3 s / 6 waypoint / 0.5 s 间隔 | `VADv2/VADv2_config_voca4096.py`：`plan_fut_mode=256`（训练）、`plan_fut_mode_testing=4096`、`valid_fut_ts=6`、`plan_anchors_path='carla_plan_vocabulary_4096.npy'`；`VADv2/VADv2_head.py:204` `self.plan_anchors = np.load(plan_anchors_path)`；`:940` `Dt = 0.5` | **一致，且更彻底**：见下方"回归被乘 0"一条 |
| **VADv2** | 损失 = IL（KL/交叉熵）+ 冲突项 + token 项 | `VADv2_config_voca4096.py`：**`loss_plan_cls_expert` 权重 200.0**（唯一被放大的规划损失）；`loss_plan_cls_col` / `_bd` / `_cl` / `loss_plan_reg` / `loss_plan_bound` / `loss_plan_agent_dis` / `loss_plan_map_theta` **权重全为 0.0** | **需修正印象**：在**已发布的这份配置里**，冲突项与回归项**全部被关闭**，规划只靠"专家分类"一项监督 |
| **DiffusionDrive**（DP-A02） | 截断扩散 + **K-means 锚点先验** | `navsim/agents/diffusiondrive/transfuser_model_v2.py:407` `plan_anchor = np.load(plan_anchor_path)`；`transfuser_config.py:19` 默认值是一个**作者本机绝对路径**（`/home/users/bencheng.liao/.../kmeans_navsim_traj_20.npy`） | **一致**；但**v1 仓库内没有这个 `.npy`**（见 §D） |
| **DiffusionDriveV2**（DP-A03） | 两阶段（RL 约束 + mode selector） | `diffusiondrivev2_model_sel.py:929-930`：`vocab_pdm_gt_path='gtrs_traj/navtrain_16384.pkl'`、`vocab_path='gtrs_traj/16384.npy'`；仓库内**只有 `16384.npy`，`.pkl` 缺失** | **部分一致**：词表本体在，**PDM 子分数表不在**（见 §D） |

## C. 「轨迹词表 / 锚点」机制的代码谱系（本项目最重要的一条线）

这是本项目研究对象（扩散规划器）**真正的前身线**。五个环节的代码级证据：

| 环 | 工作 | 词表 | 词表怎么用 | 代码证据 |
|---|---|---|---|---|
| ① | **VAD**（ICCV'23） | **无** | 单模轨迹回归 | `ego_query = nn.Embedding(1, ...)`；`loss_plan_reg` 权重 1.0 |
| ② | **VADv2**（ICLR'26） | **4096**（`carla_plan_vocabulary_4096.npy`，CARLA） | **纯分类**：从 4096 条里选概率最高的一条；**轨迹就是那条锚点，回归分支被乘 0 丢弃** | `used_plan_anchors` → `pos2posemb2d` → ego_query；`outputs_ego_trajs = outputs_ego_trajs * 0. + self.used_plan_anchors[None]` |
| ③ | **Hydra-MDP**（CVPR'24 挑战赛第 1） | 4096 / 8192 | 多教师多目标蒸馏到词表分数上 | **代码未公开**（§A）——此环**只能凭论文** |
| ④ | **DiffusionDrive**（CVPR'25） | **20**（K-means 聚类 NAVSIM 轨迹） | 词表当**扩散先验**：在锚点上加极低噪声再 2 步去噪 | `plan_anchor_path` / `kmeans_navsim_traj_20.npy` |
| ⑤ | **DiffusionDriveV2** | **16384**（40 waypoint） | 词表**与扩散采样结果拼进同一候选池**，由 scorer 选优 | `torch.cat((diffusion_output, vocab), dim=1)` |

**这条线的读法**：

- 环节 ①② 说明**"多模态候选 + 先验词表"不是扩散带来的**——2024 年初的 VADv2 就已成立，而且比后来的扩散方案**更彻底**（连回归都不要）。
- 环节 ④ 才是扩散的介入点：**词表从"被选择的答案集"变成"生成的起点"**（锚点 + 极低噪声 = 截断扩散）。
- 环节 ⑤ 是**回退**：词表重新变成"被选择的答案集"，而且这次和扩散输出**混在一起**被同一个 scorer 评判。
- 因此"扩散规划器"这条线的**独特性只在环节 ④ 成立**：一旦进入"词表 + 选优"，扩散生成器的贡献就无法从分数里分离出来。

## D. 关键实现细节（本轮静态核验已解决）

| 问题 | 结论 | 证据 |
|---|---|---|
| VADv2 的**回归分支到底有没有用** | **没有**。`outputs_ego_trajs = self.plan_reg_branch(ego_feats)` 算出来后，下一行被 `outputs_ego_trajs * 0. + self.used_plan_anchors[None]` **整体替换为锚点**——回归输出被乘 0 丢弃。规划输出**只能是词表里的一条** | `VADv2_head.py:1112-1119` |
| VADv2 训练时用多少条锚点 | **256 条**（`plan_fut_mode=256`），从 4096 条里 **`torch.multinomial(..., replacement=False)` 随机采样**；且**把 GT 最近的锚点强行塞进这批**（`used_index[-1] = best_match_idx`，`best_match_idx` 由 `cumsum` 后的 L2 距离 `argmin` 得到） | `VADv2_head.py:945-956` |
| VADv2 的"运动学掩码"有效吗 | **无效**。`kinodynamic_mask = (norm(anchors[:,0,:]) - pred_dis).abs() < 100000000000`——阈值 **1e11**，等价于"全部通过"，看起来是被禁用的遗留代码 | `VADv2_head.py:944-946` |
| VADv2 的 ego query 从哪来 | 从**锚点位置编码**来：`pos2posemb2d(used_plan_anchors.reshape(...))` → `ego_query_pre_branch`。**不是可学习的 `nn.Embedding`**（那行被注释掉了） | `VADv2_head.py:455-457`（注释）、`964-969` |
| VADv2 的停车轨迹如何处理 | 把位移接近 0 的锚点**强制置零**，并**固定 `used_plan_anchors[0] = 0.`**（即词表第 0 条永远是"停住"） | `VADv2_head.py:960-962` |
| VADv2 发布了什么 | README 原文："**Core code of VADv2 (config and model) is available in the `VADv2` folder. Easy to integrate it into the VADv1 framework**"——即**只发布 config + head 两个文件**，需自行接进 v1；且 `VADv2_config_voca4096.py` 声明的 `type='v116ADTR'` / `v116ADTRHead` **在整个仓库里没有任何注册**，开箱不可运行 | `VAD/README.md`、`grep v116ADTRHead` 无结果 |
| 词表文件是否随仓库发布 | **多数不在仓库树里，但多数有公开下载渠道**（本轮逐渠道核验见 **§H**）：`VAD` 全仓 **0 个 `.npy`**（`carla_plan_vocabulary_4096.npy` 缺失，且 `hustvl/VAD` **无 release**）→ **唯一真正不可得**；`DiffusionDrive`（v1）全仓 0 个 `.npy`，但官方 **Release 资产**里有 `kmeans_navsim_traj_20.npy`（**已下载实测：2688 B，(20,8,2) float64**）；`DiffusionDriveV2` 仓库树内有 `kmeans_navsim_traj_20.npy` 与 `gtrs_traj/16384.npy`（**(16384, 40, 3)** float32，由文件字节数 7,864,448 = 16384×40×3×4 + 128 头确认），但 `gtrs_traj/navtrain_16384.pkl` **缺失**；SparseDrive / UniAD 的锚点文件也均有公开渠道（§H） | 各仓库 `find *.npy` + **GitHub Releases API + 实际下载核验** |

## E. 仍然待核验（需要运行环境或更多阅读）

1. **Hydra-MDP 与 DriveVLM 无法做代码级核验**（仓库零代码），其机制主张停留在论文自述级。
2. **VADv2 无法开箱运行**：`v116ADTRHead` 未注册、词表 `.npy` 未发布——要复现需先自行重建 4096 词表（论文未给构造脚本）。
3. ~~**DiffusionDrive 的 20 条锚点无法本地重建**：v1 仓库无 `.npy`，只有作者本机路径；V2 仓库内的同名文件是否与 v1 一致**未核验**。~~ **已解决（§H.1）**：v1 的官方 Release 资产里就有该文件，**已下载并与 V2 仓库内文件逐字节比对，完全相同**。
4. 所有论文的**指标数字**都必须实际运行才能验证——静态检查只能确认"代码里有对应实现"，不能确认"实现了论文声称的效果"。
5. **`gtrs_traj/navtrain_16384.pkl`（DiffusionDriveV2 的 PDM 子分数表）仍缺失**，且四个 Releases 渠道都没有（§H.1 表）。

## F. 由本轮代码核验得出的三条判断

1. **"有官方代码"这条记录本身不可靠，必须逐个核验**。本轮在 13 个主干仓库里查出 **2 个零代码**（Hydra-MDP、DriveVLM）；在研究对象侧查出 2 个（WorldRFT 为空、Drive-WM 不含规划器）；在借鉴来源侧查出 VADv2 为**部分发布**。→ **repositories.md 的"选择标准：论文有官方代码"应改成"论文声称有官方代码，且已核验代码存在"**，并把核验结果写进表里。
2. **"轨迹词表 + 选优"是一条比扩散更早、更强的线**。VADv2（2024-02）已用 4096 条词表做纯分类、**连回归都不要**；Hydra-MDP 沿用；DiffusionDrive 才把词表改成扩散起点；V2 又退回"词表 + 选优"。→ 研究对象若要做"扩散规划器"，必须回答"**在词表已经能选到 89.3 分的情况下，扩散生成带来的是什么**"——这是 [preparation.md](../../ideas/preparation.md) 里那条核心对照的代码级版本。
3. **两个关键节点的词表文件都不在公开仓库里**（VADv2 的 4096、DiffusionDrive 的 20）。→ 任何"复现基线再比较"的计划都**必须先解决词表重建**，否则连基线都跑不起来。这一条直接影响实验协议的资源估算。

## G. 非生成式基线的规划头：输出模态数与选优机制

**动因**：本工作空间把"**非生成式基线不低于 DiffusionDrive**"当作核心对照，但从没在代码层确认过——这些基线**到底输出几条轨迹**、**有没有选优**、**损失结构是什么**。本节把 UniAD 与 SparseDrive 两个最具代表性的 nuScenes 基线拆到规划头一级。

| 项 | **UniAD**（CVPR'23 最佳论文，E2E-01） | **SparseDrive**（E2E-04） | VAD v1（E2E-02） | VADv2（E2E-03） |
|---|---|---|---|---|
| 规划头类 | `PlanningHeadSingleMode` | `MotionPlanningHead` + `MotionPlanningRefinementModule` | `VADHead` | `VADv2Head` |
| **输出模态数** | **1** | **18 = 3 命令 × 6 模态** | 1 | 4096（推理）/ 256（训练） |
| 单模是**代码强制**还是论文简化 | **代码强制**：`self.mlp_fuser(plan_query).max(1, keepdim=True)[0]` 在候选 query 维上做 **max-pool**，P→1 | 非单模 | `self.ego_query = nn.Embedding(1, embed_dims)` | 非单模 |
| 输出形式 | `(-1, 6, 2)` 6 步**累积位移**（`torch.cumsum(..., dim=1)`） | 6 步位移 → decode 时 `cumsum` | 6 步位移 | **词表锚点**（回归被乘 0） |
| 锚点 / 词表 | **无** | `kmeans_plan_6.npy`，**仅作 query 初始化** | 无 | 4096 词表 = **输出答案集** |
| 导航命令 | `nn.Embedding(3, embed_dims)`；**eval 用 GT 命令** | 3 命令分组；`data['gt_ego_fut_cmd'].argmax(dim=-1)` **eval 也用 GT** | 3 命令 | 3 命令 |
| 选优机制 | 无（单模） | 分层：① GT 命令选组 → ② `plan_cls.argmax` 选模态 → ③ 碰撞 rescore | 无 | `argmax` |
| 碰撞后处理 | **默认开启**：`use_col_optim=True` → 测试时 CasADi `CollisionNonlinearOptimizer`（`occ_filter_range=5.0`、`sigma=1.0`、`alpha_collision=5.0`） | `use_rescore=True` → `plan_cls + col.float() * -999`（**非优化，直接扣分**） | 无 | 冲突损失（已发布配置里权重 **0.0**） |
| 规划损失 | `PlanningLoss` = masked **ADE**；`CollisionLoss` 三档 `delta=0.0/0.5/1.0`，权重 2.5/1.0/0.25 | cls `FocalLoss(0.5)` + reg `L1Loss(1.0)`（**仅 best mode**，赢家通吃）+ status `L1Loss(1.0)` | `loss_plan_reg` `L1Loss(1.0)` | `loss_plan_cls_expert` **200.0**，其余全 0.0 |
| 规划视野 | 6 步 = **3 s @2 Hz** | 6 步 = **3 s @2 Hz** | 同 | 同（`valid_fut_ts=6`） |

**证据位置**：`UniAD/projects/mmdet3d_plugin/uniad/dense_heads/planning_head.py`、`UniAD/projects/mmdet3d_plugin/losses/planning_loss.py`、`UniAD/projects/configs/stage2_e2e/base_e2e.py`、`SparseDrive/projects/mmdet3d_plugin/models/motion/{motion_planning_head,motion_blocks,decoder,target}.py`、`SparseDrive/projects/configs/sparsedrive_small_stage2.py`、`SparseDrive/tools/kmeans/kmeans_plan.py`、`SparseDrive/projects/mmdet3d_plugin/datasets/evaluation/planning/planning_eval.py`。

### G.1 七条必须记住的代码级事实

1. **UniAD 的"单模"是代码强制的**。[planning_head.py](../repos/UniAD/projects/mmdet3d_plugin/uniad/dense_heads/planning_head.py) 里先构造 P 个候选 query（`sdc_traj_query` + `sdc_track_query` + `navi_embed` 拼接后过 `mlp_fuser`），紧接着在候选维上做 **max-pool** 压成 1 个。类名直接叫 `PlanningHeadSingleMode`。→ **在"非生成式基线"里，UniAD 连多模态候选都不输出**，任何"多模态"对比对它都不适用。

2. **UniAD 的默认配置带一个"测试时优化"组件**。`base_e2e.py:57 use_col_optim = True`（**默认开**），测试时调用 `CollisionNonlinearOptimizer`——用 CasADi 在占用栅格约束下对轨迹做非线性优化。训练侧的 `CollisionLoss` 则用 `inter_bbox` 做**轴对齐包围盒相交**近似（`to_corners` 虽然算了旋转矩阵，但 `inter_bbox` 只取 min/max，旋转被丢弃）。→ **UniAD 的公开数字里含后处理优化**，复现基线时必须对齐这个开关，否则不是同一个系统。

3. **SparseDrive 的 18 提案 = 3 命令 × 6 模态，且命令是 GT 输入**。[motion_blocks.py](../repos/SparseDrive/projects/mmdet3d_plugin/models/motion/motion_blocks.py) 把 `plan_reg_branch` 输出 reshape 成 `(bs, 1, 3 * ego_fut_mode, ego_fut_ts, 2)`，`ego_fut_mode=6`（[sparsedrive_small_stage2.py:62](../repos/SparseDrive/projects/configs/sparsedrive_small_stage2.py#L62)）→ **18 条**；[decoder.py](../repos/SparseDrive/projects/mmdet3d_plugin/models/motion/decoder.py) 的 `HierarchicalPlanningDecoder.decode` 同样 reshape 成 `(bs, 3, 6, 6, 2)`。`decode` 与 `PlanningTarget.sample` **都用 `data['gt_ego_fut_cmd'].argmax(dim=-1)` 选命令组** → **命令是评测输入，不是预测目标**（与 UniAD 的 `navi_embed(3)` 同类）。

4. **SparseDrive 的"分层选优"第二层是事后碰撞扣分，不是学到的 scorer**。`rescore` 里 `score_offset = col.float() * -999; plan_cls = plan_cls + score_offset`；碰撞判定用 `corners_in_box`（**角点落在对方框内的近似**）；只对 `det_confidence ≥ score_thresh=0.5` 的智能体生效；只用 **top-1 运动模态**（`num_motion_mode=1`）；且**当 6 个模态全部碰撞时不做任何惩罚**（`col[all_col] = False`，注释原文 "for case that all modes collide, no need to rescore"）。车身尺寸硬编码 `[4.08, 1.73, 1.56] × dim_scale=1.1`。→ 与 DiffusionDriveV2 的**学到的 mode selector** 不是一回事，做对照时必须区分"**学到的选优**"与"**事后规则扣分**"。

5. **SparseDrive 的锚点是"query 初始化"，不是"输出答案集"**。[kmeans_plan.py](../repos/SparseDrive/tools/kmeans/kmeans_plan.py)（`K=6`）对 **GT 累积轨迹按命令分组**（`navi_trajs = [[], [], []]`）做 KMeans，存成 `(3, 6, 6, 2)` 的 `kmeans_plan_6.npy`；head 里只用于 `plan_mode_query = self.plan_anchor_encoder(gen_sineembed_for_position(plan_anchor[..., -1, :]))`。**输出仍是 MLP 回归**（`plan_reg_branch` → `ego_fut_ts * 2`）。→ 这是「轨迹词表 / 锚点」的**第四种用法**：① VADv2 = 输出答案集；② DiffusionDrive = 扩散起点；③ DiffusionDriveV2 = 候选池成员；④ **SparseDrive = query 初始化**。

6. **SparseDrive 的训练侧 rescore 与评测侧碰撞口径不一致**。评测 [planning_eval.py](../repos/SparseDrive/projects/mmdet3d_plugin/datasets/evaluation/planning/planning_eval.py) 用 `shapely Polygon.intersects`（**精确多边形相交**）+ 车身 `4.084 × 1.85` + "follow uniad" 的 **+0.5 m 纵向偏移**；训练侧 rescore 用**角点近似** + 车身 `4.08 × 1.73 × 1.1`。→ **rescore 的代理指标 ≠ 评测指标**，"rescore 提升"不等于"碰撞率下降"。

7. **nuScenes 系的规划视野统一是 3 s / 6 步**（UniAD `planning_steps=6`、SparseDrive `ego_fut_ts=6`、VADv2 `valid_fut_ts=6`，均 @2 Hz），与 NAVSIM 系的 **4.0 s / 8 poses** 不同。→ **跨基准的规划数字本来就不该直接比**，这条与 [diffusion_planner_code_traces.md](diffusion_planner_code_traces.md) §F 的 `tf_d_model` / `lidar_seq_len` 一起构成"对齐清单"。

### G.2 对"生成式 vs 非生成式"对照的影响

把 §G.1 与 §C 合起来看，**"非生成式基线"这个词其实覆盖了三种完全不同的系统**：

| 类别 | 代表 | 候选来源 | 最终输出 | 后处理 |
|---|---|---|---|---|
| 纯单模回归 | UniAD、VAD v1 | 无候选 | 1 条 | 测试时非线性优化（UniAD） |
| 先验锚点 + 回归 | SparseDrive | 18 条（3 命令 × 6 模态） | 1 条（cls argmax） | 碰撞规则扣分 |
| 离散词表 + 分类 | VADv2、Hydra-MDP | 4096 / 8192 条 | 1 条（argmax） | 无 |

→ 因此"非生成式基线不低于 DiffusionDrive"这句话**必须指定是哪一个**：UniAD/VAD v1 是**真单模**，拿它当"非生成式"代表会低估基线；**真正的对手是 VADv2 与 Hydra-MDP 这一类的"离散词表 + 分类"**，而它们恰好是 DiffusionDrive 的直接前身（§C 环节 ②③）。这一条直接收窄了 [preparation.md](../../ideas/preparation.md) 里那条核心对照的可选范围。

## H. 锚点 / 词表文件的公开渠道核验——"必须先重建词表"这个阻塞大半不存在

**动因**：§D 与 §E 一直记着一条硬阻塞——"**两个关键词表文件都不在公开仓库里，复现基线前必须先解决词表重建**"，并据此写进了 [state.md](../../state.md) 的待续清单与 [preparation.md](../../ideas/preparation.md) 的资源估算。但"不在仓库树里"≠"不可得"：本轮改用 **GitHub Releases API + 实际下载 + 内容实测** 三条证据重查，结论是**这个阻塞被大幅高估**。

### H.1 逐文件核验（全部为实测，非推断）

| 文件 | 谁需要它 / 期望形状 | 公开渠道 | 实测结果 |
|---|---|---|---|
| `kmeans_navsim_traj_20.npy` | **DiffusionDrive v1**（`transfuser_model_v2.py:407` `np.load` 后断言 **(20,8,2)**） | v1 仓库**无**（配置里只有作者本机绝对路径），但 `docs/train_eval.md:13` 指向官方 **Release 资产**：`hustvl/DiffusionDrive` → tag `DiffusionDrive_88p1_PDMS_Eval_file` | **已下载**：2,688 B，**shape (20,8,2)、float64**，md5 `0378349a47b896b96c3f1bc8f7eb156d`；**与 `DiffusionDriveV2` 仓库树内的同名文件逐字节相同**（`bytes identical: True`）→ **§E 第 3 项解决**；该资产已有 **4,148 次下载** |
| `kmeans_plan_6.npy` | **SparseDrive**（`sparsedrive_small_stage1/2.py:406` `plan_anchor=`）——`ego_fut_mode=6`，期望 **(3,6,6,2)** | SparseDrive 自己的 Release（tag `v1.0`）**只有权重与日志，没有锚点**；但 `hustvl/DiffusionDrive` 的 tag **`DiffusionDrive_nuScenes`** 里有一整套。直链形如 `https://github.com/hustvl/DiffusionDrive/releases/download/DiffusionDrive_nuScenes/<文件名>`（本轮实测该 URL 可下载） | **已下载**：992 B，**shape (3,6,6,2)、float32** → **与 SparseDrive 期望一致**。同批还有 `kmeans_motion_6.npy` **(10,6,12,2)**、`kmeans_map_100.npy` **(100,20,2)**、`kmeans_det_900.npy` **(900,11)**，与 SparseDrive 的四个 `anchor=` 配置项一一对应 |
| 同上，但**给 DIVER 用** | **DIVER** stage1 配置要 `data/kmeans/kmeans_plan_6.npy` | 同上一行（文件名相同） | **形状不兼容**：DIVER 自带的 `adzoo/sparsedrive/tools/kmeans/kmeans_plan.py` 是 `K=6` + `navi_trajs[cmd-1]`（**6 组命令**）→ 产出 **(6,6,6,2)**，且依赖 `./data/infos/b2d_infos_train.pkl`（**Bench2Drive** 数据）。→ **公开可下载的 (3,6,6,2) 不能给 DIVER 用**；同名文件在两套代码里**语义不同** |
| `motion_anchor_infos_mode6.pkl` | **UniAD**（`base_e2e.py:419` `anchor_info_path=`） | UniAD Release tag `v1.0` 资产（**5,109 B，5,908 次下载**）+ `docs/DATA_PREP.md:42` 给出 HuggingFace 直链（`OpenDriveLab/UniAD2.0_R101_nuScenes`） | **渠道确认可用**（未下载，因 UniAD 侧本轮不涉及复现） |
| `carla_plan_vocabulary_4096.npy` | **VADv2**（`VADv2_head.py:204` `np.load(plan_anchors_path)`） | `hustvl/VAD` **无任何 release**；全仓 0 个 `.npy`；README 的下载链接只有**模型权重**（Google Drive） | **仍不可得** → **唯一真正剩下的词表阻塞**，但构造线索已明确（**§H.4.2**：来源是 CARLA GT 轨迹、形状 (4096,6,2)、累积位移空间、配置注释留了 `gt_trajs.npy`） |
| `gtrs_traj/navtrain_16384.pkl` | **DiffusionDriveV2**（`vocab_pdm_gt_path`） | 四个 Releases 渠道都没有，**但仓库自己的 `docs/install.md:20-21` 给了 HuggingFace 直链**（**§H.4**） | **可下载但 30.5 GB**（实测 HTTP 200、`x-linked-size: 30508754314`）→ **不是"缺失"，是成本** |

### H.2 三条判断

1. **"必须先重建词表"这条阻塞，对 DiffusionDrive / SparseDrive / UniAD 三条线都不成立**——三个文件都能直接下载，其中 DiffusionDrive 的 20 锚点我还做了**逐字节比对**确认 v1/v2 同源。→ [state.md](../../state.md) 待续清单第 10 项与 [preparation.md](../../ideas/preparation.md) 的资源估算**需要下调**。
2. **真正剩下的两个空洞是**：**VADv2 的 4096 词表**（无任何渠道，且需自行写构造脚本）与 **DiffusionDriveV2 的 `navtrain_16384.pkl`**（PDM 子分数表）。前者恰好是"**离散词表 + 分类**"这一类最强基线的入口（§G.2），因此**"复现 VADv2 这类基线"仍然是最贵的一步**。→ **第二十四轮复查后第 2 项要改**（见 **§H.4**）：`navtrain_16384.pkl` **有官方 HuggingFace 直链**（在仓库自己的 `docs/install.md` 里），只是**体积 30.5 GB**——所以它**不是"不可得"，而是"下载与存储成本"**；**唯一真不可得的仍只有 VADv2 的 4096 词表**（但构造线索已明确，见 §H.4.2）。
3. **"同名文件"是个陷阱**：`kmeans_plan_6.npy` 在 SparseDrive 是 **(3,6,6,2)**、在 DIVER 是 **(6,6,6,2)**，**文件名相同、命令组数与数据来源都不同**。→ 引用或复用锚点文件时**必须同时记录形状与生成脚本**，否则会静默出错（形状不匹配在 `np.load` 阶段不会报错，要到 anchor encoder 的维度运算才炸）。

### H.3 对"轨迹词表"谱系（§C）的补正

§C 里 DiffusionDrive 那一环（环节 ④）此前依赖"锚点文件未发布"，本轮实测后可以升级为**完整证据链**：锚点文件**公开可得**（Release 资产）→ 形状 **(20,8,2)** 与代码断言一致 → 与 V2 的同名文件**逐字节相同**。即**"词表当扩散起点"这一环从论文级升级到了可复现级**。

**顺带更正一处口径**（DIVER 的候选数，原记在 [diffusion_planner_code_traces.md](diffusion_planner_code_traces.md) §G）：DIVER 的 `num_cmd` **不是候选数而是"命令组数"**。逐项证据：8 个配置里 3 个 `num_cmd=6`、5 个 `num_cmd=1`，而**唯一实例化扩散头**（`DriveStyleMotionPlanningHead`，全仓只有 `motion_planning_head_DriveStyle.py` import `diffusers`）的是 `DIVER_small_b2d_stage2_targetpoint_multiplan.py`（`num_cmd=6`、`plan_anchor=kmeans_plan_6.npy` 生效）；但它的 decoder `HierarchicalPlanningDecoder.decode` 里是 `classification.reshape(bs, 1, self.ego_fut_mode)`（`decoder.py:136`）→ **输出候选数恒为 `ego_fut_mode=6`**。→ 原记的"36 候选"是**误读**；正确表述是"**`num_cmd` 决定锚点的命令组数，输出模态数由 `ego_fut_mode` 决定**"。

### H.4 第二十四轮复查：两个"空洞"的状态都要更新（一个其实有直链，但 30 GB）

§H.1 的表把这两个文件记为"仍不可得 / 仍缺失"。本轮复查**仓库自身的 docs 与类默认值**后，两条记录都需要更正：

| 文件 | 原记 | 复查结论 | 证据 |
|---|---|---|---|
| `gtrs_traj/navtrain_16384.pkl` | "四个 Releases 渠道都没有 → **仍缺失**" | **有官方直链，但体积 30.5 GB** → **不是"不可得"，而是"下载与存储成本"** | `DiffusionDriveV2/docs/install.md:20-21` 原文：`cd gtrs_traj` + `wget https://huggingface.co/Zzxxxxxxxx/gtrs/resolve/main/navtrain_16384.pkl`（用途原文写 "To utilize GTRS trajectories as **data augmentation during mode selector training**, please download the simulated ground-truths for the GTRS vocabulary"）。**实测**：该链接返回 **HTTP 200**，`x-linked-size: **30508754314**`（30.5 GB） |
| `carla_plan_vocabulary_4096.npy` | "无任何渠道，需自写构造脚本" | **仍无渠道，但构造线索比原先记录的多**（见下） | 见 H.4.2 |

#### H.4.1 `navtrain_16384.pkl` 里到底存了什么（从代码读出）

`diffusiondrivev2_model_sel.py:1202-1235` 的 `get_vocab_pdm_subscores` 给出完整结构：

- `joblib.load(vocab_pdm_gt_path)` 后是 **`{token: {metric_name: np.array(16384,)}}`**——**按 navtrain 的 token 索引**，每个 token 存 **16384 条词表轨迹的 6 个 PDM 子分数**（这就是它 30.5 GB 的原因）。
- **6 个 metric 名**（代码里带内部名 → 词表字段名的映射表）：`no_collision → **no_at_fault_collisions**`、`drivable_area → **drivable_area_compliance**`、`progress → **ego_progress**`、`ttc → **time_to_collision_within_bound**`、`comfort → **history_comfort**`、`dir_weighted → **driving_direction_compliance**`。
- **组合式就是 PDMS 公式本身**：`final = NC × DAC × (5·TTC + …)`（与 [benchmarks.md §2](../../direction/benchmarks.md) 记录的 NAVSIM PDMS 权重一致）。
- 与 `self.vocab = np.load(vocab_path)`（即仓库内已有的 `gtrs_traj/16384.npy`，**(16384,40,3)**）配对使用。

→ 即 §D 里"V2 的词表是预计算 PDM 子分数查找表"这一条，现在有了**完整的字段名与组合式**。

#### H.4.2 VADv2 的 4096 词表：仍不可得，但构造线索明确

- **代码里引用了两个都不在仓库里的词表文件**：配置用 `carla_plan_vocabulary_4096.npy`（`VADv2_config_voca4096.py:104`），而**类的默认值是另一个**——`VADv2_head.py:177 plan_anchors_path='./plan_anchors_endpoint_242.npy'`（"endpoint_242"，一个 **242 条**的早期变体）。
- **构造来源有直接线索**：`VADv2_config_voca4096.py:104` 的同一行里**注释保留了替代路径 `#'./gt_trajs.npy'`** → **词表是从 GT 轨迹聚出来的**。
- **形状可由用法反推**：`self.plan_anchors[:,0,:]`（取每条锚点的第一个点）+ `plan_anchors.reshape(1, plan_fut_mode * fut_ts, -1)` → **`(N, fut_ts, 2)` = (4096, 6, 2)**。
- **锚点在"累积位移"空间**：`best_match_idx = torch.linalg.norm(ego_fut_trajs[0].cumsum(dim=-2) - self.plan_anchors, dim=-1).sum(dim=-1).argmin()` —— **GT 先 `cumsum` 再与锚点比**；且输出被 `outputs_ego_trajs = outputs_ego_trajs * 0. + self.used_plan_anchors[None]` **整体替换**，说明**锚点与回归输出同空间**。
- **数据源是 CARLA，不是 nuScenes**：文件名即 `carla_plan_vocabulary`；且 `VAD/README.md:27` 明写 "**CARLA implementation of VADv1 is available on Bench2Drive**"。→ **重建需要 CARLA/Bench2Drive 的专家轨迹 + 自写聚类脚本**。

### H.5 对资源估算的影响（两处更新）

| 项 | 更新后的状态 |
|---|---|
| **DiffusionDriveV2 的 PDM 子分数表** | 从"**缺失**"改为"**有 HuggingFace 直链，但 30.5 GB**" → 任何"复现 V2 的 mode selector"计划都要把 **30 GB 下载 + 存储**算进去；且它的用途是 **mode selector 训练的 data augmentation**，不是推理必需 |
| **VADv2 的 4096 词表** | **仍是唯一真不可得**，但**不再是"无从下手"**：来源（CARLA GT 轨迹）、形状（(4096,6,2)）、空间（累积位移）、构造线索（`gt_trajs.npy` 注释）都已明确 → 缺的是 **Bench2Drive/CARLA 专家轨迹数据 + 一个聚类脚本** |

## I. 「特权信息三段式」的代码级核验——推理期输入权限清单

**动因**：[direction/lineage.md](../../direction/lineage.md) 里有一条**领域级结构观察**——"**特权信息的三段式**"（① 输入即特权 → ② 输入侧去特权 → ③ 特权作为可选辅助/提示）。该条目前明确标注为"**AI 归纳，依据上表的'输入'列**"，即**只有论文级依据**。同时 [preparation.md](../../ideas/preparation.md) 第 6 节要求"**输入权限必须分别标注**"，但一直缺一份代码级清单。本节把这两件事一起补上：**逐个读各仓库推理期实际声明的传感器 / 数据管线实际读取的字段**。

### I.1 推理期输入清单（逐仓库，读 `sensors()` 与数据管线）

| 仓库 | 相机 | LiDAR | 地图 | ego 运动学 | 路由/命令 | 代码证据 |
|---|---|---|---|---|---|---|
| **ST-P3**（CARLA） | **4 视角** rgb（前/左/右/后，各 400×300） | **无** | 无 HD 地图（只用 GPS 路径点） | IMU + GNSS + speedometer | `RoutePlanner`（GPS） | `carla_agent.py:sensors()` |
| **TCP**（CARLA） | rgb（+第二视角） | **无**——`base_agent.py` 里 `sensor.lidar.ray_cast` **整段被注释掉**（`:170`） | 无 | IMU + GNSS + speedometer | 无（用 GPS） | `leaderboard/team_code/tcp_agent.py:sensors()` |
| **TransFuser**（CARLA） | rgb ×3（+1 局部视角） | **有**（`sensor.lidar.ray_cast`） | 无 | IMU + GNSS + speedometer | 无 | `team_code_transfuser/submission_agent.py:sensors()` |
| **UniAD**（nuScenes） | 6 视角（BEVFormer） | `use_lidar=False` | **`use_map=False`** | **未发现 `ego_status` 类消费**；`use_external=True` **声明但全仓只读 `modality['use_camera']`** | `command`（`traj_api.get_sdc_planning_label`） | `stage2_e2e/base_e2e.py:29-31`、`nuscenes_e2e_dataset.py:363-368`、`datasets/nuscenes_e2e_dataset.py:514` |
| **VAD v1 / v2**（nuScenes） | 6 视角 | `use_lidar=False` | **`use_map=False`** | **`ego_lcf_feat`**（`info['gt_ego_lcf_feat']`；VADv2 配置取 `ego_lcf_feat_idx=[0,1,4]`） | `ego_fut_cmd` | `VAD/projects/configs/VAD/VAD_base_e2e.py:31`、`nuscenes_vad_dataset.py:1312`、`VADv2_config_voca4096.py:102` |
| **SparseDrive**（nuScenes） | 6 视角 | `use_lidar=False` | **`use_map=False`** | **`ego_status` = CAN bus 的 `pose.accel`（加速度）+ `steeranglefeedback`（转向角）**——尽管配置写 `use_external=False` | `num_cmd=3` 命令组 | `sparsedrive_small_stage2.py:618-624`、`tools/data_converter/nuscenes_converter.py:419-432`、`motion/instance_queue.py:29,51`、`nuscenes_3d_dataset.py:310` |
| `Hydra-MDP` / `DriveVLM` | — | — | — | — | — | **零代码**，无法核验（§A） |

### I.2 三条判断

1. **三段式在代码层成立，但第 2 段的措辞必须收紧**。lineage 写"网络只见相机（**+LiDAR**）"，而代码层**三个工作里只有 TransFuser 真的吃 LiDAR**：**ST-P3 是 4 视角纯相机**，**TCP 也是纯相机**——它的 LiDAR 行在 `base_agent.py` 里**整段被注释掉**（`:170`）。→ "去特权"这一段的准确表述是"**只见相机，LiDAR 仅 TransFuser 有**"。
2. **`use_external` 这个 config flag 不可信，而且两个方向都错**：**UniAD 声明 `True` 却全仓未消费**（grep `use_external` 在 `projects/` 下只命中配置本身；数据集只读 `modality['use_camera']`）；**SparseDrive 声明 `False` 却实际消费 CAN bus 的 `ego_status`**（`instance_queue.py` 里 `prev_ego_status` + `ego_feature_encoder`）。→ **判断"输入权限"必须看数据管线实际读了什么，不能看 config flag**。这直接决定 [preparation.md](../../ideas/preparation.md) 第 6 节的"输入权限标注"该怎么做：**按实测字段标，不按配置文件标**。
3. **nuScenes 四家在感知侧是彻底去特权的，但"特权"残留三处**：四家**一致** `use_lidar=False` + `use_map=False`（**都不用 HD 地图、都不用 LiDAR**，只有 6 视角相机）——这是代码级确认的强事实。残留的三处是：① **`gt_sdc_*` 系列**（UniAD 的自车辅助监督标签，**只在训练侧**）；② **路由命令**（UniAD `command` / VAD `ego_fut_cmd` / SparseDrive `num_cmd=3` / NAVSIM 系的 `driving_command`——**四家都用，属导航输入而非特权**）；③ **ego 运动学**（VAD 的 `ego_lcf_feat`、SparseDrive 的 CAN `ego_status`）。→ ②③ **不是网络输入特权，但都是跨基准比较时必须声明的输入权限**：CARLA 系用 GPS + route planner，nuScenes 系用 `command` + CAN bus，NAVSIM 系用 `driving_command` + 矢量化自车状态——**三者可得性不同，这正是"输入权限不可横比"的代码级依据**。

## J. GenAD（CVPR'24）的代码级核验——"生成式但非扩散"的第二条路线

**动因**：GenAD（[2402.11502](https://arxiv.org/abs/2402.11502)）是 13 个主干仓库里**规模最大（848 个 `.py`）却一直没做代码级核验**的一个，而它在 [direction/lineage.md](../../direction/lineage.md) 阶段 III 里与"回归/分类"并列，自述为"生成式端到端"（README 首句 "**GenAD casts autonomous driving as a generative modeling problem**"）。本轮把它读完，结论是**这条"生成式"与扩散完全无关，且应当被单独归类**。

### J.1 组合关系：**基于 VAD 的代码库**

| 证据 | 内容 |
|---|---|
| 数据集文件名 | `projects/mmdet3d_plugin/datasets/**nuscenes_vad_dataset.py**`，类 `GenADCustomNuScenesDataset(NuScenesDataset)` |
| 闭环配置路径 | `closed-loop/adzoo/genad/configs/**VAD**/GenAD_config_b2d.py`（目录名就叫 `VAD`） |
| 继承的写法 | `self.ego_query = nn.Embedding(1, self.embed_dims)`（`:420`）——**与 VAD v1 完全同款** |
| **但改掉了一处 VAD 的 ego 输入** | `ego_lcf_feat_idx=None`（VAD 用 `[0,1,4]`）→ **GenAD 不消费 `ego_lcf_feat`** |
| README 自带对照表 | VAD(Paper) 39.42 / VAD(Github Update) 42.35 / VAD(Reproduction) 38.16 / **GenAD 44.81**；成功率 0.159 |

→ **GenAD 与 VAD 是同一代码库的两代**，且作者自己在 README 里用 VAD 作基线。

### J.2 生成机制：**对角高斯隐变量（CVAE 式）+ spatial GRU**，不是扩散

| 项 | 代码证据 |
|---|---|
| 分布类型 | `generator/distributions.py::DistributionModule` 的 docstring 原文："A convolutional net that parametrises a **diagonal Gaussian** distribution"；输出 `(mu, log_sigma)`，`log_sigma` 被 `torch.clamp` 到 **`[-5.0, 5.0]`** |
| 隐变量维度 | `self.latent_dim = 32`、`self.probabilistic = True`（`GenAD_head.py:442-445` **硬编码**） |
| 未来预测器 | `generator/state_prediction.py::FuturePrediction`——docstring "future prediction with **grus**"，`SpatialGRU` × 3 + `Bottleneck` 残差块；另有 `PredictModel`（`nn.GRU` + 三层 MLP） |
| **训练/推理用不同分布**（核心） | `GenAD_head.py:1962-1976`：<br>`if self.training: mu = future_mu; sigma = exp(future_log_sigma)` ← **后验**（当前特征 + 未来 GT）<br>`else: mu = present_mu; sigma = exp(present_log_sigma)` ← **先验**（只用当前特征）<br>`sample = mu + sigma * noise` ← **重参数化采样** |
| 两个分布的对齐 | `ProbabilisticLoss`（`@LOSSES.register_module()`，docstring "**kl-loss for present distribution and future distribution**"）算的是**两个对角高斯之间的解析 KL**：`log σ_p − log σ_f − 1/2 + (σ_f² + (μ_f − μ_p)²)/(2σ_p²)` = **KL(N_future ‖ N_present)**；配置 `loss_vae_gen=dict(type='ProbabilisticLoss', loss_weight=**1.0**)` **启用** |

→ 这是**标准 CVAE 的重参数化**：训练用后验、推理用先验、两者由 KL 对齐。**全仓无任何扩散日程 / 去噪步 / 噪声调度**。

### J.3 规划输出与损失

| 项 | 代码证据 |
|---|---|
| 视野 | `fut_ts=6`、`valid_fut_ts=6` → **3 s @2 Hz**，与 UniAD / SparseDrive / VAD **同一视野** |
| 输出模态数 | `ego_fut_mode` 默认 **3**（head `:144`），**闭环 config 覆盖为 6**（`ego_fut_mode=6, #here`） |
| 输出张量形状 | 逐帧解码后 `torch.stack(ego_fut_trajs_list, dim=2)` → **`(B, ego_fut_mode, fut_ts, 2)`**（默认 (B,3,6,2)；闭环 (B,6,6,2)）。注意**只有 (x,y)，没有朝向** |
| **规划损失四项全开** | `loss_plan_reg`（L1，**1.0**）、`loss_plan_bound`（`PlanMapBoundLoss`，**1.0**，`dis_thresh=1.0`）、`loss_plan_col`（`PlanCollisionLoss`，**1.0**）、`loss_plan_dir`（`PlanMapDirectionLoss`，**0.5**） |

→ **与 VAD 形成鲜明对照**：VAD 的规划只靠 `loss_plan_cls_expert=200` 一项（其余**全为 0**），**GenAD 走的是"回归 + 三项几何约束损失"**。→ **"VAD 家族"内部并不统一**。

### J.4 对 §C「轨迹词表/锚点」谱系的补正

- **GenAD 的 ego 规划器没有任何词表 / 锚点**：`projects/` 全仓 grep `vocabulary|plan_anchor|kmeans` **零命中**。
- 闭环目录里确有 `kmeans_anchors`，但**只在智能体运动预测头**（`closed-loop/mmcv/models/dense_heads/motion_head*.py`、`base_motion_head.py`）——是给**其他交通参与者**的，**不是自车规划**。
- → **"生成式"在本领域有两条独立路线**：① **隐变量生成**（GenAD：对角高斯 + GRU + KL，**无词表**）；② **轨迹词表生成**（VADv2 → DiffusionDrive：先有 4096 词表，扩散只是把词表当**起点**）。**两者的先验来源完全不同**——引用"生成式规划器"时必须区分。

### J.5 三条判断

1. **GenAD 是扩散规划器之前"生成式规划"的代表，且其生成机制与扩散无关**（对角高斯隐变量 + spatial GRU + 解析 KL）。→ 本项目做"生成式 vs 非生成式"对照时，**必须把 GenAD 作为独立的第四类**：它既不是"单模回归"（UniAD/VAD v1），也不是"离散词表 + 分类"（VADv2/Hydra-MDP），更不是扩散。**⚠ 更正（第三十轮）**：本节原写"第三类"，但紧接着的三个否定（单模回归 / 离散词表+分类 / 扩散）已经占了 1–3 位 → GenAD 是**第四类**，与 [judgments.md §C](../../judgments.md) 及 [preparation.md](../../ideas/preparation.md) S4 对齐。
2. **GenAD 与 VAD 同库、两代、范式相反**：VAD 把回归分支乘 0 只留分类，GenAD 用回归 + 几何约束损失。→ **"VAD 家族"不能当作一个整体引用**。
3. **"生成式"不等于"多模态"，多模态的来源分两类**：GenAD 的隐变量是**一个 32 维连续高斯**（输出 3 或 6 条候选靠 `ego_fut_mode` 个解码头），VADv2 的 4096 是**离散词表**。→ 这与 [C003](diffusion_planner_code_traces.md) §H.4 的"起点先验 5 类"是**不同维度**的分类，两者都要在比较表里标。

---

**§K 及以后见 [e2e_trunk_code_traces-2.md](e2e_trunk_code_traces-2.md)**（本册为 §A–§J；§K–§M 含 CARLA 系 6 基线 / TransFuser·TCP·ST-P3 / LBC·CIL·NEAT·DriveLM）。拆分原因：原文 67 KB，超 Read 工具 64 KB 上限。
