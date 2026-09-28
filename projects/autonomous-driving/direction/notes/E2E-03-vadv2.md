# E2E-03 · VADv2（动作词表概率分布 —— 扩散规划器的思想前身）

- **原题**：VADv2: End-to-End Vectorized Autonomous Driving via Probabilistic Planning
- **作者/载体**：Bo Jiang 等（hustvl）；arXiv [2402.13243](https://arxiv.org/abs/2402.13243) v2；**页眉标注 ICLR 2026**
- **代码**：**部分发布** — [hustvl/VAD](https://github.com/hustvl/VAD)（与 VAD 同仓）。`VADv2/` 目录下**只有两个文件**（`VADv2_config_voca4096.py` + `VADv2_head.py`），README 原文："Core code of VADv2 (config and model) is available in the `VADv2` folder. **Easy to integrate it into the VADv1 framework**"（2026-09-23 核验）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22
- **为什么它对本项目最重要**：它的"动作词表 + 概率分布"是 **DiffusionDrive 锚点先验的直接思想前身**。

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 场景表征 | 向量化 + **场景 token 化**：map / agent / traffic element / image 四类 token；agent token 沿用 VAD | §3.1 |
| 规划输出 | **动作词表 V 上的概率分布 p(a)**，默认 **N=4096**；推理取最高概率动作 | §3.2、§3.4 |
| 时间规格 | 3s 未来、**6 个 waypoint、间隔 0.5s**，控制 10 Hz | §4.1 |
| 规划架构 | 级联 Transformer decoder：query=轨迹 token，key/value=scene token，接 sigmoid MLP；与感知 token 联合训练（辅助：建图、检测/运动预测、红绿灯/停车标志） | Eq.3 |
| 监督 | IL（分布用 KL/交叉熵）+ 冲突项（负样本）+ token 项 | Eq.4–7 |
| 主结果 | CARLA Town05 Long **DS 85.1 / RC 98.4 / IS 0.87**（Tab.1）；**Bench2Drive DS 76.15 / SR 50.46**（Tab.5）；**NAVSIM navtest PDMS 89.3**（Tab.2）；NAVSIMv2 EPDMS 85.8（Tab.3）；3DGS 基准 CR 0.270（Tab.4） | 各表 |
| 推理成本 | **未获取**（未报 FPS/延迟） | — |
| 自述局限 | 仿真与 3DGS 闭环环境中的 agent 行为朴素、真实感不足 | §5 |

## 继承关系

- **基于**：VAD（同组）、MapTRv2、BEVFormer。
- **被谁继承**：Hydra-MDP **明确写 "Following VADv2"**（沿用其词表与解码器设计）；Hydra-MDP++、Hydra-NeXt 延续该线；**DiffusionDrive 的锚点词表（K-means 聚类）在思想上与之同源**，区别在于 DiffusionDrive 用扩散过程在词表上"生成/精修"，而 VADv2 是分类式取最大概率。

## 对本项目的意义（重要）

1. **"多模态候选 + 先验词表"不是扩散带来的**：这条思想在 2024 年初的 VADv2 就已成立，Hydra-MDP 随即沿用。扩散规划器真正的贡献是**在词表上做连续生成与精修**（以及后来的"无词表"方案，如 MeanFuser 的高斯混合噪声）。
2. **一条必须正视的对照**：VADv2 报 NAVSIM navtest PDMS **89.3**，高于 DiffusionDrive 的 88.1。但两者 backbone/输入权限不同，**不可直接横比**（[preparation.md 第 6 节](../../ideas/preparation.md)）。
3. **它把规划输出变成分布，使"规则/优化模块可即插即用"**（§3.4）——这与后来"用 RL 奖励约束生成质量"（DIVER、DDV2）是同一动机的不同实现。

## 代码核验（2026-09-23）

读 `VADv2/VADv2_config_voca4096.py` 与 `VADv2/VADv2_head.py`，**核心机制全部得到代码确认，且比论文写得更彻底**：

| 项 | 代码证据 |
|---|---|
| 词表与规模 | `plan_anchors_path='carla_plan_vocabulary_4096.npy'`；`plan_fut_mode=256`（训练）/ `plan_fut_mode_testing=4096`（推理）；`valid_fut_ts=6`、`Dt = 0.5`（3 s / 6 点 / 0.5 s） |
| **回归分支被丢弃** | `outputs_ego_trajs = self.plan_reg_branch(ego_feats)` 算完后，下一行 **`outputs_ego_trajs = outputs_ego_trajs * 0. + self.used_plan_anchors[None]`**——回归输出被**乘 0 整体替换为锚点**。**规划输出只能是词表里的一条** |
| 监督只剩分类 | `loss_plan_cls_expert` 权重 **200.0**；而 `loss_plan_cls_col` / `_bd` / `_cl`、`loss_plan_reg`、`loss_plan_bound`、`loss_plan_agent_dis`、`loss_plan_map_theta` **权重全为 0.0**——已发布配置里**冲突项与回归项全部关闭** |
| query 来自锚点 | `pos2posemb2d(used_plan_anchors...)` → `ego_query_pre_branch`；可学习的 `nn.Embedding(plan_fut_mode, ...)` 那行**被注释掉** |
| 训练采样策略 | 每步从 4096 条里 **`torch.multinomial(..., 256, replacement=False)`** 随机取 256 条，并把 **GT 最近的锚点强行塞进这批**（`used_index[-1] = best_match_idx`，由 `cumsum` 后 L2 距离 `argmin` 得到） |
| 运动学掩码 | `kinodynamic_mask = (norm(anchors[:,0,:]) - pred_dis).abs() < 1e11`——阈值 **1e11**，等价于**不过滤**（疑似遗留代码） |
| 停车轨迹 | 位移近 0 的锚点强制置零，并**固定 `used_plan_anchors[0] = 0.`**（词表第 0 条永远是"停住"） |

**开箱不可运行的三个原因**：① `v116ADTRHead` / `v116ADTR` **在整个仓库里没有任何注册**（`grep` 无结果）；② 词表 `carla_plan_vocabulary_4096.npy` **未随仓库发布**（VAD 全仓 0 个 `.npy`）；③ 论文未给词表构造脚本。

**谱系含义**：本笔记第 30 行的判断（"先验词表不是扩散带来的"）已由代码确认——VADv2 比后来的扩散方案**更彻底**，连回归都不要。完整五环谱系见 [e2e_trunk_code_traces.md](../../code/traces/e2e_trunk_code_traces.md) §C。
