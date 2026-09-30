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

- [scripts/](scripts) — 工作空间脚本（都只读、不修改被检查的文件）
  - `fetch_citations.py` — 从 Semantic Scholar **批量抓论文元数据**（引用数、影响力引用数、venue 等），**带 429 指数退避重试**——429 间歇出现且与间隔无关（实测连续 4 次 429 后第 5 次成功），故重试是必需的而非可选；输出 TSV 且末列自动写取数日期，凭据自动读 [tools.env](tools.env)。用法 `python3 shared/scripts/fetch_citations.py arXiv:2307.15818 ...`
  - `check_links.py` — **十项检查**：死链 / `index.md`·`state.md` 行数预算 / **表格单元格数**（应为表头列数；已处理 `\|` 转义并跳过 ``` 围栏代码块）/ **引用可达性**（孤儿文件 + 只被 `sources.md` 引用的"弱引用"）/ **章节引用可达性**（链接文字里的 `§X` 必须在目标文件里；错册或不存在都报）/ **笔记的「对本项目的意义」节**（`notes/*.md` 必写）/ **小方向 README 的必写 4 节**（`topics/<x>/README.md` 必写）/ **判断条数一致性**（`judgments*.md` 的实际 bullet 数 = 节标题声明 = `judgments.md` 索引表 = `state.md` 索引表与总条数）/ **声明计数 vs 权威源**（**两个项目**的"N 篇 / N 个 / N 条" = 目录数 / 论文表编号数 / 笔记文件数 / 章节行数；规则登记在脚本的 `COUNT_RULES`）/ **CSV 与 markdown 表的 ID 一致性**（4 对；双表示时 CSV 是权威源，两边 ID 集合须完全相同；对子登记在 `CSV_ID_PAIRS`）。跳过 `archive`、`.trae`、`scratch`，弱引用检查另跳过 `raw/`，链接扫描另跳过行内代码跨度，理由见脚本内注释
  - `normalize_links.py` — 把相对链接规范化为「相对当前文件位置」的标准形式（拆卷/迁移后修链接用）
- **工作空间的运行设施**（第四十八轮起，细则见 [ai/rules.md](../ai/rules.md) §执行与清理纪律）：① **已 git**——每轮收尾提交一次，`code/repos/`（1.6 GB）/ `inbox/scratch/` / `.trae/` 由 [`.gitignore`](../.gitignore) 忽略；② **临时产物根 = `inbox/scratch/`**（工作空间**内**——`/tmp` 在权限自动允许范围之外，每次访问都会弹授权，故不再使用）。

## 工具与凭据

- [工具与凭据](tools.md) — 各工具的**调用方式、额度、成本与已知坑**（含 Ai4Scholar 付费计费规则、Consensus 字段含义、Semantic Scholar 429 成因、GitHub 代理配置）
- **凭据**：[tools.env](tools.env)（已 gitignore，不进版本历史）。用前 `source shared/tools.env`。其中 `AI4SCHOLAR_API_KEY` 系**用户付费积分**，调用前须查余额并说明用途，禁止探测式调用

**论文检索工具速查**（细节与坑见 [tools.md](tools.md)）

| 工具 | 状态 | 最适合 | 认证 | 成本 |
|---|---|---|---|---|
| arXiv API | ✅ **主要来源** | 预印本检索与全文 | 无 | 免费 |
| OpenAlex | ✅ | 引用数、正式版记录 | 无 | 免费 |
| Crossref | ✅ | DOI、卷期、出版年 | 无 | 免费 |
| Consensus REST | ✅ | 语义检索、结论摘要 | `x-api-key` | 30 次/月 |
| Ai4Scholar | ✅ **付费** | 批量、引用网络、Google Scholar | `Bearer` | 积分制 |
| Semantic Scholar 官方 | ⚠️ 需 key | 影响力引用数、推荐 | `x-api-key` | 免费 key = 1 req/s |
