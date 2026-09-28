# WM-17 · Policy World Model（单目相机 40 FPS，把世界建模与规划统一）

- **原题**：From Forecasting to Planning: Policy World Model for Collaborative State-Action Prediction
- **作者/载体**：Wenyuan Fan 等（大连理工大学）；arXiv [2510.19654](https://arxiv.org/abs/2510.19654) v2（2025-11，cs.CV）；**NeurIPS 2025 Poster**（`comments` 标注）
- **代码**：**有** — [github.com/6550Zhao/Policy-World-Model](https://github.com/6550Zhao/Policy-World-Model)（论文称"Code and model weights will be released"）
- **证据等级**：全文（PDF + `pdftotext -layout`，读摘要、Table 1/2/4 与效率段）
- **笔记日期**：2026-09-23

## 摘要原文（节选）

> …the world models for world simulation and decoupled from trajectory planning… We introduce a new driving paradigm, Policy World Model (PWM), which not only integrates world modeling and planning within a unified architecture, but is also able to transfer learned world knowledge through the proposed action-free future… scheme. Through collaborative state-action prediction… Despite utilizing [single-view] input, our method matches or exceeds state-of-the-art approaches [with] multi-view and multi-modal inputs.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 核心主张 | 现有世界模型**为仿真而建、与轨迹规划解耦**；PWM 把**世界建模与规划放进同一架构**，并做"状态-动作协同预测" | 摘要 |
| 效率设计 | 图像 tokenizer（上下文引导的压缩与解码）+ **并行 token 生成** + 自适应 dynamic focal loss | §3.1、摘要 |
| **推理速度** | **约 40 FPS**（单张 A800，batch size 1，**不含像素空间解码**）；论文称相对"零未来帧"基线的额外延迟"marginal" | §4 效率段 |
| **未来帧数的最优点** | **10 帧最优**。更短则时序动态不足；更长则预测质量下降并**引入幻觉**（单前视角感知有限），反而损害决策 | §4 效率段、Table 4 |
| **NAVSIM navtest** | **PDMS 88.1，仅用单视角相机（SC）** —— 与 DiffusionDrive 88.1（相机+LiDAR）持平；TTC **95.4**、NC **98.6** 均高于 DiffusionDrive（94.7 / 98.2） | Table 2 |
| nuScenes | 平均碰撞率与 ADE 均优于 OccWorld-D、Omni-Q、RDA-Driver、DiffusionDrive 等 | Table 1 |
| **量化权衡（重要）** | 在 NAVSIM 上观察到互补权衡：**不预测未来帧 → EP 更高**（轨迹在时限内推进更远）；**预测未来帧 → NC 更高**（更安全） | §4 末段 |

## 局限（本人自述 / 本笔记指出）

- **本人自述**：单前视角输入导致感知有限，长时程预测"可能引入幻觉"。
- **本笔记指出**：40 FPS 是**不含像素空间解码**的数字；若需要可视化/仿真用途，速度会下降。

## 对本项目的意义

- **它量化了"世界模型作为条件"的收益与代价**——这正是 [lineage.md](../lineage.md) 接口差异第 3 问标记的空白（"收益来源未拆解"）。PWM 给出的答案是：**未来帧条件买到的是安全性（NC↑、碰撞率↓），代价是进度（EP↓）**。这是目前看到的最直接的一条证据。
- **40 FPS + 单目相机**说明世界模型不必吃掉实时性余量——但它走的是"统一架构"路线（世界模型即规划器），**不是**给外部扩散器供条件。
- **10 帧最优**是一个可复用的超参结论（对应研究对象侧的"条件信息量"旋钮）。
- 与 [transfer.md](../../diffusion-planner/transfer.md) 第 3 节"从预测转向规划（状态-动作联合预测）"是同一路线，本次读全文后**可从"摘要级"升级为"全文级"**。

## 待核验

- 40 FPS 的完整测量条件（是否含感知前向、是否含 tokenizer 解码）需读附录确认。
- 代码**已克隆并做静态核验**：世界建模与规划确在**同一 LLM 的一次前向**内（`navsim_forward` 同时返回未来帧 token 交叉熵与轨迹 L1），损失配比 `video_coeff: 0.3` / `tj_coeff: 1.0`；轨迹 query 排在**未来帧 token 之后**，规划头读 `hidden_states[:, -8:]`。详见 [world_model_code_traces.md](../../../code/traces/world_model_code_traces.md)。
- "action-free future scheme"的确切含义（如何在无动作标签时学到未来）未细读。
