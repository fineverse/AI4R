# WM-06 · LAW / Latent World Model（无感知输入的潜世界模型，ICLR 2025）

- **原题**：Enhancing End-to-End Autonomous Driving with Latent World Model（论文内自称 **LAW**）
- **作者/载体**：Yingyan Li、Lue Fan、Jiawei He 等（中科院自动化所等）；arXiv [2406.08481](https://arxiv.org/abs/2406.08481)；**ICLR 2025**（首页标注 "Published as a conference paper at ICLR 2025"）
- **代码**：本次未核验
- **证据等级**：全文（PDF + `pdftotext -layout`，读 Table 1/2/3 与消融段）
- **笔记日期**：2026-09-23

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 定位 | **无感知输入**（perception-free）的潜世界模型：不做检测/分割/占据，直接用**自监督的潜预测**作为规划表征 | 摘要、§1 |
| 自监督任务 | 用当前帧特征 + 自车动作预测**未来帧的潜特征**，作为辅助自监督任务 | §方法 |
| **nuScenes 规划** | **LAW（无感知）L2 平均 0.61 m / 碰撞平均 0.30%**；**LAW（带感知）L2 0.49 / 碰撞 0.19**。同表 VAD 0.72 / 0.22，UniAD 1.03 / 0.31 | Table 1 |
| **NAVSIM** | **PDMS 84.6**（NC 96.4 / DAC 95.4 / TTC 88.7 / Comf 99.9 / EP 81.7） | Table 2 |
| **CARLA Town05 Long** | DS **70.1±2.6**、RC 97.8±0.9、IS 0.72±0.03 | Table 3 |
| 潜预测的时间跨度 | 消融对比 0.5 / 1.5 / 3.0 / 10.0 秒 | Table 6 |
| 潜世界模型架构 | 对比 Linear Projection 等不同设计 | Table 7 |

## 局限（本笔记指出）

- **"state-of-the-art in overall PDMS" 的口径需注意**：Table 2 里 LAW（84.6）确实高于同表所有方法，但**该表不含 DiffusionDrive（88.1）**——ICLR 2025 投稿时点早于 DiffusionDrive（2024-11）。**这是时间差，不是数字冲突**，但引用时不能说"LAW 超过 DiffusionDrive"。

## 对本项目的意义

- **它证明了"世界模型不必解码回像素"也能提升规划**——这正是 [lineage.md](../lineage.md) 阶段 4（潜空间）的核心论点，也是"潜空间与规划器接口最顺"这条判断的最早证据之一。
- **无感知输入即可用**：对研究对象有直接含义——扩散规划器若要接世界模型条件，**不一定要接一个完整的世界模型**，一个自监督的潜预测头可能就够。
- **L2 提升但碰撞率未同步改善**（无感知版 0.61 m / 0.30%，带感知版 0.49 / 0.19）：再次指向"轨迹精度与安全性不是同一个指标"（呼应 [preparation.md](../../../ideas/preparation.md) P2c）。
- 与 [transfer.md](../../diffusion-planner/transfer.md) 第 3 节"双潜世界模型做预训练"同族；本次读全文后**可从"摘要级"升级为"全文级"**。

## 待核验

- 代码未核验；潜预测的具体损失形式与"自车动作"的用法未细读。
- 与 WM-18 WorldRFT 的关系：后者明确批评"重建导向的表征学习把感知与规划纠缠"——**LAW 正是被批评的那一类**，两者可作为一条对照线。
