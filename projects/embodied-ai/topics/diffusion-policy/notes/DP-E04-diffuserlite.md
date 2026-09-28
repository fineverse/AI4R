# DP-E04 · DiffuserLite（粗到细规划）

- **原题**：DiffuserLite: Towards Real-time Diffusion Planning
- **作者/载体**：Zibin Dong 等；arXiv [2401.15443](https://arxiv.org/abs/2401.15443) v5（2024-01 首发）；NeurIPS 2024
- **代码**：见论文项目页（未核验）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 表示 | 状态序列 + 逆动力学出动作；3 级"规划精化过程"（PRP，粗到细），temporal jump 32/8/1 与 16/4/1；总 horizon 129（MuJoCo/Antmaze）/49（Kitchen） | §3 |
| 生成 | 扩散 3 步（MuJoCo/Kitchen）/5 步（Antmaze）；R1 Euler 3 步；R2 1–2 步；可选 rectified flow | §4 |
| 引导 | CFG（Eq.6），**只加在最粗一级**；critic 条件（IQL 值，Eq.9/10）用于选择最优候选 | Eq.6/9/10 |
| 推理成本 | MuJoCo 平均 **122.44 Hz**（runtime 0.008–0.020 s）；对比 Diffuser **1.5 Hz / 0.665 s**、Decision Diffuser **0.47 Hz / 2.142 s**（Table 1） | Table 1 |
| 关键消融 | Table 7：仅末级 → −84.1%、无 PRP → −27.1%、DD-small → −72.3%（Hopper 平均）；**2 级在 Antmaze 掉到 0.0**，需 3–4 级（Table 6） | Table 6/7 |
| 插件效果 | 作为插件提升频率 **560%**，性能仅降 3.2%（Table 5） | Table 5 |
| 自述局限 | CFG 需调目标条件，多级结构下更繁琐 | §7 |

## 对本项目的意义（AI 判断）

- **最相关的一篇**：122 Hz 远超驾驶 10 Hz 需求；"粗到细"与分层轨迹规划（远端粗、近端细）在结构上直接对应；逆动力学 = 轨迹到控制量的转换。
- 对本项目的具体含义：**若目标只是"更快"，DiffuserLite 的 PRP 已经把这条路走通**（560% 频率提升、3.2% 性能损失）。因此"再做一个更快的扩散规划器"不是好选题，除非速度与**硬约束**同时被要求（此时 PRP 的粗层是否还能保证约束，是一个未验证的问题）。
- 一个可直接检验的假设：把 PRP 用在驾驶上，**粗层的约束违反如何传播到细层**——现有工作没有回答。

## 待核验

- 官方代码；PRP 的级数与驾驶视野（8 秒 @10 Hz）如何对应。
