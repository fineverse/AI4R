# 世界模型 → 规划器代码脉络（主张 → 代码）

更新时间：2026-09-23  
证据等级：**代码静态检查**（OccWorld / PWM / Drive-WM / WorldRFT 已克隆读文件与配置；**WoTE、DriveLaW、Drive-OccWorld、World4Drive、LAW、DrivingGen 未落盘，走 `raw.githubusercontent.com` 逐文件取证**；**全部未安装依赖、未运行**）。仓库清单与 commit 见 [repositories.md](../repositories.md)。  
**核验级别（定义见 [ai/rules.md §代码静态检查](../../../../ai/rules.md)）**：**已克隆的 4 个为 L1 逐文件核验**；**走 `raw` 的 6 个为 L3**（与 L1 同级可支持机制结论）；**WorldRFT 空仓 / Drive-WM 不含规划器为 L2**（只确认仓库存在与目录结构）。  
读法：本文件回答研究脉络三关系中的两条——**组合关系**（模块来自哪篇论文）与**主张—代码关系**（论文卖点对应哪些文件）。机制层面的借鉴清单见 [transfer.md](../../topics/diffusion-planner/transfer.md)，继承关系见 [lineage.md](../../topics/world-model/lineage.md)。

**本文件的核心问题**：世界模型的"未来预测"到底以什么形式进入规划器？**10 个仓库**给出多种答案，其中**两个是负面结论**（WorldRFT 空仓、Drive-WM 不含规划器），**两个是"世界模型 + 扩散规划器"的实证**（DriveLaW），**三个是"选优依据"的不同信号**（WoTE / Drive-OccWorld / World4Drive），**一个是"轨迹指标由感知反推"的评测基准**（DrivingGen，§J）。

## A. 主张—代码对照（逐个核验）

| 论文 | 论文主张 | 代码证据（文件 / 类 / 配置） | 一致性判断 |
|---|---|---|---|
| **OccWorld**（WM-03） | 世界模型与规划**联合**：用占据 token 与自车 pose token 在同一自回归 transformer 里共同演化 | `model/transformer/PlanUtransformer.py`：`class PlanUAutoRegTransformer(BaseModule)`，`forward(self, tokens, pose_tokens)`；`model/TransVQVAE.py:forward_autoreg_with_pose`（214 行）在 `for i in range(mid_frame, end_frame)` 里反复调 `self.transformer.forward_autoreg_step(z_q_predict, pose_tokens=rel_poses_state, ...)` | **一致**：占据 token 与 pose token 是**同一序列里的两类 token**，由同一个 transformer 每步同时产出 |
| **OccWorld** | （隐含印象）规划为生成式 | `loss/plan_reg_loss_lidar.py`：`PlanRegLossLidar.__init__(self, weight=1.0, num_modes=3, ...)`，`loss = torch.sqrt(((rel_pose - gt_rel_pose) ** 2).sum(-1)) * weight` | **需更正印象**：规划是 **3 模式多模态回归**（L2 回归 + 模式加权），**不是扩散/生成式** |
| **OccWorld** | codebook 512 | `config/occworld.py`：`n_e_ = 512`；`pose_attn_layers = 2`、`temporal_attn_layers = 6` | **一致**（与论文 512 码本吻合） |
| **Policy World Model**（WM-17） | "Unified Framework：把世界建模与轨迹规划整合进**单一架构**"（README 原文） | `models/modeling_showo.py:navsim_forward`（374 行）**一次前向返回 `(logits, loss_dynamic, loss_tj, mmu_index, eod_img_d)`**；`training/fine-tune_navsim.py:567`：`loss = config.training.video_coeff * loss_video + config.training.tj_coeff * loss_tj` | **一致且更具体**：未来帧 token 的交叉熵（`loss_dynamic`）与轨迹 L1（`loss_tj`）来自**同一个 LLM 的同一次前向** |
| **Policy World Model** | 规划头读取"世界模型的未来表示" | `modeling_showo.py:449`：`logits_tj = self.action_forward(hidden_states[:, -8:])`；`416`：`input_embeddings[:, -action_len:, :] = act_queries`（动作 query 占据序列**末尾** action_len 位，即在未来帧 token **之后**） | **一致**：轨迹由"未来帧 token 之后的隐状态"解出，即**规划条件里含模型自己对未来的表示** |
| **Policy World Model** | 运动加权 / 视频与轨迹的损失配比 | `configs/sft_navsim/navsim.yaml`：`video_coeff: 0.3`、`tj_coeff: 1.0`、`motion_weight: True`、`nfp_loss: {alpha_coffe: 1.0, beta_coffe: 0.4}`；`modeling_showo.py:441`：`weights_dynamic = amplify_weight * 0.4 + (~amplify_weight) * 1.0` | **一致**：视频损失权重 0.3、轨迹 1.0；**变化 token 权重 1.0、未变 token 权重 0.4** |
| **WorldRFT**（WM-18） | 论文表记"有官方代码" | 仓库仅 `LICENSE` + `readme.md`；readme 原文："I'm currently busy with my courses and unable to organize the code in time. **The code will be sorted out and uploaded soon.**" | **不一致，需更正**：截至 2026-09-23 **无任何代码** |
| **Drive-WM**（WM-01） | 世界模型生成未来图像 + tree-based planner + image reward | 仓库为 **vendored `diffusers`**（`src/diffusers/`），`scripts/` 全是模型转换脚本（`convert_*.py`），顶层为 `pyproject.toml`/`setup.py`/`docs/`/`tests/` 的 diffusers 工程结构 | **部分一致**：图像生成侧（世界模型本体）有实现；**论文的 tree-based planner 与 image reward 不在仓库内** |
| **Drive-WM** | （因此）论文的"选优器"机制 | 仓库内无 planner / reward 相关模块 | **无法代码级核验** |

## B. 组合关系（模块来自哪里）

| 模块 | 来源 | 证据 |
|---|---|---|
| PWM 主干 LLM | **Show-o**（+ `phi-1_5`） | `navsim.yaml`：`showo.load_from_showo: True`、`llm_model_path: '.../phi-1_5'`、`pretrained_model_path: '.../show-o-w-clip-vit'` |
| PWM 视频 tokenizer | **MAGVIT-v2** | `navsim.yaml`：`vq_model.type: "Compressive_magvit_v2"`、`checkpoints/magvitv2`、`num_vq_embeddings: 8192`、`latent_size: 4`、`patch_size: 2` |
| PWM 规划评测 | **NAVSIM + nuPlan devkit** | 仓库内 vendored `navsim/`（含 `traffic_agents_policies/`、`planning/script/config/`） |
| PWM 权重发布 | HuggingFace `zzzz12334/Policy_World_Model` | README「Models」段（Stage 1/2 Tokenizer+Pretrain、Stage 3 nuScenes/NavSim） |
| OccWorld 占据 tokenizer | 自研 `TransVQVAE`（codebook 512） | `model/TransVQVAE.py`、`config/occworld.py:n_e_ = 512` |
| OccWorld 规划损失 | 自研 `PlanRegLossLidar`（3 模式 + GT 模式加权） | `loss/plan_reg_loss_lidar.py` |
| OccWorld 评测口径 | **ST-P3 协议** | `TransVQVAE.autoreg_for_stp3_metric`、`compute_planner_metric_stp3`（含 `plan_L2_{}s`、`plan_obj_col_{}s`） |
| OccWorld 依赖 | mmdet3d / nuScenes 系 | `config/` 下 mmdet3d 风格配置 |

## C. 关键实现细节（本轮静态核验已解决）

| 问题 | 结论 | 证据 |
|---|---|---|
| OccWorld 自回归时，**预测出的未来占据 token 是否回灌**（有无 teacher-forcing 泄漏） | **回灌预测值**：`z_q_ = z_q_[:, -1:].clone().detach().argmax(dim=2)` → `get_codebook_entry` → `z_q_predict = torch.cat([z_q_predict, z_q_], dim=1)`；pose token 同样回灌（`rel_poses = torch.cat([rel_poses, rel_poses_[:, -1:]], dim=1)`） | `TransVQVAE.py:265-270` |
| OccWorld 的**未来驾驶模式**从哪来 | **来自 GT**：`self.decode_pose(rel_poses_[:, -1:], gt_mode[:, i:i+1], rel_poses_sumed)`；评测时 `pred_ego_fut_trajs[gt_mode.bool()]` 直接按 GT 模式选分支 | `TransVQVAE.py:271`、`TransVQVAE.py:453` |
| OccWorld 自回归的起止 | `start_frame=0, mid_frame=6, end_frame=12`：**前 6 帧用 GT 占据 token，后 6 帧自回归生成** | `PlanUtransformer.py:435`、`TransVQVAE.py:214` |
| OccWorld 自回归循环写在哪 | **不在 transformer 里**。`PlanUAutoRegTransformer.forward_autoreg`（435 行）是定义但**未见调用**；`TransVQVAE.forward_autoreg`（334 行）是 `pass` 空壳；真正的循环在 `TransVQVAE.forward_autoreg_with_pose`（214 行），它逐步调 `forward_autoreg_step` | `PlanUtransformer.py:435`、`TransVQVAE.py:334`、`TransVQVAE.py:259-273` |
| PWM 动作 query 如何注入 | **零初始化的可学习 query** 覆盖序列末尾 `action_len` 位：`self.action_queries.weight.data.fill_(0)`、`input_embeddings[:, -action_len:, :] = act_queries` | `modeling_showo.py:92-93`、`modeling_showo.py:416` |
| PWM 轨迹头结构 | 两层：`pred_act_mlps`（ModuleList）+ `pred_trajectory`；入口 `action_forward(x)`。`models/action_head.py` 另有抽象基类 `ActionDecoder` 与实现 `MlpDecoder`（用于 RL/LLaRP 血统的分支） | `modeling_showo.py:113-117`、`models/action_head.py:14,34` |
| PWM 取哪几位隐状态解轨迹 | NAVSIM 分支 `hidden_states[:, -8:]`；另一分支 `hidden_states[:, -6:]` | `modeling_showo.py:449`、`modeling_showo.py:359/368` |

## D. 仍然待核验（需要运行环境或更多阅读）

1. **PWM 的 40 点 vs 8 点口径冲突**：`navsim.yaml` 写 `proposal_sampling.num_poses: 40`，但训练取 `hidden_states[:, -8:]`、`pwm_dataset.py` 的 `compute_targets` 返回 8 点（`num_trajectory_frames=8`）。需读 dataset/评测脚本确认 40 是候选采样数还是最终轨迹长度。
2. **OccWorld 是否有不含 GT 模式的纯推理路径**：`autoreg_for_stp3_metric` 用 GT 模式选分支；若上线推理没有 GT 模式，模式需由模型预测——仓库内未见对应分支。
3. **WorldRFT 的全部主张无法做代码级核验**（无代码）。
4. **Drive-WM 的 tree-based planner 与 image reward 无法做代码级核验**（不在仓库内）。
5. 所有论文的**指标数字**都必须实际运行才能验证——静态检查只能确认"代码里有对应实现"，不能确认"实现了论文声称的效果"。

## E. WoTE 的代码级核验（第二十四轮新增）

仓库 [liyingyanUCAS/WoTE](https://github.com/liyingyanUCAS/WoTE)（ICCV'25）。**未克隆到本地**（与 VLA 侧同策略，走 `raw.githubusercontent.com` 逐文件取证，不占 GitHub API 额度）：`navsim/agents/WoTE/WoTE_model.py`(41,430 B)、`WoTE_agent.py`(8,328 B)、`WoTE_targets.py`(20,441 B)、`configs/default.py`(4,929 B)、`modules/blocks.py`(4,257 B)。

### E.1 主张—代码对照

| 论文主张 | 代码证据（文件 / 行） | 一致性判断 |
|---|---|---|
| 轨迹锚由 **K-means 聚类**得到，数量 **N=256** | `configs/default.py:123`：`num_traj_anchor: int = 256`；`:127` `cluster_file_path = f'.../trajectory_anchors_{num_traj_anchor}.npy'`；`WoTE_targets.py:53`：`self.trajectory_anchors_all = np.load(cluster_file)`；`WoTE_model.py:69`：`self.trajectory_anchors = torch.nn.Parameter(...)` | **一致** |
| 轨迹精修 = 锚 + 交叉注意力 + MLP 回归 offset（**非扩散**） | `WoTE_model.py:362` `_predict_offset`：`offset_tf_decoder(ego_feat, flatten_bev_feature)` → `offset_score_head`；`:675` `trajectory_anchors = self.trajectory_anchors + offset` | **一致**：全仓无扩散日程/去噪步 |
| BEV 世界模型预测未来状态 | `:107` `self.latent_world_model = nn.TransformerEncoder(wm_encoder_layer, num_layers=TRANSFORMER_NUM_LAYERS)`；`:431` `_inject_fut_ego_into_bev(..., fut_idx=8, h=8, w=8)`；`configs/default.py:24` `num_keyval = 64 # 8*8` → **BEV 空间 8×8** | **一致** |
| 奖励模型 = **imitation + simulation 五准则** | `:119` `self.reward_head`（imitation，`:666` `torch.softmax`）+ `:124` `self.sim_reward_heads = nn.ModuleList([...] for _ in range(NUM_SCORE_HEADS))`（`:670` `sigmoid`）；`:723` `assert len(sim_rewards) == 5`，注释原文 `S_NC, S_DAC, S_TTC, S_EP, S_COMFORT` | **一致**，且**与 PDMS 公式同构**——`:730-734` 是 `w[0]·log(im) + w[1]·log(S_NC) + w[2]·log(S_DAC) + w[3]·log(5·S_TTC + 2·S_COMFORT + 5·S_EP)`，即**在 log 空间复现 PDMS 的加权结构** |
| 选优 = 取奖励最高的一条 | `:651` `select_best_trajectory` → `:652` `best_trajectory_idx = torch.argmax(final_rewards, dim=-1)` → `poses = trajectory_anchors[best_idx]` → `:654` `.view(batch_size, 8, 3)` | **一致** |
| 训练需真值（nuPlan 模拟器给 BEV 与规则奖励），推理不需 | `configs/default.py:125` `use_sim_reward: bool = True`、`:126` `sim_reward_dict_path = f'.../formatted_pdm_score_{num_traj_anchor}.npy'`；`WoTE_targets.py:48` `sim_reward_dict = np.load(self.sim_reward_dict_path, allow_pickle=True).item()`、`:82` `sim_reward_dict[token]['trajectory_scores'][0]` | **一致**：规则奖励是**按 token 离线预计算的查表**，推理路径（`forward_test`）不读它 |
| 输出 8 poses @ 2 Hz | `configs/default.py:12` `TrajectorySampling(time_horizon=4, interval_length=0.5)` → `num_poses = 8`；`:654` `poses.view(batch_size, 8, 3)` | **一致** |
| 世界模型预测 **t+2s 与 t+4s 两步**未来状态 | `:110` `self.num_fut_timestep = config.num_fut_timestep if hasattr(...) else 4`，`:306-307` `num_iterations = self.num_fut_timestep`、`interval = 8 // num_iterations`；**但 `configs/default.py:144` `num_fut_timestep = 1`** → `num_iterations = 1`、`interval = 8` → 实际只跑 **`fut_idx = 8`（t+4s）一步** | **需收窄**：代码**支持**多步（改配置即可），但**已发布的默认配置只跑 1 步** → 与 ORION 的 20 模态扩散消融同类（**机制在代码里但被配置关闭**） |
| `use_wm` 开关 | `WoTE_agent.py:47` `use_wm=False` —— **全文件唯一出现处，从未被读取** | **声明未接线**（与 DIVER 的 dummy reward、HDP 的双 LoRA 同类） |

### E.2 组合关系（模块来自哪里）

| 模块 | 来源 | 证据 |
|---|---|---|
| WoTE 主干 | **TransFuser**（navsim 适配版） | 仓库内 vendored `navsim/agents/transfuser/`；论文 Table 3 第一行自称 baseline TransFuser |
| 锚点 + 规则奖励表 | 自研 K-means 脚本 + **nuPlan 模拟器离线打分** | `scripts/misc/k_means_trajs.py`、`scripts/misc/gen_pdm_score.sh`、`trajectory_anchors_256.npy` / `formatted_pdm_score_256.npy`（README 与 Google Drive 均提供） |
| 评测口径 | **NAVSIM + nuPlan devkit v1.2** | README 安装段 `pip install git+.../nuplan-devkit.git@nuplan-devkit-v1.2` |
| 同组前作 | **LAW**（ICLR'25）= 本工作空间 **WM-06** | README「More from Us」原文；两篇同属 Lue Fan / Zhaoxiang Zhang 组 |

### E.3 关键实现细节

| 问题 | 结论 | 证据 |
|---|---|---|
| 奖励模型里的"未来状态"从哪来 | 世界模型每步把**未来自车状态注入 BEV**（注入坐标直接取 `self.trajectory_anchors[:, fut_idx-1, :2]`），再把**各步 BEV 特征沿通道拼接**送进 `reward_conv_net`（`input_channels=(num_fut_timestep+1)*hidden_dim`） | `:431-444`、`:466-481` |
| 训练时评的是锚还是精修轨迹 | **训练喂锚、测试评精修轨迹**——预计算的 BEV 与 PDM 分数都是**锚**的（`WoTE_targets.py` 只按锚采样监督） | `WoTE_targets.py:80-85` + 论文 §4.2 |
| 预计算 PDM 子分数表的结构 | `dict[token]['trajectory_scores'][0][metric_key]`，5 个 key 与 `weighted_reward_calculation` 的 `sim_keys` 一一对应 | `WoTE_targets.py:80-85` |
| 锚点是否随权重发布 | **否**——加载 checkpoint 时**显式删除** `trajectory_anchors`，由 `.npy` 重建 | `WoTE_agent.py:79-80` `del state_dict["agent.WoTE_model.trajectory_anchors"]` |

> **与 DiffusionDriveV2 的结构同构（值得单独记一条）**：WoTE 的 `formatted_pdm_score_256.npy` 是**按 token 预计算的 PDM 子分数查表**，与 DP-A09 DiffusionDriveV2 的 `navtrain_16384.pkl` 是**同一种工程手法**——都是"用离线模拟器给候选轨迹打规则分，把结果当成监督/选优信号"。→ **"用模拟器离线给候选打分"这条路线在扩散侧与非扩散侧各有一个实例**，见 [C003 §E3](../traces/diffusion_planner_code_traces.md)。

## G. DriveLaW 的代码级核验（第二十四轮补充，重点）

仓库 [xiaomi-research/drivelaw](https://github.com/xiaomi-research/drivelaw)（CVPR'26，~32 MB / 2376 文件，最后推送 2026-08-24）。**这是世界模型侧唯一一个把"世界模型 + 扩散规划器"放进同一个 NAVSIM 仓库的工作**，也是本轮最有价值的发现。未克隆，走 `raw.githubusercontent.com` 取证。

### G.1 仓库里同时存在三样东西

| 内容 | 路径 | 说明 |
|---|---|---|
| 自研 agent + 视频世界模型 | `navsim/agents/videodrive/`（`videodrive_agent.py` 22,737 B；`video_models/ltx_models/transformer_ltx.py` 29,702 B、**`transformer_ltx_anchor.py` 30,858 B**；`video_models/pipeline/pipeline_ltx_condition.py` 69,109 B、**`pipeline_ltx_condition_scorer.py` 69,609 B**） | 生成侧是 **LTX 视频模型**；存在 `*_anchor` 与 `*_scorer` 两个变体 |
| **`ReCogDriveDiffusionPlanner`** | `navsim/agents/videodrive/video_models/planner/diffusion_planner.py`(41,923 B)、`lightningdit.py`(9,009 B) | **一个完整的扩散规划器**（`config_class = ReCogDriveDiffusionPlannerConfig`） |
| **DiffusionDrive 基线** | `navsim/agents/diffusiondrive/`（`transfuser_model_v2.py` 22,659 B、`modules/scheduler.py` 等） | 作者在同一仓里保留了 DiffusionDrive 作为对照 |

### G.2 两条并行的"世界模型 → 规划器"接口（**本工作空间首次见到同仓并列**）

**接口 A：动作专家长在视频 transformer 内部**（`VideoDriveAgent`，默认路径）

- 主干确认为 **LTX 视频扩散 transformer**：`video_model_infer_navsim.yaml` 里 `diffusion_model_class: LTXVideoTransformer3DModel`、`diffusion_scheduler_class: FlowMatchEulerDiscreteScheduler`、`num_layers: 28`、`num_attention_heads: 32`、`in/out_channels: 128`、`vae_class: AutoencoderKLLTXVideo`。
- **关键字段**：**`action_expert: true`、`action_in_channels: 3`、`action_num_attention_heads: 16`、`action_attention_head_dim: 32`** → **动作不是外挂头，而是 transformer 内部的一个专家分支**；`train_mode: 'action_full'`、`action_loss_scale: 1.0`、`return_action: true`、**`return_video: false`** → **训练时只出动作、不出视频**；`num_inference_step: 5`、`noise_to_first_frame: 0.0`。
- README 原文把这一步称为 "**Stage 2: Diffusion Planner Imitation Learning**"，并用 **PDM score 在 navtest 上评测**（`run_videodrive_agent_pdm_score_evaluation.sh`）。
- **判断**：这是"**世界模型即规划器**"的一种实现——**与 π0 的 action expert 同构**（工作空间已有其代码核验，见 [transfer.md §1.4](../../topics/diffusion-planner/transfer.md)）。→ 它落在五条接口路线**之外**，应作为**路线 1 的变体**记：不是"未来 token 与 pose token 交替生成"，而是"**同一个扩散 transformer 里既有视频去噪专家、又有动作专家**"。

**接口 B：世界模型隐状态离线缓存 → 独立扩散规划器**（`recogdrive` 路径，**但 agent 未发布**）

- README 的 Step 1 是 `run_caching_videodrive_hidden_state.sh`：用 `agent=videodrive_agent` 把**世界模型的隐状态**跑遍 navtrain 并缓存到 `CACHE_PATH=.../videodrive_agent_cache_dir_final_front`；`run_metric_caching.sh` 再缓存 PDM 指标。
- `run_training_recogdrive.py` 的 `custom_collate_fn` **直接读 `features['last_hidden_state']`**（`rnn_utils.pad_sequence(...)`），特征只有四项：`history_trajectory` / `high_command_one_hot` / **`last_hidden_state`** / `status_feature`，监督信号只有 `trajectory`。→ **"世界模型的隐状态"就是规划器唯一的感知条件**。
- `recogdrive_agent.yaml` 声明 `_target_: navsim.agents.recogdrive.recogdrive_agent.ReCogDriveAgent`，字段含 `sampling_method: 'ddim'`、`dit_type: 'small'`、`cache_hidden_state: True`、`metric_cache_path`、`reference_policy_checkpoint`、`grpo: False`。
- **但 `navsim/agents/` 下只有 `diffusiondrive`、`transfuser`、`videodrive` 三个目录——没有 `recogdrive/`** → **`recogdrive_agent.yaml` 是死引用**，`ReCogDriveAgent` 未随仓库发布。
- **判断**：接口 B 的**数据管线（缓存隐状态）与训练脚本都在**，但**被缓存的隐状态喂给谁（agent 本体）不在**。→ 这是"**声明未接线**"的又一实例，且比 DIVER 的 dummy reward 更隐蔽：**配置与训练脚本都在，缺的是被 `_target_` 指向的那个模块**。

### G.3 `ReCogDriveDiffusionPlannerConfig` 的实测字段（扩散规划器侧的可比数字）

| 字段 | 值 | 意义 |
|---|---|---|
| `action_horizon` | **8** | NAVSIM 8 路点（与工作空间"NAVSIM 评测视野 4.0 s"一致） |
| `sampling_method` | `'ddim'`（默认） | 三种路线并列：**`flow` / `ddpm` / `ddim`**（`FlowConfig` / `DDPMConfig` / `DDIMConfig`，训练步数 **100**） |
| `num_inference_steps` | **5** | 去噪 5 步 |
| `hidden_size` / `input_embedding_dim` | 1024 / 1536 | 规划器宽度 / VLM 侧输入宽度 |
| `ego_status_encoder_type` | `'mlp'` 或 `'attention'` | — |
| **`grpo`** | **`False`（默认）** | GRPO 分支存在但**默认关闭**——与 ORION 的 `use_diff_decoder = False`、HDP 的零权重投影项同类 |
| **`grpo_cfg.scorer_config`** | `PDMScorerConfig(progress_weight=10.0, ttc_weight=5.0, comfortable_weight=2.0)` | **RL 奖励是真 PDM scorer**（另有 `metric_cache_path` 与 `reference_policy_checkpoint`）→ 与 AutoVLA 同类，属"RL 词义核验"清单里**最强的一档** |

> **对研究对象的意义**：DriveLaW 证明了"**视频世界模型 + 扩散规划器**"这条路已被 CVPR'26 工作走通，且**两种接法都试过**（专家内嵌 / 隐状态外挂）。→ 研究对象若做"世界模型 + 扩散规划器"，**接口位的选择本身已有前人对照**；真正剩下的空白仍是 **收益来源拆解**（对应 [transfer.md](../../topics/diffusion-planner/transfer.md) §3 的"共同空白"）。

## H. 由代码得出的判断

1. **"世界模型 → 规划器"已有三条代码级核验的接口路线**：① **token 级联合自回归**（OccWorld：未来占据 token 与 pose token 在同一序列里交替生成）；② **隐状态级条件**（PWM：未来帧 token 先占据序列，轨迹 query 排在其后，读其隐状态）；③ **选优器**（**WoTE**：世界模型预测每条候选轨迹的未来 BEV → 奖励模型打分 → `argmax` 选一条）。① 把未来**显式生成**出来再消费，② 只把未来的**内部表示**喂给规划头，③ 把未来当作**评价候选的依据**——三者的规划器本身都不是生成式。
2. **"世界模型必然慢"在代码层也站不住**：OccWorld 的规划输出是 3 模式 L2 回归（`num_modes=3`），不是迭代采样；其自回归只跑 6 步。WoTE 更进一步——其规划器是**锚 + 一次交叉注意力 + MLP 回归**，自报延迟 **18.7 ms**（L20，256 轨迹，论文 Table 6）。这与论文自报的 18 FPS 方向一致（数字本身待运行验证）。
3. **"选优器"形态的第二个代码级实证，且它与 WM-01 不同**：WM-01（Drive-WM）的选优是**树搜索在 3 个命令间选**（无代码可核验）；WoTE 的选优是**在 256 条候选轨迹上学到的奖励模型打分 + argmax**（代码可核验）。→ 论文表把两者并列时必须区分"**命令级选优**"与"**轨迹级选优**"。
4. **两条负面发现改变了论文表的可信度分布**：WM-18（WorldRFT）的"有官方代码"是错的；WM-01（Drive-WM）的代码范围只有图像生成侧。引用这两篇的机制时，必须标注"无代码可核验"。
5. **"世界模型 + 扩散规划器"已有前人做过，且两种接法都在同一仓里**（DriveLaW，§G）：**接口 A** 把动作专家嵌进视频扩散 transformer（与 π0 同构，训练时 `return_video: false`）；**接口 B** 把世界模型隐状态离线缓存后喂给独立的扩散规划器。→ **对研究对象而言，"接在哪一层"这个问题的答案空间已被别人穷举过**；剩下的真空白是**收益来源拆解**（未来信息是"条件"还是"训练信号"）。
6. **"选优依据"这条路线现有三种代码级核验的实现，且粒度/信号都不同**（§I）：① **学到的奖励模型**（WoTE：256 候选 + imitation/五准则打分）；② **规则 cost volume**（**Drive-OccWorld**：世界模型输出的未来占据 → `instance_occupancy` / `drivable_area` → cost → `topk(largest=False)`）；③ **世界模型自身的损失**（**World4Drive**：重建 + KL + 余弦 → `argmin`）。→ 引用"用世界模型选优"时必须写明是**哪一种信号**。
7. **三家都存在"选择环节用 GT"的问题**（§I）：**OccWorld** 的未来驾驶模式取自 GT（§C 已记）、**Drive-OccWorld** 训练时用 **GT 占据**算 cost、**World4Drive** 的模态分配用 **GT 的 FDE**（`select_optimal_modality`）。→ 这是"选优/模态分配"这一环的**系统性弱点**，不是个别实现问题；引用它们的"多模态"能力时必须标注。

## I. Drive-OccWorld / World4Drive / LAW 的代码级核验（第二十四轮补充）

世界模型侧"代码可用性全表"（[world-model/verification.md §5](../../topics/world-model/verification.md)）确认了另外 3 个"世界模型 + 显式规划器"仓库，本轮一并核验（**均未克隆**，走 `raw.githubusercontent.com`）。

### I.1 WM-04 Drive-OccWorld：**占据进入 cost volume**——"选优依据"的规则版

| 问题 | 结论 | 证据 |
|---|---|---|
| 世界模型的未来预测怎么进规划器 | **不是与 pose token 联合生成**，而是**单独预测未来语义占据 → `argmax` 成类别图 → `detach()` → 送进规划头** | `drive_occworld.py:339` `ref_sem_occupancy = self.future_pred_head.forward_head(ref_bev.unsqueeze(0).unsqueeze(0))[-1, -1, 0].argmax(-1).detach()`；`:342` `self.plan_head(ref_bev, ref_sample_traj, ref_sem_occupancy, ref_command, ref_real_traj)` |
| 占据在规划头里做什么 | 算 **`instance_occupancy`**（实例类）与 **`drivable_area`**（可行驶区），二者进 `Cost_Function` → **cost volume 选优** | `plan_head.py:363-366` `torch.isin(sem_occupancy, self.instance_cls).float().max(-1)[0].detach()`；`:181` `self.cost_function = Cost_Function(plan_grid_conf)` |
| 怎么选 | **取 cost 最小的候选** | `:319` `CC, KK = torch.topk(CS, k, dim=-1, largest=False)`；`:322` `select_traj = trajs[ii[:,None], KK]` |
| cost 怎么学 | **hinge：要求 GT 轨迹的 cost 低于采样轨迹** | `:301-305` `gt_cost_fo = cost_function(cost_volume, gt_trajs)`、`sm_cost_fo = cost_function(cost_volume, trajs)`、**`L = F.relu(gt_cost_fo - sm_cost_fo)`** |
| 候选轨迹从哪来 | 预采样候选按 **3 个 command 均分**（`self.num = int(self.sample_num / 3)`） | `:190`、`:342-347` |
| 训练/推理的占据来源不同 | **训练用 GT 占据、推理用预测占据** | `:338` 注释原文 "use pred_occupancy to calculate sample_traj cost during inference, **GT_occupancy during training**"；`:657` 注释 "using GT occupancy to calculate sample_traj cost during training" |
| 规划视野 | **`planning_steps = 1` → 逐帧滚动**（`pred_under_ref = torch.cumsum(outs_planning, dim=1)`） | `plan_head.py:234`、`drive_occworld.py:522` |
| 两个 head 版本 | **`PlanHead_v1` 用 sem_occupancy 区分类别**（"fine-grained_MMO"）；**`PlanHead_v2` 不用占据**（"inflated_GMO"） | `drive_occworld.py:337/343/417/429` |

**组合关系（负面发现）**：**规划损失直接抄自 UniAD**——`losses/planning_loss.py` 的文件头原文是 `UniAD: Planning-oriented Autonomous Driving (https://arxiv.org/abs/2212.10156) / Source code: https://github.com/OpenDriveLab/UniAD / Copyright (c) OpenDriveLab`；其 `CollisionLoss.inter_bbox` 仍是 **min/max → 轴对齐包围盒**，与 [C005 §G](e2e_trunk_code_traces.md) 记录的 **UniAD 训练侧退化完全一致**。

### I.2 WM-07 World4Drive：**世界模型损失当"模态分配准则"**

| 问题 | 结论 | 证据 |
|---|---|---|
| 组合关系 | **`class W4D(VAD)` —— 直接继承 VAD** | `W4D/W4D.py:21` |
| 损失配比 | `wm_loss_weight = 0.2`、`semantic_loss_weight = 0.05` | `W4D.py:35/61` |
| 世界模型的损失族 | `loss_reconstruction` / **`loss_kl`** / `loss_cosine` / `loss_wm_diversity` / `loss_traj_diversity` | `waypoint_query_decoder_simple.py:440-543` |
| **模态怎么选** | **用"世界模型损失 + GT 的 FDE"综合最小者**：`loss_rec = 重建 + KL + 余弦`；`total_loss = loss_rec*wm_loss_weight + tm_loss_tensor*weight_tm`；**`best_modality_idx = total_loss.argmin(dim=-1)`** | `:605-628` `select_optimal_modality(...)` |
| **关键限定** | **FDE 项与 GT 比**（`torch.norm(pred_traj_i[:,-1,:] - gt_trajs[:,-1,:])`）→ **这是训练期的模态分配，不是推理期选优**；测试走 **`best_traj_idx = torch.argmax(cur_waypoint_cls, dim=1)`** | `:618`、`:404` |
| 锚点 | `np.load('data/kmeans/kmeans_plan_6.npy')` → **6 模式锚点，与 SparseDrive 同名文件** | `:212` |
| **形状疑点（需运行确认）** | `tm_loss_tensor = torch.cat(tm_loss_list, dim=0)` 把 B 个长度张量沿 dim=0 拼接 → 得 `[B*num_modalities]`，与 `loss_rec_tensor` 的 `[B, num_modalities]` 相乘**只在 B=1 时成立** | `:620-623` |

> **与 OccWorld 的对照**：两者都**把"哪个模态/模式该被监督"交给 GT 侧**（OccWorld 用 GT 模式选分支、World4Drive 用 GT 的 FDE）——但 World4Drive **额外把世界模型损失加进了选择准则**，即"**能让世界模型更好预测未来的模态更可信**"。这是本工作空间见到的**唯一一种用世界模型损失做选择的实现**。

### I.3 WM-06 LAW：**动作条件世界模型 + 潜空间重建**

| 问题 | 结论 | 证据 |
|---|---|---|
| 世界模型以什么为条件 | **以自车 waypoint 为动作条件**：`action_aware_encoder(cat([view_query_feat, cur_waypoint]))` → `_wm_decoder(...)` → 预测下一帧潜状态 | `LAW/dense_heads/waypoint_query_decoder.py:239-246` `wm_prediction(view_query_feat, cur_waypoint)` |
| 重建目标是什么 | **重建的是 view query 特征，不是像素/占据** | `:232-237` `loss_reconstruction(reconstructed_view_query_feat, observed_view_query_feat)` |
| 规划输出 | 轨迹回归（`loss_plan_reg`） | `:248-256` `loss_3d` |
| **一处更正** | `VAD/utils/CD_loss.py` **不是"对比蒸馏"**——它是**轨迹点损失集合**（`ordered_pts_smooth_l1_loss` / `pts_l1_loss` / `ordered_pts_dir_cos_loss` / `OrderedPtsSmoothL1Loss` 等） | `CD_loss.py` 全文类名与 `@LOSSES.register_module()` |

> LAW 的"**perception-free**"在代码层的准确含义是：**世界模型与规划都在 view query 特征空间里做，重建目标也是特征**，不解码回像素或占据。→ 与 PWM（隐状态级条件）和 WM-08 DLWM（潜特征）同属**潜空间路线**，但 LAW 的**动作条件是显式 waypoint**。

### I.4 本节结论

- **"选优依据"这条路线现在有三种代码级核验的实现**：**学到的奖励模型**（WoTE）/ **规则 cost volume**（Drive-OccWorld）/ **世界模型自身的损失**（World4Drive）。→ 引用"用世界模型选优"时**必须写明信号类型**。
- **"选择环节用 GT"是三家共有的系统性弱点**：OccWorld（GT 模式）/ Drive-OccWorld（训练用 GT 占据）/ World4Drive（GT 的 FDE）。→ 这直接影响"多模态"主张的可信度。
- **代码复用谱系又添一环**：Drive-OccWorld 的**规划损失抄自 UniAD**（含轴对齐退化），World4Drive **继承 VAD**（锚点 `kmeans_plan_6.npy` 同名），LAW **长在 VAD 代码库上**（`VAD/VAD_head.py`）。→ **"4D 占据/潜世界模型"这一支的实现大多寄生在 nuScenes 系 E2E 主干代码上**，与 [C005](e2e_trunk_code_traces.md) 的谱系一致。

## J. WM-20 DrivingGen 的代码级核验（第二十四轮新增）——一个"轨迹指标由感知反推"的评测基准

仓库 [youngzhou1999/DrivingGen](https://github.com/youngzhou1999/DrivingGen)（**ICLR'26**，Apache-2.0，`size` 62461 KB，`pushed_at` **2026-03-13**，`created` 2026-01-06，42 stars）。它是世界模型侧**唯一还有代码但未核验**的一篇，也是本表 WM-20 的定位（"生成式视频世界模型的评测基准"）。未克隆，走 `raw.githubusercontent.com` + trees API 取证。

### J.1 它评的是什么（逐项核实）

| 问题 | 结论 | 证据 |
|---|---|---|
| 评"生成质量"还是"规划有效性" | **以生成质量为主，附带"轨迹合理性"**。**没有任何"把生成视频喂给下游规划器"的接口** | 在 `drivinggen/` 的 23 个 `.py` 里 grep `planner｜plan_head｜pdm_score｜navsim` **零命中** |
| **它的"轨迹"从哪来** | **从生成视频里用感知栈反推出来**——**自车轨迹**用 **UniDepth + Visual SLAM**；**其他 agent 轨迹**用 **UniDepthV2 + YOLOv10 + SAMURAI** | `extract_traj_ego_unidepth.py:15-25`（`from unidepth.models import UniDepthV1, UniDepthV2`、`from visual_slam.vo import *`、`from ultralytics import YOLOv10`）；`extract_traj_agent_unidepth.py:40-71`（`init_depth_model` 加载 unidepth-v2-vitl14、`init_det_model` 加载 yolov10x.pt）、`:118-136`（像素+深度+内参+位姿 → 3D 轨迹）、`:461`（SAMURAI 跟踪） |
| 视频侧指标 | FVD(`fvd2048_100f`)、**IEEE P2020 客观质量**（mtf50 / mtf10 / CTA / edge_rise_time / total_distortion / flare / gradient_entropy / blur_extent / chroma_aberration 等）、CLIP-IQA+、**DINOv3 场景一致性**、agent 外观一致性、agent missing、LPIPS / SSIM | `video_distribution.py`、`p2020_v2.py`、`video_sub_q.py`、`video_v_consist.py`、`video_a_consist.py`、`video_a_missing.py`、`lpips_metric.py`、`ssim_metric.py` |
| 轨迹侧指标 | **FTD**、`traj_quality`（comfort / curvature_rms / speed）、`traj_consistency`、**ADE**、**DTW**；对齐用 **Umeyama SVD（`scale=False`）+ SG 平滑** | `traj_quality.py`、`traj_consistency.py`、`traj_alignment.py`、`z-sample_ftd.py:386-433` |
| 外部依赖 | UniDepthV2、**DINOv3**、**Cosmos-Reason1-7B**（做 agent missing 判断）、CLIP-IQA+（pyiqa）、SEA-RAFT（光流）、stylegan-v（FVD）、MTR（FTD 编码器）、Wan2.2-I2V-A14B（示例生成器） | `video_v_consist.py:57`、`video_a_missing.py:117`、`video_sub_q.py:22-24`、`traj_distribution.py:27,299`、`infer_example_wan.py:110` |
| 数据集 | HuggingFace `yangzhou99/DrivingGen` | `down_dataset.py:6-10` |
| 代码规模 | 1274 blob；`.py` **627**（`drivinggen/` 23 + `third_parties/` **604**）；`third_parties/` 共 **1240** blob = **7 个整仓 vendor**（yolov10 501、samurai 213、UniDepth 200、cosmos-reason1 123、stylegan-v 90、SEA-RAFT 58、MTR 55） | trees 统计 |

### J.2 四条硬发现

1. **它的"轨迹指标"不是规划器指标，而是"感知反推指标"**：ADE / FDE / DTW / traj_consistency 的评价对象是**"用 UniDepth + Visual SLAM 从生成视频里反推出来的自车轨迹" vs GT**。→ **误差里混入了这套感知栈自身的误差**。引用 DrivingGen 的"轨迹合理性"数字时**必须标注这一层**；**它不能用来评价"生成式规划器"**（与 [benchmarks.md](../../direction/benchmarks.md) 的 NAVSIM/PDMS 完全不是一回事）。
2. **没有任何 planner-in-the-loop 接口**：全仓（含 7 个 vendored 仓库）**没有**把生成的未来帧输入规划器/下游决策的代码。→ **"世界模型 → 规划器"这条接口在本仓库里不存在**；这与 §E/§I 的"五条接口路线"是不同层面的东西——**DrivingGen 只评"生成得像不像"，不评"生成得有没有用"**。
3. **代码明显未收尾**：**6 处未注释的 `pdb.set_trace()`**（`extract_traj_agent_unidepth.py:374`、`extract_traj_ego_unidepth.py:378`、`p2020.py:402`、`traj_distribution.py:323`、`video_a_consist.py:250`、`video_v_consist.py:144`）+ **硬编码作者本机绝对路径**（`extract_traj_agent_unidepth.py:71` 的 `/shared_disk/users/yang.zhou/iclr_open_source/DrivingGen/ckpt/yolov10x.pt`、`:375` 的 `/mnt/cache/zhouyang/dg-bench/nuplan_1.1/val_sensor_data_10hz_0530`）。→ 与 DIVER 的"未清断点"同类，但**规模更大**。
4. **agent 轨迹评测在驱动脚本里被注释掉**：`z-sample_ftd.py:352-356` 的 `if args.metric == 'a_consist' or args.metric == 'a_missing' or args.metric == 'all':` 整段被注释 → **agent 外观一致性 / missing 这两项在 FTD 驱动路径上不会被执行**（**机制在代码里但被注释关闭**，与 ORION 的 `use_diff_decoder=False`、WoTE 的 `num_fut_timestep=1` 同类）。

**另注**：**仓内无任何权重文件**（树里 `.pt/.pth/.ckpt/.safetensors` **0 个**），三个关键 ckpt（YOLOv10 / MTR / SEA-RAFT）需自行获取 → **开箱不可运行**。

### J.3 对研究对象的判断

- **DrivingGen 对本项目的直接可用性低**：它评的是"生成视频的质量与几何合理性"，**不是规划有效性**；且其轨迹指标依赖一套额外的单目深度 + SLAM + 检测 + 跟踪栈，**可复现性受这些外部模型版本牵制**。
- **但它给出一个有用的方法论警告**：**"用生成模型的输出反推下游量再打分"这种评测方式，会把感知误差混进指标里**——这正是 [benchmarks.md §2](../../direction/benchmarks.md) 记录的 NAVSIM 问题（EP 是批内相对分、EPDMS 权重以本方法终点为中心）的**另一种形态**。→ 本项目若要评"生成式规划器"，**不能走"从输出反推"这条路**。
- **对 WM 表的补正**：WM-20 的"评价工具"定位成立，但**"评测工具"要限定为"生成质量 + 几何合理性"，不含规划有效性**；且其代码**开箱不可运行**（无权重 + 未清断点 + 硬编码路径）。
