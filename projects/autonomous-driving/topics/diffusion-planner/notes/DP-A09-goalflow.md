# DP-A09 · GoalFlow

- **原题**：GoalFlow: Goal-Driven Flow Matching for Multimodal Trajectories Generation in End-to-End Autonomous Driving
- **作者/载体**：Zebin Xing 等；arXiv [2503.05689](https://arxiv.org/abs/2503.05689) v6（2025-03-07 首发）；abs 页无 Comments，录用信息未获取
- **代码**：[YvanYin/GoalFlow](https://github.com/YvanYin/GoalFlow)（见 [code/repositories.md](../../../code/repositories.md)）
- **证据等级**：全文（arXiv HTML 逐节提取）+ 摘要
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> To resolve the trajectory divergence problem inherent in diffusion-based methods, GoalFlow constrains the generated trajectories by introducing a goal point. GoalFlow establishes a novel scoring mechanism that selects the most appropriate goal point from the candidate points...

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 生成机制 | Rectified Flow（flow matching 的 OT 直线路径） | Eq.1–2 |
| 噪声起点 | 纯高斯 x0~N(0,σ²I)；**σ 必须 <0.1 才稳定**（σ 过大性能骤降，σ 过小退化为回归） | Table 4 |
| 条件 | 训练时按 classifier-free guidance 随机 mask 条件；**goal 条件**=4096/8192 聚类 goal 词表 + 距离分数 δ^dis 与可行驶区域分数 δ^dac 选点；**无 classifier guidance** | §3.2.3、§4.4 |
| 输入 | 相机（前/左/右拼接）+ LiDAR，Transfuser 式融合成 BEV；含 HD map / 3D bbox 辅助监督 | §3.2.2 |
| 输出 | 候选轨迹集（生成 128/256 条选 1 条）；4 秒 @2 Hz，LQR 插值到 10 Hz | §4.2、§4.4 |
| 训练 | 分阶段：先单独训感知（L_HD/L_bbox/L_loc 权重 10/1/10）→ goal 构造器（CE）→ planner 用 L1 对齐 flow 向量场；**无 RL** | Eq.13–17 |
| NAVSIM Test | **PDMS 90.3**（NC 98.4 / DAC 98.3 / TTC 94.6 / CF 100 / EP 85.0）；GT 终点作 goal 的变体 92.1；人类 94.8 | Table 1 |
| 步数-延迟 | 20 步 177.8 ms（89.9）；10 步 92.4 ms（90.1）；**5 步 49.0 ms（90.3）**；1 步 10.4 ms（88.9） | Table 3 |
| 消融 | 无 goal 85.6 → +距离分数 88.5 → +DAC 分数 89.4 → +轨迹 scorer 90.3 | Table 2 |

## 作者自述局限

- 无独立局限章节；明确承认**预测 goal point 可能出错并误导轨迹**，用 shadow trajectory 兜底（§3.2.4）。

## 对本项目的意义

- 是流匹配路线的事实基准：MeanFuser、WAM-Flow、DiffusionDriveV2 都直接与它比较。
- 对本项目最重要的两条信息：
  1. **goal 条件是当前最有效的条件形式**（+4.7 PDMS，Table 2），但它的失败模式（goal 选错）被作者自己承认。
  2. **5 步是性价比拐点**（49.0 ms / 90.3），1 步掉到 88.9——说明"少步化"不是无代价的。

## 待核验

- Table 1 中未列 DiffusionDrive，跨论文比较只能靠 DiffusionDriveV2 的反向引用（GoalFlow ResNet-34 85.7 / V2-99 90.3），backbone 不同不可横比。
- 训练总预算与感知预训练成本（正文未给）。

## 代码核验（2026-09-23）

| 项 | 代码证据 |
|---|---|
| **主干确证沿用 TransFuser** | `navsim/agents/goalflow/resnet_backbone.py` 首行 docstring 原文 **"Implements the TransFuser vision backbone."**；`goalflow_config.py` 与 navsim 的 `transfuser_config.py` **逐字段相同**（`resnet34/resnet34`、LiDAR ±32 m、`pixels_per_meter=4.0`、`hist_max_per_pixel=5`、相机 1024×256、LiDAR 256×256、anchors 8/32/8/8、`n_layer=2/n_head=4/n_scale=4`、`bev_features_channels=64`、`num_bev_classes=7`）。→ 是 **navsim 的 TransFuser 适配版**，不是 CARLA 原版（原版 `pixels_per_meter=8.0`、`n_layer=8`、相机 960×480） |
| **主干比 DiffusionDrive 宽一倍** | agent yaml（`goalflow_agent_traj.yaml:30`）覆盖 **`tf_d_model: 512`**，而 DiffusionDrive 是 **256**、MeanFuser 是 **128**；`tf_num_layers 3` / `tf_num_head 8` 相同 |
| **训练视野比 DiffusionDrive 长，但输出被切成同样长** | `trajectory_sampling = TrajectorySampling(time_horizon=5.5, interval_length=0.5)` → **训练目标 11 点 / 5.5 s**（DD、MeanFuser 为 8 点 / 4 s）；但 `goalflow_model_traj.py:407-410` 是 `pred_trajs[:,:,1:1+8,:].mean(1)`——**输出前切成前 8 点**，`Trajectory.__post_init__`（`dataclasses.py:215-225`，默认 4 s/0.5 s）也断言必须 8 点 |
| **评测视野 4.0 s** | scorer 与 simulator 的 `proposal_sampling` 是 NAVSIM 标准 `40 poses @ 0.1 s`；→ **第 9–11 点（4.0–5.5 s）参与训练却不参与打分**（机制是**模型侧截断**，不是 simulator 截断） |
| **最终输出是"128 条采样的均值"，不是选优** | 公开评测脚本 `scripts/evaluation/run_goalflow_trajs.sh` 用 `agent=goalflow_agent_traj`（`anchor_size=128`、`use_nearest=false`、`ep_score_weight=0.0`）；`pred_trajs[:,:,1:1+8,:].mean(1)` 对 **128 条流轨迹取均值**。`use_nearest=true` 时才改为按到 navi 目标点的距离 `argmin` 选一条（可选叠加 `ep_score_weight` 的 progress 项） |
| 主干选项 | 有 `v99_pretrained_path`，即存在 **V2-99 主干**选项（对应它自报的"ResNet-34 85.7 / V2-99 90.3"两档） |
| 词表字段 | `voc_path: ''`（未启用）；`infer_steps: 100` |

**对"85.7 vs 90.3 矛盾"的补充解释**：除 backbone（ResNet-34 vs V2-99）外，GoalFlow 与 DD/MeanFuser 之间还有 **`tf_d_model`（512 vs 256/128）** 一重差异；训练视野虽然更长（11 点 vs 8 点），但**输出前被切齐到 8 点**，所以视野不构成横比障碍——真正的障碍是**主干宽度**。

完整对照表见 [diffusion_planner_code_traces.md §F](../../../code/traces/diffusion_planner_code_traces.md)。
