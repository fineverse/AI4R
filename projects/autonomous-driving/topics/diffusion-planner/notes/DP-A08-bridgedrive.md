# DP-A08 · BridgeDrive

- **原题**：BridgeDrive: Diffusion Bridge Policy for Closed-Loop Trajectory Planning in Autonomous Driving
- **作者/载体**：Shu Liu 等；arXiv [2509.23589](https://arxiv.org/abs/2509.23589) v4（2025-09-28 首发）；**ICLR 2026 录用**
- **代码**：未见官方仓库
- **证据等级**：全文（arXiv HTML 逐节提取）+ 摘要
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> A key challenge is how to effectively guide these models for safe and reactive planning in closed-loop settings, where the ego vehicle's actions influence future states. Recent work leverages typical expert driving behaviors (i.e., anchors) to guide diffusion planners but relies on a truncated diffusion schedule that introduces an asymmetry between the forward and denoising processes, diverging from the core principles of diffusion models.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 核心主张 | 截断扩散的前向加噪与去噪不对称，**偏离扩散模型核心原理**，可能致不可预测行为与性能受损 | 摘要、§1、§2.3 |
| 方法 | 锚点引导**扩散桥**（Doob bridge）：x_T=锚点 → x_0=轨迹；桥核 q(x_t\|x_0,x_T)=N(a_t x_T+b_t x_0, c_t²I)；PF-ODE | Eq.6–8 |
| 锚点获取 | 分类器 h_φ 预测最近锚点；一阶 DDIM 采样已足够 | §3.3 |
| 约束方式 | **无 CBF、无能量引导、无 RL**；约束只来自锚点先验 | §3.3、§4 |
| 训练 | 仿真无关；加权 MSE 去噪 + 分类器交叉熵；**无 RL** | Eq.9、Alg.1 |
| 推理成本 | **0.10 s / 20 步**（BridgeDrive_temp 与 BridgeDrive_geo 相同）；同表 DiffusionDrive 0.05 s / 2 步 | Table 7（PDF 核验） |
| Bench2Drive（CARLA LB2.0） | BridgeDrive_geo **DS 87.99±0.67 / SR 74.99±1.35** / Effi 236.49 / Comf 20.98 | Table 2、Table 5（PDF 核验） |
| NAVSIM navtest | **PDMS 88.0**（NC 98.2 / DAC 96.1 / TTC 94.5 / Comf 100 / EP 82.3）；同表 DiffusionDrive 报告 88.1、**复现 87.6** | Table 4（PDF 核验） |
| 与 DiffusionDrive 对比 | **有直接对比**，且给出对方复现值（87.6），这是本批论文中少见的严谨做法 | Table 4 |
| 消融（Table 2） | DiffusionDrive_temp 77.68/52.72、DiffusionDrive_geo 80.79/58.18；Full Diffusion_temp 79.75/58.18、Full Diffusion_geo 83.85/67.27；BridgeDrive_temp 81.97/59.90、**BridgeDrive_geo 87.99/74.99**（DS/SR）——几何路点显著优于时间路点 | Table 2（PDF 核验） |
| 舒适性代价 | 明确承认"prioritizes safety over Comfortness"：Comf 20.98，倾向频繁刹车 | §4.1、Table 2 题注 |

## 作者自述局限（§5）

- 可蒸馏为一步规划器以加速（即当前仍非一步）。
- 仍难处理 OOD 场景。

## 对本项目的意义

- 它是对 DiffusionDrive 最"理论性"的批评：**同一条锚点路线，换掉截断日程**。若本项目想动"生成日程"，必须先说明与 BridgeDrive 的差别。
- **但结果值得注意**：换成理论上更正确的扩散桥后，NAVSIM PDMS 88.0 只与 DiffusionDrive 的 88.1 追平（对方复现 87.6），代价是 20 步 vs 2 步、0.10 s vs 0.05 s。这说明"理论一致性"本身并不自动带来性能，**改进必须落在别的轴上**。
- 它的安全来自先验而非约束，代价是舒适性（Comf 20.98）——正好给"约束注入"方向留出对照：把舒适性与安全性同时显式建模。

## 待核验

- 无官方代码，复现成本高；若要作为基线需自行实现桥核与 PF-ODE。
- 摘要中"89.25% SR / 96.34 DS（LEAD）"与 Table 2/5 的 74.99/87.99 口径不同（可能 LEAD 指不同配置），需回原文确认，当前两处并存记录。
