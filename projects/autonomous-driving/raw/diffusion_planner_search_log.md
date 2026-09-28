# 扩散规划器检索日志

检索日期：2026-09-22（Asia/Shanghai）  
目标：为"扩散规划器（Diffusion Planner）"方向建立文献基础——主方向自动驾驶端到端规划，次方向具身智能（用于取可迁移机制）。产出综述表、论文表、核心论文笔记、待下载 PDF 清单与官方代码快照。

## 使用的入口

| 来源 | 查询/入口 | 用途 |
|---|---|---|
| arXiv API | `all:"diffusion planner"` | 直接命中同名方向与相邻工作 |
| arXiv API | `abs:"diffusion" AND abs:"planning" AND abs:"autonomous driving"` | 主方向方法论文 |
| arXiv API | `ti:"diffusion" AND abs:"autonomous driving"` | 标题含扩散、摘要涉及驾驶的工作 |
| arXiv API | `all:"diffusion policy"` | 具身侧扩散策略 |
| arXiv API | `ti:"survey" AND abs:"diffusion" AND (abs:"planning" OR abs:"decision making" OR abs:"control")` | 扩散 + 规划/决策综述 |
| arXiv API | `all:"flow matching" AND all:"autonomous driving"` | 流匹配这一主要竞争路线 |
| arXiv API | `ti:"diffusion" AND abs:"trajectory generation"` | 轨迹生成类工作 |
| arXiv API | `abs:"generative" AND abs:"planner" AND abs:"autonomous driving"` | 生成式规划器 |
| arXiv API | `id_list=<77 个候选 ID>` 批量核验 | 逐条核对标题、作者、日期、版本、comments |
| Crossref | `works/{DOI}` | 核验非 arXiv 条目（ICTC、ACM CSUR、Frontiers） |
| OpenAlex | `works?filter=doi:10.48550/arxiv.<id>` | 尝试取引用数（**结果不可用，见下**） |
| 网页检索 | 子代理检索（4 个并行） | 发现候选清单：AD 方法、具身策略、综述缺口、2026 前沿 |
| arXiv HTML / PDF | `arxiv.org/html/<id>`、`arxiv.org/pdf/<id>` + `pdftotext -layout` | 核心论文全文与表格数值核验 |
| GitHub | `git ls-remote` + `git clone --depth 1` | 核验并保存官方代码快照 |

## 工具限制（重要）

1. **Python urllib 访问 arXiv API 返回 406**：即使带 User-Agent 也被拒；本机 `curl` 正常。后续脚本改用 curl 落盘 XML，再用 Python 解析。
2. **OpenAlex 引用数不可用**：本批 77 条中 8 条查不到，且返回的数值明显不完整（Diffuser 仅 62、DiffusionDrive 为 0），与公开量级不符，因此所有表**不设引用数列**，改用"是否被后续工作直接对比"作为影响力线索。
3. **arXiv HTML 的表格单元格会丢失**：HTML→文本转换后表格只剩题注，故部分论文的关键数字需回到 PDF（`pdftotext -layout`）补齐；无法补齐的一律标"未获取"。
4. **子代理汇报只能作为线索**：所有 arXiv ID 均已由本线程用 arXiv API 二次核验（77/77 命中，无编造 ID）；但子代理给出的数字只有标注"全文"的才计入证据，其余按摘要级处理。
5. 本次仍**没有本地运行任何模型**，全部证据止于摘要/全文阅读与代码静态检查。

## 核验记录

- 候选 ID 核验：77 个 ID 全部命中，无失效或编造 ID。核验当日最新版本号已写入论文表"载体与版本"列。
- 重点更正：网络上常被引用的 "Diffusion Planner = arXiv 2501.18809" 是错的（该号是另一主题论文）；真实 ID 为 [2501.15564](https://arxiv.org/abs/2501.15564)，标题为《Diffusion-Based Planning for Autonomous Driving with Flexible Guidance》。
- 术语更正：DiffusionDrive 的 "v3" 指 arXiv 2411.15139 的第三版（CVPR camera-ready），**不存在独立的 DiffusionDriveV3 论文**；同团队后续工作是 DiffusionDriveV2（2512.07745）。
- 边界排除：DiMA（2501.09757）是 MLLM 蒸馏到视觉规划器，**不使用扩散**，仅作对照；Epona/DrivingWorld 等为场景生成；GoMatch 为 flow matching 轨迹预测（非 ego 规划）。

## 纳入判断

1. 生成过程用于规划输出（轨迹、轨迹集合、控制量）的才纳入方法表；只做感知/场景生成/轨迹预测的排除。
2. 综述按"是否直接围绕扩散+规划决策"分级；驾驶侧的生成式规划综述单独成组。
3. 通用决策域（离线 RL）的工作登记在具身表，在驾驶表中只保留指针，避免同一工作两处各写一份。
4. 版本合并：同一工作的 arXiv 多版本只登记一次，取核验当日最新版本。
5. 论文只在"有官方代码"或"被后续工作反复对比"时才进入代码下载清单。

## 第二轮检索（同日，补齐关键全文）

目标：把"约束/引导"这条最可能的 idea 主线的直接竞争者从摘要级推到全文级，并补齐具身奠基论文的设计结论。

| 来源 | 入口 | 产出 |
|---|---|---|
| arXiv PDF + `pdftotext -layout` | 2511.18729、2603.10330、2608.09484、2604.12656、2509.20253、2606.00519 | 约束/引导路线 6 篇全文事实（含公式编号、定理编号、违规率、FPS） |
| arXiv PDF + `pdftotext -layout` | 2205.09991、2211.15657、2208.06193、2305.20081、2401.15443、2405.07503、2407.01812、2409.00588 | 具身奠基 8 篇（引导尺度、步数、频率、延迟、消融） |
| arXiv API | `id_list=2208.06193` | 核验 Diffusion-QL 真实 ID |
| 本线程 grep 复核 | 2603.10330、2511.18729 | 复核最关键的论断（PC-Diffuser 的 CBF 证书与 100%→10.29%；GuideFlow 的 43.0 与"直接施加约束"） |

第二轮的两处更正（已写入论文表与 state.md）：

1. **2305.20081 是 EDP，不是 Diffusion-QL**；Diffusion-QL 的真实 ID 是 [2208.06193](https://arxiv.org/abs/2208.06193)。两篇已分列为 DP-E03（Diffusion-QL）与 DP-E28（EDP）。
2. **PC-Diffuser（2603.10330）已在驾驶域给出认证级硬约束**：逐去噪步 CBF-QP，Thm.1（速度级 CBF 可行性）+ Cor.1（前向不变性），nuPlan all-collision 挑战集碰撞率 100%→10.29%，代价 5× 延迟（约 2 fps）。因此"驾驶域无硬约束"的初判作废，[ideas/preparation.md](../ideas/preparation.md) 的方向 A 已重写。

## 第三轮检索（同日，补齐渠道与预印本）

用户提示：预印本 PDF 由 AI 自行解决，并询问 Semantic Scholar 与预印本网站是否使用。本轮据此补测渠道。

| 渠道 | 状态 | 结果 |
|---|---|---|
| **Semantic Scholar API** | **不可用** | `api.semanticscholar.org` 连续返回 **429 Too Many Requests**（重试 3 次、间隔 8 秒仍 429；2026-09-20 那次也是 429）。共享 IP 未带 API key，无法作为检索与引用数来源 |
| **OpenReview API** | **可用** | `api2.openreview.net/notes/search` 返回 200，可用于查投稿/评审记录（本轮用它确认有以 DiffusionDrive 为基础的相关投稿） |
| **TechRxiv** | 受限 | `techrxiv.org/doi/...` 返回 **403**，预印本 PDF 不可直接取；但 OpenAlex 可确认记录存在（DP-S12） |
| arXiv 预印本 | **可用（主要来源）** | 本轮靠它找到付费墙论文的预印本：**DP-S11（ACM CSUR）→ arXiv 2505.08854**；并发现漏掉的一篇同题综述 **2505.15863（DP-S15）** |
| OpenAlex 引用数 | **可用（方法需修正）** | 见下 |

### 引用数方法的更正（重要）

第二轮结论"OpenAlex 引用数不可用"是**错误判断**：当时只按 `doi:10.48550/arxiv.<id>` 查询，而 OpenAlex 对同一工作常有多条记录，**arXiv 存根记录一律显示 0 引用**。按标题检索取正式版记录后，数值合理且与既有 E2E 综述表一致（S001 = 570、S031 = 20）。

已补齐的快照（详见各表的"影响力快照"节）：DiffusionDrive 81（CVPR）、GoalFlow 28（CVPR）、Diffusion Policy 531（IJRR）、DP3 181、NoMaD 125、π0 236。

同时确认一条限制：**PMLR/ICML 类论文无 DOI，OpenAlex 只有 arXiv 记录，引用数被严重低估**（Diffuser 62、Decision Diffuser 32），因此引用数不用于影响力排序。

### 付费墙条目的预印本核查结果

| 条目 | 是否有预印本 | 处理 |
|---|---|---|
| DP-S11 ACM CSUR 生成式驾驶综述 | ✅ arXiv 2505.08854 | **自行取全文，不需要用户下载** |
| S001 TPAMI 端到端综述 | ✅ arXiv 2306.16927 | **自行取全文** |
| S031 IEEE TITS 扩散+ITS 综述 | ✅ arXiv 2409.15816 | **自行取全文** |
| S034 IEEE Access 扩散+E2E 综述 | ❌ arXiv 未检索到 | 仍需用户下载（IEEE Access 通常开放） |
| DP-S10 ICTC 流匹配机器人综述 | ❌ arXiv 未检索到 | 仍需用户下载（IEEE 付费） |
| DP-S12 TechRxiv 扩散策略综述 | ⚠️ 有记录但页面 403 | 暂不可取 |

## 产出

| 文件 | 内容 |
|---|---|
| [surveys/diffusion_planner_surveys.md](../topics/diffusion-planner/surveys/diffusion_planner_surveys.md) | 综述表（DP-S01…DP-S15 + 交叉引用 + 空白确认 + 引用快照） |
| [papers/diffusion_planner_ad.md](../topics/diffusion-planner/papers/diffusion_planner_ad.md) | 自动驾驶扩散规划器论文表（DP-A01…DP-A34） |
| [papers/diffusion_planner_embodied.md](../../embodied-ai/topics/diffusion-policy/papers/diffusion_planner_embodied.md) | 具身与通用决策表（DP-E01…DP-E28）+ 可迁移机制 + 引用快照 |
| [notes/](../topics/diffusion-planner/notes) | 研究对象核心论文笔记（一篇一文件） |
| [pdfs_pending.md](../pdfs_pending.md) | 待下载 PDF 清单（按优先级） |
| [repositories.md](../code/repositories.md) | 官方代码仓库快照清单（含 commit） |
| [preparation.md](../ideas/preparation.md) | idea 讨论准备材料 |
