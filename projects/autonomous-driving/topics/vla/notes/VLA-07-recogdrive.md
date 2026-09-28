# VLA-07 · ReCogDrive（认知引导扩散规划器 + DGRPO，13.3 Hz）

- **原题**：ReCogDrive: A Reinforced Cognitive Framework for End-to-End Autonomous Driving
- **作者/载体**：Yongkang Li 等；arXiv [2506.08052](https://arxiv.org/abs/2506.08052) v2（2025-06）
- **代码**：**[xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive)**（**611★**，**ICLR 2026**，最后推送 2026-09-22）；**本条 2026-09-24 第三十六轮更正**——论文正文确未给仓库，但**仓库已发布**，且**研究对象侧（DP-A28）早已做过代码级核验**（[C003 §M](../../../code/traces/diffusion_planner_code_traces-2.md)）
- **证据等级**：全文（PDF + `pdftotext -layout`，读正文与 Table 1/2）
- **笔记日期**：2026-09-23

## 摘要原文（节选）

> …we present ReCogDrive, an end-to-end autonomous driving system, which possesses rich driving priors and generates continuous, stable trajectories via a diffusion denoising process.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 三大组件 | ① 可扩展分层数据管线（**2.3M 开源驾驶数据 + 752K 自动标注 Q&A**）② **认知引导扩散规划器**（Cognition-Guided Diffusion Planner）③ **扩散组相对策略优化 DGRPO**（Diffusion Group Relative Policy Optimization） | §4.1/§4.2/§4.3 |
| 对 VLM 直出轨迹的三点批评 | (1) 预训练知识的领域鸿沟；(2) **模态错配**——离散语言空间与连续动作空间冲突，自回归解码会产生物理不可行轨迹；(3) 高推理延迟 | §2 相关工作的分析 |
| **主结果** | **NAVSIM navtest PDMS 90.8**，**纯相机输入**；NC 97.9 / DAC 97.3 / TTC 94.9 / Comf 100 / **EP 87.3** | Table 1 |
| 同表对比 | DiffusionDrive 88.1（相机+LiDAR）、WoTE 88.3（相机+LiDAR）、Hydra-MDP 86.5；VLM 基线 QwenVL2.5-8B† 83.3、InternVL3-8B† 83.3 | Table 1 |
| 提升幅度 | 相对 DiffusionDrive **+2.7 PDMS**、相对 WoTE +2.5（且**仅用相机**） | §5.2 |
| **推理频率** | **13.3 Hz**（对比 InternVL3-2B f.t. **1.7 Hz**、InternVL3-8B f.t. **0.9 Hz**）——即比 VLM 直出轨迹快 **约 8–15 倍** | Figure 1 |
| CARLA Bench2Drive | DS **71.36**、Success **45.45**、Efficiency 138.18、**Comfort 17.45（很低）** | Table 2 |

## 局限（本人自述）

- 仍存在**相对较高的推理延迟**（结论段"Future work may address these issues by…"提及帧序列与高推理延迟，正文 §6 结论段）。

## 对本项目的意义

- **回答了 VLA 侧最关键的一个问题——延迟**：13.3 Hz 已经跨过 10 Hz 门槛（而 VLM 直出轨迹只有 0.9–1.7 Hz）。做法是**把语言关在"认知"层、把连续轨迹交给扩散器**，与 [transfer.md](../../diffusion-planner/transfer.md) 第 2 节"双系统分离"是同一思路的实证。
- **EP 87.3 vs DiffusionDrive 82.2（+5.1）**：提升主要落在 EP（ego progress）上，说明 DGRPO 的 RL 后训练主要改善"敢走"而非"更安全"——这与 [preparation.md](../../../ideas/preparation.md) P2c（分数与可行性不一致）同向。
- **Comfort 17.45 极低**：在 Bench2Drive 上舒适性很差，说明"高频 + 高质量"与"舒适"之间仍有冲突。
- 它同时给出**纯相机**结果却超过相机+LiDAR 的基线，说明**输入权限的差异比模态数量更重要**（呼应 [direction/benchmarks.md](../../../direction/benchmarks.md) 的比较口径）。

## 待核验

- DGRPO 的具体形式（组相对优势如何作用在扩散反链上）未细读，与 DiffusionDriveV2 的锚内/锚间 GRPO 是否同源**待比较**。
- 13.3 Hz 的测量硬件未在本次阅读范围内确认。
- **⚠ 本条已于第三十六轮作废**（原写"无代码，无法核验 PDMS 90.8"）——仓库 [xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive) **已发布且有 611★**；但**本笔记未对 navtest 90.8 这一数字做复现核验**，研究对象侧的代码级核验只回答了"DGRPO 是什么"（[C003 §M](../../../code/traces/diffusion_planner_code_traces-2.md)）。
