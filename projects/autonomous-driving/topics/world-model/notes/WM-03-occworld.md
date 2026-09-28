# WM-03 · OccWorld（3D 占据世界模型，ECCV 2024，62 引用）

- **原题**：OccWorld: Learning a 3D Occupancy World Model for Autonomous Driving
- **作者/载体**：Wenzhao Zheng 等；arXiv [2311.16038](https://arxiv.org/abs/2311.16038)；**ECCV 2024**（OpenAlex 记为 LNCS）
- **代码**：**有** — [github.com/wzzheng/OccWorld](https://github.com/wzzheng/OccWorld)（`comments` 标注）
- **证据等级**：全文（PDF + `pdftotext -layout`，读摘要与 Table 2）
- **笔记日期**：2026-09-23

## 摘要原文（节选）

> …we explore a new framework of learning a world model, OccWorld, in the 3D Occupancy space to simultaneously predict the movement of the ego car and the evolution of the surrounding scenes. We propose to learn a world model based on 3D occupancy rather than 3D bounding boxes and segmentation maps for three reasons: 1) **expressiveness**… 2) **efficiency**（3D occupancy 可从稀疏 LiDAR 点更经济地获得）3) **versatility**（同时适配视觉与 LiDAR）。

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 核心 | 在**3D 占据空间**学世界模型，同时预测**自车运动**与**场景演化** | 摘要 |
| 为什么用占据而非 3D 框 | ① 表达力更强（更细的 3D 结构）② 获取更经济 ③ 同时适配视觉与 LiDAR | 摘要 |
| 预测方式 | 训练时屏蔽所有时序注意力中的未来信息；推理时用 **2 秒历史**自回归预测**未来 3 秒** | §实验设置 |
| **规划结果（Table 2）** | **OccWorld-O†（3D-Occ 输入，无辅助监督）：L2 平均 0.64 m、碰撞率平均 0.24%、18.0 FPS** | Table 2 |
| 同表对比 | VAD-Base† 0.72 m / 0.22% / 4.5 FPS；UniAD 1.03 m / 0.31% / 1.8 FPS；VAD-Tiny† 0.78 m / 0.38% / 16.8 FPS | Table 2 |
| 无 † 版本 | OccWorld-O：1.17 m / 0.60% / 18.0 FPS（说明 † 的度量口径差异显著） | Table 2 |
| 场景 tokenizer | **codebook 512 最优**，更大（如 1024）导致过拟合 | Table 3 |

## 局限（本笔记指出）

- **输入权限是特权级**：Table 2 的 OccWorld-O† 用 **3D-Occ 作为输入**，不是原始传感器；与相机方法不构成同条件对比。
- 视觉版（OccWorld-D/T/S）明显弱于 OccWorld-O：OccWorld-D L2 0.77 / 碰撞 0.32；OccWorld-S（无辅助监督）1.83 / 2.02。

## 对本项目的意义

- **"3D 占据"这条路线的最早系统化工作**，对应 [lineage.md](../lineage.md) 阶段 2（4D/占据空间）。它给出了这条路线最初的取舍理由（表达力/经济性/通用性），是理解后续 Drive-OccWorld、Implicit Residual WM 的起点。
- **18 FPS 且规划指标优于 UniAD（1.8 FPS）**：占据世界模型在 2023 年就已经比端到端基线快 10×，说明"世界模型必然慢"不成立——**慢的是解码回像素，不是潜/占据预测**。
- **codebook 512 最优、更大过拟合**：与研究对象侧的"锚点词表大小 vs 性能"权衡（DP-A02/A14）是同一类问题，可对照。
- 与 [transfer.md](../../diffusion-planner/transfer.md) 第 3 节相邻；本次读全文后其条目**可从"摘要级"升级为"全文级"**。

## 待核验

- 代码**已克隆并做静态核验**：规划是 **3 模式 L2 回归**（`PlanRegLossLidar(num_modes=3)`，非生成式）；自回归时预测 token **回灌**、无 teacher forcing 泄漏；**未来驾驶模式来自 GT**（`decode_pose(..., gt_mode[:, i:i+1], ...)`、评测时 `pred_ego_fut_trajs[gt_mode.bool()]`）。详见 [world_model_code_traces.md](../../../code/traces/world_model_code_traces.md)。
- † 标记的度量口径差异（同模型 L2 1.17 → 0.64）原因未在本次阅读范围内确认。
