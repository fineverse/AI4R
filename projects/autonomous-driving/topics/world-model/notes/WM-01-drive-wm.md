# WM-01 · Drive-WM（首个与端到端规划器兼容的驾驶世界模型，CVPR 2024，100 引用）

- **原题**：Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving
- **作者/载体**：Yuqi Wang 等；arXiv [2311.17918](https://arxiv.org/abs/2311.17918)；**CVPR 2024**（综述 [2512.16760](https://arxiv.org/abs/2512.16760) §3.2 表标注）
- **代码**：**部分** — [github.com/BraveGroup/Drive-WM](https://github.com/BraveGroup/Drive-WM)（`comments` 标注）。2026-09-23 克隆核验：仓库是 **vendored `diffusers`**（`src/diffusers/`）+ 模型转换脚本，**只含图像生成侧；论文的 tree-based planner 与 image reward 不在仓库内**
- **证据等级**：全文（PDF + `pdftotext -layout`，读摘要与 Table 3/4）
- **笔记日期**：2026-09-23

## 摘要原文（节选）

> …we propose Drive-WM, **the first driving world model compatible with existing end-to-end planning models**. Through a joint spatial-temporal modeling facilitated by **view factorization**, our model generates high-fidelity multiview videos in driving scenes. Building on its powerful generation ability, we showcase the potential of applying the world model for **safe driving planning for the first time**.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 定位 | **首个与既有端到端规划模型兼容的驾驶世界模型** | 摘要 |
| 生成方式 | 联合时空建模 + **视角分解（view factorization）**，生成多视角视频 | 摘要、Table 2 |
| 视角分解的收益 | 提升多视角一致性（论文称一致性从 45.8% 提升） | Table 2c |
| 统一条件接口 | layout 条件对生成质量与一致性影响显著；论文称统一条件接口展示"世界模型可当神经仿真器"的潜力 | §5.2、Table 2a |
| **规划用法** | 用**树搜索（tree-based planner）**在三个候选命令（直行/左转/右转）中，用世界模型生成的未来**选最优命令** | §5.3、Table 3 |
| **规划结果（Table 3）** | VAD（GT 命令）L2 平均 0.72 m / 碰撞 0.22%；**VAD（随机命令）1.02 / 0.93%**；**Ours（树搜索选命令）0.80 / 0.26%** | Table 3 |
| 图像奖励设计 | 用两个子奖励（**map reward + object reward**）评估生成的未来 | Table 4 |
| OOD 规划 | 在域外场景中，用世界模型筛掉的坏情况可通过微调规划器恢复 | Table 5 |

## 局限（本笔记指出）

- **它不生成轨迹**：规划仍由 VAD 完成，世界模型只用于**在候选命令间选优**。因此它属于"生成之后的否决/选优层"，**不是"作为条件的生成器"**。
- Table 3 显示：用世界模型选命令（0.80 / 0.26%）**仍略差于直接用 GT 命令（0.72 / 0.22%）**——即选优器不完美，但远好于随机命令（1.02 / 0.93%）。

## 对本项目的意义

- **它给出了"世界模型 → 选优"这条路线的最早实证**，且量化了价值：**选优把随机命令的碰撞率从 0.93% 压到 0.26%，接近 GT 命令的 0.22%**。这是 [lineage.md](../lineage.md) 接口差异第 1 问（作为条件还是作为规划器）的第三种形态——**既不是条件、也不是规划器，而是选优器**。
- **对研究对象的直接含义**：扩散规划器本身已生成多模态候选（锚点/高斯混合），**不需要再外挂一个生成器**；需要的正是"怎么在候选里选"——这与 [preparation.md](../../../ideas/preparation.md) 的 P4（选优器是新瓶颈）**完全对上**，而 Drive-WM 提供了一个可借鉴的"用生成未来做奖励"的选优思路。
- **视角分解 45.8% 一致性提升**说明多视角一致性是世界模型质量的硬指标，但**与规划性能的关系未被量化**。
- 与 [transfer.md](../../diffusion-planner/transfer.md) 第 3 节"潜空间 rollout + 选动作"是同一族；本次读全文后其条目**可从"摘要级"升级为"全文级"**。

## 待核验

- 代码**已克隆**：只有图像生成侧，**tree-based planner 与 image reward 无代码可核验**（见 [world_model_code_traces.md](../../../code/traces/world_model_code_traces.md)）。
- 树搜索的候选数量只有 3 个（三个命令），与扩散规划器的 20–32 个锚点候选**不是一个量级**，可迁移性需评估。
