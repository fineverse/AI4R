# 第四十五轮（2026-09-24）· 换 basename 的拆册，留下 17 处悬空章节引用

**动因**：第四十四轮把"声明的计数"整条线纳入了机器检查。顺着"还有什么引用没被机器核过"往下问，落到一个此前只被**部分**覆盖的维度：**正文里写 `§X` 指向某文件，那个文件里到底有没有这一节**。

现有的第五项「分册引用归属」只认 **`X.md` ↔ `X-2.md` 这种同 basename 的册对**。于是本轮先做了一次**全库普查**（366 条带 `§` 的文件内链接），不看册对、只看"目标文件里有没有这一节"。

## 结论

### 1. 查出 17 处悬空引用，全是同一类

**根因**：`vla/papers.md` 与 `world-model/papers.md` 的 **§4 之后**（已读全文与代码核验）在早前轮次被拆到了 **`verification.md` / `verification-2.md`**——**换了 basename**。引用却仍写着 `papers.md §5…§14`，而这两份论文表现在**只有 §1–§4**。

→ **册对逻辑完全看不见**（它只在 `papers.md` 与一个不存在的 `papers-2.md` 之间找），所以这 17 处从拆册那天起就一直是坏的。

| 原引用 | 正确去处 | 处数 |
|---|---|---|
| `vla/papers.md §5 / §5、§6 / §6 / §7 / §7.1 / §7.2 / §7.3 / §8` | `vla/verification.md`（§5–§8） | 10 |
| `vla/papers.md §10 / §11–§14` | `vla/verification-2.md`（§9–§14） | 3 |
| `world-model/papers.md §5` | `world-model/verification.md`（§5） | 4 |

**分布在 6 个文件**：`state.md`（1）、`code/repositories.md`（6）、`code/traces/world_model_code_traces.md`（1）、`history/rounds-18-23.md`（3）、`history/rounds-24c.md`（1）、`history/rounds-24a.md`（5）。

**历史记录也修了**（这是第二次修历史文件的链接——第三十轮修过 `rounds-24a.md` 的三处）：修的是**指针**、不是内容，轮次记录里"当时看到了什么"一字未动。

**做法**：先 `cp` 六个文件到 `/tmp/ai4r/fix_stale_sec_refs_45/`，再用脚本逐条 `assert` 旧链接存在后替换**链接文字与链接目标**（不改任何正文），17 处全部命中。

### 2. 把第五项从"错册"扩成"可达性"

原规则只覆盖"章节在册兄弟里"，新规则覆盖**三种情形**：

| 情形 | 现在会报什么 |
|---|---|
| `§X` 在目标文件里 | 通过 |
| `§X` 不在目标、但在它的册兄弟里 | **错册**（原来只有这一种） |
| `§X` 两边都没有 | **目标文件里没有这一节**（新增） |

实现要点：`§7.2` 只看**主节号** `7`（避免把子节引用误判）；`sections()` 加缓存（366 条引用不必重复读文件）；死链由第一项报、这里跳过。

**负向测试**（两条路径各测一次）：把 `[C003 §M](…code_traces-2.md)` 改成 `§A`（§A 只存在于第一册）→ 报 **3 处错册**（同一链接文字出现在 3 行）；把 `[vla/verification.md §5、§6]` 改成 `§Z、§6` → 报 **1 处"没有这一节"**；均改回后 0 处。

### 3. 一句方法论

**这是同一类坑的第三次**：第二十八轮 C003 的 §I–§P（52 处）、第三十轮 C005 的 §K–§M（13 处）、本轮 17 处。前两次的教训是"**拆册后要改引用**"，本轮的教训更细一层：**"拆册"不只有 `X → X + X-2` 一种形态；`X → Y + Y-2`（换 basename）时，任何只认"册对"的检查都会失明。** 检查的判据应当落在**"§X 在不在目标文件里"**这个更本质的问题上，而不是"它在不在册兄弟里"。

## 产出

| 类别 | 文件与章节 |
|---|---|
| 悬空引用 | **17 处已改**，涉及 [state.md](../state.md)、[code/repositories.md](../code/repositories.md)（6 处）、[world_model_code_traces.md](../code/traces/world_model_code_traces.md)、[rounds-18-23.md](rounds-18-23.md)（3 处）、[rounds-24c.md](rounds-24c.md)、[rounds-24a.md](rounds-24a.md)（5 处） |
| 维护脚本 | [shared/scripts/check_links.py](../../../shared/scripts/check_links.py) **第五项由"分册引用归属"扩为"章节引用可达性"**（新增"两边都没有"这一情形 + `sections()` 缓存 + `§7.2` 只看主节号）；文件头同步 |
| 工作流 | [ai/workflows.md](../../../ai/workflows.md) §轮次收尾第 7 条：第五项改名 + 补"**换 basename 拆册尤其要跑**"；[shared/index.md](../../../shared/index.md) 脚本说明同步 |
| 状态 / 索引 | [state.md](../state.md)（当前阶段、卷数 26→**27**）、[history.md](../history.md)（**27 卷**）、[index.md](../index.md)、[README.md](../../../README.md) |
| 中间产物 | `/tmp/ai4r/fix_stale_sec_refs_45.py`、`/tmp/ai4r/fix_stale_sec_refs_45/`（6 个改写前备份）、`/tmp/ai4r/repos_bak_45.md`（负向测试备份）→ 已登记 [inbox/cleanup.md](../../../inbox/cleanup.md) |

**验证**：`check_links.py` **九项全绿**（135 个 md 文件，退出码 0）；**带 `§` 的链接引用 366 条，不可达 0 条**；改写前后逐文件比对，**正文零改动**（脚本只替换 `[文字](目标)` 这一对）。

**一句话**：**第五项检查原先只会问"这一节在不在册兄弟里"，而 `papers.md` 的 §5–§14 是被拆到 `verification.md`（换了 basename）的——册对逻辑完全看不见，17 处引用坏了很久没人知道。改成问"这一节在不在目标文件里"，这类坑就再也藏不住。**
