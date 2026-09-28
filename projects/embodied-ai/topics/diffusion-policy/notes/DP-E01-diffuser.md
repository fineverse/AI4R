# DP-E01 · Diffuser（引导式规划的源头）

- **原题**：Planning with Diffusion for Flexible Behavior Synthesis
- **作者/载体**：Michael Janner 等；arXiv [2205.09991](https://arxiv.org/abs/2205.09991) v2（2022-05 首发）；ICML 2022 长报告
- **代码**：[jannerm/diffuser](https://github.com/jannerm/diffuser)（已克隆，见 [code/repositories.md](../../../../autonomous-driving/code/repositories.md)）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 表示 | 状态-动作**联合**的二维数组轨迹（Eq.2） | Eq.2 |
| 规划视野 | T=32（locomotion）、128（block stacking）、128/265/384（Maze 三档） | 附录 C.4 |
| 生成 | 起点 τ^N~N(0,I)；去噪步 N=20（locomotion）/100（stacking）；**非 action chunk**（整条轨迹一次生成） | 附录 C.6 |
| 引导 | **classifier guidance**（Eq.3）：μ + αΣ∇J(µ)，g=∇log p(O\|τ)=∇J(µ)；引导尺度 **α=0.1**（Hopper-medium-expert 用 0.0001） | Eq.3、附录 C.7 |
| 约束 | **inpainting**（Dirac δ 扰动函数）约束首末状态 | Eq.1、Alg.1 第 10 行 |
| 训练 | 简化 ε 目标 L=E‖ε−ε_θ‖²；**纯离线，无 RL 微调** | §3 |
| 结果 | Maze2D **113.9/121.5/123.0** vs MPPI 33.2/10.2/5.1、CQL 5.7/5.0/12.5（Table 1）；D4RL 平均 77.5（Table 2）；堆叠 58.7/45.6/58.9 vs BCQ 0.0/0.0/0.0（Table 3） | Table 1/2/3 |
| 关键负结论 | 把 Diffuser 当**纯 dynamics model** 塞进 MPPI，性能 "performed no better than random" | §5.3 |
| 推理成本 | 迭代慢（§5.4）；warm-start 后步数可在 2–100 间调，Fig.7 称用 1/10 步数性能仅微降。**无 FPS/延迟数字（原文未给）** | §5.4、Fig.7 |
| 自述局限 | 单次规划生成慢 | §5.4 |

## 对本项目的意义（AI 判断）

- **可直接对应**：轨迹级生成 + 起点 inpainting（= 当前位姿约束）+ 奖励梯度引导（= 代价/约束梯度）。这与驾驶侧"分类器引导 + 可行驶区域能量"的做法同源（DP-A01 Diffusion Planner 的能量函数就是这一形式）。
- **明显不成立**：无动力学/运动学硬约束、无多智能体交互、开环且慢。
- **最值得记住的一条**：§5.3 的负结论说明**"更好的生成模型"不等于"更好的规划器"**——价值在于建模与规划耦合，而不是预测精度。这对"只把扩散当轨迹生成器"的做法是一个警告。

## 待核验

- 引导尺度 α 在不同任务间差 3 个数量级（0.1 vs 0.0001），说明引导对尺度极其敏感——驾驶侧的等价标定问题尚无人系统研究。
