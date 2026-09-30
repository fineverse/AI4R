# 第六十八轮（2026-09-30）· 整合支线投递：navhard 竞品表 + "选优器/候选池"专线

**动因**：用户："处理支线投递"。开轮 pre-flight 发现 `inbox/` 有 1 篇投递（`63a81a6 支线投递：navhard 竞品登记 + "选优器/候选池"专线检索`），并**发现该会话自报了 4 项违规**——本轮一并裁决与整合。

## 一、支线自报的违规：逐条核查后的裁决

| 自报 | 核查 | 裁决 |
|---|---|---|
| **1. 开工前没跑通道 B** | 属实（其首批提交在 12:24，而 `CURRENT.md` 与纪律在 14:19 后的第 60 轮才建） | **纪律生效前的事，不追溯**；但**根因要堵**（见 §五） |
| **2. 以"主线程模式"改了 8 个已存在文件并提交**（`5860b6b`…`84ebbaa`） | **`git merge-base --is-ancestor` 实测：这 8 个提交早已是 `master` 的祖先**（12:24–12:36，即**轮 57/58 的工作**），内容**已在知识树里**、并已被第 58、60 两轮复看过 | **全部保留，不回溯**——它们不是"新出现的问题"，而是**纪律建立之前的历史** |
| **3. 覆盖了 `rounds-59.md`** | 其自称已 `git checkout --` 恢复 | **接受**；现 `rounds-59.md` 完好（本轮复查：卷数、内容一致） |
| **4. 本轮对 `history.md`/`sota-plan.md`/`index.md` 的改动已撤销、改为投递物** | 属实，工作区干净、这三份文件无未提交改动 | **这正是纪律期望的行为**，无需处理 |

> **本节的关键结论**：这 8 个提交**本来就在历史里**——说明"违规"发生在纪律生效之前，**不是本轮新增的破坏**。真正要处理的是**根因**（见 §五）。

## 二、采纳的两份新文件（含必要的修正）

两份均在 `topics/diffusion-planner/papers/`（**新建 = 支线可写**，符合 §一.1）：

| 文件 | 内容 | 整合时做的修正 |
|---|---|---|
| [navhard_competitors.md](../topics/diffusion-planner/papers/navhard_competitors.md) | **DP-C01–C05**（DrivoR / SimScale / GTRS-E / ZTRS / DriveSuprim）+ 8 行"已登记在别处"的指针 | ① **修 6 处死链**（`../../ideas/` → `../../../ideas/` 等：原路径按"在项目根"写，实际在 `papers/` 下）；② **补 ZTRS 的分数冲突注明**（自报 **45.5** vs 本表 **48.1**，原因**待核不可断言**） |
| [scoring_line.md](../topics/diffusion-planner/papers/scoring_line.md) | 方向 B 的文献地基：**§一 4 条（摘要级）** + **§二 17 条（线索级）** | ① **修 4 处死链**；② **证据等级改准**（"§一 = 主线程核验" → "**摘要级（已独立复核）**"）；③ **删掉两条查不实的断言**（BeyondDrive 的"有代码"与"MeanFuser 同组"，摘要均未提） |

**核对过的事实**：navhard_competitors.md 的 13 行分数**逐条与 [sota-plan.md §1](../ideas/sota-plan.md) 吻合**（二级引用，已注明"本表不新增核验"）。

## 三、主线程对 §一 的 4 条做了**独立复核**（投递物是线索不是事实）

投递物称这 4 条"已核验"，但仍属**摘要级**，故本轮**逐条 `WebFetch` 读 arXiv abs 页**：

| 条目 | 复核结果 |
|---|---|
| **TOAD** `2606.07170` | ✅ **逐字吻合**——`NAVSIM-v1 (94.7 PDMS)`、`NAVSIM-v2 (56.3 EPDMS)`、CEM、no retraining、plug-and-play、six base planners、valeoai project page |
| **Vault** `2606.06219` | ✅ **逐字吻合**——94.6 PDMS v1 / 91.2 EPDMS v2、"Under review as a conference paper at **ICLR 2027**"、reward-gated positive pool、学到的 scorer 预测官方分及子指标、"without policy gradients, learned reward models"、v2 = 2026-09-28 |
| **DriveVer** `2607.00399` | ✅ **逐字吻合**——condition-driven clustering + balanced sampling（ego state + nav command）、34M、dual-head（safety confidence + geometric refinement） |
| **BeyondDrive** `2605.19771` | ✅ 数字吻合（**89.7 PDMS on NAVSIMv1**、Latent Transfuser 基线、flow matching 硬负样本、Repulsive Distance Loss）；**但其"有代码"摘要未提** → 已改为"未核" |

> **一处降级**：投递物把 §一 标为"全文级"，**实际只读到摘要** → 已在文件里改为"**摘要级（已独立复核）**"。

## 四、落盘的三处（`index.md` / `sota-plan.md §9.7` / `state.md`）

1. **[index.md](../index.md)** papers 行：加入两份新表的指针（否则它们是孤儿）。
2. **[sota-plan.md §9.7](../ideas/sota-plan.md)**（新节，投递物 §2.2 建议的内容，**经改写**）：把"榜一易主"**明确降为条件待核**、把"§8 依据没错但'做选优'已不新"写成结论，并补一句**TOAD 的"无需重训"恰好打在我们的算力优势上**。
3. **同文件 §2.1 与 §3 各加一处 ⚠ 指针**（指向 §9.7）——**理由**：第四十轮立的"**口径警告必须写进读者会直接抄数字的那张表**"，这里同理：**可能被推翻的前提，要标在前提所在处**，不能只写在 §9.7。
4. **[state.md](../state.md) 待续第 23 项**：4 项待核（**TOAD split / Vault venue / 17 条线索级 / BeyondDrive 两条**），**前两项优先级最高**（可能推翻已写下的判断）。

## 五、根因与规则层补丁（本轮唯一新增规则）

**根因**：这个会话**不知道规则存在**——它 12:24 就在同一个工作树里以"主线程模式"干活，而协作纪律是 14:19 之后才建的。**硬通道（`git log` / `git status`）本可以救它**（第 61 轮就把硬通道定为"底线"），但它**没跑**。

**补丁**：在 [AGENTS.md](../../../AGENTS.md)（**每个会话的入口，AI 启动时按序读取**）里加一行，把"并行会话"这件事**从隐性变显性**——否则下一次"新会话"仍会重演。

> **教训**：纪律写得再细，**若入口文件不提它，新会话就看不见它**。这与第 66/67 轮"规则之间会打架"是同一族问题的另一面：**规则不仅要自洽，还要可被发现**。

## 六、产出

| 类别 | 文件与章节 |
|---|---|
| 采纳 | [navhard_competitors.md](../topics/diffusion-planner/papers/navhard_competitors.md)（修 6 死链 + 补 ZTRS 冲突注明）、[scoring_line.md](../topics/diffusion-planner/papers/scoring_line.md)（修 4 死链 + 证据等级改准 + 删 2 条不实断言） |
| 判断 | [sota-plan.md §9.7](../ideas/sota-plan.md)（新节）+ §2.1/§3 的 ⚠ 指针 |
| 导航 | [index.md](../index.md) papers 行（两份新表入链） |
| 状态 | [state.md](../state.md)（待续**第 23 项** 4 项待核）、[history.md](../history.md)（49 → **50 卷**）、[CURRENT.md](CURRENT.md) |
| 规则 | [AGENTS.md](../../../AGENTS.md)（入口处加"并行会话"一行） |
| 归档 | 投递物移入 `archive/2026-09-30-支线交付-navhard竞品与选优专线.md`（含归档说明与 8 个提交的裁决），`inbox/` 根清空 |
| 中间产物 | 本轮**未产生** |

**验证**：`check_links.py` **全部通过、`exit 0`**（本轮共修 **10 处死链**：两份新文件 6+4）。

## 七、方法论

1. **"自报违规"要先核查再裁决**——本篇自报的第 2 条（8 个提交）经 `git merge-base --is-ancestor` 一查，**它们早就是历史的一部分**（轮 57/58），根本不是新破坏。**若照单全收去"回滚"，等于把已经过两轮复看的成果删掉。**
2. **"已核验"要问是哪一级**——投递物把 4 条标为"全文级"，实际只到摘要；**本轮降级并逐条复核**（数字全对，但级别标错）。**级别标错比数字标错更隐蔽**。
3. **可能推翻前提的发现，要标在"前提所在处"**——TOAD 的 56.3 若为 navhard，受影响的是 **§1 的表**与 **§3 的子榜定义**，所以三处都标（§2.1 / §3 / §9.7），而不是只写在 §9.7。
