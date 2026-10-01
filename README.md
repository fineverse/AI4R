# AI4R 工作空间

AI 辅助深度学习科研：文献检索 → 研究脉络 → idea → 实验 → 论文。

> 本文件是给人看的入口。AI 启动规则见 [AGENTS.md](AGENTS.md)，内部组织设计见 [shared/workspace-design.md](shared/workspace-design.md)。

## 当前项目

| 项目 | 角色 | 状态 |
|---|---|---|
| [autonomous-driving](projects/autonomous-driving/project.md) · 自动驾驶 | **主方向** | 领域脉络 + 研究对象（扩散规划器）脉络完成（**继承关系 S1–S4 分级**）；两借鉴来源 **52 篇全部全文级**；重组地图 + 冲 SOTA 作战文件就绪 · 2026-10-01 |
| [embodied-ai](projects/embodied-ai/project.md) · 具身智能 | 次方向（来源领域） | 脉络初稿 + 两借鉴来源建表（28 篇，摘要级）；三表证据维度（T 档 / §1.1）已补齐 · 2026-10-01 |

两个项目平级。项目内固定 `direction/`（大方向）+ `topics/`（小方向）两层。

## 最近动态

**最新一轮：第七十九轮（2026-10-01）**——**全工作空间修复（A–E 组，非专题研究轮）**：把同日巡查清单逐条落地——脚本数据破坏修复、A 组真错误 ×11（π0 venue 联网核验、GR00T N1 机制、CSV 重刷等）、检查器 +3 项、archive 16 件头部统一（→ [rounds-79.md](projects/autonomous-driving/history/rounds-79.md)）。

**上一轮：第七十八轮（2026-10-01）**——**规则体系优化（服务 CCF-A）**：5 路审查后六批次修体系本身——6 处漏网真错误（DrivoR 矛盾行、幽灵文件、L 级错标）、检查器 5 项加固、**两决策文件瘦身出预警带**、同步位扩 9 处 + 8 处时间戳清账、**规则拆双层（新建 ai/lessons.md，rules −28%）**、方法学加固（T1/T2 分界、失败实验登记、复现声明）（→ [rounds-78.md](projects/autonomous-driving/history/rounds-78.md)）。

**上一轮：第七十七轮（2026-10-01）**——**工作空间遗留问题修复**（非专题研究轮）：5 个只读巡查智能体全面巡查 + 按批准计划七批次清账——修 `normalize_links.py` 数据风险、`check_links` 新增**第 13 项（README 轮次表完整性）**与 3 条计数登记、**「收尾同步 7 处」权威清单**落进 workflows、**具身侧补记第 55/57/59/60 四轮**并修正 55/59 轮归属误记、待续清单清账（删 11 行已结账、新增 #28/#29）、scratch/归档组织；更正 8 处事实级错误（→ [rounds-77.md](projects/autonomous-driving/history/rounds-77.md)）。

**逐轮详情以 [autonomous-driving/history.md](projects/autonomous-driving/history.md)（索引 + 61 卷）为准**；当前阶段与待续清单见两个项目的 `state.md`，**本节只留指针、不写结论**（规则见 [ai/workflows.md](ai/workflows.md) §轮次收尾第 3 条）。

> **⚠ 第七十六轮补记**：本轮发现 **README 的「最近动态」被第 73–75 轮的收尾漏掉了**（它当时仍停在"54 卷 / 最新第七十二轮"）——**这是"收尾同步 7 处"里漏掉一处的又一次实证**，见 [rounds-76.md](projects/autonomous-driving/history/rounds-76.md)。（**第七十七轮后续**：已把「收尾同步 7 处」定为权威清单并加第 13 项机器检查，见 [ai/workflows.md §轮次收尾](ai/workflows.md)；本轮并补上指针表漏掉的第 67/68 轮两行。）

| 轮次 | 指针 |
|---|---|
| **第七十九轮** | [rounds-79.md](projects/autonomous-driving/history/rounds-79.md) — 全工作空间修复（A–E 组）：脚本数据破坏修复、A 组真错误 ×11、检查器 +3 项、archive 头部统一 |
| **第七十八轮** | [rounds-78.md](projects/autonomous-driving/history/rounds-78.md) — 规则体系优化（服务 CCF-A）：拆双层 lessons.md、两文件出预警带、T1/T2 分界与复现声明 |
| **第七十七轮** | [rounds-77.md](projects/autonomous-driving/history/rounds-77.md) — 工作空间遗留问题修复：五路巡查 + 七批次清账（新检查第 13 项、收尾同步位权威清单、具身补四轮、待续清账） |
| **第七十六轮** | [rounds-76.md](projects/autonomous-driving/history/rounds-76.md) — 裁决 73–75 + 消化「重组地图」；卷数并入机器检查 |
| **第七十五轮** | [rounds-75.md](projects/autonomous-driving/history/rounds-75.md) — 建立「重组地图」（→ [recombination-map.md](projects/autonomous-driving/ideas/recombination-map.md)） |
| **第七十四轮** | [rounds-74.md](projects/autonomous-driving/history/rounds-74.md) — 文档体积政策（两线制 + 按角色分档）（→ [ai/rules.md §文件更新](ai/rules.md)） |
| **第七十三轮** | [rounds-73.md](projects/autonomous-driving/history/rounds-73.md) — 代码继承关系系统梳理（三批，S1–S4 分级） |
| **第七十二轮** | [rounds-72.md](projects/autonomous-driving/history/rounds-72.md) — 整合"论文对比方案"：`sota-plan.md` 新增 §10（→ [sota-plan.md §10](projects/autonomous-driving/ideas/sota-plan.md)） |
| **第七十一轮** | [rounds-71.md](projects/autonomous-driving/history/rounds-71.md) — 传播核查第 70 轮的三处前提级改动（16 个文件） |
| **第七十轮** | [rounds-70.md](projects/autonomous-driving/history/rounds-70.md) — 官方榜重建分数格局 + 三处代码翻案 + §周扫机制（→ [sota-plan.md §1.0](projects/autonomous-driving/ideas/sota-plan.md)） |
| **第六十九届** | [rounds-69.md](projects/autonomous-driving/history/rounds-69.md) — 核实 TOAD split → navhard 榜一易主（⚠ 两处已被第 70 轮推翻）（→ [judgments.md](projects/autonomous-driving/judgments.md) D 组、[sota-plan.md §9.7](projects/autonomous-driving/ideas/sota-plan.md)） |
| **第六十八轮** | [rounds-68.md](projects/autonomous-driving/history/rounds-68.md) — 整合支线投递：navhard 竞品表 +「选优器 / 候选池」专线（→ [navhard_competitors.md](projects/autonomous-driving/topics/diffusion-planner/papers/navhard_competitors.md)、[scoring_line.md](projects/autonomous-driving/topics/diffusion-planner/papers/scoring_line.md)） |
| **第六十七轮** | [rounds-67.md](projects/autonomous-driving/history/rounds-67.md) — 整合两篇投递：理正收尾步序 + 取消 `CURRENT.md` 投递登记区（→ [ai/workflows.md §轮次收尾](ai/workflows.md)） |
| **第六十六轮** | [rounds-66.md](projects/autonomous-driving/history/rounds-66.md) — 机制实测 + 修规则自相矛盾 + 落盘沙箱/覆盖边界（→ [ai/rules.md §执行与清理纪律](ai/rules.md) 第 10 条） |
| **第六十五轮** | [rounds-65.md](projects/autonomous-driving/history/rounds-65.md) — 收敛三处冗余（检查清单 / git 命令 / 两文原则节） |
| **第六十四轮** | [rounds-64.md](projects/autonomous-driving/history/rounds-64.md) — `check_links` 的「文档体积预算」检查（→ [check_links.py](shared/scripts/check_links.py)） |
| **第六十三轮** | [rounds-63.md](projects/autonomous-driving/history/rounds-63.md) — 传播核查（第 55–62 轮）+ 待核清单分档（→ [state.md](projects/autonomous-driving/state.md) 待续第 19 项） |
| **第六十二轮** | [rounds-62.md](projects/autonomous-driving/history/rounds-62.md) — 整合支线第二篇：`check_links` 第 11 项 + 开轮 pre-flight + git 三小项（→ [check_links.py](shared/scripts/check_links.py)） |
| **第六十一轮** | [rounds-61.md](projects/autonomous-driving/history/rounds-61.md) — 完善并行会话的同步机制（→ [ai/rules.md §支线协作纪律](ai/rules.md)、[ai/templates.md §支线投递物](ai/templates.md)） |
| **第六十轮** | [rounds-60.md](projects/autonomous-driving/history/rounds-60.md) — 整合支线投递：协作纪律 + 关闭 4 项遗留（→ [history/CURRENT.md](projects/autonomous-driving/history/CURRENT.md)） |
| **第五十九轮** | [rounds-59.md](projects/autonomous-driving/history/rounds-59.md) — S2 官方 API 补齐 VLA 表缺口（引用数 14/14、venue、GR00T N1 悬案）+ 发现 S2 venue 系统性误记 |
| **第五十八轮** | [rounds-58.md](projects/autonomous-driving/history/rounds-58.md) — 工作流与工作空间整理（审计 + 修 stale） |
| **第五十七轮** | [rounds-57.md](projects/autonomous-driving/history/rounds-57.md) — 按需补齐 8 张论文表的质量依据/证据等级/代码状态（⚠ 当时**实际只提交了 6 张**；缺的具身侧 VLA / 世界模型两张已由**第六十轮补上**） |
| **第五十六轮** | [rounds-56.md](projects/autonomous-driving/history/rounds-56.md) — 补 49–54 轮指针 + HF checkpoint 定位（`datasets/OpenDriveLab/SimScale`） |
| **第五十五轮** | [rounds-55.md](projects/autonomous-driving/history/rounds-55.md) — 网络排查（TUN fake-ip / HF 解锁）+ [工具与凭据](shared/tools.md) 固化 + VLA 表补 S2 口径引用数 |
| **第五十四轮** | [rounds-54.md](projects/autonomous-driving/history/rounds-54.md) — 把完整政策分与候选池诊断分开（→ [protocol.md](projects/autonomous-driving/experiments/protocol.md)） |
| **第五十三轮** | [rounds-53.md](projects/autonomous-driving/history/rounds-53.md) — 修正选优协议的聚合口径：`C_N` 降级为 oracle 诊断量 |
| **第五十二轮** | [rounds-52.md](projects/autonomous-driving/history/rounds-52.md) — 收敛等待项为两类真实阻塞 |
| **第五十一轮** | [rounds-51.md](projects/autonomous-driving/history/rounds-51.md) — 当前态传播核查 |
| **第五十轮** | [rounds-50.md](projects/autonomous-driving/history/rounds-50.md) — 只读任务优先走内置工具（→ [AGENTS.md](AGENTS.md)、[ai/rules.md](ai/rules.md)） |
| **第四十九轮** | [rounds-49.md](projects/autonomous-driving/history/rounds-49.md) — 路线 B 第一步写成预注册实验协议（→ [protocol.md](projects/autonomous-driving/experiments/protocol.md)） |
| **第四十八轮** | [rounds-48.md](projects/autonomous-driving/history/rounds-48.md) — 授权弹窗根因 + 临时根迁入工作空间 + `git init`（→ [ai/rules.md §执行与清理纪律](ai/rules.md)、[inbox/scratch/](inbox/scratch/)） |
| **第四十七轮** | [rounds-47.md](projects/autonomous-driving/history/rounds-47.md) — 41–43 轮结论的传播核查（→ [preparation.md §5.1](projects/autonomous-driving/ideas/preparation.md)） |
| **第四十六轮** | [rounds-46.md](projects/autonomous-driving/history/rounds-46.md) — CSV 与 md 的 ID 一致性入检查 |
| **第四十五轮** | [rounds-45.md](projects/autonomous-driving/history/rounds-45.md) — 17 处悬空章节引用（→ [check_links.py](shared/scripts/check_links.py) 第五项） |
| **第四十四轮** | [rounds-44.md](projects/autonomous-driving/history/rounds-44.md) — 判断条数 + 声明计数入检查（→ [judgments.md §D](projects/autonomous-driving/judgments.md)） |
| **第四十三轮** | [rounds-43.md](projects/autonomous-driving/history/rounds-43.md) — GTRS Table 1 填空白 + 反向证据（→ [sota-plan.md §9.6](projects/autonomous-driving/ideas/sota-plan.md)） |
| **第四十二轮** | [rounds-42.md](projects/autonomous-driving/history/rounds-42.md) — 选优损失账本（→ [sota-plan.md §9](projects/autonomous-driving/ideas/sota-plan.md)） |
| **第四十一轮** | [rounds-41.md](projects/autonomous-driving/history/rounds-41.md) — 目标与算力定案 → 方向重排（→ [sota-plan.md §8](projects/autonomous-driving/ideas/sota-plan.md)） |
| **第四十轮** | [rounds-40.md](projects/autonomous-driving/history/rounds-40.md) — 传播核查（4 处 stale，含 1 处真错误） |
| **第三十九轮** | [rounds-39.md](projects/autonomous-driving/history/rounds-39.md) — 本地 devkit 口径 + EC 不进分（→ [benchmarks.md §2.10](projects/autonomous-driving/direction/benchmarks.md)） |
| **第三十八轮** | [rounds-38.md](projects/autonomous-driving/history/rounds-38.md) — EPDMS 两套官方实现（→ [benchmarks.md §2.9](projects/autonomous-driving/direction/benchmarks.md)） |
| **第三十七轮** | [rounds-37.md](projects/autonomous-driving/history/rounds-37.md) — 三份 navhard 表交叉核对（→ [sota-plan.md §7.7](projects/autonomous-driving/ideas/sota-plan.md)） |
| **第三十六轮** | [rounds-36.md](projects/autonomous-driving/history/rounds-36.md) — 路线② 起点重估 + `judgments.md` 拆册（→ [sota-plan.md §7.6](projects/autonomous-driving/ideas/sota-plan.md)） |
| **第三十五轮** | [rounds-35.md](projects/autonomous-driving/history/rounds-35.md) — 提分账本（追问「scorer ≈ +20」的成立条件） |
| **第三十四轮** | [rounds-34.md](projects/autonomous-driving/history/rounds-34.md) — 小方向 README 的必写节（6/6 补齐） |
| **第三十三轮** | [rounds-33.md](projects/autonomous-driving/history/rounds-33.md) — `judgments.md` 58 条内部一致性审计 |
| **第三十二轮** | [rounds-32.md](projects/autonomous-driving/history/rounds-32.md) — §3/§4/§5 溯源收尾 + DriveWorld-VLA 的 ID 错配 |
| **第三十一轮** | [rounds-31.md](projects/autonomous-driving/history/rounds-31.md) — 笔记「对本项目的意义」节补齐与统一 |
| **第三十轮** | [rounds-30.md](projects/autonomous-driving/history/rounds-30.md) — S1–S30 溯源 + 分册错册引用清账 |
| **第二十九轮** | [rounds-29.md](projects/autonomous-driving/history/rounds-29.md) — 具身侧知识层审计 + 引用可达性入检查脚本 |
| **第二十八轮** | [rounds-28.md](projects/autonomous-driving/history/rounds-28.md) — 知识层一致性审计 + 工作流落地 |
| **第二十七轮** | [rounds-27.md](projects/autonomous-driving/history/rounds-27.md) — 按"提分成为 SOTA"重排方向 → [sota-plan.md](projects/autonomous-driving/ideas/sota-plan.md) |
| **第二十六轮** | [rounds-26.md](projects/autonomous-driving/history/rounds-26.md) — 消化信息 + 工作空间与工作流迭代 |
| 更早（第一至二十五轮） | [history.md](projects/autonomous-driving/history.md) §分卷 |
| 具身侧（第七、八、二十五、二十六、二十九、五十五、五十七、五十九、六十轮） | [embodied-ai/history.md](projects/embodied-ai/history.md) |

## 等待用户

- **⚠ 防"成果搞丢"的两件事**（2026-09-30 实测：**删除有审批闸、覆盖没有闸**——写文件不弹窗，覆盖就是覆盖了；所以只有版本控制 + 异地副本能救）：
  1. **加私有远端**（代理已通）——目前所有工作只在**一块盘**上；
  2. **备份 `.git`**（打 tar 到别的盘/远端）——**`.git` 是不可再生资产**：工作文件丢了能重写，**提交历史丢了永远没了**。
- **`~/.bashrc` 加代理两行**（HF 直连不通的根因就是它，不是权限问题）：

```bash
export https_proxy=http://127.0.0.1:7897
export http_proxy=http://127.0.0.1:7897
```

- 下载付费墙 PDF（**8 条**），清单见 [pdfs_pending.md](projects/autonomous-driving/pdfs_pending.md)
- **Zotero 库备份**（2026-10-01 第七十八轮立）：工作空间规则是"PDF 留 Zotero"——**8 篇付费墙 PDF 下载后唯一载体就是 Zotero 库**（不可再生，工作空间只有笔记）；建议随 `.git` 一起做异地备份
- **GITHUB_TOKEN 轮换**（tools.md §GitHub 已建议）：当前 fine-grained token 曾以明文出现在对话记录（低风险：仅公开仓库只读），建议顺手换新
- 为路线 B 实验取得 SimScale 的 DiffusionDrive checkpoint，并准备 NAVSIM v2 `navhard` 数据；协议已写在 [experiments/protocol.md](projects/autonomous-driving/experiments/protocol.md)（**数据盘路径需加沙箱白名单**，见 [state.md](projects/autonomous-driving/state.md) 待续第 21 项）
- 如要正式立项，仍需用户明确确认；GPU、预算和主基准已经确定，不再作为待决策项

## 想细看时

- 自动驾驶项目进度：[projects/autonomous-driving/state.md](projects/autonomous-driving/state.md)
- 自动驾驶资料导航：[projects/autonomous-driving/index.md](projects/autonomous-driving/index.md)
- 具身智能资料导航：[projects/embodied-ai/index.md](projects/embodied-ai/index.md)
- 研究方法与原则：[shared/research-workflow.md](shared/research-workflow.md)
- 工具与跨项目资料：[shared/index.md](shared/index.md)
