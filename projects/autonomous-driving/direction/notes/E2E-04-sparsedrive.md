# E2E-04 · SparseDrive（全稀疏表征 + 多候选规划）

- **原题**：SparseDrive: End-to-End Autonomous Driving via Sparse Scene Representation
- **作者/载体**：Wenchao Sun 等；arXiv [2405.19620](https://arxiv.org/abs/2405.19620) v2（2024-05-31）；preprint（under review）
- **代码**：[swc-17/SparseDrive](https://github.com/swc-17/SparseDrive)（本轮下载）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22

## 为什么它重要

**把 VAD 的"向量化但仍有 BEV"推进到"全稀疏、无稠密 BEV"**（对称稀疏感知统一检测/跟踪/建图），并且**首次把规划显式建模为"多模态分类 + 重打分选择"**。

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 场景表征 | **全稀疏**：实例特征 + 几何锚；对称稀疏感知统一检测/跟踪/建图，无稠密 BEV | §3.2、Fig.1b |
| 规划输出 | **多候选轨迹** τ_p∈R^{Nc×Kp×Tp×2}：**Kp=6 模态 × 3 类命令 = 18 提案**，经分层选择 + 碰撞感知重打分取最高分 | §3.3、附录 B.2 |
| 时间规格 | Tp=6 @2 Hz（3s） | 附录 B.2 |
| 规划架构 | **并行运动规划器**：ego 实例初始化 + 时空交互（agent-agent / agent-map / agent-temporal）+ 分层选择；与运动预测并行联合训练 | §3.3 |
| 辅助任务 | 检测、建图、ego 状态、深度估计 | Eq.3 |
| 监督 | IL（winner-takes-all + ego 状态回归），**无蒸馏/RL** | 附录 B.3 |
| 主结果 | nuScenes 开环 **L2 0.58m / 碰撞 0.06%**（avg），较 VAD 降 L2 19.4%、碰撞 71.4% | Tab.2b、§4.1 |
| 推理成本 | SparseDrive-S **9.0 FPS**、SparseDrive-B 7.3 FPS | Tab.3 |
| 自述局限 | 单任务（如在线建图）仍落后专用方法；数据规模不足、**开环评测不充分** | §5 |
| 继承 | 基于 Sparse4Dv3（ID 分配）、MapTR；被 VADv2 列为 Bench2Drive 基线 | — |

## 代码核验（2026-09-23）

读 `projects/mmdet3d_plugin/models/motion/{motion_planning_head,motion_blocks,decoder,target}.py`、`projects/configs/sparsedrive_small_stage2.py` 与 `tools/kmeans/kmeans_plan.py`，**论文的"18 提案 + 分层选择 + 碰撞重打分"逐条得到代码确认**：

| 项 | 代码证据 |
|---|---|
| **18 提案** | `MotionPlanningRefinementModule.forward`：`plan_reg = self.plan_reg_branch(plan_query).reshape(bs, 1, 3 * self.ego_fut_mode, self.ego_fut_ts, 2)`；配置 `ego_fut_mode = 6`（[sparsedrive_small_stage2.py:62](../../code/repos/SparseDrive/projects/configs/sparsedrive_small_stage2.py#L62)）→ **3 命令 × 6 模态 = 18**；`HierarchicalPlanningDecoder.decode` 同样 reshape 成 `(bs, 3, 6, 6, 2)` |
| 锚点怎么来的 | `tools/kmeans/kmeans_plan.py`：`K=6`，对 **GT 累积轨迹**（`gt_ego_fut_trajs.cumsum(axis=-2)`）**按命令分组**（`navi_trajs = [[], [], []]`）做 KMeans，存成 `(3, 6, 6, 2)` 的 `kmeans_plan_6.npy` |
| 锚点怎么用的 | **只做 query 初始化**：`plan_mode_query = self.plan_anchor_encoder(gen_sineembed_for_position(plan_anchor[..., -1, :]))`；输出仍是 **MLP 回归**（`plan_reg_branch` → `ego_fut_ts * 2`）。→ **不是词表分类**（与 VADv2 相反） |
| 命令是 GT 输入 | `decode` 与 `PlanningTarget.sample` **都用 `data['gt_ego_fut_cmd'].argmax(dim=-1)` 选命令组** → **评测时命令由 GT 给出，不是预测目标** |
| **分层选择的第二层是规则扣分，不是学到的 scorer** | `rescore(...)`：由 `plan_reg` 造 ego box（车身硬编码 `[4.08, 1.73, 1.56] × dim_scale=1.1`）、由**预测的运动 top-1 模态**造 agent box，`col = check_collision(...)`，**`score_offset = col.float() * -999; plan_cls = plan_cls + score_offset`**；只对 `det_confidence ≥ 0.5` 的智能体生效；**6 个模态全碰撞时不做任何惩罚**（`col[all_col] = False`） |
| 碰撞判定（训练侧） | `corners_in_box`——**角点落在对方框内的近似**，不是精确多边形相交 |
| 损失 | cls `FocalLoss(0.5)` + reg `L1Loss(1.0)`（**仅监督 best mode**，`get_best_reg` 取 `argmin` 累积距离 → 赢家通吃）+ ego status `L1Loss(1.0)`。注意：**规划 reg 损失在"位移"上算，而运动 reg 损失做了 `.cumsum(dim=-2)`**（两者不对称） |
| 评测口径 | `planning_eval.py` 用 `shapely Polygon.intersects`（**精确**）+ 车身 `4.084 × 1.85` + "follow uniad" 的 **+0.5 m 纵向偏移**；指标 = L2（0.5–3.0 s 逐步，取 1/2/3 s 平均）+ `obj_col`（GT 也碰撞）+ `obj_box_col`（仅 ego 碰撞）。→ **训练侧 rescore 的代理指标 ≠ 评测指标** |

> 两个结论：(1) 论文的"多模态 + 分层选择"是真的，但**第二层选择是事后规则**，不是 DiffusionDriveV2 那种**学到的 mode selector**；(2) 锚点在 SparseDrive 里是**第四种用法**（query 初始化），既不是"输出答案集"（VADv2）也不是"扩散起点"（DiffusionDrive）。详见 [e2e_trunk_code_traces.md](../../code/traces/e2e_trunk_code_traces.md) §G。

## 对本项目的意义

1. **DIVER 直接基于 SparseDrive 的代码库**（DIVER README 引用 SparseDrive 5 处），说明"扩散规划器"在这一支上是**嫁接在稀疏规划器之上**的，而不是从零重建。
2. 它自己承认"**开环评测不充分**"——这是 E2E 领域的共性自述，与 S032 §VII.C、S001 §3.3 一致。
3. 它的"6 模态 × 3 命令 = 18 提案"与 DiffusionDrive 的锚点数量级不同（DiffusionDrive 用 K-means 得更多锚点），**"候选数量多少合适"在两侧都没有系统研究**。
