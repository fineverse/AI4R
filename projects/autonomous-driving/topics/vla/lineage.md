# VLA（驾驶侧）发展脉络（2023 → 2026）

更新时间：2026-09-23  
读法：本文件只写**已核验的事实**与**明确标注的判断**；论文编号见 [papers.md](papers.md)（VLA-xx）。  
证据等级：本脉络基于 **4 篇综述的全文**（[2506.24044](https://arxiv.org/abs/2506.24044)、[2512.16760](https://arxiv.org/abs/2512.16760)）+ 18 篇代表工作的**摘要与元数据**，**无代码核验、无运行**。

## 一句话总结

VLA 在驾驶侧经历了**四次闭环收紧**：语言从"解释器"（不碰控制）→ "模块化规划的中间表示" → "端到端管线的直接输出" → "带推理与记忆的控制中枢"。到 2026 年，**语言已经能进控制回路，代价是推理频率**——这也是它与扩散规划器最直接的冲突点。

## 阶段划分

| 阶段 | 时间 | 分界标志 | 代表 | 解决了什么 | 留下什么 |
|---|---|---|---|---|---|
| 1 VLM as Explainer | 2023 | 语言输出**不接控制**，车辆仍由 PID 等传统模块驱动 | VLA-01 DriveGPT4、VLA-02 ADriver-I | 提升可解释性 | 语言只是"覆盖层"；逐帧长描述带来延迟；通用视觉编码器在无关细节上浪费算力 |
| 2 Modular VLA | 2024–2025 | 语言变成**中间表示**（waypoint / 元动作），再接动作头 | VLA-03 OpenDriveVLA、VLA-04 DriveMoE、VLA-05 SafeAuto、VLA-06~08 DiffVLA/ReCogDrive/KnowDiffuser | 语言真正进入规划环节 | 仍是多阶段管线（感知→语言→规划→控制），**引入延迟与级联失效风险** |
| 3 End-to-end VLA | 2024–2025 | 单一多模态网络**直接输出**轨迹或控制 | VLA-09 EMMA、VLA-10 CoVLA、VLA-11 AutoVLA、VLA-13 DriveVLM、VLA-14 DriveLM | 消除模块边界；反应快 | 长时程推理弱；难以给出细粒度解释 |
| 4 Reasoning-Augmented | 2025–2026 | VLM/LLM 进入**控制回路中心**，加记忆与工具使用 | VLA-15 ORION、VLA-16 MindDrive、VLA-17 Drive My Way、VLA-18 ExploreVLA | 长时程推理、自我反思、偏好对齐 | **索引城市级记忆、把 LLM 推理压进 30 Hz 控制回路、形式化验证** 三个新问题 |

**分期来源**：阶段 1–4 直接采用 VLA4AD 综述（2506.24044 §4 + Figure 3）的划分，其分界标志是"语言与控制的耦合程度"，不是年份。另一篇综述（2512.16760）改用"VLM 主干形态"分期（single-system / dual-system），**两套分期方式不同**，见下节。

## 关键转移

### 转移 1：语言从"覆盖层"变成"规划输入"（阶段 1 → 2）
- **之前**：语言只描述场景或给出高层机动标签（"slow down"），控制由传统模块做。
- **之后**：语言输出中间表示（waypoint 序列、元动作），再转成轨迹。
- **判断**：这是**收益最明确的一次**——语言终于能改变车的动作。代价是**重新引入模块边界**，延迟和级联失效回来了。

### 转移 2：模块边界被消除（阶段 2 → 3）
- **之前**：感知→语言→规划→控制四段，逐段传递。
- **之后**：单次前向直接出轨迹或控制量。
- **判断**：解决了延迟与级联失效，但**长时程推理能力下降**——综述明确指出端到端 VLA"仍难以做远期规划与复杂应急"。

### 转移 3：推理回到回路中心，用"双系统"换频率（阶段 3 → 4）
- **之前**：端到端反应快但不会"想"。
- **之后**：VLM/LLM 做高层推理（慢系统），低层网络做实时轨迹生成（快系统），**分离两者以同时拿到推理与实时性**（2512.16760 §2.2.2 / §1005）。
- **判断**：这是本领域对"推理 vs 频率"矛盾的**主流答案**，也是对研究对象最可借鉴的一条设计——见下节。

## 与研究对象（扩散规划器）的接口差异

| # | 问题 | 结论 | 依据 |
|---|---|---|---|
| 1 | **接口形态**：轨迹、动作 token 还是语言？ | 三种**都有**，且按阶段递进：阶段 1–2 多为语言/waypoint 中间层，阶段 3 起直接出轨迹，VLA-11 AutoVLA 走**离散 drive token** | [papers.md](papers.md) 输出形态列 |
| 2 | **延迟代价** | 综述把"把 LLM 推理压进 **30 Hz** 控制回路"列为**未解挑战**（2506.24044 §8：`sub-30 Hz reasoning throughput`；§587 称在车规硬件上做到 ≥30 Hz "non-[trivial]"）。已核验的极端反例：DriveLM **0.16 FPS**（见 [E2E-11](../../direction/notes/E2E-11-drivelm.md)），比实时方案（扩散规划器 45–59 FPS）低两个数量级 | 综述全文 + 领域笔记 |
| 3 | **语言条件是否被淹没** | **是**。回归训练下语言条件被视觉先验边缘化（"条件策略坍缩"，LCS DP-A26 摘要级）；DiffVLA / ReCogDrive 从工程侧绕开（把语言当作引导信号而非直接回归目标） | 研究对象表 DP-A26/A27/A28 |
| 4 | **可迁移机制** | ① **双系统分离**（慢推理 + 快生成）→ 可映射为"LLM 出目标/约束、扩散器出轨迹"；② **语言作为引导而非回归目标**（ReCogDrive 的 action-mask 机制，避免高实时开销）；③ **语言中间表示**（waypoint/元动作）→ 可直接当锚点先验（KnowDiffuser DP-A30 已这么做） | 见 [transfer.md 第 2 节](../diffusion-planner/transfer.md) |

## 继承关系（论文 / README 级，无代码核验）

读法：本侧脉络为**摘要 + 元数据级、无代码核验**，下表只收**论文 / README 明确自述的基座与前作**；强度分级 S1–S4 的定义见 [workflows.md §代码脉络梳理](../../../../ai/workflows.md)，**因无代码核验，多数条目上限为 S2/S3**。

| 工作 | 基线 / 来源 | 强度 | 证据 |
|---|---|---|---|
| VLA-19 SimLingo | 同组前作 **CarLLaVA**（该工作的 preliminary 挑战赛技术报告） | S2 | [papers.md VLA-19](papers.md)（`comments` 原文指向） |
| VLA-17 Drive My Way | 基座 **SimLingo**（"基座 + 残差 + PID"） | S2 | [verification.md §7.3](verification.md) |
| VLA-06 DiffVLA | VLM 引导基于 **Senna-VLM**（ViT-L/14 CLIP + Vicuna-v1.5-7B） | S3 | [notes/VLA-06-diffvla.md](notes/VLA-06-diffvla.md) |
| VLA-04 DriveMoE | 底座 = **π0**（论文 §3.1 标题即 "Drive-π0 Baseline"），复用其 flow matching 动作头 | S3 | [embodied 大方向脉络 §5](../../../embodied-ai/direction/lineage.md) |
| VLA-22 VaViM/VaVAM | **VaVAM = VaViM（视频预训练主干）+ flow matching 动作专家**；论文称"完整 pipeline"，**代码冻结 VaViM** | **S1（代码级冻结）** | [papers.md VLA-22](papers.md)、[verification-2.md](verification-2.md) |
| VLA-09 EMMA | 基于 **Gemini 1.0 Nano-1** 微调（另有 PaLI-X 变体 EMMA†） | S2 | [verification-2.md](verification-2.md) |

**两条判断**：① 驾驶 VLA 的**基座**多来自通用 VLM（Gemini / Qwen2.5-VL / Senna-VLM）或**具身 VLA**（π0），**自研底座极少**；② **VLA-20 AutoMoT / VLA-23 UniDriveVLA / VLA-24 LaST-VLA 同属"小米系 MoT-VLA"**，是**同族并行**而非互为前作。

## 未解决问题

| # | 问题 | 谁明确提出 | 证据等级 |
|---|---|---|---|
| 1 | **推理频率压不进 30 Hz 控制回路** | 2506.24044 §8（`sub-30 Hz reasoning throughput`） | 综述全文 |
| 2 | **语言条件策略缺乏形式化验证** | 2506.24044 §8（`formal verification of language-conditioned policies`） | 综述全文 |
| 3 | **长尾泛化与 sim-to-real** | 2506.24044 §8 | 综述全文 |
| 4 | **城市级记忆的索引成本** | 2506.24044 §4.4（ORION 用 QT-Former 存数分钟观测） | 综述全文 |
| 5 | **架构与系统效率**、**核心能力与可信性** | 2512.16760 §6.1.1 / §6.1.3 | 综述全文 |
| 6 | **社区缺共享评测协议与开源工具链** | 2506.24044 §8 结论段 | 综述全文 |

## 证据边界

- 本脉络**只依赖综述全文 + 代表工作的摘要与元数据**，未读任何一篇 VLA 论文的完整正文（DriveVLM / DriveLM 除外，它们属领域层笔记）。
- 阶段划分**来自综述作者**，不是我自己的判断；我做的只是把两套分期方式并列呈现并指出分歧。
- 表中所有数字（引用、venue、FPS）均标注来源；`—` 表示未取到，不是 0。
- **"可迁移机制"一节是 AI 判断**，不是已成立结论；落地前必须重新验证（见 [transfer.md](../diffusion-planner/transfer.md) 的使用约定）。
