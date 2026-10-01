# 第七十七轮（2026-10-01）· 工作空间遗留问题修复（五路巡查 + 七批次清账）

**性质**：非专题研究轮——用户要求"多派几个智能体彻底巡查一遍工作空间的遗留问题"，主线程派 **5 个只读巡查智能体**（组织 / 索引与机器检查 / 规则与工作流 / 待办与悬案 / 内容质量与平级一致性），核实全部问题点到文件与行号后，按用户批准的计划（`.trae/documents/2026-10-01-工作空间遗留问题修复计划.md`）一次修完。**用户三项决策**：scratch 先备份再清空；一轮做完；`.trae/documents/` 三件移入 `archive/plans/`。**范围排除**：远端 / 备份 `.git` / bashrc 代理（待续 #22，用户明示放一放）。

## 一、巡查发现（六类，均经主线程复核）

1. **数据风险**：`normalize_links.py` 的排除路径是 2026-09-23 重构前旧址（`topics/diffusion-planner/code/repos`）→ 条件永不命中，`--apply` 会走进 **1.65 GB 第三方快照**改写链接。
2. **机器检查盲区**：README 轮次指针表**漏第 67/68 轮两行**（第 76 轮只补了「最近动态」；漏行不产生死链，现有检查全抓不到）；scoring_line **"17 条线索级"实为 15 条**（未登记计数，漂移无人发现）；pdfs_pending 8 条、DP-C 7 条也未登记。
3. **规则/工作流不自洽**：「收尾同步 7 处」在 workflows/README/归档件三处口径互不重合（正是历次漏同步的根因）；`workspace-design.md` 运行纪律 5（"未分拣视为可清理"）与第 11 项检查冲突、纪律 8（"单会话单项目"）已被支线机制取代；scratch 清理口径在 rules 第 7 条 / cleanup.md / .gitignore 注释三处互相矛盾；rules §一.1 与 §一.4 对支线提交范围表述不一；`.gitignore` 注释声称 SKIP_DIRS 跳过 `.vscode`（实际没有）。
4. **导航失真**：具身侧第 55/57/59/60 四轮对具身文件有实质改动但 `embodied-ai/history.md` 零逐轮记录（停在 29 轮）；embodied state 把第 59 轮的工作误记为"第 55 轮用 S2 官方 API"。
5. **待续清单失真**：AD `state.md` 22 行中 11 行已结账仍滞留（违背第 52 轮"启动入口不当已解决项当当前任务"）；#16 与 #26 是矛盾指令；#14 空号无说明；navhard 竞品表 2 处待核与 59 轮 3 条待办未升入任何清单。
6. **组织残留**：`inbox/scratch/` 34 个一次性产物（零引用、不在 git）；`.trae/documents/` 3 个已完成计划不进 git（静默丢失风险）；archive 文件名 "+"-" 分隔符 3:7 混用；`__pycache__` 字节码残留。

## 二、做法（七批次）

| 批次 | 内容 |
|---|---|
| A 数据风险 | `normalize_links.py` 改为按目录名剪枝（SKIP_DIRS 与 check_links 同口径：repos/archive/scratch/.git/.trae/__pycache__/node_modules）——顺带修掉旧路径；dry-run 验证排除生效 |
| B 机器检查 | `check_links.py` **新增第 13 项「README 轮次表完整性」**（最新一卷必须入 README + 区间无缺口——修完前实跑精确报出 67/68 缺口）；**COUNT_RULES 新增 3 条**（scoring_line §二 / pdfs_pending / DP-C）；SKIP_DIRS 加 `.vscode`（让 .gitignore 注释变真） |
| C 规则自洽 | workflows：**插入「收尾同步位清单（权威定义，共 7 处）」**+ 开轮第 1 步补 `git log` + 周扫"每周必跑"改"每次周扫必跑"；rules：§一.4 支线提交范围补新建文件、第 7 条定 scratch 清理口径、第 9 条补忽略清单指针；workspace-design：纪律 4 补 PDF 例外、纪律 5 重写（inbox 只放投递物）、纪律 8 改为支线机制、组织原则 6 成文论文表形态约定、更新时间；`.gitignore` 注释对齐新口径；shared/index（"都只读"改为实况 + S2 状态 ✅）；profile（GPU/目标已定）；tools.md 时间戳 + tools.env 积分注解对齐 487 实测 |
| D 导航索引 | README 补 67/68 两行、当前项目表刷新到 10-01、补记框加后续说明、具身侧行扩到九轮；AD history 写新记录约定改为"每轮一卷"（与实践一致）；**embodied history 补 55/57/59/60 四条**（只从 AD 侧卷提取事实）+ "当前 9 轮"；embodied index 同步；embodied state 修轮次误记 + 引用数口径不可混比 + 待续 #5（写 diffusion-policy lineage） |
| E 待续清账 | AD state 删 11 行已结账（#1–3/4–5/7/11/12/13/15/16/17/18/20）；#16 关闭并入 #26 注记；#14 空号加脚注（**编号不复用、不重排**）；#10/#19 瘦身；#8 补 S034 直下结果；**新增 #28**（navhard 竞品 2 处待核）**#29**（引用数口径三条可选补齐）；删行前 Grep 全库「待续第」核对外部引用（发现并修复 sota-plan:381 引 #17、preparation:343 引 #7 两处活指针） |
| F 内容小修 | 17→15（state / index / **sota-plan §9.6 证据边界**共三处——第三处是收尾复验时发现的漏网；三处全部并入 COUNT_RULES）；#9 §J 错册改指 C003-2；rules "§分册约定"改实名"§分册、编号与更正约定"；DP-E 表 T 档**补 E28 行**（T1：NeurIPS 2023 + 有代码）+ 文件头时间戳；protocol `C_N^full` 拆分双定义；#22 改题"用户侧三件事" |
| G 文件组织 | `.trae/documents/` 三件 → `archive/plans/`（补日期前缀 + 归档头，进 git）；archive 3 个 "+" 文件名改 "-"（同步修 rounds-60/62/66 三处引用，含 1 处真链接）；`__pycache__` 与 scratch 的删除命令登记 `cleanup.md` 待用户执行（rm 被跳过，未重试）；scratch 已先 tar 备份到 `/tmp/ai4r_scratch_backup_20261001.tar.gz`（210 KB） |

## 三、更正清单（事实级，共 8 处）

1. **embodied state 轮次误记**：原"第五十五轮用 S2 官方 API 补齐 VLA 表引用数（7→14/14）"——实为**第五十五轮用 Ai4Scholar 查得 7/14**，**第五十九轮**用 S2 官方 API 补齐 14/14（rounds-55/59 可证）。
2. **scoring_line §二条数**：17 → **15**（state #23 ③、AD index、sota-plan §9.6 证据边界共三处——第三处系收尾复验发现；三处声明全部登记进 COUNT_RULES）。
3. **state #9 错册**：§J 在 C003 第二册（§I–§P），原链接只指第一册。
4. **DP-E 表 T 档缺 E28 行**：第 57 轮"逐行"漏一行，本轮补（T1）。
5. **protocol `C_N` 一符两义**：full-pipeline oracle 版改名 `C_N^full` 并注明与 ceiling@N 区分。
6. **shared/index S2 状态**："⚠️ 需 key"→"✅ 有 key（09-30 配置）"（与 tools.md 一致）；profile "GPU 待补充"→双 3090 已定。
7. **rules L113 裸 § 引用**："§分册约定"→"§分册、编号与更正约定"（templates 实名；链接文字外的 § 机器不管，人工修）。
8. **两处活指针修复**：sota-plan:381 原指待续 #17、preparation:343 原指 #7（两行已删）——分别改为指向 rounds-56 与 protocol 本体，顺带修掉"沙箱访问不了 HF"的过时表述（sota-plan 处）。

## 四、已知未改（有意，非遗漏）

- `preparation.md` L341 "工作沙箱访问不了 HF（http 000）"：带"第四十轮前已实测"限定，且实践结论（大文件仍建议用户在沙箱外下载）成立；该文件距硬线仅 636 B，不为一句历史表述冒险。
- rounds 历史卷内对旧待续项号（#13 等）与旧 archive 文件名的"当时"记述：历史记录不改（改名处的 3 处活引用已修，纯历史记述保留）。
- **scratch 实际删除未执行**：rm 命令被用户跳过 → 未重试；命令与范围、备份位置登记在 [inbox/cleanup.md](../../../inbox/cleanup.md)「当前待清理」，择机一次授权即可。
- AGENTS.md 与 rules 的双写：有意保留（启动文件需自包含），本轮未动 AGENTS.md。

## 五、产出

| 类别 | 文件 |
|---|---|
| 脚本 | [check_links.py](../../../shared/scripts/check_links.py)（第 13 项 + COUNT_RULES 3 条 + SKIP_DIRS）、[normalize_links.py](../../../shared/scripts/normalize_links.py)（排除路径） |
| 规则 | [ai/workflows.md](../../../ai/workflows.md)（同步位权威清单等 3 处）、[ai/rules.md](../../../ai/rules.md)（3 处）、[workspace-design.md](../../../shared/workspace-design.md)（5 处）、[.gitignore](../../../.gitignore)（注释） |
| 导航 | [README.md](../../../README.md)（67/68 行等 4 处）、AD [history.md](../history.md)（约定）、[state.md](../state.md)、[index.md](../index.md)、embodied [history.md](../../embodied-ai/history.md)/[state.md](../../embodied-ai/state.md)/[index.md](../../embodied-ai/index.md) |
| 内容 | [diffusion_planner_embodied.md](../../embodied-ai/topics/diffusion-policy/papers/diffusion_planner_embodied.md)（E28）、[protocol.md](../experiments/protocol.md)（C_N^full）、[pdfs_pending.md](../pdfs_pending.md)（S034）、[sota-plan.md](../ideas/sota-plan.md)/[preparation.md](../ideas/preparation.md)（指针） |
| 组织 | archive/plans/ 新增 3 件、archive 改名 3 件、[inbox/cleanup.md](../../../inbox/cleanup.md)（待执行命令 + 新口径） |

## 六、状态同步

| 位置 | 改动 |
|---|---|
| state.md | 待续清单清账（删 11 行、关 #16、#14 脚注、新增 #28/#29）；当前阶段改为本轮摘要 |
| history.md | 索引加 77 行；卷数 58 → **59** |
| index.md / README.md | 「最近动态」+ 指针表加 77 行 |
| CURRENT.md | 「在改」区清空 |
| 验证 | `check_links.py` **exit 0**（含新第 13 项与 3 条新计数——修复前实跑曾精确报出 67/68 缺口与 17≠15，即检查器自身先被验证） |
