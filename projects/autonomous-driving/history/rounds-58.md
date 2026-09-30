# 第五十八轮（2026-09-30）：工作流与工作空间整理（审计 + 修 stale）

## 动因

用户要求"整理一下现在的工作流和工作空间"。派只读子代理审计 8 份工作流文档（[AGENTS.md](../../../AGENTS.md) / [rules.md](../../../ai/rules.md) / [workflows.md](../../../ai/workflows.md) / [templates.md](../../../ai/templates.md) / [workspace-design.md](../../../shared/workspace-design.md) / [research-workflow.md](../../../shared/research-workflow.md) / [shared/index.md](../../../shared/index.md) / [README.md](../../../README.md)）与 `projects/`、`shared/`、`inbox/` 目录结构。

## 审计结论（要点）

- **职责矩阵清晰**：`rules.md` = 证据等级/尺寸/清理的唯一定义处；`workspace-design.md` = 组织唯一定义处；`README.md` 明确声明"不定义结构"。8 份文档均有明确角色。
- **确认 6 处 stale**（见下"已修"）。
- **结构问题**（本轮未动，见"未做"）：`history/` 命名不一致（`rounds-24a/b/c`、单轮 `rounds-25` 违反对照 `rounds-<起始>-<结束>.md`）；topic 布局不一致（`diffusion-planner`/`diffusion-policy` 用 `papers/` 子目录，`vla`/`world-model` 用扁平 `papers.md`）。
- **冗余**：git 提交命令与 `.gitignore` 三条在 `rules.md` 与 `workflows.md` **逐字重复**；"十项检查"清单在 **3 处**（脚本 docstring / `shared/index.md` / `workflows.md`）重复；`research-workflow.md` 与 `workspace-design.md` 各写一节工作空间原则。
- **约定落地度**：`check_links.py` 已机器化 10 项；**未机器化**的有——文档 ≤64 KB（仅人工"看体积"）、每轮 git 提交、不可逆前备份、分册 `-2` 命名、README「最近动态」指针。

## 已修（6 处，本轮）

| 文件 | 问题 | 修法 |
|---|---|---|
| [README.md](../../../README.md) | 「最近动态」停在第五十六轮 | 补第五十七轮，并把上一轮降为"上一轮" |
| [README.md](../../../README.md) | 写"索引 + 31 卷" | → **39 卷**（与 `index.md`/`state.md`/`history.md` 对齐） |
| [project.md](../project.md) | 「当前状态」写"第五十一轮" | → **第五十七轮** |
| [state.md](../state.md) | 写"拆为 7 卷" | → **5 卷**（与 `workspace-design.md` 对齐） |
| [templates.md](../../../ai/templates.md) | "两份 `papers` 按 `-2` 命名"（**工作空间无任何 `papers-2.md`**） | 改述为"同名分册 / 换 basename"两种真实形态 |
| [templates.md](../../../ai/templates.md) | 代码脉络分册范围只写了一种 | 补三种脉络各自的 §范围与分册点 |
| [index.md](../index.md) | 把 `experiments/records/` 等**不存在**的目录列为"待建设" | 改为"尚未建立"并说明触发条件 |
| [.gitignore](../../../.gitignore) | 未忽略 `.vscode/` | 补上 |

## 验证

`check_links.py` 全绿（死链 0 / 分册章节引用 0 不可达 / 三项计数一致）。提交 `2591377`。

## 未做（结构类，改动面大，留待用户确认）

1. `history/` 卷文件命名统一（`rounds-24a/b/c`、单轮卷）；
2. 两个 topic 的论文表布局统一（子目录 vs 扁平）；
3. 三处冗余（git 命令、十项检查清单、两文原则节）收敛为"一处定义 + 指针"；
4. 未机器化的约定（体积、git 提交、README 指针）补进 `check_links.py`。
