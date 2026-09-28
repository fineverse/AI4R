# 第四十一轮（2026-09-24）· 用户给了两个改变前提的新信息 → 方向重排

**动因**：用户提出两个**此前不在工作空间里的前提**：

1. **最终目的**：「**最核心目标是发表一篇自动驾驶方向 CCF-A 类会议论文；只要能实现这个目标，其他都可以妥协**」→ **SOTA 是手段，不是目的**。
2. **实际算力**：「**自备双卡 RTX 3090 做实验**，出成果后再花钱租大显存卡，**上限 A800 80G**」。

第 2 条尤其要紧：**`sota-plan.md §4` 的整个排序是在"算力未定"下做的**，而它的第一名（B 选优器）**唯一依据就是 `scorer ≈ +20`**。

## 做法

① 把新前提落盘（`preparation.md §7.1/§7.2`、`context.md`、`state.md` 待续清单第 6 项）；② 用**已核验的训练规模**算一遍"48 GB 能做什么"；③ 复核 B 的排序依据——**发现它的原始依据拿不到**，于是去找替代依据；④ 在找替代依据时**把一个一直没钉死语义的数字核到了原文**。

## 结论（含更正）

### 1. 算力账：三条轴被直接排除

| 轴 / 路线 | 代表工作的**实际训练规模** | 48 GB 下 |
|---|---|---|
| **VLA** | ReCogDrive 2.3M 数据 + 7B 级 VLM | ❌ |
| **世界模型（视频扩散）** | 视频扩散预训练 | ❌ |
| **路线①「复现 DriveFuture」** | 原文自述 **8×NVIDIA 5090 / 100 epochs**（≈12–16× 3090） | ❌（A800 单卡也补不上） |
| **NAVSIM 评测本身** | devkit 是 2D 伪仿真、无渲染 | ✅ 很便宜 |
| **60M 级规划器（DiffusionDrive 档）** | 60M 参数 / ResNet-34 | ✅ 可训 |
| **选优器 / 约束层等小模块** | 参数少 | ✅ 便宜 |

→ **能做的只剩"冻结 + 小规模训练 + 推理期"这一类。**

### 2. **§4 把 B 排第一的依据要改：那个 +20 拿不到**

§4 排 B 第一，**唯一依据是 `scorer ≈ +20`**。但第 35–37 轮已证明：那个 +20 是 **DriveFuture 自己 100 候选池**上的受控值（34.6 → 55.5），且**不能叠在"已含选择环节"的方法上**；而我们训得起的生成器是 **20 锚点**的 → **+20 不可达**。

### 3. **但核到一个更可靠的替代依据——而且它一直躺在本工作空间的表里，只是语义没钉死**

`DP-A02` / `DP-A03` 的笔记里一直抄着 DDV2 Table 3 的 `Div 42.3 / Top-1 93.5 / Top-5 84.3 / Top-10 75.3`，但**从没核过 `Top-K` 是什么**。本轮下载 DDV2 论文（arXiv 2512.07745）逐字核：

> **题注**："**PDMS@K denotes the PDMS score evaluated on the Top-K ranked trajectories**"
> **正文**："The results presented here are the models' **raw outputs, evaluated before their respective selection modules**（即 DiffusionDrive 的分类器 / DDV2 的 selector）… **@1 称 upper bound、@10 称 lower bound**"

→ **`PDMS@1` = 原始 20 条候选里最好那条的 PDMS = 池子天花板**。于是：

| 方法（均 20 条候选） | 池子天花板 `PDMS@1` | 其选优模块的输出 | **选优损失** |
|---|---|---|---|
| **DiffusionDrive** | **93.5** | **88.1** | **−5.4** |
| **DiffusionDriveV2** | **94.9** | **91.2** | **−3.7** |

**而且 DDV2 自己写下了动机原话**："**this over-reliance is a critical concern**, as selector modules typically have fewer parameters, leading to weaker generalization capabilities. Consequently, **they are prone to failure in out-of-distribution scenarios**"。

→ **这是方向 B 最强的一条证据**：① **已发表、同基准**（不是推测）；② **在 2×3090 上完全可复现**（冻结 60M 模型 + 训一个头）；③ **动机可直接引用原文**。

### 4. **B 的目标要从"打败 48.0"改成"压缩选优损失"**（本轮最要紧的一句）

- **不是**"总分超过某个别人的数"——那依赖别人放不放代码、用哪套口径（§7.7.1 已证明三张表互差 3.3–5.2）
- **而是**"**把选优损失从 5.4 压到 X**"——**天花板自己可测**、不依赖别人放代码、且可复现
- 且 **navhard 是 OOD 场景**，按 DDV2 自述的 hazard，那里损失**应当更大** → **这正是论文的主结果**

### 5. 第一步（纯推理，2×3090 足够）

1. 跑通 **SimScale 的 `diffusiondrive_sim_navhard.ckpt`（navhard 32.6，已发布的最强扩散规划器）** → 拿自己的可信基线 + 验证本地 devkit 口径
2. **量 navhard 上的池子天花板**——**这一步是全新的：DDV2 只做了 navtest**
3. 量 floor（固定取第 0 条）与 top-1 违规分布

→ **天花板 − 基线 = B 的全部空间**；若 navhard 上的差显著大于 navtest 的 5.4，**B 成立**；若几乎不涨（池子被 20 锚点锁死），**转 A**，且评测脚手架已搭好。

## 产出

| 类别 | 文件与章节 |
|---|---|
| 前提记录 | [preparation.md §7.1 / §7.2](../ideas/preparation.md)（**7.1/7.2 已回**，含"48 GB 能做什么"的算力账）、[context.md](../context.md) 的资源行、[state.md](../state.md) 待续清单第 6 项 |
| 方向重排 | [sota-plan.md](../ideas/sota-plan.md) **新增 §8（§8.1–§8.5）**；**§4 的 B 行改写**（依据从 +20 换成选优损失） |
| 语义钉死 | [DP-A02 笔记](../topics/diffusion-planner/notes/DP-A02-diffusiondrive.md) 与 [DP-A03 笔记](../topics/diffusion-planner/notes/DP-A03-diffusiondrivev2.md) 的 `PDMS@K` 行（**核到原文**：raw outputs / before selection modules / @1 = upper bound） |
| 判断边界 | [judgments.md §D](../judgments.md) 新增 1 条（D 组 9 → **10**，总数 63 → **64**） |
| 设计前提 | [preparation.md](../ideas/preparation.md) **P4 量化**（选优器瓶颈 → "选优损失 5.4 / 3.7"） |
| 状态 / 索引 | [state.md](../state.md)（当前阶段、索引表 D 行、条数 64）、[history.md](../history.md)（22→**23** 卷）、[index.md](../index.md)、[README.md](../../../README.md) |
| 中间产物 | `/tmp/ai4r/ddv2.pdf`（3.6 MB）+ `ddv2.txt` → 已登记 [inbox/cleanup.md](../../../inbox/cleanup.md) |

**验证**：`check_links.py` **七项全绿**，退出码 0。

**一句话**：**用户把目标从"SOTA"改成"CCF-A"，把算力定成 2×3090——两条一起把 §4 的排序依据打掉了；但复核过程中把一个一直没钉死语义的数字（DDV2 的 `PDMS@1`）核到原文，结果它是"池子天花板"，于是 B 不但没被淘汰，反而换到了一个更硬的依据上：不追别人的总分，改追"压缩选优损失"。**
