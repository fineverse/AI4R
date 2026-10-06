# 自动驾驶项目状态

更新时间：2026-10-06（阶段 1 事实校准；最近正式研究轮仍为第七十九轮）
逐轮详细记录已迁出至 [history.md](history.md)（**2026-09-23 拆为 5 卷，后续各轮新增，共 61 卷，`history.md` 现为索引**，见 [history/](history/)；同目录 [CURRENT.md](history/CURRENT.md) 为**本轮「在改」文件清单**（软通道，单写者 = 主线程；**第六十七轮起不再登记投递物**——登记表就是 `inbox/` 本身））；本文件只保留当前阶段、待续清单与判断边界。

## 当前阶段

**项目未立项**。文献调研与代码核验已完成（第一至七十九轮），现处于 **idea 讨论 + 实验准备**阶段；最近正式研究轮仍为**第七十九轮（2026-10-01）**。2026-10-05 至 10-06 已完成一批服务器准备与冒烟检查，但它们不是实验结果。

- **逐轮记录**（做了什么、更正了什么、产出在哪）：[history.md](history.md)（索引 + 61 卷，第一至七十九轮全覆盖）。
- **并行会话同步机制**：[ai/rules.md](../../ai/rules.md) §支线协作纪律——写前检查 Git 状态，以目标路径所有权隔离写入，提交只按明确路径暂存；目标重叠时等待、改派或使用 [投递物模板](../../ai/templates.md)。`history/CURRENT.md` 仅用于持续时间较长的并行研究任务。
- **决策核心**：[sota-plan.md](ideas/sota-plan.md)（冲 SOTA 作战文件）、[preparation.md](ideas/preparation.md)（S1–S30 设计前提 + 候选方向）。
- **运行准备现状**：SimScale checkpoint 已取得并校验（243,596,717 bytes；SHA-256 `8fdbdb3f…d963f`），Python 3.9.25 / PyTorch 2.2.1 环境、NAVSIM/nuPlan 运行副本与场景 pickle 已存在；current/history 传感器压缩包已落盘。目前只确认 `unpacked/current`，尚未确认历史帧资产闭合。
- **关键阻塞**：路线 B 协议**尚未正式运行**。真实传感器输入前向仍未通过；agent 声明的 8 相机 × 4 帧输入与本地文件布局尚未闭合，依赖锁定、实际评分路径和 SimScale/NAVSIM 兼容性仍待核验。零输入前向、缓存或评分冒烟均不得写成模型复现成功。

> **本节原有一段"第一至四十八轮日志"，已于 2026-09-30（第五十七轮）删除**：它累积 8000 余字，与 [history/](history/) 逐轮记录重复、且未随第四十九轮以后更新——**这正是"`state.md` 与 `history.md` 轮次不同步"的根因**。按第四十八轮给 README 定的规则（**当前态只留指针、不写结论**）移除；逐轮内容一律看 [history/](history/) 各卷。

**结构**：领域—专题两级树——`direction/`（大方向）+ `topics/`（小方向：`diffusion-planner` 研究对象，`vla` / `world-model` 借鉴来源）。具身智能为平级项目 [embodied-ai](../embodied-ai/index.md)。

**主要产出**：

| 类别 | 内容 |
|---|---|
| 脉络 | [E2E AD](direction/lineage.md)（1989→2026）、[扩散规划器](topics/diffusion-planner/lineage.md)（2022→2026）、[VLA](topics/vla/lineage.md)（四阶段）、[世界模型](topics/world-model/lineage.md)（五类空间 + **五条接口路线**） |
| 协议 | [benchmarks.md](direction/benchmarks.md) — 基准清单 + **NAVSIM 的代码级口径**（PDMS/EPDMS 的权重、乘法项、判定阈值、两阶段聚合；§2.5 另含 **Agent 与评测接口**：契约、输入权限硬边界、8 vs 40 poses、轨迹重仿真）+ **nuPlan 的代码级口径**（§2.6）+ **Bench2Drive 四项指标的代码级口径**（§2.7：DS = `max(RC × IS, 0)`、分母硬编码 220、Effi 是速度比、Comf 是时间占比）+ **nuScenes 开环的代码级口径**（§2.8：**同名 L2/碰撞在 UniAD / VAD / VADv2 / SparseDrive 里是四套不同实现**） |
| 论文表 | [E2E 综述 S001–S045](direction/surveys/e2e_ad_surveys.md)、[研究对象 DP-A01–A34](topics/diffusion-planner/papers/diffusion_planner_ad.md)、[VLA **28** 篇](topics/vla/papers.md)（**第二十四轮从边界外补入 9 篇：VLA-20–28**）、[世界模型 24 篇](topics/world-model/papers.md)；**逐行信息维度按实况分列（第六十轮更正）**——驾驶侧 4 表（DP-A 与 DP-S 的「T 档」、VLA 与 WM 的「§1.1 证据等级与代码状态」）＋**具身 DP-E 表的「T 档」**已补；**具身 VLA / 具身 WM 两表的 §1.1 由第六十轮补上**；**综述 S 表只归档已读全文的 5 篇，其余 40 条标「未核」** |
| 笔记 | 47 篇（领域 16 + 研究对象 14 + 具身 9 + [VLA 3](topics/vla/notes) + [世界模型 5](topics/world-model/notes)）；两借鉴来源**已读全文共 52 篇**（VLA 28 + 世界模型 24，**两表全部读成全文**），其中 **28 篇已做代码核验**（VLA-03/05/**06**/11/12/15/16/17/19/20/21/22/25/27 + WM-01/02/03/04/06/07/10/11/15/16/17/18/20/24），**摘要级 0 篇** |
| 代码 | **37 个官方仓库快照（1.65 GB，未安装未运行）** + 三份[代码脉络](code/traces/)（[扩散规划器侧](code/traces/diffusion_planner_code_traces.md)（**研究对象侧 13 个仓库全部结账：12 逐文件核验 + DriveFine 零代码**）、[世界模型→规划器接口](code/traces/world_model_code_traces.md)（**§E 为 WoTE**）、[E2E 主干](code/traces/e2e_trunk_code_traces.md)）；**VLA 侧在列 8 个仓库全部已源码核验**（结论写在 [vla/verification.md](topics/vla/verification.md) **§4.4**（第三十六轮新增 DiffVLA）与 §5–§7，未另开 trace 文件；其中 7 个**未落盘**，走 API/raw 逐文件取证） |
| 机制 | [transfer.md](topics/diffusion-planner/transfer.md)（来源 → 对象，**§1 现 15 条**——**⚠ 第四十四轮更正**：此处原写 16 条，第三十二轮把 §1 条数改正后漏改的两处之一） |
| 规范 | [文献质量分档](../../shared/literature-quality.md)、[工作空间设计](../../shared/workspace-design.md) |
| idea | [sota-plan.md](ideas/sota-plan.md)（**冲 SOTA 作战文件**：navhard 分数格局——**§1.0 官方公开榜 20 行 + §1 论文口径 13 行**——与逐行代码状态 + 子榜门槛 + 七方向重排 + 四条推荐路线）；[preparation.md](ideas/preparation.md)（**§2 = S1–S30 设计前提清单**、§5.0 = 七方向横向比较、§5 = 7 个候选方向，均未验证）；[recombination-map.md](ideas/recombination-map.md)（**重组地图：结构（血统）× 因果（受控增益）**——**只做连接、不复制论证**，含"结构相邻但因果未测"的 idea 候选区）；[judgments.md](judgments.md)（判断边界详细版**第一册 §A–§D**）+ [judgments-2.md](judgments-2.md)（**第二册 §E–§H**） |
| 工作流 | [ai/rules.md](../../ai/rules.md) 定义证据、路径级协作、耐久资产保护与 Git 安全；[ai/workflows.md](../../ai/workflows.md) 按只读审计、快速维护、研究更新/实验运行、正式里程碑四类分流。提交只暂存明确路径；push 需用户授权；round tag 只在里程碑 commit 后创建。检查器现状见脚本 docstring，阶段 3 将拆分 content/environment/release profile。 |

## 待续清单（没做完的，按优先级）

| # | 事项 | 状态与阻塞原因 | 记录位置 |
|---|---|---|---|
| 6 | 与用户讨论方向，收敛 1–2 个候选 | **标准与资源都已定（2026-09-24）**：① **最终目的 = 发一篇自动驾驶方向 CCF-A 会议论文**（"只要能实现这个目标，其他都可以妥协"）→ **SOTA 是手段不是目的**，评价标准改为「**提点幅度 × 可复现性 × 子榜可辩护性**」的乘积；② **算力 = 自备双卡 RTX 3090（48 GB），出成果后可租到 A800 80G（单卡）** → **直接排除 VLA / 世界模型 / 路线①（DriveFuture 原文 8×5090 / 100 epochs）**，只剩"冻结 + 小规模 + 推理期"。→ **第四十一轮据此重排**：**[sota-plan.md §8](ideas/sota-plan.md)**（B 选优器仍第一，**但目标从"打败 48.0"改成"压缩选优损失"**）；**7.1/7.2 的原始选项表见 [preparation.md §7](ideas/preparation.md)** | [sota-plan.md §8](ideas/sota-plan.md)、[preparation.md §7](ideas/preparation.md) |
| 8 | 用户协助下载 8 篇付费墙 PDF | 待用户。**S034（IEEE Access）2026-10-01 已试直下**：DOI → ieeexplore 返 **202（反爬挑战），命令行不通**，仍需浏览器；S016/S019/S020/S035 的 OA 入口此前已试、一律 403（见 [pdfs_pending.md](pdfs_pending.md) 文内注） | [pdfs_pending.md](pdfs_pending.md) |
| 9 | 代码结论需运行环境才能验证：扩散规划器侧 5 项（§D）+ **§G DIVER 的 `num_cmd` 内部不一致**（**已解决**：是"命令组数"口径误读，见 [C005 §H.3](code/traces/e2e_trunk_code_traces.md)）+ **§H FeaXDrive 的违规率取自哪一列** + **§J HDP 的初始噪声 `0.1` 与训练端 `σ(1)≈1` 的尺度差** + 世界模型侧 5 项 + E2E 主干侧 4 项 | 依赖算力与数据 | 三份 [code/traces/](code/traces/) §D，及 [C003 §G/§H](code/traces/diffusion_planner_code_traces.md) 与 [C003-2 §J](code/traces/diffusion_planner_code_traces-2.md)（⚠ 第七十七轮修错册：§J 在第二册 §I–§P） |
| 10 | **锚点/词表：只剩 VADv2 的 `carla_plan_vocabulary_4096.npy` 需自行重建** | 构造线索已明确（来源 = CARLA GT 轨迹、形状 **(4096,6,2)**、**累积位移空间**、配置注释留了 `#'./gt_trajs.npy'`）→ 缺 **Bench2Drive/CARLA 专家轨迹 + 自写聚类脚本**。其余全部结账（第二十四轮复查）：DiffusionDrive 20 锚点（已下载并与 V2 逐字节比对相同）、SparseDrive 四个 `kmeans_*.npy`（(3,6,6,2) 已实测匹配）、UniAD `motion_anchor_infos_mode6.pkl` 均可直下；DiffusionDriveV2 的 `navtrain_16384.pkl` 有官方 HF 直链但 **30.5 GB**（是成本非缺失，且非推理必需）。**注意** DIVER 的同名 `kmeans_plan_6.npy` 是 (6,6,6,2)，与公开的 (3,6,6,2) **不通用** | [E2E 主干脉络 §H/§H.4](code/traces/e2e_trunk_code_traces.md) |
| 19 | **论文表质量维度的剩余缺口**（第六十三轮分档；已完成的补齐见 [rounds-57.md](history/rounds-57.md)、[rounds-60.md](history/rounds-60.md)） | **② 值得动且便宜（真正的工作项）**：**具身 4 条「代码未核验」**（DP-E13/E24/E26/E27，走 GitHub API/raw 即可，本空间已核过 40+ 仓）＋ **DP-A29 DriveFine**（只需补团队/录用信号；"零代码"已由 [C003 §K](code/traces/diffusion_planner_code_traces-2.md) 结账）＋ **DP-E16**（无代码，只剩团队信号）。**① 判据问题非信息缺口**：DP-S03/S05/S12 venue 不在白名单 → 扩白名单或按 T5 归，没有"去核"动作；**③ 无入口 / 等外部事件**（搁置）：DP-A04/A19/A25/A30/A32/A34、DP-S06/S08/S13、DP-E07、B011；**④ 需用户**：DP-S10（ICTC 2025）。**S 表其余 40 条「未核」永久搁置**（非选题依赖）；具身 VLA+WM 升全文级属"按需" | [rounds-63.md](history/rounds-63.md) |
| 21 | **把数据盘位置改成可配置运行参数** | 当前服务器的数据根已定为 `/root/autodl-tmp/ai4r_navsim`，本会话可读；旧环境的“沙箱白名单阻塞”不再是当前事实。后续需在阶段 4 用配置项替代硬编码，避免换机器后失效。 | [experiments/protocol.md](experiments/protocol.md)、[rounds-66.md](history/rounds-66.md) |
| 22 | **用户侧防丢失事项** | ① 私有远端 ✅（2026-10-04 已建立并推送）；② `.git` 异地备份仍未完成。旧机器的 `~/.bashrc` 本地代理配置不迁移到当前服务器，网络配置按机器分别记录。 | [rounds-67.md](history/rounds-67.md)、[README.md](../../README.md) §等待用户 |
| 23 | **"选优器专线"的待核**（第六十八轮立；**第六十九轮解 ①、第七十轮解 ⑤**） | ~~① TOAD 的 56.3 属哪个 split~~ → **✅ `navhard-two-stage`**；~~⑤ TOAD 代码是否发布~~ → **✅ 已发布**（`valeoai/TOAD` 25★，`scorer.py` + `train_pdm_scorer.py` 都在）——**它因此成为方向 B 的"可运行直接对手"**。**剩余**：② **Vault 是否已中稿**（摘要写 "Under review at ICLR 2027"）**与有无代码**；③ [scoring_line.md](topics/diffusion-planner/papers/scoring_line.md) **§二 15 条线索级**（arXiv ID / venue / 代码全未核）；④ BeyondDrive 的 **"MeanFuser 同组"与"有代码"**（摘要均未提）；⑥ **TOAD 的 56.3 / 56.512 两个数字均未被独立复现**（论文自报 vs 官方榜，差 0.2） | [scoring_line.md](topics/diffusion-planner/papers/scoring_line.md)、[rounds-69.md](history/rounds-69.md) |
| 24 | **官方榜的三项未查事项**（第七十轮立） | ① **`DriveFuture` 为何不在官方榜**（全文检索 0 命中）——未提交？还是用了另一套评测？**这个决定了 §1 与 §1.0 能否被看成"同一基准的两套数字"**；② **官方榜前 6 名里 4 个匿名队**（`guest9527` 60.561 / `CooWAIM` / `Aqua10086` / `zzzzz` / `Joctor`）身份未知，**榜首不可追溯**；③ **榜二的 `EABOT.AI&NJU` 与 `Rtwotwo/DriveTTO` 的对应关系未证实**（榜上无链接，且该仓是占位仓）。→ **这三项直接影响"子榜辩护"能不能写**，优先级高于 ②③④ | [sota-plan.md §1.0](ideas/sota-plan.md)、[judgments.md B 组](judgments.md) |
| 25 | **官方榜是"易失效事实"，需定期重取**（第七十轮立） | 榜单**每天都在变**（20 行里有 11 行的提交日期在 2026-09）→ §1.0 的快照**会过期**。**已固化做法**：`ai/workflows.md` **§周扫**的"榜单线"（成本 = 1 次 POST）。**取数日期必须随数字一起写**（现为 2026-09-30） | [ai/workflows.md](../../ai/workflows.md) §周扫、[sota-plan.md §1.0](ideas/sota-plan.md) |
| 26 | **文档体积：政策已定、两份决策文件仍在预警带**（第七十三轮立、**第七十四轮已处理**；**第七十六轮确认"暂缓拆册"判断**） | **政策（第七十四轮）**：实测确认 **64 KiB 是 Read 工具硬上限**（整读 67 KB 报 `exceeds the limit of 64KB`）→ 定**两线制**（硬线 64 KiB / 预警线 60 KiB）与**按文件角色分档**处理，落 [ai/rules.md](../../ai/rules.md) §文件更新 + `check_links.py` 第 12 项。**已处理**：① `history.md` **66 KB → 9.6 KB**（索引类**瘦身**，信息全在各卷）；② `sota-plan.md` **67,243 → 65,215 B**（决策类**去重**：§7.7.2 / §7.7.4 / §7.7.5 中与 `judgments`·`benchmarks` 重复的长引文压成"摘要 + 指针"）→ **`check_links.py` 恢复 exit 0**。**仍遗留（预警、未超线）**：~~`sota-plan.md` 距硬线 321 B、`preparation.md` 距硬线 636 B~~ → **✅ 第七十八轮已双双出预警带**（sota-plan 65,256 → **61,250 B**：§6 指针化 + §7.6.1/§7.7.4/§7.7.5/§9.5/§9.7 瘦身；preparation 64,919 → **60,201 B**：§5.0/§5.1 收拢 + 方向 A/B 卡片压缩）——但余量仍薄（190 / 1,239 B），**零和编辑纪律**已写入 [ai/rules.md](../../ai/rules.md) §文件更新（预警带内新增 N 字节须同步删 ≥N）。**可持续解（判为成本高、暂缓）**：拆册——但 `sota-plan.md` 有 **66 处**跨 §7–§10 引用（分布 26 个文件），且拆点**两侧互相引用**（非"引用最少"边界）。**✅ 第七十六轮主线程确认暂缓成立**，并加一条硬约束：**这两个文件在瘦身之前不得再追加**（本轮要写进 `sota-plan` 的结论已改落到 [recombination-map.md](ideas/recombination-map.md)）——**这是新政策第一次实际生效**（第七十七轮注：**本条取代并关闭原 #16**"撞线先拆 preparation-2.md"——拆册判暂缓后两条并存矛盾，以本条硬约束为准） | [ai/rules.md](../../ai/rules.md) §文件更新、[shared/scripts/check_links.py](../../shared/scripts/check_links.py) 第 12 项、[rounds-74.md](history/rounds-74.md)、[rounds-76.md](history/rounds-76.md) |
| 27 | **TOAD 的 related work 引了一句"oracle studies"，未核**（第七十六轮立） | TOAD 论文原文："**oracle studies show an ideal selection can beat the human driver [53], suggesting the candidate set, not the scorer, often limits performance**"。**这条直接关系到 ③（navhard 池子天花板是否真的无人报告）**：若 [53] 是**在 navhard 上**做的 oracle 研究，③ 就不成立。**候选**：[53] 可能是 GTRS（它的 Table 1 是 navhard 池子表）、也可能是 DDV2 的 navtest `PDMS@1`（但那不在 navhard）。**待办**：读 TOAD PDF 的参考文献 [53] 定位。**同时**：**Vault 是否报 navhard 天花板也未核**（摘要未提）。**落点（第七十八轮定）**：结论写入 [recombination-map.md](ideas/recombination-map.md) 或 [scoring_line.md](topics/diffusion-planner/papers/scoring_line.md)——**不进 `sota-plan.md`**（该文件已按零和纪律管理，见 #26） | [sota-plan.md §9.5](ideas/sota-plan.md)、[recombination-map.md](ideas/recombination-map.md) §交叉结论 3、[rounds-76.md](history/rounds-76.md) |
| 28 | **navhard 竞品表的 2 处待核**（第七十七轮从表内升入） | ① **DP-C04 ZTRS**：自报 **45.5** vs 本表 **48.1**（差 2.6，与"两套 EPDMS 实现"的差同量级，**原因待核不可断言**）；② **DP-C06 DriveZero**：venue 与机制标签未核（真实仓 117★，官方公开榜里"有仓库"的最高一条） | [navhard_competitors.md](topics/diffusion-planner/papers/navhard_competitors.md) DP-C04/C06 行 |
| 29 | **引用数口径统一的三条可选补齐**（第五十九轮 §五立，**等用户定优先级**） | ① 具身 WM / DP-E 表（现为 OpenAlex，系统性低估）；② E2E 综述 S 表（OpenAlex 2026-09-20 快照）；③ 驾驶侧 VLA / WM 表。**不建议无差别全补**——引用数只是辅助判据，本空间的排序依据是 T 档与代码可得性 | [rounds-59.md](history/rounds-59.md) §五 |

> **编号约定（第七十七轮定）**：① **编号 14 已于第二十七轮完成并删除**（[rounds-27.md](history/rounds-27.md)）；**编号不复用、不重排**——外部「待续第 N 项」引用（README、profile、judgments、traces、sota-plan 等）不受清账影响。② 第七十七轮清账删除的已结账行（原 #1–3 / #4–5 / #7 / #11 / #12 / #13 / #15 / #16 / #17 / #18 / #20）记录在各轮卷与其「记录位置」所指文件。

## 当前判断边界（索引）

**67 条判断的完整论证、出处与代码事实见 [judgments.md](judgments.md)（第一册 §A–§D）+ [judgments-2.md](judgments-2.md)（第二册 §E–§H）**（已按 A–H 分组；本表只留分组索引，便于整读）。**第三十六轮已按既定约定拆册**（第一册 31 KB / 第二册 33 KB，均远低于 64 KB 上限）。

| 组 | 主题 | 条数 |
|---|---|---|
| **A** | 证据边界与工作空间状态（立项、只克隆、未复现、引用数口径） | 6 |
| **B** | 指标与基准口径——为什么跨论文数字不可横比（含 **navhard 13 行对照**、**"scorer ≈ +20" 的成立条件**、**三份 navhard 表的交叉核对**、**EPDMS 的两套官方实现**、**EC 不进分 + 本地 devkit 口径 + changelog 时间线**、**"论文里的表 ≠ 官方榜" + "仓库存在 ≠ 有代码"**） | 11 |
| **C** | "生成式 / 扩散"这个词的真伪（含**八类"名字≠实际"陷阱**） | 7 |
| **D** | 锚点 · 词表 · 选优（含**"选优损失"是可测量**：`PDMS@1` = 池子天花板；**"候选池越大越好"是错的**；**"做选优"已被 TOAD 的"测试时搜索"占据**——论文口径榜一 56.3 / 官方榜 #8 56.512、头部被压平、**代码已发布**） | 12 |
| **E** | RL 与可行性 | 7 |
| **F** | 逐方法的代码级结论（世界模型侧 + 研究对象侧，含 36 仓结账） | 12 |
| **G** | 非生成式基线与特权信息 | 6 |
| **H** | VLA 与具身侧 | 6 |
