# WM-18 · WorldRFT（规划导向潜世界模型 + GRPO，nuScenes 碰撞率 −83%）

- **原题**：WorldRFT: Latent World Model Planning with Reinforcement Fine-Tuning for Autonomous Driving
- **作者/载体**：Pengxuanyang 等；arXiv [2512.19133](https://arxiv.org/abs/2512.19133) v1（2025-12）；**AAAI 2026**（`comments` 标注）
- **代码**：**无** — [github.com/pengxuanyang/WorldRFT](https://github.com/pengxuanyang/WorldRFT) **仓库为空**（仅 `LICENSE` + `readme.md`；readme 原文称 "The code will be sorted out and uploaded soon"，截至 2026-09-23 仍无代码）
- **证据等级**：全文（PDF + `pdftotext -layout`，读摘要、Table 1/2/4 与消融段）
- **笔记日期**：2026-09-23

## 摘要原文（节选）

> …the reconstruction-oriented representation learning tangles perception with planning tasks, leading to suboptimal optimization for planning… we propose WorldRFT, a planning-oriented latent world model framework that aligns scene representation learning with planning via a hierarchical planning decomposition and local-aware interactive refinement mechanism, augmented by reinforcement learning fine-tuning (RFT)… On nuScenes, it reduces collision rates by 83% (0.30% → 0.05%). On NavSim, using camera-only sensors input, it attains competitive performance with the LiDAR-based SOTA method DiffusionDrive (87.8 vs. 88.1 PDMS).

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| **对现有潜世界模型的批评** | **重建导向的表征学习把感知与规划任务纠缠在一起**，对规划而言是次优优化 | 摘要 |
| 三大组件 | ① 引入 **VGGT 视觉-几何基础模型**增强 3D 空间感知（**无需显式深度监督**）② **分层规划任务分解**引导表征优化 ③ **局部感知迭代精修**（local-aware iterative refinement） | 摘要、消融段 |
| RL 后训练 | **GRPO**（Group Relative Policy Optimization），用**轨迹高斯化** + **碰撞感知奖励**微调策略 | 摘要 |
| **nuScenes 主结果** | 碰撞率 **0.30% → 0.05%（−83%）** | 摘要 |
| **NavSIM 主结果** | **PDMS 87.8，仅相机输入**；相对 LiDAR 的 SOTA DiffusionDrive（88.1）**仅差 0.3** | 摘要、Table 2 |
| RL 的效果（nuScenes） | 无 RFT：NC 97.5 / DAC 96.0 / TTC 94.0；**有 RFT：NC 97.8 / DAC 96.8 / TTC 94.0** | Table 1 |
| VGGT 的贡献 | 加入 VGGT 使 ADE 降 7.7%（0.52→0.48）、碰撞率 0.08→0.05 | Table 4（消融） |
| 精修迭代次数 K | K=3 使碰撞率降 37.5%（0.08→0.05）；K=6 收益递减且碰撞率略回升 | Table 6（消融） |
| 规划接口 | 4 秒规划视野、**2 Hz** 轨迹点 | 正文预处理段 |

## 局限（本人自述 / 本笔记指出）

- **本人自述**：NavSIM 上仍**落后 DiffusionDrive 0.3 PDMS**（相机 vs 相机+LiDAR），未宣称超越。
- **本笔记指出**：论文的 NavSIM 详细结果放在补充材料，本次只读到 nuScenes 的完整表。

## 对本项目的意义

- **它的核心批评与研究对象直接相关**：**"重建导向的表征学习把感知与规划纠缠"**——这正是扩散规划器用世界模型做条件时会遇到的问题（世界模型为重建而训，条件未必对规划有用）。它与 DriveFuture 的动机（"未来潜状态被当作预测目标而非规划条件"）**同源**。
- **GRPO 用在潜世界模型上**：与研究对象侧的 DiffusionDriveV2 / DIVER 用 RL 后训练是同一族手段，但这里的奖励是**碰撞感知**的，且报告了**碰撞率 −83%** 这一具体数字——可作为"RL 后训练能否改善可行性"的对照证据（呼应 [preparation.md](../../../ideas/preparation.md) P2c）。
- **仓库为空，无法做代码级核验**（2026-09-23 克隆后确认，见 [world_model_code_traces.md](../../../code/traces/world_model_code_traces.md)）。
- 与 [transfer.md](../../diffusion-planner/transfer.md) 第 3 节"双潜世界模型做预训练"相邻；本次读全文后，其机制条目**可从"摘要级"升级为"全文级"**。

## 待核验

- **2 Hz 轨迹点**远低于研究对象所需的 10 Hz —— 说明它**不是实时方案**，这条必须写进 transfer.md 的"障碍"栏。
- GRPO 的具体优势函数形式（正文提到 relative advantage function）未细读。
- 代码**不存在**（仓库为空），机制**无代码可核验**。
