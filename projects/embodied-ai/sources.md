# 具身智能来源索引

更新时间：2026-09-23  
只登记**归属本项目**的来源；自动驾驶侧来源见 [autonomous-driving/sources.md](../autonomous-driving/sources.md)。

## 来源登记

| 编号 | 来源 | 来源角色与当前状态 | 后续关注 |
|---|---|---|---|
| L005 | [具身与通用决策扩散规划器论文表](topics/diffusion-policy/papers/diffusion_planner_embodied.md)（[CSV](topics/diffusion-policy/papers/diffusion_planner_embodied.csv)） | 2026-09-22 检索；DP-E01…DP-E28，含"可迁移机制"小节（待验证假设）与引用快照 | 迁移机制落到驾驶前需重新验证；优先 DP-E09、DP-E17、DP-E08 |
| L014 | 具身侧论文笔记 9 篇 | [DP-E01](topics/diffusion-policy/notes/DP-E01-diffuser.md)、[DP-E04](topics/diffusion-policy/notes/DP-E04-diffuserlite.md)、[DP-E08](topics/diffusion-policy/notes/DP-E08-safeflowmatcher.md)、[DP-E09](topics/diffusion-policy/notes/DP-E09-diffusion-policy.md)、[DP-E10](topics/diffusion-policy/notes/DP-E10-dp3.md)、[DP-E11](topics/diffusion-policy/notes/DP-E11-consistency-policy.md)、[DP-E15](topics/diffusion-policy/notes/DP-E15-dppo.md)、[DP-E17](topics/diffusion-policy/notes/DP-E17-nomad.md)、[DP-E19](topics/diffusion-policy/notes/DP-E19-pi0.md) | 均全文级（arXiv HTML 逐节提取或 PDF 逐表核对） |
| B009 | [RoboMimic](https://arxiv.org/abs/2108.03298)（[项目页](https://robomimic.github.io/)） | 离线人类示范的学习与基准（CoRL 2021） | 与具身侧监督信号设计的对照 |
| B010 | [LIBERO](https://arxiv.org/abs/2306.03310)（[项目页](https://libero-project.github.io/)） | 终身机器人学习的知识迁移基准 | 跨任务迁移评价，对应驾驶跨场景泛化 |
| B011 | [EBench](https://arxiv.org/abs/2606.18239) | 通用移动操作策略的要素级诊断基准（26 任务 / 5 能力 / 4 泛化维度） | 反例参照：单一成功率标量不足以诊断策略 |

## 与自动驾驶项目的交叉

- 可迁移机制的**汇总处**在自动驾驶侧：[transfer.md](../autonomous-driving/topics/diffusion-planner/transfer.md)
- **代码仓库跨项目共用**：具身侧的 6 个仓库保存在自动驾驶项目的 `code/repos/`，未按项目拆分——**理由与完整清单见 [workspace-design.md](../../shared/workspace-design.md) §当前落地状态**（此处不重复）
