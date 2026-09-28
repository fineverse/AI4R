# 第二十五轮

更新时间：2026-09-23

## 29. 两个借鉴来源各补读全文 + 代码核验：VLA-22 / 25 / 27 与 WM-15 / 16

**动因**：待续清单第 3 项——两个借鉴来源仍有 26 篇为摘要级（VLA 11 + 世界模型 14）。按"与研究对象接点最紧"排序，本轮挑 **VLA-22 VaViM/VaVAM**（官方代码 + 权重，视频-动作模型）、**VLA-25 Reasoning-VLA**（NUS，有官方仓库）、**VLA-27 Counterfactual VLA**（NVIDIA + Stanford，自反思机制）与 **WM-15 AdaWM**、**WM-16 Raw2Drive**（两篇都是"世界模型 → RL 的 reward/next-state"路线）。

**做法**：**并行派 4 个 Explore 子代理**读 arXiv 全文（`abs` → `html` → PDF + `pdftotext -layout` 三路交叉补全），GitHub 侧**每个子代理 ≤5 次 API**、其余走 `raw.githubusercontent.com`，**不克隆仓库**；中间产物全部落 `/tmp/ai4r/{vavam,reasoningvla,cfvla,wm1516}_probe/`。主线程只做写回与判断。

**结论（按论文）**：

| 编号 | 本轮的关键新增事实 | 代码状态 |
|---|---|---|
| **VLA-22 VaViM/VaVAM** | **VaViM = LlamaGen VQGAN（16384 词表）+ GPT-2 自回归**；**VaVAM = VaViM + flow matching 动作专家（Euler 10 步）**，输出 **6 waypoint @2 Hz = 3 s**；接口是**逐层 joint attention**（动作 token 看全部视觉 token，视觉 token 保持因果掩码）。**⚠ 论文称"完整 pipeline"，代码 `video_action_model.py:64` 却 `self.gpt.requires_grad_(False)` → 冻结 VaViM**，论文全文无 frozen 字样。**无受控消融**（没有"视频预训练 vs 从零训练"对照）→ **"视频预训练本身值多少"无法量化**。其 NeuroNCAP "SOTA" 是**闭式口径 + 基线全无后处理**（同表 UniAD 无后处理 0.73/88.6，加后处理 1.84/68.7）。**规模↑反而变差**（B 139k 仅 1.781/70.0）。**输入权限：仅前视单目 512×288、8 帧 @2 Hz，无 LiDAR/地图/自车运动学** | **完整**（训练 + 推理 + 配置 + 权重，权重在 GitHub Releases v1.0.0）；**闭式评测依赖外部 fork `F-Barto/neuro-ncap`** |
| **VLA-25 Reasoning-VLA** | Qwen2.5-VL + **可学习 action queries**，**双向 mask 一次前向并行输出全部轨迹** → **动作是连续回归**（论文明确对比 π0 的离散 token）。**RL 论文明写用 GRPO**（§3.6 原句 "GRPO replaces the critic model … with an estimation of group scores"；附录 `beta 0.04`、`num_generations 8`），**但 ratio/clip/advantage 归一化均未声明**。**奖励是硬 0/1 阶跃规则分**（转向 0.84、加速度 6），非 PDM 分。**⚠ 结构疑点**：动作是回归而 GRPO 作用于 token 序列（`max_completion_length 768`）→ **奖励梯度如何回流到动作头未说明**；CoT 文本是模板占位。**消融每个组件增益都很小**（1.45 → 0.32/0.29/0.29 → 0.26），**无 RL-only 受控对照**。**7B+ 开环变好但闭环变差**（2.25→2.19，59.4→59.8）。**输入权限：3 路相机**（nuScenes 实为 6 路）+ 自车状态 + 固定 prompt，无 LiDAR/地图 | **仓库为空壳**——`xipi702/Reasoning-VLA` 文件树只有 `README.md`（113 B，"… # Comming Soon."），**无 RL 脚本、无奖励实现、无权重** |
| **VLA-27 Counterfactual VLA** | 机制是 **`meta-actions → CF reasoning → updated meta-actions → trajectory`** 的自反思环，触发由生成 `Action:` / `Thinking:` 词决定。**⚠ 名不副实**：摘要称 "simulates potential outcomes"，但**全文无任何前向仿真 / 世界模型 / verifier**（§1 自述 "without an external world model or verifier"）→ 实质是**用 GT meta-action 事后诊断文本做 SFT**；教师 prompt 明令不提 GT，**却同时喂入 expert meta-action** → **GT 泄漏面**。**⚠ 无任何公开 benchmark**（只在私有 80,000 h 数据的验证子集上开环评）。**⚠ 数字口径混用**：摘要 17.6% 用的是**无 route 版**，表中最佳 0.6712 是**有 route 版**（相对 traj-only 实为 27.7%）。**⚠ 受控对照削弱主张**：`meta-act 0.8411 → multi-round（丢弃推理文本、仅复用高分样本）0.7906 → CF-VLA 0.7650` → **"反思推理"本身只值约 3%**；**force-think 0.9319 比 traj-only 还差**、修正后 IOU 反降。**输入权限：两路前视（wide/tele）、4 帧 @2 Hz、448×796，无 LiDAR/地图/自然语言指令** | **未找到官方仓库**；唯一命中 `pengzhenghao/cfvla` 是 **CVPR'26 项目主页**（只有 `.gitignore` / `README.md`(130 B) / `index.html` / `static/`） |
| **WM-15 AdaWM** | **Dreamer v3 式 RSSM**，预测 **BEV 语义图的潜状态**（非像素视频）；规划器是 **Dreamer v3 actor-critic，在想象 rollout 中训练 → 非生成式**。**"adaptive" 只是微调调度**（TV 距离判失配，模型侧 LoRA/NoLa、策略侧凸组合权重），不是结构自适应。**接口位 = ②隐状态级条件**（actor/critic 以 model state 为条件，reward/next-state 取自世界模型 reward 头与潜动力学）→ **世界模型确被规划器消费**。**数字无 nuPlan/nuScenes**，用 CARLA 自定义 TTC/SR（ROM03 2.05/0.82 vs DreamerV3 0.95/0.40）。**消融无"去掉世界模型"对照**。**⚠ 特权 BEV 泄漏到推理侧**（训练与推理同用 128×128 语义分割）。**可疑点**：正文称 ROM03 为"环岛"而配置是 `NoScenario_Town03`；**基线不微调、比较不对称**；单次运行无方差 | **无官方代码**；Reproducibility 称"将提供"却无链接 |
| **WM-16 Raw2Drive** | **双流 MBRL：两套 Dreamer v3 RSSM + 两套 actor-critic**；特权流 = 时序 BEV 语义掩码（43 通道），原始流 = 环视 RGB + IMU 经 BEVFormer 编码。**对齐非对抗非对比**：Spatial-Temporal Alignment（L2）+ Abstract-State Alignment（deterministic L2 / stochastic KL）；rollout **只从原始流采样一次**喂两流。**RL 是 Dreamer v3 actor-critic，不是 PPO/SAC**。**接口位同时命中 ② 与 ⑤**：**reward/continue 由特权世界模型头经 Head Guidance 提供**，另把特权策略的动作分布**蒸馏**至原始策略。**Bench2Drive DS 71.36 / SR 50.24**（同表特权 Think2Drive 91.85/85.41）；**CARLA v2 leaderboard 仅 DS 4.12/3.56**。**消融**：rollout guidance 全缺 **DS 0.0**；**直接沿用特权策略 58.4 vs 微调 83.5**；**无"完全去掉世界模型"对照**。**⚠ 原始流相机路数/分辨率/帧率/历史帧均未给出**。**可疑点**：leaderboard 仅 4.12/3.56 却称"CARLA Leaderboard 2.0 唯一 RL E2E 方法"；消融用 10-clip Dev10，**DS 83.5 与主表 71.36 口径不同** | **只有 README**——`Thinklab-SJTU/Raw2Drive` 仅 2 commits、文件树只有 `README.md`（321 B），内容仅标题 + "Official inference code" 一行 → **README 称有推理代码，仓库 0 代码** |

**本轮新增的四条判断**：

1. **"VLA + 生成式动作头"再添一例，且这例接得更深**：VaVAM 是 **flow matching + 逐层 joint attention**，与 SpanVLA（换动作头）、UniDriveVLA（MoT 内嵌）、AutoMoT（独立后置扩散头）合计**四例**。
2. **"论文声称 vs 代码实测"新增第四种形态**：**机制在代码里且被走到，但训练被冻结而论文未声明**（VaVAM 冻结 VaViM）。前三种是"配置全关"（ORION）、"只实现一半"（MindDrive）、"根本没发布"（DMW）。
3. **"有代码"这一档积累到七种形态**：完整 / 关键部分未发布 / 训练脚本未发布 / 只有项目页 / 核心模块未发布 / 有仓库但功能项全未勾选 / **仓库为空壳**（Reasoning-VLA）。
4. **"世界模型 → 规划器"的第 5 条路线（RL 的 reward/next-state 来源）现有两个实例，但仍是五条里唯一"零可核验代码"的**（Imagine-2-Drive "Code coming soon"、Raw2Drive 只有 README）。另：**"特权信息"在世界模型侧出现分叉**——AdaWM **泄漏到推理侧**，Raw2Drive **严格限定训练侧**。

**产出**：[vla/papers.md](../topics/vla/papers.md) 新增 **§11（11.1–11.4）**、§2 证据边界更新（已读全文 20、代码核验 10）；[world-model/papers.md](../topics/world-model/papers.md) 新增 **§4.2**、WM-15/16 的 §1 行与 §5 代码行更新、表头证据状态更新（已读全文 11）；[state.md](../state.md) 的当前阶段、主要产出、待续第 3 项、"RL 词义核验"清单（八种 → **九种**）、"论文声称 vs 代码实测"（三种 → **四种**）、"有代码"（四档 → **七档**）、接口路线 ⑤ 更新；[README.md](../../../README.md) 追加最近动态。**未克隆任何仓库**。

## 30. 同一批的第二轮：DriveLaW 全文（对照已有代码事实）+ DriveWorld / TrafficBots 源码级 + NuInteract 核验

**动因**：§29 之后，按"与研究对象接点最紧 + 还剩有代码可核"两条排序，挑出 4 个目标：**WM-11 DriveLaW 的论文全文**（唯一"世界模型 + 扩散规划器"的桥，已有代码结论但缺论文侧）、**WM-02 DriveWorld** 与 **WM-10 TrafficBots**（两篇有仓库但未做源码级核验）、**VLA-21 NuInteract**（CCF-A + 官方代码，但未读过全文）。

**做法**：同 §29——4 个 Explore 子代理并行读全文（`abs` → `html` → PDF），GitHub API 每个 ≤5 次、其余走 `raw`，**不克隆**；产物落 `/tmp/ai4r/{drivelaw,driveworld,trafficbots,nuinteract}_probe/`。

**结论（按论文）**：

| 编号 | 本轮的关键新增事实 |
|---|---|
| **WM-11 DriveLaW** | **论文全文与已有代码事实逐条对照，发现四处不一致**。论文只讲**接口 B**（缓存 Video DiT 去噪**第一步**每个 Transformer 块的中间特征 {f₁…f_B}，作独立 **133 M Action DiT** 的 cross-attention keys），而**代码默认路径是接口 A**（`action_expert: true` + `return_video: false`）；论文说喂全部 28 块，代码只读 `features['last_hidden_state']`（单张量）；**论文自相矛盾**——§4.1 说轨迹微调"updating both the Video DiT and the Planning DiT"，§A.2 却说 "gradient isolation … is preserved"；**Table 5 的 "VLM Hidden State" PDMS=86.5 与 Table 2 的 "ReCogDrive-IL" 86.5 完全相同**（Fig.4 明说 VLM 特征取自 ReCogDrive）→ 数字口径复用嫌疑。**规划头**：flow matching、5 步、纯高斯先验、无锚点；**全文无 RL、无 scorer**。**navtest PDMS 89.1**（> WoTE 88.3 / DiffusionDrive 88.1）；**全文未出现 EPDMS / NAVSIM v2 / navhard / Bench2Drive / DiffusionDriveV2**。**⚠ 本轮最有价值的两张受控消融**：**Table 5「表征来源」BEV 84.1 / VLM hidden 86.5 / Video latents 89.1（+5.0）**；**Table 4 视频预训练规模 scratch 85.9 → 7.6M 帧 89.1（+3.2）**；**Table 6 条件去噪步 t=1 89.1 / t=5 86.9 / t=10 23.2**。**消融缺口**：没有"去掉视频生成 / 去掉隐状态条件"的规划消融、没有接口 A vs B 对照、没有规划去噪步数消融 |
| **WM-02 DriveWorld** | **它是预训练表征，不是端到端规划器**——世界模型 = Image Encoder + 2D→3D 变换 + **MSSM（Dynamic Memory Bank + Static Scene Propagation）** + Decoder，预测 **3D 占据 + 动作**（不是视频、不是潜特征重建）；**只有"图像 → BEV"编码器被预训练，rollout 层在微调时被丢弃**，规划头**直接沿用 UniAD**（单模回归）。**数字**：检测 mAP 0.442（vs BEVFormer+ImageNet 0.377，**+6.5%**）但 **vs BEVDistill 0.439 仅 +0.003**；规划 avg L2 0.92 / 碰撞 0.26%（vs UniAD 1.03 / 0.31）。**受控消融**：baseline 0.429 → **+DMB 反掉到 0.425** → +MLN 0.432 → +Task Prompt 0.436；**无"预训练 vs 从零"行**。**代码：未找到任何官方仓库**，且**"同名不同篇"**——综述指向的 `yvanyin/drivingworld` 是**另一篇** DrivingWorld（`2412.19505`） |
| **WM-10 TrafficBots** | **⚠ 不算"世界模型 → 规划器"这条线**：自称 world model，但**规划模块是 future work**、**全文无自车规划评测**、README 原文 "repo contains only the experiments for the Waymo Motion Prediction Challenge"、作者自评 "not comparable to SOTA open-loop methods"。**不是"每条 route 一个 bot"**——是**单一共享策略网**，条件于 **destination 分类 + 16 维 personality CVAE**，输出 **DiagGaussian (acc, yaw_rate)** 经 **unicycle 动力学自回归积分**，多模态来自采样（K=6 条联合未来）。**数字**：WOMD test mAP 0.212 / minADE 1.313（vs SceneTransformer 0.279 / 0.612）→ **低于当年 SOTA**。**消融**：**w/o persona mAP 掉到 0.06**；**用 goal 替 destination 虽 minADE 更小但 veh col 12.3% / run red 1.35%（因果错误）**；`docs/ablation_models.md` **自承消融未复现**。**代码核验**：`action_head.py` 是 **DiagGaussian 动作头（非轨迹头、无锚点）**、`goal_manager.py` 是 **DestCategorical（1 个 polyline 索引）**，**无自车规划代码、无任何权重文件**；**配置里关掉的机制**：`traffic_rule_checker` 四项全 `False`、`diffbar_reward.w_collision=0`——**而 Table II 的 veh col / run red / passive 正依赖它们** |
| **VLA-21 NuInteract** | **⚠ 是"理解侧"的数据集 + 理解侧模型，不是 VLA 规划器**：论文 §III-A 明确 **planning 的答案是 high-level command，不是轨迹**；**§VI Limitation 自述** "planning tasks only concentrate on high-level commands rather than specific trajectories"；**源码印证**——planning 集合 `max_new_tokens: 10`，**全仓 243 文件无任何 trajectory / waypoint 代码**。**是什么**：数据集 **850 场景 / 34 K 帧 / 239 K 图 / 1.5 M pairs**（nuScenes 自动标注）+ **DriveMonkey 框架**（LLaVA 式 LVLM + 可插拔 spatial processor，取 **PETR** backbone + 30 个可学习 query）。**数字**：3D VG Pr 51.90 / mAP 34.53（vs 同 backbone InternVL2-8B 31.47 / 24.67）；**Plan Acc 82.64 vs 46.93**；**⚠ 2D VG 反而略低**。**消融**：**query 数 10 → 900 时 Pr 43.94 → 58.47 但 mAP 33.10 → 7.12**（精度—召回权衡）；去 3D PE 后 Pr/mAP 42.13 / 21.10 → 51.66 / 34.26。**代码与数据真实发布**（GitHub Releases + HF `zczhao/DriveMonkey`）；**可疑点**：arXiv 仍是 v1 且无 `journal_ref`（TIP 2026 未体现）、§V-C 的 5.8% 与 Tab.III(a) 的 +4.8 对不上、评测脚本 `--data_lenth` 默认 None 只取 500 条 |

**本轮新增的三条判断**：

1. **"世界模型带来收益"第一次有了量级可比的受控消融**：DriveLaW 的 **Table 5 是"同一规划器只换输入表征"的干净对照（BEV 84.1 → 视频潜状态 89.1，+5.0 PDMS）**，Table 4 的"从零训练 85.9 → 视频预训练 89.1"给 +3.2 → **与 SpanVLA 的"换动作头 +5.2"、GoalFlow 的"加 goal 条件 +4.7"、DriveFuture 的"加未来条件 +3.7"同量级**，"世界模型潜状态"这一维**不比另外两维更大**。
2. **"自称世界模型"必须再分"预训练表征 / 规划回路 / 只有仿真侧"三档**：DriveWorld 是**预训练表征**（rollout 层被丢弃、规划头抄 UniAD），TrafficBots 是**只有仿真侧**（规划模块是 future work），NuInteract 是**理解侧数据集** → **"世界模型 → 规划器"这条线上真正端到端的实例，比论文标题暗示的少得多**。
3. **"同名不同篇"陷阱再增一例**：DriveWorld 的代码被综述指向 `yvanyin/drivingworld`，实为另一篇 DrivingWorld（`2412.19505`）→ **查代码必须核对 arXiv ID，不能只核标题**。

**产出**：[world-model/papers.md](../topics/world-model/papers.md) 新增 **§4.3**、WM-02/10/11 的 §1 行与 §5 代码行更新、表头证据状态更新（已读全文 16、代码核验 14）、§2 证据边界更新；[world-model/lineage.md](../topics/world-model/lineage.md) 的路线 ⑤ 补入 WM-16 与 WM-15 并标注"五条里唯一零可核验代码"；[vla/papers.md](../topics/vla/papers.md) 新增 **§12**、VLA-21 行更新、§2 证据边界更新（已读全文 21、代码核验 11）；[state.md](../state.md) 的当前阶段、主要产出、待续第 3 项、"同名不同篇"扩入第十七轮那条、"自称世界模型"新增一条判断边界；[README.md](../../../README.md) 追加最近动态。**未克隆任何仓库**。

## 31. 第三轮：把"有代码无论文"的 3 篇补齐，并补两篇最早期的 VLA

**动因**：§30 之后剩下 8 篇摘要级，其中 **WM-04 Drive-OccWorld / WM-05 IR-WM / WM-07 World4Drive 已有逐文件代码核验、只缺论文全文**（"有代码无论文"）——这类补齐的边际价值最高，因为论文与代码可以直接对照。另两篇 **WM-12 DrivingGPT / WM-14 Think2Drive** 是"自称有码但仓库不存在"的两篇。VLA 侧则补**建表最早、长期只有摘要级的 VLA-09 EMMA（Waymo）与 VLA-10 CoVLA**。

**做法**：同前——4 个 Explore 子代理并行读全文（`abs` → `html` → PDF），GitHub API 每个 ≤5 次、其余走 `raw`，**不克隆**；产物落 `/tmp/ai4r/{wm0407,irwm,wm1214,vla0910}_probe/`。

**结论（本轮最有价值的两条）**：

1. **"世界模型收益"的量化证据从 1 条增加到 3 条，且口径都是"同一规划器换输入"**：

| 来源 | 对照 | 量级 |
|---|---|---|
| **WM-11 DriveLaW** Table 5 | BEV 84.1 → **Video latents 89.1** | **+5.0 PDMS** |
| **WM-07 World4Drive** Table 3 行 5→6 | 无 WM（L2 0.61 / 碰撞 0.36）→ 全量（0.50 / 0.16） | **L2 −18.0% / 碰撞 −55.6%** |
| **WM-05 IR-WM** Table V | Decoupled（不用未来 BEV）0.87 → Semi 0.53 | **+0.34 m（劣化 64%）** |
| （WM-14 Think2Drive Table 1） | model-free PPO 57.5 → 有世界模型 83.8 | +26.3（**跨方法比较，非同一规划器**） |

→ **加上 EMMA 的"语言中间层 +6.7%"，四条机制轴的受控收益全在 +3.7 ~ +6.7 区间**（世界模型 +5.0 / 生成机制 +5.2 / 条件 +4.7 与 +3.7 / 语言中间层 +6.7）→ **没有任何一轴"远大于"其他轴**。这是本工作空间**最稳定的一条跨论文结论**。**但三条世界模型证据的基准与指标各不相同（NAVSIM PDMS / nuScenes L2），不能直接横比**。

2. **但"世界模型"内部的机制差异被回避**：**IR-WM 的核心卖点是"残差"却恰恰没有"去掉残差"的消融**（且代码 `drive_occworldV2.py:374/381/384` 那行加法挂着 `# TODO: predict residual bev features`）；**Drive-OccWorld / DrivingGPT / Think2Drive 都没有"去掉世界模型"的消融**（Think2Drive 连"去掉潜空间想象"都没有）→ **本轮读的 5 篇里，只有 World4Drive 一篇把"世界模型的有无"做成了表内受控行**。

**其余关键事实**：
- **WM-04 Drive-OccWorld**：规划器是 **ST-P3 式"采样 + 规则 cost 选优"**（Agent-Safety + Road-Safety + **Learned-Volume**，取最小）；**候选数论文只给符号、未给数值**；**同一方法三种协议口径（L2 avg 0.85 / 0.47 / 0.32）**；**图 10 展示 5 步滚动而代码 `planning_steps=1`**；摘要的 mIoU_f 提升（9.5%/6.1%）与正文（9.4%/6%）**冲突**。
- **WM-05 IR-WM**：残差加在 **BEV 特征层**（Eq.6 `S^bev_t = ΔS^bev_t + S^bev_{t-1}`），**占据只是辅助监督**；**碰撞率口径选择性表述**——Table IV 里 IR-WM 的 **1 s 碰撞 0.14% 反高于** Drive-OccWorld / UniAD / VAD（0.05/0.05/0.04%），正文只强调 avg 0.17% 更优；论文的 FA 是 **AdaNorm 语义/动态调制**，代码 `_align_bev_coordnates` 偏**坐标对齐**，描述与实现可能不符。
- **WM-07 World4Drive**：世界模型在**潜空间**（Metric3D v2 深度 + Grounded-SAM 伪语义作训练侧先验）；**动作条件 = 意图**（词表 **N=8192、K=6**，**与 VADv2 同源**）；**Table 3 行 4 的 L2(0.49) 反优于行 6(0.50)** → 意图主要只降碰撞，而论文称"加意图显著提升"。
- **WM-14 Think2Drive**：**奖励 Eq.8 是"速度 + 沿路 + 偏离车道 + 转向成本"，不是 CARLA 规则分**（DS 仅用于评测）→ **WM-16 Raw2Drive 沿用的就是这个奖励**；**训练与推理都用特权信息、无不对称**；**"efficient" 没有加速倍数**，只有"单 A6000 3 天"，附录 C 的"每 100K 步省约 1 天"指**异步重载工程**；摘要称 "100% route completion" 而 Table 3 的 RC = 98.6。
- **WM-12 DrivingGPT**：**"multi-modal" 实际只有图像 + 动作两个模态**；序列按帧交替、**未来动作条件于自身生成的图像 token**（"读自己生成出来的未来"）；**NAVSIM PDMS 82.4**；**FVD 存在 142.61 与 278.11 两口径**；**仓库 404 确认不存在**。
- **VLA-09 EMMA**：**"轨迹即文本"的第二个实例**（纯文本浮点数，无回归头、无特殊 token）；**语言中间层受控消融 +6.7%**；**未在 NAVSIM 评测**；**⚠ venue 更正——arXiv `comments` 显示 "Accepted by TMLR"**（附 OpenReview `kH3t5lmOU8`），此前记的"仅预印本（T4）"应改；可疑点包括"相对提升数字对应的是 EMMA+ 而非 EMMA 行""Table 5 的 +1.4% (±2.8%) 统计上不显著"。
- **VLA-10 CoVLA**：**以数据集为主**（10,000 场景 / 83.3 h / 6 M 帧，全自动标注）+ 基线 CoVLA-Agent；**轨迹用"特殊 token + MLP 回归头"，与 EMMA 的"轨迹即文本"正好相反**；**只在自有数据集评 ADE/FDE、无任何外部 benchmark 与基线对比**；**语言中间层受控对照：GT 字幕 vs 预测字幕 ADE 降 14.8% / FDE 降 26.1%**。

**本批第三条判断**：**"轨迹怎么表示"至少有四种做法，各有失败模式**——**纯文本数字**（EMMA、Impromptu VLA → 依赖解析器）/ **特殊 token + 回归头**（CoVLA）/ **离散轨迹词表**（VADv2 → DiffusionDrive）/ **连续回归或生成**（SpanVLA、VaVAM）→ 引用任何"VLA 输出轨迹"的说法前必须先问"轨迹是以什么形式生成的"。

**产出**：[world-model/papers.md](../topics/world-model/papers.md) 新增 **§4.4**、WM-04/05/07/12/14 的 §1 行更新、表头与 §2 证据边界更新（已读全文 21、余 3）；[vla/papers.md](../topics/vla/papers.md) 新增 **§13**、VLA-09 行 venue 更正、VLA-10 行更新、§2 证据边界更新（已读全文 23、余 5）；[state.md](../state.md) 的当前阶段、主要产出、待续第 3 项、"四条机制轴同量级"并入 DriveLaW 那条判断边界。**未克隆任何仓库**。

## 32. 第四批：把两个借鉴来源的最后 8 篇读完——**两表 52 篇至此全部为全文级**

**动因**：§31 之后只剩 8 篇摘要级（VLA-01/02/05/12/28 + WM-08/13/20），本轮一次清空，使**"读全文"这条任务结账**。

**做法**：同前——4 个 Explore 子代理并行读全文（`abs` → `html` → PDF），GitHub API 每个 ≤5 次、其余走 `raw`，**不克隆**；产物落 `/tmp/ai4r/{vla0102,vla0512,da_udwm,wm0820}_probe/`。

**结论（本轮的关键事实）**：

| 编号 | 关键新增事实 |
|---|---|
| **VLA-01 DriveGPT4** | **只做开环单步控制**（车速 + 转向角，**非轨迹**），控制量以数字嵌在**文本 token** 里（仿 RT-2）；**闭环是 future work**（§VI）。**⚠ 承诺开源的原文位置更正**：**"The code and dataset will be publicly available" 只写在项目网页、不在论文里**（论文正文只写 "The webpage … is available at …"）；官方 GitHub 无此仓，项目页 Code 链指向**清华云盘 Seafile**。受控消融：去 mix-finetune → CIDEr 99.10→76.51、speed RMSE 1.30→4.67。**未在 CARLA / NAVSIM / Bench2Drive 评测** |
| **VLA-02 ADriver-I** | **⚠ 要拆开**：**VDM 预测的是未来帧图像、不是动作**；单步控制实验用真实帧、动作不经过扩散中间产物；**只有"无限驾驶"里生成帧才回灌 MLLM** → **仅部分落在"世界模型 → 规划器"线上**。动作由 MLLM 出**文本 token 数字**（非 MLP 回归）。**最优数字在私有集、头条数字在 nuScenes，两口径并存**；FID/FVD 与 DriveDreamer 的输入输出帧数不同（4F→4F vs 1F→12F）→ **跨设置比较不公平** |
| **VLA-05 SafeAuto** | **⚠ 措辞更正**：论文全篇用 "**MLN / 一阶逻辑**"、**没有 "fuzzy" 字样** → 此前记的"10 条模糊逻辑硬规则"应改为"**10 条 MLN 一阶逻辑硬规则**"；规则是**乘积 t-范数的可微松弛、无阈值，权重靠训练学习**。**⚠ "否决" = 重写高层动作查询并重新 prompt**（重采样 / 重提示），**不是数值级降级**。**⚠ 无碰撞率、无闭环**（只评 BDD-X 与 DriveLM 开放集），**MLN 边际仅 ~1.2 个准确率点**（91.00→92.18）。**10 条规则原文已抄录**（论文 Tab.17 = 代码 `pgm/config.py:48-98`） |
| **VLA-12 Impromptu VLA** | **是"数据集 + 微调配方"，不是新规划架构**（~80 k clips）。**⚠ 轨迹口径三方不一致**：**prompt(3 步) / parser(6 点) / 论文(5 s)**，且**训练 prompt 用 `[displacement, theta]`、推理用 `[x, y]`，语义亦不一致**。**无"CoT 对齐动作"的受控消融**；**Tab.2 的 Static 子项反而变差**而摘要只报均值；**前视训练 vs 3 路推理** |
| **VLA-28 DriveAction** | **动作根树 = 三层（顶层动作节点 → 中层语言任务 → 底层视觉任务），共 14 个任务**；**⚠ 明确不含轨迹**（§3.2 放弃高频轨迹、只取离散决策；HF 字段仅 QA + `image_0-2`）→ **不能做轨迹级规划评测**；最好 o1 V-L-A 93.56%；**Table 3 与 Table 19 数字冲突** |
| **WM-08 DLWM** | **⚠ 措辞更正**：所谓 "dual" 指**两个独立世界模型**（Gaussian-flow 引导 / ego-planning 引导），**不是两个潜空间**——二者共享**同一潜表示 = BEV 特征**。**与规划的关系：非生成式**——规划头是**回归 MLP**，**世界模型仅作预训练表征**。**✅ Tab.7 Dual vs Unified（去掉解耦 mIoU 19.3→18.9、L2 0.46→0.58）**。**⚠ 世界模型传播用 GT ego motion**（Eq.5，§H 承认）→ 特权信息未突出。**⚠ §4.4 称与 BEV-Planner "tie"，实则碰撞 0.49% vs 0.19%**；**Tab.1 注脚自曝 GaussianWorld 指标重复计算中间帧并自行重评** |
| **WM-13 UniDrive-WM** | **基于 ORION 构建**；**规划器是生成式**（高斯隐空间 + 重参数化 + 回归解码），**⚠ 去掉了 ORION 的 KL 正则**。**接口位 = ①token 级联合自回归 + 轨迹条件**（planning token 紧邻置于 image tokens 之前；AR+Diff 分支接 64 个 latent query 做 **flow-matching 扩散解码**）；**无 RL**。Bench2Drive **DS 79.31 / SR 56.42**（ORION 77.74/54.62）。**✅ Table 6：加生成使 1 s L2 0.269→0.247、碰撞 0.214→0.198**；**⚠ 去检测监督影响最大**（L2 0.482、碰撞 0.387）；**速度 AR 2 fps / AR+Diff 0.4 fps**。**⚠ 摘要"10.4% 碰撞率"无法复现**；nuScenes 碰撞率并非最优（0.31 vs FSDrive 0.19）→ "previous best" 不成立；**只有项目页（README 仍是模板原文）** |
| **WM-20 DrivingGen** | **⚠ §6 原文明确"当前全为 open-loop"、"no standardized closed-loop framework exists yet"、"infeasible at this stage"**，把 CARLA / Navsim 闭环列为未来方向。**⚠ 论文自承两处**：§4.1 称 ADE/DTW 误差可源于生成视频伪影 "impair SLAM-based trajectory recovery"；**B.9 称轨迹类指标与人类一致性最差**；**B.2 对 SLAM 失败帧做常速外推 + 随机抖动**（**使 ADE 15.18 → 16.84**）→ **ADE 数值受管线选择支配**。指标四类 = 分布（FVD + **FTD**）/ 质量 / 时序一致性 / 轨迹对齐；**⚠ 无 FID**；**400 样本 / 14 个模型基线**；**单前视** |

**本轮新增的三条判断**：

1. **"VLA 阶段 1（解释器）"两篇的代表作都不是规划器**：DriveGPT4 只做开环单步控制、ADriver-I 的规划由 MLLM 直接完成 → **引用"VLA 能做规划"时不能从这两篇取证**；它们的价值是**"文本即控制"的早期形态**（与 EMMA / Impromptu 的"轨迹即文本"同源）。
2. **"安全层"这一类目前只有 SafeAuto 一个可读实现，而它的证据强度被两件事限制**：① **否决 = 重新 prompt**（不是数值级投影或降级）；② **只评开放集、无碰撞率、无闭环**，且 **MLN 边际只有 ~1.2 个准确率点** → 对方向 A 而言，**"符号否决层"仍是一个未在闭环下被验证的选项**。
3. **"评生成式规划器"这件事目前没有现成工具，且 DrivingGen 明确承认自己不做** → **不能复用它的轨迹指标**（混入感知误差 + 失败帧外推），**可复用的只有分布 / 质量 / 时序一致性三类框架与 FTD 这个做法**。

**产出**：[vla/papers.md](../topics/vla/papers.md) 新增 **§14（14.1–14.6）**、VLA-01/02/05/12/28 的 §1 行更新、**§8.2 的"模糊逻辑"措辞更正**、§2 证据边界更新（**28/28 全文、13 篇代码核验**）；[world-model/papers.md](../topics/world-model/papers.md) 新增 **§4.5**、WM-08/13/20 的 §1 行与 §5 代码行更新、表头与 §2 证据边界更新（**24/24 全文**）；[state.md](../state.md) 的当前阶段、主要产出、待续第 3 项（**标记为已结账**）、判断边界（DrivingGen 的 §6 原文、"自称世界模型"补三例）。**未克隆任何仓库**。
