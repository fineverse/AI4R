# DP-A14 · MeanFuser

- **原题**：MeanFuser: Fast One-Step Multi-Modal Trajectory Generation and Adaptive Reconstruction via MeanFlow for End-to-End Autonomous Driving
- **作者/载体**：Junli Wang 等；arXiv [2602.20060](https://arxiv.org/abs/2602.20060) v2（2026-02-23 首发）；**CVPR 2026 录用**
- **代码**：[wjl2244/MeanFuser](https://github.com/wjl2244/MeanFuser)（见 [code/repositories.md](../../../code/repositories.md)）
- **证据等级**：全文（arXiv HTML 逐节提取）+ 摘要
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> ...these methods rely on discrete anchor vocabularies that must sufficiently cover the trajectory distribution during testing to ensure robustness, inducing an inherent trade-off between vocabulary size and model performance. To overcome this limitation, we propose MeanFuser... (1) Gaussian Mixture Noise (GMN) to guide generative sampling... (2) adapt "MeanFlow Identity" to end-to-end planning...

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 要解决的问题 | 锚点/词表离散化需要在测试时覆盖轨迹分布，形成"词表大小 vs 性能"固有权衡；vanilla 扩散有模式坍缩、多步采样慢 | 摘要、§1 |
| 生成机制 | **MeanFlow**：直接学平均速度场，消除 ODE 数值误差 → 一步采样 x₁=x₀+u_θ(x₀,0,1) | Eq.5 |
| 噪声起点 | **高斯混合噪声（GMN）**，K=8 分量；并行采样 8 条 | §4.2、§5.2 |
| 选优 | Adaptive Reconstruction Module（注意力选/重建） | §5.2 |
| 训练 | MeanFlow 损失 + 映射损失 + ARM 损失；**纯模仿，不用基准指标做奖励** | Eq.6–7、13、15、§4.4 |
| 推理成本 | **59 FPS**（端到端）；Table 3：MeanFuser 54.6M 参数 / PDMS 89.0 / 规划模块 434 / 端到端 59；GoalFlow 62.3M/85.7/11/10；DiffusionDrive 60.7M/88.1/75/39。正文称规划模块相对 GoalFlow、DiffusionDrive 加速 **39.45× 与 5.78×**（与 434/11、434/75 一致，故该列应为规划模块吞吐） | Table 3（PDF 核验）、§1、§5.3 |
| NAVSIM v1 | **PDMS 89.0**（NC 98.6 / DAC 97.0 / TTC 95.0 / Comf 100 / EP 82.8）；同表 DiffusionDrive 88.1、WoTE 88.3、Hydra-MDP 86.5、GoalFlow* 85.7 | Table 1（PDF 核验） |
| NAVSIM v2 | **EPDMS 89.5**（同表 DiffusionDrive† 88.3、DriveSuprim 83.1、Hydra-MDP++ 81.4） | Table 2（PDF 核验） |
| 消融 | M0 87.3（+3.3，MeanFlow 解码）；M1 88.2（+0.9，GMN）；M2 **89.0**（+0.8，ARM）；**M3 71.2（−17.8，简单平均各 proposal）**；基线 TransFuser 84.0、DiffusionDrive 88.1 | Table 4（PDF 核验） |

## 作者自述局限

- GMN 的分量权重 π_k 固定为 1，混合参数建模留待未来（§4.2）。

## 对本项目的意义

- 直接针对 DiffusionDrive 的"锚点词表"这一结构假设：用**连续**高斯混合噪声替代离散词表，且用 MeanFlow 把步数压到 1。
- 对本项目最有价值的消融是 **M3：简单平均各 proposal 掉 17.8 PDMS**——说明**多候选的融合/选优方式比生成本身更敏感**，支持把"选优机制"当作独立研究对象。
- 与 DiffusionDrive、GoalFlow 均有直接对比，是当前最有可比性的前沿基线之一。
- **一条重要的可比性证据**：MeanFuser Table 1 把 GoalFlow 记为 85.7（带 *），而 GoalFlow 自己报 90.3。同一基准、同一方法，两篇论文数字差 4.6 分，说明"对齐 backbone/输入权限"的复现口径差异极大——做比较实验时必须自己复现基线，不能引用他人表格。

## 待核验

- Table 3 中"规划模块"列的**单位**未在 HTML/PDF 文本中直接写明，当前按正文倍数关系推断为吞吐（FPS）；需回原文表头确认。

## 代码核验（2026-09-23）

| 项 | 代码证据 |
|---|---|
| **"去词表"主张得到确认**（原待核验项，已解决） | `meanfuser_config.py` 里**没有任何锚点/词表字段**（对比 DiffusionDrive 的 `plan_anchor_path`）；取而代之是 `noise_type: str = 'multi_gaussian'` 与 `navtrain_mean_std_path = 'tools/gaussian_mixed_noise/navtrain_8_mean_std.pkl'`（K=8 高斯混合统计量）。agent yaml 也把 `noise_type` 显式设为 `'multi_gaussian'`、`num_proposals: 8` |
| 一步采样 | 同文件：`num_sample_steps: int = 1`；`use_fm_cfg: bool = False`（**未启用 CFG**） |
| **主干比 DiffusionDrive 窄一半** | `MeanfuserConfig.tf_d_model = 128`（DD/V2 为 **256**）；其 `navsim/agents/transfuser/transfuser_config.py`（256）是 **vendored 的 TransFuser 基线，不被 MeanfuserAgent 使用**（agent 用的是 `MeanfuserConfig`） |
| **输入时序比 DiffusionDrive 长** | agent yaml 覆盖 `lidar_seq_len: 4`（DD 为 **1**） |
| 损失只剩一项 | `trajectory_weight 10.0`；DD 有四项（trajectory 12 + cls 10 + reg 8 + diff 20） |
| GMN 的 K=8 与 DD 锚点 20 条是否可比（原待核验项，部分解决） | 代码确认二者是**不同性质的先验**：DD 的 20 条是 **K-means 离散锚点**（分类 + 扩散起点），MeanFuser 的 K=8 是**连续高斯混合的统计量**（`_mean_std.pkl`）。数量不同（8 vs 20）**不宜直接类比** |

**对"85.7 vs 90.3 矛盾"的补充**：MeanFuser 与 DD 之间除损失与先验不同外，还有 **`tf_d_model`（128 vs 256）与 `lidar_seq_len`（4 vs 1）**两重主干/输入差异。

完整对照表见 [diffusion_planner_code_traces.md §F](../../../code/traces/diffusion_planner_code_traces.md)。
