# 小方向：VLA（视觉-语言-动作模型）

- **角色**：**借鉴来源** —— 不是研究对象，只取可迁移机制
- **所属领域**：自动驾驶（本项目）；具身侧的同名小方向见 [embodied-ai](../../../embodied-ai/topics/vla/README.md)，**内容不同，各自成文**
- **状态**：**已完成四轮**（第一轮薄脉络 + 论文表 18 篇；第二轮 3 篇读全文；第二十一至二十三轮 6 篇源码核验；第二十四至二十五轮补入 9 篇 VLA-20–28 并读完全部全文）→ **在表 28 篇全部全文级、14 篇已源码核验**
- **更新时间**：2026-09-23

## 本小方向的文件

| 文件 | 回答什么 |
|---|---|
| [lineage.md](lineage.md) | 2023→2026 四阶段脉络 + **与研究对象接口的 4 个问题** |
| [papers.md](papers.md) | 代表工作 **28 篇**（带 venue/CCF、引用、**质量依据 T 档**）+ 边界外清单（**轻量入口**）；**逐篇全文与代码核验结论拆到 [verification.md](verification.md)（§4–§8）+ [verification-2.md](verification-2.md)（§9–§14）** |
| [notes/](notes) | **3 篇全文笔记**：[VLA-06 DiffVLA](notes/VLA-06-diffvla.md)、[VLA-07 ReCogDrive](notes/VLA-07-recogdrive.md)、[VLA-08 KnowDiffuser](notes/VLA-08-knowdiffuser.md) |

## 为什么关注

VLA 把语言作为条件/接口，是 2024–2026 驾驶侧的一条支线。对研究对象的潜在价值在于：**条件信号怎么进生成器**，以及**语言条件是否真的被用上**。

## 要回答的问题

1. **接口形态**：VLA 输出的是轨迹、动作 token 还是语言？三种形态与扩散规划器的输出接口如何对接？
2. **延迟代价**：语言模型带来的延迟有多大，是否可能满足 ≥10 Hz 的规划频率？
3. **条件是否被淹没**：回归训练下语言条件是否被视觉先验边缘化（"条件策略坍缩"）？
4. **可迁移机制**：VLA 里有没有能改进扩散规划器**条件来源**的机制（对应 [../diffusion-planner/README.md](../diffusion-planner/README.md) 的横切轴 2）？

## 已知线索 → 已升级为正式条目

| 线索 | 现在的状态 |
|---|---|
| DriveVLM / DriveLM：VLM 支线，DriveLM 实测 **0.16 FPS** | 已升为 [papers.md](papers.md) **VLA-13 / VLA-14**（T1）；笔记在 [../../direction/notes/](../../direction/notes) |
| "条件策略坍缩"（语言条件被视觉先验边缘化） | 已写入 [lineage.md](lineage.md) 接口差异第 3 问；来源 DP-A26 |
| 驾驶侧 VLA 生成式规划器（DiffVLA、ReCogDrive、KnowDiffuser） | 已升为 **VLA-06 / VLA-07 / VLA-08**（T4，与研究对象直接同构） |
| 具身侧 VLA（π0 / π0.5） | 仍属具身项目，见 [embodied-ai](../../../embodied-ai/topics/diffusion-policy/notes/DP-E19-pi0.md) |

## 边界

- 不重复领域层的 VLM 支线内容（那些在 [../../direction/notes/](../../direction/notes)）。
- 本小方向只保留"能搬到研究对象上"的部分。

## 产出状态

**四轮已完成**：① `lineage.md`（四阶段脉络）与 `papers.md`（28 篇论文表）已建立；② 可迁移机制已回填 [../diffusion-planner/transfer.md](../diffusion-planner/transfer.md) 第 2 节；③ 逐篇全文与代码核验结论写在 [verification.md](verification.md) / [verification-2.md](verification-2.md) —— **28/28 全文级、14 篇源码核验、28 篇全部核过代码可用性**。

**边界外清单已复核完毕**（第二十四轮：15 条复核 → 9 条升为 VLA-20–28）。
