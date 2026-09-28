# 具身智能项目 · 逐轮工作记录

更新时间：2026-09-23  
用途：保存**每一轮的详细记录**（做了什么、更正了什么、产出在哪）。[state.md](state.md) 只保留**当前阶段 + 待续清单 + 判断边界**，需要追溯细节时读本文件。  
约定与自动驾驶项目一致（见 [ai/workflows.md](../../ai/workflows.md)、[workspace-design.md](../../shared/workspace-design.md) §运行纪律第 3 条）：**本文件超过 200 行时按时间段拆卷**（当前 **5 轮**：第七、八、二十五、二十六、二十九轮，未到阈值）。

## 第七轮（知识体系重构：本项目从自动驾驶项目中独立，2026-09-23）

- 从原 `diffusiondrive` 项目**独立为本项目**（该项目同期改名为 `autonomous-driving`）
- 迁入论文表 [DP-E01–E28](topics/diffusion-policy/papers/diffusion_planner_embodied.md) + CSV（含"可迁移机制"节）
- 迁入 9 篇笔记至 [topics/diffusion-policy/notes/](topics/diffusion-policy/notes)（DP-E01/E04/E08/E09/E10/E11/E15/E17/E19）
- 新建 `direction/` 与 `topics/{vla,world-model}/README.md` **骨架**
- 迁入前的工作记录（第一至六轮）留在自动驾驶项目的 [state.md](../autonomous-driving/state.md) 与 [history.md](../autonomous-driving/history.md)

## 第八轮（结构复查与二次优化，2026-09-23）

- 本项目的 6 个代码仓库**不单独存放**，与其余 31 个一并放在自动驾驶项目根的 [code/repos/](../autonomous-driving/code/repos)——理由见 [workspace-design.md](../../shared/workspace-design.md) §当前落地状态
- `topics/<x>/topic.md` 统一改名为 `README.md`

## 第二十五轮（脉络与两个借鉴来源建表，2026-09-23）

- [direction/lineage.md](direction/lineage.md) **从骨架写成初稿**：具身侧两条线（策略的动作表示 4 段 / 世界模型 3 段）+ **与自动驾驶的接口差异表（5 维，含具体数字与出处）** + "量级差异 vs 结构差异"的判断 + 4 条已发生的迁移实证
- 新建 [topics/vla/papers.md](topics/vla/papers.md)（**14 篇**）+ [lineage.md](topics/vla/lineage.md)
- 新建 [topics/world-model/papers.md](topics/world-model/papers.md)（**14 篇**）+ [lineage.md](topics/world-model/lineage.md)
- 回填自动驾驶侧的 [transfer.md](../autonomous-driving/topics/diffusion-planner/transfer.md) 第 1 节（新增 6 条可迁移机制候选）
- **同轮两条更正**：① `topics/diffusion-policy` 表里 FLOWER 的仓库链接**是 404**，实为 `flower_vla_pret` / `flower_vla_calvin`；② 该表**摘要级条目数由"约 10 条"更正为 15 条**
- **同轮两条被证伪的常见说法**（写在 [direction/lineage.md](direction/lineage.md)）：① "动作 token → 动作块 → 连续头"在具身侧**不成立**（ACT 与 Diffusion Policy 同在 2023 年）；② "重建 → 预测 → 对比"**也不成立**（对比是自 2020 年起的平行支线）

## 第二十六轮（结构对齐，2026-09-23）

**动因**：主项目 `autonomous-driving` 做了一轮工作流与结构升级，本项目需对齐；子代理审计出 6 处缺陷。

- **修掉一处直接矛盾**：[project.md](project.md) 原写"`direction/lineage.md` 目前只有骨架；`topics/vla/`、`topics/world-model/` 尚无资料"，与 [state.md](state.md) 的第二十五轮记录**直接冲突**（未随上一轮更新）→ 已按实际状态更正
- **收敛 4 处重复**："6 个仓库跨项目共用、未拆分"原在 `state.md`（两处）、`project.md`、`sources.md` 各写一份 → 统一为**指向 [workspace-design.md](../../shared/workspace-design.md) §当前落地状态**的指针
- **结构对齐**：本文件新建（此前逐轮记录内联在 `state.md`）；`state.md` 的「下一步」改为与主项目一致的「**待续清单**」表格，「已完成」迁出到本文件
- **术语对齐**：证据状态统一用 [ai/rules.md](../../ai/rules.md) §证据等级的权威术语（含代码核验 **L1/L2/L3** 标注位）

## 第二十九轮（知识层一致性审计与收口，2026-09-24）

**动因**：主项目第二十八轮做的是**知识层**审计（不只看链接与计数），本轮把同一套五问搬到本项目。

- **修掉 8 处事实冲突**，最严重的是 **DP-E08 的代码级别三处互相矛盾**——[diffusion_planner_embodied.md](topics/diffusion-policy/papers/diffusion_planner_embodied.md) 文件头写「DP-E08 …为 L1（仓库已落盘）」，但同表该行与笔记都写"未核验"，而 AD 表 DP-A20 明确「**无公开仓库**」。**实为 `DP-E01`**（落盘的 4 个仓库是 `diffuser / diffusion_policy / 3D-Diffusion-Policy / visualnav-transformer`）→ 已更正并标 ⚠
- **另 7 处**：两份脉络的"未取得控制频率"与已登记的 RDT-1B / FLOWER / π0.5 频率冲突；Consistency Policy 的 venue 两说；**DP-E10 编码器"3 层 MLP"→ 代码实测 4 层 Linear**；**DP-E19「总 3.3B」→ 代码实测 2.3B**；本文件原写"当前 3 轮"（实含 4 轮）；**B009–B011 的链接指向主项目**（应指本项目）；"第二十五轮新增 6 条"被两个小方向 README 各认领一次
- **3 处悬空引用**：上述 B009 跨项目指错、`world-model/lineage.md` 的"本页 §3 的第三问"（实为 `README.md` 问题清单第 3 条）、**AD 表"指针行"清单漏列 §A 的 DP-E01 行**
- **论文表"未核验"落后于"指针"侧**：AD 表的 DP-A17/A20/A23/A24 已给出代码结论，而"完整登记"的 DP-E05/E06/E07/E08 仍写"未核验"→ 四行**回填真实代码状态并回指 AD 编号**
- **笔记可达性**：8 篇笔记（DP-E01/E04/E08/E09/E10/E11/E15/E17）此前除 `sources.md` 外无任何入链 → 在论文表对应行补指针；该项并已成为 [shared/scripts/check_links.py](../../shared/scripts/check_links.py) 的**第四项检查**（引用可达性）
- **验证**：四项检查全绿（死链 0 / 行数超限 0 / 表格不匹配 0 / 孤儿 0 / 弱引用 0）
