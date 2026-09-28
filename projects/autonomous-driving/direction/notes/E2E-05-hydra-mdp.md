# E2E-05 · Hydra-MDP（规则教师多目标蒸馏）

- **原题**：Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation
- **作者/载体**：Zhenxin Li 等（NVIDIA）；arXiv [2406.06978](https://arxiv.org/abs/2406.06978) v4（2024-08-30）；技术报告，**NAVSIM 挑战赛第 1 名**
- **代码**：**无** — [NVlabs/Hydra-MDP](https://github.com/NVlabs/Hydra-MDP) 已克隆，但**仓库为零代码**（仅 `README.md` + 一张示意图）；README 原文："Delay in code and model release due to company policy. Stay tuned for updates."（2026-09-23 核验）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22

## 为什么它重要

它是**"规则教师蒸馏"这一支的代表**：把 NC / DAC / TTC / 舒适性 / 进度等**子分数**作为教师信号训练多个头，是后来 DIVER 复用 PDMS 奖励的直接来源。

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 场景表征 | 沿用 **Transfuser** 的 LiDAR BEV + 前视拼接图像 → environmental tokens（未自建新表征） | §2.2 |
| 规划输出 | **词表上的概率分布 + 多目标子分数**：词表由 nuPlan 采 **700K 轨迹 K-means** 得 V_k（k=4096/8192）；每条 40 个时间戳 (x,y,heading)、10 Hz、4s 未来；推理按代价取最低 | §2.2、Eq.11 |
| 规划架构 | 多 head 轨迹解码器（Transformer encoder+decoder）；感知网沿用 Transfuser；与感知联合训练（辅助：3D 检测、BEV 分割） | §2.2 |
| 监督 | IL + **规则教师多目标蒸馏**：L = L_im（对 L2 距离软标签做交叉熵）+ L_kd（对 NC/DAC/TTC/C/EP 子分数做 BCE） | Eq.8–10 |
| 主结果 | NAVSIM navtest PDMS **82.6**（V4096）→ **86.5**（V8192-W-EP）（Tab.1）；扩模型后 **89.9 / 90.3 / 91.0**（Tab.2） | Tab.1/2 |
| 推理成本 | **未获取**（仅列 8×A100 训练配置） | §3.2 |
| 自述局限 | **无独立局限章节**；文中提到 PDM 整体分数分布不规则会导致退化，故需多目标学习 | §3.3 |
| 继承 | **明确 "Following VADv2"**（词表与解码器设计）+ Transfuser（感知）；被 Hydra-MDP++、Hydra-NeXt 延续 | — |

## 对本项目的意义

1. **它把"评价指标"变成了训练信号**：NC/DAC/TTC/C/EP 这些子分数既是评测项也是蒸馏目标。这带来一个值得警惕的循环——**指标既当裁判又当教练**，S032 §VII.C 的"子指标饱和"与这种耦合直接相关。
2. **DIVER 复用了它的 PDMS 奖励**（本项目 DP-A16 笔记已记），说明扩散规划器的 RL 后训练在奖励设计上**没有独立于这条线**。
3. **它的 91.0 是本项目目前看到 NAVSIM navtest 上最高的数字之一**（与 DiffusionDriveV2 的 91.2 同量级），但 backbone 与输入权限不同，**不可直接横比**。

## 代码核验（2026-09-23）

- **仓库零代码**，本笔记的全部内容**只能停留在论文自述级**，机制无法做代码级核验。
- **它在代码谱系上是一个断点**：`轨迹词表 + 选优` 这条线的前一环 VADv2（4096 词表、纯分类，代码可见）与后一环 DiffusionDrive（20 锚点当扩散先验，代码可见）**都能核验**，只有中间的 Hydra-MDP 不能。详见 [e2e_trunk_code_traces.md](../../code/traces/e2e_trunk_code_traces.md) §C。
- 其词表规模（4096 / 8192）与 **DiffusionDriveV2 仓库内的 `gtrs_traj/16384.npy`** 属同一机制族，但**后者与前者的继承关系只能凭论文与 README 推断**，无代码证据。
