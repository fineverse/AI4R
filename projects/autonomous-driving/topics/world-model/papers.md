# 世界模型（驾驶侧）论文表

更新时间：2026-10-01（内容含 §1.1 至第六十轮；头戳此前停在 2026-09-23）  
**文件结构**：本文件 = 表 + 证据边界 + 补录结果 + 代码可用性全表（**轻量入口**）；**§4 的逐篇全文核验结论已拆到** [verification.md](verification.md)（53.7 KB）。**凡引用"§4"的地方请改看该册。**（拆分原因：原文 73 KB，超 Read 工具 64 KB 上限，无法整读。）  
检索范围：2023–2026，arXiv 12 组查询去重 **510 篇**（`wm1–wm6`），按 [literature-quality.md](../../../../shared/literature-quality.md) 分档筛选后收录 **24 篇**。  
证据状态：**全部 24 篇均已读全文**（第二十四、二十五轮分四批补齐，逐篇结论见 [verification.md](verification.md)）；其中 **14 篇已做代码级核验**（WM-01、**WM-02**、WM-03、WM-04、WM-06、WM-07、**WM-10**、WM-11、**WM-15、WM-16**、WM-17、WM-18、WM-20、WM-24，见 [world_model_code_traces.md](../../code/traces/world_model_code_traces.md) 与 §5）。  
**代码静态检查的级别**（定义见 [ai/rules.md](../../../../ai/rules.md) §代码静态检查）：**已克隆的 4 个（OccWorld / PWM / Drive-WM / WorldRFT）为 L1**；**走 `raw` 的 6 个（WoTE / DriveLaW / Drive-OccWorld / World4Drive / LAW / DrivingGen）为 L3**（**未克隆**）；**空仓或范围不符的为 L2**。  
**质量依据**：T 档含义见 [literature-quality.md](../../../../shared/literature-quality.md) §4；venue 与引用数为 OpenAlex **2026-09-23 快照**，录用信息优先取 arXiv `comments` 字段。  
相关：[lineage.md](lineage.md)（薄脉络）、[研究对象表](../diffusion-planner/papers/diffusion_planner_ad.md)（DP-Axx）

## 1. 按预测表示分类的代表工作

| 编号 | 论文 | 年 | venue / CCF | 引用 | 预测表示 | 与规划的关系 | 质量依据 |
|---|---|---|---|---|---|---|---|
| WM-01 | [Drive-WM（Driving into the Future）](https://arxiv.org/abs/2311.17918) | 2023 | CVPR'24 / CCF-A | 100 | 多视角视频 | 视频预测 + 规划，有官方代码（**代码仅含图像生成侧**） | T1：CVPR'24；引用 100；**代码核验：仓库为 vendored diffusers，tree-based planner 与 image reward 不在仓库内** |
| WM-02 | [DriveWorld](https://arxiv.org/abs/2405.04390) | 2024 | CVPR'24 / CCF-A | 25 | 4D 预训练表征（3D 占据 + 动作） | **预训练表征，不是规划器**：只有"图像 → BEV"编码器被预训练，**世界模型 rollout 层在微调时被丢弃**；规划头**直接沿用 UniAD**（单模回归）。navtest 无；nuScenes 开环 L2 0.92 / 碰撞 0.26%（vs UniAD 1.03 / 0.31）。**无官方代码**（综述指向的 `yvanyin/drivingworld` 是**另一篇**） | T1：CVPR'24（`comments` 标注）；引用 25；**第二十五轮升全文，见 §4.3** |
| WM-03 | [OccWorld](https://arxiv.org/abs/2311.16038) | 2023 | ECCV'24 / CCF-B | 62 | 3D 占据 | 占据预测 → 轨迹，有官方代码 | T1：ECCV'24（OpenAlex 记为 LNCS）；引用 62 |
| WM-04 | [Drive-OccWorld](https://arxiv.org/abs/2408.14197) | 2024 | AAAI'25 / CCF-A | 11 | 4D 占据（未来语义占据 + 3D flow） | **④选优依据**：世界模型出未来占据 → Agent-Safety + Road-Safety + **Learned-Volume** 三项 cost → 取最小；**规划器是 ST-P3 式"采样 + 规则 cost 选优"，非生成式**；**候选数论文未给**。nuScenes 开环 L2 avg 0.85（†）/ 0.47（‡）/ 0.32（‡∗）。**⚠ 无"去掉世界模型"的规划消融** | T2：`comments` 标注 "Accepted by AAAI2025"；**第二十五轮升全文，见 §4.4**；代码见 [C004 §I](../../code/traces/world_model_code_traces.md) |
| WM-05 | [Implicit Residual World Models](https://arxiv.org/abs/2510.16729) | 2025 | ICRA'26（白名单） | — | 4D 占据（隐式残差，**残差加在 BEV 特征层**） | **④选优依据 + 隐状态条件**：`S^bev_t = ΔS^bev_t + S^bev_{t-1}`，预测**未来 4 帧**；规划器非生成式（plan query 出位移）。**三档耦合**：Tightly（占据经 ST-P3 cost 过滤）/ **Semi（默认，纯特征条件）** / Fully Decoupled。**✅ 受控消融：Decoupled L2 0.87 vs Semi 0.53（+0.34 m）**。**⚠ 没有"去掉残差"的消融**，且代码那行加法挂着 `# TODO: predict residual bev features` | T2：`comments` 标注 "ICRA 2026"；**第二十五轮升全文，见 §4.4**；代码在同仓 `ir-wm` 分支 |
| WM-06 | [Latent World Model（Enhancing E2E AD with LWM）](https://arxiv.org/abs/2406.08481) | 2024 | ICLR'25 / CCF-A | — | 潜特征 | 自监督潜空间 → 端到端规划 | T2：`comments` 标注 "ICLR 2025" |
| WM-07 | [World4Drive](https://arxiv.org/abs/2507.00603) | 2025 | ICCV'25 / CCF-A | — | 潜特征（意图感知） | **④选优依据（信号 = 潜空间重建距离）**：预测未来帧潜，`argmin` 选模态、ScoreNet focal loss 对齐；**规划器非生成式**（词表 6 条 × 3 命令）。**✅ Table 3 是本工作空间最干净的一条"世界模型有无"受控消融：无 WM 行 L2 0.61 / 碰撞 0.36 → 全量行 L2 0.50 / 碰撞 0.16（即"去掉世界模型"则 L2 劣化 18.0%、碰撞率劣化 55.6%）**。nuScenes L2 avg 0.50 / 碰撞 0.16；**NAVSIM PDMS 85.1（仅相机）** | T2：`comments` 标注 "ICCV 2025"；**第二十五轮升全文，见 §4.4**；代码见 [C004 §I](../../code/traces/world_model_code_traces.md) |
| WM-08 | [DLWM](https://arxiv.org/abs/2604.00969) | 2026 | CVPR'26 / CCF-A | — | 潜特征（**两个独立世界模型**，共享 BEV 潜表示） | **预训练表征，不是规划器**：高斯中心两阶段自监督（3D 语义高斯渲染重建）；**规划头是回归 MLP**，推理只用感知 + 任务头。**✅ Tab.7 Dual vs Unified：去掉解耦 mIoU 19.3→18.9、L2 0.46→0.58**。规划 L2 0.46 / 碰撞 0.19%。**⚠ "dual" 指两个世界模型，不是两个潜空间**（已更正）；**世界模型传播用 GT ego motion** | T2：`comments` 标注 "Accepted by CVPR 2026"；**第二十五轮升全文，见 §4.5**；**无官方代码** |
| WM-09 | [DriveFuture](https://arxiv.org/abs/2605.09701) | 2026 | arXiv | — | 潜特征（未来感知） | **作为条件喂给扩散规划器**（②隐状态级条件）：世界模型出 **16 个 future query token（d=256）** 喂进去噪器；规划器是 **DDPM DiT（5 层）+ 100 条候选 + GTRS-Dense 选优**。**受控收益 +3.7（navhard 无 scorer：30.9→34.6）；"条件化 vs 辅助损失" +2.5（34.6 vs 32.1）** | T4：**与研究对象直接同构**；= 研究对象表 DP-A31，已有[全文笔记](../diffusion-planner/notes/DP-A31-drivefuture.md)。**⚠ 第二十四轮更正**：此前记的"navhard 24.2→55.5"是**误读**——那两个数字是 Table 1 里**两行不同方法**，且 55.5 **含 GTRS-Dense scorer**；受控消融（Table 4，不含 scorer）只有 30.9→34.6 |
| WM-10 | [TrafficBots](https://arxiv.org/abs/2303.04116) | 2023 | ICRA'23（白名单） | 34 | 矢量化多智能体 | **⚠ 不算"世界模型 → 规划器"这条线**：自称 world model，但**规划模块是 future work**、**全文无自车规划评测**；实体是**多智能体闭环 bot 策略**（共享策略网 + destination 分类 + 16 维 personality CVAE，输出 DiagGaussian 动作经 unicycle 积分）。WOMD 运动预测 mAP 0.212 / minADE 1.313，**低于当年 SOTA** | T1：ICRA'23（`comments` 标注）；引用 34；**第二十五轮升全文，见 §4.3** |
| WM-11 | [DriveLaW](https://arxiv.org/abs/2512.23421) | 2025 | CVPR'26 / CCF-A | — | 潜空间（统一规划与生成） | **潜空间统一规划与视频生成**：Video DiT 去噪第一步的**逐块中间特征**作 cross-attention keys 喂入独立 **133 M Action DiT**（flow matching，5 步，纯高斯先验）。navtest **PDMS 89.1**（> WoTE 88.3 / DiffusionDrive 88.1）。**受控消融最有价值**：**BEV 84.1 / VLM hidden 86.5 / Video latents 89.1**；**scratch 85.9 → 视频预训练 7.6M 帧 89.1**。**⚠ 论文只讲接口 B，代码默认路径却是接口 A**；且 §4.1「联合更新两个 DiT」与 §A.2「梯度隔离」**自相矛盾** | T2：`comments` 标注 "CVPR 2026"；**第二十五轮升全文，见 §4.3**；代码见 [C004 §G](../../code/traces/world_model_code_traces.md) |
| WM-12 | [DrivingGPT](https://arxiv.org/abs/2412.18607) | 2024 | ICCV'25 / CCF-A | — | 多模态自回归 token（**实际只有图像 + 动作**） | **①token 级联合自回归**：VQ-VAE 图像 token 与量化动作 token 同序列交替生成，**未来动作条件于自身生成的图像 token**（"读自己生成出来的未来"）。**NAVSIM PDMS 82.4**（基线 77.8）。**⚠ 无"去掉世界模型"消融**；**仓库 404，不存在** | T2：venue 据 [2512.16760](https://arxiv.org/abs/2512.16760) §3.2 表（ICCV'25）；**第二十五轮升全文，见 §4.4** |
| WM-13 | [UniDrive-WM](https://arxiv.org/abs/2601.04453) | 2026 | ECCV'26（白名单） | — | 统一理解 + 规划 + 生成 | **①token 级联合自回归 + 轨迹条件**：**基于 ORION 构建**，planning token 紧邻置于 image tokens 之前；AR+Diff 分支接 64 个 latent query 做 **flow-matching 扩散解码**。**⚠ 去掉了 ORION 的 KL 正则**；**无 RL**。Bench2Drive **DS 79.31 / SR 56.42**（ORION 77.74/54.62）。**✅ Table 6：加生成使 1 s L2 0.269→0.247、碰撞 0.214→0.198**；**⚠ 去检测监督影响最大**（L2 0.482、碰撞 0.387）；速度 AR 2 fps / AR+Diff 0.4 fps。**⚠ 摘要"10.4% 碰撞率"无法复现**，nuScenes 碰撞率并非最优；**只有项目页（README 仍是模板原文）** | T2：`comments` 标注 "Accepted to ECCV 2026"；**第二十五轮升全文，见 §4.5** |
| WM-14 | [Think2Drive](https://arxiv.org/abs/2402.16720) | 2024 | ECCV'24 / CCF-B | 2 | 潜世界模型（DreamerV3 式 RSSM） | **②隐状态条件 + ⑤RL 的 reward/next-state 来源**：actor-critic 在潜空间想象 rollout T=15。**✅ 唯一受控对照：model-free PPO（Roach）DS 57.5 → 83.8**。**⚠ 奖励 Eq.8 是"速度 + 沿路 + 偏离 + 转向"，不是 CARLA 规则分**；**训练与推理都用特权信息**。DS 83.8 / RC 99.6（CornerCaseRepo）、v2 DS 56.8 | T2：`comments` 标注 "Accepted by ECCV 2024"；**第二十五轮升全文，见 §4.4**；**无官方代码** |
| WM-15 | [AdaWM](https://arxiv.org/abs/2501.13072) | 2025 | ICLR'25 / CCF-A | — | 潜世界模型（BEV 语义图潜状态） | **②隐状态级条件**：Dreamer v3 actor-critic 以 model state 为条件、在想象 rollout 中训练（**非生成式**）；reward/next-state 取自世界模型。**"adaptive" 只是微调调度**（TV 距离判失配、模型侧 LoRA/NoLa、策略侧凸组合权重）。**无官方代码**；**特权 BEV 泄漏到推理侧** | T2：`comments` 标注 "ICLR 2025"；**第二十五轮升全文**，见 §4.2 |
| WM-16 | [Raw2Drive](https://arxiv.org/abs/2505.16394) | 2025 | NeurIPS'25 / CCF-A | — | 双流（原始 + 特权） | **②隐状态条件 + ⑤RL 的 reward/next-state 来源**：两套 Dreamer v3 RSSM + 两 actor-critic，reward/continue 由**特权世界模型头**经 Head Guidance 提供；对齐用 **L2 + KL**（非对抗非对比）。Bench2Drive **DS 71.36 / SR 50.24**；**特权仅训练侧**。**代码只有 README** | T2：`comments` 标注 "Accepted by NeurIPS 2025"；**第二十五轮升全文**，见 §4.2 |
| WM-17 | [Policy World Model](https://arxiv.org/abs/2510.19654) | 2025 | NeurIPS'25 / CCF-A | — | 状态-动作联合 | 从预测转向规划 | T2：`comments` 标注 "Accepted by NeurIPS 2025 (Poster)" |
| WM-18 | [WorldRFT](https://arxiv.org/abs/2512.19133) | 2025 | AAAI'26 / CCF-A | 5 | 潜世界模型 | 潜世界模型规划 + 强化微调，**无代码可核验** | T2：`comments` 标注 "AAAI 2026"；**代码核验：官方仓库为空（仅 LICENSE + readme）** |
| WM-19 | [FutureX](https://arxiv.org/abs/2512.11226) | 2025 | arXiv | — | 潜特征（潜 CoT） | **②隐状态级条件**：潜世界模型出推理链 `Z_CoT`，Summarizer 以 `Z_CoT` + 初始轨迹回归修正量。**规划器是非生成式纯回归**（无扩散/流匹配）；**"条件 + 辅助损失并存"**（`L_lat` 把预测未来潜对齐 GT）。NAVSIM navtest PDMS：LTF **83.8→89.2（+5.4）**、TransFuser **84.0→90.2（+6.2）**；CARLA Longest6 DS **+11.0/+18.6** | T4：与研究对象条件轴同构；仅预印本。**全文核验（第二十四轮）**：**无官方代码**（摘要只写 "Code will be released"，未给 repo URL）→ **"条件 vs 辅助损失"只能按论文文字判断**；且**未来条件与 GT 未来监督纠缠**（`L_lat`），"纯条件收益"难剥离；延迟表 N 与 ms 对应自相矛盾（N=4→17.0 ms，又称 N 减小→31.3 ms） |
| WM-20 | [DrivingGen](https://arxiv.org/abs/2601.01528) | 2026 | ICLR'26 / CCF-A | — | 生成式视频（基准） | **评价工具**：生成式视频世界模型基准（**400 样本 / 14 个模型基线**）。**⚠ §6 明确"当前全为 open-loop"、"no standardized closed-loop framework exists yet"** → **不评规划有效性**；其 **ADE/DTW 从生成视频用 SLAM 反推**，**论文自承与人类一致性最差**（B.9）且**失败帧做常速外推**（使 ADE 15.18→16.84） | T2：`comments` 标注 "ICLR 2026 Poster"；**第二十五轮升全文，见 §4.5**；代码见 [C004 §J](../../code/traces/world_model_code_traces.md) |
| WM-21 | [DriveDreamer](https://arxiv.org/abs/2309.09777) | 2023 | ECCV'24 / CCF-B | — | 未来图像/视频（16 帧）+ 未来动作 | **特征级条件**：池化 Auto-DM 多尺度 UNet 特征 + 历史动作 → MLP 出未来动作 | T1：ECCV'24；**代码核验：仓库只有生成侧，无规划脚本**（见 §4.1） |
| WM-22 | [RenderWorld](https://arxiv.org/abs/2409.11356) | 2024 | ICRA'25（白名单） | — | 3D 语义占据 + 自车位移 | **token 级联合自回归**（OccWorld 式 masked temporal attention）+ 自车位移解码 | T1：`comments` 原文 "Accepted in 2025 IEEE International Conference on Robotics and Automation"；**无官方代码** |
| WM-23 | [Imagine-2-Drive](https://arxiv.org/abs/2411.10171) | 2024 | IROS'25（**投稿状态**） | — | 未来前视 RGB（H=9 帧） | **世界模型当"想象环境"**：DPA 轨迹 → 预测未来观测 + 奖励 → 回灌 PPO | T2：`comments` 原文 "**Submitted to** IROS 2025"；**代码未发布**（README "Code coming soon!"） |
| WM-24 | [WoTE](https://arxiv.org/abs/2504.01941) | 2025 | ICCV'25 / CCF-A | — | 未来 BEV（8×8） | **选优器**：256 条 K-means 锚 + 学到的奖励模型打分 → `argmax` 选优；**规划器本身非扩散** | T1：ICCV'25；**已代码核验**（§4.1 + [C004 §E](../../code/traces/world_model_code_traces.md)）：256 锚 / `argmax` 选优 / 8 poses@2 Hz 全部成立 |

**分类归属**：WM-01/02 属视觉空间；03–05 属 4D/占据空间；06–09 属潜空间；10/11 属矢量化空间；12/13 属统一生成+规划；14–16 属闭环 RL；17–19 属"作为条件"；20 是评价基准。分界标志见 [lineage.md](lineage.md)。  
**第二十四轮新增 4 条按同一口径归类**：**WM-21 DriveDreamer → 视觉空间**；**WM-22 RenderWorld → 4D/占据空间**；**WM-23 Imagine-2-Drive → 闭环 RL 的新子类"世界模型当想象环境"**；**WM-24 WoTE → 新类别"选优器"**（与 WM-01 并列，但 WM-01 是命令级选优、WM-24 是轨迹级选优）。

## 1.1 逐行证据等级与代码状态（2026-09-30 补，供跨表检索）

> 证据等级定义见 [rules.md](../../../../ai/rules.md) §证据等级；代码状态取自本表各行「质量依据」列 + [repositories.md §D](../../code/repositories.md) + [C004](../../code/traces/world_model_code_traces.md)，**未新查**。

| 编号 | 证据等级 | 代码状态 |
|---|---|---|
| WM-01 Drive-WM | 全文 + 代码 L1 | 有代码但**范围不符**（仅图像生成侧，无 tree planner） |
| WM-02 DriveWorld | 全文 | 无官方代码 |
| WM-03 OccWorld | 全文 + 代码 L1 | **有代码**（世界模型 + 规划器齐全） |
| WM-04 Drive-OccWorld | 全文 + 代码 L3 | **有代码** |
| WM-05 Implicit Residual WM | 全文 | 有仓库（同仓 `ir-wm` 分支），**未核验** |
| WM-06 Latent World Model | 全文 + 代码 L3 | **有代码** |
| WM-07 World4Drive | 全文 + 代码 L3 | **有代码** |
| WM-08 DLWM | 全文 | 无官方代码 |
| WM-09 DriveFuture | 全文 | 无代码（= DP-A31） |
| WM-10 TrafficBots | 全文 + 代码 L1 | **有代码** |
| WM-11 DriveLaW | 全文 + 代码 L3 | **有代码** |
| WM-12 DrivingGPT | 全文 | 仓库**不存在** |
| WM-13 UniDrive-WM | 全文 | 只有项目页（无代码） |
| WM-14 Think2Drive | 全文 | 无官方代码 |
| WM-15 AdaWM | 全文 + 代码 L1 | **有代码** |
| WM-16 Raw2Drive | 全文 + 代码 L1 | 仓库**只有 README** |
| WM-17 Policy World Model | 全文 + 代码 L1 | **有代码**（世界模型 + 规划头齐全） |
| WM-18 WorldRFT | 全文 + 代码 L1 | 仓库**为空** |
| WM-19 FutureX | 全文 | 无官方代码 |
| WM-20 DrivingGen | 全文 + 代码 L3 | **有代码** |
| WM-21 DriveDreamer | 全文 | 代码**范围不符**（只有生成侧） |
| WM-22 RenderWorld | 全文 | 无官方代码 |
| WM-23 Imagine-2-Drive | 全文 | 代码未发布 |
| WM-24 WoTE | 全文 + 代码 L3 | **有代码**（256 锚 + argmax 选优） |

## 2. 证据边界

- **全部 24 篇已读全文**（§4）——本表**不再有摘要级条目**。
- 引用数为 OpenAlex **2026-09-23 快照**；`—` 表示未取到，**不是 0**。2025–2026 年工作引用接近 0 属正常（见 [literature-quality.md](../../../../shared/literature-quality.md) §1）。
- **venue 来源分三类**：① arXiv `comments` 字段（最可靠，如 WM-22/23）② 综述表格（[2512.16760](https://arxiv.org/abs/2512.16760) §3.2）③ 论文/仓库 README 自述（WM-24 的 ICCV'25）。已在"质量依据"列逐条注明。
- WM-09 DriveFuture 是唯一与研究对象**直接同构**的条目，已在研究对象侧有全文笔记（DP-A31），本表只作指针。
- **同一个方法的数字可能有三个口径**（WM-24 WoTE 实证）：**README 88.3**（NC 98.5 / DAC 96.8 / EP 81.9 / TTC 94.9 / Comfort 99.9，8×L20 训 3 h）vs **论文 Table 1（navtest）87.1** vs **论文 Table 3/6 消融表 85.6**。→ **引用时须写明取自哪一张表**，这与 [benchmarks.md §2](../../direction/benchmarks.md) 的"跨论文不可横比"是同一问题的表内版本。

## 3. 补录结果：arXiv ID 与 venue 的核验

**2026-09-23 首次尝试时 arXiv 与 OpenAlex 双渠道同时限流**（OpenAlex 当日额度耗尽、arXiv 返回 429）。**第二十一轮复检解决 5 项 arXiv ID，第二十四轮已全部收进 §1 表**（原为独立待补清单）：

| 名称 | arXiv ID | 独立核验到的 venue | 现已收进 |
|---|---|---|---|
| DriveDreamer | **2309.09777**（2023-09-18）✓ | **未获确认**：arXiv `comments` 只给项目页；OpenAlex 按 DOI 与按标题都只返回 arXiv 存根（15 引用），无 ECCV 正式版记录 | **WM-21** |
| GenAD | **2402.11502**（2024-02-18）✓ | 未获确认（`comments` 只给代码链接） | **不单列**：见下方同名陷阱 |
| Imagine-2-Drive | **2411.10171**（2024-11-15）✓ | **需收窄**：`comments` 原文 "**Submitted to** IROS 2025" → 是**投稿状态，不是录用** | **WM-23** |
| RenderWorld | **2409.11356**（2024-09-17）✓ | **comments 明确**："Accepted in 2025 IEEE International Conference on Robotics and Automation" → **ICRA 2025 录用** | **WM-22** |
| WoTE | **2504.01941**（2025-04-02）✓ | **未获确认**：无 `comments`；OpenAlex 按标题查到一条 2025 年 `conference-paper`（15 引用）但**来源名为空**；仓库 README 自述 ICCV'25 | **WM-24** |

> **同名陷阱（须记住）**：`2402.11502` 是本项目**已代码核验过**的那篇 GenAD（[C005 §J](../../code/traces/e2e_trunk_code_traces.md)：32 维对角高斯隐变量 + spatial GRU + 解析 KL 的 CVAE 式生成器，属 E2E 主干侧）；而 [2403.09630](https://arxiv.org/abs/2403.09630) "GenAD: Generalized Predictive Model for Autonomous Driving" 是 **OpenDriveLab 的数据集论文**（CVPR'24 Highlight），**两者不是同一篇**。→ 世界模型侧**不新增 GenAD 条目**，只作指向 E2E 主干侧的指针。

**已全部解决（2/2，2026-09-23）**——两条**都不是抄错，而是"没有 arXiv 版本"**：

| 名称 | 真实全称 / 出处 | 结论 |
|---|---|---|
| **NeMo** | **Neural Volumetric World Models for Autonomous Driving**（Zanming Huang、Jimuyang Zhang、Eshed Ohn-Bar，Boston University） | **只有会议版**：**ECCV 2024**（LNCS vol. 15075 Part XVII, pp. 195–213；dblp `conf/eccv/HuangZO24`），OpenReview `forum?id=mWazUXaT6d`。**arXiv 确认无版本**（`ti:"Neural Volumetric World Models"` 与 `all:"Neural Volumetric World Models"` 均 **0 命中**）→ **引用时用 ECCV'24 会议版**。撞名的 NVIDIA **NeMo** 工具链与此无关 |
| **OccVAR** | **OccVAR: Scalable 4D Occupancy Prediction via Next-Scale Prediction**（Bu Jin、Xiaotao Hu、Songen Gu、Yupeng Zheng 等） | **是未中稿并已撤稿的 ICLR 2025 投稿**（OpenReview `forum?id=X2HnTFsFm8`，2024-11-15 作者主动撤稿），**从未上传 arXiv**。→ **同作者组的后继工作已改名 [OccTENS](https://arxiv.org/abs/2509.03887)（arXiv `2509.03887`，"OccTENS: 3D Occupancy World Model via Temporal Next-Scale Prediction"）** → **引用时直接用 OccTENS**（已实测确认该 arXiv 页标题与 `citation_title` 均为 OccTENS） |

> **核验方式**（可复用）：arXiv API 走 **HTTPS**（`https://export.arxiv.org/api/query`；HTTP 会 301、`urllib` 默认 UA 会 406，**必须用 `curl`**），按 `ti:"<标题>"` 检索并读 `<arxiv:comment>` 字段；venue 再用 OpenAlex 按 DOI **与按标题**各查一次（按 DOI 只会拿到 arXiv 存根，**必须按标题查正式版**）。**当按标题在 arXiv 找不到时，先怀疑"根本没有 arXiv 版本"（会议版 / 撤稿投稿），再去 OpenReview 与出版社目录页反查——不要只反复换关键词搜 arXiv。**

**已解决一项（2026-09-23）**：原列在此处的 **LAW** 已确认为 arXiv [2406.08481](https://arxiv.org/abs/2406.08481)（论文内自称 LAW），即本表 **WM-06**，已移出待补。

## 4. 已读全文（已拆出）

**§4 的逐篇详细结论已拆到 [verification.md](verification.md)**（原文 73 KB、超 Read 工具 64 KB 上限，无法整读）。索引：

| 节 | 内容 |
|---|---|
| §4.0 | 第一轮 5 篇（WM-01/03/06/17/18） |
| §4.1 | 第二十四轮 5 篇（WM-19/21/22/23/24） |
| §4.2 | 第二十五轮 WM-15 AdaWM、WM-16 Raw2Drive |
| §4.3 | 第二十五轮 WM-02 DriveWorld、WM-10 TrafficBots、WM-11 DriveLaW |
| §4.4 | 第二十五轮 WM-04/05/07/12/14 |
| §4.5 | 第二十五轮 WM-08/13/20——**24 篇至此全部读过全文** |
