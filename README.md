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

**最新一轮：第六十一轮（2026-09-30）**——**完善并行会话的同步机制**：第六十轮把支线提案原样装进去，本轮检查它**自己会不会失效**，查出四个漏洞（只有软通道 / 方向单向 / 无恢复程序 / 投递物无结构）→ 补 **通道 B（写文件前必跑 `git log` + `git status`）**、**恢复程序**、**[投递物模板](ai/templates.md)**，纪律重写为 4 节 12 条（→ [rounds-61.md](projects/autonomous-driving/history/rounds-61.md)、[ai/rules.md §支线协作纪律](ai/rules.md)）。

**上一轮：第六十轮（2026-09-30）**——整合支线投递：**安装协作纪律**（`ai/rules.md` 新增 §支线协作纪律、`workflows.md` §轮次收尾第 9 步、新建 [history/CURRENT.md](projects/autonomous-driving/history/CURRENT.md)）＋关闭 4 项遗留（补具身 VLA/WM 两表的 §1.1、S2 venue 警告只进 `tools.md`、清理未执行已登记、`/tmp` 违规在规则层堵住）→ [rounds-60.md](projects/autonomous-driving/history/rounds-60.md)。

**逐轮详情以 [autonomous-driving/history.md](projects/autonomous-driving/history.md)（索引 + 42 卷）为准**；当前阶段与待续清单见两个项目的 `state.md`，**本节只留指针、不写结论**（规则见 [ai/workflows.md](ai/workflows.md) §轮次收尾第 3 条）。

| 轮次 | 指针 |
|---|---|
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
| 具身侧（第七、八、二十五、二十六、二十九轮） | [embodied-ai/history.md](projects/embodied-ai/history.md) |

## 等待用户

- 下载付费墙 PDF（**8 条**），清单见 [pdfs_pending.md](projects/autonomous-driving/pdfs_pending.md)
- 为路线 B 实验取得 SimScale 的 DiffusionDrive checkpoint，并准备 NAVSIM v2 `navhard` 数据；协议已写在 [experiments/protocol.md](projects/autonomous-driving/experiments/protocol.md)
- 如要正式立项，仍需用户明确确认；GPU、预算和主基准已经确定，不再作为待决策项

## 想细看时

- 自动驾驶项目进度：[projects/autonomous-driving/state.md](projects/autonomous-driving/state.md)
- 自动驾驶资料导航：[projects/autonomous-driving/index.md](projects/autonomous-driving/index.md)
- 具身智能资料导航：[projects/embodied-ai/index.md](projects/embodied-ai/index.md)
- 研究方法与原则：[shared/research-workflow.md](shared/research-workflow.md)
- 工具与跨项目资料：[shared/index.md](shared/index.md)
