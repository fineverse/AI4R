# DP-E11 · Consistency Policy（一致性蒸馏加速）

- **原题**：Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation
- **作者/载体**：Aaditya Prasad 等；arXiv [2405.07503](https://arxiv.org/abs/2405.07503) v2（2024-05）；**正文未标注会议**
- **代码**：见项目页（未核验）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 机制 | 从 EDM teacher 蒸馏出自一致性 student（CTM）：单步 z~N(0,I) 直接出 x，或 3 步 chaining；初始方差 N(0,1/T²)；**无引导/约束**（纯模仿） | §3 |
| 动作空间 | action chunk=16（每步 10D：EE pos 3 + rot 6 + gripper 1；移动任务 13D） | 附录 C |
| 频率 | 真机 Franka 策略 **15 Hz**（底层 1 kHz） | 附录 C |
| 性能 | ToolHang 单步 0.70 / 3 步 0.77（DDPM 0.79、DDiM 0.14，Table I） | Table I |
| **延迟（关键）** | DDPM(100 NFE) **110 ms**、DDiM(15) **11 ms**、CP(1) **1 ms**、CP(3) **2 ms**（Table III）；真机 DDiM 192 ms vs CP **21 ms**（Table XI） | Table III/XI |
| 关键设计 | 一致性目标（CTM-local 最佳 0.92）、降低初始方差（1→1/T² 使 0.9→0.92）、预设 chaining 步、dropout | Table V–IX |
| 自述局限 | 损失多模态、训练较不稳、移动任务精度略低、训练更耗时 | §V |

## 对本项目的意义（AI 判断）

- 把多步去噪蒸馏为 1–3 步**直接满足驾驶实时性**：1 ms 级延迟远超驾驶 10 Hz 需求（100 ms 预算）。
- **但要注意**：驾驶侧已经用更简单的手段达到了实时（DiffusionDrive 2 步截断扩散 45 FPS、MeanFuser 一步 59 FPS），所以**一致性蒸馏在驾驶上的边际收益主要是"从 2 步降到 1 步"，而不是数量级提升**。它真正可能有价值的地方是：在**引入约束/引导导致步数增加**时，用它把代价压回去——这个组合本轮检索未见有人做。
- **明显不成立**：chunk=16 @15 Hz ≈ 1 秒视野，对驾驶过短；无约束机制。

## 待核验

- 官方代码与会议信息。
- 一致性蒸馏与"带约束的少步采样"是否兼容（蒸馏目标会绕过约束投影）。
