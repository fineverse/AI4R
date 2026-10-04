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

- [scripts/](scripts) — 工作空间脚本（`check_links.py` 只读；`normalize_links.py --apply` 会改写链接、`fetch_citations.py` 输出 TSV——用途见各条目）
  - `fetch_citations.py` — 从 Semantic Scholar **批量抓论文元数据**（引用数、影响力引用数、venue 等），**带 429 指数退避重试**——429 间歇出现且与间隔无关（实测连续 4 次 429 后第 5 次成功），故重试是必需的而非可选；输出 TSV 且末列自动写取数日期，凭据自动读 [tools.env](tools.env)。用法 `python3 shared/scripts/fetch_citations.py arXiv:2307.15818 ...`
  - `check_links.py` — 工作空间完整性检查。**逐项清单、跳过目录与豁免规则一律见脚本 docstring，本文件不重复、不写数字**（第六十五轮收敛：此前"十项 / 十一项 / 十二项"在 `脚本 / 本文件 / workflows.md` **三处各写一次**，加一项要改三处，**已实际漏过两次**）。用法 `python3 shared/scripts/check_links.py`；**`exit 0` 才算通过**（任一项不过即 `exit 1`，明细打印在输出里）
  - `normalize_links.py` — 把相对链接规范化为「相对当前文件位置」的标准形式（拆卷/迁移后修链接用）
- [skills/](skills) — 工作空间技能（IDE 无关；每技能一个目录，入口为该目录下的 `SKILL.md`）
  - [zotero/SKILL.md](skills/zotero/SKILL.md) — 操作本地 Zotero Desktop 文献库（搜索、导出 BibTeX、读全文、导入），经本地 API `127.0.0.1:23119`；辅助脚本 `skills/zotero/scripts/zotero.py`
- **工作空间的运行设施**（第四十八轮起，细则见 [ai/rules.md](../ai/rules.md) §执行与清理纪律）：① **已 git**（私有远端 `fineverse/AI4R`，每轮收尾 commit + push）——`code/repos/`（1.6 GB）/ `inbox/scratch/` / `.trae/` 由 [`.gitignore`](../.gitignore) 忽略；② **临时产物根 = `inbox/scratch/`**（工作空间**内**——`/tmp` 虽沙箱可写，但不在权限模式的自动允许范围内，每次访问都会弹授权，故不再使用）；③ **并行会话的同步机制**——见 [ai/rules.md](../ai/rules.md) §支线协作纪律：软通道 [projects/autonomous-driving/history/CURRENT.md](../projects/autonomous-driving/history/CURRENT.md)（事先声明在改什么）+ 硬通道 `git log --oneline -5` / `git status --short`（写文件前必跑）；支线投递物模板见 [ai/templates.md](../ai/templates.md) §支线投递物。

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
| Semantic Scholar 官方 | ✅ **有 key**（2026-09-30 配置，见 [tools.md](tools.md)） | 引用数、影响力引用数、推荐 | `x-api-key` | 免费 key = 1 req/s |
