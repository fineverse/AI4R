# 小方向：扩散策略（Diffusion Policy）

- **角色**：对应自动驾驶侧的研究对象（[扩散规划器](../../../autonomous-driving/topics/diffusion-planner/README.md)）
- **所属领域**：具身智能（本项目）
- **状态**：资料已迁入，**未写脉络**。**在表 28 篇**（DP-E01–E28）；**9 篇有全文笔记**（DP-E01/E04/E08/E09/E10/E11/E15/E17/E19）；**代码级核验**：**DP-E01/E09/E10/E17/E19 为 L1**（仓库已落盘）+ **DP-E05/E06/E07/E08 已核代码可用性**；**逐篇证据状态以 [papers/](papers) 末列为准**（多数为"元数据 + 摘要"）
- **更新时间**：2026-09-24

## 边界

- **纳入**：生成过程用于**动作或轨迹决策**的工作（含通用决策 / 离线 RL / 机器人策略 / 导航）。
- **不纳入**：纯感知、纯图像生成。

## 本小方向的文件

| 文件 | 回答什么 |
|---|---|
| [papers/](papers) | DP-E01–E28 论文表（含"可迁移机制"节）+ CSV |
| [notes/](notes) | 9 篇单篇笔记 |
| [../../direction/lineage.md](../../direction/lineage.md) | 具身智能大方向脉络（两条线 + **与自动驾驶的 5 维接口差异表**） |
| [../../../autonomous-driving/topics/diffusion-planner/transfer.md](../../../autonomous-driving/topics/diffusion-planner/transfer.md) | 可迁移机制的**汇总处**（§1 = 具身侧 15 条） |

## 与自动驾驶侧的差异（要点）

| 维度 | 具身（本小方向） | 自动驾驶（研究对象） |
|---|---|---|
| 输出 | 动作块 / 关节位置 / 末端位姿 | 轨迹（如 8 秒 @10 Hz） |
| 频率要求 | 5–15 Hz 常见 | ≥10 Hz，实时方案 45–59 FPS |
| 安全约束 | 一般无形式化要求 | 有碰撞 / 运动学 / 可行驶区要求 |
| 基准 | RoboMimic、LIBERO、EBench（B009–B011） | NAVSIM、Bench2Drive、nuPlan |

## 要回答的问题

1. **哪些机制在代码层被证实**、可以搬到驾驶的轨迹生成？（现在多数只有摘要级证据）
2. **哪些结论是结构性的、不能搬**？具身是"高维瞬时动作"、驾驶是"低维长序列"，两者**没有共享接口**（见 [direction/lineage.md §3.1](../../direction/lineage.md)）
3. 28 篇里**哪些值得升全文级**？优先"有官方代码 + 有受控消融"的——判据来自本项目自己的教训：**论文级数字必须先核代码**（[transfer.md §1.1](../../../autonomous-driving/topics/diffusion-planner/transfer.md) 已据此更正过 3 条）

## 产出状态

**已完成**：① 论文表 DP-E01–E28（含"可迁移机制"节）+ CSV；② 9 篇全文笔记；③ 具身智能大方向脉络（两条线 + **与自动驾驶的 5 维接口差异表** + 4 条迁移实证）。

可迁移到研究对象的机制**不在本文件重复**，统一汇总在 [autonomous-driving/transfer.md](../../../autonomous-driving/topics/diffusion-planner/transfer.md) §1。
