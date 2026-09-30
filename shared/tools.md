# 工具与凭据

更新时间：2026-09-29
用途：记录外部工具的**调用方式、额度、成本与已知坑**。索引见 [index.md](index.md)；文献质量判据另见 [literature-quality.md](literature-quality.md)。

## 凭据

所有 API key 存于 [tools.env](tools.env)（**已 gitignore，不进版本历史**）。使用前：

```bash
source /home/verse/dev/AI4R/shared/tools.env
```

| 变量 | 服务 | 性质 |
|---|---|---|
| `CONSENSUS_API_KEY` | Consensus | 免费档（30 次/月） |
| `AI4SCHOLAR_API_KEY` | Ai4Scholar | **付费积分**，用前必查余额 |
| `GITHUB_TOKEN` | GitHub API | fine-grained PAT，仅公开仓库只读；5000/小时 |

## 论文检索工具总表

| 工具 | 状态 | 最适合 | 认证 | 成本 / 限额 |
|---|---|---|---|---|
| arXiv API | ✅ **主要来源** | 预印本检索与全文 | 无 | 免费 |
| OpenAlex | ✅ | 引用数、正式版记录 | 无 | 免费 |
| Crossref | ✅ | DOI、卷期、出版年 | 无 | 免费 |
| Consensus REST | ✅ | 语义检索、结论摘要 | `x-api-key` | 30 次/月（免费档） |
| Ai4Scholar | ✅ **付费** | 批量、引用网络、Google Scholar、PubMed | `Bearer` | 积分制，1 次≈1–2 积分 |
| Semantic Scholar 官方 | ⚠️ 需 key | 影响力引用数、推荐 | `x-api-key` | 无 key 不可用；免费 key = 1 req/s |
| Semantic Scholar MCP / Consensus MCP | ❌ MCP 通道不可用 | — | — | 改用对应 REST API |

## 各工具细节

### arXiv API（主要来源）
- Python `urllib` 访问会被 **406 拒绝**，须用 `curl`
- 无限流问题，是核验 arXiv 论文时最稳的通道

### OpenAlex
- 按标题检索取**正式版记录**才有真实引用数
- 按 `doi:10.48550/arxiv.<id>` 查到的是 arXiv 存根记录，**引用数一律为 0**

### Semantic Scholar 官方 API
- **未认证 = 不可用**。429 是**全局共享池饱和**（非本地配额），**等待无效**——实测隔 15 秒重试 3 次全 429，单条 GET 连续 7 次仅 1 次穿透
- 唯一解法：申请[免费 key](https://www.semanticscholar.org/product/api)（1 req/s 独占清额度）
- 若只为绕开限流，也可走 Ai4Scholar 代理（它自带高配 key），但需付费

### Consensus REST API
- 端点：`GET https://api.consensus.app/v1/search?query=<关键词>`
- 认证：请求头 `x-api-key`（**不是** `Authorization: Bearer`，后者返回 401）
- 返回：固定 **20 条**/次；顶层 `results` `page` `page_size` `is_end`；用 `page` 翻页（`limit`/`take`/`per_page` **均无效**）
- 单条 16 字段：`title` `abstract` `authors` `doi` `journal_name` `volume` `pages` `publish_year` `publish_date` `url` `citation_count` `influential_citation_count` `study_type` `sjr_best_quartile` `is_preprint` `takeaway`
- **可信且对本工作空间最有用**：`sjr_best_quartile`（期刊分区）、`study_type`、`is_preprint` —— 直接对应 [文献质量分档](literature-quality.md) 的 T1–T5 判据；`takeaway` 是论文结论的一句话，可加速论文表填行
- `include_full_text_chunks=true` 返回 0 条（付费档功能，未开通）
- 额度：Free 30 次/月、Pro 500、Deep 2000；**API 与 MCP 共用同一配额**

### Ai4Scholar（付费代理层）

**性质**：不是自建数据库，是 Semantic Scholar / PubMed / Google Scholar / Google Patents 的**转售代理**。它的价值在于自带高配 key，把 S2 的 429 变成稳定服务。

**调用规范**
- Base URL：`https://ai4scholar.net/graph/v1`
- 认证：`Authorization: Bearer <key>`（**不是** `x-api-key`——那是 S2 官方写法）
- **免费端点**：`GET https://ai4scholar.net/api/credits` 查余额，**不扣费**
- **对账头**：每个计费响应返回 `x-credits-charged`（本次扣费）、`x-credits-remaining`（余额）
- **失败不扣费**：上游报错或超时自动退还

**常用端点**（结构镜像 S2）

| 端点 | 方法 | 说明 |
|---|---|---|
| `/graph/v1/paper/search` | GET | 关键词检索 |
| `/graph/v1/paper/search/bulk` | GET | 批量检索，最多 1000 条 |
| `/graph/v1/paper/{id}` | GET | 论文详情（支持 DOI / arXiv ID / PMID） |
| `/graph/v1/paper/batch` | POST | **批量详情，最多 500 篇** |
| `/graph/v1/paper/{id}/citations` | GET | 被引 |
| `/graph/v1/paper/{id}/references` | GET | 参考文献 |
| `/graph/v1/author/search` | GET | 作者检索（含 h-index） |
| `/graph/v1/author/{id}/papers` | GET | 作者论文列表 |

**成本纪律（重要）**
- 这是**用户付费购买的额度**。使用前先查余额；调用前应能说明用途与预计次数；**禁止探测式调用**（拿它试参数、试端点）
- 实测计费：`paper/batch` 一次查 **7 篇 = 2 积分**。批量显著优于逐篇
- 余额：**487 积分**（2026-09-29 本次调用后）

**数据质量坑（2026-09-29 实测）**
- `publicationTypes` **不可信**：7 篇全部返回 `['JournalArticle']`，但其中含 CoRL、RSS 会议论文
- `isOpenAccess` **有误**：OpenVLA（arXiv 2406.09246）、Octo 标注为「否」，但它们是公开 arXiv 论文
- → 判会议/期刊**只看 `venue`**；判预印本用 **`venue == 'arXiv.org'`**；需要可靠的分区/预印本字段时改用 Consensus 的 `sjr_best_quartile` / `is_preprint`

### 其他
- OpenReview API（`api2.openreview.net`）：可用，查投稿与评审记录
- TechRxiv：页面 403，PDF 不可直接取
- Zotero：通过插件访问本地文献库
- `pdftotext -layout`：PDF 表格数值抽取（arXiv HTML 转换会丢表格单元格）

## 网络访问

**GitHub**：Clash Verge 开「系统代理」，端口 `127.0.0.1:7897`；shell 需自行导出（Clash Verge 的系统代理只改 GNOME 设置，**不导出到 shell**）：

```bash
export https_proxy=http://127.0.0.1:7897
export http_proxy=http://127.0.0.1:7897
```

设置后 `git clone`、`curl`、`pip`、`huggingface_hub` 全部自动走代理。`codeload` 走代理 2.97 MB/s、直连 3.97 MB/s，可选 `no_proxy=codeload.github.com` 排除。

**不要开「虚拟网卡模式」（TUN）**：它强制 fake-ip DNS，把 `github.com` 解析成 `198.18.0.1`——**正是 TUN 网卡自己的地址**，连它等于连本地网卡，443 无监听 → 秒拒。症状是「连接被拒绝」或 TLS 中途断开。关掉 TUN 后该 DNS 分配仍可能残留，故以环境变量为准。

**绕行方案（不依赖 `github.com`）**：
- 取仓库：`curl -L -o repo.tar.gz https://api.github.com/repos/{owner}/{repo}/tarball/{ref}`（302 到 codeload，实测 2.3 MB/s）
- 列 Release 资产：`https://api.github.com/repos/{owner}/{repo}/releases`

**GitHub API token**（`GITHUB_TOKEN`，见 [tools.env](tools.env)）：fine-grained，仅 `Contents: Read-only` + 自动的 `Metadata: Read-only`，账户权限全空。**认证后 5000/小时**（未认证 60/小时），**搜索 30/分钟**（未认证 10/分钟）。请求头用 `Authorization: Bearer $GITHUB_TOKEN`。
- ⚠ **只用 API 时不需要代理**（`api.github.com` 直连可达）；**`git clone` 才需要走代理**（`github.com` 直连不通，见上）
- ⚠ 该 token 曾以明文出现在对话记录中，建议轮换（低风险：仅公开仓库只读、无写权限）
- 曾出现 `/repos/*` 稳定返回 500，2026-09-29 复查已恢复，判断为 GitHub 侧瞬时故障或权限传播延迟，**非 token 配置问题**
