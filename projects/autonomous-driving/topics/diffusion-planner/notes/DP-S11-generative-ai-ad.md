# DP-S11 · Generative AI for Autonomous Driving: Frontiers and Opportunities（ACM CSUR 预印本全文）

- **原题**：Generative AI for Autonomous Driving: Frontiers and Opportunities
- **作者/载体**：Yuping Wang 等；正式版 ACM Computing Surveys 2026-08-07（[DOI](https://doi.org/10.1145/3838726)）；本笔记读的是预印本 [arXiv 2505.08854v1](https://arxiv.org/abs/2505.08854)（2025-05-13）
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **引用数**：1（OpenAlex ACM CSUR 正式版记录）
- **笔记日期**：2026-09-22

## 分类框架（全文核验）

| 章节 | 内容 |
|---|---|
| §3 数据集/基准 | Table 1–4 |
| §4 生成模型基础 | VAE / GAN / DM / NeRF / SMPL / AR & LM |
| §5 按模态的前沿 | Table 5 图像、6 LiDAR、**7 轨迹**、8 占据、9 视频、10 3D/4D、11 编辑、12 LLM、13 MLLM |
| §6 应用 | 合成数据、**E2E AD**、个性化、数字孪生、场景理解、ITS |
| §7 具身智能 | — |
| §8 讨论 | 8.1–8.18（18 个小节） |

规模：参考文献编号至 **[912]**（子代理统计，含重复）；未声明"覆盖 N 篇"。

## 与扩散规划器直接相关的部分

- **§5.3 + Table 7** 把轨迹生成中的扩散类工作归为一类，列出 **Diffusion-Planner（ICLR'25，nuPlan）**、MotionDiffuser、SDT、DJINN、Scenario Diffusion。
- **§6.2** 在 E2E AD 应用中列 **DiffusionDrive（截断扩散、实时）**、DiffAD、**GoalFlow（目标引导解决轨迹发散）**。
- 它的评价（可直接引用）：扩散是轨迹生成的 **SOTA**（复杂分布 + 多条件控制），但**迭代采样计算昂贵，实时部署困难**（§5.3）。

## 最值得注意的一条主张（§8.9）

论文主张：生成式规划器需要外部的**规则式 "safety governor"** 来**否决越界轨迹**。

对本项目的含义：这与"把约束写进生成过程"（DP-A21/A12）和"把约束前移到结构层"（DP-A22）是**第三种立场**——**约束放在生成之后的否决层**。三种立场都已有代表，可构成完整讨论框架。

## 其他开放问题（§8 摘录）

- 8.1 场景/数据/基准：生成场景的真实性与多样性验证、长尾基准缺口、PINN 物理约束；
- 8.2 E2E 的理论与算法基础（SSRL / LRM）；
- 8.3 数字孪生 Real2Sim2Real；
- 8.9 可信性：不确定性、运行时监控、形式验证；
- 8.11 部署；8.12 伦理；8.18 负面社会影响。

## 对本项目的意义

- 用于论证"扩散规划器已是轨迹生成的 SOTA 类"以及"实时部署困难"这两个前提（比单篇论文的自述更有分量）。
- §8.9 的 "safety governor" 主张，是方向 A 讨论中必须回应的替代方案。
