# E2E-11 · DriveLM（Graph VQA：把规划写成问答）

- **原题**：DriveLM: Driving with Graph Visual Question Answering
- **作者/载体**：Chonghao Sima 等（OpenDriveLab 等）；arXiv [2312.14150](https://arxiv.org/abs/2312.14150) v3（2025-01）；ECCV 2024
- **代码**：[OpenDriveLab/DriveLM](https://github.com/OpenDriveLab/DriveLM)（已下载）
- **证据等级**：全文（PDF 正文抽取缺失，改用官方 HTML v3 复核）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 输入 | 低分辨率前视图 + 文本 QA 图；**无 LiDAR、无时序** | §4.2、Discussion |
| 输出 | 语言 QA（感知 P1-3 / 行为 B / 运动 M）+ 行为（速度/转向 5 bins）+ 航点（轨迹 token 化，256 bins） | §2.1、附录 E.2 |
| 监督 | VLM 监督微调（BLIP-2 / LLaMA-Adapter，LoRA）下一 token 预测 + 图提示 / teacher forcing | 附录 E.1 |
| 关键设计 | **Graph VQA 任务 + 数据集 + 指标 + DriveLM-Agent baseline**（数据：DriveLM-nuScenes 144k QA、CARLA 697k QA） | 摘要、§2、Table 1 |
| 主结果 | nuScenes 开环：DriveLM-Agent Graph **ADE 1.74m / 碰撞 1.89%**（UniAD-Single 1.80/2.62；BLIP-RT-2 2.63/2.77）；Waymo zero-shot ADE 2.63/FDE 6.17（UniAD-Single 4.16/9.31） | Table 2 |
| 推理成本 | 3.955B 参数（12.9M 可训）/ 24.2T FLOPs / **0.16 FPS**（约 10× 慢于 UniAD 的 1.8 FPS） | Table 5 |
| 自述局限 | 效率低；仅前视、无 LiDAR/360°；**仅开环** | Discussion |

## 在脉络中的位置

- **继承**：BLIP-2 / RT-2 的 token 化思路；与 UniAD-Single 对比。
- **转折意义**：它把"规划"重写成**图结构的问答任务**，并配套数据集与指标——属于输出接口与评测口径的双重创新。

## 对本项目的意义

**0.16 FPS** 是本项目见过的最低实时性之一。它说明语言接口路线的代价不在"模型大小"而在"自回归解码"。若本项目要在驾驶规划里用语言，**必须是非自回归/可并行的形式**（WAM-Flow 的离散流匹配正是这个方向，见 DP-A13）。
