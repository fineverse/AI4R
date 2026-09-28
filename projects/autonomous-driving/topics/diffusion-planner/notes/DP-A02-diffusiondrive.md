# DP-A02 · DiffusionDrive（本项目基线案例）

- **原题**：DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving
- **作者/载体**：Bencheng Liao 等（hustvl）；arXiv [2411.15139](https://arxiv.org/abs/2411.15139) v3（2024-11-22 首发）；CVPR 2025 Highlight
- **代码**：[hustvl/DiffusionDrive](https://github.com/hustvl/DiffusionDrive)，快照 commit `9b52ed0ec06b073d82d6f392ab084c7b301c8681`（见 [code/repositories.md](../../../code/repositories.md)）
- **证据等级**：摘要 + 前序会话已读正文/附录文字 + 代码静态检查（**未运行**）
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> ...we propose a novel truncated diffusion policy that incorporates prior multi-mode anchors and truncates the diffusion schedule, enabling the model to learn denoising from anchored Gaussian distribution to the multi-mode driving action distribution. Additionally, we design an efficient cascade diffusion decoder for enhanced interaction with conditional scene context.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 核心机制 | 截断扩散日程：从"锚定高斯分布"出发去噪（锚点由 K-means 聚类得到），级联扩散解码器增强与场景上下文的交互 | 摘要 |
| 去噪步数 | 2 步 | 摘要（"truncated"）；前序会话正文阅读 |
| NAVSIM v1 | **88.1 PDMS**（对齐 ResNet-34 backbone），摘要称"无花哨技巧"下刷新记录 | 摘要 |
| 速度 | 4090 上 45 FPS | 摘要 |
| 多样性 / **原始池天花板** | DDV2 Table 3 反向引用：**Div 42.3 / PDMS@1 93.5 / PDMS@5 84.3 / PDMS@10 75.3**。**⚠ 第四十一轮把口径核到原文**（DDV2 §5.3 与 Table 3 题注，PDF 逐字）：**PDMS@K 是在"各自的选优模块之前"的原始输出上算的**（原文 "the models' raw outputs, evaluated **before their respective selection modules**"；题注 "PDMS@K denotes the PDMS score evaluated on the **Top-K ranked** trajectories"），且正文把 **@1 称 upper bound、@10 称 lower bound** → **`PDMS@1` = 原始 20 条候选里最好那条的 PDMS（即"池子天花板"/oracle@20）** → **本模型的"选优损失"= 93.5（天花板）− 88.1（分类器实际选出）= 5.4**（DDV2 的同一口径是 94.9 − 91.2 = **3.7**；两个量分属 navtest 天花板 gap，见 [sota-plan.md §9](../../../ideas/sota-plan.md)） | DDV2 全文 Table 3（第四十一轮 PDF 核验语义） |
| 后续被直接对比 | GoalFlow、MeanFuser、WAM-Flow、DiffusionDriveV2、DIVER 等均以其为对比对象 | 各论文表格 |

## 局限（来自后续工作的批评，非本人自述）

- **BridgeDrive（DP-A08）**：截断扩散的前向加噪与去噪过程不对称，偏离扩散模型核心原理，可能带来不可预测行为。
- **MeanFuser（DP-A14）**：依赖离散锚点词表，需要在测试时覆盖轨迹分布，形成"词表大小 vs 性能"的固有权衡。
- **DiffusionDriveV2（DP-A03）**：单纯模仿学习缺乏约束，出现"多样性 vs 一致高质量"的两难。
- **G2SD（DP-A22）**：推理期引导会造成流形破裂（该批评针对引导式方法，DiffusionDrive 本身无引导）。

## 对本项目的意义

- 它是当前扩散规划器里**被引用与被对比最密集**的基线，任何新方法若不与它在同 backbone、同评测下比较，说服力会被削弱。
- 其"锚点 + 2 步"的工程形态已经把实时性做满，因此**可改进空间集中在质量、约束与选优**，而不是速度。

## 待核验

- nuScenes 分支未做与 NAVSIM 分支同等程度的代码核验。

## 代码核验（2026-09-23）

| 项 | 代码证据 |
|---|---|
| 锚点词表 | `transfuser_config.py:19`：`plan_anchor_path` 默认值是**作者本机绝对路径**；**v1 仓库内没有任何 `.npy`**——锚点文件**未随仓库发布** |
| 训练损失有 4 项（原待核验项，已解决） | 同文件：`trajectory_weight 12.0` + `trajectory_cls_weight 10.0` + `trajectory_reg_weight 8.0` + `diff_loss_weight 20.0` → 与"锚点分类 + 轨迹回归 + 扩散去噪"的三头设计一致 |
| 主干规格 | `tf_d_model 256`、`tf_num_layers 3`、`tf_num_head 8`、`num_bounding_boxes 30`、`lidar_seq_len 1`、图像/LiDAR 均 resnet34、LiDAR ±32 m / 256×256 |
| **与 V2 的可比性** | **DD 与 V2 的 `transfuser_config.py` 逐字节完全相同**（`diff` 无输出），agent yaml 也只覆盖 `trajectory_sampling`（4 s / 0.5 s）与 `latent: False` → **V2 的 91.2 vs DD 的 88.1 可以直接归因于"RL 后训练 + mode selector"**。这是本项目**唯一一对主干完全对齐**的工作 |

完整对照表见 [diffusion_planner_code_traces.md §F](../../../code/traces/diffusion_planner_code_traces.md)。
