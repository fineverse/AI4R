# 第七十一轮（2026-09-30）· 传播核查：第 70 轮改的三处前提，别处还有多少旧话

**动因**：第 70 轮改动了三处**前提级事实**（① "论文里的表"≠官方榜；② TOAD/DrivoR 代码已发布 + VLA 三条翻案；③ "有代码的最高"随口径变），但改动只落在少数文件里。**这类"前提级改动"最容易在别处留下与它矛盾的旧表述**——本工作空间的历史上，每一轮传播核查都能抓出若干处。

**做法**：把一个**只读子代理**做全目录扫描（排除 `code/repos/`、`history/rounds-*`、`archive/`——后者按约定"保留当时事实、不追改"），给它四处新事实 + 六类要抓的模式；拿回清单后**由主线程逐条改**。

## 一、扫描结果：**stale 散落各处，不集中在少数文件**

共约 20 处，**最密的三个文件**是 `ideas/sota-plan.md`（6+ 处，§5/§6/§8 未随 §1/§3 更新）、`ideas/preparation.md`、`judgments.md`；其次 `topics/vla/` 三册、若干 README/索引。

## 二、修掉的地方（**全部就地加 `⚠ 第七十一轮`，保留原句**）

| 新事实 | 修掉的位置 |
|---|---|
| **DrivoR 有代码** | `sota-plan.md` **§1 表 DrivoR 行**（原写"官方代码：无 / 无仓库、无 project page"→ **直接错误**）、**§5.1 第 ③ 层**（"54.6（DrivoR，无代码）"）、**§5.2 的拟用话术**（"榜首 55.5 与第二 54.6 都没有代码"——**这段是要写进论文自圆其说里的，最危险**）、`preparation.md §5.1 三句话结论`、`judgments.md B 组第一条`、`topics/diffusion-planner/README.md`（**两处**：为什么关注 + 已知线索表） |
| **论文表 ≠ 官方榜** | `sota-plan.md` **§5.1 第 ④ 层**（"数据集 SOTA 55.5 无代码"→ 补"官方榜榜一是匿名队、DriveFuture 不在榜上"）、`navhard_competitors.md` 的**指针表标题**（"在榜"→"在**论文口径**的榜"）与 DriveFuture 行、`notes/DP-A31-drivefuture.md` **标题行**（"当前 navhard 榜首"）、**六处"navhard 13 行分数格局"的描述**（`state.md` / `index.md` / `preparation.md` ×2 / `topics/diffusion-planner/README.md` / `sources.md L021`）→ 统一改为"**§1.0 官方公开榜 20 行 + §1 论文口径 13 行**" |
| **VLA 三条翻案** | `vla/verification.md §5.3`、`vla/papers.md §2 证据边界`（**两处**）、`vla/verification-2.md §10.4/§11.4`、`judgments-2.md H 组`（"只有项目页"那一档）、`sources.md L015`、`embodied-ai/direction/lineage.md`（DriveMoE"无官方仓库"） |
| **顺带（非本轮新事实）** | `scoring_line.md §四` 待办仍列"TOAD 代码是否发布"→ 已划掉；**`world-model/lineage.md` 两处"DriveFuture 换条件后把 DiffusionDrive 从 24.2 提到 55.5"**——这是第三十五轮就已更正的**误归因**（受控的"换条件"只值 +3.7，+20.9 是 scorer），**两处一直没改** |

## 三、产出

| 类别 | 文件 |
|---|---|
| 修改 | `ideas/sota-plan.md`、`ideas/preparation.md`、`judgments.md`、`judgments-2.md`、`sources.md`、`state.md`、`index.md`、`topics/diffusion-planner/README.md`、`topics/diffusion-planner/papers/navhard_competitors.md`、`topics/diffusion-planner/papers/scoring_line.md`、`topics/diffusion-planner/notes/DP-A31-drivefuture.md`、`topics/vla/papers.md`、`topics/vla/verification.md`、`topics/vla/verification-2.md`、`topics/world-model/lineage.md`、`embodied-ai/direction/lineage.md`、`history.md`（52 → **53 卷**）、`README.md` |
| 未改（按约定） | `history/rounds-*.md` 与 `archive/` 里的旧表述（**历史记录保留当时事实**） |

**验证**：`check_links.py` **全部通过、`exit 0`**。

## 四、方法论

1. **"前提级改动"必须配一次传播核查**——本轮改的三处里，两处（官方榜、代码翻案）都**推翻了此前的承重结论**，而**受影响的位置远多于改动位置**（改了 6 个文件，stale 出现在 16 个文件里）。
2. **最危险的一类是"拟用话术"**——`sota-plan.md §5.2` 那段是**准备写进论文"自圆其说"里的话**，它同时含两处已失效的断言。→ **凡"会被直接抄进论文"的段落，改动时要优先扫。**
3. **子代理只做扫描、主线程做修改**——扫描是机械劳动（可委派、便宜），而"这句到底废没废、改成什么"需要判断（都在主线程）。
4. **顺带抓到一个"更早该改却没改"的**：`world-model/lineage.md` 的 24.2→55.5 误归因，**从第三十五轮起就带着**，此后 36 轮里做过多次传播核查都没扫到（因为它不在"navhard 分数格局"这个关键词下）。→ **传播核查的搜索词要按"结论的语义"设，不能只按"源头的文件名"设。**
