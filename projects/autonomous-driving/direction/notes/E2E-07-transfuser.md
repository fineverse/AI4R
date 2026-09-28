# E2E-07 · TransFuser（输入表示转折：注意力融合 + 去特权）

- **原题**：Multi-Modal Fusion Transformer for End-to-End Autonomous Driving
- **作者/载体**：Aditya Prakash 等（autonomousvision）；arXiv [2104.09224](https://arxiv.org/abs/2104.09224) v1（2021-04）；CVPR 2021
- **代码**：[autonomousvision/transfuser](https://github.com/autonomousvision/transfuser)（已下载，分支 2022）
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 输入 | 前视 RGB 400×300 → 256×256（FOV 100°）+ LiDAR BEV 32m×32m、0.125m/px、256×256×2ch；**输入侧无特权**，仅稀疏 GPS 目标 + 导航命令 | §3.2、§4 |
| 输出 | BEV 差分航点 **T=4**，由 PID 转 steer/throttle/brake | §3.4 |
| 监督 | **纯 IL/BC**，L1 航点损失；训练数据由特权专家采集 | Eq.5、§4 |
| 关键设计 | **多尺度 transformer 全局注意力融合图像与 LiDAR**（替代此前的几何/投影融合） | 摘要、§3.3 |
| 主结果 | CARLA 0.9.10 Town05：Short **DS 54.52**/RC 78.41；Long **DS 33.15**/RC 56.36；专家 Short 84.67/Long 38.60；碰撞较几何融合降 **76.11%**、红灯违规降 21.93% | Table 1a/1b |
| 推理成本 | **未获取**（v1 无 FPS/延迟表） | — |
| 自述局限 | 红灯在对侧难见；未用语义监督；所有融合方法的红灯违规都偏高 | §4.1 |

## 在脉络中的位置

- **继承**：LBC 的蒸馏设定 + ContFuse 的几何融合。
- **转折意义**：**输入表示**的转折点——首次用注意力做 RGB+LiDAR 融合，并明确**把特权信息从输入侧移出**（只留在训练教师里）。
- **被谁继承**：TCP、ST-P3 均以它为 baseline 并超越（TCP Table 1：Transfuser 61.181 < TCP 69.714）。

## 对本项目的意义

**本项目主线的 GoalFlow 与 DiffusionDrive 都用 TransFuser 系感知主干**——它是驾驶扩散规划器最普遍继承的感知模块。两条直接后果：① 与 NAVSIM 系扩散规划器对比时，**"感知主干"这一维不是差异来源**，真正要控的是 `tf_d_model` / `lidar_seq_len` 等宽度与输入权限（见 [C003 §F](../../code/traces/diffusion_planner_code_traces.md)）；② 若本项目自建基线，**沿用 TransFuser 主干是"与榜面对齐"的最低成本选择**，代价是继承它的输入权限（相机 + LiDAR）。
