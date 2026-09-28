# VLA-06 · DiffVLA（VLM 命令引导的稀疏-稠密混合扩散规划器）

- **原题**：DiffVLA: Vision-Language Guided Diffusion Planning for Autonomous Driving
- **作者/载体**：Anqing Jiang 等（RIX, Bosch；清华 AIR；上海大学；上海交大；东南大学）；arXiv [2505.19381](https://arxiv.org/abs/2505.19381) v4（2025-06）。**性质：NAVSIM v2 竞赛（Autonomous Grand Challenge 2025）技术报告，无会议/期刊 venue**
- **代码**：**[boschresearch/DiffVLA](https://github.com/boschresearch/DiffVLA)**（36★，Apache-2.0，44 MB，最后推送 2025-12-08）；⚠ `DiffVLA/DiffVLA` 是**空壳**（0 KB / 10★）。**⚠⚠ 但发布版与论文不同**——轨迹头已从 Diffusion Drive 换成自研 Transformer 头（见下方「代码核验」）。**本条 2026-09-24 第三十六轮更正**（此前记"未见官方代码"）
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **笔记日期**：2026-09-23

## 摘要原文（节选）

> …we propose a novel hybrid sparse-dense diffusion policy, empowered by a Vision-Language Model (VLM), called Diff-VLA. We explore the sparse diffusion representation for efficient multi-modal driving behavior. Moreover, we rethink the effectiveness of VLM driving decision and improve the trajectory generation guidance through deep interaction across agent, map instances and VLM output. Our methods achieves 45.0 PDMS.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 三模块 | ① VLM 引导（基于 **Senna-VLM**：ViT-L/14 CLIP 视觉编码器 + **Vicuna-v1.5-7B** LLM）② 稀疏-稠密混合感知（**VoV-99** backbone；BEV 128×128 覆盖 64×64 m；聚合 30 个 agent + 自车）③ 截断扩散规划器 | §1 贡献列表、§2、§3 |
| 扩散起点先验 | NavTrain 轨迹 k-means 聚类得词表 V，加高斯噪声得锚点；**N_anchor = 32**（对比 DiffusionDrive 的 20） | §4 Planning |
| 规划视野 | T_h = 4（秒） | §4 Planning |
| 主结果 | **45.0 EPDMS**（navsim-v2 私有测试集，竞赛成绩） | Table 2 |
| 分阶段子指标异常 | stage-1（无扩散规划器）no-at-fault collisions **95.71** / lane keeping **97.14**；stage-2（含扩散规划器）降到 **81.27** / **59.85** | Table 2 |
| 后处理 hack | 观察到高速下碰撞率偏高，**对轨迹在 y 轴施加 2% 减速**，称"有效避免碰撞且其他分数无明显差异" | §5.1 |
| 训练 | 两阶段；VLM 仅训 **1 epoch**（lr 2e-5）；stage-2 冻结 VLM 与稀疏感知权重 | §6.1.1、Table 1 |

## 局限（本人自述）

- **各模块分开训练**（VLM / 稀疏感知 / 稠密感知 / 规划头各自训练），端到端联合训练"尚未探索，可能带来性能提升"（§7）。

## 对本项目的意义

- 与研究对象的**接口最直接**：VLM 输出高层横向/纵向控制命令（one-hot 编码）→ 与导航指令合并 → 作为扩散规划的语义引导条件。这正是 [transfer.md](../../diffusion-planner/transfer.md) 第 2 节"语言作为引导而非回归目标"的一条实现。
- **锚点数 32（vs DiffusionDrive 20）**：说明锚点词表规模是可调的超参，不是固定值。
- **一个必须记下的负面证据**：加了扩散规划器后，碰撞与车道保持子指标**显著变差**（95.71→81.27、97.14→59.85），而总分更高。说明 EPDMS 与安全性子指标不一致——与 [preparation.md](../../../ideas/preparation.md) 的 P2c（分数与可行性不一致）**同向**。
- **纯生成结果仍需后处理兜底**（2% y 轴减速），这是"生成式规划器不敢直接用"的一个现实例证。

## 代码核验（2026-09-24 第三十六轮，L3：GitHub API + `raw` 逐文件取证，**未克隆**）

**⚠ 最要紧的一条：发布代码里没有论文的那个扩散头。**

| 项 | 证据 |
|---|---|
| **仓库自述与论文的差异** | README §5「Notifications」原文：**"The released version has some modifications compared to the paper on arXiv: 1. The trajectory head has been updated from Diffusion Drive to a self-developed Transformer-based Trajectory Head. 2. A reward loss derived from multiple EPDM sub-metrics has been introduced to guide training."** |
| **活跃头** | `navsim/agents/diffvla/trajectory_head_reward.py`（目录下**没有任何扩散轨迹头文件**）；`modules/` 只剩 `conditional_unet1d.py` 与 `scheduler.py` 两件扩散残件；`diffvla_config.py` 里 `diff_loss_weight = 20.0` 仍在但**不被活跃头使用** |
| **它其实是一个"选优器"** | `RewardHead` 按 **nc / dac / ddc / tlc / ep / tc / lk / hc 八个 EPDM 子指标**各出一个头；损失 `compute_reward_loss` 是 **BCE against 离线 GT 标签**（监督来自 `pdm_scores_8192`，由 `navsim/misc/gen_multi_trajs_pdm_score_ours.py` 生成）。**推理期**（`forward_test`）：`combined_score = w1·cls + w2·nc + w3·dac + w4·(5·tc + 2·lk) + w5·ddc`，**`w = [1.0, 4.0, 1.2, 0.02, 8.0]` 是手调常数**，然后 `argmax` 选一条。→ **`ep` 与 `hc` 算了但没进最终分** |
| **锚点与论文不一致** | 配置 `num_voc = 8192`（论文写 **N_anchor = 32**）；`diffvla_data_exp/planning_vb/` 下**9 档锚点文件全部已发布**（32 / 64 / 128 / 256 / 512 / 1024 / 2048 / 4096 / 8192，最大 786 KB）——**这是本项目里锚点文件发布得最全的一个仓库** |
| 二阶段结构仍在 | `_refine_traj` 走 **2 个 stage**（每个 stage：锚点 MLP → BEV 采样 → cross-BEV → cross-agent → FFN → offset 回归），`out2` 是 **8192 条精修后的轨迹**，再由分类头/打分头**选一条** |
| 训练规模（仓库自述） | 8×H20 约 **45 min × 30**；仓库提供 `fast_test.sh`（自述比官方评测快，**分差 < 0.25%**） |

**推论**：**45.0 是论文里带扩散头的竞赛成绩，发布代码不是那个配置**，且仓库**未报告该版本的任何分数**。→ 见 [sota-plan.md §7.6](../../../ideas/sota-plan.md) 的路线 ② 起点重估（结论：起点应改为 DiffusionDrive 24.2）。另：**发布版是"离线 GT 打分监督的选择器"的第 4 个代码级实例**，且候选池 **8192**——它是"把离线 GT 监督换成在线信号"这条方向的**最合适载体**。

## 待核验

- **发布版的 navhard 分数未知**（仓库未报告）；无法确认"换成打分头之后"与论文 45.0 的差距。
- 与 DiffusionDrive 的对比不成立：本报告未给出同 backbone、同输入权限的受控对比。
- 竞赛成绩（45.0）与论文自报数字的可比性未知。
- 2% y 轴减速后处理在发布代码里的实现位置未核（论文 §5.1）。
