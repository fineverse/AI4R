# DP-E17 · NoMaD（最接近驾驶的具身扩散策略）

- **原题**：NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration
- **作者/载体**：Ajay Sridhar 等；arXiv [2310.07896](https://arxiv.org/abs/2310.07896) v1（2023-10-11）
- **代码**：[robodhruv/visualnav-transformer](https://github.com/robodhruv/visualnav-transformer)（见 [code/repositories.md](../../../../autonomous-driving/code/repositories.md)）
- **证据等级**：全文（arXiv HTML 逐节提取）+ 摘要
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> ...we describe how we can train a single unified diffusion policy to handle both goal-directed navigation and goal-agnostic exploration, with the latter providing the ability to search novel environments...

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 观测 | 当前及过去 RGB o_{t−P:t}（EfficientNet-B0），可选目标图像 o_g | §III |
| 动作 | 未来动作序列 a_{t:t+H}（导航 waypoint）；控制频率未给；H 未获取 | §III |
| 扩散机制 | DDPM，起点高斯；K=10 步去噪；1D U-Net（15 卷积层） | §IV-C |
| 目标掩码 | 条件 c_t 以 Bernoulli p_m=0.5 随机掩码目标 → **同一策略同时做目标导航与无目标探索** | §IV-A |
| 关键消融 | 视觉编码器最关键（Table III）：ViNT Transformer 编码器 + attention goal masking 最优，CNN/ViT 均差；统一策略 ≈ 专用策略（Table II） | Table II/III |
| 参数效率 | 比 ViNT 子目标扩散方案少 15× 参数（Table I） | Table I |
| 数据 | GNM + SACSoN，**>100 小时真机轨迹** | §IV-C |
| 结果 | 6 个环境；无向探索超 Subgoal Diffusion >25%（Tab I）；已知环境匹配 SOTA | Table I |

## 作者自述局限（§VI）

- 目标只支持图像模态。
- 前沿探索策略较简单。

## 对本项目的意义（AI 判断）

- **四篇具身核心论文中最接近驾驶的一篇**：输入（前视相机 + 目标）与输出（2D waypoint 序列）与驾驶规划器几乎同构；评价（成功率/碰撞数）可映射为到达率/碰撞率。
- **明显不成立**：动作只是 2D 运动学，无车辆动力学、无他车博弈、无交通规则语义。
- **可借机制**：目标掩码让同一策略在"有目标/无目标"间切换——对应驾驶中"有导航指令/无指令"以及多指令切换；这比"额外加一个 goal encoder"更轻。

## 待核验

- action chunk 长度 H 与控制频率（正文未获取）。
- 是否有人在驾驶数据上复现过 goal masking（本轮检索未见）。
