# DP-E15 · DPPO（在线 RL 微调扩散策略）

- **原题**：Diffusion Policy Policy Optimization
- **作者/载体**：Allen Z. Ren 等；arXiv [2409.00588](https://arxiv.org/abs/2409.00588) v3（2024-09 首发，2024-12 更新）
- **代码**：见项目页（未核验）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 核心思路 | 把**去噪链嵌入环境 MDP**，构成"双层 MDP"，用 PPO 策略梯度微调；优势函数含**去噪折扣** γ_DENOISE | §4.1–4.2、Def 4.1 |
| 训练流程 | 预训练 BC（K=20 状态 / 100 像素）→ 在线 RL 微调**最后 10 步**或 5 步 DDIM | §5.3 |
| 细节 | σ_min clip 0.01–0.1、cosine schedule；action chunk Ta=4（Gym/Kitchen）、4/8（Robomimic）、8（Furniture） | §4.3、§5.3 |
| 关键结论 | **值估计只依赖 state 最关键**；噪声 clip 有 sweet spot；微调 K′=10 最省（K′=3 次优）；Ta=16 仍稳定 | §5.5、附录 C.2、Fig.A5 |
| 结果 | 状态/像素下均超 Gaussian/GMM 基线（Transport >90%，**首个 >50%**）；真机 One-leg **DPPO 80%（16/20）vs Gaussian 0%** | Fig.7/8 |
| 训练成本 | Gym 平均比 DAWR/DIPO/DQL 快 41%/37%/12%，比 QSM/DRWR/IDQL 慢 43%/33%/7% | Table A1–A5 |
| 频率 | 真机 10 Hz（底层阻抗控制 1 kHz） | §5 |
| 自述局限 | 样本效率低于 off-policy 方法 | §7 |

## 对本项目的意义（AI 判断）

- **最实用的一条路线**：BC 预训练 + 在线 RL 微调，对应驾驶侧的"模仿学习基线 + RL 后训练"（DDV2、DIVER 都在做，但用的是离线 GRPO/REINFORCE）。
- **明确不成立/需注意**：DPPO 需要**在线交互**；驾驶中真实道路在线试错不可接受，只能在高保真仿真（CARLA/Bench2Drive）里做——这正是 DiffusionDrive 家族走 NAVSIM 离线 RL 的原因。
- 可借的具体细节：**只微调最后 10 步**（而不是整条链）显著省算力；**值估计只依赖 state**；噪声 clip 有最优区间。这些在驾驶侧还没有系统验证。

## 待核验

- 官方代码；"微调最后 10 步"在 2 步截断扩散（DiffusionDrive）上是否还有意义。
