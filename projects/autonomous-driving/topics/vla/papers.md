# VLA（驾驶侧）论文表

更新时间：2026-10-01（内容含 §1.1 至第五十七轮；头戳此前停在 2026-09-23）  
**文件结构**：本文件 = 表 + 证据边界 + 边界外清单（**轻量入口**）；**逐篇全文与代码核验结论已拆到两册**——[verification.md](verification.md)（§4–§8）与 [verification-2.md](verification-2.md)（§9–§14）。**凡引用"§4 及以后"的地方请改看这两册。**（拆分原因：原文 110 KB，超 Read 工具 64 KB 上限，无法整读。）  
检索范围：2023–2026，arXiv 12 组查询去重 **510 篇**（`vla1–vla6`），按 [literature-quality.md](../../../../shared/literature-quality.md) 分档筛选后收录 **28 篇**（VLA-01–28；VLA-19 与 VLA-20–28 分别于 2026-09-23 从边界外补入）。  
证据状态：**28/28 已读全文**，其中 **14 篇已做源码级核验**（名单见 §2）；**本表没有任何一篇在本地运行过**。
**代码静态检查的级别**（定义见 [ai/rules.md](../../../../ai/rules.md) §代码静态检查）：**OpenDriveVLA 为 L1**（已落盘到 `code/repos/`，逐文件核验）；**其余 5 个为 L3**（走 GitHub API + `raw` 逐文件取证、**未克隆**）；**ExploreVLA / DriveMoE 等"只有项目页"的为 L2**。**⚠ 第七十轮更正（周扫）**：**DriveMoE（VLA-04）/ ExploreVLA（VLA-18）/ SpanVLA（VLA-26）三篇的官方仓库均存在**，原记"只有项目页 / 无仓库"**是"按论文 `comments` 里的链接判定、未做方法名检索"所致**（见 §2 与下方代码状态表三行）。  
**质量依据**：T 档含义见 [literature-quality.md](../../../../shared/literature-quality.md) §4；venue 与引用数为 OpenAlex 2026-09-23 快照，录用信息优先取 arXiv `comments` 字段（**venue 需三渠道并行核验**，见 §2）。  
相关：[lineage.md](lineage.md)（薄脉络）、[研究对象表](../diffusion-planner/papers/diffusion_planner_ad.md)（DP-Axx）

## 1. 四阶段与代表工作

| 编号 | 论文 | 年 | venue / CCF | 引用 | 输出形态 | 质量依据 |
|---|---|---|---|---|---|---|
| VLA-01 | [DriveGPT4](https://arxiv.org/abs/2310.01412) | 2023 | RA-L / CCF-B | 409 | 语言解释 + 低层控制 | T1：RA-L；`comments` 标注 "Accepted by RA-L"；引用 409。**全文核验（第二十五轮，见 §14.1）**：**只做开环单步控制**（车速 + 转向角，**非轨迹**），控制量以数字嵌在**文本 token** 里（仿 RT-2）；**闭环是 future work**；**⚠ "The code and dataset will be publicly available" 只写在项目网页、不在论文里**（项目页 Code 链指向清华云盘，非 GitHub） |
| VLA-02 | [ADriver-I](https://arxiv.org/abs/2311.13549) | 2023 | arXiv（tech report） | 7 | 语言 + 低层控制 | T4：**与世界模型交叉**（用扩散预测未来帧再出动作）；仅预印本。**全文核验（第二十五轮，见 §14.2）**：**⚠ 要拆开**——**VDM 预测的是未来帧图像、不是动作**，单步控制实验用真实帧，**只有"无限驾驶"里生成帧才回灌 MLLM** → **仅部分落在"世界模型 → 规划器"线上**；动作由 MLLM 出**文本 token 数字**（非 MLP 回归）；**最优数字在私有集、头条数字在 nuScenes，两口径并存**；FID/FVD 与 DriveDreamer 的输入输出帧数不同（4F→4F vs 1F→12F）→ **跨设置比较不公平** |
| VLA-03 | [OpenDriveVLA](https://arxiv.org/abs/2503.23463) | 2025 | AAAI'26 / CCF-A | 25 | 语言中间 waypoint → 轨迹 | T1：AAAI；引用 25 |
| VLA-04 | [DriveMoE](https://arxiv.org/abs/2505.16278) | 2025 | CVPR'26 / CCF-A | 0 | 低层控制（MoE 专家路由） | T2：`comments` 标注 "Accepted by CVPR 2026" |
| VLA-05 | [SafeAuto](https://arxiv.org/abs/2503.00211) | 2025 | arXiv | 0 | 低层控制（符号逻辑否决层） | T3：被 VLA4AD 综述 §4.2 详细讨论（神经符号安全核）；仅预印本。**全文核验（第二十五轮，见 §14.3）**：三件套 = PDCE 损失 / **MLN 安全核** / 多模态 RAG；**⚠ 措辞更正——是 MLN 一阶逻辑、论文无 "fuzzy" 字样**；**⚠ "否决" = 重写高层动作查询并重新 prompt，不是数值级降级**；**⚠ 无碰撞率、无闭环**（只评 BDD-X 与 DriveLM 开放集），**MLN 边际仅 ~1.2 个准确率点**；规则违例率 11.64%→4.50%；**代码完整** |
| VLA-06 | [DiffVLA](https://arxiv.org/abs/2505.19381) | 2025 | arXiv | 1 | 轨迹（VLM 引导扩散） | T4：**与研究对象直接同构**（VLM→扩散引导）；= 研究对象表 DP-A27。**⚠ 代码状态第三十六轮更正**：有官方代码 [boschresearch/DiffVLA](https://github.com/boschresearch/DiffVLA)（36★），**但发布版轨迹头已从扩散换成 EPDM 打分头**（→ 45.0 不可复现），见 [笔记 §代码核验](notes/VLA-06-diffvla.md) |
| VLA-07 | [ReCogDrive](https://arxiv.org/abs/2506.08052) | 2025 | arXiv | 1 | 轨迹（自回归 VLM + 扩散） | T4：同上；= DP-A28。**⚠ 代码状态第三十六轮更正**：有官方代码 [xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive)（**611★**，ICLR 2026，2026-09-22 仍在更新）；代码级核验在研究对象侧完成（[C003 §M](../../code/traces/diffusion_planner_code_traces-2.md)） |
| VLA-08 | [KnowDiffuser](https://arxiv.org/abs/2603.10441) | 2026 | arXiv | — | 轨迹（LLM 元动作→锚点先验） | T4：同上；= DP-A30 |
| VLA-09 | [EMMA](https://arxiv.org/abs/2410.23262)（End-to-End Multimodal Model for AD） | 2024 | **TMLR**（Waymo） | 5 | 多任务（检测 + 规划） | **⚠ venue 更正（第二十五轮）**：arXiv `comments` 显示 "**Accepted by TMLR**"（附 OpenReview `kH3t5lmOU8`）→ 此前记的"仅预印本（T4）"应改为 **TMLR 录用**。团队 Waymo；**无代码**（项目页是 Waymo blog）。**全文核验（第二十五轮，见 §13.1）**：**"轨迹即文本"的第二个实例**（轨迹写成纯文本浮点数，无回归头、无特殊 token）；**语言中间层受控消融 +6.7%**（关键物体 +1.5 / 元决策 +3.0）；nuScenes L2 Avg 0.32（EMMA+ 0.29）；**未在 NAVSIM 评测** |
| VLA-10 | [CoVLA](https://arxiv.org/abs/2408.10845) | 2024 | WACV'25（白名单） | 27 | 轨迹 | T1：WACV'25；引用 27。**全文核验（第二十五轮，见 §13.2）**：**以数据集为主**（10,000 场景 / 83.3 h / 6 M 帧，全自动标注）+ 基线 **CoVLA-Agent**；**轨迹用"特殊 token + MLP 回归头"，与 EMMA 的"轨迹即文本"正好相反**；**只在自有数据集评 ADE/FDE、无任何外部 benchmark 与基线对比**；**语言中间层受控对照：GT 字幕 vs 预测字幕 ADE 降 14.8%**；**无代码**（只有 HF 数据集） |
| VLA-11 | [AutoVLA](https://arxiv.org/abs/2506.13757) | 2025 | NeurIPS'25 / CCF-A | 0 | 离散 drive token → 轨迹 | T2：`comments` 标注 "NeurIPS 2025" |
| VLA-12 | [Impromptu VLA](https://arxiv.org/abs/2505.23757) | 2025 | arXiv | 0 | 轨迹（CoT 对齐动作） | T3：被 VLA4AD 综述 §4.4 详细讨论；仅预印本。**全文核验（第二十五轮，见 §14.4）**：**是"数据集 + 微调配方"，不是新规划架构**（~80 k clips，由 8 个开源数据集 2 M clips 蒸馏；Qwen2.5-VL 3B/7B）；**生成式轨迹即文本**；**⚠ 轨迹口径三方不一致——prompt(3 步) / parser(6 点) / 论文(5 s)**，且**训练 prompt 用 `[displacement, theta]`、推理用 `[x, y]`，语义亦不一致**；**无"CoT 对齐动作"的受控消融**；**Tab. 2 的 Static 子项反而变差**而摘要只报均值 |
| VLA-13 | [DriveVLM](https://arxiv.org/abs/2402.12289) | 2024 | CoRL'24（白名单） | — | 语言中间层 → 轨迹 | T1；**已有全文笔记** [E2E-10](../../direction/notes/E2E-10-drivevlm.md) |
| VLA-14 | [DriveLM](https://arxiv.org/abs/2312.14150) | 2024 | ECCV'24 / CCF-B | — | Graph VQA → 轨迹 | T1；**已有全文笔记** [E2E-11](../../direction/notes/E2E-11-drivelm.md) |
| VLA-15 | [ORION](https://arxiv.org/abs/2503.19755) | 2025 | arXiv | — | 轨迹 + 解释（QT-Former 记忆） | T3：被 VLA4AD 综述 §4.4 详细讨论；仅预印本 |
| VLA-16 | [MindDrive](https://arxiv.org/abs/2512.13636) | 2025 | ECCV'26（白名单） | 5 | 轨迹（在线 RL） | T2：`comments` 标注 "Accepted by ECCV 2026" |
| VLA-17 | [Drive My Way](https://arxiv.org/abs/2603.25740) | 2026 | CVPR'26 / CCF-A | 0 | 轨迹（驾驶风格偏好对齐） | T2：`comments` 标注 "CVPR 2026" |
| VLA-18 | [ExploreVLA](https://arxiv.org/abs/2604.02714) | 2026 | ECCV'26（白名单） | 0 | 轨迹（稠密世界建模 + 探索） | T2：`comments` 标注 "Accepted to ECCV 2026"；~~**"有代码"需更正**——`comments` 的 code 链接指向的**就是项目页本身**，项目页只有图/表/BibTeX，**没有 GitHub 仓库**（2026-09-23 核实）~~ → **⚠ 第七十轮更正（周扫）**：**官方仓存在**：[zihaosheng/ExploreVLA](https://github.com/zihaosheng/ExploreVLA)（30★ / MIT / pushed 2026-07-26）——**但属"部分发布"**（model / ckpt 仍未发） |
| VLA-19 | [SimLingo](https://arxiv.org/abs/2503.09594) | 2025 | **CVPR'25 / CCF-A** | — | 轨迹 + 语言（三任务：闭环驾驶 / 视觉语言理解 / **语言-动作对齐**） | T1：`comments` 明确 "**CVPR 2025**. 1st Place @ CARLA Challenge 2024"；**纯相机**（明确排除 LiDAR）；Bench2Drive **SOTA**。**2026-09-23 从边界外补入**——此前未收录是因未取到 venue。**注意：CarLLaVA（2406.10165）是本工作的 preliminary 挑战赛技术报告**（`comments` 原文指向），同组 |

| VLA-20 | [AutoMoT](https://arxiv.org/abs/2603.14851) | 2026 | **ICML'26 Spotlight Poster / CCF-A** | — | 统一 VLA（理解 / 决策 / 规划三专家）+ **异步推理** + **扩散动作精修头** | **T1（第二十四轮从边界外补入）**：**venue 独立核实**（ICML 官方 slides `icml.cc/media/icml-2026/Slides/64489.pdf` + poster 页 `659594` + 一作 LinkedIn 明示 accepted）。团队 = **NTU AutoMan Lab + Harvard + 小米汽车**；代码 `OscarHuangWind/AutoMoT` + HF 模型 `Oscar-Huang/AutoMoT` + HF 数据集 `Oscar-Huang/nuSync`。**与研究对象最相关的一条**：它有 **"Generative (Diffusion) Head" / diffusion-based action refiner** → **Bench2Drive 87.34 DS / 70.00% SR，加 refiner 后 89.42 DS / 74.09% SR** → **VLA 侧"带扩散头"的实证，且 B2D 成绩高于 SimLingo（85.07）**。**⚠ 全文 + 代码核验后必须降级（第二十四轮，见 §9）**：**其 "Action Refiner"（扩散头）根本没发布**——仓库 TODO `- [ ] Release the Action Refiner` 未勾选，**全仓 grep `diffusion`/`refiner`/`denois`/`adaln` 零命中**，实际规划头是**纯 MLP 回归**（`WaypointsHead`），推理直接 `waypoints_head(...)` 后送 PID；README 自报的数字是 **87.34 DS / 70.00 SR（即不含 AR 的口径）** → **89.42 / 74.09 不可从发布代码复现**。另：**论文写 multi-view，代码只有 4 帧前视 RGB + 1 帧 LiDAR BEV**；**"37 ms · 27 Hz" 是不含 AR 的口径**（开 AR 后 63.0 ms / 16.0 Hz） |
| VLA-21 | [NuInteract](https://arxiv.org/abs/2505.08725) | 2025 | **IEEE TIP 2026 / CCF-A** | 1 | 多视角图文数据集（1.5M pairs）+ DriveMonkey 框架（3D grounding） | **T1（第二十四轮从边界外补入）**：**venue 独立核实**——DOI `10.1109/tip.2026.3719473` 经 Crossref 反查确认为 **IEEE Transactions on Image Processing, 2026**，标题与 arXiv 一致。团队 = HUST（Xiang Bai）+ 小米汽车；代码 `zc-zhao/DriveMonkey`。**注意**：arXiv `comments` 只写 "The dataset and code will be released at this https URL"，**不含 venue 信息** → **venue 不能只看 arXiv comments**。**全文 + 代码核验（第二十五轮，见 §12）**：**⚠ 它是"理解侧"的数据集 + 理解侧模型，不是 VLA 规划器**——论文 §VI 自述 "planning tasks only concentrate on **high-level commands rather than specific trajectories**"，**代码全仓无任何 trajectory / waypoint**；数据集 **850 场景 / 34 K 帧 / 1.5 M pairs**（nuScenes 自动标注）；代码与数据**真实发布**（GitHub Releases + HF 权重） |
| VLA-22 | [VaViM / VaVAM](https://arxiv.org/abs/2502.15672) | 2025 | arXiv（无录用信息） | — | 自回归**视频**生成模型 + 视频-动作模型（6 waypoint @2Hz） | **T4（第二十四轮从边界外补入）**：团队 = **valeo.ai**（法国 Valeo 工业研究实验室）；官方代码 + **权重** `valeoai/VideoActionModel`（170 stars）。研究"视频预训练能否迁移到驾驶" → 与"世界模型 → 规划器"这条借鉴线相关。**全文 + 代码核验（第二十五轮，见 §11.1）**：**VaVAM = VaViM + flow matching 动作专家（Euler 10 步）**，接口是**逐层 joint attention**；**⚠ 论文称"完整 pipeline"但代码 `video_action_model.py:64` 冻结 VaViM**；**无受控消融**（没有"视频预训练 vs 从零训练"对照）；NeuroNCAP "SOTA" 是**闭式口径 + 基线全无后处理** |
| VLA-23 | [UniDriveVLA](https://arxiv.org/abs/2604.02190) | 2026 | arXiv（无录用信息） | — | MoT 三专家解耦理解 / 感知 / 规划的统一 VLA | **T4（第二十四轮从边界外补入）**：团队 = HUST + **小米汽车** + 澳门大学；官方代码 + 模型 `xiaomi-research/unidrivevla`。**与 VLA-20 AutoMoT 同属"小米系 MoT-VLA"**。**全文核验（第二十四轮，见 §10.3）**：**MoT 三专家（理解/感知/规划）+ Action 分支内嵌 flow-matching 轨迹生成**，**全文无 RL/GRPO**；**采样步数与起点分布论文未给**；**Bench2Drive DS 78.37 / SR 51.82 / Effi 198.86 / Comf 11.78**，多能力均值 51.53，nuScenes 开环 Avg L2 0.51；消融 MoT vs shared-weight L2 0.533 vs 0.641。**代码/权重/数据均已发布**（Updates 唯一未完成项 `Release model on Navsim`）→ **本批四篇里唯一接近可复现的** |
| VLA-24 | [LaST-VLA](https://arxiv.org/abs/2603.01928) | 2026 | arXiv（无录用信息） | — | 潜时空 CoT + GRPO | **T4（第二十四轮从边界外补入）**：团队 = 清华 + **小米汽车** + 澳门大学；论文称代码已提供。**NAVSIM v1 91.3 PDMS / v2 87.1 EPDMS** → 与"RL 后训练"这条线相关。**全文核验（第二十四轮，见 §10.2）**：**纯自回归离散 token，无扩散/流匹配/VAE**（waypoints 用**文本 token** 表示）；其 **GRPO 是较完整的一种**（组内标准化优势 + **clip** + **KL**，无 critic/GAE），**"RL 词义核验"第 8 种**；消融 **去 WM+3D 的 RL 87.2 vs 全量 91.3（+4.1）**、**文本 CoT 87.2 vs 潜 CoT 91.3（+4.1）**；**单目前视相机**。**代码实际不可复现**：`luo-yc17/LaST-VLA` 的 "Currently Supported Features" **四项全未勾选**（推理代码 / 权重 / 训练代码 / 训练数据） |
| VLA-25 | [Reasoning-VLA](https://arxiv.org/abs/2511.19912) | 2025 | arXiv（无录用信息） | — | 可学习 action queries + SFT/RL 的通用 VLA | **T4（第二十四轮从边界外补入）**：团队 = **NUS（Tat-Seng Chua）+ 兰大 + USTC + 清华 + UNSW**；官方代码 `xipi702/Reasoning-VLA`。**全文 + 代码核验（第二十五轮，见 §11.2）**：**动作是连续回归**（可学习 action queries 双向 mask 一次前向出全部轨迹）；**论文声明用 GRPO**（critic-free、组内打分做 advantage）但**代码仓库是空壳**（只有 113 B README）→ **不可核验**；**奖励是硬 0/1 阶跃规则分**；**7B+ 开环变好但闭环变差** |
| VLA-26 | [SpanVLA](https://arxiv.org/abs/2604.19710) | 2026 | arXiv（无录用信息） | — | 自回归推理 + **flow-matching 动作专家 + GRPO**（负样本 / 恢复） | **T4（第二十四轮从边界外补入）**：团队 = **UCLA + Motional + Northeastern**（Motional 为知名 AV 公司）；仅项目页。**与研究对象最相关**：**flow-matching 动作专家 + GRPO** 正是本项目方向 A/B 的组合。**全文核验（第二十四轮，见 §10.1）**：起点是**历史轨迹嵌入经 MLP**（**不是纯高斯**，训练注入高斯噪声）、**5 步**；**动作头受控消融：flow matching 90.3 vs L1 回归 85.1（+5.2 PDMS）**，代价是动作生成 0.02→0.08 s；**RFT 82.1→90.3（+8.2）**；其 "GRPO" **论文自己声明取消了 clip**（§4.1 原文 "single policy update per step … eliminates the need for clipping"），奖励是**复合式**（PDMS + 负样本 L2 + 恢复 + 推理长度 + 一致性规则）。**无 Bench2Drive**；~~**无 GitHub 仓库、也未承诺发布**~~ → **⚠ 第七十轮更正（周扫）**：**官方仓存在**：[motional/SpanVLA](https://github.com/motional/SpanVLA)（53★ / pushed 2026-04-29）——**但仓内只有 `README.md` + `images/`（2.8 MB），无任何代码**（Release Plan 未打勾）→ **"代码待发布"成立，"无仓库"不成立** |
| VLA-27 | [Counterfactual VLA](https://arxiv.org/abs/2512.24426) | 2025 | arXiv（无录用信息） | — | **自反思 VLA**：反事实推理修正 meta-action 后再出轨迹 | **T4（第二十四轮从边界外补入）**：团队 = **NVIDIA + UCLA + Stanford**（Marco Pavone、Bolei Zhou、Danfei Xu、Yan Wang）；**未找到官方仓库**。**全文核验（第二十五轮，见 §11.3）**：**⚠ "counterfactual" 名不副实**——摘要称 "simulates potential outcomes"，但**全文无任何前向仿真 / 世界模型 / verifier**（§1 自述 "without an external world model or verifier"），实质是**用 GT meta-action 事后诊断文本做 SFT**；**⚠ 无任何公开 benchmark**（只在私有 80,000 h 数据上开环评）；**受控对照显示"反思推理"本身只值约 3%**（multi-round 数据重采样就值 5%） |
| VLA-28 | [DriveAction](https://arxiv.org/abs/2506.05667) | 2025 | arXiv（无录用信息） | — | VLA 驾驶决策**基准**（16,185 QA / 2,610 场景，动作根树评估） | **T4（第二十四轮从边界外补入）**：团队 = **Li Auto Inc.（理想汽车）**；数据集已开源（HF `LiAuto-DriveAction/drive-action`）。**注意这是数据集/基准，不是规划器**。**全文核验（第二十五轮，见 §14.5）**：**动作根树 = 三层（顶层动作节点 → 中层语言任务 → 底层视觉任务），共 14 个任务**；**⚠ 明确不含轨迹**（§3.2 放弃高频轨迹、只取离散决策；HF 字段仅 QA + `image_0-2`）→ **不能做轨迹级规划评测**；最好 o1 V-L-A 93.56%；**Table 3 与 Table 19 数字冲突**；无代码仓库 |

**阶段归属**：VLA-01/02 属阶段 1（解释器）；03–08 属阶段 2（模块化）；09–14 与 **19** 属阶段 3（端到端）；15–18 属阶段 4（推理增强）；**20–28 属阶段 3/4 的 2025–2026 增补（第二十四轮从边界外补入）**。分界标志见 [lineage.md](lineage.md)。

## 1.1 逐行证据等级与代码状态（2026-09-30 补，供跨表检索）

> 证据等级定义见 [rules.md](../../../../ai/rules.md) §证据等级；代码状态取自 §2 与本表各行「质量依据」列 + [repositories.md §E](../../code/repositories.md)，**未新查**。

| 编号 | 证据等级 | 代码状态 |
|---|---|---|
| VLA-01 DriveGPT4 | 全文 | 无代码（项目页指向清华云盘） |
| VLA-02 ADriver-I | 全文 | 无代码 |
| VLA-03 OpenDriveVLA | 全文 + 代码 L1 | **有代码**（落盘逐文件核验） |
| VLA-04 DriveMoE | 全文 + 代码 L3 | **有代码**（[Thinklab-SJTU/DriveMoE](https://github.com/Thinklab-SJTU/DriveMoE)，235★ / pushed 2026-07-03 / 含 `src/` `config/` `ckpts/`）——**⚠ 第七十轮更正**：原记"只有项目页（无仓库）" |
| VLA-05 SafeAuto | 全文 + 代码 L3 | **有代码**（完整） |
| VLA-06 DiffVLA | 全文 + 代码 L3 | **有代码但发布版换头**（45.0 不可复现） |
| VLA-07 ReCogDrive | 全文 + 代码 L3 | **有代码**（611★，核验在研究对象侧） |
| VLA-08 KnowDiffuser | 全文 | = DP-A30（见研究对象表） |
| VLA-09 EMMA | 全文 | 无代码 |
| VLA-10 CoVLA | 全文 | 只有数据集（HF），无代码 |
| VLA-11 AutoVLA | 全文 + 代码 L3 | **有代码**（API 逐文件取证） |
| VLA-12 Impromptu VLA | 全文 + 代码 L3 | **有代码** |
| VLA-13 DriveVLM | 全文 | 无代码（= E2E-10，项目主页） |
| VLA-14 DriveLM | 全文 | 有仓库（数据/挑战赛工具为主） |
| VLA-15 ORION | 全文 + 代码 L3 | **有代码** |
| VLA-16 MindDrive | 全文 + 代码 L3 | **有代码** |
| VLA-17 Drive My Way | 全文 + 代码 L3 | **有代码** |
| VLA-18 ExploreVLA | 全文 + 代码 L3 | **有代码（部分发布）**（[zihaosheng/ExploreVLA](https://github.com/zihaosheng/ExploreVLA)，30★ / MIT / pushed 2026-07-26；**model / ckpt 未发**）——**⚠ 第七十轮更正**：原记"无仓库（只有项目页）" |
| VLA-19 SimLingo | 全文 + 代码 L3 | **有代码**（补上 N_w/N_p） |
| VLA-20 AutoMoT | 全文 + 代码 L3 | **有代码但扩散头未发布** |
| VLA-21 NuInteract | 全文 + 代码 L3 | **有代码**（DriveMonkey，真实发布） |
| VLA-22 VaViM/VaVAM | 全文 + 代码 L3 | **有代码+权重** |
| VLA-23 UniDriveVLA | 全文 | **有代码+模型+数据** |
| VLA-24 LaST-VLA | 全文 | 有仓库但四项未发布（不可复现） |
| VLA-25 Reasoning-VLA | 全文 + 代码 L3 | 代码空壳（113 B README） |
| VLA-26 SpanVLA | 全文 | **有仓库但仓内无代码**（[motional/SpanVLA](https://github.com/motional/SpanVLA)，53★，仅 README + images）——**⚠ 第七十轮更正**：原记"无仓库" |
| VLA-27 Counterfactual VLA | 全文 | 无仓库 |
| VLA-28 DriveAction | 全文 | 只有数据集，无代码 |

## 2. 证据边界
- **在表 28 篇**（VLA-01–28），**全部 28 篇均已读全文**（第一轮建表的 19 篇 + 第二十四轮补入的 20–28；最后 5 篇 01/02/05/12/28 于第二十五轮补齐，见 §14）。
- **代码核验**：**14 篇已做源码级核验**——**DiffVLA（§4.4，第三十六轮 L3）**、AutoVLA / OpenDriveVLA（§5）、SimLingo（§6）、**ORION / MindDrive / Drive My Way（§7）**、**SafeAuto 与 Impromptu VLA（§8）**、**AutoMoT（§9）**、**VaViM/VaVAM（完整，§11.1）、Reasoning-VLA（空壳仓库，§11.2）、Counterfactual VLA（无仓库，§11.3）**、**NuInteract / DriveMonkey（真实发布，§12）**；**ExploreVLA / DriveMoE ~~无仓库可核~~** → **⚠ 第七十一轮更正：两篇的官方仓都存在**（ExploreVLA 30★ / DriveMoE 235★，见 §2 与代码状态表），**判据错在"只看论文链接、未做方法名检索"**；**本表没有任何一篇在本地运行过**（全部为静态检查）。**注**：§10–§14 是**全文级**（`WebFetch`/`curl` 读 HTML + PDF）；**代码侧只有 §11.1 VaVAM 与 §12 DriveMonkey 是"完整可训练"**——**SpanVLA 有仓库但仓内无代码**（⚠ 第七十一轮更正）、LaST-VLA 四项全未发布、Reasoning-VLA 空壳、CF-VLA 只有项目主页、EMMA / CoVLA / DriveGPT4 / ADriver-I / DriveAction 无代码。
- 引用数为 **OpenAlex 2026-09-23 快照**，会变动；2025–2026 年的工作引用数接近 0 属正常（见 [literature-quality.md](../../../../shared/literature-quality.md) §1）。
- `—` 表示 OpenAlex 未返回可用引用数，**不是 0**。
- 已发表信息优先取 `comments` 字段，其次取 OpenAlex 的正式版记录；两者冲突时以 `comments` 为准并在此说明。**第二十四轮的教训：venue 不能只看 arXiv `comments`**——VLA-20 AutoMoT 与 VLA-21 NuInteract 的 `comments` 里**都没有录用信息**，venue 是靠 ICML 官方 slides/poster 页与 **Crossref 按 DOI 反查**才拿到的（见 §3）。
- **未核实项**：LMDrive、RAG-Driver 在综述中被列为代表工作，但**取不到可核验的 venue**，故未收录（见 §3 边界外清单）；CarLLaVA 已查清是 SimLingo 的 preliminary 技术报告；**SimLingo 已于 2026-09-23 补入为 VLA-19**。

## 3. 边界外清单（含**第二十四轮的 15 条逐一复核**）

**第二十四轮对清单做了逐条复核（15 条），结果：9 条升为正式收录（VLA-20–28），2 条因"仅 Workshop / 匿名投稿"继续留在边界外，4 条仍不确定。** 复核口径按 [literature-quality.md](../../../../shared/literature-quality.md)：已发表看 CCF/白名单（T1/T2）；预印本看**强团队 +（官方代码 或 方法独特）**（T4）。

| 条目 | 复核到的信息 | 判定 |
|---|---|---|
| **NuInteract**（2505.08725） | **IEEE TIP 2026（CCF-A）**，DOI `10.1109/tip.2026.3719473` 经 Crossref 反查确认；HUST + 小米汽车 | **升为 VLA-21（T1）** |
| **AutoMoT**（2603.14851） | **ICML 2026 Spotlight Poster（CCF-A）**，ICML 官方 slides/poster 页 + 一作明示；NTU AutoMan Lab + Harvard + 小米汽车；代码/模型/数据集全开源；**带扩散动作精修头** | **升为 VLA-20（T1）** |
| **VaViM / VaVAM**（2502.15672） | valeo.ai；官方代码 + **权重**（170 stars） | **升为 VLA-22（T4）** |
| **UniDriveVLA**（2604.02190） | HUST + 小米汽车 + 澳大；官方代码 + 模型 | **升为 VLA-23（T4）** |
| **LaST-VLA**（2603.01928） | 清华 + 小米汽车 + 澳大；称代码已提供；NAVSIM v1 91.3 / v2 87.1 | **升为 VLA-24（T4）** |
| **Reasoning-VLA**（2511.19912） | NUS（Tat-Seng Chua）等；官方代码 | **升为 VLA-25（T4）** |
| **SpanVLA**（2604.19710） | UCLA + **Motional** + Northeastern；flow-matching + GRPO | **升为 VLA-26（T4）** |
| **Counterfactual VLA**（2512.24426） | **NVIDIA + UCLA + Stanford**（Pavone / Zhou / Xu）；自反思机制；**无官方仓库** | **升为 VLA-27（T4）** |
| **DriveAction**（2506.05667） | **Li Auto**；数据集已开源（HF） | **升为 VLA-28（T4，但它是基准不是规划器）** |
| **LangCoop**（2504.13406） | 查到 **CVPR**W**2025**（Workshop，不在白名单），引用 9；Texas A&M + KAIST | **继续留在边界外**（仅 Workshop；原"无录用信息"的理由已失效，改记这一条） |
| **StyleVLA**（2603.09482） | TUM + NTU；**匿名投稿**（8 页，投 IEEE），仅匿名页 | **继续留在边界外**（匿名投稿 + 无公开代码） |
| **HiST-VLA**（2602.13329） | Bosch Corporate Research + 上海大学；NAVSIM v2 EPDMS 88.6；**无代码** | **仍不确定**（团队强，但无代码也无录用 → 未同时满足 T4 双条件） |
| **SAMoE-VLA**（2603.08113） | 清华 AIR（Yan Wang 组）；代码仅 "will be released soon" | **仍不确定**（同上） |
| **LVDrive**（2605.22089） | HKUST（Dan Xu）+ 小米汽车；**无代码、无录用** | **仍不确定**（同上） |
| **AutoDrive-R²**（2509.01944） | **阿里 AMAP** + 中山大学等；**无代码、无录用** | **仍不确定**（同上） |
| LMDrive（[2312.07488](https://arxiv.org/abs/2312.07488)）、RAG-Driver（[2402.10828](https://arxiv.org/abs/2402.10828)） | arXiv ID 已确认，但 `comments` 分别只给项目页 / 篇幅信息，**venue 仍不可核验** | 继续留在边界外 |
| CarLLaVA（[2406.10165](https://arxiv.org/abs/2406.10165)） | `comments` 只写 "Outstanding Champion & Innovation Award @ CARLA Autonomous Driving Challenge"，无会议录用；且**已被 SimLingo 的 `comments` 明确指为后者的 preliminary 挑战赛技术报告** | **不单独收录**，作为 VLA-19 的指针 |
| VDRive、Discrete Diffusion for Reflective VLA、WAM-Diff | 与研究对象相关（VLA + 扩散），但 `comments` 标注 WIP/篇幅 | 未达 T4 门槛，留在边界外 |

**一条方法论收获**：**"取不到 venue"常常不是"没有 venue"，而是"arXiv `comments` 里没写"**——AutoMoT 与 NuInteract 的 venue 分别是从 **ICML 官方 slides/poster 页** 与 **Crossref 按 DOI 反查**拿到的。→ **venue 核验要三渠道并行：arXiv `comments` + OpenAlex 按标题 + Crossref 按 DOI**（且 OpenAlex 匿名查询会 429 限流，需备用渠道）。

## 4. 已读全文与代码核验（已拆出）

**逐篇详细结论已拆到两册**：[verification.md](verification.md)（§4–§8，38.6 KB）与 [verification-2.md](verification-2.md)（§9–§14，49.5 KB）。索引：

| 节 | 内容 |
|---|---|
| §4 | 已读全文（4.0 第一轮 / 4.1 第二十四轮 / 4.2 第二十一轮 / 4.3 第二十二轮） |
| §5 | 代码级核验：AutoVLA（5.1）、OpenDriveVLA（5.2） |
| §6 | SimLingo 的代码级核验 |
| §7 | ORION / MindDrive / Drive My Way 的代码级核验 |
| §8 | 剩余 6 篇的代码可用性 + Impromptu VLA / SafeAuto 的源码核验 |
| §9 | AutoMoT（VLA-20）：**扩散头没有发布** |
| §10 | SpanVLA / LaST-VLA / UniDriveVLA 全文核验 |
| §11 | VaViM/VaVAM、Reasoning-VLA、Counterfactual VLA |
| §12 | NuInteract（VLA-21） |
| §13 | EMMA（VLA-09）与 CoVLA（VLA-10） |
| §4–§8 | → [verification.md](verification.md) |
| §9–§14 | → [verification-2.md](verification-2.md) |
