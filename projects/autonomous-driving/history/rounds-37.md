# 第三十七轮（2026-09-24）· 三份 navhard 表的交叉核对：GTRS-E 的定义找到了，SimScale 的 53.2 查不到

**动因**：第三十六轮的教训是"§1 的**代码实际状态**一列当年只核了**仓库存在 + 星数**，对 DiffVLA 是**承重地错了**"。§6 里恰好还挂着两条同类的"**承重但未核**"事项：

- **「SimScale 的 +8.6 对更强基线是否成立」**——标注为"**这是路线 ③ 的前置**"；
- **「GTRS-E 的确切定义」**——标注为"**未在任何论文中定义**"，而 **49.4 是第 ② 层涨分门槛**。

两条都直接决定用户要选的那条路线值不值得走，所以本轮把它们核到**论文原文**（不只是仓库）。

## 做法

把 **SimScale（arXiv 2511.23369）与 GTRS（arXiv 2506.06664）两篇 PDF** 下载到 `/tmp/ai4r/`（11.7 MB / 1.7 MB）并 `pdftotext -layout` 逐表核；两个仓库用 **GitHub API + `raw`** 取元数据、根目录、README 与 Model Zoo（**均未克隆**）。

## 结论（含更正）

### 1. 副产品比预期大：现在有**三份互相独立的 navhard 表**，而它们对不上

| 方法 | DriveFuture Table 1 | **SimScale Table 1** | **GTRS Table 2** | 判定 |
|---|---|---|---|---|
| **PDM-Closed**（GT 感知特权） | — | **51.3** | **51.3** | ✅ **两篇逐字一致** |
| LTF（≈ 表中 TransFuser） | 23.1 | 24.4（w/o） | **23.1** | ⚠ 差 1.3 |
| **DiffusionDrive** | **24.2** | **27.5**（w/o） | — | **⚠ 差 3.3** |
| GTRS-Dense | — | 38.3（R34）/ 41.9（V2-99） | **41.7**（V2-99）/ 43.4 / **45.3**（ViT-L，最佳单模） | V2-99 一致 |
| GTRS-E-Lite / **GTRS-E** | — / **49.4** | — | **46.6** / **49.4** | ✅ **两篇一致** |
| **SimScale** | **53.2** | **48.0**（其自报 SOTA） | — | **⚠⚠ 差 5.2** |

→ **"同一基准跨论文仍不可横比"的第二个根因**：此前只知道 **PDMS/EPDMS 的口径差异**（EP 是批内相对分、第二阶段高斯权重以本方法终点为中心）；现在有了**同基准、同方法、同指标**却仍差 3.3 / 5.2 的直接实例 → 根因是"**基线配置 / 评测脚本 / 提交版本**"不同。**已写入 [judgments.md §B](../judgments.md) 新增一条，并给 [preparation.md](../ideas/preparation.md) 的 **P8 清单补 ⑤⑥ 两例**（四个 → **六个**）**。

### 2. **「GTRS-E 未在任何论文中定义」是错的**

GTRS 论文 **Table 2（= navhard 表）题注**原文：**"The challenge-winning entry **GTRS-E ensembles all six models from GTRS-Dense and GTRS-Aug**"**；正文："**an ensemble of all six variants, reaches 49.4 EPDMS, approaching the performance of PDM-Closed**"。→ **49.4 确实是 navhard 数字，且不是"推测"**。

**但接着发现一个更要紧的事实**：49.4 是**六模型集成**，而 `NVlabs/GTRS` 只发 **4 个 checkpoint、其中只有 2 个属于这六个**（`gtrs_dense_vov.ckpt` **41.7**、`gtrs_aug_vov.ckpt` **42.1**，**都是 V2-99**）→ **49.4 不可复现**；**可复现单模最高 42.1**，**而 45.3 那个最佳单模（GTRS-Dense + ViT-L）也没发布**。→ **第 ② 层门槛要从 49.4 降到 42.1**。

### 3. **路线 ③ 的前置解决，且答案是正面的**

+8.6 出自 SimScale 摘要（"up to +8.6 EPDMS on navhard"），**对应仓库 Model Zoo 里 GTRS-Dense / ResNet34 / rewards-only 行（46.9）**。四条基线的增益（全部来自 SimScale 自己的表）：

| 基线 | 骨干 | 基线 | co-training 后 | 增益 |
|---|---|---|---|---|
| LTF | ResNet34 | 24.4 | 30.2 | +5.8 |
| **DiffusionDrive** | ResNet34 | 27.5 | **32.6** | **+5.1** |
| GTRS-Dense | ResNet34 | 38.3 | 46.9 | **+8.6** |
| GTRS-Dense | V2-99 | 41.9 | 48.0 | +6.1 |

→ **"对更强基线是否成立"的答案是"成立且不衰减"**——**最强的那条基线拿到最大增益**。

→ **而且有一个现成的组合**：SimScale **已测过 DiffusionDrive**（正是第三十六轮选定的起点），仓库里有 `diffusiondrive_agent.yaml`，HF 上有 **`diffusiondrive_sim_navhard.ckpt`** → **路线 ② 与路线 ③ 可以在同一起点上串起来，第一步只需推理**。

### 4. **SimScale 的 53.2 降级为"待核"**

SimScale 论文原文写 **"GTRS-Dense (V2-99) achieves a score of 48.0, establishing a new SOTA on navhard"**；**53.2 在 PDF 全文（1529 行）里不存在**，仓库 Model Zoo 最高也是 48.0。→ 推测是**官方 navhard 排行榜上的后续提交**（两篇相差半年），**但我们无法核实** → §1 / §3 / §5.1 / §7.5 的相关行已标注。

### 5. 顺带发现：SimScale 让 DiffusionDrive 的**舒适性塌掉一半**（P2c 的第二个同基准实例）

DiffusionDrive 逐阶段（SimScale Table 1）：S1 EC **79.6 → 59.6**；S2 EC **72.8 → 31.9**。而**总 EPDMS 涨 5.1**，涨分几乎全在 S2 的 **LK +14.4** 与 **NC +6.3**（S1 仅 +0.8）。→ **"涨分"与"舒适"在这条路上反向**，且**正好发生在我们选定的起点上** → 已写入 [preparation.md](../ideas/preparation.md) **P2c** 与 [sota-plan.md §5.4](../ideas/sota-plan.md) 的"必须一起报的代价"。

## 产出

| 类别 | 文件与章节 |
|---|---|
| 冲 SOTA 文件 | [sota-plan.md](../ideas/sota-plan.md) **新增 §7.7（§7.7.1–§7.7.4）**；更正 §1（SimScale / GTRS-E 两行）、§3 子榜、§5.1 第②③层、§5.4 路线 ③、§6（两条关闭 + 一条新增）、§7.5 第②③层；文件头 |
| 判断边界 | [judgments.md §B](../judgments.md) 新增 1 条（B 组 7 → **8**，总数 60 → **61**）；同条 §B 旧条里的"唯一一份 navhard 对照"改为"第一份" |
| 设计前提 / 问题 | [preparation.md](../ideas/preparation.md) **P8 清单 4 → 6 个实例**（补 navhard 的 ⑤⑥）+ **P2c 补第二个实例** + §6.1 的 navhard 指针补 §7.7 |
| 代码清单 | [code/repositories.md](../code/repositories.md) §下一步新增第 4 条（SimScale / GTRS 两仓的 ckpt 清单与"49.4 不可复现"） |
| 来源登记 | [sources.md](../sources.md) 新增 **L022**（两个 navhard 侧仓库 + 两篇 PDF 已逐表核）；顺带修 **L021 的"navhard 完整 12 行"→ 13 行**（第三十轮的 12→13 修正漏了这一处）并补上 §7/§7.6/§7.7 的指针 |
| 状态 / 索引 | [state.md](../state.md)（当前阶段、判断边界索引表 B 行、条数 61、**待续清单新增第 16 项：`preparation.md` 57.2 KB 的拆册预警**）、[history.md](../history.md)（18→**19** 卷）、[index.md](../index.md)、[README.md](../../../README.md) |
| 中间产物 | `/tmp/ai4r/simscale.pdf`、`gtrs.pdf` + 两个 `.txt`（仅用于本轮核表）→ 已登记 [inbox/cleanup.md](../../../inbox/cleanup.md) |

**验证**：`check_links.py` **七项全绿**（死链 0、表格 0 错、孤儿 0 / 弱引用 0、分册错册 0、笔记必写节 0 缺、小方向 README 0 缺），退出码 0。

**一句话**：**上一轮发现"榜上那个 45.0 在发布代码里不存在"；这轮发现"榜上那个 49.4 是六模型集成、只发了两个"，同时把路线 ③ 唯一的前置问题变成了正面结论——顺带证明了同一基准上跨论文依然不可横比。**
