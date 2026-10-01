# 具身智能发展脉络

更新时间：2026-09-23  
状态：**初稿**（第二十五轮补写；证据以摘要级为主，已标明）。  
约定：脉络类文档写**判断**（阶段划分、关键转移、未解决问题），事实留在论文表与笔记里。  
相关：[VLA 小方向](../topics/vla/README.md)、[世界模型小方向](../topics/world-model/README.md)、[扩散策略论文表](../topics/diffusion-policy/papers/diffusion_planner_embodied.md)、对自动驾驶侧的迁移机制 [transfer.md](../../autonomous-driving/topics/diffusion-planner/transfer.md)。

## 1. 阶段划分

具身侧（机器人学习）的演化**不是一条线，而是两条线交错**——"**策略怎么表示动作**"与"**世界模型怎么建模未来**"。两条线各自分段，交叉点在 2024–2025 年。

### 线 A：策略的动作表示（4 段）

| 段 | 时期 | 分界标志 | 代表 | 输出形态 |
|---|---|---|---|---|
| **A1 单步回归模仿学习** | 2017–2023 | 行为克隆 + 单步动作回归 | RT-1（`2212.06817`，RSS'23）、原始 BC | 单步连续动作 |
| **A2 动作块（action chunking）** | 2023 | **ACT（`2304.13705`，RSS'23）首提"一次出 k 步"**，解决"单步决策的时间不一致" | ACT（k 步 + CVAE） | 动作块（k 步） |
| **A3 生成式动作头** | 2023–2025 | **Diffusion Policy（`2303.04137`，RSS'23 / IJRR'24）把动作块交给扩散去噪** | Diffusion Policy、Octo、CogACT、DexVLA、GR00T N1（扩散）；π0、FLOWER、SmolVLA、GR-3（**flow matching**） | 动作块 + 扩散 / 流匹配 |
| **A4 VLM 底座 + 动作头** | 2023–2026 | **RT-2（`2307.15818`，CoRL'23）把动作当文本 token**；**π0（`2410.24164`，RSS'25）改用流匹配动作专家** | 离散 token 派：RT-2、OpenVLA、π0-FAST；连续头派：π0、OpenVLA-OFT、SpatialVLA | 动作 token **或** 动作块 |

**⚠ 一处需要纠正的常见说法**：**"动作 token → 动作块 → 连续动作头"这个顺序在 VLA 血统里成立，但在整个具身侧不成立**——**动作块（ACT）与生成式连续头（Diffusion Policy）同在 2023 年出现，是并行而非先后**；VLA 血统**滞后一年**（RT-2 与 OpenVLA 都还是**离散 token、单步自回归**）。真正的转折点是 **π0（RSS'25）与 OpenVLA-OFT（RSS'25）**：OFT 论文原文即把"AR 单步"列为瓶颈（"3-5 Hz … too slow for 25-50+ Hz"），并证明**连续 L1 回归 ≈ 扩散且更快**。π0-FAST 是离散路线的**最后一次自我修正**（用 DCT 压缩 token，而非简单分箱）。

### 线 B：世界模型（3 段）

| 段 | 时期 | 分界标志 | 代表 | 与策略的耦合 |
|---|---|---|---|---|
| **B1 潜空间想象 rollout** | 2018–至今 | **World Models（`1803.10122`，NeurIPS'18）** → PlaNet（ICML'19）→ Dreamer v1/v2/v3 | Dreamer v3（**Nature 2025**，DOI `10.1038/s41586-025-08744-2`）、**TD-MPC2（ICLR'24）**、DINO-WM | 在学到的潜动力学里想象 → 学策略 / 做 MPC |
| **B2 可交互生成环境** | 2023–2026 | **UniSim（`2310.06114`，ICLR'24 oral）与 Genie（`2402.15391`，ICML'24）** | Genie / Genie 2 / Genie 3、iVideoGPT、Genie Envisioner、Cosmos、Wan | 当"可玩的生成环境" → 造数据 / 训策略 |
| **B3 联合训练** | 2025–2026 | 动作与未来帧**互相促进** | **WorldVLA（`2506.21539`）**、**DiWA（CoRL'25）**、**Dreamer 4（`2509.24527`）** | 联合优化世界模型与策略 |

**⚠ 两处需要纠正的常见说法**：
1. **"重建 → 预测 → 对比"这个顺序不成立**。成立的只有前半段：**重建主导 2018–2023**（Dreamer v3 仍带像素解码器）；**转折点是"特征预测"**——**V-JEPA（`2404.08471`，2024-02）**摘要明示 "without the use of … reconstruction"，**DINO-WM（`2411.04983`，2024-11）**明示 "without reconstructing the visual world"。**"对比"不是后一阶段，而是自 2020 年起的平行支线**（C-SWM `1911.12247` ICLR'20、DreamerPro、ReCoRe），VPP（`2412.14803`，ICML'25 Spotlight）摘要把"单图重建"与"双图对比"**并列为"此前范式"**。
2. **"潜空间 rollout 已被生成式环境取代"不成立**——它是**分化而非取代**：**生成式环境服务"仿真与数据生成"，潜空间 rollout 服务"决策优化"**；**Dreamer 4（2025）把两者合流**（在视频世界模型内部做潜 rollout，Minecraft 实时）。TD-MPC2（ICLR'24）与 DINO-WM 仍在走潜空间路线。

## 2. 关键转移：每次解决了什么、留下什么

| 转移 | 解决了 | 留下的问题 |
|---|---|---|
| 单步回归 → **动作块** | 时间不一致、高频抖动 | **块长度成了超参**（DP 的 `Tp=16/Ta=8`、π0 的 `H=50`）；块越长、闭环反应越慢 |
| 动作块 → **生成式动作头** | 多模态动作分布（同一观测有多个合理动作） | **推理成本**（扩散 10–100 步）；且**"扩散是否必要"始终没被干净回答**（见下） |
| 离散 token → **连续动作头** | 推理频率（OpenVLA 3–5 Hz → OFT 吞吐 26×） | **动作分箱 / token 化带来的精度损失**（π0-FAST 用 DCT 压缩是补丁） |
| 世界模型"当环境" → **联合训练** | 世界模型与策略目标不一致 | **谁带谁**（WorldVLA 是动作促未来帧、DiWA 是世界模型微调策略）未定 |

**一条最要紧的量化事实**：**"扩散 vs 回归"的受控对照在具身侧有，但结论是"差不多"**——**OpenVLA-OFT 证明连续 L1 回归 ≈ 扩散且更快**；**RDT-1B 的 `regress` 变体去掉扩散后大幅掉分**（真机 50→12.5 / 62.5→50 / 100→12.5）；**FLOWER 的受控消融直接比较 flow / L1 / 离散 token**。→ **结论依任务而定，不存在"扩散一定更好"**。这与自动驾驶侧的发现**方向一致**：**SpanVLA 的"回归头 → flow matching"是 +5.2 PDMS**（受控），**但 OpenVLA-OFT 在具身侧给出的是相反证据**。

## 3. 与自动驾驶的接口差异（**本项目对自动驾驶侧最有价值的输出**）

同名技术（扩散策略 / VLA / 世界模型）在两个领域里**不是同一个东西**。逐维对照（数字均给出处；标注"摘要级"者为论文自述未核验）：

### 3.1 输出形式与动作空间

| 维度 | 具身侧 | 自动驾驶侧 |
|---|---|---|
| 单步动作维度 | **7–32 维**（π0 `action_dim=32` 含 padding；Consistency Policy 10/13 维；DP3 4–52 维；**RDT-1B 128 维统一动作空间**） | **2–3 维**（每个 pose 是 `(x, y, heading)`） |
| 动作块长度 | DP `Tp=16/Ta=8`（代码里 22 个配置有 14 个取 8）、π0 `H=50`、Consistency 16 | NAVSIM **8 poses @2 Hz**；nuScenes **6 步 @2 Hz**；nuPlan **80 步 @10 Hz** |
| 有没有"轨迹"这个概念 | **没有独立轨迹层**（Diffuser 生成的是状态-动作序列，不是规划轨迹） | **输出本身就是轨迹** |
| → 判断 | **维度结构相反**：具身是"**高维瞬时动作**"，驾驶是"**低维长序列**"。**两者没有共享的接口**，任何"搬运"都必须经过一次语义转换 | |

### 3.2 延迟与控制频率

| 具身侧 | 频率 / 延迟 | 驾驶侧 | 频率 / 延迟 |
|---|---|---|---|
| DiffuserLite | **122 Hz**（0.008–0.020 s） | MeanFuser | **59 FPS** |
| ACT | **50 Hz** | DiffusionDrive | **45 FPS** |
| GR00T N1（System 1） | **120 Hz**；16 步 chunk **63.9 ms**（L40）。⚠ **频率有 120 Hz 与 30 Hz 两说**，见论文表 DP-E22 | Diffusion Planner（DP-A01） | **约 20 Hz**（8 s @10 Hz 耗时 0.05 s） |
| Consistency Policy | 真机 **15 Hz**；CP(1) **1 ms**、CP(3) 2 ms（DDPM 110 ms） | WoTE | **18.7 ms** |
| Diffusion Policy | 真机 **10 Hz**（插值 125 Hz）；3080 上 0.1 s（10 步） | GuideFlow | **3.6 FPS** |
| RDT-1B | chunk 推理 **6 Hz** | **PC-Diffuser（去噪内 CBF-QP）** | **约 2 fps**（5× vanilla） |
| OpenVLA | **3–5 Hz**（A100） | FeaXDrive | 348.73 ms（VLM 占 70.3%） |
| RT-2 | 330–1000 ms（**<3 Hz**，二手来源） | DiffusionDriveV2 / HDP | **未取得** |

**→ 判断**：**无约束时两边同量级**（10–100 Hz），**频率本身不是障碍**（驾驶侧已用 2 步截断与 1 步 MeanFlow 达标）。**但一旦加硬约束，驾驶侧掉到 2–4 fps，而具身侧的 CBF 方案仍在毫秒级**（SafeFlowMatcher 的 S-TIME **4.71 ms**）——**差约 2 个数量级**。

**⚠ 一个必须避开的陷阱**：**π0 的"50 Hz"是"执行 chunk 的控制频率"，不是模型前向频率**（20 Hz 重规划时执行 16/50 步）。**具身侧 VLA 的真实推理频率普遍在 5–15 Hz**，与驾驶侧 ≥10 Hz 的余量**很小**。

### 3.3 安全约束与失败代价

| 侧 | 硬约束代表 | 机制 | 结果 |
|---|---|---|---|
| 具身 | **SafeFlowMatcher**（`2509.24243`） | flow matching + **CBF-QP，只对执行路径逐路点施加**，有前向不变性定理 | S-TIME **4.71 ms**；但**只在 Maze2D / Walker2D / Block Stacking 等低维域** |
| 具身 | SafeDiffuser（基线） | 约束加在**中间隐状态** | **Trap Rate 72%**（"看起来安全"） |
| 驾驶 | **PC-Diffuser**（DP-A21） | **去噪内逐路点 CBF-QP**，带证书 | 碰撞率 **100% → 10.29%**；代价 **5× / 约 2 fps** |
| 驾驶 | **GuideFlow**（DP-A12） | 速度偏置（实为朝专家轨迹的常数偏置） | navhard EPDMS 43.0 |
| 驾驶 | **SafeAuto**（VLA-05） | **MLN 一阶逻辑否决层**（否决 = 重新 prompt） | MLN 边际仅 **~1.2 个准确率点**，**无碰撞率、无闭环** |
| 驾驶 | **FeaXDrive**（DP-A18） | 曲率界 + SDF 软引导 | 曲率违规 **0.88%** vs DiffusionDrive 8.59% |

**→ 判断：不是同一类问题。** 具身侧的"安全"是**低维 toy 域的约束满足**（Trap Rate），代表工作**都不在真机高维**；驾驶侧的"安全"是**碰撞（乘性惩罚归零）+ 运动学可行性**。**具身的失败 = 没抓到（成功率）**，**驾驶的失败 = 撞车（NC/DAC 归零）**。→ **SafeDiffuser 的"Trap Rate 72%"在驾驶语境下没有对应量**。

### 3.4 评测口径

| 侧 | 基准 | 主指标 | 有"安全违规率"吗 |
|---|---|---|---|
| 具身 | LIBERO、SimplerEnv、RoboMimic、ManiSkill2、CALVIN | **成功率**（二值任务完成） | **常规基准没有**；只有 SafeFlowMatcher 自设 Trap / Barrier |
| 驾驶 | NAVSIM PDMS/EPDMS、nuPlan 闭环、Bench2Drive DS/SR/IS、nuScenes 开环 | PDMS = `(NC × DAC) × [加权项]`，**含碰撞率且乘性归零** | **有** |

**→ 不能互相借用**：PDMS 是"碰撞乘性归零 × 进度/舒适加权"，具身成功率是"任务完成二值量"，**结构不同**；且驾驶侧数字**跨论文不可横比**（见 [benchmarks.md §2](../../autonomous-driving/direction/benchmarks.md)）。

### 3.5 输入与预测表示

| 维度 | 具身侧 | 自动驾驶侧 |
|---|---|---|
| 输入 | **低维本体状态** + **egocentric RGB 视频流** + 语言指令 | **多传感器（相机 + LiDAR）→ BEV / 矢量化 map+agent** |
| 有无固定 ego 坐标系 | **无**（靠第一视角视觉流） | **有**（自车坐标系 + HD map） |
| "未来"是什么 | **物体 / 接触的演化**（需 3D / 接触建模） | **BEV 占据 / agent 轨迹** |
| 世界模型是否 action-conditioned | **普遍是**（Genie 用无监督潜动作；NWM / UniSim 直接吃动作） | **多以 ego 轨迹 / 导航命令为条件** |

## 4. 哪些差异决定了"不能直接迁移"

**分两类，判断不同**：

| 类别 | 具体差异 | 能否靠工程解决 |
|---|---|---|
| **量级差异** | 推理频率（具身 10–122 Hz vs 驾驶 45–59 FPS）、动作块长度、少步化步数 | **能**——驾驶侧已用 2 步截断（DiffusionDrive）与 1 步 MeanFlow（MeanFuser）达标 |
| **结构差异** | ① **输出语义**（高维瞬时关节动作 vs 低维长序列轨迹，**无共享接口**）② **约束位置与代价**（驾驶需碰撞/运动学硬约束且加约束后掉 2 个数量级；具身硬约束只在低维 toy 域）③ **评测结构**（成功率 vs PDMS，**指标不可互换**） | **不能**——只能重新定义接口，不能"平移" |

→ **结论**：**"具身侧有现成的动作头可以搬"这句话只在"动作头这一层"成立，且必须经过一次语义转换（关节动作 → BEV 路点）**；**而"安全约束""评测口径""控制频率"三层不能搬**。

## 5. 已发生的迁移实证（"能不能搬"已被回答为"已经有人在搬"）

| 工作 | 搬了什么 | 搬到哪一层 | 结果 |
|---|---|---|---|
| **DriveMoE**（VLA-04，`2505.16278`） | **底座就是 π0**（论文 §3.1 标题即 "Drive-π0 Baseline"），复用其 **flow matching 动作头** | VLM + 动作头 → 驾驶轨迹层 | 输出 10 waypoint；Bench2Drive **DS 74.22 / SR 48.64%**；**无官方仓库** → **⚠ 第七十一轮更正：官方仓存在**（[Thinklab-SJTU/DriveMoE](https://github.com/Thinklab-SJTU/DriveMoE)，235★） |
| **VaViM/VaVAM**（VLA-22，`2502.15672`） | 与具身 VLA 同构的 **flow matching 动作头 + 逐层 joint attention** | 视频-动作模型 → 6 waypoint @2 Hz | **主干 VaViM 被冻结**（`requires_grad_(False)`，**论文未声明**）；NeuroNCAP 碰撞 57.9%（闭式口径）；**无受控消融** |
| **DriveLaW**（WM-11，`2512.23421`） | `action_expert: true` + `num_inference_steps: 5` —— **与 π0 的 action expert 同构**（接口 A） | 世界模型视频 transformer **内部** | Table 5：BEV 84.1 → 视频潜状态 **89.1（+5.0 PDMS）**；接口 B 的"喂给谁"是**死引用、未发布** |
| **ReCogDrive**（DP-A28，`2506.08052`） | VLM + 扩散规划器（DriveLaW 的上游） | 语言 → 扩散规划器 | NAVSIM **90.8**（RL 阶段 +4.3） |

**两条判断**：
1. **π0 的 flow matching 动作头已经搬进驾驶（DriveMoE / DriveLaW），收益在 +3 ~ +5 PDMS 量级**——**与"换动作头 +5.2 / 加 goal 条件 +4.7"同量级** → **具身动作头不是更大的收益维度**。
2. **"联合训练"多名义不符**：**VaVAM 冻结主干**（论文未声明）、**DriveLaW 的论文只讲接口 B 而代码默认接口 A** → **搬运过程中"声称端到端、实际冻结/外挂"是常见形态**，引用前必须核代码。

**未找到的工作**：**"在机器人数据上预训练后独立迁移到驾驶"没有实例**（DriveMoE 是"直接以 π0 为底座"的最接近形态）；**"在驾驶数据上训 LIBERO 式动作块"亦未找到**。

## 6. 继承关系（论文 / README 级，无代码核验）

本页约定"写判断、事实留表与笔记"，故本节只写**血统判断 + 指针**，不复制论文表。强度分级 S1–S4 见 [workflows.md §代码脉络梳理](../../../ai/workflows.md)。

- **策略动作线（线 A）是一条清晰的继承链**：`BC → ACT（首提动作块）→ Diffusion Policy / π0`。其中 **Diffusion Policy 直接把 ACT 的动作块交给扩散去噪**；**RT-2 把"动作当文本 token"、OpenVLA 把它开源化、π0 用 flow matching 动作专家取而代之**（见 §1 线 A 与 [VLA 小方向脉络](../topics/vla/lineage.md)）。
- **世界模型线（线 B）同理清晰**：`World Models（NeurIPS'18）→ PlaNet → Dreamer v1/v2/v3`（潜 rollout）→ **V-JEPA / DINO-WM 的"去重建"** → **WorldVLA / DiWA / Dreamer 4 的"联合训练"**（见 §1 线 B）。
- **π0 是两条线之外、跨领域共用的枢纽**：驾驶侧的 **DriveMoE 以 π0 为底座**、**DriveLaW 的 `action_expert` 与 π0 同构**（见 §5）——**这是具身 → 驾驶唯一的成体系血统转移**。
- **一处代码级硬继承（S1）**：**VaVAM = VaViM（视频预训练主干）+ flow matching 动作专家**，且代码**冻结 VaViM**（论文未声明，见 §5 与 [vla papers.md VLA-22](../../autonomous-driving/topics/vla/papers.md)）。

## 7. 待补

- **全文级证据**：本页数字多数为**摘要级 + 论文自述**（具身侧 14 篇 VLA 与 14 篇世界模型**均未读全文**）；驾驶侧数字引自本工作空间已核验的论文表与代码脉络。
- **未取得的关键数字**：**DP3 的控制频率**；DiffusionDriveV2 / HDP 的 FPS。
  - **⚠ 更正（第二十九轮）**：原列 **RDT-1B / FLOWER / π0.5**，但三者频率**已登记**——RDT-1B 见本页 §3.2「chunk 推理 **6 Hz**」，FLOWER（DP-E14）与 π0.5（DP-E20）见[扩散策略论文表](../topics/diffusion-policy/papers/diffusion_planner_embodied.md)。注意其中的 "50 Hz" 是**执行动作块的控制频率**，不是模型前向频率（见本页 §3.2 末的陷阱）。
- **可深化**：具身侧"世界模型 + 扩散策略"的**接口**（本页第 3.5 节的最后一问）尚未有代码级证据。
