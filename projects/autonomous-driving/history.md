# 自动驾驶项目 · 逐轮工作记录（索引）

更新时间：2026-10-01
用途：**索引**——每轮**一行概览**（做了什么），**详情在各卷** [history/rounds-*.md](history/)。[state.md](state.md) 只保留**当前阶段 + 待续清单 + 判断边界**。
**第七十四轮瘦身**：本文件原为 66 KB（超 Read 工具 64 KiB 整读上限），根因是**每行的内容与本卷正文逐字重复**（详情本就在 `rounds-*.md`）→ 按 [ai/rules.md](../../ai/rules.md) §文件更新的「**超限处理按文件角色分档**」，**索引类走瘦身、不拆册**：各行压缩为一行概览，**信息一字未删**（都在对应卷里）。同时修掉原表**被空行切断成多段**、「49–59 与 60–73 顺序相反」两处格式问题。
同目录另有 [CURRENT.md](history/CURRENT.md)——**并行会话的同步机制（软通道，单写者 = 主线程）**：只写本轮「在改」文件清单；**非卷**。

## 分卷（共 58 卷）

| 卷 | 轮次 | 概览 |
|---|---|---|
| [rounds-01-08.md](history/rounds-01-08.md) | 第一至第八轮 | 通用检索、扩散规划器专题建表与补全文、消化整理、知识体系树状化 |
| [rounds-09-17.md](history/rounds-09-17.md) | 第九至第十七轮 | 文献质量规范 + VLA / 世界模型第一轮；世界模型源码级分析、非生成式基线规划头、锚点 / 词表公开渠道 |
| [rounds-18-23.md](history/rounds-18-23.md) | 第十八至第二十三轮 | 特权信息输入权限、GenAD 生成机制、具身迁移机制 + NAVSIM 评测接口、VLA 侧三轮 |
| [rounds-24a.md](history/rounds-24a.md) | 第二十四轮（§1–§16） | 世界模型侧 4 篇升全文 + WoTE 源码核验、DriveLaW、Drive-OccWorld / World4Drive / LAW、Flow Planner、CARLA 系基线 |
| [rounds-24b.md](history/rounds-24b.md) | 第二十四轮（§17–§21） | nuPlan 闭环 / Bench2Drive / nuScenes 开环三套口径、研究对象侧代码可用性全表 |
| [rounds-24c.md](history/rounds-24c.md) | 第二十四轮（§22–§27） | GuideFlow、LCS / BridgeDrive、MPDiffuser / DIPOLE、NeMo / OccVAR 结账、VLA 边界外复核、AutoMoT |
| [rounds-25.md](history/rounds-25.md) | 第二十五轮 | VLA-22/25/27 与多篇 WM 全文 + 代码核验；两表 **52 篇全部升全文** |
| [rounds-26.md](history/rounds-26.md) | 第二十六轮 | 消化 + 工作流迭代：`AGENTS.md` 重写、`preparation.md §2` 重写为 S1–S30、`judgments.md` 分 A–H |
| [rounds-27.md](history/rounds-27.md) | 第二十七轮 | 按"提分优先"新标准重排方向：navhard 13 行格局 + 新建 `sota-plan.md` |
| [rounds-28.md](history/rounds-28.md) | 第二十八轮 | 知识层一致性审计（8 处事实冲突 + 58 处悬空引用）+ 代码脉络模板重写 |
| [rounds-29.md](history/rounds-29.md) | 第二十九轮 | 具身侧知识层审计；引用可达性（孤儿 / 弱引用）入检查脚本 |
| [rounds-30.md](history/rounds-30.md) | 第三十轮 | S1–S30 量化依据溯源；C005 错册引用 13 处；分册引用归属入检查 |
| [rounds-31.md](history/rounds-31.md) | 第三十一轮 | 笔记「对本项目的意义」节补齐与统一（27 处改名） |
| [rounds-32.md](history/rounds-32.md) | 第三十二轮 | §3 / §4 / §5 溯源收尾（DriveWorld-VLA 的 arXiv ID 配错等） |
| [rounds-33.md](history/rounds-33.md) | 第三十三轮 | `judgments.md` 58 条内部一致性审计（"RL 词义"计数 3/5/9 三种说法） |
| [rounds-34.md](history/rounds-34.md) | 第三十四轮 | 小方向 README 「必写 4 节」规格化 + 补齐 6 个 README |
| [rounds-35.md](history/rounds-35.md) | 第三十五轮 | 提分账本：追问「scorer ≈ +20」的三个成立条件 |
| [rounds-36.md](history/rounds-36.md) | 第三十六轮 | 路线②起点重估（DiffVLA 发布代码无扩散头）+ `judgments.md` 拆册 |
| [rounds-37.md](history/rounds-37.md) | 第三十七轮 | 三份 navhard 表交叉核对（"同一基准跨论文仍不可横比"的第二根因） |
| [rounds-38.md](history/rounds-38.md) | 第三十八轮 | EPDMS 两套官方实现 —— 53.2 的谜底 |
| [rounds-39.md](history/rounds-39.md) | 第三十九轮 | 本地 devkit 是哪一套口径；意外发现 **EC 不进分** |
| [rounds-40.md](history/rounds-40.md) | 第四十轮 | 传播核查第三十六至三十九轮的口径结论（抓 4 处 stale） |
| [rounds-41.md](history/rounds-41.md) | 第四十一轮 | 用户给新前提（CCF-A + 双 3090）→ 方向重排；选优损失账本起 |
| [rounds-42.md](history/rounds-42.md) | 第四十二轮 | 选优损失账本：**天花板 gap 与地板 gap 是两个量** |
| [rounds-43.md](history/rounds-43.md) | 第四十三轮 | GTRS Table 1 填掉两处空白 + 一条反向证据 |
| [rounds-44.md](history/rounds-44.md) | 第四十四轮 | 一条判断被静默删 → 判断条数一致性入检查（第八 / 九项） |
| [rounds-45.md](history/rounds-45.md) | 第四十五轮 | 换 basename 拆册留下 17 处悬空引用 → 章节可达性检查 |
| [rounds-46.md](history/rounds-46.md) | 第四十六轮 | 把"CSV 是权威源"锁进机器检查（第十项） |
| [rounds-47.md](history/rounds-47.md) | 第四十七轮 | 传播核查（第四十一至四十三轮结论没进 `preparation.md`） |
| [rounds-48.md](history/rounds-48.md) | 第四十八轮 | 授权弹窗根因：临时产物搬进工作空间 + `git init` |
| [rounds-49.md](history/rounds-49.md) | 第四十九轮 | 路线 B 第一步落成预注册协议 |
| [rounds-50.md](history/rounds-50.md) | 第五十轮 | 把"只读优先"改成明确的工具规则 |
| [rounds-51.md](history/rounds-51.md) | 第五十一轮 | 当前态传播核查（README / state / project 的旧轮次） |
| [rounds-52.md](history/rounds-52.md) | 第五十二轮 | 收敛等待项 |
| [rounds-53.md](history/rounds-53.md) | 第五十三轮 | 修正选优协议聚合口径 |
| [rounds-54.md](history/rounds-54.md) | 第五十四轮 | 分开完整政策比较与候选池诊断 |
| [rounds-55.md](history/rounds-55.md) | 第五十五轮 | 网络排查与论文检索工具固化 |
| [rounds-56.md](history/rounds-56.md) | 第五十六轮 | 补齐轮次指针 + HF checkpoint 定位 |
| [rounds-57.md](history/rounds-57.md) | 第五十七轮 | 按需补信息维度（8 张表）；⚠ 事故：误覆盖 / 误删 `rounds-54`・`rounds-55` |
| [rounds-58.md](history/rounds-58.md) | 第五十八轮 | 工作流与工作空间整理（修 8 处 stale） |
| [rounds-59.md](history/rounds-59.md) | 第五十九轮（支线） | 用 S2 官方 API 补具身表三缺口（记入 S2 venue 系统性误记） |
| [rounds-60.md](history/rounds-60.md) | 第六十轮 | 整合支线投递：安装协作纪律 + 关闭 4 项遗留 |
| [rounds-61.md](history/rounds-61.md) | 第六十一轮 | 完善并行会话同步机制（硬通道）——查出四个漏洞 |
| [rounds-62.md](history/rounds-62.md) | 第六十二轮 | 整合支线第二篇：整合投递物从 checklist 变机器检查（第 11 项） |
| [rounds-63.md](history/rounds-63.md) | 第六十三轮 | 传播核查（第 55–62 轮）+ 待核清单分档 |
| [rounds-64.md](history/rounds-64.md) | 第六十四轮 | 把"文档 ≤ 64 KB"从人工目测变成机器检查（第 12 项） |
| [rounds-65.md](history/rounds-65.md) | 第六十五轮 | 收敛三处冗余 |
| [rounds-66.md](history/rounds-66.md) | 第六十六轮 | 机制实测：硬机制全通，查出规则自相矛盾 + 一处虚报 |
| [rounds-67.md](history/rounds-67.md) | 第六十七轮 | 整合两篇投递：理正收尾步序 + 取消 `CURRENT.md` 投递登记区 |
| [rounds-68.md](history/rounds-68.md) | 第六十八轮 | 整合支线投递：navhard 竞品表 + "选优器 / 候选池"专线 |
| [rounds-69.md](history/rounds-69.md) | 第六十九轮 | TOAD 的 split 核实：navhard 榜一易主 |
| [rounds-70.md](history/rounds-70.md) | 第七十轮 | 整合"周扫"投递：官方榜重建分数格局 + 三处代码翻案 + §周扫机制 |
| [rounds-71.md](history/rounds-71.md) | 第七十一轮 | 传播核查：第 70 轮改的三处前提，别处还有多少旧话 |
| [rounds-72.md](history/rounds-72.md) | 第七十二轮 | 整合"论文对比方案"投递：`sota-plan.md` 新增 §10 |
| [rounds-73.md](history/rounds-73.md) | 第七十三轮 | 重点代码继承关系系统梳理（三批）+ 决策文件消化 |
| [rounds-74.md](history/rounds-74.md) | 第七十四轮 | 文档体积政策（两线制 + 按角色分档）；`history.md` 瘦身 66→9.6 KB、`sota-plan.md` 去重至硬线以下 |
| [rounds-75.md](history/rounds-75.md) | 第七十五轮 | 建立「重组地图」（结构 × 因果）：新建 `ideas/recombination-map.md`，把血统与受控增益按行对齐 |
| [rounds-76.md](history/rounds-76.md) | 第七十六轮 | 裁决第 73–75 轮（接受、不回退）+ 消化「重组地图」：TOAD 不推翻候选区 ③，但 TOAD 的 related work 已把我们的前提说成主流；卷数并入机器检查 |

## 写新记录的约定

- **追加到最新的那一卷**；当该卷超过 **200 行**时，新建下一卷（命名沿用 `rounds-<起始>-<结束>.md`）并回到本表登记。
- 每轮记录保持现有结构：**动因 → 做法 → 结论（含更正）→ 产出（指向具体文件与章节）**。
- **本表是索引、卷是正文**：本表每轮**只写一行概览**，**详细过程只写进该轮卷文件**（2026-10-01 第七十四轮瘦身时定——此前每行复述整轮内容，把本文件涨到 66 KB）。**引用可以重复，计数不能**：本表的"卷数"须与 `history/rounds-*.md` 实际个数一致。
- 记录里只写"这一轮新增了什么"，不重复 [state.md](state.md) 的判断边界与 [code/traces/](code/traces/) 的逐项对照。
- **路径层数陷阱**：卷文件在 `projects/<项目>/history/` 下，**比 `state.md` 多一层**——引用 `ai/`、`shared/` 要用 **`../../../`**。实测**已两次写少一层**（第三十三轮的 `ai/workflows.md`、第三十四轮的 `ai/templates.md`，都被 `check_links.py` 当场抓到）→ **写完轮次记录必须先跑一次检查脚本**。
