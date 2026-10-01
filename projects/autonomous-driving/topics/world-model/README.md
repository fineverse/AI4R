# 小方向：世界模型（World Model）

- **角色**：**借鉴来源** —— 不是研究对象，只取可迁移机制
- **所属领域**：自动驾驶（本项目）；具身侧的同名小方向见 [embodied-ai](../../../embodied-ai/topics/world-model/README.md)，**内容不同，各自成文**
- **状态**：**已完成四轮**（第一轮薄脉络 + 论文表 20 篇；第二轮 5 篇读全文；第三轮 4 篇读全文 + WoTE 代码级核验；第二十四至二十五轮把接口细化到五条、补录 4 篇并读完全部全文）→ **在表 24 篇全部全文级、13 篇已源码核验**
- **更新时间**：2026-09-23

## 本小方向的文件

| 文件 | 回答什么 |
|---|---|
| [lineage.md](lineage.md) | 2023→2026 五类预测空间脉络 + **世界模型 → 规划器的五条接口路线** + **与研究对象接口的 4 个问题** |
| [papers.md](papers.md) | 代表工作 **24 篇**（带 venue/CCF、引用、**质量依据 T 档**）+ 补录结果 + 边界外清单（**轻量入口**）；**§4 逐篇全文核验结论拆到 [verification.md](verification.md)** |
| [notes/](notes) | **5 篇全文笔记**：[WM-01 Drive-WM](notes/WM-01-drive-wm.md)、[WM-03 OccWorld](notes/WM-03-occworld.md)、[WM-06 LAW](notes/WM-06-law-latent-world-model.md)、[WM-17 Policy World Model](notes/WM-17-policy-world-model.md)、[WM-18 WorldRFT](notes/WM-18-worldrft.md)（**WM-19/21/22/23/24 五篇的关键事实已拆到 [verification.md §4.1](verification.md)**） |

## 为什么关注

世界模型与规划器的接口最紧：它既可能作为**条件**（未来潜状态）喂给生成器，也可能自己就是规划器。驾驶侧已有实证表明这条轴的收益远大于改生成日程。

## 要回答的问题

1. **作为条件还是作为规划器**：世界模型是给扩散规划器提供条件，还是直接替代它？
2. **潜状态 vs 显式预测**：未来潜状态、显式轨迹预测、occupancy 三类表示，哪一种与扩散生成器的接口最顺？
3. **收益来源**：把未来信息作为条件带来的提升，究竟来自"信息更多"还是"训练信号更好"？
4. **代价**：世界模型自身的推理成本是否吃掉了实时性余量？

## 已知线索 → 已升级为正式条目

| 线索 | 现在的状态 |
|---|---|
| DriveFuture：换条件（未来潜状态）后在 NAVSIM v2 navhard 让 DiffusionDrive **受控 +3.7（30.9→34.6）**；**55.5 含 scorer**（⚠ 第七十一轮更正：勿写成"24.2→55.5 是换条件的收益"） | 已升为 [papers.md](papers.md) **WM-09**（T4，与研究对象直接同构）；[全文笔记](../diffusion-planner/notes/DP-A31-drivefuture.md) |
| "改条件的收益大于改生成日程"（AI 判断） | 保留为**待验证假设**；[lineage.md](lineage.md) 接口差异第 3 问把它列为"可做实验的空白" |
| WAM-Flow：世界模型 + 离散流匹配 | 仍在研究对象表 DP-A13（摘要级），未升为 WM 条目 |
| 具身侧世界模型（Dreamer / Genie 系） | 仍属具身项目，见 [embodied-ai](../../../embodied-ai/topics/world-model/README.md) |

## 边界

- 不重复领域层内容；本小方向只保留"能搬到研究对象上"的部分。

## 产出状态

**四轮已完成**：① `lineage.md`（五类预测空间脉络）与 `papers.md`（24 篇论文表）已建立；② 可迁移机制已回填 [../diffusion-planner/transfer.md](../diffusion-planner/transfer.md) 第 3 节；③ **第二十四轮把"世界模型 → 规划器"的接口从三条细化到五条**（新增"特征级条件"与"RL 的 reward/next-state 来源"），并对 **WoTE 做了代码级核验**（结论见 [C004 §E](../../code/traces/world_model_code_traces.md)）；④ **第二十四至二十五轮**：arXiv ID 补录 **8/8 解决**（含两个"根本没有 arXiv 版本"的：NeMo = ECCV'24 会议版、OccVAR = 已撤稿投稿），并**把 24 篇全部读成全文** → **摘要级 0 篇、14 篇已源码核验**（结论见 [verification.md](verification.md)）。

**下一轮待补**：本小方向**文献侧已结账**；再推进只有两条路——运行验证（需算力与数据），或从 [preparation.md §5](../../ideas/preparation.md) 的候选方向里挑一个做受控实验。
