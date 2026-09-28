# 扩散规划器相关综述（2022–2026）

更新时间：2026-09-22  
检索对象：以"扩散模型 / 流匹配用于规划与决策"为核心，主方向自动驾驶（端到端轨迹规划），次方向具身智能（机器人决策、操作、导航）。  
本表与 [E2E-AD 综述表](../../../direction/surveys/e2e_ad_surveys.md)（编号 S001–S045）并列，不重复登记其中已有条目，交叉条目在 D 组指向原编号。

## 纳入与证据规则

- **A：直接主题综述**：标题或主要分类直接围绕"扩散/流匹配 + 规划或决策"。
- **B：主方向综述**：自动驾驶中的生成式规划、轨迹规划、生成式驾驶全景；扩散只是其中一类。
- **C：次方向与专题**：机器人操作扩散策略、世界模型、运动规划、RL×扩散、受控扩散理论。
- **D：交叉引用**：已登记在 E2E-AD 综述表中的条目，此处只给指针。
- **E：待核验**：仅拿到索引级信息或链接未能打开，不作为结论依据。

证据状态沿用本项目约定：`元数据`（索引/DOI）、`摘要`（已读官方摘要）、`全文`（已读正文）、`目录`（已读可访问 HTML 章节结构）。

引用数说明（**2026-09-22 更正**）：此前记录"OpenAlex 引用数不可用"是**判断错误**——当时只查了 arXiv 的 DOI 存根记录（这些记录一律显示 0 引用）。OpenAlex 对同一工作常有多条记录，**正式版记录才有真实引用数**（例如 DiffusionDrive 的 arXiv 记录 0、CVPR 记录 81）。正确做法是按标题检索取正式版记录。下表为按此方法取到的快照（低相似度匹配一律不采用）：

| 综述 | 引用数（OpenAlex 快照 2026-09-22） | 备注 |
|---|---|---|
| S001 End-to-End AD: Challenges and Frontiers | **570**（TPAMI 正式版） | arXiv 存根记录仅 22 |
| S031 Diffusion Models for ITS | 20（IEEE TITS 正式版） | arXiv 存根记录仅 2 |
| DP-S03 Diffusion models for robotic manipulation | 30（Frontiers 正式版） | — |
| DP-S01 Diffusion Models for RL: A Survey | 12 | 仅 arXiv 记录，**无正式版 DOI，引用数被低估** |
| DP-S11 Generative AI for AD | 1（ACM CSUR 正式版） | 2026 新综述 |
| DP-S12 A Survey on Diffusion Policy for Robotic Manipulation | 3（TechRxiv） | — |

**重要限制**：PMLR/ICML 等无 DOI 的会议论文在 OpenAlex 只有 arXiv 记录，引用数被严重低估（如 Diffuser 显示 62、Decision Diffuser 显示 32，明显低于实际）。因此引用数只能作粗略参考，不能作为影响力排序依据。

## A. 直接主题：扩散 / 流匹配 + 规划决策

| ID | 级别 | 综述（原题） | 作者（首位/等） | 载体、年与版本 | 核心范围与分类框架 | 资产 | 与扩散规划器的关系 | 证据状态 |
|---|---|---|---|---|---|---|---|---|
| DP-S01 | A | [Diffusion Models for Reinforcement Learning: A Survey](https://arxiv.org/abs/2311.01223) | Zhengbang Zhu et al. | arXiv 2311.01223v4，2023-11 首发 | 按扩散模型在 RL 中的三种角色分类：规划器 / 策略 / 数据合成器 | [Diff4RLSurvey](https://github.com/apexrl/Diff4RLSurvey) | 把"扩散规划器"作为一类角色系统定位，是入门该子领域的框架性入口 | 元数据 + 摘要 |
| DP-S02 | A | [Diffusion Models for Reinforcement Learning: Foundations, Taxonomy, and Development](https://arxiv.org/abs/2510.12253) | Changfu Xu et al. | arXiv 2510.12253v1，2025-10；标注 Under Review | 双轴分类：功能角色 × 在线/离线，含多智能体 | [D4RL-FTD](https://github.com/ChangfuXu/D4RL-FTD) | DP-S01 的更新版框架，可用于定位"扩散规划器 + RL 微调"这一支 | 元数据 + 摘要 |
| DP-S09 | A | [FlowRL: A Taxonomy and Modular Framework for Reinforcement Learning with Diffusion Policies](https://arxiv.org/abs/2603.27450) | Chenxiao Gao et al. | arXiv 2603.27450v2，2026-03；RLC 2026 录用 | 扩散/流策略的 RL 算法分类 + 引导机制模块化框架 | [flow-rl](https://github.com/typoverflow/flow-rl) | 直接对应 DIVER、DiffusionDriveV2、DIPOLE 这一支"生成式规划器 + RL"路线 | 元数据 + 摘要 |
| DP-S14 | A（实证研究，非综述） | [What Makes a Good Diffusion Planner for Decision Making?](https://arxiv.org/abs/2503.00535) | Haofei Lu、Dongqi Han、Yifei Shen、Dongsheng Li | arXiv 2503.00535v1，2025-03；ICLR 2025 Spotlight | 在离线 RL 设定下训练并评估 6000+ 个扩散模型，系统检验引导采样、网络结构、动作生成、规划策略 | [DiffusionVeteran](https://github.com/Josh00-Lu/DiffusionVeteran) | 直接约束设计选择：摘要称"无引导采样 + 选择可优于引导采样""Transformer 优于 U-Net"，与常见做法相反 | 元数据 + 摘要；**2026-09-23 代码核验：三条引导路线（MCSS/cfg/cg）在同一 planner 上并列实现，消融网格见 [代码脉络](../../../code/traces/diffusion_planner_code_traces.md) §C** |

## B. 主方向：自动驾驶中的生成式规划与轨迹规划

| ID | 级别 | 综述（原题） | 作者（首位/等） | 载体、年与版本 | 核心范围与分类框架 | 资产 | 与扩散规划器的关系 | 证据状态 |
|---|---|---|---|---|---|---|---|---|
| DP-S04 | B | [Foundation Models for Trajectory Planning in Autonomous Driving: A Review](https://arxiv.org/abs/2512.00021) | Kemal Oksuz et al. | arXiv 2512.00021v2，2025-10 首发；标注 TMLR Survey Certification | 37 种轨迹规划方法的层次化分类，覆盖生成式/扩散类规划器 | [FMs-for-driving-trajectories](https://github.com/fiveai/FMs-for-driving-trajectories) | 主方向最直接入口：把扩散规划器放进"基础模型做轨迹规划"的整体分类中 | 元数据 + 摘要 |
| DP-S11 | B | [Generative AI for Autonomous Driving: Frontiers and Opportunities](https://doi.org/10.1145/3838726)（预印本 [arXiv 2505.08854](https://arxiv.org/abs/2505.08854)） | Yuping Wang et al. | ACM Computing Surveys，2026-08-07；arXiv v1 2025-05-13 | §5.3+Table 7 把扩散类轨迹生成单列（Diffusion-Planner、MotionDiffuser、SDT、DJINN、Scenario Diffusion）；§6.2 列 DiffusionDrive、DiffAD、GoalFlow；§8 讨论 18 小节 | 未核验 | **已读全文**（[笔记](../notes/DP-S11-generative-ai-ad.md)）。关键立场：扩散是轨迹生成 SOTA 但实时部署困难；**§8.9 主张生成式规划器需外部规则式 "safety governor" 否决越界轨迹**——这是"约束放在生成之后"的第三种立场 | 全文（预印本 PDF） |
| DP-S15 | B | [Generative AI for Autonomous Driving: A Review](https://arxiv.org/abs/2505.15863) | Katharina Winter et al. | arXiv v1 2025-05-21；comments 称已投 IEEE | 生成模型两分（可逆类 / 隐式类含 DM）；§VI 运动规划列 CoBL-Diffusion、SafeDiffuser（CBF）、DDM-Lag、扩散物理 MPC；§VII E2E 按 DM/VAE/Transformer/LLM 分类 | 未核验 | **已读全文**（[笔记](../notes/DP-S15-generative-ai-ad-review.md)）。最有价值的是对评价的批评：多数生成式规划器只优化开环；E2E 闭环下常输给更简单方法；NAVSIM 缺反应性、CARLA 有 sim-to-real gap | 全文（预印本 PDF） |
| DP-S10 | B | [A Survey on Flow Matching for Robotic Trajectory Generation and Control](https://doi.org/10.1109/ICTC66702.2025.11388651) | 未核验 | ICTC 2025，2025-10-14 | 流匹配用于机器人轨迹生成与控制 | 未核验 | 流匹配是本项目主方向 2025–2026 的主要竞争路线（GoalFlow、FlowDrive、WAM-Flow 等） | 元数据（Crossref 核验；作者与摘要未取到） |

## C. 次方向与专题

| ID | 级别 | 综述（原题） | 作者（首位/等） | 载体、年与版本 | 核心范围与分类框架 | 资产 | 与扩散规划器的关系 | 证据状态 |
|---|---|---|---|---|---|---|---|---|
| DP-S03 | C | [Diffusion models for robotic manipulation: a survey](https://arxiv.org/abs/2504.08438) | Rosa Wolf et al. | arXiv 2504.08438v3，2025-04；Frontiers in Robotics and AI，2025-09-09，[DOI](https://doi.org/10.3389/frobt.2025.1606247) | 抓取、轨迹扩散、数据增强；模仿学习与 RL 两套框架；含 receding horizon 与 DiT 技术表 | 未核验 | 具身侧最完整的扩散策略综述，是"可迁移机制"清单的主要来源 | 元数据 + 摘要（两处链接均已核验） |
| DP-S12 | C | A Survey on Diffusion Policy for Robotic Manipulation: Taxonomy, Analysis, and ... | 未核验 | TechRxiv，2025；[DOI 10.36227/techrxiv.174378343.39356214](https://doi.org/10.36227/techrxiv.174378343.39356214) | 机器人操作扩散策略的分类与分析 | 未核验 | 具身侧扩散策略专题；**OpenAlex 已确认该记录存在（2025，3 次引用）**，但 TechRxiv 页面返回 403，全文暂不可取 | 元数据（OpenAlex 核验；Crossref 未命中） |
| DP-S05 | C | [A Comprehensive Review of Generative Physical Artificial Intelligence](https://arxiv.org/abs/2609.18111) | Satyam Gaba et al. | arXiv 2609.18111v1，2026-09-16；[IEEE IoT-J](https://doi.org/10.1109/JIOT.2026.3671268) | 五类生成式物理 AI：RFM / VLA / LBM / DPM（扩散物理模型）/ WFM | 未核验 | 提供"扩散物理模型"这一上位概念，便于把规划器与物理约束结合 | 元数据 + 摘要 |
| DP-S06 | C | [Ergodic Control and Controlled Diffusion for Robot Learning: Review and Tutorial](https://arxiv.org/abs/2609.13295) | Max Muchen Sun et al. | arXiv 2609.13295v1，2026-09-09；标注 under review at Foundations and Trends in Robotics | 受控扩散与遍历控制的理论综述与教程 | 未核验 | 若要把安全/可行性约束写进生成过程，这是理论工具入口（对应 CBF、引导采样一类做法） | 元数据 + 摘要 |
| DP-S07 | C | [Robotic Video World Models: A Survey](https://arxiv.org/abs/2601.07823) | Zhiting Mei et al. | arXiv 2601.07823v2，2026-01-12 | 视频扩散/流匹配世界模型在机器人中的应用与挑战 | [awesome-robotics-video-world-model-papers](https://github.com/irom-princeton/awesome-robotics-video-world-model-papers) | 对应驾驶侧 DriveFuture 等"世界模型条件化扩散规划器" | 元数据 + 摘要 |
| DP-S08 | C | [A Review of Learning-Based Motion Planning: Toward Data-Driven Optimal Control](https://arxiv.org/abs/2512.11944) | Jia Hu et al. | arXiv 2512.11944v2，2025-12-12（44 页） | 学习式运动规划全景，含生成式方法与安全权衡 | 未核验 | 提供"生成式规划 vs 优化式规划"的对照视角与安全评价维度 | 元数据 + 摘要 |

## D. 交叉引用（已在 E2E-AD 综述表中登记）

以下 4 篇已通过 arXiv 预印本读到全文，笔记单独成文件：

| 原编号 | 综述 | 笔记 | 与本表的关系 |
|---|---|---|---|
| S001 | End-to-End Autonomous Driving: Challenges and Frontiers（TPAMI 2024） | [笔记](../../../direction/notes/S001-end-to-end-ad-survey.md) | E2E 通用骨架；**全文只在 §4.3 一句话提到扩散**，无生成式规划器类别，不能用于定位扩散规划器 |
| S031 | Diffusion Models for Intelligent Transportation Systems: A Survey（TITS 2025） | [笔记](../../../direction/notes/S031-diffusion-its-survey.md) | 扩散 + ITS 上位综述；§IV.A.3 的 Planning 支线直接对应本项目；明确指出实时性（MID 100 步需 17 秒）与无统一评测 |
| S032 | Planning-Oriented End-to-End Autonomous Driving（arXiv 2608.20111） | [笔记](../../../direction/notes/S032-planning-oriented-e2e.md) | 本项目**规划口径主锚**；四轴 taxonomy 与比较口径一致；§VII.C 反对设单一 best method |
| S033 | Post-Training in End-to-End Autonomous Driving（arXiv 2607.08072） | [笔记](../../../direction/notes/S033-post-training-e2e.md) | 扩散/流匹配后训练的分类与批评；§8 点名"超越 GRPO"是空白 |

| 原编号 | 综述 | 与本表的关系 |
|---|---|---|
| S025 | A Survey of Autonomous Driving Trajectory Prediction（Machines 2025） | 轨迹预测中的扩散方法，与规划器共享输出表示 |
| S034 | Diffusion Models for End-to-End Autonomous Driving: A Survey（IEEE Access 2026） | 扩散 + E2E 的 perception/prediction/planning/control 五分类，最直接的驾驶侧扩散专题；**无 arXiv 预印本，待用户下载** |

## E. 待核验

| 条目 | 索引信息 | 缺什么 |
|---|---|---|
| DP-S13 | Diffusion Policies for Embodied Robotic Intelligence: A Survey；ICICC 2026 | 无 arXiv 记录，未找到可核验入口（OpenAlex 也无匹配记录） |
| DP-S10 | A Survey on Flow Matching for Robotic Trajectory Generation and Control；ICTC 2025，[DOI](https://doi.org/10.1109/ICTC66702.2025.11388651) | Crossref 元数据已核验（会议论文），但 **OpenAlex 无匹配记录、arXiv 无预印本**；作者、摘要、分类框架均未取到，需 IEEE 全文 |

## 本次检索确认的空白

未检索到**专门针对"扩散引导采样 / 安全约束注入"的专题综述**：现有引导与约束内容多内嵌于上表综述，或散落在单篇方法论文中（如 SafeFlowMatcher、PC-Diffuser、G2SD、LSC）。若后续 idea 落在"约束/引导"，需要自己从方法论文汇编，而不是引用现成综述。

## 优先阅读顺序

1. **先定位子领域**：DP-S01 → DP-S14（框架 + 设计选择的实证结论）。
2. **再固定主方向口径**：DP-S04 → S032 → S034 → S031。
3. **再看 RL 支线**：DP-S02 → DP-S09 → S033。
4. **最后取可迁移机制**：DP-S03 → DP-S07 → DP-S06。
