# E2E-AD 综述检索日志

检索日期：2026-09-20（Asia/Shanghai）  
目标：检索 2024、2025、2026 年自动驾驶端到端模型综述，并补充数据集、仿真、评测、规划、扩散、世界模型、VLM/VLA 和后训练专题。

## 使用的入口

| 来源 | 查询/入口 | 用途 |
|---|---|---|
| arXiv API | `all:"end-to-end autonomous driving" AND (all:survey OR all:review)` | 找到直接 E2E 预印本、摘要、版本号和作者声明 |
| arXiv API | `all:"autonomous driving" AND (all:survey OR all:review)` | 扩展到 VLM、world model、数据/仿真和专题综述 |
| arXiv API | `all:"end-to-end driving"` | 检查标题未使用完整短语的 E2E 工作，排除普通方法论文 |
| OpenAlex | `works?search=...`、按 DOI 查询、按 DOI 批量过滤 | 去重、出版年、载体、引用数、摘要索引 |
| Crossref | `works/{DOI}` | 核验正式 DOI、作者、正式出版日期、卷期/载体和摘要/全文链接 |
| 出版商页面 | IEEE Xplore、Springer、ACM、MDPI、Frontiers、Elsevier、TechRxiv | 补充正式摘要、出版状态、HTML 章节和全文入口 |
| Semantic Scholar | 论文检索 API | 本次触发 429，未作为最终单一证据 |
| Zotero 本地连接器 | 关键词：`end-to-end autonomous driving`、`autonomous driving survey/review`、`VLA autonomous driving` | 检查用户本地文献库；本次没有匹配条目 |

## 纳入判断

1. 标题或摘要直接讨论 E2E-AD 的全栈、规划、训练、后训练或扩散模型，优先纳入。
2. 数据集、仿真、评价、规划、轨迹预测、world model、VLM/VLA 等专题，只有在能直接约束 E2E 研究设计时纳入。
3. 普通方法论文、标题只含 “end-to-end” 但不是综述的条目排除。
4. 同 DOI、同标题的 arXiv/期刊/会议/TechRxiv 版本合并；TechRxiv S019 的 v1/v2/v3 合并为最新 v3。
5. 年份分开记录 `first_publication_year` 和 `formal_publication_year`，避免 DOI 前缀年、online-first 年和卷期年混淆。

## 第二轮：全文可得性核查（2026-09-22）

为梳理 E2E 发展脉络，尝试获取以下综述全文：

| 编号 | 尝试的入口 | 结果 |
|---|---|---|
| S002 | arXiv 2307.04370 PDF | ✅ **成功**，已读全文并写 [笔记](../direction/notes/S002-e2e-ad-survey.md)（含历史路线图、CARLA RC/IS/DS 指标、开放问题） |
| S016 | ACM CSUR（DOI 10.1145/3729420）+ arXiv 检索 | ❌ ACM 403，无 arXiv 预印本 |
| S018 | IEEE IoT-J（DOI 10.1109/JIOT.2025.3635092）+ arXiv 检索 | ❌ IEEE 403，无 arXiv 预印本 |
| S019 | TechRxiv v3 | ❌ Cloudflare 403 |
| S020 | TechRxiv v1 | ❌ 403（仅官方摘要） |
| S035 | MDPI Actuators（DOI 10.3390/act15080427） | ❌ MDPI 403（curl 与 WebFetch 均失败） |

**注意**：检索中另发现同作者（Yunxing Chen）的 [arXiv 2603.16050](https://arxiv.org/abs/2603.16050)《The Era of End-to-End Autonomy》（Electronics 2026），叙事同为 modular→E2E→LDM，但**不是 S035 本体**，不用于代填。

结论：E2E 侧综述的**全文可得性远差于扩散侧**（扩散侧 6 篇全部通过 arXiv 预印本拿到）。因此发展脉络以 S001/S002/S032/S033 全文 + 逐条核实的代表工作时间线为准，见 [lineage/e2e_ad_lineage.md](../direction/lineage.md)。

## 限制

- Consensus 本次返回异常并随后限流；Semantic Scholar 返回 429。
- 公开索引中的引用数会变化，表格仅保存 OpenAlex 2026-09-20 快照。
- 大多数条目尚未保存全文或仓库快照；摘要级证据不能代替全文阅读、代码静态检查或独立复现。
- 出版商页面的摘要、卷期和 online-first 日期可能互不一致；冲突记录在主表备注中，正式引用时需要再次固定版本。
