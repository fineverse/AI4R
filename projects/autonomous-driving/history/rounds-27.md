# 第二十七轮（按「提分成为 SOTA」重排方向，2026-09-24）

**动因**：用户定下选择标准——**「只要能提点成为新 SOTA 就行；创新只要能自圆其说就行；最好是数据集 SOTA，退而求其次本小方向的 SOTA 也可接受。」**

**这条标准推翻了 `preparation.md` §5.0 的排序依据**：§5.0 按"核验后空白大小"排序，把 C/D/E/G 因"已被别人做过"降级；新标准下**"已被别人做过"不再构成淘汰理由**（自圆其说即可），排序依据改为 **① 目标基准上还剩多少分 ② 有没有已量化的机制可直接叠加 ③ 成本**。

## 1. 补上 navhard 的完整分数格局（**本轮最要紧的一项**）

**做法**：此前 `preparation.md §6.1` 的 navhard 列只有 6 行（仅我们收集过的扩散规划器）。本轮从 **DriveFuture Table 1**（已 PDF 逐格核验）取出**完整 12 行对照**，并逐行标注代码状态。

| 方法 | navhard EPDMS | 代码状态（**§5 子代理逐仓库核验后**） |
|---|---|---|
| DriveFuture | **55.5** | **无官方代码** |
| DrivoR | 54.6 | **无代码**（仅承诺 "will be made available"） |
| SimScale | 53.2 | **有代码**，但**不是规划器**（模型无关的 co-training 框架） |
| GTRS-E | 49.4 | **有代码 + checkpoints**（半生成） |
| ZTRS | 48.1 | **有代码 + checkpoint**（非生成式） |
| DiffVLA | 45.0 | **有代码**（纯扩散） |
| **DIVER** | **43.4** | **有代码** |
| DriveSuprim | 42.1 | **有代码 + checkpoints**（非生成式） |
| World4Drive | 34.9 | 有代码 |
| MindDrive | 30.9 | 有代码 |
| GuideFlow | **27.1**（社区口径）/ 43.0（自报） | 有代码但版本错位 |
| DiffusionDrive | 24.2 | 有代码 |
| TransFuser | 23.1 | 有代码（非生成式） |

**三条新结论**（已写入 [judgments.md §B](../judgments.md) 与 [sota-plan.md §1](../ideas/sota-plan.md)）：

1. **"榜上 SOTA ≠ 可复现 SOTA"**：第一名 55.5 **无代码**；第二、三名（54.6 / 53.2）当时**不在我们的论文表里**；**GuideFlow 自报 43.0 与社区口径 27.1 差 15.9 分，且 43.0 不可从发布代码复现** → **navhard 上"有官方代码"的规划器最高是 GTRS-E 49.4（半生成）/ DiffVLA 45.0（纯扩散）**（本节初稿误记为"DIVER 43.4"，**§5 已更正**）。
2. **"高分靠 scorer"从推测升级为同文数字**：DriveFuture 同文的受控消融（**不含 scorer**）是 **34.6**，含 scorer 是 **55.5** → **scorer 的量级 ≈ +20，远大于机制本身（+3.7）**（§2 的 S9 由此从"可能被低估"升级为同文数字）。
3. **navhard 的分数被乘性违规项支配**（PDMS/EPDMS 的 NC 是 **0/1 乘性项**，一次碰撞即把该帧乘 0）→ **降违规的边际收益是非线性的**，与 navtest"分数已挤在 88–91"完全不同。

## 2. 新增「按提分成为 SOTA 重排」（取代 §5.0 的排序依据）

> 本节内容最初写在 `preparation.md §5.1`，**当天因该文件达到 60.8 KB / 64 KB 上限而整块拆出为 [ideas/sota-plan.md](../ideas/sota-plan.md)**（见 §6）。下面按**拆出后**的章节号记录。

- **§1** navhard 完整分数格局（上表）
- **§2** **「小方向 SOTA」的可操作定义 = 用一条真约束切出子榜**——列出 5 个子榜与空位，其中**两个真空位**（navhard 上"实时 ≥10 Hz"与"可复现硬约束"）都落在方向 A；**涨分杠杆最大的一条**（scorer ≈ +20）落在方向 B
- **§4** 7 个方向按「涨分潜力 / 成本 / 自圆其说难度」重排：**B 第一、A 第二**，C/E/G 备选，D 低优先，**F 不涨分**（仅作论文中的一节）
- **§5** **四条**推荐路线：① 主推"**复现 + 拆解 navhard 榜首**"（**四层涨分目标：45.0 纯扩散 SOTA / 49.4 生成式 SOTA / 53.2·54.6 前二 / 55.5 数据集 SOTA**）；② 成本最低的"**只训 scorer**"；③ **套用 SimScale 的 co-training 框架**（§5 子代理核验后新增）；④ 最省力的"**直接打真空位**"

**并修正了 §5 的横切读法**：S24（四轴收益同量级 +3.7~+6.7）在新标准下的推论从"不能按收益排序"改为——**"既然四轴同量级而 scorer 的量级远大于它们，提分的最高杠杆不在'再加一轴机制'，而在'把选优这一环做好'"**。

## 3. 同步更新

- `preparation.md`：文件头 §5 行加"排序依据已被 [sota-plan.md](../ideas/sota-plan.md) 取代"；§5.0 横切读法加 2026-09-24 提示；§6.1 navhard 列加"不完整，完整见 sota-plan.md §1"；**§7.3 整节重写**（改为"路线②→路线①"）、**§7.4 标记基本确定**（NAVSIM v2 `navhard_two_stage` 为主表）、**§7.2 加"你的表态指向要做实验，与'继续探索'不一致"**、§7 抬头写明只剩 7.1 与 7.2 待回；**§5.1 拆出后留 922 字节指针 + 三句话结论**
- `judgments.md`：§B 新增一条（"榜上 SOTA ≠ 可复现 SOTA"）→ **B 组 5 → 6 条，总数 57 → 58**
- `state.md`：待续清单第 6 项改为"用户已定标准 + 已重排"；**新增第 14 项**——补齐 navhard 前几名并核代码状态（**提分路线的直接阻塞**）
- `README.md`：最近动态加两行；"等待用户"改为只列 7.1 / 7.2
- `index.md` / `sources.md` / `context.md` / `diffusion-planner/README.md`：补 `sota-plan.md` 入口与指针

## 4. 产出与状态

- **待用户**：① **7.1 可用 GPU 与预算**（决定走"只训 scorer"还是端到端）② **7.2 是否升级为正式课题**（你的表态指向要做实验）
- **下一步（不依赖用户即可做）**：**待续清单第 14 项**——查 **DrivoR / SimScale / GTRS-E / ZTRS / DiffVLA / DriveSuprim** 的论文与代码状态（**已于本节 §5 完成**）
- ⚠ **体积预警**：`preparation.md` 本轮一度达 **60.8 KB / 64 KB（95%）** → **已按阈值把 §5.1 拆出为 `ideas/sota-plan.md`**（见 §6），拆后 60.8 KB → **53.3 KB**
- 验证：120 个 md、**死链 9 条**（仍全为 `archive/plans/` 已声明项）；**无第一方文档超 64 KB**；`state.md` 55 行、`index.md` 70 行；`judgments.md` **58 条 / A–H 八组，各组声明条数与实际一致**

## 5. 子代理核验 navhard 前几名（**门槛因此重算**）

**动因**：§1 的表里 DrivoR（54.6）与 SimScale（53.2）**不在本工作空间论文表里**，代码状态未知 → 若它们有代码，上面所有门槛要重算。派 1 个 Explore 子代理只读核验 6 个方法（**未克隆任何仓库**，用 WebSearch/WebFetch + GitHub API；缓存 `/tmp/ai4r/navhard_top_probe/`）。

| 方法 | navhard | 论文 / venue | 代码 | 生成式？ |
|---|---|---|---|---|
| DrivoR | 54.6 | arXiv 2601.05083 / CVPR 2026 | **无**（仅承诺 "will be made available"） | **否**（纯 Transformer，proposal 生成 + 评分） |
| SimScale | 53.2 | arXiv 2511.23369 / CVPR 2026 Oral | **有完整代码**（OpenDriveLab，327★ 活跃） | **不是规划器**——模型无关的 sim-real co-training 框架（报告 **+8.6 EPDMS**） |
| GTRS-E | 49.4 | arXiv 2506.06664（CVPR'25 AGC 冠军方案） | **有 + checkpoints**（NVlabs/GTRS，288★） | **半生成**（含扩散生成器，主体是词表评分） |
| ZTRS | 48.1 | arXiv 2510.24108 / ECCV 2026 | **有 + checkpoint**（77★） | **否**（离散词表 + RL/EPO） |
| DiffVLA | 45.0 | arXiv 2505.19381（4 页报告） | **有**（boschresearch/DiffVLA）；⚠ `DiffVLA/DiffVLA` 是空壳 | **是**（纯扩散） |
| DriveSuprim | 42.1 | arXiv 2506.06659 / AAAI 2026 | **有 + checkpoints**（38★） | **否**（coarse-to-fine 词表评分） |

**四条改变了结论的发现**：

1. **navhard 前二都没有代码**（55.5 与 54.6）→ 这个基准的"头部"目前是空的。
2. **"有代码的生成式/扩散规划器"门槛从 43.4（DIVER）升到 49.4（GTRS-E，半生成）/ 45.0（纯扩散 DiffVLA）**——因为 GTRS-E / ZTRS / DiffVLA / DriveSuprim **四家都有可运行的真实现 + checkpoint**。→ 涨分目标改为四层：**45.0 / 49.4 / 53.2 或 54.6 / 55.5**。
3. **SimScale 是"增益工具"而不是对手**——它不是规划器，而是**模型无关的 sim-real co-training 框架**，有代码且活跃更新。→ 新增**路线 ③：套用 SimScale 的框架**（但 +8.6 是它对**某个基线**的报告值，**对更强基线是否成立需先验证**；且它已测过"回归 / 扩散 / 词表"三类，故只能当增益工具、**不能当创新点**）。
4. **副产品：本小方向的对手集比榜面小得多**——12 行里 **DrivoR / ZTRS / DriveSuprim 都是选择/评分式（非生成式）**，GTRS-E 是半生成 → **只有 DriveFuture 与 DiffVLA 是纯生成式规划器**。这是"退而求其次本小方向 SOTA"那条路的直接依据。

**两处需标注的不确定**：① **"GTRS-E" 未在任何论文中定义**——按 NVlabs/GTRS 仓库（DP 25.6 / GTRS-Dense 41.7 / GTRS-Aug 42.1）与挑战赛 49.4 判断，**推测为 GTRS 集成变体**；② **ZTRS 自报 45.5 与 DriveFuture 表记 48.1 不一致**，引用时须注明。

## 6. 体积处理：§5.1 拆出为 `ideas/sota-plan.md`

`preparation.md` 在写入 §5.1 后达 **60.8 KB / 64 KB（95%）**。按 `ai/rules.md` §文件更新的"任何文档 ≤64 KB"阈值，**把 §5.1（8446 字节）整块拆出为 [ideas/sota-plan.md](../ideas/sota-plan.md)**，`preparation.md` 只留 922 字节的指针 + 三句话结论 → **60.8 KB → 53.3 KB**。

**两文件的分工**：`preparation.md` = 讨论用的**前提与方向空间**（S1–S30 / P1–P9 / 7 方向详细描述）；`sota-plan.md` = **冲 SOTA 的作战文件**（navhard 格局与逐行代码状态、子榜门槛、七方向重排、四条推荐路线）。已同步 `index.md`、`state.md`、`README.md`、`judgments.md §B`，并把 `preparation.md` 内 **8 处指向旧 §5.1 的锚点全部改为指向新文件**。

## 7. 交接前：保存应保存的内容 + 整理现有材料

**动因**：用户准备**切换到新会话**，要求"保存一下应该保存的内容，再处理整理一下现有的材料"。派 1 个只读子代理做全库审计（stale 交叉引用 / 孤儿与未索引项 / `/tmp` 缓存是否已落盘 / `archive/` 组织）。

### 7.1 抢救两个维护脚本（**清理前必做**）

`/tmp/ai4r/` 里有两个**每轮都在用**的校验脚本，清理前落到工作空间，否则要重写：新建 `shared/scripts/`，放入

| 文件 | 来源 | 改动 |
|---|---|---|
| [shared/scripts/check_links.py](../../../shared/scripts/check_links.py) | `/tmp/ai4r/check_links.py`（46 行） | `SKIP_DIRS` 加入 **`archive`** 与 **`.trae`**，docstring 写明理由 |
| [shared/scripts/normalize_links.py](../../../shared/scripts/normalize_links.py) | `/tmp/ai4r/normalize_links.py`（54 行） | 原样复制（拆卷/迁移后修相对链接层级用，已在两轮用过） |

**为什么排除 `archive`**：该目录按约定"默认不加载"，其中历史方案记的是重构**前**的路径（`projects/diffusiondrive/` 等），8 条死链属预期且文件头已声明。**若计入，这 8 条会永久淹没真正的新死链** → 排除后"死链 0"才重新有信号意义。**为什么排除 `.trae`**：那是 IDE 产物（计划文件、skill），不属于工作空间知识树，其正文按仓库根书写路径，与检查器"相对当前文件"的口径不同。

→ **死链从 9 条降到 0 条**（退出码 0），且不再需要"9 条已声明项"这个长期豁免。

### 7.2 修 16 处 stale（**本轮最要紧的一项**）

审计发现 16 处与事实不符的陈述。**三处最要紧**：

1. **`sources.md` 的 L015 / L017 两个索引条目落后一整轮**——L015 记 VLA"**19 篇** / 已读全文 **13 篇** / **8 篇**源码核验 / 剩 **6 篇摘要级**"，实际是 **28 篇 / 28 篇全部全文级 / 13 篇源码核验 / 摘要级 0**；L017 记世界模型"**9 篇**已读全文 / **5 篇**源码核验 / 补录**已解决 6/8** 剩 NeMo 与 OccVAR"，实际是 **24/24 全文级 / 14 篇源码核验 / 补录 8/8 已解决**。→ **新会话若按索引读会得到错信息**。
2. **`state.md:8`（"当前阶段"，新会话第一眼）** 仍写"**有官方代码的最高只有 DIVER 43.4**"并指向已迁走的 `preparation.md §5.1`——**这是第二十七轮自己漏改的**（§5 的子代理核验已把它更正为 45.0 / 49.4）。
3. **`shared/index.md:12`** 写 `domain/` "当前仅 CCF 目录"，但 CCF 早已上提为 `shared/ccf/`，该目录**现在是空的**。

其余 13 处：`history.md:19`（同 2）、`rounds-27.md` 三处（初稿的 43.4 与"三层目标"→ 已就地更正为四层）、`state.md:32`（§5.1 → `sota-plan.md §4`）、`state.md:21/:23`（`transfer.md` 同一表两行重复）、`project.md:37`（二十六 → **二十七轮**）、`pdfs_pending.md:60/:65`（36 → **37** 个仓库、1.6 → **1.65 GB**、"32 个"加"当时"限定）、`index.md:12`（8 → **9 卷**）、`shared/workspace-design.md:42/:43`（7 → **9 卷**、57 → **58 条**）、`README.md:31`（57 → **58 条**、`state.md` 54 → **55 行**）、`topics/diffusion-planner/README.md:28`（**两份→三份**脉络、**三层级→四层级**）、`inbox/cleanup.md:86`（`code/repos` "无空目录" → 更正为**有 3 个未初始化的 submodule**）。

### 7.3 补 5 处索引与指针

`shared/index.md`（`domain/` 改为"当前为空，保留占位" + 新增 **§工作空间维护 → `scripts/`**）、`index.md`（补 `experiments/results/`）、`topics/diffusion-planner/README.md`（补 `sota-plan.md` 入口）、`context.md`（补 `sota-plan.md §5` 指针）、`sources.md`（**新增 L021 行**登记 `sota-plan.md`）。

### 7.4 执行清理（用户一次授权）

`rm -rf /tmp/ai4r /tmp/ai4r-*`（**877 MB / 205 条目 + 47 个散件**）+ `rmdir` 两个空壳目录（`projects/diffusiondrive` 的 11 个空目录、`shared/domain`）。

**用 `rmdir` 而非 `rm -rf` 删空壳目录**——若非空（说明迁移有遗漏）会报错，而不是静默删掉内容。

**复查**：`/tmp` 下 `ai4r*` 残留 **0**；两个空壳目录均不存在；全库空目录只剩 `code/repos/` 下 **3 个未初始化 submodule** 与 3 个**有意占位**（`experiments/records`、`experiments/results`、`writing`）。**`inbox/cleanup.md` 的待删表已清空**，过程记入其「执行记录」。

### 7.5 交接形态（用户已定）

**不新建"接手说明"文件**——新会话靠现有链条接手：`AGENTS.md` 启动链（8 个入口的"什么时候读"）→ `README.md`（两项目 + 等待用户）→ `state.md`（当前阶段 + 待续清单 14 项 + 判断边界分组索引）→ [ideas/sota-plan.md](../ideas/sota-plan.md)（决策核心）。

**验证**：`check_links.py` **死链 0 / 退出码 0**、所有 `index.md`/`state.md` ≤100 行；无第一方文档超 64 KB；孤儿 **0**；清理项全部生效。
