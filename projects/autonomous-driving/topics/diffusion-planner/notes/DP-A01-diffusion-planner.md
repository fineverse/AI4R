# DP-A01 · Diffusion Planner（扩散规划器）

- **原题**：Diffusion-Based Planning for Autonomous Driving with Flexible Guidance
- **作者/载体**：Yinan Zheng 等；arXiv [2501.15564](https://arxiv.org/abs/2501.15564) v2（2025-01-26 首发，v2 2025-02-09）；**ICLR 2025**（从同组后续工作 Flow Planner 的 BibTeX 得到，见 [DP-A11 行](../papers/diffusion_planner_ad.md)）
- **代码**：[ZhengYinan-AIR/Diffusion-Planner](https://github.com/ZhengYinan-AIR/Diffusion-Planner)（已保存快照，见 [code/repositories.md](../../../code/repositories.md)）
- **证据等级**：全文（arXiv HTML 逐节提取）+ 摘要
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> We propose a novel transformer-based Diffusion Planner for closed-loop planning, which can effectively model multi-modal driving behavior and ensure trajectory quality without any rule-based refinement. Our model supports joint modeling of both prediction and planning tasks under the same architecture, enabling cooperative behaviors between vehicles. Moreover, by learning the gradient of the trajectory score function...

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 输入表示 | 矢量化：当前状态、历史帧、车道 polyline、静态物体、导航 route 车道；**无 BEV、无图像** | §4.2 |
| 输出 | ego + M 个最近邻车的**未来轨迹联合生成**，8 秒 @10 Hz | §4.4 |
| 多模态方式 | 每次推理只出 1 条；多模态靠多次采样 + 低温采样 | §5.1 |
| 噪声起点 | 纯高斯 x^t→N(0,I)，学 score 的 DiT | Eq.1 |
| 采样器 | DPM-Solver + 低温采样；正文未给去噪步数（附录 C.3 表 5 仅网格搜索） | §4.4 |
| 引导 | **训练无关的 classifier guidance**（diffusion posterior sampling 近似），论文 Eq.8 的能量函数含**目标车速 / 舒适 / 避碰 / 可行驶区域四项** | Eq.8、§4.3 |
| 训练目标 | 单阶段扩散重建 L=‖μθ(x^t,t,C)−x^0‖²；联合预测+规划；数据增强（扰动当前状态 + 插值）+ z-score 归一化；**无 RL/后训练** | Eq.5 |
| 推理成本 | 约 20 Hz；附录 E 给"8 秒@10 Hz 耗时 0.05 秒" | §4.4、附录 E |
| nuPlan Val14（NR/R） | 无 refine 89.87/82.80；**加 refine 94.26/92.90** | Table 1 |
| nuPlan Test14-hard | 无 refine 75.99/69.22；加 refine 78.87/82.00 | Table 1 |
| 自采数据 | 200 小时配送车数据，92.08 | Table 2 |
| 消融（Test14） | base 89.19；去 z-score 85.02、去插值 83.78、去增强 76.53、加 ego 状态 78.65、SDE 82.90；预测车辆数过多引入噪声 | Table 3、Fig.6/7 |

## 作者自述局限（附录 E）

1. 依赖矢量化地图 + 检测，存在信息损失。
2. **横向灵活性差**（大幅变道/避让弱），且输出轨迹与下游控制器之间存在 gap。
3. **样本效率低**，未来可用一致性模型/蒸馏加速。

## 对本项目的意义

- 不同基准（nuPlan 闭环 vs NAVSIM 非反应式），**无直接比较**。
- 路线差异：Diffusion Planner 是"纯噪声起点 + 多步 + classifier guidance + 联合预测规划"；DiffusionDrive 是"锚点先验 + 2 步截断扩散 + 单帧规划"。前者强调无需规则后处理，后者强调实时。
- 对本项目的意义：它证明"引导可以替代规则后处理"，但横向灵活性与样本效率是明确短板；这两点是可以被攻击的接口。

## 代码核验（2026-09-23）

读 `diffusion_planner/model/guidance/`、`model/diffusion_utils/sampling.py`、`model/module/decoder.py`：

| 项 | 代码证据 |
|---|---|
| **引导只有 1 项（需更正上表）** | `guidance_wrapper.py`：**`self._guidance_fns = [collision_guidance_fn]`**；`model/guidance/` 目录下**只有 `collision.py`**（外加一篇 `documentation_guidance.md` 教用户自己加）。→ 论文的**目标车速 / 舒适 / 可行驶区域三项引导未发布**，只有避碰 |
| **引导只作用于扩散末段** | `collision.py:70-71`：`mask_diffusion_time = (t < 0.1 and t > 0.005)`，`x = torch.where(mask_diffusion_time, x, x.detach())`——t 不在此区间时**梯度被切断** |
| **引导强度硬编码** | `collision.py:126` `return 3.0 * reward`；`decoder.py:136` `guidance_scale=0.5` → 有效强度 **1.5** |
| **噪声起点** | `decoder.py:105`：`torch.cat([current_states[:, :, None], torch.randn(...) * 0.5], dim=2)`——**未来帧噪声尺度 0.5**（非标准 1.0） |
| **硬约束** | `decoder.py:107-110, 121`：`initial_state_constraint` 作为 `correcting_xt_fn`——**每一步都把第 0 帧强制重置为当前状态** |
| **去噪步数（原待核验项，已解决）** | `sampling.py:10`：**`diffusion_steps=10`**；DPM-Solver++、`order=2`、`skip_type="logSNR"`、`method="multistep"`、`denoise_to_zero=True`；注释："Steps in [10, 20] can generate quite good samples. And steps = 20 can almost converge." |
| **避碰能量实现** | 有向矩形距离（SAT 投影法）`batch_signed_distance_rect`；`INFLATION = 1.0` m、`CLIP_DISTANCE = 1.0`；距离分 >1 / ≤1 两组各取均值相加再 `.exp()`；梯度经 **21 点高斯核 conv1d 做时间维平滑**；自车几何硬编码 `COG_TO_REAR = 1.67` + nuPlan Pacifica 参数 |

**"refine" 的歧义已澄清（原待核验项）**：README 表里的 "w/ refine (ours)" / "w/o refine." 是 **nuPlan 闭环评测的口径**，不是本仓库的功能；仓库内 `data_augmentation.py` 的 `refine_horizon` / `num_refine` 是**数据增强用的五次样条插值**，与评测口径无关。

**顺带更正一条文献记录**：上游 README 直链了同组的 **Flow Planner（NeurIPS 2025）= `DiffusionAD/Flow-Planner`**，而本项目论文表把 **DP-A11 Flow Planner 记作"未见官方"——这条是错的**（见 [papers/diffusion_planner_ad.md](../papers/diffusion_planner_ad.md) DP-A11 行）。
