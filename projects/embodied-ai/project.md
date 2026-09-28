# 具身智能探索项目

项目性质：**次方向 / 来源领域**，尚未选定为正式课题。  
在 AI4R 中与 [autonomous-driving](../autonomous-driving/project.md) **平级**：它是一个有自己大方向与小方向的完整领域，**不隶属于自动驾驶**。

## 定位

为研究对象（自动驾驶侧的[扩散规划器](../autonomous-driving/topics/diffusion-planner/README.md)）提供**可迁移机制**。本项目不追求领域覆盖完整，只求"够取材"。

## 与自动驾驶项目的关系

- **单向借鉴**：具身 → 自动驾驶。汇总在 [自动驾驶 transfer.md](../autonomous-driving/topics/diffusion-planner/transfer.md) 第 1 节。
- **不共享文档**：VLA、世界模型在两个项目里**同名不同内容**（输出形式、基准、延迟约束各异），各自成文。

## 结构约定

与自动驾驶项目相同的**领域—专题两级树**（约定见 [workspace-design.md](../../shared/workspace-design.md)「领域—专题骨架」）：

- `direction/` — 大方向：具身智能脉络
- `topics/<小方向>/` — 小方向：`diffusion-policy`、`vla`、`world-model`

## 当前边界

- 具身侧多数条目为**摘要级**；"可迁移机制"是 AI 判断，不是已成立结论。
- **资料状态（2026-09-23 第二十六轮更正）**：`direction/lineage.md` **已从骨架写成初稿**（两条线 + 与自动驾驶的 5 维接口差异表）；`topics/vla/` 与 `topics/world-model/` **已各建 14 篇论文表 + 脉络**（均摘要级）。此前本行写"只有骨架 / 尚无资料"，未随第二十五轮更新，**已更正**。
- 具身侧的 6 个代码仓库**保存在自动驾驶项目的 `code/repos/` 中，未按项目拆分**——**理由与完整清单见 [workspace-design.md](../../shared/workspace-design.md) §当前落地状态**（此处不重复）。

## 当前状态

已从原 `diffusiondrive` 项目迁入具身侧论文表（DP-E01–E28）与 9 篇笔记。详见 [state.md](state.md)；逐轮记录见 [history.md](history.md)。
