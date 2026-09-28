# 自动驾驶项目 · 逐轮工作记录 · 第一至第八轮

本卷范围：**第一至第八轮**。内容：通用检索、扩散规划器专题建表与补全文、消化整理、知识体系重构（树状化 + 二次优化）。
索引见 [../history.md](../history.md)；当前状态见 [../state.md](../state.md)。

---


## 通用（非专题轮次）

- 检索 2024–2026 年自动驾驶端到端相关综述 45 篇（S001–S045），建表分级
- 阅读 DiffusionDrive v3 正文/附录文字，静态检查官方 NAVSIM 分支核心代码（未运行）
- 核验 NAVSIM、Bench2Drive、nuPlan、nuScenes、Waymax、MetaDrive、Waymo、Argoverse 2 官方说明
- 解析《第七版 CCF 推荐国际学术会议和期刊目录（2026 正式版）》为结构化数据 681 条，落地 [shared/ccf/](../../../shared/ccf)

## 扩散规划器专题 · 第一轮（检索与建表）

- 8 组 arXiv API 查询 + 4 个并行子代理检索；77 个候选 arXiv ID **全部核验命中**，无编造 ID
- 综述表 DP-S01…DP-S14（含 3 条待核验付费墙条目），确认"引导/约束"无专题综述
- AD 论文表 DP-A01…DP-A34、具身表 DP-E01…DP-E28（含可迁移机制）
- 用 arXiv PDF + `pdftotext -layout` 补齐 5 篇论文的表格数值（HTML 转换会丢表格单元格）
- 克隆 12 个官方代码仓库并记录 commit（约 450 MB）；4 个因 TLS 中断未获取

## 扩散规划器专题 · 第二轮（补齐关键全文）

- 全文提取 13 篇（约束/引导路线 6 篇 + 具身奠基 7 篇），笔记累计 21 篇
- **更正 1**：2305.20081 是 EDP 而非 Diffusion-QL；Diffusion-QL 真实 ID 为 [2208.06193](https://arxiv.org/abs/2208.06193)，已分列为 DP-E03 / DP-E28
- **更正 2**：PC-Diffuser（DP-A21）已在**驾驶域**给出认证级硬约束（逐去噪步 CBF-QP + Thm.1/Cor.1，nuPlan all-collision CR 100%→10.29%），代价约 2 fps；此前"驾驶域无硬约束"的初判已修正
- 新增可测证据：FeaXDrive 报 DiffusionDrive 曲率违规率 8.59%（自身 0.88%）；约束之间会互相干扰；PDMS 与可行性不一致
- 更新 [ideas/preparation.md](../ideas/preparation.md)：新增 P2b/P2c、约束位置三路线对立（去噪内 / 结构层 / 软引导）、方向 A 重写

## 扩散规划器专题 · 第三轮（渠道与预印本）

- 渠道核验：Semantic Scholar API **仍为 429 不可用**（重试 3 次）；**OpenReview API 可用**；TechRxiv 返回 403；arXiv 预印本为主要全文来源
- **更正 3**：此前"OpenAlex 引用数不可用"是错误判断——按 arXiv DOI 查到的是存根记录（一律 0 引用），按标题取正式版记录即可（DiffusionDrive 81、GoalFlow 28、Diffusion Policy 531）；同时确认 PMLR/ICML 类论文引用数被低估，不用于排序
- 付费墙条目预印本核查：S001、S031、DP-S11 均有 arXiv 预印本，**已改为自行取全文**；用户待下载项从 6 条降到 3 条
- 新发现漏掉的一篇同题综述：Generative AI for Autonomous Driving: A Review（[2505.15863](https://arxiv.org/abs/2505.15863)，DP-S15）
- 6 篇综述预印本全文提取（S001/S031/S032/S033/DP-S11/DP-S15），笔记累计 **27 篇**（论文 21 + 综述 6）
- **更正 4**：HDP（DP-A06）此前误记为"无代码"，官方实现是 [Hyper-Diffusion-Planner](https://github.com/ZhengYinan-AIR/Hyper-Diffusion-Planner)；新发现 PC-Diffuser（Eugene29/PC-Diffuser）与 FeaXDrive（BaoyunWang/FeaXDrive）也有官方代码
- preparation.md 新增第 2b 节：四篇 2024–2026 综述在"实时性 / 评价协议 / 安全保证"三点上**收敛一致**，并整理出"约束放在哪一层"的**四种立场**（去噪内 / 结构层 / 生成后否决 / 软引导）

## 扩散规划器专题 · 第四轮（两条发展脉络 + 代码补齐）

- 新建两条脉络：**[E2E AD 发展脉络](../direction/lineage.md)**（1989→2026，四阶段 + 三条轴 + 评价协议演进 + 代表基线技术细节表）与 **[扩散规划器发展脉络](../topics/diffusion-planner/lineage.md)**（2022→2026，五阶段 + 三次转移 + 代码级继承关系）
- 关键发现 1：**VADv2（ICLR 2026）的动作词表概率分布是 DiffusionDrive 锚点先验的思想前身**，Hydra-MDP 明写 "Following VADv2"——"多模态候选 + 先验词表"不是扩散带来的
- 关键发现 2：**非生成式的 VADv2（NAVSIM 89.3）与 Hydra-MDP（91.0）并不低于 DiffusionDrive（88.1）**（backbone 不同不可横比，但说明生成式机制非性能充分条件）
- 关键发现 3：驾驶扩散规划器几乎全部长在 **NAVSIM** 或 **nuPlan/PLUTO** 两个代码生态上；**更正**：HDP 仓库同仓提供 navsim 与 nuplan 两套实现，说明代码层跨生态已打通，**仍成立的是"没有工作在同一基准上对比两个生态的方法"**
- 新增笔记：E2E 代表工作 5 篇（UniAD/VAD/VADv2/SparseDrive/Hydra-MDP）+ S002 综述，笔记累计 **33 篇**
- E2E 综述全文可得性核实：6 篇中仅 **S002** 可得（其余 S016/S018/S019/S020/S035 均 403 且无 arXiv 预印本），已记入两处
- **代码补齐（多重试 + tarball 兜底生效）**：新增 DiffusionDriveV2、Diffusion-Planner、GoalFlow、MeanFuser、Hyper-Diffusion-Planner、PC-Diffuser、FeaXDrive、UniAD、VAD 等；并更正 4 处仓库名（CIL=LBC 与 SparseDrive、Hydra-MDP 我原先记错）

## 扩散规划器专题 · 第五轮（早期主干补齐 + 代码脉络）

- E2E 早期主干 6 篇全文提取（ChauffeurNet、TransFuser、TCP、ST-P3、DriveVLM、DriveLM），E2E 笔记累计 11 篇、总笔记 **39 篇**
- 新增结构观察：**特权信息三段式**（输入即特权 → 输入侧去特权 → 特权作可选辅助/提示），并核验 VLM 支线与传统 E2E 的接口差异（DriveLM **0.16 FPS**，约 10× 慢于 UniAD）
- 新建 [code/traces/diffusion_planner_code_traces.md](../code/traces/diffusion_planner_code_traces.md)：**主张—代码对照 10 项 + 组合关系 6 项**（静态检查）。关键证据：锚点词表是 `kmeans_navsim_traj_20.npy`（**20 条锚点**）、V2 另有 `gtrs_traj/16384.npy`（16384 条轨迹词表，论文未展开）、MeanFuser 配置 `num_sample_steps=1` / `num_proposals=8`、PC-Diffuser 的 CBF 实现位于其 submodule 的 `safety/pc_diffuser/` 与 `safety/mpc_cbf/`
- 代码快照从 29 增至 **32 个仓库（约 1.5 GB）**：transfuser、GenAD、DriveLM 补齐；PC-Diffuser 的两个 git submodule 也已取出（分支 `public`）
- 约束条件记录：**GitHub API 未认证额度已耗尽（403 rate limit）**；E2E 综述的 OA 入口（ACM/MDPI/TechRxiv）一律 403，全文确实不可得
- 代码脉络追加 5 项静态核验结论：DiffusionDrive 的截断实现为**噪声加在 t=8（共 1000 步）**、`step_num=2`；V2 模型输出含 `reward`/`sub_rewards`（16384 词表用于奖励而非先验）、GRPO 以 `all_log_probs [B, G*N, step_num]` 分组记录；PC-Diffuser **自带 QP 求解器**（未调 cvxpy）、屏障为线性间距 `h = D − (r_e+r_n)`；MeanFuser 的 `ARMModel` 独立成模块

## 第六轮（消化与工作空间整理，2026-09-23）

- **全文覆盖核查**：临时目录中提取的 **37 个 arXiv 全文 ID 全部已在工作空间登记，无遗漏**；其中 31 篇有单篇笔记，6 篇（DP-A04/A05、DP-E02/E03/E12/E28）登记为"仅表格一行"，但表格行已含生成机制、基准数值与消融（等价于笔记粒度），**未另建笔记**
- **结论**：全文事实已全部沉淀到表格/笔记/脉络，**删除临时目录不丢信息**（清单与一次性命令见 [inbox/cleanup.md](../../../inbox/cleanup.md)）
- **一致性修复**：修正 `state.md` 自身失真（"两轮"→五轮、仓库数 12/16→32/32、"OpenAlex 不可用"与更正 3 矛盾）、`project.md`（"12 篇笔记"→39）、`index.md` 与 `sources.md`（"未获取仓库"已全部获取）、`README.md`（待下载 PDF 由 3 条更正为 **8 条**）、`pdfs_pending.md` C/D 节（4 个仓库已补齐）
- **导航修复**：21 篇扩散侧论文笔记此前无任何入链，已在 [sources.md](../sources.md) 增加聚合条目 L013
- **执行与清理纪律**：新增"中间产物单一根 `/tmp/ai4r/` + 流程中不删除 + 收尾一次性清理"，写入 [AGENTS.md](../../../AGENTS.md)、[ai/rules.md](../../../ai/rules.md) 与 [workspace-design.md](../../../shared/workspace-design.md) 运行纪律第 9 条

## 第七轮（知识体系重构：树状化，2026-09-23）

- 项目由 `diffusiondrive` 改名为 **`autonomous-driving`**（大方向命名）；具身智能独立为平级项目 [embodied-ai](../../embodied-ai/index.md)
- 项目内改为**领域—专题两级树**：`direction/`（大方向：脉络 + 基准 + 领域级综述与笔记）、`topics/`（小方向：脉络 + 论文表 + 笔记 + 代码）
- 小方向划分：`diffusion-planner`（**研究对象**，最厚）、`vla` 与 `world-model`（**借鉴来源**）
- 新增 [transfer.md](../topics/diffusion-planner/transfer.md)：把"来源 → 对象"的可借鉴机制从 `preparation.md` 抽为独立文件，跨领域借鉴由此承载，不共享文档
- 新增 [direction/benchmarks.md](../direction/benchmarks.md)：基准与评价协议从 `context.md` 与来源索引中抽出，成为大方向公共资产
- 迁移采用 `mv` + 全量相对链接重写（207 处链接规范化，死链 0）；39 篇笔记数量守恒（领域 15 + 对象 15 + 具身 9）；32 个代码仓库完整保留
- 组织约定上升为规则：`shared/workspace-design.md` 新增「领域—专题骨架」，`ai/templates.md` 新增脉络 / README / transfer 三个模板

## 第八轮（结构复查与二次优化，2026-09-23）

- **归属修正**：`code/` 从 `topics/diffusion-planner/` 上移到**项目根**——其内容跨三层（研究对象 13 / 领域级 E2E 主干 13 / 具身侧 6 个仓库），放小方向下是错的
- **去重复**：`ideas/preparation.md` 第 4 节的机制表删除，只留指针；机制正式副本统一在 [transfer.md](../topics/diffusion-planner/transfer.md)（此前两处各写一份，违反单一事实源）
- **命名清理**：`topics/<x>/topic.md` 改为 `README.md`（目录入口约定）；`shared/domain/ccf/` 上提为 `shared/ccf/`（去掉多余层级）；`S031` 笔记按"跟着所属表走"归入 [direction/notes/](../direction/notes)（领域笔记 16、研究对象笔记 14）
- **规则追上实际**：`ai/templates.md` 的「论文阅读笔记」模板重写为与实际笔记一致的格式；`ai/workflows.md` 新增「脉络梳理」工作流；`shared/workspace-design.md` 原则 2 与原则 6 的矛盾（"单个课题" vs "一个领域"）已统一
- **归档**：重构方案移入 [archive/plans/](../../../archive/plans)（历史留痕，默认不加载）
- 链接 300 处全部有效，死链 0
