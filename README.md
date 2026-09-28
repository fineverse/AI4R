# AI4R 工作空间

AI 辅助深度学习科研：文献检索 → 研究脉络 → idea → 实验 → 论文。

> 本文件是给人看的入口。AI 启动规则见 [AGENTS.md](AGENTS.md)，内部组织设计见 [shared/workspace-design.md](shared/workspace-design.md)。

## 当前项目

| 项目 | 角色 | 状态 |
|---|---|---|
| [autonomous-driving](projects/autonomous-driving/project.md) · 自动驾驶 | **主方向** | 领域脉络 + 研究对象（扩散规划器）脉络完成；两借鉴来源 **52 篇全部全文级** · 2026-09-23 |
| [embodied-ai](projects/embodied-ai/project.md) · 具身智能 | 次方向（来源领域） | 脉络初稿 + 两借鉴来源建表（28 篇，摘要级）· 2026-09-23 |

两个项目平级。项目内固定 `direction/`（大方向）+ `topics/`（小方向）两层。

## 最近动态

**最新一轮：第四十八轮（2026-09-28）**——**授权弹窗的根因：把临时产物搬出了工作空间**：用户第二次提"经常需要授权，特别是去 `/tmp`"→ 诊断出**三层根因**（我违反纪律第 6 条 / **`/tmp` 在工作空间外 → 每一次访问都走授权** / 工作空间无 git）→ **用户拍板**：临时根迁到 **`inbox/scratch/`**（工作空间内）、**`git init` + 每轮收尾提交一次**（初始提交 `c9fba6e`）。**逐轮详情见 [autonomous-driving/history.md](projects/autonomous-driving/history.md)（索引 + 30 卷）**；当前阶段与待续清单见两个项目的 `state.md`，**本节只留指针、不写结论**（规则见 [ai/workflows.md](ai/workflows.md) §轮次收尾第 3 条）。

| 轮次 | 指针 |
|---|---|
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
| 具身侧（第七、八、二十五、二十六、二十九轮） | [embodied-ai/history.md](projects/embodied-ai/history.md) |

## 等待用户

- **（一次性）授权清理 `/tmp/ai4r/` 遗留**（约 28 MB，第二十九至四十七轮的产物）——一条命令，见 [inbox/cleanup.md](inbox/cleanup.md) §当前待清理；跑完 `/tmp/ai4r/` 不再产生新内容
- 下载付费墙 PDF（**8 条**），清单见 [pdfs_pending.md](projects/autonomous-driving/pdfs_pending.md)
- **只剩两项待你回**（[preparation.md §7](projects/autonomous-driving/ideas/preparation.md)）：**7.1 可用 GPU 与预算**（决定走"只训 scorer"还是端到端）、**7.2 是否升级为正式课题**（你的表态指向要做实验）——其余两项已定（方向已重排、主基准 = NAVSIM v2 navhard）

## 想细看时

- 自动驾驶项目进度：[projects/autonomous-driving/state.md](projects/autonomous-driving/state.md)
- 自动驾驶资料导航：[projects/autonomous-driving/index.md](projects/autonomous-driving/index.md)
- 具身智能资料导航：[projects/embodied-ai/index.md](projects/embodied-ai/index.md)
- 研究方法与原则：[shared/research-workflow.md](shared/research-workflow.md)
- 工具与跨项目资料：[shared/index.md](shared/index.md)
