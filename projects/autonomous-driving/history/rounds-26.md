# 第二十六轮（消化信息 + 工作空间与工作流迭代，为 idea 讨论做准备，2026-09-23）

**目标**：用户下达"整理消化信息，迭代工作空间和工作流，为讨论 idea 做准备"。

**做法**：先派 1 个 Explore 子代理对 8 个工作流/设计文档做"与实际做法是否一致"的只读审计（要求逐条给 `文件:行号`），主线程同时通读 idea 讨论的核心交付物 `preparation.md`。审计结果与本轮改动如下。

## 1. 审计发现的四类问题

| 类别 | 具体问题 |
|---|---|
| **过时** | `AGENTS.md` 仍用"当前**激活项目**"单数口径（现为两个平级项目）；`ai/templates.md` 记"39 篇笔记"（实为 47）；`shared/workspace-design.md` 记"36 个仓库快照"（实为 37）；`rules.md` 与 `workspace-design.md` 都写"README 约 30 行"（实测 46 行）；`research-workflow.md` 停在 2026-09-22，未反映两级树与两项目 |
| **重复定义** | 「执行与清理纪律」三处（`rules.md` / `workspace-design.md` / `AGENTS.md`）；「领域—专题两级树」两处；「证据等级」三处（`rules.md` / `research-workflow.md` / `templates.md`）；「README 维护纪律」两处；「state/index 角色」两处；「lineage 规范」两处 |
| **规则缺口**（`ai/` 层全无） | ① **子代理纪律**（只散在项目文件里）② 文献检索流程未接 T1–T5 质量分档 ③ **代码核验的 L1/L2/L3 三级**未定义 ④ **64 KB 体积阈值**只在 `workspace-design.md` ⑤ **拆分安全要求**未进 `rules.md` |
| **启动链失效** | 不再有"激活项目"；实际入口为 README（两平级项目）→ 各项目 `project.md` / `state.md` / `index.md`，且 `autonomous-driving` 另有 `context.md` / `judgments.md` / `history.md`，`AGENTS.md` 完全未提 |

## 2. 工作流迭代（`ai/` 与 `shared/`）

**`ai/rules.md`**（改动最大）：
- 证据等级表标注为**唯一定义处**，新增 **"代码静态检查"再分三级**——**L1 逐文件核验 / L2 仓库存在性 / L3 API + `raw` 取证（未克隆）**，并写明各级"能支持什么结论、不能支持什么"；配套记下 **L3 的字节数必须与 trees API 的 `size` 逐一对齐**、以及已知克隆会失败的情形（大仓 / LFS / tarball 固定字节截断——实测 Flow Planner 在约 4.5 MB 处稳定截断）
- 新增 **venue 三渠道并行核验**（`comments` + OpenAlex 按标题 + Crossref 按 DOI），并记下"按标题在 arXiv 找不到时先怀疑**根本没有 arXiv 版本**"（实测 NeMo = ECCV'24 会议版、OccVAR = 已撤稿投稿）
- 新增 **§子代理纪律**（7 条）：**只出线索不出结论、不得写文档、多轮探索一律委派、交付物内容主线程自己写、必须缓存、不克隆大仓、全库 Grep 排除 `code/repos/`**
- **§文件更新**补入三条**尺寸阈值**（`index`/`state` ≤100 行、**任何文档 ≤64 KB**、笔记一篇一文件），并写明 `state.md` 的两种超限形态
- **§执行与清理纪律**新增第 8 条：**不可逆操作前先 `cp` 备份 + 完成后验证体积守恒与死链**，附上一轮事故记录；并指出 **`history/` 与 `judgments.md` 是唯一可用的重建来源**

**`ai/workflows.md`**（整篇重写）：
- 文献检索补入 **T1–T5 质量分档**（预印本口径）、venue 三渠道、**边界外清单要定期复核**（实测 15 条复核里 9 条应升级）
- 新增 **§论文精读**：**必须先区分受控消融与榜上对比**（附误读教训）
- 代码脉络梳理补入 **L1/L2/L3 标注**与**七类"名字 ≠ 实际"陷阱**，并强调**负面结论同等重要**
- 新增 **§Idea 讨论准备**：固定 `preparation.md` 的 7 节结构 + 三条纪律（每条方向必写重合风险、收益量级要横向对齐、不自动升级为选定方向）

**`shared/workspace-design.md`**：把「README 维护纪律」「文件尺寸预算」「执行与清理纪律」改为**指针 + 执行台账**（规则本体归 `rules.md`），运行纪律第 3 条现在只记"何时拆了什么"与两个踩过的坑；仓库数 36 → **37**。

**`shared/research-workflow.md`**：证据等级与 state/index 角色改为指针；更新时间与落地状态更新到 2026-09-23。

**`ai/templates.md`**：笔记数 39 → **47**；笔记模板的「代码」字段加 **L1/L2/L3 标注位**、「证据等级」字段改为指向 `rules.md`。

**`AGENTS.md`**（重写）：去掉"激活项目"单数口径，改为**两个平级项目**；新增**入口文件表**（8 个入口各写"什么时候读"），补齐 `context.md` / `judgments.md` / `history.md` / `sources.md`；清理纪律处补入"不可逆操作前先备份"。

## 3. 消化信息：`preparation.md` 去重与重构（**本轮最有价值的一项**）

**问题**：`preparation.md` §2（21.2 KB、25 条长 bullet）与上一轮刚拆出的 `judgments.md`（52 KB、57 条）**高度重叠**——同一批代码事实在两处各写一份，违反运行纪律第 1 条「单一事实源」。且 §2 每行长数千字，**无法作为讨论时的依据清单**。

**改法**：§2 整节重写为**「设计前提清单」**——**S1–S30，一行一条**，固定三列「**设计前提 + 量化依据 + 对设计的约束**」，按 6 组分类（生成机制 / 选择机制 / 约束与可行性 / 条件与世界模型 / **跨轴结论** / 资源与口径）；**完整论证与 `文件:行号` 一律指向 `judgments.md` 与三份代码脉络**，本节不重复。

| 指标 | 改前 | 改后 |
|---|---|---|
| §2 体积 | 21.2 KB | **11.0 KB** |
| 全文体积 | 51.0 KB | **42.5 KB** |
| 是否可整读讨论 | 否（每行数千字） | **是**（一行一条，S 编号可被 §5 引用） |

**同时新增两处"讨论用"结构**：
1. **文件头的「本文件怎么用」表**——7 节各写"讨论时的用法"，并明确**逐轮更新日志移出本文件**（归 `history.md`）
2. **§5 开头的「方向 → 依据对照」表**——7 个方向各标「创新位置 / 依据的 S 与 P 编号 / 重合风险 / 一句话现状」，并附**横切读法**：**四条机制轴的受控收益全在 +3.7 ~ +6.7，没有一轴远大于其他轴 → 选方向不要以"哪一轴收益更大"为依据**

**新提炼的一条结论（写入 §5 横切读法）**：S24（四轴同量级）的直接含义是**方向选择不能靠"收益更大"来排序**，只能靠**可行性、可测性、资源**——这把 §5 的讨论从"哪个方向涨分多"转成"哪个方向在资源约束下可被验证"。

## 4. 补上 §5 最缺的一块：**七方向横向比较**（讨论的决策依据）

**问题**：§5 逐个列了 7 个方向的五要素，但**没有把它们放在同一组轴上比**——讨论时无法据以决策。

**改法**：新增 **§5.0**，用五条轴做横向表：**核验后空白大小 / 能否用现有资源验证 / 最小实验成本 / 失败退路 / 证据基础（代码级）**。轴值全部来自本文件的 S/P 事实与代码核验结论，**不含猜测**。

**由此得出的四条初步判断（明确标注"供讨论，不是决定"）**：
1. **只有 A（约束注入层级与实时化）和 B（候选选择/评分器）同时满足"空白真实 + 现有资源可验证 + 失败有退路"**；C/D/E/G 的空白在核验后都被压小；F 的空白真实但**贡献门槛最高**（公认开放问题里"提出批评"不值钱）
2. **A 与 B 的差别在"要不要训练"**：B 只需冻结生成器训评分器，**是唯一能在算力受限时先跑起来的方向**；A 直击一个已量化的缺口（S12：实时方案无硬约束、有硬约束约 2 fps）
3. **A 与 B 不互斥**：B 的评分器可给 A 提供"约束是否被违反"的独立判据 → **算力紧张时"先 B 探路、再做 A"是可行路径**
4. **一个尚未被覆盖的交叉点**：**"拆解收益来源"**——四轴各自 +3~+7 但**没人做过"把两项收益拆开"的受控实验**（四轴同量级本身就是证据）→ **不构成独立方向，但可作为 A 或 B 实验设计里的一节**

## 5. 具身侧项目（`embodied-ai`）的结构对齐

派第二个子代理对次项目做结构审计，发现 6 处缺陷并全部修掉：

| 缺陷 | 修法 |
|---|---|
| **`project.md` 与 `state.md` 直接矛盾**：`project.md` 写"`direction/lineage.md` 只有骨架；`topics/vla/`、`topics/world-model/` 尚无资料"，而 `state.md` 记第二十五轮**已写成初稿并各建 14 篇表** | 按实际状态更正，并写明"此前未随上一轮更新" |
| **「6 个仓库跨项目共用」在 4 处各写一份**（`state.md` 两处 + `project.md` + `sources.md`） | 统一为**指向 [workspace-design.md](../../../shared/workspace-design.md) §当前落地状态**的指针 |
| **逐轮记录内联在 `state.md`**（「已完成」节） | 新建 [embodied-ai/history.md](../../embodied-ai/history.md)，把第七、八、二十五轮迁出；`state.md` 的「下一步」改为与主项目一致的「**待续清单**」表格 |
| **证据词表非标准**：`diffusion_planner_embodied.md` 用 `未获取`（不在权威档位里） | 改为指向 [ai/rules.md](../../../ai/rules.md) §证据等级，并补 **L1/L2/L3** 标注要求；**查实 `openpi` 已克隆在 `code/repos/`，故 DP-E19 的核验确为 L1**，同表补记 DP-E08/E09/E10/E17 亦为 L1 |
| `index.md` 未列 `history.md` | 补入入口 |
| `state.md` 的判断边界与 `direction/lineage.md` 的证据边界重叠 | `state.md` 只留结论，细节指向 `lineage.md` |

**审计同时确认的两件好事**：`embodied-ai` **无文件超 64 KB**（最大 26.6 KB）、**全量链接 0 条失效**。

## 6. 产出与状态

- 改动的文件：`AGENTS.md`、`ai/rules.md`、`ai/workflows.md`、`ai/templates.md`、`shared/workspace-design.md`、`shared/research-workflow.md`、`ideas/preparation.md`（7 个，第一批）；`embodied-ai` 的 `project.md`、`state.md`、`index.md`、`sources.md`、`topics/diffusion-policy/papers/diffusion_planner_embodied.md` + **新建 `embodied-ai/history.md`**（6 个，第二批）；`judgments.md`、`state.md`、`ideas/preparation.md` + 3 处 stale 引用（第三批，见 §7）；**数字一致性抽查**再改 `project.md`、`context.md`、`topics/diffusion-planner/README.md`、`topics/vla/README.md`、`topics/world-model/README.md`、`sources.md`、`topics/diffusion-planner/transfer.md`、`code/traces/diffusion_planner_code_traces-2.md`、`ai/workflows.md`（9 个，见 §8）
- 备份：改动前 `preparation.md`、`transfer.md`（第一批）与 `judgments.md`、`state.md`（第三批）已 `cp` 到 `/tmp/ai4r/backup-20260923/`（按新纪律第 8 条）
- 验证（全部完成后复跑）：**119 个 md、死链 9 条**（全为 `archive/plans/` 已声明项）、**孤儿 0**；**全库无第一方文档超 64 KB**；两项目的 `state.md`/`index.md` 均在 100 行内（主项目 `state.md` 100 → **54 行**）
- **待用户**：[preparation.md §7](../ideas/preparation.md) 的四项（资源、课题定位、起点方向、评价口径）——**第三批已给建议默认值，认可即可回"按默认走"**；§5.0 已给出初步排序供讨论起点

## 7. 第三批：判断边界的可导航化 + §7 的可拍板化

**问题（两处）**：
1. `judgments.md` 的 57 条判断**平铺无分组**（53 KB），而 `state.md` 的"索引"是**从这 57 条机械抽出的首段粗体**——既是重复副本，又有 6 条抽出的标签信息量不足（如 `- 未选定正式课题`、`- 只完成克隆`、`- 四轮`），且 `state.md` 恰好卡在 **100/100 行**、无余量。
2. `preparation.md` §7 只有 4 条**纯提问**——讨论时无法快速收敛，等于把决策成本全推给用户。

**改法**：
- **`judgments.md` 按主题分为 A–H 八组**（**只重排、未改一字**）：A 证据边界与工作空间状态（6）/ B 指标与基准口径（5）/ C "生成式·扩散"这个词的真伪（6）/ D 锚点·词表·选优（9）/ E RL 与可行性（7）/ F 逐方法的代码级结论（12）/ G 非生成式基线与特权信息（6）/ H VLA 与具身侧（6）；文件头加**分组索引表**（组 / 主题 / 条数 / 覆盖范围）。
- **`state.md` 的索引从 57 行压到 8 行**（同一张分组表），**删掉与 `judgments.md` 的重复副本** → `state.md` 100 行 → **54 行**、14.6 KB → **12.1 KB**，重新有了余量。
- **`preparation.md` §7 改为「需要你拍板的四项」**：每项给**选项表 + 建议默认值 + "这一项会改变什么"**——① 资源（默认单卡 ≤24 GB）② 课题定位（默认暂不立项）③ 起点方向（默认先 B 后 A）④ 评价口径（默认只用 NAVSIM、navhard 为主）。用户认可默认值只需回一句"按默认走"。
- 同步修 3 处 stale 引用（`AGENTS.md` / `ai/rules.md` / `shared/workspace-design.md` 的"只留一行摘要索引" → "分组索引"），并把 `preparation.md` 文件头指向的轮次记录从 `rounds-25.md` 更正为 `rounds-26.md`。
- **孤儿文件审计**：全库 115 个第一方 md（不含 `archive/` 与 `code/repos/`）中查出 **1 个真孤儿**——`embodied-ai/topics/diffusion-policy/README.md`（另两个 topic README 被 `lineage.md` 显式链接，故未漏）→ 具身侧 `index.md` 的三个小方向行改为**指向各 `README.md`**（与主项目 index 的写法一致）。修后**孤儿 0**。

**安全性**（按 `rules.md` 执行与清理纪律第 8 条）：改动前 `judgments.md` 与 `state.md` 已 `cp` 到 `/tmp/ai4r/backup-20260923/`；重排脚本自证 **57 条 bullet 字节级集合不变**（仅顺序变化），体积差 **+2465 字节 = 新增的分组标题与索引表**。

**本轮至此结束**：三条线（工作流迭代、具身侧结构对齐、判断边界可导航化 + §7 可拍板化）全部收尾；`preparation.md` 已可作为讨论依据（**§2 前提清单 → §5.0 横向比较 → §5 方向 → §7 拍板**）。

## 8. 第三批（续）：跨文档数字一致性抽查（**查出 7 处 stale**）

**做法**：对 `37/36 个仓库`、`47/39 篇笔记`、`52/28/24/14 篇`、`已完成 N 轮`、`只有骨架 / 尚无资料` 等计数做全库 Grep，逐条比对权威源（`state.md` / `code/repositories.md` / `sources.md`）。

| 文件 | 原写法 | 更正为 |
|---|---|---|
| [project.md](../project.md) | "`topics/vla/` 与 `topics/world-model/` 目前**只有骨架，尚无资料**" | 两表**已全部读成全文**（28 + 24，其中 27 篇另有代码级核验）——与 `state.md` **直接矛盾** |
| project.md | "文献调研已完成**十六轮**…**36 个**仓库快照（1.6 GB）…逐个核验后发现 7 个无代码" | 该段**降级为指针**（"进度、待续清单、判断边界一律以 `state.md` 为准"），只留一句话现状 |
| project.md | "当前**激活**的研究案例" | "探索案例"（"激活项目"口径已在第一批废除） |
| [topics/diffusion-planner/README.md](../topics/diffusion-planner/README.md) | "**36 个**仓库快照" ×2 | **37 个** |
| [topics/vla/README.md](../topics/vla/README.md) | "已完成**两轮**…论文表 **18 篇**"；"下一轮待补：LMDrive / CarLLaVA / SimLingo / RAG-Driver 的 venue 核验" | **四轮**、**28 篇全部全文级 + 13 篇源码核验**；边界外清单**已复核完毕**（15 条 → 9 条升为 VLA-20–28） |
| [topics/world-model/README.md](../topics/world-model/README.md) | "已完成**三轮**…已读全文小节（**9 篇**）"；"下一轮待补：NeMo / OccVAR 的 arXiv ID 仍无解；剩 **15 篇**摘要级" | **四轮**、**24 篇全部全文级 + 14 篇源码核验**；arXiv ID **8/8 已解决**、**摘要级 0 篇** |
| [judgments-2.md §H](../judgments-2.md)（第三十六轮分册后指向） | "已读全文 **20 篇**、**10 篇**源码级核验" | **28 篇**、**13 篇**，并指向 `vla/papers.md §14` 的逐篇清单 |
| [sources.md](../sources.md) L007 | "代码仓库获取状态（**36 个**已全部获取）" | **37 个**，并指向 C002 |

另把 3 处 **"36 个"的历史陈述**加上"当时 36 个 / 第二十一轮起为 37 个"的限定（[judgments-2.md §F](../judgments-2.md)（第三十六轮分册后指向）、[transfer.md §1.4](../topics/diffusion-planner/transfer.md)、[diffusion_planner_code_traces-2.md §K](../code/traces/diffusion_planner_code_traces-2.md)），避免与当前快照数混淆。

**另有一处不是计数、而是"清单已完成但未打勾"**：[context.md](../context.md) 的「决策前必须补齐的信息」5 条里有 3 条**早已核完**（commit 已固定、NAVSIM/nuScenes 口径已代码级核验、同条件后续工作的代码与性能来源已核完），却仍以"待办"形式列出，且文件头还写着"当前**激活**的探索案例"（2026-09-22 版）→ 改为**带状态列的表格**，只剩"可用 GPU / 存储 / 预算"一项待用户。

**根因**：`project.md` 与三个 topic `README.md` 的"状态"字段是**手写的当前态摘要**，而每轮实际更新的是 `state.md` 与 `history/`——两者之间没有联动，于是逐轮漂移。**处理**：① `project.md` 的"当前状态"降级为指针；② topic `README.md` 保留状态字段（它们是入口，需要一眼看到进度）；③ **把"轮次收尾"写成 [ai/workflows.md](../../../ai/workflows.md) §轮次收尾**，列出必须同步的 7 个位置与计数类事实的权威源。
