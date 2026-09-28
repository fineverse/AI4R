# S002 · Recent Advancements in End-to-End Autonomous Driving Using Deep Learning（全文）

- **原题**：Recent Advancements in End-to-End Autonomous Driving Using Deep Learning: A Survey
- **作者/载体**：Pranav Singh Chib、Pravendra Singh；正式版 IEEE TIV 9(1):103–118（2024，DOI 前缀 2023）；本笔记读的是预印本 [arXiv 2307.04370](https://arxiv.org/abs/2307.04370) v2（2023-09-19）
- **代码/文献列表**：[Pranav-chib/Recent-Advancements-in-End-to-End-Autonomous-Driving-using-Deep-Learning](https://github.com/Pranav-chib/Recent-Advancements-in-End-to-End-Autonomous-Driving-using-Deep-Learning)
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **引用数**：294（OpenAlex 快照）
- **笔记日期**：2026-09-22
- **本轮唯一拿到全文的 E2E 综述**（其余 S016/S018/S019/S020/S035 均 403，见 [e2e_ad_lineage.md](../lineage.md) 的证据边界）

## 它怎么讲历史（关键）

**不按年份严格分期**，而是用"路线图"（Fig.2、§1）按时间顺序回顾关键里程碑，再按技术主题分类。它明确标注的"首次"只有三处：

| 里程碑 | 内容 | 出处 |
|---|---|---|
| **首个 E2E 尝试** | Pomerleau 的 **ALVINN**（3 层网络直接输出转向） | §3 |
| **首个有效 RL** | Liang 等 | §6.2 |
| CARLA 2019 挑战赛视觉方案夺冠 | Toromanoff 等 | §4.1 |

## 分类框架

输入模态（§4）→ 输出模态（§5）→ 学习方法 IL / RL（§6）→ 域适应（§7）→ 安全（§8）→ 可解释性（§9）→ 评估（§10）。

代表工作（Table 3 含年份）：ALVINN、DAVE / DAVE-2、Transfuser、LAV、TCP、ST-P3、Think Twice、MP3、NEAT、CaRINA 等。

## 评价协议（本项目直接可用）

- **开环**（KITTI / nuScenes）：MinADE / MinFDE、L2、碰撞率；
- **闭环**（CARLA LeaderBoard / NoCrash）：**RC（路线完成）、IS（违规分数）、DS = RC × IS**（§10、Table 7）。
- 对开环的批评**较温和**：只说它"更快但无法评估实时反应"；闭环的缺点是"初始配置复杂 + 域差"。

## 开放问题（§12.1–12.5）

1. 学习鲁棒性（IL 的分布漂移、RL 不稳定）；
2. 安全；
3. 可解释性；
4. 协同感知；
5. 大视觉 / 语言模型。

## 关键资产

Table 3（方法总表）、Table 7（CARLA 榜单）、Table 8（数据集 + 年份）、Table 9（仿真器）；全文 28 页。

## 对本项目的意义

- 它是"**开环 → 闭环**"这一评价转向的**早期权威记录**（DS = RC × IS 的出处），可用于论证"为什么后来需要 NAVSIM 这类伪闭环"。
- 它的"首次"标注只给了 ALVINN 与 Liang 的 RL——**这与 S001（TPAMI）只提 270+ 篇而不给里程碑、S018 归因基础模型、S019 归因 VLM** 形成对照，说明各综述对"转折点归因"分歧明显。
