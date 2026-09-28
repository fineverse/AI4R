# E2E-09 · ST-P3（输入转折：多视角→3D→BEV，且不用 HD 地图）

- **原题**：ST-P3: End-to-end Vision-based Autonomous Driving via Spatial-Temporal Feature Learning
- **作者/载体**：Shengchao Hu 等（OpenDriveLab）；arXiv [2207.07601](https://arxiv.org/abs/2207.07601) v2（2022-07）；ECCV 2022
- **代码**：[OpenDriveLab/ST-P3](https://github.com/OpenDriveLab/ST-P3)（已下载）
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 输入 | **6 路环视视频**（过去 1.0s / 3 帧）+ 高层命令；**不使用 HD 地图** | §3.3、§4 |
| 输出 | BEV 轨迹（bicycle 采样器 + cost volume + GRU 精修），规划 horizon **3.0s** | §3.3、§4.1 |
| 监督 | 多任务端到端 IL：L = L_per + α·L_pre + β·L_pla（**α/β 可学习**）；感知含分割/实例/深度/地图，预测未来分割，规划用 max-margin + L1 | Eq.7、Eq.8 |
| 关键设计 | 三模块：egocentric aligned accumulation、dual pathway、prior-knowledge refinement（可解释的视觉 E2E） | §1、§3 |
| 主结果 | nuScenes：感知 mean IoU 42.69（Table 1）；未来分割 IoU 38.63/38.87（Table 2）；开环规划 **L2 1.33/2.11/2.90m、碰撞 0.23/0.62/1.27%**（Table 3）；CARLA Town05 Short DS 55.14/RC 86.74、Long DS 11.45/RC 83.15（Table 4） | 各表 |
| 推理成本 | 未获取 | — |
| 自述局限 | 未获取（结论无专门局限章节） | — |

## 在脉络中的位置

- **继承**：LSS / FIERY / MP3 / NMP / P3；以 Transfuser 作为 LiDAR 对照。
- **转折意义**：**输入表示**的第二次转折——从多视角视频做 3D 累积再转 BEV，并且**去掉 HD 地图**，把"地图依赖"从输入侧剔除。
- **被谁继承**：UniAD（把它的感知-预测-规划多任务结构升级为 query 打通的全栈）、DriveVLM 把它列为先前方法。

## 对本项目的意义

ST-P3 的 **CARLA Long DS 仅 11.45** 而 Short DS 55.14——**同一模型在两个难度档位差 5 倍**，这是"平均分掩盖长尾"的早期证据，与 2026 年 navhard（DiffusionDrive 24.2 vs navtest 88.1）是同一现象的历史回声。
