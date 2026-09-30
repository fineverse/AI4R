# navhard 竞品登记表（非扩散 / 选择式方法）

更新时间：2026-09-30
**为什么单独成表**：[研究对象表](diffusion_planner_ad.md)（DP-A）的纳入标准是"**扩散 / 流匹配 / 扩散桥作自车规划器**"；而 navhard 榜单前列里有一批**选择 / 评分式（非生成式）**方法——它们是本项目要超越的**对手**，也是"子榜辩护"的直接依据，但**不符合 DP-A 的纳入标准**。此前它们只散落在 [sota-plan.md §1](../../../ideas/sota-plan.md) 里，**没有各自的证据等级、代码状态与 venue 记录**，故在此正式登记。

编号规则：`DP-Cxx`（C = Competitor）。分数与代码状态**直接取自 [sota-plan.md §1](../../../ideas/sota-plan.md)**（来源 = DriveFuture Table 1 逐格核验 + 子代理逐仓库核验 + 第三十六至三十八轮的文件级更正），**本表不新增核验**。

> **⚠ 口径警告**：本表分数是 DriveFuture 表里的 **`EPDMS`（修复后官方实现）**；各论文自报的数字多为修复前的 `EPDMS*`，**同一方法两套实现差 2.0–5.2 分**。**列内排序可用、行间分差不作精度用**。详见 [benchmarks.md §2.3/§2.9](../../../direction/benchmarks.md)。

## 竞品表

| ID | 方法 | navhard EPDMS | 论文 / venue | 官方代码 | 代码实际状态 | 生成式？ |
|---|---|---|---|---|---|---|
| DP-C01 | **DrivoR** | **54.6**（榜二） | arXiv 2601.05083 / **CVPR 2026** | **无** | 摘要仅写 "Code and checkpoints **will be made available**"，**无仓库、无 project page** | **否**（纯 Transformer，proposal 生成 + 评分） |
| DP-C02 | **SimScale** | **53.2** | arXiv 2511.23369 / **CVPR 2026 Oral** | [OpenDriveLab/SimScale](https://github.com/OpenDriveLab/SimScale) | **真实现 + checkpoints**（327★ / Apache-2.0 / 2026-09-18 仍在更新） | **不是规划器**——是 **sim-real co-training 框架，模型无关**（已测 LTF / DiffusionDrive / GTRS-Dense） |
| DP-C03 | **GTRS-E** | **49.4** | arXiv 2506.06664（CVPR 2025 AGC **冠军方案**） | [NVlabs/GTRS](https://github.com/NVlabs/GTRS) | **真实现，但 49.4 不可复现**——`GTRS-E` = **六个模型的集成**（Table 2 题注原文），仓库只发 **4 个 ckpt、其中仅 2 个属于这六个**（`gtrs_dense_vov` 41.7 / `gtrs_aug_vov` 42.1，都是 V2-99）→ **可复现单模最高 42.1** | **半生成**（含扩散轨迹生成器，主体是词表评分） |
| DP-C04 | **ZTRS** | **48.1** | arXiv 2510.24108 / **ECCV 2026** | [woxihuanjiangguo/ZTRS](https://github.com/woxihuanjiangguo/ZTRS) | **真实现 + checkpoint**（77★）。⚠ **自报 45.5 vs 本表 48.1，差 2.6**——与 §7.7.5 的"两套 `EPDMS` 实现"差同量级（**原因待核，不可断言**） | **否**（离散词表 + RL/EPO，选择式） |
| DP-C05 | **DriveSuprim** | **42.1** | arXiv 2506.06659 / **AAAI 2026** | [William-Yao-2000/DriveSuprim](https://github.com/William-Yao-2000/DriveSuprim) | **真实现 + checkpoints**（38★） | **否**（coarse-to-fine 词表评分） |

## 在榜但已登记在别处的（指针）

| 方法 | navhard EPDMS | 登记位置 |
|---|---|---|
| **DriveFuture** | **55.5**（榜一） | [DP-A31](diffusion_planner_ad.md)（= WM-09）；**无代码** |
| **DiffVLA** | 45.0 | [DP-A27](diffusion_planner_ad.md)（= VLA-06）；**发布版已换头，45.0 不可复现** |
| **DIVER** | 43.4 | [DP-A16](diffusion_planner_ad.md)；真实现 |
| **GuideFlow** | 27.1（社区口径）/ 43.0（自报） | [DP-A12](diffusion_planner_ad.md)；**43.0 不可复现** |
| **World4Drive** | 34.9 | [WM-07](../../world-model/papers.md) |
| **MindDrive** | 30.9 | [VLA-12](../../vla/papers.md) |
| **DiffusionDrive** | 24.2 | [DP-A02](diffusion_planner_ad.md)；本项目路线 B 起点 |
| **TransFuser** | 23.1 | [E2E-07](../../../direction/notes/E2E-07-transfuser.md) |

## 三条对本项目的直接含义

1. **榜一、榜二都无代码**（DriveFuture 55.5 / DrivoR 54.6）→ navhard 的"头部"当前拿不到，**"复现榜一"这条路不可行**；
2. **本表 5 个竞品里 5 个都不是"纯扩散规划器"** → **"有代码的纯扩散规划器"这个子榜在发布代码层面是空的**（见 [sota-plan.md §3](../../../ideas/sota-plan.md)）——这是"子榜可辩护性"的依据；
3. **SimScale（C02）是唯一"有代码 + 有 ckpt"的榜首段方法**，且它发布了 **DiffusionDrive 的 navhard ckpt** → **路线 B 第一步（纯推理测天花板）可基于它启动**，无需训练（见 [experiments/protocol.md](../../../experiments/protocol.md)）。
