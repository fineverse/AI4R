# AI4R 启动规则

每次开始工作，按顺序读取并遵守：

1. 本文件
2. [`README.md`](README.md) — 当前有两个**平级项目**（`autonomous-driving` 主方向、`embodied-ai` 次方向），看清哪个是本次任务的目标
3. 目标项目的 `project.md`、`state.md`、`index.md`

**项目的入口文件（按需，不要一次全读）**：

| 文件 | 什么时候读 |
|---|---|
| `project.md` | 确认项目定义与边界 |
| `state.md` | 每次必读——当前阶段、待续清单、**判断边界索引** |
| `index.md` | 找"某个内容在哪个文件" |
| `context.md` | 需要研究约束（数据/算力/评价口径）时 |
| `judgments.md` | 需要某条判断的**完整论证与代码出处**时（`state.md` 只留 A–H 分组索引）。**分两册**：`judgments.md` = §A–§D，`judgments-2.md` = §E–§H（2026-09-24 拆，索引表在 `judgments.md` 头部） |
| `history.md`（+ `history/` 分卷） | 需要"某轮做了什么、更正了什么"时 |
| `sources.md` / `pdfs_pending.md` | 需要来源编号或待下载清单时 |

随后按任务类型按需读取项目内对应文件，不扫描目录，不递归加载，不默认读取 `archive/`、`shared/`、`ai/`。
项目内固定**领域—专题两级树**：`direction/` 是大方向（脉络、基准、领域级综述与笔记），`topics/<小方向>/` 是小方向（`README.md` 声明角色与待回答问题、`lineage.md`、论文表、笔记）。跨专题资产（`sources.md`、`pdfs_pending.md`、`raw/`、`code/`）放项目根。

AI 详细行为规范在 [`ai/rules.md`](ai/rules.md)，任务分级与工作流在 [`ai/workflows.md`](ai/workflows.md)，仅在任务需要时读取。

**写入前检查**：凡会修改文件，先运行 `git log --oneline -5` 与 `git status --short`，识别已有改动的归属和本次目标路径。工作树非空不等于冲突；只有目标路径重叠且归属不明时才停止写入并协调。提交只按明确路径暂存，提交前检查 staged diff。

**读取与执行**：优先使用当前环境的专用读取、搜索和定位工具；缺失时允许使用范围收窄的只读 shell（搜索优先 `rg`，不可用时用 `grep`；定位可用 `find`；分段读取可用 `sed`）。中间产物放 `inbox/scratch/`，但虚拟环境、runtime、checkpoint 等耐久资产不得按临时文件清理。不可逆改写前先备份，完成后检查 diff、链接和工作树状态。
