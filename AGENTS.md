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

AI 详细行为规范在 [`ai/rules.md`](ai/rules.md)，工作流在 [`ai/workflows.md`](ai/workflows.md)，仅在需要引用具体规范时读取。
**并行会话**：本工作空间**可能同时有别的会话在改同一批文件**（同一工作树，改动是 **last-write-wins、覆盖无警告**）。**动手前先读 [`ai/rules.md`](ai/rules.md) §支线协作纪律并跑开轮 pre-flight**（`git log --oneline -5` + `git status --short`）——**若你不是本轮的主线程**（轮次号只由主线程分配），**只可新建文件、不可修改已存在的文件**（要改就写进 `inbox/` 投递物）。
**读取工具优先级**：读取文件用内置 Read，搜索用 Grep，找文件用 Glob；批量读取用 Read 批处理。**禁止用命令行读取文本、搜索内容、列举文件或统计行数/体积**。只有运行程序、检查脚本或生成产物才用命令行；调用前说明内置工具无法完成的具体原因。内置工具因权限边界不可用时，不得改用命令行绕过，应暂停该项读取并说明阻塞。
**执行与清理纪律**（每次都遵守）：中间产物只放 **`inbox/scratch/`**（**工作空间内**——`/tmp` 在权限自动允许范围之外，每一次访问都会弹授权，见 [`ai/rules.md`](ai/rules.md) §执行与清理纪律第四十八轮修正）；**只读一律用 Read/Grep/Glob，不起 shell**；流程中不做删除；待删清单累积到 `inbox/cleanup.md`，收尾时用一条命令一次授权；**不可逆操作（拆分、批量改写）前先 `cp` 备份到 `inbox/scratch/`，完成后立即比对体积**；**每轮收尾提交一次 git**。详见 [`ai/rules.md`](ai/rules.md) §执行与清理纪律。
