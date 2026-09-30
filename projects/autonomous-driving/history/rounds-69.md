# 第六十九轮（2026-09-30）· TOAD 的 split 核实：navhard 榜一易主

**动因**：第六十八轮整合支线投递时立下最高优先级待核项——**TOAD（arXiv 2606.07170）报 v2 56.3 EPDMS，但摘要未指明 split**；若为 navhard，则 `sota-plan.md` §1 的榜一与 §3 的子榜辩护前提都要改。本轮把它核到**论文正文**。

## 一、核实过程与结果

读 **arXiv HTML 版**（`arxiv.org/html/2606.07170v1`）正文，两处原文定案：

| 位置 | 原文 | 说明 |
|---|---|---|
| §4.1 Benchmarks | "We evaluate on NAVSIM-v1 (navtest split) and NAVSIM-v2 (**navhard-two-stage split**)" | **split 明写** |
| §4.2 Main results | "the six planners start almost 20 EPDMS points apart (**34.7 to 54.6**) but all land between **49.0 and 56.3** after search"；"DrivoR, already the strongest, gains +3.1% to reach **56.3 EPDMS**, outperforming the strongest learned method (**DriveFuture**, 55.5) … only 0.3 behind the privileged PDM-Closed (56.6)" | **56.3 是 navhard 的数** |

→ **结论：56.3 就是 navhard。** 这一条**同时删掉了 §9.7 原有的条件句**（"若为 navhard 则…"）。

## 二、推翻/更新了哪些已写下的东西

| 对象 | 原状 | 现状 |
|---|---|---|
| `sota-plan.md` §1 榜一 | DriveFuture **55.5** | **TOAD + DrivoR 56.3**（只比用 GT 感知的 PDM-Closed 56.6 低 0.3） |
| `sota-plan.md` §2.1「榜上头部拿不到代码」 | 榜一 55.5 无代码 | **结论仍成立**——TOAD 代码**未发布**（"will be made publicly available"）→ **榜一换了名字，性质没变** |
| `sota-plan.md` §3「有代码的任意方法 = SimScale 53.2」 | 唯一一行 | **持有者仍是 53.2**（TOAD 无代码），但**"榜上最高"（56.3）与"有代码的最高"（53.2）自此不是同一个数**——已在行内显式写明 |
| `sota-plan.md` §9.7 第 ① 条 | 条件推断 + ⚠⚠ 待核 | **改为已核实**，并把"头部被压平"写成新发现 |
| `scoring_line.md` TOAD 行 / §三.2 / §四 | 待核 | 同步改为已核 |

**⚠ 一个必须写清的量级**：TOAD **把头部压平**了——六个 base planner 原本 **34.7–54.6**（差近 20 分），测试时搜索后**全部落在 49.0–56.3**（**最弱的 iPad +43.6%，最强的 DrivoR 只 +3.1%**）。**"base planner 本身好不好"这件事被大幅削弱**，而 TOAD **无需重训、只用公开 ckpt**。

## 三、新落盘：`judgments.md` D 组新增 1 条（**65 → 66**）

新增条目 **"做选优"已被"测试时搜索"这条路线占据，而它把 navhard 榜一推高到 56.3**，写进 **D 组**（锚点 · 词表 · 选优，**11 → 12 条**）。**三条硬事实 + 两条本项目含义**：

- 硬事实：① split = navhard-two-stage；② 头部被压平（34.7–54.6 → 49.0–56.3）；③ navhard 上"拿 progress 换安全"（原文）。
- 含义：① **方向 B 的叙事必须改**——TOAD 不是"从池子里挑一条"，而是"**用 scorer 当 reward 搜出池子里没有的轨迹**"，**比"压缩选优损失"更强** → **区分点只能落在"监督信号"上**；② **它打在我们的算力护城河上**——"无需重训 + 用别人的公开 ckpt"意味着**任何人都能叠出这个涨幅**，而我们把"冻结 + 小规模"当优势。
- **两条限定**：**(a)** TOAD 代码未发布 → **56.3 当前不可复现**；**(b)** 上述数字来自**论文正文（全文级）但未经独立复现**。

计数按第四节同步（节标题、`judgments.md` 索引表、`state.md` 索引表与总条数四处）。

## 四、产出

| 类别 | 文件与章节 |
|---|---|
| 判断 | [judgments.md](../judgments.md) **D 组新增第 12 条**（+ 分组索引表 D 行 11→12） |
| 作战文件 | [sota-plan.md](../ideas/sota-plan.md)：**§9.7 第 ① 条改为已核实** + §2.1 与 §3 两处更正 + §9.7 证据边界行 |
| 专线表 | [scoring_line.md](../topics/diffusion-planner/papers/scoring_line.md)：TOAD 行、证据等级行、§三.2、§四 同步 |
| 状态 | [state.md](../state.md)：**判断 65 → 66**、D 行 11 → 12、**待续第 23 项第 ① 解掉并新增 ⑤⑥**（TOAD 代码发布 / 56.3 未独立复现）、[history.md](../history.md)（50 → **51 卷**）、[index.md](../index.md)、[CURRENT.md](CURRENT.md) |
| 中间产物 | arXiv HTML 由 `WebFetch` 直接取回（**未落盘**） |

**验证**：`check_links.py` **全部通过、`exit 0`**（含「判断条数一致性」——四处计数同步后一致）。

## 五、方法论

1. **摘要级不够时，"再取一层"往往很便宜**——第六十八轮只能从摘要得到"56.3"、split 未知，本轮一次 `WebFetch` 读 HTML 正文即定案。**代价一次抓取，收益是删掉一条可能推翻前提的不确定性**。→ **"待核项"应优先做"能一次定案"的那些**。
2. **推翻前提的发现，要同时改"前提"和"结论"两处**——本轮改了 §1/§2.1/§3（前提所在处）与 §9.7/判断条目（结论所在处），**因为只改一处会留下互相矛盾的两种说法**（这正是本工作空间反复出现的 stale）。
3. **"榜上最高"与"有代码的最高"是两个数，不能混用**——TOAD 让这两者首次分离（56.3 vs 53.2）。**引用"最高"时必须写明限定词**。
4. **意外收获比原问题更重要**：本轮原本只想回答"是不是 navhard"，却拿到**"头部被压平"**——它直接削弱了"把 base planner 做好"这条叙事，**对方向选择的影响大于 split 本身**。
