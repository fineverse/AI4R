# 小方向：世界模型（具身侧）

- **角色**：**借鉴来源**
- **所属领域**：具身智能（本项目）
- **状态**：**已建表**（第二十五轮）：**在表 14 篇**、脉络初稿已写 → **全部摘要级**（**已读全文 0 篇、已源码核验 0 篇**；逐篇状态见 [papers.md](papers.md) 末列）。**待续**：把"有官方代码 + 有受控消融"的几篇升全文级
- **更新时间**：2026-09-24
- **产出**：[papers.md](papers.md)（14 篇，含预测表示 / 训练目标 / 耦合方式 / 代码）、[lineage.md](lineage.md)（三段 + 三条判断）

## 本小方向的文件

| 文件 | 回答什么 |
|---|---|
| [papers.md](papers.md) | 14 篇代表工作（预测表示 / 训练目标 / 与策略的耦合方式 / 代码可用性） |
| [lineage.md](lineage.md) | 三段（W1 重建式潜 rollout → W2 特征预测 → W3 生成式环境 + 联合训练）+ 三条判断 |
| [../vla/papers.md](../vla/papers.md) | 与之常合并讨论的 VLA 侧（WorldVLA / DiWA 两侧都有线索） |

## 与自动驾驶侧同名小方向的区别

**同名不同内容，各自成文。** 差异见下：

| 维度 | 具身（本文件） | 自动驾驶（[同名小方向](../../../autonomous-driving/topics/world-model/README.md)） |
|---|---|---|
| 目标 | 策略学习与想象 rollout | 给规划器当条件 |
| 输入 | 低维状态 / 图像 | BEV / 矢量化 / 传感器 |
| 代表 | Dreamer、Genie | DriveFuture、GAIA |

## 要回答的问题

1. 具身侧世界模型的**训练目标**是什么（重建 / 预测 / 对比）？与规划器的耦合方式有哪些？
2. "在潜空间里做 rollout 再选动作"这条路，能否映射到驾驶的轨迹选优？
3. 世界模型与扩散策略结合时的**接口**是什么？

## 已掌握的事实（指针）

目前**无全文级资料**。驾驶侧的相关线索在 [autonomous-driving/topics/world-model/README.md](../../../autonomous-driving/topics/world-model/README.md)。

## 边界

- **不重复**领域层的世界模型脉络（那些在 [direction/lineage.md](../../direction/lineage.md)）。
- 本小方向只保留"**能搬到研究对象（扩散规划器）上**"的部分；纯具身机器人任务本身不在范围内。
- **与驾驶侧同名小方向内容不同、各自成文**——不要交叉引用两边的论文编号（`WM-xx` 是驾驶侧的）。

## 产出状态

**已完成**：① 本目录已有 [papers.md](papers.md) 与 [lineage.md](lineage.md)；② 可迁移条目回填 [autonomous-driving/transfer.md](../../../autonomous-driving/topics/diffusion-planner/transfer.md) 第 1 节（**§1.5「第二十五轮新增 6 条候选」是 VLA 侧与世界模型侧合并计**，不是本小方向各 6 条）。

**下一步**：把重点论文升全文级——优先有官方代码 + 有受控消融的（**TD-MPC2、DINO-WM、WorldVLA、DiWA**）。
