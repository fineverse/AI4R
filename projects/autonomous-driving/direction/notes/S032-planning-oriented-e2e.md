# S032 · Planning-Oriented End-to-End Autonomous Driving（预印本全文）

- **原题**：Planning-Oriented End-to-End Autonomous Driving: Architectures, Evaluation, and Emerging Paradigms
- **作者/载体**：Yanchen Guan 等；arXiv [2608.20111v1](https://arxiv.org/abs/2608.20111)（2026-08-20）
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **笔记日期**：2026-09-22
- **定位**：本项目**规划口径的主锚**（state.md 第一轮就把 S032 列为优先阅读）

## 分类框架（全文核验）

- **Table II 四轴 taxonomy**：输入表示 / 输出空间 / 监督信号 / 评测协议。
- §III 历史演进；§V 架构；§VI 世界模型与 VLA；§VII 基准与指标；§VIII 安全/鲁棒/部署；§IX 可复现性与未来；**Table IV 设计权衡**（含"Generative or probabilistic planner"一行）。
- 检索期：2015 – 2026 年 6 月（§II.B），含前向/后向引文追踪；Table III 列代表性方法（子代理统计 23 条）。**未给出覆盖篇数**。

## 与扩散规划器直接相关的部分

- 扩散类被归入输出空间的"多模态轨迹分布 / 场景 rollout"，并在 Table IV 中作为 **"Generative or probabilistic planner"** 一行讨论；Table III 列出 VADv2、**DiffusionDrive[64]**、**WAM-Flow[21]**（离散流匹配）。
- **§IV.D 明确把"如何评估生成式规划"列为开放问题**：生成分布只有在能把**安全、目标一致的轨迹排在前面**时才有用。
- **Table VII** 指出 WAM-Flow 需要奖励对齐与独立复现——与本项目"数字均为论文自述、未复现"的边界一致。

## 评价协议（本项目最需要的一节）

- Table VIII 资源（CARLA / nuScenes / nuPlan / Bench2Drive / NAVSIM / DriveLM / TAD-E2E / WOD-E2E）；**Table IX 各协议能支持什么结论**；Table XI 可复现性清单。
- **§VII.C**：**跨协议排名会反转**、子指标饱和、**NAVSIM 只是代理证据**；作者建议**不要设单一 "best method" 列**。

## 开放问题（Table XIII + §IX.C）

指标有效性、长尾鲁棒、师生不对称、世界模型校准、语言-动作落地、形式与经验安全、算力部署、可复现性。

## 对本项目的意义

1. 它的四轴（输入/输出/监督/评价）与本项目 preparation.md 第 6 节的比较口径**完全一致**，可直接作为引用依据。
2. §VII.C 的"跨协议排名反转 + 子指标饱和 + 不要设 best method 列"是**反对继续刷 navtest 分数**的权威依据（与本项目从数字里发现的 navtest 饱和相互印证）。
3. §IV.D 把"生成式规划的评价"单列为开放问题——这正是 preparation.md 方向 F 的依据来源。
