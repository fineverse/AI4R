# 自动驾驶项目 · 逐轮工作记录 · 第二十四轮（前半，§1–§16）

本卷范围：**第二十四轮（前半，§1–§16）**。内容：世界模型侧 4 篇升全文 + WoTE 源码核验、世界模型代码可用性全表、DriveLaW、Drive-OccWorld / World4Drive / LAW、Flow Planner、IR-WM 分支、CARLA 系 6 个基线、两个词表空洞复查、TransFuser / TCP / ST-P3、回填 preparation.md、DrivingGen、LBC / CIL / NEAT / DriveLM。
索引见 [../history.md](../history.md)；当前状态见 [../state.md](../state.md)。

---

## 第二十四轮（世界模型侧：4 篇升全文 + WoTE 源码核验，接口路线定型为五条，2026-09-23）

**动因**：VLA 侧在列 6 个仓库已全部核完，**下一块未核验的领域回到世界模型侧**——§3 补录到的 5 个 arXiv ID 已确认但**尚未读全文**，且世界模型的"接口路线"此前只有三条（且只有两条有代码级证据）。

**做法**：派出**两个并行子代理**读 4 篇全文（DriveDreamer / RenderWorld / Imagine-2-Drive / WoTE），**主线程**做 WoTE 的源码级核验（`raw.githubusercontent.com` 逐文件取证，**不占 GitHub API 额度**——上一轮已实测未认证 API 只有 60 次/小时）。

**核到的四组结论**（全文事实写入 [world-model/papers.md §4.1](../topics/world-model/papers.md)，代码结论写入 [C004 §E](../code/traces/world_model_code_traces.md)）：

### 1. WoTE（WM-24，ICCV'25）：**选优器形态的第一个可代码核验实证，且是"非扩散规划器超过扩散规划器"**

- **三段式逐条一致**：`configs/default.py:123 num_traj_anchor = 256`（K-means 锚）→ `WoTE_model.py:362 _predict_offset`（锚经 MLP 编码成 query，与 BEV 做 cross-attention，MLP 头出 offset，`:675 锚 + offset`）→ `:107 self.latent_world_model = nn.TransformerEncoder(...)` + `:111 self.reward_conv_net`
- **选优 = 学到的奖励模型 + argmax**：`:119 reward_head`（imitation，`softmax`）+ `:124 sim_reward_heads`（**5 个头**，`sigmoid`，注释原文 `S_NC, S_DAC, S_TTC, S_EP, S_COMFORT`）；`:723 assert len(sim_rewards) == 5`；`:730-734` 的加权式 **在 log 空间复现了 PDMS 的加权结构**；`:651 select_best_trajectory` → `:652 torch.argmax(final_rewards, dim=-1)`
- **规模与延迟**：`:12 TrajectorySampling(time_horizon=4, interval_length=0.5)` → **8 poses @ 2 Hz**（`:654 .view(batch_size, 8, 3)`）；BEV **8×8**（`num_keyval = 64 # 8*8`）；论文 Table 6 报 **18.7 ms（L20，256 轨迹）**
- **三处需收窄**：① **数字有三个口径**——README **88.3** / 论文 Table 1（navtest）**87.1** / Table 3·6 消融表 **85.6**；② **论文称预测 t+2s 与 t+4s 两步，默认配置 `num_fut_timestep = 1` 只跑一步**（`interval = 8 // 1 = 8` → `fut_idx = 8`）→ 与 ORION 的"配置全量关闭"同类；③ **`WoTE_agent.py:47 use_wm=False` 全文件唯一出现处、从未被读取**（声明未接线）
- **两条结构事实**：**锚点不随权重发布**（`:79-80` 加载时显式 `del state_dict[...trajectory_anchors]`，由 `.npy` 重建）；**规则奖励是离线预计算的查表**（`WoTE_targets.py:48/82` 读 `formatted_pdm_score_256.npy`，按 `token['trajectory_scores'][0]` 取 5 个指标）→ **与 DiffusionDriveV2 的 `navtrain_16384.pkl` 是同一种手法**
- **同组前作**：README「More from Us」列 **LAW（ICLR'25）= 本工作空间 WM-06**

### 2. DriveDreamer（WM-21，ECCV'24）：**特征级条件**，但代码范围不符

- 两阶段训练（阶段一学交通结构、阶段二用 **ActionFormer**（GRU + cross-attention 吃动作）预测未来结构条件）；基座 **SD v1.4（冻结）**；联合生成**未来 16 帧视频 + 16 个未来动作**；动作空间 = **yaw 角 + 速度**
- **规划接口＝特征级**：原文 "pool multi-scale UNet features from Auto-DM" + 历史动作特征 → **MLP 出未来动作**
- 开环规划 L2 **0.29 m** / 碰撞 **0.15**（Table 3）
- **代码核验：仓库只有生成侧，未见规划脚本** → 与 WM-01 同类"代码范围不符"

### 3. RenderWorld（WM-22，ICRA'25）：**token 级联合自回归的第二个实证**

- **Img2Occ**（3D Gaussian Splatting 自监督生成 3D 占据标签）→ **AM-VAE**（**两个独立 VQ-VAE 分别编码 air / non-air，各带码本**）→ **自回归世界模型，明确沿用 OccWorld 的 masked temporal attention + 多尺度子世界模型**
- **同时解码未来占据与自车位移**（`d_ego(z_0)` + L2 loss）
- Table III：3D-Occ 输入下 **L2 avg 1.03 m / 碰撞 0.61%**，优于 OccWorld-S（1.17 / 0.60）；Table IV：**码本 512 最优**，**latent 分辨率比码本更关键**（25²/100² 都明显更差）
- **未找到官方代码仓库**

### 4. Imagine-2-Drive（WM-23，IROS'25 投稿）：**世界模型当"想象环境"**

- 世界模型 **DiffDreamer** 基于 **SVD** 架构、由 **Vista**（约 1700 h）初始化；**一次预测多帧**（把前 P 帧噪声位替换成历史观测、当前帧重复多次）以抑制误差累积，并加 reward 头补齐 MDP
- 策略 **DPA** = 扩散策略（U-Net + **DDIM**），动作是**离散 one-hot 嵌入（11 维）**；**用 PPO 在 DiffDreamer 的想象空间里更新**，无需在线交互
- Table I：**SR 83.33% / Infraction 0.70 per km / RC 82.13%**（vs Dreamer-V3 63.33 / 1.52 / 67.53）
- **一处自相矛盾**：摘要写 RC 提升 **15%**、正文写 **14.6%**
- **代码未发布**（README "Code coming soon!"）

**本轮最有价值的三点**：

1. **"世界模型 → 规划器"的接口由三条定型为五条**：① token 级联合自回归（OccWorld **代码级** / RenderWorld 全文）② 隐状态级条件（PWM **代码级**）③ **特征级条件**（DriveDreamer）④ **选优依据**（Drive-WM 命令级 / **WoTE 轨迹级，代码级**）⑤ **RL 的 reward/next-state 来源**（Imagine-2-Drive）。→ **路线 1–4 的规划器本身都不是生成式**——**"世界模型进规划器"不要求规划器是扩散的**。
2. **"选优器"这一形态从 1 个实证变成 2 个，且粒度必须区分**：Drive-WM 是**命令级**（树搜索在 3 个命令间选，无代码）、WoTE 是**轨迹级**（256 条候选 + 学到的奖励模型打分，代码级）。→ 论文表把两者并列时必须写明粒度。
3. **对研究对象新增一个可借鉴的接口位**：WoTE 证明"世界模型给候选轨迹打分"能把 PDMS 从 83.2 提到 85.6（论文 Table 3），而**它的规划器根本不是扩散的**。→ 研究对象侧若做"世界模型 + 扩散规划器"，**至少有两个接口位**：**把未来当条件喂进去噪（路线 ②③）** 与 **把未来当评价器给采样结果打分（路线 ④）**。

### 5. 世界模型侧"代码可用性全表"（子代理批量核实）

**动因**：§1 表的"质量依据"列此前只有 WM-01/03/17/18 记过代码状态，**其余 15 篇连"有没有官方代码"都没系统核过**——而这正是"源码级工作"的前提。派子代理用 `raw.githubusercontent.com` + GitHub trees API 逐仓核实（**不克隆**），结论写入 [world-model/verification.md §5](../topics/world-model/verification.md)：

- **9 篇里只有 6 篇**（WM-04 Drive-OccWorld / WM-06 LAW / WM-07 World4Drive / WM-10 TrafficBots / WM-11 DriveLaW / WM-20 DrivingGen）真能拿到与论文对应的代码；**WM-12 DrivingGPT 项目页指向的仓库不存在**（"宣称有码但未公开"）、**WM-13 UniDrive-WM 只有项目页**、**WM-16 Raw2Drive 仅 README**。
- **只有 4 篇同时含"世界模型侧 + 显式规划器"**：WM-04、WM-06、WM-07、**WM-11**。
- **唯一与研究对象直接同构的 WM-09 DriveFuture 没有官方代码**，同为"作为条件"支线的 WM-19 FutureX 也没有 → **navhard 24.2→55.5 这条最关键的数字只能停留在论文自述级**。
- 副作用：`repositories.md` 的"无代码/代码不全"清单从 **9 条升到 12 条**。

### 6. WM-11 DriveLaW 的逐文件核验（本轮最有价值的发现）

**"世界模型 + 扩散规划器"已有前人做过，且两种接法在同一个仓里**（[C004 §G](../code/traces/world_model_code_traces.md)）。DriveLaW（CVPR'26）仓库同时含 LTX 视频世界模型、**`ReCogDriveDiffusionPlanner`** 与 **DiffusionDrive 基线**：

- **接口 A（默认路径）**：`video_model_infer_navsim.yaml` 里 **`action_expert: true`**、`action_in_channels: 3`、`action_num_attention_heads: 16`、`train_mode: 'action_full'`、**`return_video: false`** → **动作专家内嵌在视频扩散 transformer 内部，训练时只出动作不出视频**；主干确认为 `LTXVideoTransformer3DModel`（28 层 / 32 heads / in-out 128）+ `FlowMatchEulerDiscreteScheduler`。→ **与 π0 的 action expert 同构**，属"世界模型即规划器"的变体。
- **接口 B（`recogdrive` 路径）**：README Step 1 是 `run_caching_videodrive_hidden_state.sh`（把**世界模型隐状态**缓存遍 navtrain）；`run_training_recogdrive.py` 的 `custom_collate_fn` **直接读 `features['last_hidden_state']`**（特征只有 `history_trajectory`/`high_command_one_shot`/`last_hidden_state`/`status_feature`，监督只有 `trajectory`）→ **隐状态是规划器唯一的感知条件**。
- **一处死引用**：`recogdrive_agent.yaml` 的 `_target_: navsim.agents.recogdrive.recogdrive_agent.ReCogDriveAgent`，**但 `navsim/agents/` 下只有 `diffusiondrive`/`transfuser`/`videodrive` 三个目录** → 接口 B 的"被喂给谁"**未随仓库发布**。这是"声明未接线"的又一实例，且比 DIVER 的 dummy reward 更隐蔽（配置与训练脚本都在，缺的是 `_target_` 指向的模块）。
- **规划器侧可比数字**：`action_horizon = 8`（NAVSIM 8 路点）、`num_inference_steps = 5`、`sampling_method = 'ddim'`（**`flow`/`ddpm`/`ddim` 三路线并列**）、`hidden_size = 1024`、`input_embedding_dim = 1536`；**`grpo = False`（默认关，与 ORION 的 `use_diff_decoder = False` 同类）**，但 `grpo_cfg.scorer_config` 是 **`PDMScorerConfig(progress_weight=10.0, ttc_weight=5.0, comfortable_weight=2.0)` + `metric_cache_path` + `reference_policy_checkpoint`** → **RL 奖励是真 PDM scorer**（"RL 词义核验"清单最强的一档）。
- **对研究对象的意义**：**"接在哪一层"这个问题的选择空间已被前人穷举**（专家内嵌 / 隐状态外挂 / 选优器 / 条件）；剩下的真空白仍是**收益来源拆解**。

### 7. VLA 侧剩余 6 篇的代码可用性 + SafeAuto / Impromptu VLA 源码核验

同批派另一个子代理核实 VLA 侧**从未核过代码可用性**的 6 篇（结论写入 [vla/verification.md §8](../topics/vla/verification.md)）：

- **"有代码"分档再补两档**：**完整**（VLA-05 SafeAuto，~100 MB/217 文件）/ **部分**（VLA-12 Impromptu VLA，~178 MB/464 文件，**训练委派 LLaMA-Factory**，仓内只有一个示例 yaml）/ **仅数据集**（VLA-10 CoVLA，只有 HF 数据集）/ **承诺未兑现**（VLA-01 DriveGPT4，正文写 "code and dataset will be publicly available" 但作者 GitHub 无此项）/ **无**（VLA-02 ADriver-I、VLA-09 EMMA）。→ **VLA 侧 19 篇至此全部核过代码可用性**。另**核定 EMMA 的 arXiv ID 为 `2410.23262`**（原表记"未核验"）。
- **Impromptu VLA**：`server.py:102-113` 的 `extract_trajectory` 用 `re.findall(r"\[([\-\d\.]+),\s*([\-\d\.]+)\]", answer)` 从自然语言抠点，**`return traj[:6]  # Limit to 6 steps`**，**解析失败直接返回 `[[0.0, 0.0]] * 6`（全零点）**；而同一文件的固定 prompt 写 "predict future waypoints for the vehicle over the **next 3 timesteps**" → **要 3 步、收 6 步**。→ **"轨迹即文本"路线现已有三个实例、三种失败模式**（OpenDriveVLA 补齐 / WAM-Flow 文本数字 / Impromptu 补零）。
- **SafeAuto**（`pgm/config.py`）：**16 个高层动作 + 5 个速度控制信号 + 3 个方向控制信号**；**`hardrule_num: int = 10`**，规则以模糊逻辑 lambda 形式（`1 - a + a*b`）写成，**分环境规则**（`SolidRedLight → ¬Accelerate ∧ ¬LeftPass ∧ ¬Yield` 等）**与控制信号自洽规则**（`KEEP_CS`、`LEFT_CS × CHANGETORIGHTLANE_LLM → …`）两类。→ **VLA 侧唯一能逐行核验的"安全门控"**，且与 DP-A21 PC-Diffuser 的"逐去噪步 CBF-QP"构成**两种注入位置的对照**（输出端否决 vs 去噪内约束）。注意 SafeAuto **不输出轨迹**，不能直接与 NAVSIM 系比指标。

**产出（续）**：[vla/papers.md](../topics/vla/papers.md) 新增 **§8（代码可用性表 + §8.1 Impromptu / §8.2 SafeAuto / §8.3 结论）**，文件头与 VLA-09 行更新；[index.md](../index.md) / [sources.md](../sources.md) L015 / [state.md](../state.md) 同步。

### 8. Drive-OccWorld / World4Drive / LAW 的逐文件核验（把"选优依据"扩到三种信号）

§5 的代码可用性全表确认了另外 3 个"世界模型 + 显式规划器"仓库，本轮一并核验（[C004 §I](../code/traces/world_model_code_traces.md)）：

- **WM-04 Drive-OccWorld**：世界模型的未来预测**不与 pose token 联合生成**，而是**单独预测未来语义占据 → `argmax` 成类别图 → `detach()` → 进规划头**（`drive_occworld.py:339/342`）；占据在规划头里算 **`instance_occupancy` 与 `drivable_area`** → 进 **`Cost_Function` → cost volume 选优**（`torch.topk(CS, k=1, largest=False)`）；cost 用 **hinge `L = relu(gt_cost_fo − sm_cost_fo)`** 学；**训练用 GT 占据、推理用预测占据**（注释原文）；**`planning_steps = 1` → 逐帧滚动**。**负面发现：规划损失直接抄自 UniAD**（`planning_loss.py` 文件头版权声明在，`inter_bbox` 的**轴对齐退化一并继承**）。
- **WM-07 World4Drive**：**`class W4D(VAD)` 继承 VAD**；`wm_loss_weight=0.2`；损失族含 `loss_kl`（**隐变量生成，与 GenAD/ORION/MindDrive 的 VAE 同族**）、`loss_cosine`、`loss_wm_diversity`、`loss_traj_diversity`。**最独特的机制是 `select_optimal_modality`**：`loss_rec = 重建 + KL + 余弦`，`total_loss = loss_rec*w + FDE_vs_GT*w_tm`，**`best_modality_idx = total_loss.argmin(-1)`** → **用世界模型损失当"哪个模态该被监督"的准则**（本工作空间唯一一例）。**限定**：FDE 项用 GT → 是**训练期模态分配**，测试走 `torch.argmax(cur_waypoint_cls)`。**形状疑点（需运行确认）**：`torch.cat(tm_loss_list, dim=0)` 得 `[B*num_modalities]`，与 `[B, num_modalities]` 相乘**只在 B=1 时成立**。
- **WM-06 LAW**：`wm_prediction(view_query_feat, cur_waypoint)` → `action_aware_encoder(cat([view_query_feat, cur_waypoint]))` → **以显式 waypoint 为动作条件预测下一帧潜状态**；`loss_reconstruction` 重建的是 **view query 特征**（不是像素/占据）→ "perception-free" 的准确含义。**一处更正**：`VAD/utils/CD_loss.py` **不是对比蒸馏**，是**轨迹点损失集合**（`ordered_pts_smooth_l1_loss` / `pts_l1_loss` / `ordered_pts_dir_cos_loss` 等）。

**新增两条判断**：① **"选优依据"现有三种代码级核验的信号**——**学到的奖励模型**（WoTE）/ **规则 cost volume**（Drive-OccWorld）/ **世界模型自身损失**（World4Drive）；② **"选择环节用 GT"是三家共有的系统性弱点**（OccWorld 的 GT 模式同类）。③ **代码复用谱系又添一环**：Drive-OccWorld 抄 UniAD、World4Drive 继承 VAD、LAW 长在 VAD 代码库上 → **"4D 占据/潜世界模型"这一支大多寄生在 nuScenes 系 E2E 主干代码上**。

**产出（续）**：[C004](../code/traces/world_model_code_traces.md) 新增 **§I（三个仓库的主张对照 + 结论）**、§H 判断扩到 7 条、文件头更新；[world-model/lineage.md](../topics/world-model/lineage.md) 路线 4 一行改写为**三种信号**；[state.md](../state.md) 新增一条判断边界；[README.md](../../../README.md) 同步。

### 9. DP-A11 Flow Planner 的代码级核验（研究对象侧最后一个"代码未获取"缺口关闭）

**动因**：DP-A11 是研究对象侧**唯一"代码本体未获取"**的仓库（`git clone` 与 codeload tarball 都在约 4.5 MB 处稳定截断）。本轮改用**逐文件取证**（GitHub trees API 1 次 + `raw.githubusercontent.com`），把**全部 72 个非图片文件**抓到本地并逐一核对字节数（与树接口 blob size 完全对齐，`truncated=false`）→ **该仓库的静态核验不再有缺口**，结论写入 [C003 §L](../code/traces/diffusion_planner_code_traces-2.md)。

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

### 10. WM-05 IR-WM 的代码位置确认（"代码在哪个分支"这个坑）

**动因**：世界模型侧代码可用性全表（§5）把 WM-05 记为"专属实现未确认"——论文只写 "Codes are available at github.com/yuyang-cloud/Drive-OccWorld"（与 WM-04 同仓）。本轮派子代理查清了：

- **main 分支 README 第 12 行原文**："Our follow-up work **IR-WM** is accepted by ICRA 2026! Please see the **`ir-wm`** branch for more details."
- **main 分支全树对 `residual｜implicit｜irwm｜ir-wm` 零命中**；**`ir-wm` 分支**（head `a83e4a24`，2026-02-08）175 个文件，README 标题即 IR-WM 的标题。
- **相对 main 新增 8 项**（即 IR-WM 专属代码）：**`drive_occworldV2.py`**（新检测器类 `Drive_OccWorld_V2`，`:374/381/384` 有残差加法 `next_bev_feats[-1] + pred_feat  # TODO: predict residual bev features`、`:253-314` 有 `_align_bev_coordnates`）+ **3 个耦合配置 `MMO_MSO_with_plan_{fully,semi,tightly}_coupled.py`** + 可视化/计时工具 + 2 个 assets。

**判断**：**"代码在哪个分支"必须查**——只看默认分支会把"有专属实现"误判成"无专属实现"。→ 查代码可用性时须同时看 **README 的 follow-up 段落**与**分支列表**，这条已写入 [world-model/verification.md §5](../topics/world-model/verification.md) 读数第 4 条。

**产出（续）**：[C003](../code/traces/diffusion_planner_code_traces.md) 新增 **§L（Flow Planner 主张对照 + 实现细节 + 四条判断）**；[papers/diffusion_planner_ad.md](../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A11 行的证据状态升级为**代码静态检查**；[world-model/verification.md §5](../topics/world-model/verification.md) WM-05 行与读数扩到四条；[repositories.md](../code/repositories.md) 的 Flow-Planner 行改为"网络阻塞但已用逐文件取证解决"；[state.md](../state.md) 待续清单第 11 项**关闭**、判断边界"词表谱系"一条补入 Flow Planner 侧证据；[README.md](../../../README.md) / [sources.md](../sources.md) / [index.md](../index.md) 同步。

### 11. CARLA 系 6 个基线的规划/控制输出（把 §G 的规划头对照补全到 13 个仓库）

**动因**：§G 的"非生成式基线规划头对照"只覆盖 **nuScenes 系 4 个**（UniAD / SparseDrive / VAD v1 / VADv2），13 个主干仓库里还有 **CARLA 系 6 个**（TransFuser / TCP / ST-P3 / LBC / CIL / NEAT）从未核过。这批仓库**已在本地**，纯静态阅读，结论写入 [C005 第二册 §K](../code/traces/e2e_trunk_code_traces-2.md)。

**五条发现**：

- **ST-P3 是"预测占据 → cost → 选优"在 CARLA 侧的早期实例，比 Drive-OccWorld（AAAI'25）早 3 年**：`carla_agent.py:458` `cost_volume=output['costvolume'][:, n_present:].detach()`——**`costvolume` 是模型输出的一路**（与未来占据预测同源）→ `stp3.py:384 select_best_traj` → **7 项规则代价**（`safetycost` / `headwaycost` / `lrdividercost` / `comfortcost` / `progresscost` / `rulecost` / **`costvolume`**，全部 clamp 到 [0,100]）→ **`torch.topk(CS, k, largest=False)` 取代价最小**；采样数 **CARLA 2400 / nuScenes 1800**（`configs/*/Planning.yml`；`config.py:145` 默认 600 是第三个值）。
- **"命令喂不喂给模型"在 CARLA 系内部就不一致**：**TransFuser 与 NEAT 都算了 `next_command` 却从未传给模型**（TransFuser `submission_agent.py:222` 只写进 `result`；`:294-295` 的模型调用参数是 `image, lidar_bev, target_point, target_point_image, velocity`——**没有 command**）；而 **TCP 真的把 `next_command` 传进了 `process_action`**（`tcp_agent.py:204`）。→ 与 nuScenes 系（UniAD / SparseDrive 的 eval 用 GT 命令）合起来：**13 个仓库对命令有三种处理方式**（显式输入 / 算了不用 / 只用 `target_point`）。
- **6 个仓库全部零锚点 / 零词表**，但 **`anchor` 在 TransFuser / NEAT 里指 transformer 的空间 attention 网格**（5×22、8×8）——**极易误判为"轨迹锚点"**。
- **ST-P3 带 VAE 但规划不是生成式（最易误标的一个）**：`distributions.py::DistributionModule` 的 latent 混合分布**只服务未来占据预测头**，规划器是"采样 + 规则代价 argmin"。→ 与 GenAD 形成**位置相反的对照**：**同为 CVAE 式隐变量，一个长在感知侧（ST-P3）、一个长在规划侧（GenAD）**。
- **TCP 是唯一"轨迹 + 控制量双分支"的**：`process_action`（Beta 分布头）与 `control_pid(pred_wp, ...)` 各出一套控制量，按 **`alpha=0.3` 融合**（`tcp_agent.py:216-224`，**两处条件不同的 alpha 赋值**）。

**判断**：**"非生成式基线"的分类从三种扩到五种**——新增 ④ **采样 + 规则代价选优**（ST-P3）与 ⑤ **按命令切分支**（LBC / CIL）。→ **ST-P3 的"采样 + 代价选优"与 DiffusionDrive 的"扩散 + scorer 选优"结构最接近，是最容易被误标成"生成式"的一类**；同时 **"把世界模型输出当 cost 去选优"不是新机制**（ST-P3 ECCV'22 已有）。

**产出（续）**：[C005](../code/traces/e2e_trunk_code_traces.md) 新增 **§K（6 仓库对照表 + 五条发现 + §G.2 分类补正）**、文件头规模描述更新；[state.md](../state.md) 的"非生成式基线"一条扩到五种、"命令维"补进输入权限一条；[sources.md](../sources.md) C005 / [index.md](../index.md) / [README.md](../../../README.md) 同步。

### 12. 两个"词表空洞"的复查：一个其实有官方直链（但 30.5 GB），另一个构造线索已明确

**动因**：§H 把 **VADv2 的 4096 词表**与 **DiffusionDriveV2 的 `navtrain_16384.pkl`** 记为"仅剩的两个空洞"，并据此写进了 [state.md](../state.md) 待续清单第 10 项与资源估算。本轮复查**仓库自身的 docs 与类默认值**，两条记录都要更正（写入 [C005 §H.4/§H.5](../code/traces/e2e_trunk_code_traces.md)）。

- **`navtrain_16384.pkl` 有官方直链**：`DiffusionDriveV2/docs/install.md:20-21` 原文 `cd gtrs_traj` + `wget https://huggingface.co/Zzxxxxxxxx/gtrs/resolve/main/navtrain_16384.pkl`（用途原文 "To utilize GTRS trajectories as **data augmentation during mode selector training**"）。**实测该链接 HTTP 200，`x-linked-size: 30508754314` = 30.5 GB** → **不是"不可得"，是下载与存储成本**，且**非推理必需**。
- **该 pkl 的结构（从代码读出）**：`joblib.load` 后是 **`{token: {metric: np.array(16384,)}}`**——按 navtrain token 索引、每个 token 存 16384 条词表轨迹的 **6 个 PDM 子分数**（这就是 30 GB 的来源）；6 个字段名与内部名的映射表在 `get_vocab_pdm_subscores` 里（`no_at_fault_collisions` / `drivable_area_compliance` / `ego_progress` / `time_to_collision_within_bound` / `history_comfort` / `driving_direction_compliance`），**组合式就是 PDMS 公式本身**（`NC × DAC × (5·TTC + …)`）。
- **VADv2 的 4096 词表仍不可得，但构造线索明确**：① 配置里**注释保留了替代路径 `#'./gt_trajs.npy'`** → 词表从 **GT 轨迹**聚出；② **类默认值是另一个文件** `plan_anchors_endpoint_242.npy`（一个 242 条的早期变体）——**代码引用了两个都不在仓库里的词表**；③ 形状可由用法反推 = **`(N, fut_ts, 2)` = (4096, 6, 2)**；④ `best_match_idx` 把 **GT 先 `cumsum` 再与锚点比** → **锚点在"累积位移"空间**（输出被 `*0. + used_plan_anchors` 整体替换，与回归输出同空间）；⑤ 数据源是 **CARLA**（文件名 + `VAD/README.md:27` 明写 CARLA 实现在 **Bench2Drive**）→ 重建需要 **CARLA/Bench2Drive 专家轨迹 + 自写聚类脚本**。

**判断**：**"两个空洞"实为"一个成本问题 + 一个数据问题"**——前者只需 30 GB 下载，后者需要一份 CARLA 专家轨迹数据；**两者都不再是"无从下手"**。→ 资源估算的表述应从"词表缺失"改成"**30 GB 存储 + 一份 CARLA 数据 + 一个聚类脚本**"。

**产出（续）**：[C005](../code/traces/e2e_trunk_code_traces.md) 新增 **§H.4（含 H.4.1 pkl 结构 / H.4.2 VADv2 线索）+ §H.5（资源估算两处更新）**，§H.1 两行与 §H.2 第 2 条同步更正；[state.md](../state.md) 待续清单第 10 项改写；[README.md](../../../README.md) / [sources.md](../sources.md) 同步。

### 13. TransFuser / TCP / ST-P3 的主张—代码对照（补 §B 的 5 项）

**动因**：§B 的主张—代码对照只有 **5 项**（VAD / VADv2 / DiffusionDrive / V2），而这三个 CARLA 系代表工作的**架构与损失主张**从未逐条核过。它们既是领域基线，也是 NAVSIM 系扩散规划器所复用主干（TransFuser）的来源。**仓库在本地，纯静态阅读**，结论写入 [C005 第二册 §L](../code/traces/e2e_trunk_code_traces-2.md)。

**五条发现**：

- **TransFuser 有两个"声明但零权重"的头**：`config.py:134-136` 的 `detailed_losses_weights = [1.0,1.0,1.0,1.0, 0.2,0.2,0.2,0.2,0.2, **0.0, 0.0**]`，末两位正是 **`loss_velocity` 与 `loss_brake`** → 两个头照常计算但**监督权重为 0**；且 `--use_velocity` 默认 **0**。
- **TransFuser 的 `n_layer` 有两套冲突默认值**：`config.py:177` 写 **8**，而 `train.py:56 --n_layer default=4` 且 `:120 config.n_layer = args.n_layer` **覆盖之** → **实际生效的是 4**。→ 与 ST-P3 的 `INSTANCE_SEG/FLOW` 一起，构成"**配置有覆盖链**"这一类陷阱。
- **ST-P3 的 "dual attention" 名不符实**：代码里是 `Dual_GRU`（`layers/temporal.py:59`）= 两个 `gru_cell` + `trusting_gate`（`nn.Conv2d(hidden, 2, 1)`）+ `torch.softmax`，最后 `cur_state = rnn_state2 * trust_gate[:,0:1] + rnn_state1 * trust_gate[:,1:]` → **全仓无任何 attention 运算**（无 QKV、无 multi-head）。→ 引用时必须改写为"**双 GRU 门控混合**"。
- **ST-P3 官方配置关掉了两个头**：`configs/nuscenes/Planning.yml:35-38` 把 `INSTANCE_SEG` / `INSTANCE_FLOW` 置为 **False**，而 `config.py:133,136` 默认 **True** → **单看 `config.py` 会误判多任务规模**；另 `cost_volume` **无直接监督**，仅经规划的 **max-margin 损失**间接学习。
- **TCP 的"轨迹引导"分两层，论文强调的那层在推理脚本里**：网络内是 `wp_att` 注意力（可学习）；**分支主次切换（`alpha=0.3`）是推理启发式**，由转向检测的 `status` 决定（`tcp_agent.py:213-224,237-253`）。→ 复现 TCP 时若只搬网络、不搬这段启发式，行为会不同。

**判断**：**"配置默认值 ≠ 实际生效值"在本工作空间累计到 6 例**（ORION 的 `use_diff_decoder`、HDP 的零权重投影项、Flow Planner 的 `alpha/beta`、WoTE 的 `num_fut_timestep`、**TransFuser 的 `n_layer`**、**ST-P3 的 `INSTANCE_SEG/FLOW`**）→ 已升级为一条判断边界：**读配置必须同时看覆盖链**。

**产出（续）**：[C005](../code/traces/e2e_trunk_code_traces.md) 新增 **§L（三张主张对照表 + 五条发现）**、文件头规模描述更新；[state.md](../state.md) 的"代码里有这个名字≠这条路径被走到"一条扩到 **8 例**并补入"配置覆盖链"陷阱；[sources.md](../sources.md) C005 / [index.md](../index.md) / [README.md](../../../README.md) 同步。

### 14. 把本轮代码级发现回填 `preparation.md`（idea 准备材料）

**动因**：本轮（第二十四轮）在三条代码脉络里积累了十几条新核验结果，但 **idea 准备材料 `preparation.md` 仍停留在旧口径**——它的 §2"可作为设计前提的已验证事实"里有两处已被推翻/扩充，§5 的方向 B/E/G 的重合风险判断也已过时。**代码级工作的直接收益就是让方向选择基于正确前提**，所以本轮做一次回填。

**五处更新**：

1. **§2"非生成式基线"从三类扩到五类**（新增 ④ **采样 + 规则代价选优**（ST-P3）/ ⑤ **按命令切分支**（LBC / CIL）），并补上"**ST-P3 的 `costvolume` 是模型输出的一路 → 用世界模型输出选优比 Drive-OccWorld 早 3 年**"。
2. **§2"两个词表空洞"改成"一个 30.5 GB 成本 + 一个 CARLA 数据问题"**（`navtrain_16384.pkl` 有官方 HF 直链但 30.5 GB；VADv2 的 4096 词表构造线索已明确）。
3. **§2 新增 4 条事实**：① **"世界模型 + 扩散规划器"已有前人做过**（DriveLaW，两种接法都在同一仓里）；② **"世界模型 → 规划器"的接口已定型为五条 + 第 6 条**，且**路线 1–4 的规划器都不是生成式**；③ **"选优依据"有三种信号、三家都在选择环节用 GT**；④ **"无锚点、无词表、无选优"的纯生成有两个代码级实例**（HDP / Flow Planner）。
4. **§5 方向 B/E/G 的重合风险上调**：方向 B 新增"三个现成选优信号 + Flow Planner 作为反面对照"；方向 E 新增"**DriveLaW 已把两种接法都实现过 → '把未来表示接进扩散规划器'这个动作本身已不新颖**"；方向 G 新增"**action expert 已经进到驾驶的视频扩散 transformer 里（与 π0 同构）→ '能不能搬'已被回答为'已经有人在搬'**"。
5. **§6.1 新增 WoTE 一行 + P8 的第四个实例**：**WoTE（非扩散规划器）的 NAVSIM v1 navtest PDMS 88.3（README）/ 87.1（论文）≥ DiffusionDrive 的 88.1** → **"生成式机制"这一维在 navtest 上已不构成优势**；且同一方法三个口径差 2.7 分（88.3 / 87.1 / 85.6）。**§6.2** 的"输出模态与选优方式"从三类扩到五类，并新增"**命令维**"标注要求。

**判断**：这次回填把"代码核验"与"方向选择"接上了——**三条最影响可行性的结论**是 ① **"世界模型 + 扩散规划器"已有 CVPR'26 先例**（影响方向 E 的新颖性）② **具身 action expert 已进驾驶**（影响方向 G）③ **"生成式"在 navtest 上不构成优势、navhard 才有区分度**（影响全部方向的价值判断）。→ **方向空间没有被关闭，但"新瓶装旧酒"的风险显著上升**；剩余的真空白集中在 **"收益来源拆解"**（未来信息是条件还是训练信号）与 **"推理期不依赖 GT 的选优"**。

**产出（续）**：[preparation.md](../ideas/preparation.md) 的**文件头**（新增"第二十四轮更新"段）、**§2**（1 处改写 + 1 处改写 + 4 条新增）、**§5 方向 B/E/G**、**§6.1**（新增 WoTE 行 + 一行读法）、**§6.2**（扩到五类 + 新增命令维）；[README.md](../../../README.md) / [sources.md](../sources.md) L008 同步。

### 15. WM-20 DrivingGen 的代码级核验——一个"轨迹指标由感知反推"的评测基准

**动因**：世界模型侧"代码可用性全表"（§5）确认 **DrivingGen 是世界模型侧唯一还有代码但未核验**的一篇（ICLR'26，61 MB / 1274 文件）。它是本表 WM-20 的定位（"生成式视频世界模型的评测基准"），而**评测方式本身**对研究对象有直接影响。结论写入 [C004 §J](../code/traces/world_model_code_traces.md)。

**四条硬发现**：

- **它的"轨迹指标"不是规划器指标，而是"感知反推指标"**：`extract_traj_ego_unidepth.py:15-25` 导入 `UniDepthV1/V2` + `visual_slam.vo` + `YOLOv10`，`extract_traj_agent_unidepth.py:40-71` 加载 `unidepth-v2-vitl14` + `yolov10x.pt`，`:118-136` 做"像素+深度+内参+位姿 → 3D 轨迹"，`:461` 用 SAMURAI 跟踪 → **ADE / FDE / DTW / traj_consistency 的评价对象是"用这套感知栈从生成视频里反推出来的自车轨迹" vs GT**，**误差里混入了感知栈自身的误差**。
- **全仓无 planner-in-the-loop 接口**：在 `drivinggen/` 的 23 个 `.py` 里 grep `planner｜plan_head｜pdm_score｜navsim` **零命中** → **"世界模型 → 规划器"这条接口在本仓库里不存在**；它只评"生成得像不像"，不评"生成得有没有用"。
- **代码明显未收尾**：**6 处未注释的 `pdb.set_trace()`**（`extract_traj_agent_unidepth.py:374`、`extract_traj_ego_unidepth.py:378`、`p2020.py:402`、`traj_distribution.py:323`、`video_a_consist.py:250`、`video_v_consist.py:144`）+ **硬编码作者本机绝对路径**（`/shared_disk/users/yang.zhou/...`、`/mnt/cache/zhouyang/dg-bench/...`）；**仓内 0 个权重文件**（树里 `.pt/.pth/.ckpt/.safetensors` 全无）→ **开箱不可运行**。
- **agent 轨迹评测在驱动脚本里被注释掉**：`z-sample_ftd.py:352-356` 的 `if args.metric == 'a_consist' or 'a_missing' or 'all':` 整段被注释 → **"机制在代码里但被注释关闭"**，与 ORION 的 `use_diff_decoder=False`、WoTE 的 `num_fut_timestep=1` 同类。

**判断**：**DrivingGen 对本项目的直接可用性低**（评的是生成质量与几何合理性，不是规划有效性；且可复现性受 UniDepth / DINOv3 / Cosmos-Reason1 / SEA-RAFT / stylegan-v 等外部模型版本牵制）。**但它给出一个方法论警告**：**"用生成模型的输出反推下游量再打分"会把上游模型的误差混进指标**——这是 NAVSIM 口径问题（EP 批内相对分、EPDMS 权重以本方法终点为中心）的**第二种形态**。→ 本项目若要评"生成式规划器"，**不能走"从输出反推"这条路**。

**产出（续）**：[C004](../code/traces/world_model_code_traces.md) 新增 **§J（逐项核实表 + 四条硬发现 + 判断）**、文件头与"核心问题"更新；[world-model/verification.md §5](../topics/world-model/verification.md) 的 WM-20 行改为"**评测基准，已代码核验**"并补限定；[state.md](../state.md) 的"NAVSIM 指标口径"一条补入**第二种形态**、代码核验计数 13→**18**；[README.md](../../../README.md) / [sources.md](../sources.md) / [index.md](../index.md) 同步。

### 16. LBC / CIL / NEAT / DriveLM 的主张—代码对照（补 §B；并更正 `lineage.md` 的一个数字来源）

**动因**：§K 只覆盖了这四个仓库的**规划/控制输出**，§L 覆盖了另外三篇的**架构与损失主张**。这四个的主张与代码范围仍空着。**仓库在本地**，纯静态阅读，结论写入 [C005 第二册 §M](../code/traces/e2e_trunk_code_traces-2.md)。

**五条发现**：

- **"attention"这个词在同一批仓库里有真有假**（本工作空间已有正反例）：**NEAT 的编码器是真 multi-head self-attention**——`architectures/encoder.py:10-46` 的 `SelfAttention` 有显式 `self.key/query/value = nn.Linear(...)`、`n_head` 切分、`att = (q @ k.transpose(-2,-1)) * (1/sqrt(hs))` → softmax → `att @ v`，`config.py:86/89` 是 `n_layer=2 / n_head=4`；而 **ST-P3 的 "dual attention" 实为 `Dual_GRU` + 门控 softmax**（§L.3）。→ **同一批仓库里"attention"必须逐篇看 QKV**。
- **LBC 的学生蒸馏是"全分支输出级 L1"，不是特征回归**：全仓**不存在 `imitation_loss`**；`train_image_phase1.py:195-199` 比较的是**学生 4 分支路点 vs 教师 4 分支路点**。→ 转述 LBC 时**不能说"蒸馏教师特征"**。
- **CIL 缺的是整个运行时**：`.gitmodules` **实测 0 字节**；`carla` 包（`driving_benchmark`/`agent`/`carla_server_pb2`）、训练脚本、数据加载器**全部缺失** → 只剩"网络定义 + 推理 + 一个 ckpt"，**端到端不可复现**。
- **两处"命令条件"的语义被削弱**：**CIL 的命令不是网络输入**，而是推理时 if/elif **选分支**；**4 维 `input_control` 占位符定义后从未被喂入**（全仓只在 `imitation_learning.py:47` 出现一次）。→ 与 §K 的 TransFuser/NEAT"算了 `next_command` 却不传"是**同一类落差**；**"命令条件"在 CARLA 系早期工作里普遍不是真正的网络条件**。
- **`direction/lineage.md` 的 "DriveLM 0.16 FPS" 在本仓库不可核验**：仓库**全无 FPS/latency 代码**，唯一数字是 README 的"**约 2 小时 / 4072 帧（batch 8）≈ 0.57 fps**"（`challenge/README.md:116-119`）——**与 0.16 FPS 不一致**。→ **已就地更正 `lineage.md` 的两处**（补"来源待补"标注 + 说明仓库内数字）。

**判断**：本轮把 E2E 主干侧的主张—代码对照从 §B 的 5 项扩到**覆盖全部 13 个仓库**（§L 三篇 + §M 四篇 + §K 的规划输出），并**顺带修掉一处无来源的引用数字**。

**产出（续）**：[C005](../code/traces/e2e_trunk_code_traces.md) 新增 **§M（四张主张对照表 + 五条发现）**、文件头规模描述更新；[direction/lineage.md](../direction/lineage.md) **两处 DriveLM 0.16 FPS 补"来源待补"**；[state.md](../state.md) 的"代码里有这个名字≠这条路径被走到"一条新增**第六类陷阱（命名与实现语义不符）**、"命令维"一条补入 CIL；[sources.md](../sources.md) C005 / [index.md](../index.md) / [README.md](../../../README.md) 同步。
