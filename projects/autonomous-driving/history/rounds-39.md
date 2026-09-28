# 第三十九轮（2026-09-24）· 我们手上这份 devkit 是哪一套口径（顺带发现 EC 根本不进分）

**动因**：第三十八轮确立了"EPDMS 有修复前 / 修复后两套官方实现"，但**没回答我们自己的实验该用哪套**——而这直接决定路线 ②③ 的第一步（用 SimScale 的 ckpt 跑评测）跑出来的分数**能不能与官方榜比**。本地 `code/repos/navsim/` 就在盘上，可以离线核。

## 做法

在本地 devkit 上做**代码级核验**（不联网）：版本/commit/是否 shallow → 找 `human_penalty_filter` 的实现与门控 → 核配置默认值与注释 → 读 README 的 changelog 拿口径时间线 → 顺带核 `weighted_metrics` 的构造与重建。

## 结论（含更正）

### 1. 版本与身份（实测）

| 项 | 值 |
|---|---|
| 版本 | `setup.py` 写 **`version="2.0.0"`** |
| commit | **`0a380a9`**（`Revise highlights and changelog in README.md`），**2025-10-27** |
| 克隆方式 | **shallow**（`git rev-parse --is-shallow-repository` = `true`）→ **本地拿不到 git 历史**，时间线只能靠 README changelog |

### 2. **README changelog 给出了本项目此前缺的口径时间线**

| 日期 | 事件 |
|---|---|
| 2025/02/28 | **v2.0** — **EPDMS 首次引入** |
| **2025/04/24** | **v2.1.2** — 发布 `navhard_two_stage`；**"Updated Extended Predictive Driver Model Score (EPDMS)"** ⚠ 第一次口径变更 |
| **2025/04/28** | **v2.2** — **AGC 2025 官方 devkit**；**提交截止 2025-05-11** |
| **2025/09/29** | **Bugfix** — "Fixed a bug in **metric filtering** where `multiplicative_metrics_prod` and `weighted_metrics` were not correctly excluded by the **human filter**"（[Issue #151](https://github.com/autonomousvision/navsim/issues/151#issue-3379282167)）⚠ **这就是 DriveFuture 说的 "human-behavior filtering fix" 的最可能对应** |
| **2025/10/27** | 本仓 HEAD |

→ **可操作的推断**（**标为推断**，DriveFuture 未给日期）：**`EPDMS*` ↔ 2025-09-29 之前 / `EPDMS` ↔ 之后**。按这个界线：
- **SimScale 的 48.0**（AGC 2025，截止 2025-05-11）→ **旧** ✓ 与第三十八轮结论一致；
- **DriveFuture 的 53.2 / 55.5**（2026-05）→ **新** ✓；
- **GTRS-E 的 49.4**（2025-06 论文）→ 按日期应是**旧**，**但它与 DriveFuture 表逐字一致** → **说明 DriveFuture 是照抄 GTRS 论文的数字，而不是重测** → **反向印证了 §7.7.1 的"混装集"判断**。

### 3. 本地这份是**修复后**的版本（三条实测）

1. **filter 存在且默认开**：`pdm_scorer.yaml:27 human_penalty_filter: True`（注释原文 "ensuring that the ego is not penalized when the human agent makes mistakes"）。
2. **含 2025-09-29 的 bugfix**：`skip_columns = {"multiplicative_metrics_prod", "weighted_metrics", "weighted_metrics_array", "pdm_score"}` ✓ + 其后的重建块（重算 `multiplicative_metrics_prod` 与 `weighted_metrics`）✓。
3. **⚠ 但 filter 只对 Stage-1 生效**：门控是 `... and metric_cache.scene_type == SceneFrameType.ORIGINAL` → **Stage-2（合成场景）不做人类过滤**。→ DriveFuture 说的 "the human-filtered subscores f_m(·) are used **consistently**" 与代码**不完全一致**，**这一层两家论文都没提**。

### 4. **⚠⚠ 意外发现：EC 根本不进 EPDMS——配置里的权重 2.0 是死权重**

`pdm_scorer.py` 原文注释与代码：

```python
# Exclude the two-frame extended comfort metric from the weighted metrics calculation.
mask = np.ones_like(self._config.weighted_metrics_array, dtype=bool)
mask[WeightedMetricIndex.TWO_FRAME_EXTENDED_COMFORT] = False
```

→ **EC 被显式排除在加权和之外**，尽管配置写了 `two_frame_extended_comfort_weight: 2.0`。→ **实际参与加权和的只有 4 项 `{EP, TTC, LK, HC}`**（`WeightedMetricIndex` 有 5 项，第 5 项被 mask）。

**三条连带更正**：

1. **`benchmarks.md §2.3` 第 3 条与公式行原来都写"EC 权重 2、在加权和里" → 已改**（公式改为 `m ∈ {EP, TTC, LK, HC}`）。
2. **与 DriveFuture 论文冲突**：论文写 `M_avg = {EP, TTC, LK, HC, EC}`、`β_EC = 2`；**本地代码把它 mask 掉** → **又一处"论文 vs 代码"**（以本地代码为准，注明可能是版本差异）。
3. **⚠ "涨分牺牲舒适性"这个说法要改写**：第三十七轮把"SimScale 让 DiffusionDrive 的 EC 从 79.6/72.8 掉到 59.6/31.9 而总分仍涨"记成 **P2c 的权衡实例**；**现在看，EC 掉一半对总分毫无影响** → **那不是权衡，而是"EPDMS 没测 EC 这一项"**（HC 才进分）。→ **P2c 的正确表述是"分数与它未覆盖的维度不一致"**，不是"分数与可行性成反比"。**DriveFuture 用"乘性安全项主导"解释同一现象，代码给出了更硬的解释。**

### 5. 两处"注释 / 论文 与代码不一致"（本项目的老类别，这里又添两例）

1. **配置注释与代码不一致**：`pdm_scorer.yaml` 注释写 "**now only for driving_direction_compliance**"，但 `pdm_score.py` 的循环是**遍历所有列**（只跳过那 4 个聚合列）→ **注释严重低估了实际作用范围**。
2. **论文与代码不一致**：DriveFuture 的 `M_avg` 含 EC、`β_EC = 2`；代码 mask 掉 EC。

### 6. 对本项目的直接结论（可执行）

1. **实验协议里必须固定 devkit 版本**：写明 **commit `0a380a9`（2025-10-27）**，它**含 2025-09-29 的 human-filter bugfix** → **用它跑出的分数是 `EPDMS`（新实现），与官方榜可比**。**这是路线 ②③ 的第一步必须先钉死的一件事。**
2. **报告 EC 时必须说明它不进分**（只作诊断列）；**论文里不要说"我们牺牲了舒适性"**。
3. **changelog 时间线是"按日期给已有数字分类"的唯一依据**（多数论文不声明口径）。

## 产出

| 类别 | 文件与章节 |
|---|---|
| 基准口径 | [benchmarks.md](../direction/benchmarks.md) **新增 §2.10（§2.10.1–§2.10.5）**；**更正 §2.3 第 3 条与公式行**（EC 不进分）；§2.3 第 4 条补"本地已含此修复" |
| 判断边界 | [judgments.md §B](../judgments.md) 新增 1 条（B 组 9 → **10**，总数 62 → **63**） |
| 冲 SOTA 文件 | [sota-plan.md](../ideas/sota-plan.md) **§7.7.4 的口径更正**（EC 不进分 → 改写"必须一起报的代价"）+ §5.4 路线③同处 + 文件头 |
| 设计前提 / 问题 | [preparation.md](../ideas/preparation.md) **P2c 第三十九轮更正**（"分数与它未覆盖的维度不一致"） |
| 状态 / 索引 | [state.md](../state.md)（当前阶段、索引表 B 行、条数 63）、[history.md](../history.md)（20→**21** 卷）、[index.md](../index.md)、[README.md](../../../README.md) |
| 中间产物 | 本轮**未产生**新中间产物（纯本地代码核验） |

**验证**：`check_links.py` **七项全绿**，退出码 0。

**一句话**：**上一轮从论文知道了"EPDMS 有两套实现"；这一轮从代码知道了"我们手上就是修复后的那套、修复的确切日期是 2025-09-29"——并且顺手发现 EC 从来就不进分，所以第三十七轮那条"涨分牺牲舒适性"的观察要改成"分数没测 EC"。**
