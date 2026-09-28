# 自动驾驶项目 · 逐轮工作记录 · 第二十四轮（前半续，§17–§21）

本卷范围：**第二十四轮（前半续，§17–§21）**。内容：nuPlan 闭环口径、Bench2Drive 四项指标、nuScenes 开环口径、研究对象侧代码可用性全表 34/34、ReCogDrive 逐文件核验。
索引见 [../history.md](../history.md)；上一卷见 [rounds-24a.md](rounds-24a.md)；下一卷见 [rounds-24c.md](rounds-24c.md)；当前状态见 [../state.md](../state.md)。

---

---

### 17. nuPlan 闭环分数的代码级核验（补 `benchmarks.md` 的第二个口径空洞）

**动因**：`benchmarks.md` 里只有 NAVSIM（§2）是代码级核验的，**nuPlan 一行只写"各类闭环分数"**——而**研究对象侧的 DP-A01 / DP-A06 / DP-A11 都以 nuPlan 为主基准**。发现 **nuplan-devkit 已随多个仓库 vendored 到本地**（`WAM-Flow/`、`PC-Diffuser/`、`GoalFlow/`），故直接读代码（**零网络成本**），结论写入 [benchmarks.md §2.6](../direction/benchmarks.md)。

**核验到的公式**（`weighted_average_metric_aggregator.py:99-124`）：

```
final_score = multiple_factor × weighted_average_score
  multiple_factor        = Π(4 个乘性项)
  weighted_average_score = Σ(weight_i × metric_i) / Σ(weight_i)   # 只对"非 None 的列"求和
```

**乘性 4 项**（`closed_loop_{reactive,nonreactive}_agents_weighted_average.yaml` 的 `multiple_metrics`）：`no_ego_at_fault_collisions`（**0 / 0.5 / 1**，按 VRU/vehicle/object 分档）、`drivable_area_compliance`（0/1）、`ego_is_making_progress`（0/1）、`driving_direction_compliance`（**0 / 0.5 / 1**）。
**加权 4 项 + 默认**：`ego_progress_along_expert_route` **5.0**、`time_to_collision_within_bound` **5.0**、`speed_limit_compliance` **4.0**、`ego_is_comfortable` **2.0**、其余 **default 1.0**。
**跨场景聚合**：场景类型分数 = `Σ(场景分) / 该类型场景数`；最终分数 = `Σ(类型分 × 该类型场景数) / 总场景数` → **按场景数加权，不是按场景类型等权**。

**三条口径事实**：

1. **nuPlan 不是"纯乘法链"**（PDMS 才是）：乘性项只有 4 个，**不含 progress / TTC / comfort**（这三项是加权项）→ 结构上比 PDMS "温和"。
2. **加权平均的分母 = `Σ(参与列权重)`，参与列由配置的 metric 列表决定** → **换一套 metric 列表，分母就变、分数就变**。→ 与 NAVSIM 的"EP 是批内相对分"是**同类的口径脆弱性**（分数不是绝对量，而是相对于"你配了哪些 metric"）。
3. **nuPlan 的进度项是"跟专家比"**（`ratio of ego to expert progress`，`score_progress_threshold: 2 [m]`），**而 PDMS 的 EP 是批内相对分** → 两者"进度"这一维的含义根本不同。
4. **reactive 与 nonreactive 两套配置的 metric 列表与权重完全相同** → 差别只在仿真环境，**不在打分口径**（与 NAVSIM 的 v1/v2 不同，后者口径本身也变）。

**判断**：`benchmarks.md` 现在有**两块代码级口径**（NAVSIM §2、nuPlan §2.6），且两者的"不可比机制"被并排写清。**下一个口径空洞是 Bench2Drive**——`DS = RC × IS` 仍是 README 级，IS/SR/Effi/Comf 的定义未核验，且其仓库未克隆（WoTE 与 DriveLaW 都报了 Bench2Drive 数字：WoTE 以 TCP 为基线、DS **+1.81**）。

**产出（续）**：[benchmarks.md](../direction/benchmarks.md) 新增 **§2.6（公式 + 与 PDMS 的结构差异表 + 三条口径事实 + 与 Bench2Drive 的对照）**，文件头证据等级与 §1 的 B003 行同步；[state.md](../state.md) 的"指标口径"一条补入**第三块口径**；[sources.md](../sources.md) B003 / [index.md](../index.md) / [README.md](../../../README.md) 同步。

**产出**：[world-model/papers.md](../topics/world-model/papers.md) 新增 **WM-21–WM-24 四行 + §4.1（4 篇全文事实）+ §5 代码可用性全表 + §5.1 DriveLaW**，§2 证据边界、§3（补录结果收进表内）、§6 边界外清单、文件头更新；[world-model/lineage.md](../topics/world-model/lineage.md) 新增**五条接口路线表 + 第 6 条（动作专家内嵌）**并改写"并行支线""转移 2""接口差异第 1 问""证据边界"；[C004](../code/traces/world_model_code_traces.md) 新增 **§E（WoTE 核验：主张对照 9 项 + 组合关系 4 项 + 实现细节 4 项）**、**§G（DriveLaW 核验：两条接口 + 死引用 + 规划器实测字段）**、§H 判断扩为五条；[repositories.md §D/§D.1](../code/repositories.md) 扩为**在列 12 个**（新增 WoTE / DriveDreamer / Drive-OccWorld / LAW / World4Drive / TrafficBots / DriveLaW / DrivingGen），"无代码/代码不全"清单 **9 → 12 条**；[transfer.md §3](../topics/diffusion-planner/transfer.md) 新增"世界模型给候选轨迹打分"一行与第 5 条接口路线；[state.md](../state.md) / [sources.md](../sources.md) / [index.md](../index.md) / [README.md](../../../README.md) / [world-model/README.md](../topics/world-model/README.md) / [inbox/cleanup.md](../../../inbox/cleanup.md) 同步。**本轮未新增本地仓库**（全部走 `raw.githubusercontent.com` + GitHub trees API 取证），本地快照仍 **37 个 / 1.65 GB**。


### 18. Bench2Drive 四项指标的代码级核验（补 `benchmarks.md` 的第三个口径空洞）

**动因**：上一节（§17）关闭 nuPlan 口径后，**唯一剩下的口径空洞就是 Bench2Drive**——`DS = RC × IS` 仍是 README 级，而 WoTE 与 DriveLaW 都报了 Bench2Drive 数字（WoTE 以 TCP 为基线、DS **+1.81**）。

**关键发现（省掉了克隆）**：**官方评测栈已被 DIVER 逐字节 vendored 到本地**（`code/repos/diver/`——DIVER 本身就跑 Bench2Drive 闭环）。用 `raw.githubusercontent.com` 取官方 `0.0.4` 分支逐字节比对，**6 个文件全部 IDENTICAL**（`statistics_manager.py`、`merge_route_json.py`、`ability_benchmark.py`、`efficiency_smoothness_benchmark.py`、`atomic_criteria.py`、`route_scenario.py`），唯一差异是 DIVER 在 `autonomous_agent.py:118` 多一行注释掉的 `pdb`。→ **零克隆成本完成代码级核验**。

**核到的四项指标**：

1. **DS = `max(RC × IS, 0)`**（`statistics_manager.py:413`）→ **220 条 route 的算术平均**（`merge_route_json.py:38`，**按 route 等权，不按里程加权**）。IS 是**乘性折扣、起手 1.0**：撞行人 **0.5** / 撞车 **0.6** / 静态物 **0.65** / 闯红灯 **0.7** / 场景超时 **0.7** / 未让行紧急车 **0.7** / 停车标志 **0.8**；**同类重复发生会连乘**（两次撞车 → 0.36）。唯一按比例扣分的是 `OUTSIDE_ROUTE_LANES_INFRACTION`（`[0,'increases']`）。**`MIN_SPEED_INFRACTION` 被标 `'unused'`**（`:37` + `:359-360` 的 `pass`）→ 2024-08-19 起低速不再影响 DS。`ROUTE_DEVIATION` / `VEHICLE_BLOCKED` **不扣分**，只把 route 标 Failed。
2. **SR**（`merge_route_json.py:20-28`）= "`status ∈ {Completed, Perfect}` **且除 `min_speed_infractions` 外零违规**" 的 route 数 / 220 → **比"跑完"严格得多**。
3. **5 项 Ability**（`ability_benchmark.py:12-18`）：Overtaking / Merging / Emergency_Brake / Give_Way / Traffic_Signs，`mean = sum/5`（硬编码）。**Traffic_Signs 被双重计数**（`:116-147`：通用判据 +1 后，再按**路口进度**判据 +1）→ 分母是"该类场景数的 2 倍"，且该支需要 **CARLA + `GlobalRoutePlanner`**。
4. **Driving Efficiency 与名字不符**：代码里是 **`actor_speed / (RATIO × mean_background_speed) × 100`**（`atomic_criteria.py:2054`，**`RATIO = 1`**，`:1968`），且**从事件消息文本里正则抠出**（`efficiency_smoothness_benchmark.py:268`）。检查点 **4 个/route**（`route_scenario.py:308`），**只对有 `min_speed_infractions` 的 route 求平均**、**丢弃 > 1000% 的检查点**。→ **官方表里 Simlingo 的 "251.72" 是"开得比周围车流快 1.5 倍"，不是完成率**；**高 Effi 与高 DS 不同向**（UniAD 120.16 / VAD 163.74 而 DS 仅 38.69 / 38.65）。
5. **Driving Smoothness = 20 步分段的合规时间占比**：先 Savitzky–Golay（win 7 / poly 2 / deriv 1 / dt 0.1），再要求 **6 项同时严格在界内**（`lon_acc (−4.05,2.40)`、`lat_acc ±4.89`、`magnitude_jerk ±8.37`、`lon_jerk ±4.13`、`yaw_acc ±1.93`、`yaw_rate ±0.95`）；route 按 20 步切块、逐块判 0/1、取平均。**6 个界的来源仓库里没有说明**。

**两处代码级问题（第六类陷阱的第 9、10 例）**：
- **`yaw_acc` 与 `yaw_rate` 在代码里是同一个数组**——`:91-103` 两处都是 `savgol_filter(_z_yaw_rate, polyorder=2, window_length=7)`，**`yaw_acc` 那处漏了 `deriv=1`**（`lon_jerk` / `magnitude_jerk` 都带了）→ 因 ±0.95 严格紧于 ±1.93，**`yaw_acc` 项恒不生效**，6 项实际只有 5 项在起作用。
- **`_approximate_derivatives`（`:168-194`）全文件从未被调用**（死代码）。

**三个口径陷阱**：① **分母硬编码 220**（`merge_route_json.py:38-39` + `ability_benchmark.py:170` 的 assert；官方 README 原文 "If there is not enough, the missed ones will be treated as 0 score"）→ **部分评测静默给偏低分**；② **Effi/Comf 的输入是 agent 自己 dump 的 `metric_info.json`**（`autonomous_agent.py:146-161` 提供，`team_code/sparsedrive_b2d_agent.py:524-525,577-578` 写盘）→ **不 dump 就拿不到这两项**；③ **0.0.4（2024-08-19）移除低速惩罚 + TickRunTime 2000→4000**，2024-10-14 又修了 Ability 的 typo → **前后数字不可混用**。

**产出**：[benchmarks.md](../direction/benchmarks.md) 新增 **§2.7（5 个小节：DS/SR、Ability、Efficiency、Smoothness、三个陷阱 + 三基准对照表）**，文件头证据等级、§1 的 B002 行、§2.6.3 的对照表同步；[sources.md](../sources.md) B002 行补代码级结论；[state.md](../state.md) 的"指标口径"一条补入**第四块口径**并撤掉"Bench2Drive 是下一个口径空洞"；[index.md](../index.md) / [README.md](../../../README.md) / [repositories.md](../code/repositories.md) 同步。**本轮未新增本地仓库**（全部走 `raw.githubusercontent.com` + 1 次 GitHub trees API）。

### 19. nuScenes 开环规划口径的代码级核验（补 `benchmarks.md` 的第四个口径空洞）

**动因**：§1 的 B004 行只有"L2、碰撞率"四个字，而**研究对象侧的四个"非生成式基线"（UniAD / VAD / VADv2 / SparseDrive）与 GenAD 的主表数字全是 nuScenes 开环 L2 / 碰撞**。四个仓库**都在本地**（`UniAD` / `VAD` / `SparseDrive` / `GenAD`）→ **零网络成本**。

**一句话结论**：**"nuScenes 开环规划指标"这个名字下至少有四套不同实现，且其中两套是同一份代码里的可切换分支。**

**四套实现的差异（同名不同义）**：

| 维度 | UniAD | VAD | VADv2 | SparseDrive |
|---|---|---|---|---|
| 文件 | `planning_head_plugin/planning_metrics.py` | `VAD/planner/metric_stp3.py`（**文件名叫 `metric_stp3`**，docstring "calculate planner metric same as stp3"） | `VADv2_head.py:2710`（内联类） | `datasets/evaluation/planning/planning_eval.py:55`（内联类） |
| 碰撞判定 | 栅格占据（GT 框 `cv2.fillPoly` → 200×200 BEV） | 同 | 同 | **`shapely.Polygon.intersects` 精确多边形相交**（对 GT 未来框 `fut_boxes`） |
| 障碍物集合 | 外部传入 `segmentation` | `human=[2..8]` / `vehicle=[14..23]`，**碰撞时合并** | `human=[0,1,2,3]` / `vehicle=[0,1,2,3]`（**两个集合相同**） | GT 未来框，无类别过滤 |
| L2 归约 | **逐时刻向量**（6 维） | **标量前缀平均 ADE**（`compute_L2` 直接 `return ade`） | 无 `update`/`compute`，聚合内联 | 逐时刻向量，**打印时前缀累积平均**（`:162`） |
| GT 碰撞时刻 | **剔除** | **剔除** | **不剔除**（`m2 = torch.ones_like(gt_box_coll)`，上一行原本的 `m2 = ~gt_box_coll` **被注释掉**） | **剔除** |
| 无效样本 | mask 乘进 L2 | — | — | **整样本丢弃**（`:144`） |
| 批大小 | 支持 B | `assert shape[0]==1` | — | **`assert B == 1`**（`:96`） |

**最硬的一条证据**：**UniAD 自己的评测代码里显式提供两套 L2 定义**（`nuscenes_e2e_dataset.py:1033-1047`）：

```python
planning_tab.title = f"{planning_evaluation_strategy}'s definition planning metrics"
if planning_evaluation_strategy == "stp3":
    row_value.append("%.4f" % float(value[: i + 1].mean()))   # 前缀累积平均
elif planning_evaluation_strategy == "uniad":
    row_value.append("%.4f" % float(value[i]))                 # 单步值
else:
    raise ValueError("planning_evaluation_strategy should be uniad or spt3")
```

配置在 `projects/configs/stage2_e2e/base_e2e.py:61`（默认 `"uniad"`）。→ **同一个表头 "L2 1s/2s/3s"，`stp3` 口径下是"0→1s / 0→2s / 0→3s 的累积平均"，`uniad` 口径下是"第 1s / 2s / 3s 那一刻的单步值"**；**SparseDrive 的打印与 VAD 的 `compute_L2` 都走 `stp3` 那一支**。

**四处需要收窄或标注的记录**：① **SparseDrive 的 `obj_col` 累加的是 GT 自己的碰撞**（`:102` `obj_coll_sum += gt_box_coll.long()`），而 UniAD 里 `obj_col`/`obj_box_col` 都是自车的 → **报其 "Collision" 必须说明取自哪一列**（需与论文表格对照确认是否复制粘贴遗留）；② **VAD 的 `metric_stp3.py` 里 `update`/`compute` 整段被注释掉**（`:310-336`），聚合写在 `VAD.py:616-637`，按 1s/2s/3s 三个前缀各算一次；③ **VAD/VADv2 会把行人栅格并进占据栅格**（`occupancy = OR(segmentation, pedestrian)`）→ 其"碰撞"含行人；④ **两处坐标映射不一致（需运行确认）**：VAD 用 `r = bev_dimension[0] − traj` 放自车**框**、用 `xi = (−bx[0]/2 − yy)/dx[0]` 放自车**中心点**，两者不是同一映射（UniAD 两处一致），且 VAD/VADv2 里 `trajs * [−1, 1]` 两行**被注释掉**。

**判断**：这是**第四类"口径脆弱性"**——§2.4 是"EP 是批内相对分"、§2.6 是"分母随配置变"、§2.7 是"分母硬编码 220"，**这次的问题是"同名列的定义本身不同"**。→ 给"不用 nuScenes 开环"提供了代码级依据（Bench2Drive 官方 README 与 CARLA_GARAGE 的公开呼吁，**不只是"指标无意义"，还包括"同名指标各家不同义"**）。**跨仓库横比 UniAD / VAD / SparseDrive 的 L2/碰撞，本项目不予采信。**

**产出**：[benchmarks.md](../direction/benchmarks.md) 新增 **§2.8（四套实现对照表 + 两套 L2 定义的代码证据 + 四处收窄 + 与本项目的关系）**，文件头证据等级与 §1 的 B004 行同步；[state.md](../state.md) 的"指标口径"一条补入**第五块口径**；[sources.md](../sources.md) B004 / [index.md](../index.md) / [README.md](../../../README.md) 同步。**本轮未新增本地仓库、未新增临时目录**。

### 20. 研究对象侧"代码可用性"全表核验：34 篇 DP-A 全部核完，并新发现 6 个官方仓库

**动因**：论文表的"代码"列在 34 篇 DP-A 里仍有 21 篇是空白、"未核验"、"未见官方"或"见前序会话记录"——**这是研究对象侧最后一块没结账的表列**（此前只对**已克隆的 13 个仓库**做过逐文件核验，未克隆的 21 篇从未查过代码可用性）。

**方法**：按用户授权，**把 21 篇拆成 3 组交给 3 个并行子代理**做信息搜集（子代理只查、不写），主线程复核关键条目。硬约束：**不克隆任何仓库**；**每个子代理最多 5 次 GitHub API 调用**（未认证限额 60/小时且三者共用出口 IP），其余走 arXiv 摘要页 / HTML 全文外链检索 / `raw.githubusercontent.com`。

**结果（34/34 核完）**：**18 篇有代码 / 1 篇占位仓库（零代码）/ 1 篇只有项目页 / 14 篇未找到官方代码**。

**三条新发现（都是"此前记错了"）**：

1. **DP-A12 GuideFlow 其实有代码，但 arXiv 给的是占位仓库**——arXiv 摘要原文 "The code will be in https://github.com/liulin815/GuideFlow"，该仓 README 原文 "**We are currently organizing the code, coming soon**"；但其 News（2026-02-21）指向 **[adept-thu/GuideFlow](https://github.com/adept-thu/GuideFlow)**，后者 News 原文 "**We released our code in navsim!**"（约 586 个 `.py`，含 `navsim_test/agents/flowdrive/modules/flow_matching.py`）。→ **"指向链陷阱"：只按论文链接打开会误判为"未发布"**。GuideFlow 的 navhard EPDMS 43.0 是本项目同基准的 SOTA，这条直接影响可复现性判断。
2. **DP-A28 ReCogDrive 的代码已公开**——**[xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive)**，arXiv v2 摘要原文 "Code and models are available at …"；README News 2025-06-11 "Code/Models are coming soon" → **2025-08-21 已释放** "the initial version of code and weight on NAVSIM, along with documentation and training/evaluation scripts"（**但 README TODO 里 "Release Bench2Drive, DriveLM, NAVSIM2.0, Drivebench evaluation frameworks" 仍未勾选**）。→ **它是 WM-11 DriveLaW 的 `ReCogDriveDiffusionPlanner` 的上游**，且其 README 里报过 **w/GRPO PDMS 90.5** → **可进"RL 词义核验"清单成为第六种**（当前五种：DIVER < HDP(RWR) < AutoVLA < FeaXDrive(GRPO) < MindDrive(完整 PPO)）。
3. **"有仓库"≠"有代码"这一层必须分开记**：DP-A29 DriveFine 是**占位仓库**（只有 README + 一张图）、**DP-A15 的 repo 里只有 GitHub Pages 站点源码 `docs/index.html`**（无 `.py`、无 README）、**DP-A17 DIPOLE 主仓 README 写 "Quick Start Comming soon."，真代码在其 git submodule `Whiterrrrr/dipole-rl`**。

**其余新确认有代码的 3 篇**：**[shuliu-ethz/BridgeDrive](https://github.com/shuliu-ethz/BridgeDrive)**（DP-A08，README News 2026-03-09 "We release the initial version of code, along with documentation and training/evaluation scripts"）、**[codingmlinprocess/LCS](https://github.com/codingmlinprocess/LCS)**（DP-A26，IROS 2026，约 495 个 `.py`，含 Bench2Drive leaderboard 与 SimLingo 训练/评测脚本 + HuggingFace checkpoint）、**[haldunbalim/MPDiffuser](https://github.com/haldunbalim/MPDiffuser)**（DP-A23，含 `mpdiffuser/` 包与 `scripts/train.py`）。

**14 篇"未找到官方代码"**（已逐篇写明证据来源与是否有发布承诺）：DP-A04 AnchDrive、A05 DriveAnchor（美团）、A07 UniTeD（Nullmax + 西湖）、A19 RoG-DAgger、A20 SafeFlowMatcher（**只有匿名补充材料**）、A22 G2SD、A24 SDGD、A25 DAPSE、A27 DiffVLA、A30 KnowDiffuser、A31 DriveFuture、A32 DiffuSearch、A33 DiMA、A34 Designing Versatile Samples。**其中 DP-A31 DriveFuture 值得单列**：它是**唯一与研究对象直接同构的世界模型侧工作（WM-09）**，附录原文 "The details are reconstructed from the training and evaluation scripts, the Hydra configuration, and the model code." 指的是**作者内部未公开**的代码，全文只有 HuggingFace 排行榜链接，**无 "will be released" 承诺**。

**产出**：[papers/diffusion_planner_ad.md](../topics/diffusion-planner/papers/diffusion_planner_ad.md) 的 **"代码"列 21 行全部补齐**，文件头新增"代码列全表核验完毕（34/34）"一段（含三级口径与三条陷阱）；[state.md](../state.md) 待续清单新增**第 13 项**（6 个新仓库未克隆未核验，并标注优先级）；[README.md](../../../README.md) 同步。**本轮未克隆任何仓库、未新增本地快照**（本地仍是 37 个 / 1.65 GB）。

### 21. ReCogDrive（DP-A28）的代码级核验——"DiffGRPO"是第六种"RL"

**动因**：上一节（§20）的全表核验发现 **DP-A28 此前记为"未见官方"是错的**——[xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive) 代码与权重都已公开。它有两个不可替代的位置：① 是 **WM-11 DriveLaW 的 `ReCogDriveDiffusionPlanner` 的上游**；② 它的 RL 阶段自称 **Diffusion Group Relative Policy Optimization（DiffGRPO）**，而本项目已维护一份"RL 词义核验"清单（五种）。→ 补做代码级核验（**未克隆**，走 `raw` 逐文件取证；全仓 359 个 blob）。

**逐项核对（实现全在 `navsim/agents/recogdrive/recogdrive_diffusion_planner.py`，全仓无任何文件名含 `grpo`/`ppo`）**：

| 要素 | 有无 | 证据 |
|---|---|---|
| 对数概率 | ✅ **真** | `:754 get_logprobs`；`:813-815` `std = exp(0.5·logvar).clamp(min=min_logprob_denoising_std)` → `Normal(mean, std)` → `dist.log_prob(x_t_minus_1)`；`mean/logvar` 来自**带梯度的** `p_mean_variance`（`:805`），采样链 `.detach()` |
| 组内归一化优势 | ✅ | `:852-854` `advantages = ((rewards_matrix − mean_r) / std_r).view(-1).detach()` |
| 去噪步折扣 | ✅ | `:862` `discount = gamma_denoising ** (num_denoising_steps − denoising_indices − 1)`，`gamma_denoising = 0.6` |
| 策略梯度项 | ✅ | `:872` `policy_loss = -torch.mean(log_probs * adv_weighted_flat)` |
| **重要性比率 `ratio`** | ❌ **全仓无** | grep `ratio` 只命中 `:233` 的 DDIM `step_ratio` |
| **比率裁剪** | ❌ | `eps_clip_value`（`:80`/`:266`）**是采样时对 `pred_noise` 的裁剪**（`:426-428`），**不是 PPO 裁剪** |
| **KL** | ❌ | `:26` `from torch.distributions import ... kl_divergence` —— **import 了却全文件零次调用** |
| **critic / GAE** | ❌ | grep 零命中 |
| BC 正则 | ✅ | `:876-886` `teacher_chains = self.old_policy.sample_chain(...)` → `bc_loss = -bc_logp.mean()` → `total_loss = policy_loss + bc_coeff·bc_loss`，`bc_coeff = 0.1`。**`old_policy` 只当 BC 教师**（`:296-298`），不参与比率或 KL |
| 奖励 | ✅ **真 PDM 分数** | `:904 reward_fn` → `:916-923` `pdm_score(..., scorer=self.train_scorer)` → `asdict(pdm_result)["score"]` → `.detach()`；权重 `progress 10.0 / ttc 5.0 / comfortable 2.0` |
| 优势裁剪 | 有开关但**默认空操作** | `:84-85` `clip_advantage_lower_quantile = 0.0` / `upper = 1.0`（全分位 = 不裁） |

**开关链**：`recogdrive_agent.yaml:21` **`grpo: False`**（`GRPOConfig` 与工厂默认也都 False）；`recogdrive_agent.py:200-205` 是三路分支；**4 个 RL 脚本显式覆盖 `agent.grpo=True`** 并配 `metric_cache_path` / `reference_policy_checkpoint`。→ **与 ORION 的"机制在代码里但被配置全量关闭"不同，这里 RL 脚本确实打开了它。**

**三条判断**：① **"DiffGRPO" = REINFORCE + 组内相对优势 + BC 正则**，不是 PPO/GRPO 完整形态 → **"RL 词义核验"清单扩到六种**：DIVER < HDP(RWR) < AutoVLA < **ReCogDrive** < FeaXDrive(GRPO) < MindDrive(完整 PPO)；**只有 MindDrive 有 critic 与 GAE，只有 FeaXDrive 与 MindDrive 有比率裁剪**。② **奖励是真的**（逐条跑 NAVSIM `PDMScorer`），与 AutoVLA 同级，远强于 DIVER 的 `0.2·map(dummy=1.0)`。③ **RL 收益可量化且两个规模一致**：Base 2B **84.1 →(IL) 86.5 →(RL) 90.8**（**+4.3**）、Large 8B **86.4 → 86.5 → 90.4**（**+3.9**）→ **这是本项目方向 A/B 的正向证据**；**但口径冲突**：ReCogDrive 自报 **90.8**，FeaXDrive 对比表记 **90.5**（本项目此前采用 90.5）→ **"同一方法跨论文数字不一致"的又一实例**。

**产出**：[C003 §M](../code/traces/diffusion_planner_code_traces-2.md) 新增一节（逐项核对表 + 开关链 + 三条判断），文件头同步；[papers/diffusion_planner_ad.md](../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A28 行补代码级结论与 README 数字；[state.md](../state.md) 的"RL 词义核验"清单扩到六种、待续第 13 项状态更新；[preparation.md §2](../ideas/preparation.md) 新增"RL 阶段净收益 ~4 PDMS"这条事实；[repositories.md §F](../code/repositories.md) / [README.md](../../../README.md) 同步。**本轮未克隆任何仓库**（ReCogDrive 走 `raw` 取证）。
