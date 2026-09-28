# VLA-08 · KnowDiffuser（LM 元动作 → 锚点先验 → 两阶段截断去噪）

- **原题**：KnowDiffuser: A Knowledge-Guided Diffusion Planner with LLM Reasoning
- **作者/载体**：Fan Ding、Xuewen Luo、Fengze Yang、Bo Yu、HwaHui Tew、Ganesh Krishnasamy、Junn Yong Loo（**Monash University Malaysia** + University of Utah）；arXiv [2603.10441](https://arxiv.org/abs/2603.10441) v2（2026-04，cs.RO）
- **代码**：未见
- **证据等级**：全文（PDF + `pdftotext -layout`，读摘要、贡献、方法与实验结论）
- **笔记日期**：2026-09-23

## 摘要原文（节选）

> …the framework employs a language model to infer context-aware meta-actions from structured scene representations, which are then mapped to prior trajectories that anchor the subsequent denoising process. A two-stage truncated denoising mechanism refines these trajectories efficiently…

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 核心思路 | **LM 推断元动作**（如 go straight / turn left/right / stop）→ **bridge 机制**把元动作映射到**历史数据得到的先验轨迹** → 从"语义对齐的先验 + 极小噪声"起步做**两阶段截断去噪** | 摘要、§I 贡献列表 |
| 去噪器 | DiT 解码器；输入为当前状态 + 加噪轨迹拼接后展平；**x0-prediction 损失**（`L = E‖x̂0 − x0‖²`） | §III（Eq.11、Eq.14–16） |
| 推理策略 | "truncated inference"——不从纯噪声采样，从语义先验起步 + 部分扩散，声称兼顾低延迟与保真 | §III 末段 |
| **外部 LLM** | 使用 **GPT-4o（2024）**作为推理 LMM | §IV.A |
| 数据与任务 | nuPlan 日志切成 10 秒序列，约 **50,000 样本**；输入前 2 秒，预测后 8 秒，0.5 秒间隔 | §IV.A |
| **主结果** | Val **NR 87.50 / R 81.25**；Test **NR 86.94 / R 81.10** | §IV 结果段 |
| 对比 | Val 上超最强基线 PlanTF **+2.67 / +4.47** 个百分点；Test 上超 GameFormer **+20.35 / +12.27**、超 PlanTF **+14.26 / +19.40** | §IV 结果段 |

## 局限（本人自述 / 本笔记指出）

- **本人自述**：目前只用 LM（文本），**未来工作才接入 VLM** 做多模态场景理解（§V 结论）。
- **本笔记指出**：对比基线是 PlanTF（纯模仿学习）、GameFormer（博弈 transformer）、PDM-Open、CKS、GUMP-m，**没有与 nuPlan 上最强的扩散规划器 Diffusion Planner（DP-A01）对比**——而后者正是同一基准上的直接竞品。

## 对本项目的意义

- 与研究对象**接口最直接**：LM 元动作 → **锚点先验**。这与 DP-A30（研究对象表内同名条目）是同一路线，也印证了 [lineage.md](../lineage.md) 阶段 2「语言变成中间表示」的判断。
- **一个必须记下的工程约束**：它把 **GPT-4o 放进规划回路**。这意味着延迟与成本取决于外部 API，与"车规实时"存在根本张力——[transfer.md](../../diffusion-planner/transfer.md) 第 2 节的"双系统分离"正是为了绕开这一点。
- 它的"bridge 机制"（元动作 → 历史轨迹先验）值得注意：把**离散语义**映射到**连续先验**，而不是让语言直接回归轨迹，是对"模态错配"（ReCogDrive 也提出同一问题）的一种解法。

## 待核验

- NR / R 两个指标的确切定义（non-reactive / reactive）与计算方式未在本次阅读中确认。
- 推理延迟数字：论文只作定性声明（"significantly reducing inference latency"），**未给出 Hz 或 ms**。
- 未与 DP-A01（Diffusion Planner）对比，无法判断在 nuPlan 上的真实位置。
