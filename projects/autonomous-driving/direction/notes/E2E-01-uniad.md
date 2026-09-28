# E2E-01 · UniAD（规划导向的开创者）

- **原题**：Planning-oriented Autonomous Driving
- **作者/载体**：Yihan Hu 等（OpenDriveLab）；arXiv [2212.10156](https://arxiv.org/abs/2212.10156) v2（2023-03）；**CVPR 2023 最佳论文**
- **代码**：[OpenDriveLab/UniAD](https://github.com/OpenDriveLab/UniAD)（已下载）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22

## 为什么它是转折点

**首次把"规划"作为整个系统的优化目标**，而不是把它当附属任务。证据：
- 标题即 "Planning-oriented"；
- 摘要明言框架应 "optimized in pursuit of the ultimate goal, i.e., planning"，各任务须 "contribute to planning"；
- Table 2 以**规划 L2 / 碰撞率**为终点逐模块验证贡献，并给出 ID-12（完整）vs ID-0（纯多任务学习）的规划优势（−0.15m avg L2、−0.51 avg Col.%）。

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 场景表征 | **BEV 栅格**（BEVFormer 产出统一 BEV 特征）+ 多任务 query（track/map/motion/occ/plan）作为节点接口 | §2 Overview |
| 规划输出 | **单条轨迹**：ego-vehicle query + command embedding 解码未来 waypoint；仅推理时用 Newton 法 + 占用图做一次后优化 | §2.4 |
| 规划架构 | 3 层 Transformer Planner；与跟踪、在线建图、运动预测、占用预测**五任务联合端到端**（两阶段：先感知 6 epoch，再全栈 20 epoch） | §2.5 |
| 监督 | IL + 占用碰撞约束；L_plan = λ_imi·L2 + λ_col·Σω·L_col，λ_imi=1、λ_col=2.5（**非蒸馏、非 RL**） | 附录 Eq.14–16 |
| 时间跨度 | 运动预测 T=12 帧 @2 Hz（6s）；规划在 1/2/3s 处评估 | 附录 Tab.15 |
| 主结果 | nuScenes 开环 **L2 1.03m / 碰撞 0.31%**（avg）；相对 ST-P3 降 L2 51.2%、碰撞 56.3% | Tab.7、§3.2 |
| 推理成本 | **1.8 FPS**、125.0M 参数、1709G FLOPs | 附录 Tab.13 |
| 自述局限 | 多任务协调算力需求大（尤其含时序）；轻量化部署待探索 | Limitations |

## 代码核验（2026-09-23）

读 `projects/mmdet3d_plugin/uniad/dense_heads/planning_head.py`、`losses/planning_loss.py` 与 `configs/stage2_e2e/base_e2e.py`，确认"单模"是**代码强制**的，且默认配置带一个**测试时优化**组件：

| 项 | 代码证据 |
|---|---|
| 规划头类名 | `PlanningHeadSingleMode`（[planning_head.py:17](../../code/repos/UniAD/projects/mmdet3d_plugin/uniad/dense_heads/planning_head.py#L17)）——**类名即结论** |
| **单模是强制的** | 先构造 P 个候选 query（`sdc_traj_query` + `sdc_track_query` + `navi_embed` 拼接 → `mlp_fuser`），随后 **`plan_query = self.mlp_fuser(plan_query).max(1, keepdim=True)[0]`**——在候选维上做 **max-pool**，P→1。**没有任何多模态输出** |
| 导航命令 | `self.navi_embed = nn.Embedding(3, embed_dims)`（3 个导航命令），**评测时喂 GT 命令** |
| 输出形式 | `self.reg_branch = nn.Sequential(..., nn.Linear(embed_dims, planning_steps * 2))` → `(-1, 6, 2)`，再 `torch.cumsum(..., dim=1)` 得**累积位移**；`bivariate_gaussian_activation` 只作用于 batch 第 0 条 |
| **后处理优化默认开启** | `base_e2e.py:57 use_col_optim = True`；测试时走 `CollisionNonlinearOptimizer(planning_steps, 0.5, sigma, alpha_collision, pos_xy_t)`（**CasADi 非线性规划**，`occ_filter_range=5.0`、`sigma=1.0`、`alpha_collision=5.0`）。→ 论文说的"推理时后优化"在代码里是**默认打开**的 |
| 损失 | `PlanningLoss` = 逐步 L2 后取 masked 均值（**ADE**）；`CollisionLoss` 三档 `delta=0.0/0.5/1.0`（`w=1.85+delta`、`h=4.084+delta`），权重 2.5/1.0/0.25。**`inter_bbox` 只取 min/max → 退化为轴对齐包围盒相交**，`to_corners` 算的旋转被丢弃 |
| 视野 | `planning_steps = 6`（3 s @2 Hz） |

> 对本项目的直接影响：UniAD 是**真单模 + 测试时优化**，把它当"非生成式基线"的代表会**低估基线**。真正该对照的是 VADv2 / Hydra-MDP 那一类"离散词表 + 分类"。详见 [e2e_trunk_code_traces.md](../../code/traces/e2e_trunk_code_traces.md) §G。

## 继承关系

- **基于**：BEVFormer、Panoptic SegFormer、DETR、MOTR。
- **被谁超越/继承**：VAD、SparseDrive 均把它作为 "previous SOTA" 明确超越；本项目的 DIVER 也把它列为对照（DIVER README 引用 UniAD 3 处）。

## 对本项目的意义

- 它确立了"**规划指标作为唯一终点**"的评价范式——这正是后来 NAVSIM/PDMS 的合法性来源，也是本项目在比较时必须固定"同基准同划分"的原因。
- 它的 **1.8 FPS** 说明"全栈联合 + 高维 BEV"的代价；扩散规划器后来能在 45–59 FPS 运行，部分原因正是**放弃了全栈联合**（只做规划模块）。这是一个重要的权衡点：**实时性与"感知-规划联合"之间存在结构性冲突**，而 2026 年的 UniTeD（DP-A07）正是想把两者重新合并。
