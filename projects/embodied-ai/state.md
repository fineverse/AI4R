# 具身智能项目状态

更新时间：2026-09-30  
逐轮详细记录已迁出至 [history.md](history.md)（**2026-09-23 第二十六轮建立**）；本文件只保留当前阶段、待续清单与判断边界。

## 当前阶段

**来源领域**（次方向），只做薄：资料已迁入（论文表 DP-E01–E28 + 9 篇笔记），**并已写出具身智能自身的脉络初稿 + 两个借鉴来源（VLA / 世界模型）的论文表与脉络**（第二十五轮）。**第二十六轮完成结构对齐**（修掉 `project.md` 与 `state.md` 的矛盾、收敛重复定义、建立本项目的 `history.md`）。**第二十九轮（2026-09-24）做知识层一致性审计**（与主项目第二十八轮同一套五问）：修 **8 处事实冲突**（最严重的是 **DP-E08 的代码级别三处互相矛盾，实为 DP-E01**）、**3 处悬空引用**（含 **B009–B011 的链接指向主项目**）、**论文表"未核验"落后于主项目指针侧**（DP-E05/E06/E07/E08 四行回填并回指 AD 编号）；8 篇笔记补上入链。**2026-09-30 补两轮**：第五十五轮**用 S2 官方 API 补齐 VLA 表引用数**（7 → **14/14**，四篇 venue 缺口补上、GR00T N1 引用数悬案关闭，并发现 **S2 的 `venue` 字段系统性误记**）；第五十七轮给 **DP-E 表**补「逐行质量依据（T 档）」。**第六十轮（主线程）补齐两个借鉴来源的「§1.1 逐行证据等级与代码状态」**——即第 57 轮声称的"8 张表"实际只落了 6 张，缺口在此关闭。项目未立项。

**结构**：与 [autonomous-driving](../autonomous-driving/index.md) 相同的**领域—专题两级树**——`direction/`（大方向）+ `topics/`（小方向：`diffusion-policy`、`vla`、`world-model`）。两项目平级，本项目**不隶属于**自动驾驶。

**主要产出**：

| 类别 | 内容 |
|---|---|
| 脉络 | [具身智能脉络](direction/lineage.md)（两条线 + **与自动驾驶的 5 维接口差异表** + 4 条迁移实证） |
| 论文表 | [扩散策略 DP-E01–E28](topics/diffusion-policy/papers/diffusion_planner_embodied.md)（+ CSV，含"可迁移机制"节 + **逐行质量依据（T 档）**）、[VLA 14 篇](topics/vla/papers.md)（**§1.1 逐行证据等级与代码状态**、§4 引用数 14/14 走 S2 口径）、[世界模型 14 篇](topics/world-model/papers.md)（**§1.1 逐行证据等级与代码状态**） |
| 笔记 | 9 篇（DP-E01/E04/E08/E09/E10/E11/E15/E17/E19，见 [notes/](topics/diffusion-policy/notes)） |
| 来源 | [sources.md](sources.md) |

## 待续清单（没做完的，按优先级）

| # | 事项 | 状态与阻塞原因 | 记录位置 |
|---|---|---|---|
| 1 | 把两借鉴来源的**重点论文升全文级** | 目前 28 篇**全部摘要级**；优先"有官方代码 + 有受控消融"的：FLOWER、RDT-1B、GR00T N1、TD-MPC2、DINO-WM、WorldVLA | [vla/papers.md](topics/vla/papers.md)、[world-model/papers.md](topics/world-model/papers.md) |
| 2 | `topics/diffusion-policy/` 的 **15 条摘要级**条目做分级补全 | 未开始（此前记为"约 10 条"，第二十五轮更正为 15） | [papers.md](topics/diffusion-policy/papers/diffusion_planner_embodied.md) |
| 3 | 继续把新产出的可迁移机制回填自动驾驶侧的 transfer.md | 第二十五轮已回填 **§1.5**（VLA 侧与世界模型侧**合并计** 6 条）；后续按需追加 | [autonomous-driving/transfer.md](../autonomous-driving/topics/diffusion-planner/transfer.md) |
| 4 | 本项目是否需要 `context.md` / `pdfs_pending.md` | 待判断——若本项目也进入 idea 讨论阶段则需要 | — |

## 当前判断边界

- 论文数字均为**论文自述**，未本地复现；具身侧的 6 个代码仓库在自动驾驶项目的 `code/repos/` 中，**未安装、未运行**（**共用理由见 [workspace-design.md](../../shared/workspace-design.md) §当前落地状态**）
- **两个借鉴来源的 28 篇（VLA 14 + 世界模型 14）全部为摘要级**——频率、benchmark、"有无权重"多为 README / 摘要自述；**引用数按 OpenAlex 标题查得的多为 arXiv 存根、系统性低估，不用于排序**
- `topics/diffusion-policy/` 的 28 条里**有 15 条为摘要级**（此前记为"约 10 条"，第二十五轮更正）
- **两条已更正的记录**：① 该表里 FLOWER 的仓库链接**是 404**，实为 `flower_vla_pret` / `flower_vla_calvin`；② 上一轮之前 `project.md` 曾记"lineage 只有骨架"，第二十六轮已更正
- **第二十九轮新增三条更正**（均因"论文表落后于代码核验"）：① **DP-E10 的编码器是 4 层 Linear**（`in→64→128→256→512`），不是论文表/笔记原写的"3 层 MLP"；仓库的 "simple" 变体改的是 **U-Net 宽度**；② **DP-E19 的总参数代码实测为 2.3B**（`gemma_2b` + `gemma_300m`），论文称 3.3B 在代码里无法确认；③ **DP-E08（SafeFlowMatcher）无公开仓库**（只有匿名 supplementary），此前被误标为 L1
- **代码可用性口径**：本表四行（DP-E05/E06/E07/E08）的代码状态**以主项目 AD 表为准**（DP-A17/A20/A23/A24），避免两处各写一份
- **两条被证伪的常见说法**（详见 [direction/lineage.md](direction/lineage.md)）："动作 token → 动作块 → 连续头"与"重建 → 预测 → 对比"**在具身侧都不成立**
- 本项目是**次方向**，不追求覆盖完整；其结论在验证前**不得直接写进自动驾驶侧的论文正文**
