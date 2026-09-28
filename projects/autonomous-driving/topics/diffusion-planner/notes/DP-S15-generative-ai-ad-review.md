# DP-S15 · Generative AI for Autonomous Driving: A Review（本轮新发现）

- **原题**：Generative AI for Autonomous Driving: A Review
- **作者/载体**：Katharina Winter 等；arXiv [2505.15863v1](https://arxiv.org/abs/2505.15863)（2025-05-21）；comments 称已投 IEEE
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **笔记日期**：2026-09-22
- **发现经过**：本轮查"ACM CSUR 那篇有没有预印本"时，按标题检索 arXiv 发现的**同题不同团队**综述。两篇并行阅读可判断该领域分类框架是否已收敛。

## 分类框架（全文核验）

- 生成模型两分：**可逆类**（Normalizing Flow / INN / NODE）与**隐式类**（VAE / GAN / **DM** / EBM），外加 GT 对照。
- §II 基础：经典策略（SL / USL / RL / IL）；§III AD 栈；§IV 场景与场景生成（含 world models）；§V 轨迹预测；§VI 运动规划（含混合方法）；§VII E2E（按 DM / VAE / Transformer / LLM 分类）；§VIII 数据集与仿真器（Table I）；§IX 挑战/建议/展望。
- 规模：166 条参考文献（子代理统计）。

## 与扩散规划器直接相关的部分

- **§VII.A.a** 在 E2E 的 DM 类中列 **Diffusion-ES**、**DiffusionDrive**。
- **§VI.B** 在运动规划中列 **CoBL-Diffusion**、**SafeDiffuser（CBF 安全滤波）**、DDM-Lag、**扩散物理状态空间 MPC**。
- 评价：DM 优化多模态轨迹采样；DiffusionDrive 用截断扩散提升实时性。

## 对评价协议的批评（本笔记最有价值的部分）

1. 开环评测**只与专家 GT 比较**；闭环评测才包含动力学与交互。
2. **多数 SOTA 生成式规划器只优化开环指标**。
3. **E2E 很少与传统方法比较，且闭环下常输给更简单的方法**。
4. **NAVSIM 缺反应性与长期真实性**；**CARLA 存在 sim-to-real gap**。

## 开放问题（§IX）

- 挑战：**安全**（SOTIF / 对抗 / CBF / HJ 可达性）、**可解释性**（行为/归因/概念/机制四类，其中**概念与机制在 AD 近乎空白**）、**实时性**。
- 建议：模型选择（VAE + 对抗损失可高质）、潜在空间选择。
- 展望：域差度量与安全感知指标、幻觉检测、**闭环事故率仍可测**、开环影子模式测试、LLM 边缘部署。

## 对本项目的意义

- 与 DP-S11 互补：DP-S11 偏"生成能力版图"，DP-S15 偏"生成式规划的评价缺陷"，**后者的批评更直接**。
- 可用于支撑两个论断：①"NAVSIM 只是代理证据"（与 S032 一致）；②"概念/机制层面的可解释性在 AD 近乎空白"——这是一条本项目尚未利用的空白。
