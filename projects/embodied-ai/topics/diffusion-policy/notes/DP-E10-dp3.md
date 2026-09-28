# DP-E10 · DP3（3D Diffusion Policy）

- **原题**：3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations
- **作者/载体**：Yanjie Ze 等；arXiv [2403.03954](https://arxiv.org/abs/2403.03954) v7（2024-03-06 首发）；RSS 2024
- **代码**：[YanjieZe/3D-Diffusion-Policy](https://github.com/YanjieZe/3D-Diffusion-Policy)（见 [code/repositories.md](../../../../autonomous-driving/code/repositories.md)）
- **证据等级**：全文（arXiv HTML 逐节提取）+ 摘要
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 观测 | 单视角深度 → 稀疏点云（84×84，512/1024 点，**去色**）+ 机器人位姿 q | §III-B |
| 动作 | 关节/末端序列，动作维度 ActD 4–52；控制频率未给；chunk 长度未获取 | Tab III |
| 扩散机制 | 条件扩散，起点高斯；条件 (v,q)；训练 100 / 推理 10 步 DDIM，sample prediction | §III-C |
| 核心结论 | **3D 表示最重要**：点云 > RGB-D / depth / voxel，接近 oracle state | Tab IV |
| 编码器结论 | 简单编码器（输出 64 维）**优于** PointNeXt / Point Transformer 及预训练版本。**⚠ 更正（第二十九轮）**：本笔记原写"**3 层 MLP**"，[transfer.md §1.1](../../../../autonomous-driving/topics/diffusion-planner/transfer.md) 代码实测为 **4 层 Linear**（`in→64→128→256→512`）+ 全局 max-pool；仓库的 "simple" 变体改的是 **U-Net 宽度**，不是编码器层数 | Tab V + 代码静态检查 |
| 细节消融 | 裁剪、LayerNorm、去色都有效 | Tab VII |
| 数据 | 72 仿真任务（7 域、每域 10 演示）、4 真机任务各 40 演示 | Tab III |
| 结果 | 仿真相对提升 24.2%（Tab I）；真机平均成功率 85% | 摘要、Tab VIII |

## 作者自述局限（§VI）

- 最优 3D 表示仍未确定。
- 未涉及极长时域任务。

## 对本项目的意义（AI 判断）

- 点云条件天然对应 LiDAR/点云感知，是四篇里**最容易搬到驾驶感知层**的一篇。
- **明显不成立**：高维关节动作 ≠ 轨迹规划；无动力学与交互建模。
- 对本项目最有用的结论是负面的那条：**"简单编码器 + 好表示"胜过"复杂编码器 + 同样表示"**。驾驶侧近年大量工作堆叠 BEV/Transformer 融合，这条结论提供了一个反向对照。

## 待核验

- action chunk 长度（正文未给）。
- 驾驶数据上是否有人复现"点云条件 + 简单编码器"的结论（本轮未见）。
