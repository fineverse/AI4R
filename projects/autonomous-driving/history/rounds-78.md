# 第七十八轮（2026-10-01）· 规则体系优化（服务 CCF-A）

**性质**：非专题研究轮——继第 77 轮"修写错的地方"之后，本轮修**体系本身**。动因：用户要求"从头到尾审查规则/方法/约定/流程，看是否合理、数据是否满足、找优化点"，5 个只读审查智能体报告 + 主线程核实后，用户定调"**大胆优化，不怕麻烦，一切服务于更好发表 CCF-A**"→ 计划（`.trae/documents/2026-10-01-规则体系优化计划.md`）批准后六批次一次做完。

**审查总判断**：规则体系功能健全（13 项机器检查全绿）但已到**补丁饱和临界点**——rules.md 24 处轮次标注四层叠压、开工认知负载 ~3.5–4 万字且约半数是事故叙事；两份决策文件距 64 KiB 硬线仅 280/617 B 且排队待写入 ≥3 项；巡查仍查出 1 处同文件自相矛盾、2 处幽灵引用、1 处 L 级错标。

## 一、做法（六批次）

| 批次 | 内容 |
|---|---|
| A 真错误 ×6 | sota-plan §6 的 DrivoR 行（"无代码需盯"与 §1.0"有代码"直接矛盾，71 轮漏改）；templates 分册约定三处失实（**world-model/verification-2.md 幽灵引用**——该文件不存在；WM 侧实为 §4–§6；traces 实为 §A–§J 跳 §F）；context.md"只剩资源一项" vs 表格"✅已回"矛盾；DP-E05 核验级别 **L2→L3**（C003 §P.2 有逐文件证据，同批 E06 正确标 L3）；证据词表漂移两处（"未获取""目录"档 → 并入六级词表）；A16 DIVER T 档补回"TAPMI 疑笔误"待核痕迹 + rules 加 **L2 级别 vs L2 误差撞名消歧** |
| B 脚本 ×5 | **normalize_links.py 移植 strip_code + 围栏豁免**（堵 `--apply` 改写示例文本的数据风险；修后 dry-run 顺手抓出本轮新写的 2 处错层死链——脚本先于人工验证了自己）；check_links **行数预算进 exit**（原只打印，state 涨到 150 行仍全绿）；**第 13 项认字母后缀**（`rounds-78a.md` 按主干 78 归组）；**README"索引 + N 卷"入 COUNT_RULES**；末尾加**阻断/提示分级汇总行**（exit 语义不变） |
| C 瘦身 | **sota-plan 65,256 → 61,250 B、preparation 64,919 → 60,201 B，双双退出预警带**：§6 整节指针化（盯/补清单归 state 待续）、§7.6.1 证据压缩（完整取证在 C003）、§7.7.4 子指标表移除（benchmarks 为权威源）、§9.7 四行表压为极简+指针（scoring_line 为权威源）、preparation §5.0 判断收拢 / §5.1 三层更正收拢为一句 / 方向 A/B 卡片压缩；**零和编辑纪律**入 rules（预警带内新增 N 字节须同步删 ≥N）；待续 #27 落点改道（结论进 recombination-map/scoring_line，不进 sota-plan） |
| D 同步与时间戳 | **收尾同步位 7→9 处**（⑧ shared/index+tools 当前态、⑨ CURRENT 页脚；"改具身文件 → embodied history 含本轮条目"入附注）；**执行序钉死**：9（整合）→1–6（同步）→7（检查）→8（提交），不重排编号只钉顺序；**8 处时间戳停更清账**（judgments 两册/preparation/pdfs_pending/benchmarks/vla/wm papers/DP-A/DP-S——只改"戳旧内容新"的正向）；embodied history 头部对齐"每轮一卷"新约；index"占位 vs 未建"两说补注；周扫"开轮纪律"压为 pre-flight 指针 |
| E 拆双层 | **新建 [ai/lessons.md](../../../ai/lessons.md)（24 条教训、六节）**：收纳 rules/workflows 全部起因/事故/演化叙事（覆盖事故、/tmp 弹窗史、计数漂移五案、同步漏做四案、支线三代废案、写作陷阱）；**rules.md 25,499 → 18,432 B（−28%）**——节名清单与 32 条条号**逐一核对全保留**（拆前基线备份 `inbox/scratch/r78_baseline/`），叙事原位换一行指针；workflows 收尾步骤同法（方法学动因句保留、事故案例转 lessons）；**AGENTS.md 修 2 处漂移**（"不得绕道命令行"统一、"比对体积"→"两项验证"）并给三段摘要加"以 rules 为准"声明——**不压成纯指针**（AGENTS 是 always_applied 唯一保证注入每个会话的文件，压缩 = 关键纪律失去启动即知性） |
| F CCF-A 方法学 | literature-quality **T1/T2 分界显式化**（按 venue 核实强度：第二渠道确认=T1、仅自述=T2，附升级路径——2026 会议论文档位从此可复核）；**"引用数不用于排序"成文**（同口径同快照日内才可比、跨源不横比）；workflows §实验 **4→6 条**：+失败实验登记四要素（假设/现象/已排除原因/对 idea 的影响——rebuttal 弹药）、+复现声明四要素（种子/硬件/ckpt 哈希/评测 commit），与 §10、protocol 互指；research-workflow 降级对齐（方法学权威声明 + 两处指针化）；README「等待用户」**补 2 项**（Zotero 库备份——8 篇付费墙 PDF 唯一载体；GITHUB_TOKEN 轮换） |

## 二、更正与发现清单（事实级）

1. **DrivoR 矛盾行**（sota-plan §6）：71 轮传播核查漏改，与 §1.0 直接矛盾——两轮巡查（77 轮五路 + 78 轮五路）均未抓到，本轮专项审查抓到。
2. **幽灵文件引用**（templates 分册约定）：声称 world-model/verification-2.md 存在——全库无此文件、历史无踪（Glob 验证）。
3. **DP-E05 L 级错标**：L2 → L3（证据在 C003 §P.2，同批次 E06 正确）。
4. **第 4 处"17 条"计数漂移**（sota-plan §9.7）：原写"21 条 = 4+17"，**加粗分隔使 77 轮的 Grep 未命中**——教训已入 lessons §三.11（措辞修正后要用多种分隔形态复查）。
5. **context.md 自相矛盾**（L45 vs L52）。
6. **本轮自查自证**：normalize 豁免移植后立刻抓到批次 A 新写的 2 处错层链接（`../../../../ai/rules.md` 应为 5 层）——修脚本的价值当场兑现。

## 三、已知未做（有意）

1. 中文节名 § 引用机器化、embodied 轮次表机器化——成本中、收益待定，避免一轮塞太满（计划"不做清单"第 6 条）。
2. AGENTS.md 完全指针化——被否决（always_applied 机制依赖其自包含性）。
3. `preparation.md` L341"沙箱访问不了 HF"历史表述——带轮次限定且实践结论成立，零和纪律下不动。
4. judgments 第三册拆点预案——按增长推演约第 100+ 轮触线，待续 #26 已载明政策，届时再定。

## 四、产出

| 类别 | 文件 |
|---|---|
| 新建 | [ai/lessons.md](../../../ai/lessons.md)（24 条教训档案） |
| 脚本 | [check_links.py](../../../shared/scripts/check_links.py)（行数进 exit、78a 正则、README 卷数登记、分级汇总）、[normalize_links.py](../../../shared/scripts/normalize_links.py)（围栏/行内代码豁免） |
| 规则 | [ai/rules.md](../../../ai/rules.md)（−28%、零和纪律、L2 消歧）、[ai/workflows.md](../../../ai/workflows.md)（同步位 9 处、执行序、§实验 6 条、收尾叙事转 lessons）、[AGENTS.md](../../../AGENTS.md)（修漂移+权威声明）、[templates.md](../../../ai/templates.md)（分册约定三处核正） |
| 方法学 | [literature-quality.md](../../../shared/literature-quality.md)（T1/T2 分界、引用数口径）、[research-workflow.md](../../../shared/research-workflow.md)（降级对齐） |
| 内容 | sota-plan/preparation（瘦身出预警带）、DP-A/DP-S/DP-E 三表（词表/L 级/待核痕迹）、context.md、pdfs_pending.md |
| 状态 | [state.md](../state.md)（#26 体积更新、#27 落点改道）、[index.md](../index.md)、embodied [history.md](../../embodied-ai/history.md)/[state.md](../../embodied-ai/state.md) |
| 用户侧 | [README.md](../../../README.md)（等待用户 +2 项） |

## 五、状态同步

| 位置 | 改动 |
|---|---|
| state.md | 当前阶段改为本轮摘要；时间戳 78 轮 |
| history.md | 索引加 78 行；卷数 59 → **60** |
| index.md / README.md | 最近动态 + 指针表加 78 行；README 等待用户 +2 项 |
| embodied history | 补第 78 条目（第 10 轮） |
| CURRENT.md | 「在改」区清空 + 页脚 78 轮 |
| 验证 | `check_links.py` **exit 0**（含全部加固）；normalize dry-run 死链 0；两文件出预警带 |
