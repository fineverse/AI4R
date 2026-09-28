# DP-A03 · DiffusionDriveV2

- **原题**：DiffusionDriveV2: Reinforcement Learning-Constrained Truncated Diffusion Modeling in End-to-End Autonomous Driving
- **作者/载体**：Jialv Zou 等（hustvl）；arXiv [2512.07745](https://arxiv.org/abs/2512.07745) v1（2025-12-08）；abs 页无 Comments，录用信息未获取
- **代码**：[hustvl/DiffusionDriveV2](https://github.com/hustvl/DiffusionDriveV2)（见 [code/repositories.md](../../../code/repositories.md)）
- **证据等级**：全文（arXiv HTML 逐节提取）+ 摘要
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> Generative diffusion models for end-to-end autonomous driving often suffer from mode collapse, tending to generate conservative and homogeneous behaviors. While DiffusionDrive employs predefined anchors representing different driving intentions to partition the action space..., its reliance on imitation learning lacks sufficient constraints, resulting in a dilemma between diversity and consistent high quality.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 输入 | 3 张前视裁剪下采样图拼接为 1024×256 + LiDAR 点云栅格化 BEV | §5.2 |
| 生成机制 | 沿用 DiffusionDrive 锚点高斯先验 τ_t=√ᾱ_t·a^k+√(1−ᾱ_t)ε 的截断扩散；推理 **2 步**；无 classifier guidance/CFG；无显式 goal 条件（目标对齐走奖励） | §5.2、Eq.3 |
| 探索噪声 | 尺度自适应**乘性**高斯噪声（纵向/横向各一，τ'=(1+ε_mul)τ）；训练 η=1，验证 η=0 | §4.3 |
| 训练 | 两阶段：冷启动自 DiffusionDrive IL 权重 → 阶段 1 RL 10 epoch（batch 512、lr 2e-4、γ=0.8、BC loss 权重 0.1）→ 阶段 2 mode selector 20 epoch（BCE + Margin-Rank） | §5.2、§7、Eq.11 |
| RL 细节 | 把去噪视作 MDP（REINFORCE/GRPO）；奖励为最终干净轨迹的轨迹级 R(τ)；碰撞轨迹 advantage 置 −1，其余 max(0,A)；Intra-Anchor GRPO + Inter-Anchor Truncated GRPO | Eq.10、§4 |
| NAVSIM v1 navtest | **PDMS 91.2**（NC 98.3 / DAC 97.9 / TTC 94.8 / Comf 99.9 / EP 87.5，ResNet-34） | Table 1 |
| 同表对比 | DiffusionDrive 88.1、DIVER 88.3、DriveSuprim 89.9、GoalFlow(V2-99) 90.3、Hydra-MDP(V2-99) 90.3 | Table 1 |
| NAVSIM v2 navtest | **EPDMS 85.5** | Table 2 |
| 多样性 / **原始池天花板**（**第四十一轮核到原文，语义已钉死**） | DDV2 **Div 30.3 / PDMS@1 94.9 / @5 91.1 / @10 84.4**；DiffusionDrive **42.3 / 93.5 / 84.3 / 75.3**；Transfuser_TD 0.1 / 85.7（三档相同）。**口径**：Table 3 题注原文 "**PDMS@K denotes the PDMS score evaluated on the Top-K ranked trajectories**"，正文明确这是 "**the models' raw outputs, evaluated before their respective selection modules**"（即 **DiffusionDrive 的分类器 / DDV2 的 selector 之前**），并把 **@1 称 upper bound、@10 称 lower bound** → **`PDMS@1` = 原始 20 条候选里最好那条的 PDMS（"池子天花板"/oracle@20）**。**→ 两个可直接引用的"选优损失"数字**：DiffusionDrive 池子天花板 **93.5** 而它的分类器只选出 **88.1**（**丢 5.4**）；DDV2 池子天花板 **94.9** 而其 selector 选出 **91.2**（**丢 3.7**） | Table 3（第四十一轮 PDF 逐字核验语义） |
| 消融 | 乘性噪声 90.1 vs 加性 89.7；有 Intra-Anchor 90.1 vs 无 89.2；有 Inter-Anchor Truncated 90.1 vs 无 89.5 | Table 4/5/6 |

## 作者自述局限

- 无独立局限章节；正文自述风险是**过度依赖下游 selector**，其参数少、OOD 下易失效（§1）。

## 对本项目的意义

- 同团队、同 backbone、同基准的**直接后继**：PDMS +3.1、EP +5.3（Table 1）。
- 关键取舍：Top-1 质量从 93.5 提升到 94.9，但多样性从 42.3 降到 30.3——即用多样性换质量。这是本项目判断"是否值得做多样性可控"的直接依据。

## 待核验

- 奖励函数的具体构成（正文未展开）。
- 延迟/FPS（正文未给）。
- nuScenes 分支未做代码核验。

## 代码核验（2026-09-23）

| 项 | 代码证据 |
|---|---|
| **主干与 DD 完全对齐**（重要） | V2 的 `transfuser_config.py` 与 DiffusionDrive 的**逐字节完全相同**；agent yaml 也只覆盖 `trajectory_sampling`（4 s / 0.5 s）与 `latent: False`。→ **+3.1 PDMS 可以直接归因于"RL 后训练 + mode selector"**，不是主干差异 |
| **selector 的实现细节**（原待核验项，已解决） | `diffusiondrivev2_model_sel.py`：候选池 = **扩散采样结果 + 16384 条词表轨迹**（`torch.cat((diffusion_output, vocab), dim=1)`），再由 **coarse scorer → top-32 → fine scorer** 选优。**最终输出可以是一条词表轨迹而非扩散样本** |
| 16384 词表的用途 | 是**预计算的 PDM 子分数查找表**（`gtrs_traj/navtrain_16384.pkl`），权重与 NAVSIM 一致：`NC × DAC × (5·TTC + 5·EP + 2·C)`；推理时随机保留约 1%（`dropout_ratio=0.99`） |
| 仓库内文件缺失 | 有 `kmeans_navsim_traj_20.npy` 与 `gtrs_traj/16384.npy`（**(16384, 40, 3)** float32，由文件字节数 7,864,448 = 16384×40×3×4 + 128 字节 numpy 头反推确认），但 **`gtrs_traj/navtrain_16384.pkl` 缺失** |
| GRPO 实现 | `diffusiondrivev2_model_rl.py`：逐步记录 `log_prob`，堆叠成 `all_log_probs`（注释形状 `[B, G*N, step_num]`）→ 与论文的锚内/锚间分组一致 |

完整对照表见 [diffusion_planner_code_traces.md §F](../../../code/traces/diffusion_planner_code_traces.md)。
