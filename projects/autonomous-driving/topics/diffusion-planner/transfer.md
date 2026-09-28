# 来源 → 研究对象：可借鉴机制表

更新时间：2026-09-23  
性质：**全部为待验证假设**，不是已成立结论。本表回答"别的路线里有什么能搬到扩散规划器上"，不重复各来源自身的脉络。  
来源编号：具身侧 `DP-Exx`（见 [embodied-ai 论文表](../../../embodied-ai/topics/diffusion-policy/papers/diffusion_planner_embodied.md)），驾驶侧 `DP-Axx`（见 [papers/](papers)），基准 `Bxxx`（见 [../../sources.md](../../sources.md)）。  
证据等级：`全文` = 已读全文并核对表格；`摘要` = 仅摘要级；`元数据` = 仅登记；`代码静态检查` = 已克隆仓库并读代码/配置（**未安装未运行**，见 [repositories.md](../../code/repositories.md)）。

## 1. 具身侧机制（已具备）

| 机制 | 来源（编号） | 证据等级 | 对应到研究对象 | 障碍 / 风险 |
|---|---|---|---|---|
| receding horizon action chunk | Diffusion Policy（DP-E09，Ta=8 最优）、NoMaD（DP-E17） | 全文 + **代码静态检查** | 预测 Tp 步轨迹、只执行 Ta 步并滚动重规划 | 规划频率与控制频率不同；视野过短丢长时程意图 |
| 粗到细分层生成（PRP） | DiffuserLite（DP-E04，122 Hz，插件式 +560% 频率 / −3.2% 性能） | 全文 | 远端粗、近端细的分层轨迹，或作加速插件 | 粗层若不含约束，约束违反如何传播到细层**无人验证** |
| 一致性蒸馏少步化 | Consistency Policy（DP-E11，1–3 ms vs DDPM 110 ms） | 全文 | 把引入约束后增加的步数代价压回去 | 驾驶侧已用 2 步 / 1 步达到实时，边际收益小；蒸馏目标可能绕过约束投影 |
| 引导式约束（可微目标 / CBF） | Diffuser（DP-E01，引导尺度 α 跨任务差 3 个数量级）、SafeFlowMatcher（DP-E08） | 全文 + **代码静态检查** | 碰撞、可行驶区域、舒适性写成引导或硬约束 | 引导会破坏可行性；硬约束有算力代价。**代码级：**已发布脚本只演示 **2 个数量级**（`scale ∈ {0.1, 0.001}`）且**单任务**；另有三条论文未写的细节见 **§1.2**（梯度按后验方差缩放 / `t_stopgrad` 晚引导 / 引导后硬投影） |
| CFG 优于 Q 引导 | Decision Diffuser（DP-E02，附录 K：离线 Q 会高估 OOD 动作） | 全文 | 选择"CFG 还是 RL 值引导" | 与 DiffusionDriveV2 / DIVER 的 RL 引导做法**相反**。**2026-09-23 代码核验给出对齐口径**：DiffusionVeteran（DP-S14）把三者并列实现——**"引导"与"选优"是两件事**（`MCSS` = 无引导采样 + critic 选优；`cfg` = 条件引导；`cg` = 分类器引导 + 按分类器分数选优），DP-E02 批评的是"用离线 Q 做**引导**"，而 MCSS 是"无引导 + 用 critic **选优**"。详见 [代码脉络](../../code/traces/diffusion_planner_code_traces.md) §C/E |
| 只扩散状态 + 逆动力学出动作 | Decision Diffuser（DP-E02，3 个环境全部提升） | 全文 | 只生成轨迹，控制量由逆动力学给出 | 驾驶输出已是轨迹，收益可能有限 |
| 在线 RL 微调的工程细节 | DPPO（DP-E15：只微调最后 10 步最省、值估计只依赖 state、噪声 clip 有最优区间） | 全文 | 扩散规划器后训练 | 需在线 / 高保真仿真交互；PG 样本效率低 |
| 训练 / 采样效率技巧 | EDP（DP-E28：action approximation + DPM-Solver，训练 5 天→5 小时） | 全文 | 降低实验迭代成本 | 面向单步动作，与轨迹块不完全同构 |
| 等变结构 | Equivariant Diffusion Policy（DP-E12：等变结构比 voxel 表示更重要） | 全文 | 车体坐标下的旋转等变先验 | 道路结构 / 规则 / 目标语义**不是**旋转不变的，直接套用不成立 |
| 3D 表示条件化 | DP3（DP-E10：简单 3D 表示 > RGB-D/voxel，3 层 MLP 已足够） | 全文 + **代码静态检查** | 点云 / LiDAR 条件规划 | 缺交互与规则语义。**代码级更正：**编码器实为 **4 层** Linear（`in→64→128→256→512`）+ 全局 max-pool，输出仅 **64 维**；仓库的 "simple" 变体改的是 **U-Net 宽度**（512/1024/2048 → 128/256/384），**不是编码器层数** |
| 统一动作空间 | RDT-1B（DP-E21） | 摘要 | 跨车型 / 跨数据集轨迹表示统一 | 会牵动基线输出接口 |
| 冻结骨干 + 只训条件通路 | Freeze-Share-Shrink（DP-E16）、FLOWER（DP-E14） | 摘要 | 新城市 / 新车队低成本适配 | 是否适用于扩散规划器**未核验** |
| 目标掩码的统一策略 | NoMaD（DP-E17：Bernoulli p=0.5 掩码目标） | 全文 + **代码静态检查** | 同一策略支持有 / 无导航目标、多指令切换 | 驾驶中无目标场景少。**代码级：**`goal_mask_prob: 0.5` 已确认；另补上论文未写的**重加权系数** `(context_size+2)/(context_size+1)`（见 §1.1） |
| 熵可控的流匹配 RL | FMER（DP-E24）、Reverse Flow Matching（DP-E23） | 摘要 | 可控多样性的后训练 | 训练稳定性与算力 |
| 要素级评价 | EBench（B011） | 元数据 | 把"单一 PDMS"拆成能力画像 | 需要额外标注与评测成本 |

**代码级补充（2026-09-23）**：§1 此前是**全表唯一没有代码级补充的一节**（§2/§3 都有），而其中 **4 个来源的仓库就在工作空间里**（`diffusion_policy`、`3D-Diffusion-Policy`、`visualnav-transformer`、`diffuser`，见 [repositories.md](../../code/repositories.md) §C）。本轮逐条核验，结论是**能核的 4 条里 3 条成立、2 条需收窄或更正**。

### 1.1 逐条核验

| 机制（§1 原文） | 论文级数字 | 代码级实测 | 判定 |
|---|---|---|---|
| receding horizon action chunk（DP-E09 "**Ta=8 最优**"；DP-E17） | Ta=8 | **Diffusion Policy**：22 个 workspace 配置里 `n_action_steps` **14 个取 8、8 个取 1**；`horizon` **13 个取 16**（即 Tp=16/Ta=8 是主流）。**NoMaD**：`train/config/nomad.yaml:58` **`len_traj_pred: 8`** | **一致且更强**：Ta=8 是**主流但不是唯一**（8 个配置取 1）；且**两个独立来源都落在 8** |
| 引导式约束（DP-E01，"引导尺度 α **跨任务差 3 个数量级**"） | 3 个数量级 | `diffuser/sampling/functions.py::n_step_guided_p_sample` 的**函数签名默认 `scale=0.001`**；而 `scripts/release-run.sh` 只扫 **`scale ∈ {0.1, 0.001}`（= **2 个数量级**）**，且**只在 `halfcheetah-medium-v2` 一个任务上** | **需收窄**：**已发布脚本只演示 2 个数量级、单任务**；"3 个数量级"只能来自论文的跨任务表 |
| 目标掩码（DP-E17，"Bernoulli **p=0.5**"） | p=0.5 | `train/config/nomad.yaml:39` **`goal_mask_prob: 0.5`** ✅；实现见 `nomad_vint.py:64-69`：`goal_mask[:, -1] = True  # Mask out the goal`、`all_masks = cat([no_mask, goal_mask])`，且**平均两个掩码时用 `(context_size+2)/(context_size+1)` 重加权** | **一致**，并补上论文未写的**重加权系数** |
| 3D 表示条件化（DP-E10，"简单 3D 表示 > RGB-D/voxel，**3 层 MLP 已足够**"） | 3 层 MLP | `model/vision/pointnet_extractor.py::PointNetEncoderXYZ` 是 **4 层 Linear**（`in→64→128→256→512`）+ `torch.max(x, 1)[0]`（全局 max-pool）+ 投影到 `out_channels`；`dp3.yaml` 里 **`encoder_output_dim: 64`**。**仓库的 "simple" 变体改的是 U-Net 宽度**（`down_dims` 512/1024/2048 → 128/256/384），**不是编码器层数** | **需更正**：编码器是 **4 层**而非 3 层；"简单"在代码里指 **U-Net 变小**，与"编码器浅"不是一回事 |

### 1.2 代码里读到、§1 未列的四条可搬机制

| 机制 | 代码证据 | 对应到研究对象 | 障碍 / 风险 |
|---|---|---|---|
| **引导梯度按后验方差缩放** | `if scale_grad_by_std: grad = model_var * grad`（`functions.py:21-22`，签名默认 `scale_grad_by_std=True`） | **这解释了"引导尺度跨任务差几个数量级"的成因**——`scale` 的绝对意义依赖任务的方差尺度，**不能跨任务复用同一个 α**。而驾驶侧 DP-A01 的引导强度是**硬编码 1.5**，正缺这一层归一化 | 需能拿到后验方差；缩放后的有效步长与去噪日程耦合 |
| **引导只在 t ≥ `t_stopgrad` 生效** | `grad[t < t_stopgrad] = 0`；`release-run.sh` 取 **`t_stopgrad=4`**（总步数 `n_diffusion_steps=20`） | 与驾驶侧 DP-A01"引导只在扩散末段（t∈(0.005,0.1)）生效"**是同一类做法**——**两个域独立收敛到"晚引导"** | 晚引导意味着早期误差无法被纠正 |
| **每步引导后立刻硬投影条件** | 引导循环**内**每步都调 `x = apply_conditioning(x, cond, model.action_dim)` | 与 PC-Diffuser 的"约束投影"同类：**引导（软）+ 投影（硬）叠加**，而不是二选一 | 投影算子需可微且不破坏流形 |
| **每步可多次引导** | `for _ in range(n_guide_steps)`；`release-run.sh` 扫 **`n_guide_steps ∈ {2, 1}`** | 引导强度有"次数 × 尺度"两个旋钮 | 多次引导的算力代价线性增长 |

### 1.3 两条判断

1. **§1 的数字必须逐条看代码**：能核验的 4 条里，**2 条需收窄或更正**（"Ta=8 最优"实为"主流但 8/22 配置取 1"；"3 个数量级"在已发布脚本里只有 **2 个数量级且单任务**；"3 层 MLP"实为 **4 层**且 "simple" 指 U-Net）。→ 与 [C003](../diffusion-planner/papers/diffusion_planner_ad.md)/[C005](../../code/traces/e2e_trunk_code_traces.md) 的结论同构：**论文级数字一律先核代码**。
2. **代码比论文多出四条工程细节**，其中"**引导梯度按后验方差缩放**"直接解释了本项目一直缺的一环——**为什么引导强度不能跨任务/跨基准复用**（对应 [preparation.md](../../ideas/preparation.md) 里"引导项数量与强度口径不明"的问题）。→ 若本项目要在驾驶侧做引导，**应把"按方差归一化"作为默认设计，而不是沿用硬编码常数**。

### 1.4 π0 / π0.5（DP-E19/E20）的代码级核验

**动因**：`openpi` 是具身侧**最后一个未做代码核验**的仓库（另一份盘点结论：**当时 36 个**仓库里只剩 `openpi` 与 `navsim` 的 Agent 侧未核；第二十一轮新增 `OpenDriveVLA` 后快照总数为 **37 个**）。其笔记 [DP-E19-pi0.md](../../../embodied-ai/topics/diffusion-policy/notes/DP-E19-pi0.md) 自述"**openpi 代码是否包含可迁移抽象需代码静态检查，尚未做**"。

**声称 vs 实测（`src/openpi/models/pi0.py` + `pi0_config.py`）**：

| 论文表声称 | 代码级实测 | 判定 |
|---|---|---|
| 条件流匹配（非 DDPM）、高斯起点、线性高斯路径、前向 Euler 10 步 | `compute_loss`：`noise = normal(...)`；`x_t = t·noise + (1−t)·actions`（**线性插值路径**）；`u_t = noise − actions`；损失 `mean((v_t − u_t)²)`（**速度场 MSE**）；`sample_actions(num_steps=10)`、`dt = −1.0/num_steps`（**Euler 反向积分 10 步**） | **完全一致** ✅ |
| 300M 动作专家 | `action_expert_variant: "gemma_300m"` | **一致** ✅ |
| **总 3.3B** | 配置只有 `paligemma_variant: "gemma_2b"` + `gemma_300m` → **2B + 300M = 2.3B**；**全仓 grep 不到 3.3 的直接来源** | **需标注**：配置可读的是 2B+300M，3.3B（含视觉塔）**在代码里无法确认** |
| action chunk H=50 | `action_horizon: int = 50` | **一致** ✅ |

**代码里比论文表多出的四条细节**：

1. **时间步采样不是均匀的，而是 `Beta(1.5, 1)`**（`pi0.py:197`：`time = jax.random.beta(time_rng, 1.5, 1, batch_shape) * 0.999 + 0.001`）——密度 ∝ t^0.5，**偏向 t=1（噪声端）**。**驾驶侧是均匀采样**（如 HDP 的 `sde.py`：`t = torch.rand(B)*(1−eps)+eps`；DiffusionDrive 的 `torch.randint(0,50)`）。→ **这是本项目未记录的一条可搬细节**：训练时把时间步密度偏向噪声端，等于**把更多容量花在"高噪声→干净"的早期阶段**。
2. **代码的时间约定与论文相反，且作者自承**（`pi0.py:226-227` 原文）："note that we use the convention more common in diffusion literature, where **t=1 is noise and t=0 is the target** distribution. **yes, this is the opposite of the pi0 paper, and I'm sorry.**" → 引用 π0 的公式时**必须先确认用的是哪套约定**（与 C003 记录的各家 `model_type`/`supervision_type` 口径问题同构）。
3. **π0.5 的差异在代码里非常具体**（`pi05` flag 触发 4 处分支）：① **状态输入被离散化并放进语言 token**（`pi0_config.py:29` 注释原文："the state input is part of the **discrete language tokens** rather than a continuous input that is part of the suffix"）；② `discrete_state_input` 默认 = `pi05`；③ `max_token_len` **48 → 200**；④ 动作专家启用 **adaRMS** 条件（`use_adarms=[False, True] if config.pi05 else [False, False]`）。→ 即 **π0 → π0.5 的关键变化之一是"状态从连续输入变成离散 token"**，这正对应本项目关心的"连续 vs 离散"维度。
4. **`action_dim: 32`**：动作维度是 32，远大于单臂 7 自由度 → 是**统一动作空间的 padding 位**（对应 DP-E21 那条"统一动作空间"机制的同类做法）。

**判断**：π0 的四条论文级声称里 **3 条代码级一致、1 条（3.3B）需标注**；代码另给出 4 条未记录细节，其中 **`Beta(1.5,1)` 时间采样**与 **"状态离散化"是 π0.5 的核心改动**两条**直接可搬**。→ 与 §1.1 的结论同构：**具身侧的论文级数字同样必须逐条看代码**。

### 1.5 第二十五轮新增：6 条未记录的可迁移机制候选

**来源**：具身侧 VLA 论文表的第二十五轮补全（**摘要级**，见 [embodied-ai/topics/vla/papers.md](../../../embodied-ai/topics/vla/papers.md)、[world-model/papers.md](../../../embodied-ai/topics/world-model/papers.md)）。**均为候选，未验证**。

| # | 机制 | 来源 | 证据等级 | 对应到研究对象 | 障碍 / 风险 |
|---|---|---|---|---|---|
| 1 | **控制频率作为显式输入特征**——把采样率喂进模型以兼容异构频率 | RDT-1B（`2410.07864`） | 摘要 | 直接解决驾驶侧"**2 Hz nuPlan / 10 Hz nuScenes / 2 Hz NAVSIM 混训**"的问题（本项目 transfer.md 已列"规划频率 ≠ 控制频率"这一障碍） | 需确认驾驶侧各基准的频率差异是否已被数据管线吃掉；若已对齐则无增益 |
| 2 | **无观测正运动学（FK）预训练动作头 + 只训条件通路**——预训练信号是"**无标注的运动学对**" | Freeze-Share-Shrink（`2511.12101`） | 摘要 | 驾驶侧可用**无标注轨迹 + 自行车模型**做轨迹先验，新城市只训条件（地图 / 指令）通路 | 比 §1 已有的"冻结骨干 + 条件通路"更具体，但**无官方代码**，不可复现 |
| 3 | **小骨干足够**——**5M MLP ≥ 244M U-Net** | Freeze-Share-Shrink | 摘要 | **直接挑战驾驶侧"大 DiT 去噪轨迹块"的容量假设**（DiffusionDrive / MeanFuser / DP-A01 都是大骨干） | 结论只在 MimicGen / LIBERO 两个基准上；驾驶的观测复杂度更高 |
| 4 | **条件机制冻结兼容性**——**调制式（FiLM / AdaLN）可冻结后适配，注意力式冻结即崩溃**（DP-T 冻结后 60.4→19.4、76.4→5.9） | Freeze-Share-Shrink | 摘要 | 跨城市 / 跨数据集的**冻结适配**必须用调制式条件——对"冻结 VLM 只训扩散头"这类做法是硬约束 | 与驾驶侧现有做法（DiffusionDrive 用 cross-attention 注入条件）**方向相反**，需实验确认 |
| 5 | **中间模态融合 / 剪 VLM 层，把容量让给动作头** | FLOWER（`2509.04996`，CoRL'25） | 摘要 | 与 §2 的"双系统分离"互补——**那是分工，这是容量分配** | 受控消融有（中间融合 vs 早融合 93.4% vs 33.4%），但只在 CALVIN / LIBERO |
| 6 | **潜动作 / 伪动作当辅助流匹配目标**——用无动作标注的视频生成伪动作扩训 | GR00T N1（`2503.14734`）的 LAPA / IDM | 摘要 | 用**无动作标注的驾驶视频**生成伪动作扩训；是 §3"世界模型当 reward/next-state 来源"之外的**第 4 条数据路线** | 伪动作质量决定上限；驾驶的"动作"是轨迹而非关节角，IDM 的对应物是什么需先定义 |

**另有一条与 §1.4 呼应的补充**：**FLOWER 的受控消融直接比较 flow / L1 / 离散 token 三路**，而**OpenVLA-OFT 证明连续 L1 回归 ≈ 扩散且更快**——**与驾驶侧 SpanVLA 的"回归 → flow matching = +5.2 PDMS"方向相反**。→ **"扩散一定更好"在具身侧不成立**，引用时必须注明是哪一侧、哪个任务（见 [embodied-ai/direction/lineage.md §2](../../../embodied-ai/direction/lineage.md)）。

## 2. VLA 侧机制（2026-09-23 第一轮；**同日读全文升级**）

来源：[../vla/papers.md](../vla/papers.md)（VLA-xx）与 [../vla/lineage.md](../vla/lineage.md)。证据等级：`综述全文` = 来自 [2506.24044](https://arxiv.org/abs/2506.24044) / [2512.16760](https://arxiv.org/abs/2512.16760) 正文；`全文` = 本次已读 PDF 正文与表格；`摘要` = 仅摘要级。

| 机制 | 来源（编号） | 证据等级 | 对应到研究对象 | 障碍 / 风险 |
|---|---|---|---|---|
| **双系统分离**：慢系统做高层推理，快系统做实时轨迹生成 | VLA-04 DriveMoE、VLA-18 ExploreVLA；2512.16760 §2.2.2 | 综述全文 | LLM/VLM 只输出**目标或约束**，扩散器负责轨迹生成——把推理频率问题挡在生成器之外 | 需要明确两系统的接口契约；高层推理若仍是瓶颈（综述列为 `sub-30 Hz` 未解），整体频率仍被拖住 |
| **语言条件进扩散器可达 13.3 Hz**（本次新增的实测值） | VLA-07 ReCogDrive（= DP-A28，[笔记](../vla/notes/VLA-07-recogdrive.md)） | 全文 | **13.3 Hz**——已跨过 10 Hz 门槛；对比 VLM 直出轨迹只有 **0.9–1.7 Hz**。证明"语言 + 扩散"这条路在频率上可行 | 仍低于综述要求的 30 Hz；NAVSIM PDMS 90.8 是**纯相机**结果，需与相机+LiDAR 基线分开比；Bench2Drive **Comfort 仅 17.45** |
| **语言作为引导而非回归目标**（action-mask 机制） | VLA-07 ReCogDrive（= DP-A28） | 全文 | 避免语言条件在回归训练下被视觉先验淹没（"条件策略坍缩"，见 DP-A26） | 具体机制（action-mask）未细读；是否通用未验证 |
| **语言中间表示当锚点先验** | VLA-08 KnowDiffuser（= DP-A30，[笔记](../vla/notes/VLA-08-knowdiffuser.md)） | 全文 | LM 推断元动作 → 映射到**历史轨迹先验** → 从先验起步做两阶段截断去噪 | **GPT-4o 在回路内**（延迟与成本受外部 API 约束）；**未与 DP-A01 对比**，在 nuPlan 上的真实位置未知 |
| **VLM 引导 + 稀疏-稠密混合扩散** | VLA-06 DiffVLA（= DP-A27，[笔记](../vla/notes/VLA-06-diffvla.md)） | 全文 | VLM 输出横/纵向命令 → 与导航指令合并 → 作为扩散的语义引导；锚点 **32 个**（vs DiffusionDrive 20） | **是竞赛技术报告，非正式论文**；加了扩散器后碰撞与车道保持子指标**反而变差**，且需"y 轴 2% 减速"后处理兜底 |
| **符号逻辑否决层**（神经符号安全核） | VLA-05 SafeAuto；2506.24044 §4.2/§8 | 综述全文 | 生成后加规则校验，否决越界轨迹 | 与综述 DP-S11 §8.9 主张的 "safety governor" **同源**；两者都**无实现与实验** |

**本次读全文后的净收获**：VLA 侧最关键的空白——**延迟**——已有实测答案（13.3 Hz），且做法与"双系统分离"一致。**新的空白**：ReCogDrive 的 Comfort 极低（17.45），说明"语言 + 扩散"在高频下牺牲了舒适性，而舒适性恰是驾驶的核心指标之一。

## 3. 世界模型侧机制（2026-09-23 第一轮；**同日读全文升级**）

来源：[../world-model/papers.md](../world-model/papers.md)（WM-xx）与 [../world-model/lineage.md](../world-model/lineage.md)。证据等级：`全文` = 本次已读 PDF 正文与表格；`摘要` = 仅摘要级。

| 机制 | 来源（编号） | 证据等级 | 对应到研究对象 | 障碍 / 风险 |
|---|---|---|---|---|
| **未来潜状态作为条件** | WM-09 DriveFuture（= DP-A31，[全文笔记](notes/DP-A31-drivefuture.md)） | 全文 | 把未来潜状态（16 个 future query token）喂给 DDPM 去噪器；**受控收益 navhard +3.7（30.9→34.6，不含 scorer）** | 收益来源未拆解；**"24.2→55.5" 是误读**（那是同表两行不同方法 + 含 scorer）；世界模型自身推理成本**未报告**；训练用 GT 未来精修 → 条件与监督纠缠 |
| **未来帧条件买安全、卖进度**（本次新增的量化结论） | WM-17 Policy World Model（[笔记](../world-model/notes/WM-17-policy-world-model.md)） | 全文 | **不预测未来帧 → EP 更高；预测未来帧 → NC 更高**。这是"条件信息量"旋钮的**收益/代价量化**，可直接作为实验的对照口径 | 该权衡是在 NAVSIM 上观察到的，**是否在 navhard 上同向未验证**；40 FPS 不含像素解码 |
| **用生成未来做"选优"**（第三种形态） | WM-01 Drive-WM（[笔记](../world-model/notes/WM-01-drive-wm.md)） | 全文 | 世界模型**既不供条件也不做规划器**，只在候选命令间选优：随机命令碰撞率 **0.93%→0.26%**，接近 GT 命令 0.22%。对研究对象的"选优器瓶颈"（P4）直接可用 | 候选只有 **3 个命令**，与扩散器的 20–32 个锚点不同量级；选优仍略差于 GT；**代码核验：仓库只有图像生成侧，选优机制无代码可核验** |
| **世界模型给候选轨迹打分**（轨迹级选优，**已代码核验**） | WM-24 WoTE（[papers.md §4.1](../world-model/papers.md)、[C004 §E](../../code/traces/world_model_code_traces.md)） | **代码静态检查** | **256 条 K-means 锚** → 世界模型预测每条候选的未来 BEV → **学到的奖励模型**（imitation softmax + 5 个 PDM 子指标 sigmoid，在 log 空间复现 PDMS 加权结构）→ `argmax` 选一条。论文 Table 3：无评估 81.0 → 有评估但用当前状态 83.2 → **加入未来状态 85.6**；NAVSIM **PDMS 88.3（README）/ 87.1（Table 1）**，延迟 **18.7 ms** | **规划器本身非扩散**（锚 + offset 回归）——所以这条机制是"**给扩散采样结果打分**"，不是"改生成器"；候选数 256 与扩散器的 20–32 不同量级；**训练需真值**（nuPlan 模拟器离线预计算的 PDM 子分数表），本项目无此基建 |
| **占据当规则 cost**（选优依据的第二种信号，**已代码核验**） | WM-04 Drive-OccWorld（[C004 §I.1](../../code/traces/world_model_code_traces.md)） | **代码静态检查** | 世界模型输出的**未来语义占据** → `argmax` → 算 `instance_occupancy` + `drivable_area` → **`Cost_Function` → cost volume → `topk(largest=False)`**；cost 用 **hinge `relu(gt_cost − sm_cost)`** 学。→ **不需要学奖励模型**，规则几何量即可 | **训练用 GT 占据**（注释原文）；**候选只有预采样的一批**且按 3 command 均分；`planning_steps=1` 逐帧滚动；**其规划损失直接抄自 UniAD**（轴对齐退化一并继承） |
| **用世界模型损失做模态分配**（选优依据的第三种信号，**已代码核验**，本工作空间唯一一例） | WM-07 World4Drive（[C004 §I.2](../../code/traces/world_model_code_traces.md)） | **代码静态检查** | **`loss_rec = 重建 + KL + 余弦`**（世界模型的三种损失之和）→ `total_loss = loss_rec·w + FDE·w_tm` → **`argmin`** 决定哪个模态被监督。→ 直觉：**能让世界模型更好预测未来的模态更可信** | **FDE 项用 GT** → 是**训练期模态分配**，不是推理期选优（测试走分类 argmax）；`torch.cat(..., dim=0)` 的形状处理**只在 B=1 时成立**（需运行确认）；**`class W4D(VAD)` 继承 VAD**，锚点用同名 `kmeans_plan_6.npy` |
| **潜预测无需解码回像素** | WM-06 LAW（[笔记](../world-model/notes/WM-06-law-latent-world-model.md)） | 全文 | **无感知输入**（perception-free）即可提升规划——扩散器接条件时**不必接完整世界模型**，一个自监督潜预测头可能就够 | L2 改善但**碰撞率未同步改善**（0.61/0.30% vs 带感知 0.49/0.19%），再次指向指标不一致 |
| **世界模型不必慢** | WM-03 OccWorld（[笔记](../world-model/notes/WM-03-occworld.md)） | 全文 | 占据世界模型 **18 FPS** 且规划指标优于 UniAD（1.8 FPS）——慢的是解码回像素，不是潜/占据预测 | 其规划输入是 **3D-Occ 特权级**，非原始传感器，与相机端到端不可比 |
| **RL 后训练同时改善安全性** | WM-18 WorldRFT（[笔记](../world-model/notes/WM-18-worldrft.md)） | 全文 | 碰撞感知奖励的 GRPO 把 nuScenes 碰撞率 **0.30%→0.05%（−83%）**；对 P2c（分数与可行性不一致）是一份正面证据 | **轨迹仅 2 Hz，非实时**；NavSIM 仍差 DiffusionDrive 0.3；**代码核验：官方仓库为空，机制无代码可核验** |
| 潜空间 rollout + 选动作 | WM-14 Think2Drive、WM-15 AdaWM、WM-16 Raw2Drive | 摘要 | 候选轨迹先在潜空间评估再选优 | 与研究对象的"选优机制"轴重合；需额外世界模型推理预算 |
| 从预测转向规划（状态-动作联合预测） | WM-17 Policy World Model | 全文 | 世界模型直接输出状态-动作对 | 与"世界模型当条件"是两条不同路线，**未在同一基准比较过** |
| 双潜世界模型做预训练 | WM-08 DLWM | 摘要 | 用世界模型提供预训练表征 | 与端到端扩散规划器的适配方式未验证 |
| 潜空间统一规划与生成 | WM-11 DriveLaW | 摘要 | 规划与视频生成共享潜空间 | 训练复杂度高；实时性未报告 |
| 生成式世界模型的评价基准 | WM-20 DrivingGen | 摘要 | 给"世界模型质量"提供评测 | 评的是**生成质量**，不是"作为条件的有效性"——后者仍是空白 |

**本次读全文后的净收获**：世界模型侧从"全部待验证"变成**有两条可量化的结论**——① 未来帧条件的收益/代价可量化（WM-17）；② 世界模型当"选优器"有实测价值（WM-01）。**共同空白仍在**：没有任何一条在**同一基准**上与本项目的现状做过对照；世界模型侧最值得做的实验仍是拆解 WM-09 的收益来源（对应 [../../ideas/preparation.md](../../ideas/preparation.md) 方向 A 之外的第二条线）。

**代码级补充（2026-09-23，见 [world_model_code_traces.md](../../code/traces/world_model_code_traces.md)）**：上述两条可量化结论的**代码可核验程度不同**。

1. **WM-17 可核验，且接口机制比论文写得更具体**：`models/modeling_showo.py:navsim_forward` 一次前向同时产出未来帧 token 的交叉熵与轨迹 L1；轨迹 query 排在**未来帧 token 之后**（`input_embeddings[:, -action_len:, :] = act_queries`），规划头读 `hidden_states[:, -8:]`。即"未来帧条件"是**隐状态级**的，不是显式图像级。损失配比在配置里：`video_coeff: 0.3` / `tj_coeff: 1.0`。
2. **WM-01 不可核验，但同形态的 WM-24 WoTE 可核验**：WM-01 的仓库只有图像生成侧（vendored diffusers），tree-based planner 与 image reward 不在其中。**第二十四轮补上了一个可核验的同形态实例**——WM-24 WoTE（ICCV'25）的"世界模型给 256 条候选轨迹打分选优"全部成立（`select_best_trajectory` → `torch.argmax(final_rewards, dim=-1)`），且其奖励模型**在 log 空间复现了 PDMS 的加权结构**。→ **"选优器"这条机制从"只有论文级证据"变成"有代码级证据"**，但**粒度不同**（WM-01 是命令级、WM-24 是轨迹级）。
3. **WM-18 不可核验**：官方仓库为空（仅 LICENSE + readme，readme 称代码 "soon" 上传）。
4. **新增一条可搬的接口路线**：WM-03 OccWorld 走的是**token 级联合自回归**——未来占据 token 与自车 pose token 在同一序列里逐步交替生成（`TransVQVAE.forward_autoreg_with_pose` 的 `for i in range(mid_frame, end_frame)` 循环），预测 token 回灌、无 teacher forcing 泄漏。这与 WM-17 的"隐状态级条件"是**两种不同的接口**，可直接作为研究对象的对照设计。
5. **接口路线已定型为五条**（第二十四轮，见 [../world-model/lineage.md](../world-model/lineage.md)）：① token 级联合自回归（OccWorld / RenderWorld）② 隐状态级条件（PWM）③ **特征级条件**（WM-21 DriveDreamer：池化 Auto-DM 多尺度 UNet 特征 + 历史动作 → MLP 出动作，**代码范围不符不可核验**）④ **选优依据**（WM-01 命令级 / WM-24 轨迹级）⑤ **RL 的 reward/next-state 来源**（WM-23 Imagine-2-Drive 把世界模型当"想象环境"回灌 PPO，**代码未发布**）。→ **路线 1–4 的规划器本身都不是生成式**；对研究对象而言可用的接口位是 **②③（当条件喂进去噪）** 与 **④（当评价器给采样结果打分）**。

## 4. 使用约定

1. 本表条目**不得**在未验证前写进论文正文当作已有结论。
2. 每条机制进入实验前，必须先确认"障碍"一栏在驾驶域是否成立。
3. 来源自身的完整脉络不在本表，见对应小方向的 `lineage.md`；本表只保留与研究对象相关的投影。
