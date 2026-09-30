# 小方向：VLA（具身侧）

- **角色**：**借鉴来源**
- **所属领域**：具身智能（本项目）
- **状态**：**已建表**（第二十五轮）：**在表 14 篇**、脉络初稿已写 → **全部摘要级**（**已读全文 0 篇、已源码核验 0 篇**；逐篇状态见 [papers.md](papers.md) 末列）。**待续**：把"有官方代码 + 有受控消融"的几篇升全文级
- **更新时间**：2026-09-30
- **产出**：[papers.md](papers.md)（14 篇，含动作形式 / 是否生成式 / 频率 / 代码；**§4 为全部 14 篇的 S2 口径引用数 + 影响力引用数**）、[lineage.md](lineage.md)（三段 + 三条判断）

## 本小方向的文件

| 文件 | 回答什么 |
|---|---|
| [papers.md](papers.md) | 14 篇代表工作（动作形式 / 是否生成式 / 频率 / 代码可用性 / §4 引用数） |
| [lineage.md](lineage.md) | 三段（V1 语言解释 → V2 离散 token → V3 连续动作头）+ 三条判断 |
| [../diffusion-policy/papers/](../diffusion-policy/papers/diffusion_planner_embodied.md) | 与之同源的**扩散策略**表（DP-Exx，含 π0 / π0.5 / FLOWER / RDT-1B 等 VLA 相关条目） |

## 与自动驾驶侧同名小方向的区别

**同名不同内容，各自成文。** 差异见下（驱动/接口层面）：

| 维度 | 具身（本文件） | 自动驾驶（[同名小方向](../../../autonomous-driving/topics/vla/README.md)） |
|---|---|---|
| 输出 | 动作 token / 动作块 | 轨迹或语言 |
| 基准 | LIBERO、SimplerEnv | NAVSIM、Bench2Drive |
| 延迟容忍 | 5–15 Hz | ≥10 Hz，且过安全约束 |
| 代表 | π0 / π0.5、OpenVLA | DriveVLM / DriveLM |

## 要回答的问题

1. VLA 在具身侧的**接口形态**如何演化（动作 token → 动作块 → 连续动作头）？
2. 与扩散策略的关系：VLA 的动作头是否也在用扩散 / 流匹配（如 π0、FLOWER）？
3. 具身侧的 VLA 有哪些**条件化机制**可能对扩散规划器有用？

## 已掌握的事实（指针）

| 内容 | 位置 | 证据等级 |
|---|---|---|
| π0 / π0.5（流匹配动作头） | [../diffusion-policy/notes/DP-E19-pi0.md](../diffusion-policy/notes/DP-E19-pi0.md) | 全文 |
| FLOWER（高效 VLA 流策略） | [../diffusion-policy/papers/](../diffusion-policy/papers/diffusion_planner_embodied.md) DP-E14 | 摘要级 |
| RDT-1B（统一动作空间） | 同上 DP-E21 | 摘要级 |

## 边界

- **不重复**领域层的 VLA 脉络（那些在 [direction/lineage.md](../../direction/lineage.md)）。
- 本小方向只保留"**能搬到研究对象（扩散规划器）上**"的部分；纯具身机器人任务本身不在范围内。
- **与驾驶侧同名小方向内容不同、各自成文**——不要交叉引用两边的论文编号（`VLA-xx` 是驾驶侧的）。

## 产出状态

**已完成**：① 本目录已有 [papers.md](papers.md) 与 [lineage.md](lineage.md)；② 可迁移条目回填 [autonomous-driving/transfer.md](../../../autonomous-driving/topics/diffusion-planner/transfer.md) 第 1 节（**§1.5「第二十五轮新增 6 条候选」是 VLA 侧与世界模型侧合并计**，不是本小方向各 6 条）。

**下一步**：把重点论文升全文级——优先有官方代码 + 有受控消融的（**FLOWER、RDT-1B、GR00T N1、OpenVLA-OFT**）。
