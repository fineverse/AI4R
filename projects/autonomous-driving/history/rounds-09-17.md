# 自动驾驶项目 · 逐轮工作记录 · 第九至第十七轮

本卷范围：**第九至第十七轮**。内容：文献质量规范 + VLA / 世界模型第一轮、代表工作全文消化、世界模型源码级分析、非生成式基线规划头、三个"非锚点"扩散规划器、PC-Diffuser、HDP、DriveFine、锚点/词表公开渠道。
索引见 [../history.md](../history.md)；当前状态见 [../state.md](../state.md)。

---

## 第九轮（文献质量规范 + VLA / 世界模型第一轮，2026-09-23）

- **新建 [文献质量分档规范](../../../shared/literature-quality.md)**：解决"预印本无 venue、无引用如何判断"。核心结论是**不给预印本算分，只分 T1–T5 档 + 标注可复核依据**；因为引用数对 <12 个月的工作天然无效
- 规范含**领域白名单**，补齐 CCF 目录的缺口——实测 CCF 把 ECCV 压到 B、IROS 压到 C，且 **CoRL / RSS / WACV / IEEE IV / ITSC / TIV / RA-L / IJRR / TMLR 完全不在目录内**
- **关键方法**：先查 arXiv `comments` 字段"救出假预印本"。实测 68 篇候选里 44 篇有标注，其中十余篇已录用（CVPR'26 / NeurIPS'25 / ECCV'26 / AAAI'25 / ICLR'25…），直接升入 T2
- **检索**：12 组 arXiv 查询、去重 **510 篇**（2026 年 226、2025 年 173）；读 4 篇综述全文（[2506.24044](https://arxiv.org/abs/2506.24044)、[2512.16760](https://arxiv.org/abs/2512.16760)、[2501.11260](https://arxiv.org/abs/2501.11260)、[2502.10498](https://arxiv.org/abs/2502.10498)）提取两套分类框架
- **产出**：[VLA 论文表 18 篇](../topics/vla/papers.md) + [VLA 薄脉络](../topics/vla/lineage.md)（四阶段）；[世界模型论文表 20 篇](../topics/world-model/papers.md) + [世界模型薄脉络](../topics/world-model/lineage.md)（五类预测空间）
- **回填** [transfer.md](../topics/diffusion-planner/transfer.md) 第 2、3 节：VLA 侧 5 条、世界模型侧 6 条机制，全部标注证据等级与障碍
- **两处关键接口结论**：① VLA 的"**双系统分离**"（慢推理 + 快生成）是对研究对象最可借鉴的设计；② 世界模型侧只有 **WM-09 DriveFuture（= DP-A31）**与研究对象直接同构，其收益来源（信息更多 vs 训练信号更好）**未被拆解，是可做实验的空白**
- **受限项**：检索末段 arXiv 与 OpenAlex **双渠道同时限流**（OpenAlex 当日额度耗尽、arXiv 429），8 篇世界模型代表工作未取到 arXiv ID，已列入 [papers.md](../topics/world-model/papers.md) §3 待补
- **状态文件拆分**：`state.md` 已达 99 行预算上限，逐轮记录迁入本文件；`state.md` 只保留当前阶段 / 下一步 / 判断边界

## 第十轮（消化代表工作全文，2026-09-23）

- **范围**：从 VLA（18 篇）与世界模型（20 篇）两张表中挑 **12 篇**优先下载全文，实际完成 **8 篇**的全文阅读与单篇笔记
- **VLA 侧 3 篇**（与研究对象直接同构）：
  - [VLA-06 DiffVLA](../topics/vla/notes/VLA-06-diffvla.md)：**性质澄清——它是 Bosch 的 NAVSIM v2 竞赛技术报告，不是正式论文**；锚点 **32 个**（vs DiffusionDrive 20）；**加了扩散规划器后碰撞（95.71→81.27）与车道保持（97.14→59.85）子指标反而显著变差**；靠"y 轴 2% 减速"后处理避碰
  - [VLA-07 ReCogDrive](../topics/vla/notes/VLA-07-recogdrive.md)：**推理 13.3 Hz**（VLM 直出轨迹只有 0.9–1.7 Hz）——**回答了 VLA 侧最关键的延迟问题**；NAVSIM PDMS **90.8 纯相机**，超相机+LiDAR 的 DiffusionDrive +2.7；但 Bench2Drive **Comfort 仅 17.45**
  - [VLA-08 KnowDiffuser](../topics/vla/notes/VLA-08-knowdiffuser.md)：把 **GPT-4o 放进规划回路**；nuPlan Test NR 86.94 / R 81.10；**未与 DP-A01 对比**；只给定性延迟声明
- **世界模型侧 5 篇**：
  - [WM-01 Drive-WM](../topics/world-model/notes/WM-01-drive-wm.md)：规划用法是**树搜索在 3 个候选命令间选优**，不生成轨迹——**第三种形态**；选优把随机命令碰撞率 **0.93%→0.26%**，接近 GT 命令 0.22%
  - [WM-03 OccWorld](../topics/world-model/notes/WM-03-occworld.md)：**18 FPS** 且规划指标优于 UniAD（1.8 FPS）——**证明"世界模型必然慢"不成立**，慢的是解码回像素
  - [WM-06 LAW](../topics/world-model/notes/WM-06-law-latent-world-model.md)：**无感知输入即可提升规划**；顺带解决了一个待补项（LAW = arXiv 2406.08481）
  - [WM-17 Policy World Model](../topics/world-model/notes/WM-17-policy-world-model.md)：**40 FPS（单目相机）**；**未来帧 10 帧最优**；**量化了权衡——未来帧条件买到安全性（NC↑），代价是进度（EP↓）**
  - [WM-18 WorldRFT](../topics/world-model/notes/WM-18-worldrft.md)：批评"重建导向表征把感知与规划纠缠"；nuScenes 碰撞率 **0.30%→0.05%（−83%）**；但**轨迹仅 2 Hz，非实时**
- **回填**：[transfer.md](../topics/diffusion-planner/transfer.md) 第 2、3 节按全文重写——世界模型侧从"全部待验证"变成**有两条可量化结论**（未来帧条件的收益/代价、世界模型当选优器的实测价值）；VLA 侧的延迟空白有了实测答案
- **两张论文表**各新增「已读全文」小节，标注 8 篇的升级与关键新增事实
- **未完成**：预定的另外 4 篇（OpenDriveVLA / DriveMoE / AutoVLA / DriveDreamer 系）未读；两表合计仍有 **30 篇为摘要级**。已记入 [state.md](../state.md) 待续清单

## 第十一轮（世界模型侧源码级静态分析，2026-09-23）

- **动因**：代表工作的全文已读，下一步能做的是**代码级核验**——论文自述的机制在代码里到底长什么样
- **新增 4 个仓库**（[repositories.md](../code/repositories.md) 32 → **36 个**，约 1.6 GB）：`OccWorld`（42M，tarball）、`Policy-World-Model`（29M）、`Drive-WM`（22M）、`WorldRFT`（208K）
- **新增产出**：[code/traces/world_model_code_traces.md](../code/traces/world_model_code_traces.md)（主张—代码对照 9 项 + 组合关系 8 项 + 实现细节 7 项 + 负面发现 2 项 + 判断 3 条）
- **核心问题与答案**："世界模型的未来预测以什么形式进入规划器？"——**两条根本不同的接口路线**：
  - **token 级联合自回归**（OccWorld）：未来占据 token 与自车 pose token 在**同一序列**里逐步交替生成（`TransVQVAE.forward_autoreg_with_pose` 的 `for i in range(mid_frame, end_frame)` 循环）；预测 token **回灌**、无 teacher forcing 泄漏；规划是 **3 模式 L2 回归**（`PlanRegLossLidar(num_modes=3)`），**不是生成式**
  - **隐状态级条件**（Policy World Model）：`models/modeling_showo.py:navsim_forward` **一次前向**同时产出未来帧 token 交叉熵与轨迹 L1；轨迹 query 排在**未来帧 token 之后**（`input_embeddings[:, -action_len:, :] = act_queries`），规划头读 `hidden_states[:, -8:]`；损失配比 `video_coeff: 0.3` / `tj_coeff: 1.0`
- **两条负面发现（更正论文表）**：
  1. **WM-18 WorldRFT 的官方仓库为空**——仅 `LICENSE` + `readme.md`，readme 称代码 "soon" 上传。论文表原记"有官方代码"**是错的**，已更正
  2. **WM-01 Drive-WM 的仓库只含图像生成侧**（vendored `diffusers` + 转换脚本），其 **tree-based planner 与 image reward 不在仓库内**——这条最有价值的"选优器"机制**无代码可核验**
- **一处待核验的口径冲突**：PWM 配置写 `proposal_sampling.num_poses: 40`，但训练取 `hidden_states[:, -8:]`、dataset 的 `compute_targets` 返回 8 点——40 是候选数还是最终轨迹长度，需运行或细读 dataset 才能定
- **一处需注意的评测口径**：OccWorld 的规划评测路径（`autoreg_for_stp3_metric`）**用 GT 驾驶模式选分支**（`pred_ego_fut_trajs[gt_mode.bool()]`），仓库内未见不含 GT 模式的纯推理分支
- **回填**：[transfer.md](../topics/diffusion-planner/transfer.md) 第 3 节补「代码级补充」段——把 WM-01/17/18 三条机制的**代码可核验程度**分开标注（WM-17 可核验且比论文更具体，WM-01/18 不可核验）
- **追加：NAVSIM 指标实现的代码级核验**（读 `navsim` 仓库 commit `0a380a9`）——解决了工作空间里反复出现的"指标口径不一致"问题：
  - **PDMS**：`(NC × DAC) × [(5·EP + 5·TTC + 2·C) / 12]`；**NC 不是二值**（撞 `AGENT_TYPES` 记 0.0、否则 0.5）；"自车责任"有明确判定规则（仅 `ACTIVE_FRONT`/`STOPPED_TRACK`，或横向碰撞且自车在多车道/非可行驶区）；TTC 只在 1 s 窗口内每 0.3 s 采样
  - **EPDMS 的四处改动**：乘法项 +DDC/+TLC；加权项 +LK/+HC；C 被 HC+EC 取代；新增假阳性过滤 `filter_m(agent, human)`
  - **两条使跨论文数字不可比的机制（新发现）**：① `_aggregate_pdm_scores` 中 `norm_constant_progress = np.max(masked_progress)`——**EP 按本批候选的最大进度归一化，是批内相对分**，候选集一变分数就变；② `SceneAggregator` 用高斯核 `exp(-d²/(2σ²))`、**σ² = 0.1（σ ≈ 0.32 m）**，距离是**本方法自己第一阶段的终点**与第二阶段跟进场景起点之差——**换方法即换权重**
  - **顺带更正一处**：[benchmarks.md](../direction/benchmarks.md) 原写"v2 navtest EPDMS 分数普遍高于 v1"，与工作空间自己的数据矛盾（DriveFuture v1 PDMS 90.7 / v2 EPDMS 89.9），已改为"接近但不系统性更高"
  - 写入 [direction/benchmarks.md §2](../direction/benchmarks.md)（新增 2.2–2.4 三节）
- **追加：DiffusionVeteran（DP-S14，ICLR'25 Spotlight）的代码级核验**——回填 [C003](../code/traces/diffusion_planner_code_traces.md)（对照 10→**11 项**、组合关系 6→**7 项**、实现细节 5→**7 项**，新增 §E 判断 2 条）：
  - **三条引导路线在同一 planner 上并列实现**：`guidance_type` = `MCSS`（**无引导**采样 `num_envs×50` 条 → 用 `DVHorizonCritic` 的 `argmax` 选一条）/ `cfg`（按目标回报做 classifier-free guidance，不重采样）/ `cg`（classifier guidance + 按 `log["log_p"]` 选一条）
  - **给出 transfer.md 里一处矛盾的对齐口径**：第 1 节原记"CFG 优于 Q 引导（DP-E02）与 DiffusionDriveV2/DIVER 的 RL 引导做法相反"——代码显示**"引导"与"选优"是两件事**：DP-E02 批评的是"用离线 Q 做引导"，而 MCSS 是"无引导 + 用 critic 选优"。已改写该行
  - **9 维消融网格可复用**：`planner_net`（transformer/unet）、`pipeline_type`（separate/joint）、`rebase_policy`、`use_diffusion_invdyn`、`planner_solver`（ddim）、`planner_sampling_steps`（20）、`policy_diffusion_steps`（10）、`planner_num_candidates`（50）等，与驾驶侧扩散规划器大部分同构，可作为实验协议起点
  - **边界**：只确认"三条路线都有可运行实现"，**不确认**论文"无引导 + 选择优于引导"的结论（6000+ 模型的结论表未在核验范围内）
- **追加：解决 C003 的一个待核验项——V2 的 16384 轨迹词表做什么用**（读 `diffusiondrivev2_model_sel.py`）：
  - 它是**预计算的 PDM 子分数查找表**（`gtrs_traj/navtrain_16384.pkl` + `16384.npy`），权重与 NAVSIM 一致：`NC × DAC × (5·TTC + 5·EP + 2·C)`
  - 关键：**词表轨迹本体被拼进同一个候选池**（`diffusion_output = torch.cat((diffusion_output, vocab), dim=1)`），再由 coarse scorer → **top-32** → fine scorer 统一选优
  - **由此得出的判断（新增 C003 §E 第 3 条）**：**V2 的最终输出可以是一条词表轨迹而非扩散样本**——所以它 91.2 的分数**不能当作"扩散生成机制本身"的能力证明**，引用时必须区分"生成器贡献"与"选优器贡献"。这条同时改写了一个原 §D 待核验项（"词表与锚点如何共同作用"）
- **追加：E2E 主干 13 个仓库的完整性全扫 + 词表机制谱系**（新建 [e2e_trunk_code_traces.md](../code/traces/e2e_trunk_code_traces.md)）：
  - **完整性核验**：逐个统计 `.py` 文件数 → **2 个零代码**：`Hydra-MDP`（仅 README + 一张图，自述因公司政策延迟发布）、`DriveVLM`（仅 `index.html` + 图片 + PDF，**是项目主页不是代码仓库**）。另有 `VADv2` 部分发布（只有 config + head）、`imitation-learning` 仅 5 个 `.py`
  - **主张—代码对照 5 项**：VAD v1 = **单模回归**（`ego_query = nn.Embedding(1, ...)`）；VADv2 = 4096 词表 + **纯分类**，且 **`outputs_ego_trajs = outputs_ego_trajs * 0. + used_plan_anchors`——回归分支被乘 0 丢弃**；VADv2 已发布配置里**冲突项与回归项权重全为 0**，只剩 `loss_plan_cls_expert`（权重 **200**）
  - **「轨迹词表 / 锚点」机制谱系 5 环（本轮最有价值的产出）**：① VAD 单模回归 → ② **VADv2 纯词表分类**（2024-02）→ ③ Hydra-MDP 沿用（**代码断点**）→ ④ **DiffusionDrive 把词表改成扩散起点**（锚点 + 极低噪声）→ ⑤ **V2 词表与扩散输出拼进同一候选池**。→ **"多模态候选 + 先验词表"不是扩散带来的；扩散的独特性只在第 ④ 环成立**
  - **实现细节 7 项**：VADv2 训练时从 4096 条随机取 256 条并把 GT 最近锚点强行塞入；`kinodynamic_mask` 阈值写成 **1e11**（等价于不过滤）；词表第 0 条固定为"停住"；`v116ADTRHead` **全仓未注册**
  - **词表文件缺失**：VADv2 的 `carla_plan_vocabulary_4096.npy`（VAD 全仓 0 个 `.npy`）与 DiffusionDrive 的 `kmeans_navsim_traj_20.npy`（配置里只有作者本机绝对路径）**都未随仓库发布**；V2 有 `16384.npy`（**(16384, 40, 3)**，由字节数 7,864,448 反推确认）但缺 `gtrs_traj/navtrain_16384.pkl`
  - **回填**：[repositories.md](../code/repositories.md) 新增「在列但实际无代码 / 代码不全」表并把选择标准改为"**已克隆核验代码存在**"；[direction/lineage.md](../direction/lineage.md) 的基线表逐条标注代码完整性；[E2E-02/03/05/10 笔记](../direction/notes/)各补「代码核验」小节
- **追加：DP-A01（Diffusion Planner）的引导实现核验**（读 `model/guidance/`、`sampling.py`、`decoder.py`）：
  - **需更正**：论文 Eq.8 的能量函数含**目标车速 / 舒适 / 避碰 / 可行驶区域四项**，但已发布代码里 **`_guidance_fns = [collision_guidance_fn]`——只有避碰一项**；`model/guidance/` 下只有 `collision.py` + 一篇教用户自己加引导的 `documentation_guidance.md`
  - **引导只作用于扩散末段**：`mask_diffusion_time = (t < 0.1 and t > 0.005)`，区间外梯度被 `x.detach()` 切断
  - **引导强度硬编码**：`collision.py` 返回 `3.0 * reward` × `decoder.py` 的 `guidance_scale=0.5` = 有效 **1.5**
  - **噪声起点非标准高斯**：`current_states + randn * 0.5`（尺度 0.5）；并用 `correcting_xt_fn` **每步把第 0 帧重置为当前状态**
  - **解决了原笔记两个待核验项**：① 去噪步数 = **10**（DPM-Solver++ / order=2 / logSNR / multistep / denoise_to_zero）；② README 表里的 "refine" 是 **nuPlan 闭环评测口径**，与仓库内 `data_augmentation.py` 的**五次样条插值**（同名 `refine_horizon`）无关
  - **顺带更正一条文献记录**：上游 README 直链 **Flow Planner（NeurIPS 2025）= `DiffusionAD/Flow-Planner`**，而论文表把 **DP-A11 记作"未见官方"是错的**，已改正并尝试补克隆
- **追加：DP-A11 Flow Planner 的仓库核验**（部分成功）：
  - **确认有官方代码 + 权重**：`DiffusionAD/Flow-Planner`，权重在 HuggingFace `ttwhy/flow-planner`
  - **代码本体未获取**：git clone 10 次重试全部卡在 TLS 握手；codeload tarball **稳定在 4,493,317 字节处被截断**（`gzip -t` 失败，3 次重试同一大小）→ 判定为**网络阻塞而非重试问题**，按纪律停止。**只取到 `README.md`**（顶层文件在 tarball 前部）
  - **README 带来的四条事实**：① 与 **DP-A01 同组**（前两位作者 Tianyi Tan、Yinan Zheng 相同），是 Diffusion Planner 的直接后续；② nuPlan Val14 NR/R **90.43/83.31**、Test14-hard **76.47/70.42**，**学习类方法中最高**（超 Diffusion Planner 89.87/82.80、75.99/69.22）；③ InterPlan Overall **61.82**（vs Diffusion Planner 52.90、PlanTF 47.70）；④ 其 BibTeX 顺带确认了 **DP-A01 的 venue = ICLR 2025**（原笔记记"录用信息未获取"）
  - **新增一条下载经验**：codeload 在本机可能中途截断，**必须用 `gzip -t` 校验**，不能只看文件非空（已写入 [repositories.md](../code/repositories.md) 下载方法第 5 条）
- **追加：同基准可比性的代码级核验（C003 新增 §F）**——把"backbone 不同不可横比"从定性说法变成**逐项对照表**（四个 NAVSIM 扩散规划器：DiffusionDrive / V2 / MeanFuser / GoalFlow）：
  - **DD 与 V2 的 `transfuser_config.py` 逐字节完全相同**（`diff` 无输出），agent yaml 也只覆盖 `trajectory_sampling` 与 `latent`。→ **V2 的 91.2 vs DD 的 88.1 可直接归因于"RL 后训练 + mode selector"**，是本项目**唯一一对主干完全对齐**的工作
  - **MeanFuser 与 DD 不齐**：`MeanfuserConfig.tf_d_model = 128`（DD 256）、agent yaml 覆盖 `lidar_seq_len: 4`（DD 1）；其 `navsim/agents/transfuser/` 是 **vendored TransFuser 基线，不被 MeanfuserAgent 使用**
  - **GoalFlow 与 DD 不齐**：agent yaml 覆盖 `tf_d_model: 512`（DD 256），轨迹 **11 点 / 5.5 s**（DD 8 点 / 4 s）
  - **评测视野四者统一为 4.0 s**（scorer/simulator 的 `proposal_sampling = 40 poses @ 0.1 s`）；GoalFlow 的**训练目标是 5.5 s / 11 点**，但**模型在输出前就切成前 8 点**（`goalflow_model_traj.py:407-410`），`Trajectory.__post_init__` 也断言必须是 8 点——**最后 1.5 s 不打分却参与训练**（口径差异成立，机制是模型侧截断）
  - **MeanFuser 的"去词表"主张得到代码确认**：配置类里**无任何锚点/词表字段**，改为 `noise_type='multi_gaussian'` + `navtrain_8_mean_std.pkl`（K=8）
  - **回填**：[benchmarks.md §3 第 2 条](../direction/benchmarks.md)改为可核对清单；DP-A02/A03/A09/A14 四篇笔记各补「代码核验」小节，并解决了它们的 4 个待核验项（DD 的训练损失项、V2 的 selector 细节、GoalFlow 的视野、MeanFuser 的 GMN 与 K=8 性质）

## 第十二轮（非生成式基线的规划头 + GoalFlow 主干，2026-09-23）

- **动因**：工作空间把"**非生成式基线不低于 DiffusionDrive**"当核心对照，但从未在代码层确认过这些基线**输出几条轨迹、有没有选优、损失是什么**。本轮把 UniAD 与 SparseDrive 拆到规划头一级，并补完 GoalFlow 的感知主干核验
- **新增产出**：[e2e_trunk_code_traces.md](../code/traces/e2e_trunk_code_traces.md) 新增 **§G 非生成式基线的规划头对照**（4 列对照表 + G.1 七条代码级事实 + G.2 三类基线的区分）
- **UniAD 核验**（读 `planning_head.py` / `planning_loss.py` / `base_e2e.py`）：
  - 类名 `PlanningHeadSingleMode`；**单模是代码强制的**——P 个候选 query 经 `mlp_fuser(...).max(1, keepdim=True)[0]` **max-pool 压成 1 个**，输出 `(-1, 6, 2)` 6 步累积位移
  - **默认配置带测试时优化**：`use_col_optim = True`，测试时走 CasADi `CollisionNonlinearOptimizer`（`occ_filter_range=5.0`/`sigma=1.0`/`alpha_collision=5.0`）→ **UniAD 的公开数字含后处理优化**，复现基线必须对齐这个开关
  - 损失 = masked **ADE**（`PlanningLoss`）+ `CollisionLoss` 三档 `delta=0.0/0.5/1.0`（权重 2.5/1.0/0.25），但 `inter_bbox` 只取 min/max → **退化为轴对齐包围盒相交**，`to_corners` 算的旋转被丢弃
- **SparseDrive 核验**（读 `motion_planning_head.py` / `motion_blocks.py` / `decoder.py` / `target.py` / `kmeans_plan.py` / `planning_eval.py`）：
  - **18 提案得到代码确证**：`plan_reg_branch` 输出 reshape 成 `(bs, 1, 3 * ego_fut_mode, ego_fut_ts, 2)`，`ego_fut_mode = 6` → **3 命令 × 6 模态**；`HierarchicalPlanningDecoder.decode` 同样 reshape 成 `(bs, 3, 6, 6, 2)`
  - **命令是 GT 输入**：`decode` 与 `PlanningTarget.sample` **都用 `data['gt_ego_fut_cmd'].argmax(dim=-1)` 选命令组**（与 UniAD 的 `navi_embed(3)` 同类）
  - **锚点是「query 初始化」而非「输出答案集」**：`kmeans_plan.py`（`K=6`）对 **GT 累积轨迹按命令分组**做 KMeans，存成 `(3, 6, 6, 2)`；head 里只用于 `plan_mode_query`，输出仍是 MLP 回归。→ 这是「轨迹词表/锚点」的**第四种用法**（前三：VADv2 答案集 / DiffusionDrive 扩散起点 / V2 候选池成员）
  - **分层选择的第二层是事后规则扣分**：`rescore` 里 `score_offset = col.float() * -999; plan_cls += score_offset`；碰撞判定用 `corners_in_box`（角点近似）；只对 `det_confidence ≥ 0.5` 的智能体、只用 top-1 运动模态；**6 个模态全碰撞时不惩罚**（`col[all_col] = False`）；车身硬编码 `[4.08, 1.73, 1.56] × 1.1`。→ 与 DiffusionDriveV2 的**学到的 mode selector** 不是一回事
  - **训练侧 rescore 与评测侧碰撞口径不一致**：评测用 `shapely Polygon.intersects`（精确）+ 车身 `4.084 × 1.85` + "follow uniad" 的 **+0.5 m 偏移**；训练侧用角点近似 + `4.08 × 1.73 × 1.1` → **rescore 代理指标 ≠ 评测指标**
- **GoalFlow 主干核验（解决 C003 §F 的一处过保守记录）**：
  - `GoalFlow/navsim/agents/goalflow/resnet_backbone.py` 首行 docstring 原文 **"Implements the TransFuser vision backbone."**；`goalflow_config.py` 与 navsim 的 `transfuser_config.py` **逐字段相同**（`resnet34/resnet34`、±32 m、`pixels_per_meter=4.0`、`hist_max_per_pixel=5`、相机 1024×256、LiDAR 256×256、anchors 8/32/8/8、`n_layer=2/n_head=4/n_scale=4`、`bev_features_channels=64`、`num_bev_classes=7`）
  - → 上一版把它写成"自有配置类"**过于保守**：它**沿 navsim 的 TransFuser 适配版**（非 CARLA 原版：原版 `pixels_per_meter=8.0`、`n_layer=8`、相机 960×480），差异集中在 `tf_d_model` 宽度（yaml 覆盖 **512** vs DD 的 256）
  - **输出聚合是"均值"不是"选优"**：公开评测脚本 `scripts/evaluation/run_goalflow_trajs.sh` 用 `agent=goalflow_agent_traj`（`anchor_size=128`、`use_nearest=false`、`ep_score_weight=0.0`）；`goalflow_model_traj.py:407-410` 为 `pred_trajs[:,:,1:1+8,:].mean(1)`——**采样 128 条 11 点流轨迹 → 切前 8 点 → 对 128 条取均值**。`use_nearest=true` 时才改为按到 navi 目标点的距离 `argmin` 选一条。→ **GoalFlow 的最终输出是"128 个样本的蒙特卡洛均值"**，与 DD（scorer 选一条）、V2（候选池选优）、SparseDrive（cls argmax + 规则扣分）在最后一步完全不同
- **对"生成式 vs 非生成式"对照的影响（§G.2）**："非生成式基线"实际覆盖**三种系统**——① 纯单模回归（UniAD / VAD v1，UniAD 还带测试时优化）；② 先验锚点 + 回归（SparseDrive，18 候选 + 规则扣分）；③ 离散词表 + 分类（VADv2 / Hydra-MDP）。→ **拿 UniAD 当"非生成式"代表会低估基线；真正的对手是 ③，而它恰好是 DiffusionDrive 的直接前身**
- **回填**：[E2E-01-uniad.md](../direction/notes/E2E-01-uniad.md) 与 [E2E-04-sparsedrive.md](../direction/notes/E2E-04-sparsedrive.md) 各补「代码核验（2026-09-23）」表；[C003](../code/traces/diffusion_planner_code_traces.md) §F 更新（配置同源性、训练/输出视野分列、结论扩到 5 条）
- **追加：DIVER（DP-A16）的代码级核验**（读 `motion_planning_head_DriveStyle.py` 约 1400 行、`decoder.py`、`DIVER_small_b2d_stage2_targetpoint_multiplan.py`、`kmeans_plan.py`、README）→ 新增 [C003 §G](../code/traces/diffusion_planner_code_traces.md)：
  - **它是唯一明确接在 SparseDrive 上的扩散规划器**：规划头换成 `DriveStyleMotionPlanningHead`，**沿用 SparseDrive 的 `operation_order`**，另加 `diff_operation_order` / `diff_noise_operation_order`；数据集是 **Bench2Drive**（`B2D3DDataset`），不是 NAVSIM
  - **两处论文主张与代码不符（更正）**：① **噪声起点不是"标准高斯"**——x₀ 是 `cmd_plan_anchor`（GT 命令对应的 plan anchor 的逐帧位移），`timesteps = torch.randint(0, 40, (bs,))` 加到 `DDIMScheduler(num_train_timesteps=1000)` 上，即**只用到前 40/1000 步**（与 DiffusionDrive 的 t=8 同思路）→ 已把 DP-A16 从"起点先验 = 纯高斯"改归"**锚点词表**"一路；② **"GRPO" 实为奖励加权损失**——`diffusion_loss = diffusion_loss * (1.0 + total_reward.mean())`，**全仓无 `log_prob` / `advantage` / PPO clip / 组内基线**（grep 无命中）
  - **奖励项实测只剩两项且 20% 是常数**：`total_reward = 0.5*div + 0.3*safe + 0.2*map`，`map_reward = 1.0`（代码注释自述 "dummy 值"），`safety_reward` 用 **GT 未来智能体轨迹** + `safe_distance=2.0`。→ 论文 Eq.20 的 **TTC / 车道保持 / Hydra-MDP PDMS 奖励在代码里都不存在**
  - **`check_collision` 语义与名字相反**：`safe=True` 起手，某智能体 `min_dist >= safe_distance` 即置 False → **只有"所有智能体都在 2 m 内"才返回 True**；`generate_safe_trajectories` 收集的因此是**离 GT 智能体极近**的样本
  - **发布状态与 SparseDrive 同类**：全仓 **0 个 `.npy`**（`kmeans_plan_6.npy` 需自建；`kmeans_plan.py` 已改为 **6 命令分组** → 该文件应是 (6,6,6,2)，与 SparseDrive 同名文件 (3,6,6,2) 不同）；且 **`forward` 里有 4 处未注释的 `pdb.set_trace()`**（另有 2 处）→ **无法直接跑通一次前向**。这是本项目**第 3 个"锚点文件未发布"的仓库**
  - **一处内部不一致（待运行确认）**：配置声明 `num_cmd=6`、`ego_fut_mode=6`，但评测用的 `HierarchicalPlanningDecoder.decode` **硬编码 `reshape(bs, 1, ego_fut_mode)`** → 最终只输出 6 条
  - **回填**：[DP-A16 笔记](../topics/diffusion-planner/notes/DP-A16-diver.md) 新增「代码核验」表并把两处不符标注在「关键事实」里；[论文表](../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A16 行补代码级更正与 venue（README 称已录用 **TAPMI 2026**，疑为 TPAMI 笔误）；「起点先验」横向对照行按代码改归

## 第十三轮（三个"非锚点"扩散规划器的代码级核验，2026-09-23）

- **动因**：第十二轮核验的对象都建立在**轨迹锚点/词表**之上。本轮挑三个**不依赖 K-means 轨迹锚点**的代表（FeaXDrive / WAM-Flow / FlowDrive），看各自用什么替代方案——直接对应 lineage 的"起点先验"维度
- **新增产出**：[C003](../code/traces/diffusion_planner_code_traces.md) 新增 **§H**（H.1 FeaXDrive / H.2 WAM-Flow / H.3 FlowDrive / H.4 起点先验维度更新）
- **FeaXDrive（DP-A18）核验**（读 `feaxdrive_diffusion_planner.py`、`trajectory_projector.py`、`feaxdrive_diffusion_planner_fagrpo.py`、`drivable_sdf.py`、3 个 slurm 脚本、README、docs）：
  - **两个核心机制都是真实实现**：`_kappa_max_adapt` 逐字实现论文 Eq.14（`min(kappa_geo_max, a_lat_max/(v²+eps))`），官方 `dyn` 档超参 **`kappa_geo_max=0.166`、`a_lat_max=6.0`、`lambda_dyn=0.01`**；`violation()` 是 **hinge-squared** 惩罚 `relu(|κ|−bound)² + relu(|a_lat|−a_max)²`；推理引导 `softplus((0.30−sdf)/0.20)` **只在最后 3/5 步生效**、步长 `0.05·progress`、作用于 **x0 估计**、XY 单位化 + heading 符号归一化×0.1
  - **但论文的"约束一致性训练"未启用（更正）**：**`lambda_proj=0.0`、`lambda_proj_supervise=0.0`**，且代码注释明写 `use_constraint_projection` **is deprecated in the current official chain** → 引用时只能说"训练期软违规惩罚 + 推理期软引导"
  - **FA-GRPO 是真 GRPO（与 DIVER 相反）**：`G=8` → `advantages=(R−mean)/std` 组内归一化 → 分位裁剪 → 折扣 `0.6^(剩余去噪步)` → 对去噪链取 `Normal(mean,std).log_prob` → `policy_loss = −mean(logp·adv)`，另加 **BC 项** `+0.1·(−logp(old_policy 链))`；奖励是**真 PDM 分数**（`PDMSimulator`+`PDMScorer`）
  - **解决了原笔记的两个待核验项**：① 有官方代码且可复现性最好（**无断点、无缺失 `.npy`**、带 slurm + 4 篇 docs）；② **违规率判据** = 先做二项式核平滑（ksize=5）、按弧长参数化用变步长中心差分算 κ、`a_lat=v²κ`、**两端点补 0**，违规率 = `(|val|>bound).mean()`，且**同时输出固定界与自适应界两套** → **论文内可比、跨论文不可比**
  - **它自己的 README 给出两条对本题最不利的数字**：**ReCogDrive w/GRPO 90.5 > FeaXDrive 90.0**；**FA-GRPO 把曲率违规从 0.88% 抬到 2.40%**（普通 GRPO 15.5%）→ "RL 提分"与"RL 破坏可行性"在同一张表里同时成立
- **WAM-Flow（DP-A13）核验**：**"数值 tokenizer" = 把 `linspace(-100, 100, 20001)` 的数字字符串（步长 0.01 m）`add_tokens` 进 102400 词表的 VLM**，轨迹以**文本数字**生成；`source_distribution="uniform"`、`discrete_fm_steps=50`、`MixtureDiscreteSoftmaxEulerSolver`（text+image token mask 联合）；输出 `extract_num_list` 解析出 **16 个数字 = 8 点 ×(x,y)**，**heading 由独立 `TrajectoryHeadingMLP` 给出**；**仅前视相机**（`cam_f0=[3]`）。→ 这条路线的"词表"是**分词器层面**的，与"轨迹码本"不是同一类东西
- **FlowDrive（DP-A10）核验**：源分布是**纯高斯**、`flow_inference_iter=8`；**"moderated" = 在采样中段（`applied_index = len(int_ts)//2 − 1`）注入 20 组 speed×lateral 几何偏移**（沿自车航向纵向拉伸 + 法向平移），再 `strong` 平滑 + `bound_speed_and_acceleration`；**选优用 navsim 的规则 `PDMScorer` argmax**（`PDMSimulator`+`PDMEmergencyBrake`，40 poses @0.1 s）。**`ego_future_clusters.pkl` 确实随仓库发布**（实测 `cluster_centers` (20,80)、`cluster_labels` (100200,)、`n_clusters=20`），但 **`ClusterStatsRetriever` 全仓只被 `_compute_weights_for_balanced_clusters` 调用** → **20 簇只做数据平衡加权，不参与生成初始化**。另 README 要求替换 tuplan_garage 的 `pdm_object_manager.py`（恒速物体应沿速度而非朝向运动），自述"significantly"提升 PDM 与 FlowDrive*
- **「轨迹簇/词表」用法从 4 类扩到 5 类**：① VADv2 = 输出答案集；② DiffusionDrive = 扩散起点；③ DiffusionDriveV2 = 候选池成员；④ SparseDrive = query 初始化；⑤ **FlowDrive = 训练样本权重**
- **核验覆盖度更新**：扩散规划器仓库**逐文件核验 11 个**（DD、DDV2、Diffusion-Planner、DiffusionVeteran、MeanFuser、GoalFlow、PC-Diffuser、DIVER、FeaXDrive、WAM-Flow、FlowDrive），另有 2 个只到结构级（HDP、DriveFine）
- **回填**：[DP-A18 笔记](../topics/diffusion-planner/notes/DP-A18-feaxdrive.md) 新增「代码核验」并把"代码：未核验"改为已核验、待核验项重写；[论文表](../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A10 / DP-A13 行补代码级补充，「起点先验」横向对照行改为 **5 类实测值**；[preparation.md](../ideas/preparation.md) §2 补"真 GRPO vs 假 GRPO"的对照

## 第十四轮（PC-Diffuser 的"硬约束"逐项核验，2026-09-23）

- **动因**：PC-Diffuser（DP-A21）是**驾驶域内唯一声称"认证级硬约束"**的工作，也是 [preparation.md](../ideas/preparation.md) 方向 A 的决定性对照。§A 只到结构级，§D 第 3 项还留着"QP 求解器实现细节与 1.14 ms 是否可复现"
- **新增产出**：[C003](../code/traces/diffusion_planner_code_traces.md) 新增 **§I**（I.1 逐项核对 + I.2 三条判断），并把 §D 第 3 项标记为"已解决一半"
- **先厘清的一件事：这个仓库里有三个方法、两套 QP**：
  - `safety/pc_diffuser/` = **PC-Diffuser 主方法**，QP 用 **CasADi `ca.qpsol('qp','qpoases')`**，决策变量是**加速度级** `[a, a_nbr(M=10), slack(M=10)]`
  - `safety/safe_diffuser/` = SafeDiffuser 基线，用 **cvxpy + OSQP**（`safety/utils.py::solve_QP`），决策变量是 **ego 位置增量 `[H,2]`**（yaw 被注释掉）
  - `safety/mpc_cbf/` = MPC-CBF 基线，CasADi NLP（N=80），调用时 `safety_mode='direct'`（非 CBF 衰减）
  - → 原 §A 记的"**自带 QP 求解器（未调 cvxpy）**"**对 PC-Diffuser 主路径成立，但不能当作整个仓库的结论**（仓库里确有 cvxpy+OSQP 路径）
- **机制逐项确认（原笔记记载准确，无需更正）**：注入点在 `dpm_solver_pytorch.data_prediction_fn`，滤在**干净估计 x0** 上；QP 目标 `(a−a_des)² + 1e4·Σ(slack+slack²)`，约束含**速度非负**与**逐邻居 degree-1 CBF**；**"只调速度、固定转向"完全一致**（ego 唯一决策量是标量加速度，转向率由 LQR 直写）；胶囊障碍 `h = sqrt(d_seg²) − (r_e+r_n)`，**docstring 原文 "linear gap distance, no bias towards far and fast vehicles"**——§A 记的"线性间距"就是它
- **但有三处需要限定**：
  1. **"逐去噪步"要看去哪个脚本**：yaml 默认 `shield_every_step: false`，**`scripts/methods/pc_diffuser.sh` 覆盖为 `true`**（并设 `selective_CBF=true`）→ 主方法确实逐去噪步；而 `mpc_cbf.sh` 没覆盖 → **MPC-CBF 基线只在最后一步滤**
  2. **"硬约束"是带松弛的**：每条邻居约束带 `slack`（权重 **1e4**），且 **QP 失败时回退到 nominal（不安全）轨迹** → "certified" 只在 QP 可行且**活跃松弛为 0** 时成立；仓库恰好**记录 `n_slack_total`** 作为诊断量
  3. **QP 次数被严重低估**：`n_steps = 1 if one_step else H − 1`，`for k in range(n_steps)` 里**每个航路点解一次**（被注释的计时打印写 `slack: {n_slack_total}/{H-1}`）→ 配 `steps=10` + `num_poses=80`，**单次规划解 QP 数百次**。→ **"1.14 ms" 是单次 QP 的口径**，不能与端到端延迟混用
- **顺带记录两条易漏的复现前提**：① README 明说为 mpc-cbf / pc-diffuser **改写了 nuplan-devkit 的 tracker**（`action_replay_tracker.py` + `set_latest_action`），否则 **CBF 输出会被 nuPlan 控制器覆盖**；② `distance_functions.py` 实现了 **5 种**距离表示（capsule / sat / sat_euclidean / circles / euclidean）
- **对方向 A 的直接影响**：障碍从"选哪一层"改成"**能不能把 QP 次数从数百降到个位数**"——更硬也更可测；同时更正 preparation 里"**FeaXDrive 未开源，违规率需自行定义**"这句（**FeaXDrive 已开源且判据已核验**）
- **回填**：[DP-A21 笔记](../topics/diffusion-planner/notes/DP-A21-pc-diffuser.md) 新增「代码核验」、venue 补 **IROS 2026**、"代码：未核验"改为已核验；[论文表](../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A21 行补代码级补充与 venue；[preparation.md](../ideas/preparation.md) 方向 A 补代码级补充并更正"FeaXDrive 未开源"

## 第十五轮（HDP 的逐文件核验，"无锚点纯扩散"的证据边界，2026-09-23）

**目标**：核验 [Hyper-Diffusion-Planner](https://github.com/ZhengYinan-AIR/Hyper-Diffusion-Planner)（DP-A06 / HDP）——它是**唯一同时提供 NAVSIM 与 nuPlan 两套实现**的仓库，也是 preparation.md 里"纯扩散不靠锚点"这条设计前提的唯一代码级候选证据；此前只做到结构级（"同仓含两套实现"）。

**读的文件**：`HDP-nuplan/` 的 `model/module/{decoder,dit}.py`、`model/diffusion_utils/{sde,sampling}.py`、`loss.py`、`train_epoch.py`、`train_predictor.py`、`planner/planner.py`、`normalization.json`、`config/planner/hyper_diffusion_planner.yaml`；`HDP-navsim/` 的 `agent/dp_vla/{dp_vla_agent,dp_vla_rl_agent}.py`、`model/{modeling_dp_vla,decoder,configuration_dp_vla}.py`、`model/diffusion_utils/diffusion_sde.py`、`agent/dp_vla/{scoring,rl_utils}.py`、`config/agent/*.yaml`、`config/agent/_shared/*.yaml`；两份 README。**并逐行对照上游 `Diffusion-Planner/diffusion_planner/model/module/decoder.py`。**

**结论（拆成四条）**：

1. **"无锚点纯扩散"成立（代码级）**：全仓 grep `anchor|kmeans|vocab|cluster` 在模型与配置路径上**零命中**（唯一命中是 nuPlan 数据处理的 `anchor_ego_state` 坐标系，与轨迹锚点无关）；nuPlan 侧 DiT 输入就是**完整 80 步轨迹**，位置编码是 `nn.Embedding(future_length=80)`（逐时间步，**不是可学习的模式 query 集**），推理从单条 `randn(80,4)*0.1` 一次去噪出整条；NAVSIM 侧 `CustomDiT(num_actions=8, dim_action=4)`（8 = 4s@2Hz 路点）同样一次出整条。NAVSIM README 自述 base 模型 88.6 PDMS 是 **"one trajectory per scene, without multi-sample selection, goal conditioning, or anchor-based decoding"**。
2. **"扩散损失空间 + 轨迹表示"的受控对照成立（这是本轮最有价值的一条）**：nuPlan 侧 `--diffusion_model_type` × `--diffusion_supervision_type` 各 4 选（`x_start`/`noise`/`v`/`score`，默认均 `x_start`），转换逻辑是 `sde.py::VPSDE_linear.transform` 的四表示互转；**真正的受控证据是两份同主干配置**——`dp_vla_agent_base.yaml` 与 `dp_vla_agent_hdp.yaml` 共用同一 `_shared/model.yaml`（同一 `DpVlaModel`），**只差四个字段**：`model_type`（noise→x_start）、`supervision_type`（null→x_start）、`kinematic_type`（waypoint→diff）、`hybrid_loss_weight`（0→0.05）。NAVSIM 侧 `model_type` **只有 3 选、没有 `v`**（`DpVlaConfig` 校验）。
3. **"数据规模"这条主张不可复现（证据边界）**：`train_predictor.py` 全部 45 个参数里数据相关只有 `--train_set` / `--train_set_list`（路径），**没有任何规模/子采样参数**；NAVSIM 侧只有三个固定 split；仓库**不含实车数据集**。→ 引用时必须**单独降级为"仅论文自述"**，不能与前两条并列声称"代码级已核验"。
4. **HDP-RL 不是 GRPO，是优势加权回归（RWR）**：`DpVlaRlAgent._rl_train_step` 的三行是 `rewards=(R−mean)/std`（**组内归一化优势**）→ `weights=exp(rewards)` → `reward_weighted_mse=(per_sample_mse*weights).mean()`。有正确的优势估计，但**没有对数概率、没有概率比、没有 PPO clip、没有 KL**。→ 本项目的"RL 词义核验"清单现在覆盖三种实现：**DIVER 最弱（`(1+r̄)` 乘性、无组内基线）< HDP（RWR）< FeaXDrive（真 GRPO）**，只有 FeaXDrive 是策略梯度。

**意外发现（相对上游 Diffusion Planner 的四处 README 未声明差异）**——逐行对照 `decoder.py` 后确认：

- **删掉联合预测**：上游 `xT = cat([current_states, randn(B,P,future_len,4)*0.5])` 是 **ego + 近邻一起生成**；HDP 是 `randn(B,80,4)*0.1`，**只生成 ego**。（README 未提，但 `train_predictor.py` 参数帮助里写了 **"[Warning] Neighbor prediction is deprecated in HDP"**）
- **删掉当前状态锚定 token**：上游把 current state 放序列首位并用 `initial_state_constraint` 每步钉死；HDP **没有首位 token**，当前状态改由 `DiT.ego_state_proj` 注入 ego 速度。
- **删掉引导模块**：上游有 `model/guidance/`（`collision_guidance_fn`、`guidance_wrapper.py`、`diffusion_planner_guidance.yaml`）且 `_guidance_fn` 非空时用 `guidance_type="classifier"`；HDP **`guidance_fn: null` 且根本没有 `guidance/` 目录**，`HyperDiffusionPlanner` 直接返回模型输出（**无引导、无 refine、无后处理**）。
- **初始噪声尺度 0.5→0.1**（NAVSIM 侧 `sample_temperature=0.5`）。
- → **判断**：引用 HDP 时**不能把它当作"Diffusion Planner + 损失空间消融"**——它是一个**退化为 ego-only 的 planner**。

**另外两处"声明未接线"**（与 DIVER 的 dummy reward、FeaXDrive 的零权重投影项同类）：

- `DpVlaModel` 声明了**双 LoRA 适配器（positive/negative）+ CFG**（`generate()` 里 `(1+cfg_scale)·pos − cfg_scale·neg`），但**全仓没有任何地方调用 `init_lora_adapter()`** → `generate()` 永远走 base 分支，**CFG 与 LoRA 不可达**。
- `DpVlaRlAgent` 的 `self.only_ep` **被赋值两次但全仓从未被读取**——"only_ep 模式"是死变量。

**还核到两条细节**：① hybrid loss 的 README 表述（`L_velocity + ω·L_waypoints`）与代码不完全一致——`train_epoch.py:105` 的第一项是**所选空间下的扩散损失**（默认 `x_start` 时不是 velocity），第二项是**预测干净轨迹的路点 MSE**（`detached_integral(..., detach_window_size=10)`，nuPlan 硬编码 10、NAVSIM 走 config 默认 1）；系数默认值两生态不一致（nuPlan **0.01**、NAVSIM base **0.0** / HDP **0.05**）。② `detached_integral` 的机制是"cumsum 的滑窗去梯度"——只保留最近 `window_size` 步的梯度。

**产出**：[C003](../code/traces/diffusion_planner_code_traces.md) 新增 **§J**（J.1–J.8，含三张对照表）；[论文表](../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A06 行升级为代码静态检查并补六条代码级补充，**并按核验结果把 DP-A06 从 C 节（截断扩散 + 锚点先验）移入 B 节（无锚点先验：纯高斯起点）**（C 节保留明细行并加反向指针，CSV 的 `分组` 同步）；[preparation.md](../ideas/preparation.md) 把"HDP 摘要称…"这条**拆成三条**（成立 / 成立 / 仅论文自述）；[topics/lineage.md](../topics/diffusion-planner/lineage.md) 与 [direction/lineage.md](../direction/lineage.md) 的"跨生态已打通"补上"两套实现不是同一模型的移植"这一限定；state / index / sources / repositories / README 同步。**核验覆盖度：逐文件核验 12 个扩散规划器仓库，只剩 DriveFine（DP-A29）为结构级。**

## 第十六轮（DriveFine 核验：研究对象侧代码核验结账，2026-09-23）

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
2. → 其**可插拔 block-MoE、生成/精修双专家、梯度阻断、hybrid RL 策略**全部只能停留在**论文自述级**，与 [E2E-05 Hydra-MDP](../direction/notes/E2E-05-hydra-mdp.md)、[E2E-10 DriveVLM](../direction/notes/E2E-10-drivevlm.md)、WM-18 WorldRFT 同类。
3. **`repositories.md` 的 DriveFine 行由"有代码"改为"零代码"**，它是本项目查出的**第 3 个零代码仓库**（研究对象侧第 2 个，与 WorldRFT 并列）。累计口径：36 个在列仓库里 **7 个实际无代码或代码不全**（sources.md C002 行、state.md、README.md 的计数同步从 6 改 7）。
4. **研究对象侧的代码级证据由此穷尽**：13 个仓库 = **12 个逐文件核验 + 1 个零代码**。→ 这条边界比"还剩 1 个没做"更有用：**扩散规划器这条线的代码级工作已经结账**，再往下推进只有两条路——**换领域做代码核验**（E2E 主干 13 个 / 世界模型 4 个 / VLA 3 篇仍有未核验项），或**进入运行验证阶段**（需算力与数据，见 state.md 待续清单第 9 项）。

**产出**：[C003](../code/traces/diffusion_planner_code_traces.md) 新增 **§K**（含三重证据表与四条判断），§A 的 DriveFine 行改为"组合关系无法核验"、§H.4 与文件头改为"13 个仓库全部结账"；[论文表](../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A29 行与 CSV 标注**零代码**；[repositories.md](../code/repositories.md) DriveFine 行改为零代码并把它加进"实际无代码/代码不全"清单（7→8 条，其中"论文声称有代码但实际没有"由 4 条改 5 条）；[topics/lineage.md](../topics/diffusion-planner/lineage.md) 组合关系表补注；sources / state / README 同步。

## 第十七轮（E2E 主干侧：锚点/词表文件的公开渠道核验，2026-09-23）

**动因**：第十六轮把研究对象侧结账后，按结论转向 E2E 主干侧。C005 里挂着一条**跨轮次反复引用的硬阻塞**——"**两个关键词表文件都不在公开仓库里，复现基线前必须先解决词表重建**"（写进了 state.md 待续清单与 preparation.md 的资源估算）。但"不在仓库树里"≠"不可得"：本轮把方法从"仓库内 `find`"换成 **GitHub Releases API + 实际下载 + 内容实测**，结论是**这个阻塞被大幅高估**。

**逐文件核验（全部实测，非推断）**：

| 文件 | 期望形状（谁要） | 渠道 | 实测 |
|---|---|---|---|
| `kmeans_navsim_traj_20.npy` | **(20,8,2)**（DiffusionDrive v1） | v1 仓库**无**，但 `docs/train_eval.md:13` 指向官方 Release 资产（tag `DiffusionDrive_88p1_PDMS_Eval_file`） | **已下载**：2,688 B，**(20,8,2) float64**，md5 `0378349a47b896b96c3f1bc8f7eb156d`；**与 DiffusionDriveV2 仓库内同名文件逐字节相同**（4,148 次下载） |
| `kmeans_plan_6.npy` | **(3,6,6,2)**（SparseDrive） | SparseDrive 自己的 release 只有权重；但 `hustvl/DiffusionDrive` 的 tag **`DiffusionDrive_nuScenes`** 有一整套 | **已下载**：992 B，**(3,6,6,2) float32** → 与配置匹配；同批 `kmeans_motion_6.npy` **(10,6,12,2)**、`kmeans_map_100.npy` **(100,20,2)**、`kmeans_det_900.npy` **(900,11)**，与 SparseDrive 的四个 `anchor=` 一一对应 |
| 同上但给 **DIVER** | **(6,6,6,2)** | 同文件名 | **不兼容**：DIVER 的 `kmeans_plan.py` 是 `K=6` + `navi_trajs[cmd-1]`（6 组命令）→ **(6,6,6,2)**，且依赖 `b2d_infos_train.pkl`（Bench2Drive） |
| `motion_anchor_infos_mode6.pkl` | UniAD `anchor_info_path` | UniAD release `v1.0`（5,109 B，5,908 次下载）+ `docs/DATA_PREP.md:42` 的 HuggingFace 直链 | 渠道确认可用 |
| `carla_plan_vocabulary_4096.npy` | VADv2 | `hustvl/VAD` **无任何 release**、全仓 0 个 `.npy`、README 只有模型权重链接 | **仍不可得** → 唯一真正剩下的词表阻塞 |
| `gtrs_traj/navtrain_16384.pkl` | DiffusionDriveV2 的 PDM 子分数表 | 四个 Releases 渠道都没有 | **仍缺失** |

**顺带更正一处口径**（DIVER 的候选数，第十二轮误记）：`num_cmd` **不是候选数而是"命令组数"**。证据：8 个配置里 3 个 `num_cmd=6`、5 个 `num_cmd=1`；**全仓唯一** import `diffusers` 的文件是 `motion_planning_head_DriveStyle.py`，而**唯一实例化这个扩散头**的配置是 `DIVER_small_b2d_stage2_targetpoint_multiplan.py`（`num_cmd=6`、`plan_anchor=kmeans_plan_6.npy` **生效**）；其 decoder `HierarchicalPlanningDecoder.decode` 是 `classification.reshape(bs, 1, self.ego_fut_mode)`（`decoder.py:136`）→ **输出候选数恒为 `ego_fut_mode=6`**。→ 原记"36 候选"是误读，**该待核验项关闭**。

**三条判断**：① 对 DiffusionDrive / SparseDrive / UniAD 三条线，"必须先重建词表"**不成立**，资源估算需下调；② 真正剩下的空洞是 **VADv2 的 4096 词表**（恰好是"离散词表 + 分类"这类最强基线的入口，§G.2）与 V2 的 PDM 子分数表；③ **"同名锚点文件"是静默陷阱**——`kmeans_plan_6.npy` 在 SparseDrive 是 (3,6,6,2)、在 DIVER 是 (6,6,6,2)，`np.load` 阶段不报错，要到 anchor encoder 的维度运算才炸。

**产出**：[C005](../code/traces/e2e_trunk_code_traces.md) 新增 **§H**（H.1 逐文件核验表 / H.2 三条判断 / H.3 对 §C 谱系的补正 + DIVER 口径更正）；§D 的"词表文件是否随仓库发布"行改写、§E 第 3 项标记**已解决**、新增第 5 项（`navtrain_16384.pkl` 仍缺失）、文件头同步；[C003](../code/traces/diffusion_planner_code_traces.md) §G 的"`num_cmd` 内部不一致"改为**已解决**并指向 C005 §H.3；state.md 待续清单第 9/10 项重写 + 新增三条判断；[preparation.md](../ideas/preparation.md) 新增"资源阻塞大半不成立"一条。
