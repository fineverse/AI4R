# E2E-10 · DriveVLM（输出接口转折：语言作为中间层）

- **原题**：DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models
- **作者/载体**：Xiaoyu Tian 等（清华 MARS Lab + 理想汽车）；arXiv [2402.12289](https://arxiv.org/abs/2402.12289) v5（2024-06）；CoRL 2024
- **代码**：**无实现代码** — [Tsinghua-MARS-Lab/DriveVLM](https://github.com/Tsinghua-MARS-Lab/DriveVLM) 已克隆，但仓库内容是 **`index.html` + `images/` + `DriveVLM.pdf`**（项目主页），**零 `.py` 文件**（2026-09-23 核验）
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 输入 | 多视角图像序列（T, T−1s … T−3s）+ 可选 3D 感知结果 + route / ego pose / velocity 的**文本提示** | §3、§4.1、§5.1 |
| 输出 | **语言**（场景描述 + 分析）+ **17 类 meta-actions** + decision description + 航点 W（3s） | §3.4、Fig.4 |
| 监督 | Qwen-VL（9.6B）监督微调 + co-tuning（Talk2Car / BDD-X / DRAMA / LLaVA 等，比例 1:1）；Dual 版引入 3D 检测/占用/规划器 | §5.1、§3.5 |
| 关键设计 | **三段 CoT**（描述 → 分析 → 分层规划）+ DriveVLM-Dual 的"慢思考 + 快行动"混合 | §1、§3 |
| 主结果 | nuScenes：DriveVLM-Dual† **L2 0.31m / 碰撞 0.10%**（DriveVLM 0.40/0.27；VAD-Base 0.37/0.14；**UniAD 1.03/0.31**）；自建 SUP-AD 上 Scene Desc 0.71、Meta-actions 0.37 | Table 2、Table 1 |
| 推理成本 | OrinX 平均 **410ms** | §6、Table 6 |
| 自述局限 | VLM 的空间定位与推理能力弱、算力需求大；GPT-4V 的场景描述存在**幻觉**并被扣分 | 摘要、§5.2 |

## 在脉络中的位置

- **继承**：UniAD / VAD（Dual 版与 VAD 协作）。
- **转折意义**：**输出接口**的转折——语言成为可解释的中间层，再由它映射到航点与 meta-action。它也是"特权信息重新进入"的代表（Dual 版把 3D 检测/占用作为提示）。

## 对本项目的意义

DriveVLM-Dual 在 nuScenes 上把 L2 从 UniAD 的 1.03m 降到 **0.31m**（开环），但代价是 410ms 与"语言幻觉"。**开环大幅领先 + 实时性极差 + 只报开环**这个组合，正是 2026 年 S032/S033 批评"评价协议未收敛"的现实来源。

## 代码核验（2026-09-23）

- **仓库是项目主页，零代码**。本笔记的**全部内容只能停留在论文自述级**。
- 影响：DriveVLM 是 VLA 支线的早期代表（[vla/lineage.md](../../topics/vla/lineage.md) 的"VLM as Explainer"阶段），而**该阶段在本工作空间内无任何可核验的实现**——当时 VLA-06/07/08 三篇（DiffVLA / ReCogDrive / KnowDiffuser）也都记为"未见官方代码"，于是写成"**VLA 侧的代码级核验整体为空白**"。**⚠ 该括注已于 2026-09-24 第三十六轮更正**：**DiffVLA（`boschresearch/DiffVLA`，36★）与 ReCogDrive（`xiaomi-research/recogdrive`，611★ / ICLR 2026）都已有官方代码**，只有 **KnowDiffuser 确认无仓库**（GitHub 搜索 0 结果）；且 VLA 侧**已有 14 篇做过源码级核验** → **"整体空白"不成立，真正空白的是"VLM as Explainer"这一个阶段**。详见 [e2e_trunk_code_traces.md](../../code/traces/e2e_trunk_code_traces.md) §A/F1。
