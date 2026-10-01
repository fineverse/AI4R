# 第七十九轮（2026-10-01）· 全工作空间修复（A–E 组）

**性质**：非专题研究轮——把同日全工作空间只读巡查（[archive/plans/2026-10-01-工作空间巡查-优化清单.md](../../../archive/plans/2026-10-01-工作空间巡查-优化清单.md)）的 A–E 组逐条落地。动因：用户先指示"先不执行、只落一份巡查清单"，随后改令"**全修复，我不怕麻烦**"→ 计划（`.trae/documents/2026-10-01-全工作空间修复计划.md`）批准后一次做完。

**基线**：巡查时 `check_links.py` **exit 0**、git 干净——**优化点全在机器检查盲区**。

## 一、做法（六批次）

| 批次 | 内容 |
|---|---|
| 0 安全网 | `git archive HEAD` 全量备份到 `inbox/scratch/r79_backup/`（249 文件 / 3.1 MB）；`CURRENT.md` 写「在改」声明 |
| 1 脚本与工具（A1 + C + E2） | **`normalize_links.py --apply` 数据破坏修复**：`code_span_re.sub('', line)` 会把行内代码整段删掉后写回 → 改**哨兵遮蔽**（夹具回归测试通过：行内代码保留、真链接正常）；`SKIP_DIRS` 补 `.vscode`；`fetch_citations.py` 加返回形状校验（堵 `zip` 静默截断）；`parse_ccf_2026.py` 删未用/重复导入；`workflows.md` 三处 `ls inbox` → Glob；`AGENTS.md`/`lessons.md` 统一 `/tmp` 措辞（沙箱可写 ≠ 权限自动允许）；`templates.md` 删重复分册句；`rules.md` §证据等级补综述表窄词表例外；`workflows.md`「不写数字」限定为"不写总数" |
| 2 A 组真错误（A2–A11） | protocol 死引用「待续项 17」+ 过时 HF 结论；**WM 表 14→13**（WM-02 无代码却计入）；WM README「24.2→55.5」旧事实；**GR00T N1 机制（扩散→流匹配）**（AD/具身两处 + CSV）；**MindDrive 交叉引用 VLA-12→VLA-16**（两文件）；sota-plan 53.2 自相矛盾（§5.1③/§7.5③ → 定案）；DrivoR 首句加更正；扩散侧 lineage 仓库数 36→37/1.6→1.65 GB；**AD 扩散表 CSV 重刷**（代码/证据状态列 30+ 行，按 ID 精确改，含 A09 均值化更正、A16 口径与证据）；**π0 venue 联网核验**（arXiv `comments` "Published in RSS 2025" → DP-E 表仅 arXiv→RSS'25、T4→T1，md + CSV） |
| 3 B 组单一事实源 | 去重口径 = **指定权威源、其余压成指针**（用户定）。已确认 preparation / recombination-map **本就以指针为主**（非"四处全文重复"），无需大改；**sota-plan §7.7.4 瘦身为指针**（数值表归 benchmarks，同时把 §10 新增的复现声明/里程碑行抵消，出预警带）；时间戳清账（recombination-map、sources）；index §7 口径、VLA 表头戳、WM README §4.1 指针、AD↔VLA 同篇证据等级（DP-A27/28/30 → 全文，md + CSV）、具身升全文清单改指针、具身"同名不同内容"原则指向 project.md |
| 4 检查器增强 | 修／加：CSV↔md ID 口径对称（md 端加词边界）；**第 5 项标题正则收紧**；**第 14 项 shared/index.md 完整性**；**第 15 项投递物已入 git**；**第 16 项轮次 tag**；`import subprocess` |
| 5 D 组结构 | **archive 16 件头部完全重排为统一样式**（用户裁决；H1 + `> **归档说明**（…）`，正文一字不改）；VLA 证据等级统一（L2 说法删除，DriveMoE/ExploreVLA 归 L3）；具身 index/state 补第 78 轮 |

## 二、更正与发现清单（事实级）

1. **`normalize_links.py --apply` 会删光行内代码**——第 78 轮"移植豁免堵数据风险"的改动**实际引入了数据破坏**（把"删空代码跨度"的结果写回文件）。夹具测试先证伪旧行为、再证新行为。
2. **subagent 报告需复核**：第 79 轮巡查清单里「决策文件四处全文重复」**部分不成立**（preparation 早已是指针）；「具身接口层级统一」经评估**代价远大于收益**。
3. **π0 venue 是错的**：DP-E 表记"仅 arXiv / T4"，而 arXiv `comments` 明写 "Published in RSS 2025" → 改为 RSS'25 / T1（三渠道之一即为权威）。
4. **WM 代码核验计数 14→13**：WM-02 无官方代码，被误计入。
5. **GR00T N1 机制**：VLA 表记"扩散"，DP-E 表（有代码核验）记"流匹配非纯扩散"——统一为流匹配，并同步 §2「扩散/流匹配」计数（5+2 → 4+3）。

## 三、已知未做（有意，含两处偏离计划）

1. **中文命名锚点检查（计划 C 组 E.6）不落盘**：实现后产生 **37 处误报**（中文锚与后文无分隔符，如 `§轮次收尾第 7 步`），违反"永久报警必被无视"的教训 → 撤除，改由第 5 项标题正则收紧覆盖。已记入脚本 docstring「务实放弃项」。
2. **具身三专题接口层级统一（计划 D）不执行**：改名 `papers/x.md`→`papers.md` 波及 **56 处**（含 **14 处历史卷**与 raw/archive），等于**改写历史记录**，收益（同构）< 代价 → 保留现状，改为在 README 注明两种布局并存。
3. **judgments.md 去重保守处理**：`judgments.md` 按 [AGENTS.md](../../../AGENTS.md) 是"**完整论证与代码出处**"的权威存储，其 B 组条目（L40–L45）是判断本身的论证而非"重复副本" → **不改写**（去重只落在 sota-plan 侧的 §7.7.4）。

## 四、产出

| 类别 | 文件 |
|---|---|
| 脚本 | [normalize_links.py](../../../shared/scripts/normalize_links.py)（哨兵遮蔽 + SKIP_DIRS）、[check_links.py](../../../shared/scripts/check_links.py)（第 14–16 项、口径对称、标题正则收紧）、[fetch_citations.py](../../../shared/scripts/fetch_citations.py)、[parse_ccf_2026.py](../../../shared/ccf/scripts/parse_ccf_2026.py) |
| 规则 | [ai/rules.md](../../../ai/rules.md)（综述表例外）、[ai/workflows.md](../../../ai/workflows.md)（Glob inbox、不写总数）、[ai/templates.md](../../../ai/templates.md)、[AGENTS.md](../../../AGENTS.md)、[ai/lessons.md](../../../ai/lessons.md) |
| 内容（AD） | protocol、sota-plan、preparation、recombination-map、sources、index、world-model 四文件、vla/papers、diffusion-planner（lineage + papers md/CSV）、navhard_competitors |
| 内容（具身） | DP-E 表 md/CSV、vla/papers（机制 + §1.1 计数）、direction/lineage、两 topics README、state、index |
| 归档 | archive 16 件头部统一 |
| 巡查清单 | [archive/plans/2026-10-01-工作空间巡查-优化清单.md](../../../archive/plans/2026-10-01-工作空间巡查-优化清单.md)（状态改"第 79 轮起执行"） |

## 五、状态同步

| 位置 | 改动 |
|---|---|
| state.md | 当前阶段改为本轮摘要；更新时间 79 轮 |
| history.md | 索引加 79 行；卷数 60 → **61** |
| index.md / README.md | README 最近动态 + 指针表加 79 行 |
| topics README | world-model / vla / diffusion-planner 状态字段按需同步 |
| embodied history | 补第 79 条目（第 11 轮） |
| CURRENT.md | 「在改」区清空 + 页脚 79 轮 |
| 验证 | `check_links.py` **exit 0**（含第 14–16 项新检查）；normalize dry-run 死链 0；sota-plan 出预警带 |
