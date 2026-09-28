# 共享资料索引

## 研究偏好

- [研究偏好与资源](profile.md)
- [AI 辅助科研流程与协作需求](research-workflow.md)
- [工作空间设计决策](workspace-design.md)
- [文献质量分档](literature-quality.md) — 判断文献值不值得读（T1–T5 + 领域白名单）；与 [ai/rules.md](../ai/rules.md) 的「证据等级」（读到了什么程度）配对使用

## 领域知识

- 领域公共知识：**无独立目录**——CCF 目录在 [ccf/](ccf)；基准与评价协议按项目存放于 [autonomous-driving/direction/benchmarks.md](../projects/autonomous-driving/direction/benchmarks.md)。（原 `shared/domain/` 空壳目录已于 2026-09-24 删除）
- [ccf/](ccf) — CCF 推荐国际学术会议和期刊目录（2026 正式版）结构化数据（681 条，含 A/B/C 评级）；解析脚本在 [ccf/scripts/](ccf/scripts)

## 工作空间维护

- [scripts/](scripts) — 维护脚本（只读工具，不修改被检查的文件）
  - `check_links.py` — **十项检查**：死链 / `index.md`·`state.md` 行数预算 / **表格单元格数**（应为表头列数；已处理 `\|` 转义并跳过 ``` 围栏代码块）/ **引用可达性**（孤儿文件 + 只被 `sources.md` 引用的"弱引用"）/ **章节引用可达性**（链接文字里的 `§X` 必须在目标文件里；错册或不存在都报）/ **笔记的「对本项目的意义」节**（`notes/*.md` 必写）/ **小方向 README 的必写 4 节**（`topics/<x>/README.md` 必写）/ **判断条数一致性**（`judgments*.md` 的实际 bullet 数 = 节标题声明 = `judgments.md` 索引表 = `state.md` 索引表与总条数）/ **声明计数 vs 权威源**（**两个项目**的"N 篇 / N 个 / N 条" = 目录数 / 论文表编号数 / 笔记文件数 / 章节行数；规则登记在脚本的 `COUNT_RULES`）/ **CSV 与 markdown 表的 ID 一致性**（4 对；双表示时 CSV 是权威源，两边 ID 集合须完全相同；对子登记在 `CSV_ID_PAIRS`）。跳过 `archive`、`.trae`、`scratch`，弱引用检查另跳过 `raw/`，链接扫描另跳过行内代码跨度，理由见脚本内注释
  - `normalize_links.py` — 把相对链接规范化为「相对当前文件位置」的标准形式（拆卷/迁移后修链接用）
- **工作空间的运行设施**（第四十八轮起，细则见 [ai/rules.md](../ai/rules.md) §执行与清理纪律）：① **已 git**——每轮收尾提交一次，`code/repos/`（1.6 GB）/ `inbox/scratch/` / `.trae/` 由 [`.gitignore`](../.gitignore) 忽略；② **临时产物根 = `inbox/scratch/`**（工作空间**内**——`/tmp` 在权限自动允许范围之外，每次访问都会弹授权，故不再使用）。

## 工具说明

- Zotero：通过插件访问本地文献库
- arXiv API / arXiv PDF：公开文献检索与全文获取（**主要来源**）；注意 Python urllib 访问 arXiv API 会被 406 拒绝，需用 curl
- OpenAlex：按标题检索取**正式版记录**才有真实引用数；按 `doi:10.48550/arxiv.<id>` 查到的是 arXiv 存根记录，引用数一律为 0（2026-09-22 核验）
- Crossref：正式 DOI、卷期与出版年核验；TechRxiv 等平台可能未收录
- Semantic Scholar API：**当前不可用**，连续返回 429（2026-09-20、2026-09-22 两次核验），不作为证据来源
- OpenReview API（`api2.openreview.net`）：**可用**，用于查投稿与评审记录（2026-09-22 核验）
- TechRxiv：页面返回 403，PDF 不可直接取（2026-09-22 核验）
- `pdftotext -layout`：PDF 表格数值抽取（arXiv HTML 转换会丢表格单元格）
- Consensus MCP：已注册，但搜索工具返回类型不兼容（2026-09-20 核验，重试仍复现），当前不可用，其结果不作为证据
