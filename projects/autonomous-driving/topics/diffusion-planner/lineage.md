# 扩散规划器发展脉络（2022 → 2026）

更新时间：2026-09-22  
读法：本文件只写**已核验的事实**与**明确标注的判断**；论文编号见 [papers/diffusion_planner_ad.md](papers/diffusion_planner_ad.md)（DP-Axx）、[papers/diffusion_planner_embodied.md](../../../embodied-ai/topics/diffusion-policy/papers/diffusion_planner_embodied.md)（DP-Exx）；笔记在 [notes/](notes)。  
代码层面的继承关系来自**已下载仓库的 README**（见 [code/repositories.md](../../code/repositories.md)），不是推测。

## 一句话总结

扩散规划器经历了**三次转移**：从"通用决策里证明可行"（2022）→ "机器人策略工程化"（2023）→ "驾驶场景实时化"（2024 末）→ "路线分化 + 条件升级"（2025–2026）。到 2026 年，**生成机制本身已不再是瓶颈**（1–2 步即可实时），瓶颈转移到**约束、选优与评价**。

## 阶段划分

| 阶段 | 时间 | 标志 | 代表 | 解决了什么 | 留下什么 |
|---|---|---|---|---|---|
| 0 范式确立 | 2022 | 把"采样"直接当"规划" | DP-E01 Diffuser（ICML'22）、DP-E02 Decision Diffuser（ICLR'23） | 证明扩散可替代轨迹优化；引导/inpainting 可解释为规划算子 | 慢（Diffuser 1.5 Hz）、无动力学约束、离线 RL 域 |
| 1 策略工程化 | 2023–2024 | 扩散策略成为机器人 IL 的强基线 | DP-E09 Diffusion Policy（RSS'23，IJRR）、DP-E03 Diffusion-QL、DP-E28 EDP、DP-E11 Consistency Policy、DP-E10 DP3、DP-E04 DiffuserLite | action chunk / receding horizon（Ta=8 最优）、少步化（1–3 ms）、3D 表示、粗到细（122 Hz） | 仍是开环任务、无他车交互 |
| 2 进入驾驶并实时化 | 2024-11 | 首次把扩散规划器做到实时并给出强基准 | DP-A02 DiffusionDrive（CVPR'25 Highlight，2 步 / 45 FPS / NAVSIM 88.1） | 用**锚点先验 + 截断日程**把去噪压到 2 步 | 锚点词表大小 vs 性能的固有权衡；IL 无约束 → 模式保守 |
| 3 路线分化 | 2025 | 同一条问题上出现四种解法 | 流匹配：DP-A09 GoalFlow（CVPR'25）；纯扩散+引导：DP-A01 Diffusion Planner（ICLR'25 Oral）；RL 约束：DP-A16 DIVER、DP-A03 DiffusionDriveV2；理论修正：DP-A08 BridgeDrive（ICLR'26） | 各自解决一个子问题：目标发散、规则后处理、模式坍缩、日程不一致 | 四条路线**没有在同一基准上互相比过**；多样性-质量两难浮现 |
| 4 一步生成 + 条件升级 + 约束 | 2026 | 生成机制趋同，竞争转向条件与约束 | DP-A14 MeanFuser（CVPR'26，一步/59 FPS）、DP-A13 WAM-Flow、DP-A31 DriveFuture（navhard 55.5）、DP-A21 PC-Diffuser（CBF 证书）、DP-A18 FeaXDrive、DP-A22 G2SD | 一步采样、世界模型条件、认证级硬约束、可行性建模 | 实时与硬约束仍不可兼得；评价协议未收敛 |

## 三次关键转移（按"变化的是什么"读）

### 转移 1：起点先验（纯高斯 → 锚点 → 连续混合 → 离散 token）
- 纯高斯：DP-A01（nuPlan）、DP-A16、DP-A09（σ<0.1 才稳定，Table 4）。
- 锚点/词表：DP-A02 家族（K-means 锚点）、DP-A04 AnchDrive（静动混合锚点）、DP-A05 DriveAnchor（2,398 条形状词表）。
- 连续混合：DP-A14 MeanFuser 用高斯混合噪声（GMN，K=8）**替代**离散词表，直接针对"词表大小 vs 性能"的权衡。
- 离散 token：DP-A13 WAM-Flow 把轨迹离散成 token 空间，做并行非因果流匹配。
- **判断**：这条线的收敛点是"**先验质量**比"离散还是连续"更重要"——MeanFuser 超过锚点方案，AnchDrive 的消融也显示 1→5 步几乎不影响（85.43→85.46）。
- **代码级补充（2026-09-23）**：锚点/词表这条线**不是扩散引入的**。代码核验显示其源头是 **VADv2**（ICLR'26，4096 条 CARLA 轨迹词表 + **纯分类，回归分支被乘 0 丢弃**），Hydra-MDP 沿用（代码未公开），DiffusionDrive 才把词表改成**扩散起点**，而 DiffusionDriveV2 又把 **16384 条词表轨迹与扩散输出拼进同一候选池**由 scorer 选优——**即回到了"词表 + 选优"**。完整五环谱系见 [e2e_trunk_code_traces.md](../../code/traces/e2e_trunk_code_traces.md) §C。

### 转移 2：约束位置（事后 → 软奖励 → 软引导 → 去噪内硬约束 → 结构层）
见 [preparation.md 第 2b 节](../../ideas/preparation.md)：四种立场都已有代表，其中"生成之后的否决层"只有综述主张（DP-S11 §8.9）、**没有实现**。

### 转移 3：条件来源（场景 → 目标点 → 语言 → 未来潜状态）
- 场景 BEV/矢量化：DP-A01、DP-A02。
- 目标点：DP-A09 GoalFlow（消融 +4.7 PDMS，Table 2）。
- 语言/推理：DP-A27 DiffVLA、DP-A28 ReCogDrive、DP-A30 KnowDiffuser。
- 未来潜状态：DP-A31 DriveFuture（navhard 受控收益 **+3.7**：30.9→34.6，不含 scorer；**注意"24.2→55.5"是同表两行不同方法 + 含 scorer，不是条件化收益**）。
- **判断（第二十四轮更正）**：**"改条件"与"改生成机制"的受控收益都在 +3 ~ +5 量级**（条件侧：GoalFlow goal 条件 +4.7、DriveFuture 未来潜状态 +3.7；生成侧：**SpanVLA 回归头→flow matching +5.2**、DiffusionDriveV2 的 RL +3.1）→ **没有哪一方"远大于"另一方**；navhard 上的高分离不开**选优器**（DriveFuture 55.5 / WoTE 88.3 都靠 scorer）。详见 [preparation.md 第 2 节](../../ideas/preparation.md)。

## 继承关系（代码层面已核验）

强度分级 S1–S4 的定义见 [workflows.md §代码脉络梳理](../../../../ai/workflows.md)。

| 工作 | 基于 / 引用了哪些代码库 | 强度 | 证据 |
|---|---|---|---|
| DP-A03 DiffusionDriveV2 | 同团队 DiffusionDrive（冷启动自其 IL 权重） | S2 | 论文 §5.2 + 仓库 README 引用 DiffusionDrive |
| DP-A01 Diffusion Planner | **nuplan-devkit**（6 处）+ 与 **PLUTO** 同源比较（3 处） | S3 | 仓库 README |
| DP-A10 FlowDrive | **nuplan-devkit** + **PLUTO**（与 DP-A01 同一 nuPlan/PLUTO 血统） | S3 | 仓库 README |
| DP-A21 PC-Diffuser | **以 Diffusion Planner 为基座**（仓库内含 `diffusion-planner-cbf` + vendored `nuplan-devkit`） | **S1** | 论文 §V + 仓库目录结构 |
| DP-A16 DIVER | **SparseDrive** 代码库（5 处）+ 复用 **Hydra-MDP** 的 PDMS 奖励 | **S1** | 仓库 README + 论文 §IV-C2 |
| DP-A09 GoalFlow | **TransFuser** 式感知（2 处）+ **Hydra-MDP**、**UniAD** 对比 | S3 | 仓库 README |
| DP-A13 WAM-Flow | **WAM-Diff**、**Janus**、**ReCogDrive**、**FUDOKI**、flow_matching | S2 | 仓库 README 致谢 |
| DP-A29 DriveFine | **ReCogDrive** + **LaViDa**（README 明写 "developed based of"）；**但仓库零代码**，组合关系无法核验 | S2 | 仓库 README + [C003 §K](../../code/traces/diffusion_planner_code_traces-2.md) |
| DP-A06 HDP | 与 DP-A01 同团队（ZhengYinan-AIR），实现为 Hyper-Diffusion-Planner，**同仓提供 `HDP-navsim` 与 `HDP-nuplan` 两套实现**；**nuPlan 侧基于 Diffusion Planner 但退化为 ego-only、删掉引导模块**（[C003 §J.6](../../code/traces/diffusion_planner_code_traces-2.md)） | **S1** | 仓库目录结构 + 代码逐行对照 |
| DP-E10 DP3 | **Diffusion Policy** + DexMV/VRL3/DAPG 等（README 明写 "built upon"） | S2 | 仓库 README |
| DP-E01 Diffuser | denoising-diffusion-pytorch + trajectory-transformer | S2 | 仓库 README |

**扩散侧的轨线两端**：本表 ⑤ 环 DiffusionDriveV2 的上游 ④ DiffusionDrive 及更前的 VAD/VADv2/Hydra-MDP 属 E2E 主干，见 [direction/lineage.md §继承关系](../../direction/lineage.md)；「五环谱系」完整代码证据见 [C005 §C](../../code/traces/e2e_trunk_code_traces.md)。

**一条重要的结构观察（2026-09-22 更正）**：驾驶侧的扩散规划器几乎全部长在两个既有代码生态上——NAVSIM 生态（DiffusionDrive 家族、GoalFlow、MeanFuser、WAM-Flow、DIVER 的评测）与 nuPlan/PLUTO 生态（Diffusion Planner、FlowDrive、PC-Diffuser）。

我此前判断"跨生态迁移无人做过"是**错的**：**HDP（DP-A06）的官方仓库同时提供 `HDP-navsim` 与 `HDP-nuplan` 两套实现**（见 [code/repositories.md](../../code/repositories.md)），说明**代码层面的跨生态已经打通**。**限定（2026-09-23 代码核验）**：两套实现**不是同一个模型的移植**——nuPlan 侧基于 Diffusion Planner 但已退化为 ego-only、删掉 `guidance/` 模块，NAVSIM 侧则是 Florence-2 + DiT 的 VLA 结构（[C003 §J.6](../../code/traces/diffusion_planner_code_traces-2.md)）。仍然成立的是更窄的一条：**没有工作在同一基准上对比"两个生态里的方法"**（例如把 nuPlan 系的 Diffusion Planner 放到 NAVSIM navhard 上，或反过来）——这仍是一个评价层面的空白。

## 评价协议的演进

| 时期 | 主评价 | 代表数字 |
|---|---|---|
| 2025 初 | nuPlan 闭环（NR/R 分数） | DP-A01：Val14 无 refine 89.87 → 加 refine 94.26 |
| 2025 中 | NAVSIM v1 navtest（PDMS） | DP-A02 88.1、DP-A09 90.3、DP-A03 91.2 |
| 2025 末 | NAVSIM v2 navtest（EPDMS） | DP-A03 85.5、DP-A14 89.5、DP-A31 89.9 |
| 2026 | NAVSIM v2 **navhard** + 违规率 | DP-A31 55.5、DP-A16 43.4、DP-A12 43.0、DP-A02 24.2；DP-A18 报曲率违规率 |

**判断**：协议演进的方向是"从单一分数到困难子集 + 多维度违规率"。这与 S032 §VII.C（跨协议排名反转、子指标饱和、NAVSIM 只是代理证据）一致。

## 当前格局（2026-09 时点）

- **实时最优**：DP-A14 MeanFuser（一步 / 59 FPS / PDMS 89.0）；DP-A02 DiffusionDrive（2 步 / 45 FPS / 88.1）。
- **navhard 最强**：DP-A31 DriveFuture（**55.5，含 GTRS-Dense scorer**）→ **高分的来源里"选优器"占了相当部分**（其不含 scorer 的受控消融只有 34.6）；同基准上 WoTE 的 88.3/87.1（navtest）也靠 scorer。
- **约束最严**：DP-A21 PC-Diffuser（有证书，但约 2 fps）。
- **最具工程价值**：DP-A05 DriveAnchor（2.06 ms / Orin，量产导向，但无公开基准）。
- **最值得警惕**：DP-A09 GoalFlow 的 90.3 与 85.7 之争——**同一方法在不同论文表格里差 4.6 分**，说明复现口径差异巨大。

## 未解决问题（与四篇综述的收敛结论一致）

见 [preparation.md 第 2b 节](../../ideas/preparation.md)：实时性、评价协议、安全保证三点在 S031/S032/S033/DP-S11/S15 中**跨来源一致**。扩散规划器特有的两条：

1. **跨生态不可比**（NAVSIM ↔ nuPlan）；
2. **约束与实时不可兼得**（2 fps vs 45 FPS 的鸿沟无人跨越）。

## 代表工作与代码对照（可下载）

代码快照共 **36 个仓库、约 1.6 GB**（扩散侧 + E2E 主干 + 具身侧 + 世界模型侧），完整清单与 commit 见 [code/repositories.md](../../code/repositories.md)。扩散侧的 7 个此前未获取仓库（DiffusionDriveV2、Diffusion Planner、GoalFlow、MeanFuser、Hyper-Diffusion-Planner、PC-Diffuser、FeaXDrive）**已全部补齐**（多重试 + tarball 兜底生效）。
