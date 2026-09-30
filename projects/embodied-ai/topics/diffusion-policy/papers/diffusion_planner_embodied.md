# 具身智能与通用决策中的扩散规划器 / 策略（2022–2026）

更新时间：2026-09-22  
检索对象：次方向。包含三类：(1) 通用决策与离线 RL 中的扩散规划器；(2) 机器人扩散策略；(3) 导航与 VLA 生成式动作头。  
编号规则：`DP-Exx`（Diffusion Planner – Embodied / general decision-making）。自动驾驶侧见 [diffusion_planner_ad.md](../../../../autonomous-driving/topics/diffusion-planner/papers/diffusion_planner_ad.md)（`DP-Axx`），综述见 [diffusion_planner_surveys.md](../../../../autonomous-driving/topics/diffusion-planner/surveys/diffusion_planner_surveys.md)（`DP-Sxx`）。

## 纳入与证据规则

- 纳入：生成过程用于**动作或轨迹决策**的工作。纯感知、纯图像生成不纳入。
- 证据状态：**术语与定义见 [ai/rules.md](../../../../../ai/rules.md) §证据等级**——`元数据`、`摘要`、`全文`（arXiv HTML 或 PDF + `pdftotext -layout` 逐表核对）、`代码静态检查`（**须再标 L1 逐文件 / L2 仓库存在性 / L3 API+raw 未克隆**）、`成功运行`、`独立复现`。**此前本表用的"未获取"不是标准档位**（2026-09-23 第二十六轮更正），凡只拿到标题/作者者一律记 `元数据`。
- **本表已知的代码级核验**：**DP-E19（π0）为 L1**（`openpi` 已克隆至 [code/repos/openpi](../../../../autonomous-driving/code/repos)，核验见 [transfer.md §1.4](../../../../autonomous-driving/topics/diffusion-planner/transfer.md)）；**DP-E01（Diffuser）、DP-E09（Diffusion Policy）、DP-E10（DP3）、DP-E17（NoMaD）为 L1**（仓库已落盘，核验见 [transfer.md §1](../../../../autonomous-driving/topics/diffusion-planner/transfer.md)）；**DP-E05/E06/E07/E08 的代码可用性已核**（见各行"代码"列）。
  - **⚠ 更正（第二十九轮）**：本行原写 `DP-E08（SafeFlowMatcher）…为 L1`，**实为 `DP-E01`**——`transfer.md` 列出的 4 个落盘仓库是 `diffuser / diffusion_policy / 3D-Diffusion-Policy / visualnav-transformer`，对应 DP-E01/E09/E10/E17。**DP-E08 无公开仓库**（论文只给匿名 supplementary），不可能为 L1；原文与该行"代码"列、与笔记 `DP-E08-safeflowmatcher.md` 三处互相矛盾。
- 编号按加入顺序分配，不保证与分组顺序一致。
- 自动驾驶侧的重复条目只在 AD 表中保留指针，完整登记在本表，避免两处各写一份。

## A. 通用决策与规划（离线 RL / 长时程）

| ID | 论文 | 作者（首位） | 载体与版本 | 生成机制 | 输出与基准 | 代码 | 可迁移机制 | 证据状态 |
|---|---|---|---|---|---|---|---|---|
| DP-E01 | [Planning with Diffusion for Flexible Behavior Synthesis](https://arxiv.org/abs/2205.09991)（Diffuser） | Michael Janner | ICML 2022（长报告）；arXiv v2 | 对整条轨迹（状态-动作联合）迭代去噪；**classifier guidance**（Eq.3，引导尺度 α=0.1，Hopper-medium-expert 用 0.0001）+ inpainting 约束首末状态；horizon T=32（locomotion）/128（stacking）/128–384（Maze）；步数 N=20/100 | 状态-动作轨迹；Maze2D **113.9/121.5/123.0** vs MPPI 33.2/10.2/5.1、CQL 5.7/5.0/12.5（Table 1）；D4RL 平均 77.5（Table 2）；堆叠 58.7/45.6/58.9 vs BCQ 0.0（Table 3） | [jannerm/diffuser](https://github.com/jannerm/diffuser) | 引导式约束（可微目标写进采样）；长时程联合去噪减少复合误差。**关键负结论**：把它当纯 dynamics model 塞进 MPPI"performed no better than random"（§5.3）→ 价值在"建模与规划耦合"而非预测精度 | 全文（PDF，逐表核对） + [笔记](../notes/DP-E01-diffuser.md) |
| DP-E02 | [Is Conditional Generative Modeling all you need for Decision-Making?](https://arxiv.org/abs/2211.15657)（Decision Diffuser） | Anurag Ajay | ICLR 2023；arXiv v4 | **只扩散状态序列**，动作由逆动力学 a_t=f_φ(s_t,s_{t+1}) 给出；CFG（Eq.8，ω∈{1.2–1.8}）+ 多条件组合（Eq.9）+ NOT 组合；K=100 步；horizon 100/56/128 | 状态序列；D4RL 平均 **81.8** vs Diffuser 75.3（Table 1）；Hopper-m 79.3 vs CondDiffuser 66.3（Table 2）；约束任务 58.0/62.7 vs Diffuser 45.6/58.9（Table 3） | [anuragajay/decision-diffuser](https://github.com/anuragajay/decision-diffuser) | 多条件在测试期组合（约束 + 技能）；**附录 K 论证 CFG 优于 Q 引导**（离线 Q 会高估 OOD 动作）；**去动作扩散 + 逆动力学在 3 个环境全部提升**，动作越不平滑收益越大。局限：不支持部分可观测、随机动力学下退化（附录 M） | 全文（PDF，逐表核对） |
| DP-E03 | [Diffusion Policies as an Expressive Policy Class for Offline Reinforcement Learning](https://arxiv.org/abs/2208.06193)（Diffusion-QL） | Zhendong Wang、Jonathan J Hunt、Mingyuan Zhou | ICLR 2023；arXiv v3（2022-08 首发） | 条件扩散作用于**动作空间**（状态为条件）；**训练期 Q 引导** L=L_d(θ)−α·E[Q_φ(s,a⁰)]，梯度穿过整条扩散链；N=5 步（D4RL 默认） | 单步动作；D4RL 平均 **88.0**（Gym 88.0/AntMaze 69.6/Adroit 65.1/Kitchen 69.0，Table 1）；消融：Diffusion-QL 106.9 ≫ CVAE-QL 76.6、BC-Diffusion 85.9 > BC-CVAE 79.9（Table 2）；N∈{2,5,10,20}，N=5 已足够（Fig.2/3） | [Zhendong-Wang/Diffusion-QL](https://github.com/Zhendong-Wang/Diffusion-QL) | 表达力（扩散）与 Q 引导缺一不可；是"离线 RL 微调生成式策略"的早期范式 | 全文（PDF，逐表核对） |
| DP-E28 | [Efficient Diffusion Policies for Offline Reinforcement Learning](https://arxiv.org/abs/2305.20081)（EDP） | Bingyi Kang | NeurIPS 2023；arXiv v2 | 策略=DDPM 反链；**action approximation** 一步构造 â⁰（Eq.9）+ DPM-Solver 把采样 1000→**15 步**；目标=L_diff（Eq.5）+ Q 引导 L_π=−E[Q(s,â⁰)]（Eq.10）；另给兼容 IQL/CRR 的似然版 | 单步动作；D4RL 全域（Table 2）；消融：action approximation 训练 2.3×/采样 3.3×，DPM-Solver 再省 2.3×训练，DQL(JAX) 比 DQL 快 5×；K=1000 优于 5–100（Table 1） | [Zhendong-Wang/Diffusion-QL](https://github.com/Zhendong-Wang/Diffusion-QL) | 早期扩散策略的**训练/采样效率**方案（训练 5 天→5 小时）。**注意**：此 ID（2305.20081）常被误标为 Diffusion-QL，两者不同（Diffusion-QL=2208.06193），本表已分列 | 全文（PDF，逐表核对） |
| DP-E04 | [DiffuserLite: Towards Real-time Diffusion Planning](https://arxiv.org/abs/2401.15443) | Zibin Dong | NeurIPS 2024；arXiv v5 | 状态序列 + 3 级"规划精化过程"（PRP，粗到细），temporal jump 32/8/1 与 16/4/1；逆动力学出动作；CFG（Eq.6）只加在最粗一级；扩散 3–5 步 | 轨迹；MuJoCo 平均 **122.44 Hz**（runtime 0.008–0.020 s），对比 Diffuser 1.5 Hz/0.665 s、Decision Diffuser 0.47 Hz/2.142 s（Table 1）。消融：仅末级 84.1%↓、无 PRP 27.1%↓、DD-small 72.3%↓（Table 7）；2 层在 Antmaze 掉到 0.0，需 3–4 层（Table 6） | 见论文项目页（未核验） | **PRP 与足够 horizon 最关键**；插件式提升频率 560% 而性能仅降 3.2%（Table 5）——是"粗到细"路线的最强证据 | 全文（PDF，逐表核对） + [笔记](../notes/DP-E04-diffuserlite.md) |
| DP-E05 | [Dichotomous Diffusion Policy Optimization](https://arxiv.org/abs/2601.00898)（DIPOLE） | Ruiming Liang | arXiv v3（2025-12） | 从 KL 正则目标导出加权回归形式，稳定优化扩散策略，避免高斯似然近似 | 通用决策/离线 RL | **有代码，但主仓是占位**——真代码在 git submodule [Whiterrrrr/dipole-rl](https://github.com/Whiterrrrr/dipole-rl)（2026-09-23 核验；明细见 [AD 表 DP-A17](../../../../autonomous-driving/topics/diffusion-planner/papers/diffusion_planner_ad.md)） | **（= AD 表 DP-A17）** 扩散策略 RL 微调的稳定性结论，可直接用于驾驶规划器后训练 | 元数据 + 摘要 + **代码可用性已核（L2）** |
| DP-E06 | [Model-Based Diffusion Sampling for Predictive Control in Offline Decision Making](https://arxiv.org/abs/2512.08280)（MPDiffuser） | Haldun Balim | arXiv v3（2025-12） | 规划器扩散 + 动力学扩散交替采样，逐步修正可行性；轻量排序模块选轨迹 | 通用离线控制 | **有代码**：[haldunbalim/MPDiffuser](https://github.com/haldunbalim/MPDiffuser)（2026-09-23 核验；**权重与数据均不可得**，两条 CLI 路径在代码里就是坏的 → 只能作机制参考，明细见 [AD 表 DP-A23](../../../../autonomous-driving/topics/diffusion-planner/papers/diffusion_planner_ad.md)） | **（= AD 表 DP-A23）** 让动力学模型参与去噪，把可行性注入生成过程（非梯度方式） | 元数据 + 摘要 + **代码可用性已核（L3）** |
| DP-E07 | [Decoupled Guidance Diffusion for Adaptive Offline Safe Reinforcement Learning](https://arxiv.org/abs/2605.02777)（SDGD） | Rufeng Chen | arXiv v2（2026-05） | 把自适应安全生成重解释为受约束分布采样，用 cost limit 条件化 CFG，解耦奖励与约束梯度 | 通用离线安全 RL | **未找到官方代码**（2026-09-23 核验：arXiv HTML v1/v2 全文与 OpenReview `GDlLS3ytBI` 均无代码链接或可用性声明，明细见 [AD 表 DP-A24](../../../../autonomous-driving/topics/diffusion-planner/papers/diffusion_planner_ad.md)） | **（= AD 表 DP-A24）** "安全预算作为条件输入"对应驾驶中可调风险偏好 | 元数据 + 摘要 + **代码可用性已核（无官方代码）** |
| DP-E08 | [SafeFlowMatcher: Safe and Fast Planning using Flow Matching with Control Barrier Functions](https://arxiv.org/abs/2509.24243) | Jeongyong Yang | ICLR 2026 poster；arXiv v3 | 流匹配 + CBF：两阶段"预测-校正"积分器；校正阶段用消失时间缩放向量场 + CBF-QP，对**执行路径逐路点**施加硬约束，仅 CFM 损失、无 RL | 路径；Maze2D、Walker2D/Hopper、Block Stacking。主结果 Score 1.632±0.003 / Trap 0% / S-TIME 4.71 ms；无约束的 FlowMatcher 1.632 / 3.51 ms；RES-SafeDiffuser **Trap 72%**（Table 1） | **无公开仓库**（2026-09-23 核验：论文 Reproducibility 段只给**匿名 supplementary**，未公开到 GitHub；勿与同作者的 SafeFlow `2504.08661` 混淆。明细见 [AD 表 DP-A20](../../../../autonomous-driving/topics/diffusion-planner/papers/diffusion_planner_ad.md)） | **（= AD 表 DP-A20）** 给出认证级硬约束（定理 1 前向不变、命题 1 有限时间收敛）；代价是校正步与 QP（闭式平均 1.14 ms）。**注意**：驾驶域的同类工作见 AD 表 DP-A21（PC-Diffuser，逐去噪步 CBF-QP + Thm.1/Cor.1） | 全文（HTML + PDF 表格核验） + [笔记](../notes/DP-E08-safeflowmatcher.md) |

## B. 机器人扩散策略

| ID | 论文 | 作者（首位） | 载体与版本 | 生成机制 | 输出与基准 | 代码 | 可迁移机制 | 证据状态 |
|---|---|---|---|---|---|---|---|---|
| DP-E09 | [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137) | Cheng Chi | RSS 2023 扩展版（IJRR 体例）；arXiv v5 | DDPM 条件去噪，视觉作条件而非联合；训练 100 步 / 推理 10 步；action chunk = 预测 Tp 步、执行 Ta 步（receding horizon） | 位置/关节动作块；4 个基准 12 任务，摘要称平均提升 46.9% | [real-stanford/diffusion_policy](https://github.com/real-stanford/diffusion_policy) | receding horizon action chunk；位置控制优于速度控制；执行步长 Ta 存在"一致性-响应性"权衡（全文称 Ta=8 最优） | 全文（HTML，逐节提取）+ 摘要 + [笔记](../notes/DP-E09-diffusion-policy.md) |
| DP-E10 | [3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations](https://arxiv.org/abs/2403.03954)（DP3） | Yanjie Ze | RSS 2024；arXiv v7 | 稀疏点云 + 轻量点编码器作为条件；DDIM 100→10 步 | 末端/关节动作序列；72 仿真任务 + 4 真机任务，摘要称仿真相对提升 24.2%、真机平均 85% | [YanjieZe/3D-Diffusion-Policy](https://github.com/YanjieZe/3D-Diffusion-Policy) | 3D 表示比 RGB/RGB-D/voxel 更有效，且**简单编码器已足够**。**⚠ 更正（第二十九轮）**：本表与笔记原写"**3 层 MLP** > PointNeXt/Point Transformer"，但代码实测编码器为 **4 层 Linear**（`in→64→128→256→512`）+ 全局 max-pool，输出仅 **64 维**；仓库的 "simple" 变体改的是 **U-Net 宽度**（512/1024/2048 → 128/256/384），**不是编码器层数**——见 [transfer.md §1.1](../../../../autonomous-driving/topics/diffusion-planner/transfer.md) | 全文（HTML，逐节提取）+ 摘要 + **代码静态检查（L1）** + [笔记](../notes/DP-E10-dp3.md) |
| DP-E11 | [Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation](https://arxiv.org/abs/2405.07503) | Aaditya Prasad | arXiv v2（2024-05）；正文未标注会议 | 从 EDM teacher 蒸馏出自一致性 student（CTM）：单步 z~N(0,I) 直接出 x，或 3 步 chaining；初始方差 N(0,1/T²)；**无引导/约束**（纯模仿） | action chunk=16（每步 10D；移动任务 13D）；真机 Franka 策略 **15 Hz**。ToolHang 单步 0.70 / 3 步 0.77（DDPM 0.79、DDiM 0.14，Table I）；**延迟：DDPM(100 NFE) 110 ms、DDiM(15) 11 ms、CP(1) 1 ms、CP(3) 2 ms**（Table III）；真机 DDiM 192 ms vs CP 21 ms（Table XI） | 见项目页（未核验） | 一致性蒸馏的加速路径（与少步截断、MeanFlow 互为替代）；**关键设计**：一致性目标、降低初始方差、预设 chaining 步、dropout（Table V–IX） | 全文（PDF，逐表核对） + [笔记](../notes/DP-E11-consistency-policy.md) |
| DP-E12 | [Equivariant Diffusion Policy](https://arxiv.org/abs/2407.01812) | Dian Wang | CoRL 2024 Oral；arXiv v3 | 利用 SO(2) 对称性做等变去噪（Prop.1/2）；条件扩散、起点高斯；训练 100 步 / 评估 DDIM 16 步；**无引导/约束** | 6-DoF 动作（绝对/相对位姿），action chunk n 步；真机 5 Hz。EquiDiff(Vo) 63.9/72.6/77.9 vs DiffPo-C 42.0/57.8/71.4（100 demos 平均 **+21.9%**，Table 2）；真机 20–60 demos 下 80–95% vs 基线 0–60%（Table 3） | 未核验 | 消融显示**等变结构比 voxel 表示更重要**（去等变 −17.6 vs 去 voxel −10.3，Table 7/8）。局限（§6）：道路结构/目标语义非旋转不变，未扩展到导航与运动 | 全文（PDF，逐表核对） |
| DP-E13 | [Diffusion Transformer Policy](https://arxiv.org/abs/2410.15959) | Zhi Hou | arXiv v6（preprint） | 用大 DiT 直接去噪 action chunk，替代小动作头 | 动作块；ManiSkill2/LIBERO/Calvin/SimplerEnv | 见项目页（未核验） | "大 Transformer 去噪动作块"与"小动作头"的容量之争 | 元数据 + 摘要 |
| DP-E14 | [FLOWER: Democratizing Generalist Robot Policies with Efficient VLA Flow Policies](https://arxiv.org/abs/2509.04996) | Moritz Reuss | CoRL 2025；arXiv v1 | 中间模态融合（剪掉至多 50% LLM 层）+ 动作专用 Global-AdaLN 条件（-20% 参数），流匹配动作头 | 连续动作块；10 个基准 / 190 任务 | **⚠ 链接已更正（第二十五轮）**：原记的 `intuitive-robots/flower_vla` **是 404**，实为 `flower_vla_pret` / `flower_vla_calvin` 两个仓 | 高效流动作头的容量分配策略，对应驾驶侧推理预算受限场景。**第二十五轮补全**：CALVIN ABC **4.53（SoTA）**、LIBERO-Long **93.4%**；受控消融 **中间融合 vs 早融合 93.4% vs 33.4%**、Global-AdaLN vs AdaLN、**flow vs L1 vs 离散 token 三路对照**；Aloha 仿真 **50 Hz**、chunk=20；⚠ **"4.53" 是平均序列长度，不是成功率** | 元数据 + 摘要（第二十五轮补全字段） |
| DP-E15 | [Diffusion Policy Policy Optimization](https://arxiv.org/abs/2409.00588)（DPPO） | Allen Z. Ren | arXiv v3（2024-12） | 把去噪链嵌入环境 MDP（"双层 MDP"），用 PPO 策略梯度微调；预训练 BC（K=20 状态 / 100 像素），微调**最后 10 步**或 5 步 DDIM；优势含去噪折扣 γ_DENOISE | action chunk Ta=4（Gym/Kitchen）、4/8（Robomimic）；真机 10 Hz（底层阻抗控制 1 kHz）。**值估计只依赖 state 最关键**；微调 K′=10 最省（K′=3 次优）；状态/像素下均超 Gaussian/GMM（Transport >90%，首个 >50%）；真机 One-leg **DPPO 80%(16/20) vs Gaussian 0%** | 见项目页（未核验） | "BC 预训练 + 在线 RL 微调"对驾驶长尾最有参考价值；代价是样本效率低于 off-policy 方法（§7），且需要在线/高保真仿真交互 | 全文（PDF，逐表核对） + [笔记](../notes/DP-E15-dppo.md) |
| DP-E16 | [Freeze, Share, Shrink: Rethinking the Action Backbone in Diffusion Policies](https://arxiv.org/abs/2511.12101) | Jian Zhou | arXiv v3（2025-11，RSS2026-Diff4RL） | 在调制条件式扩散策略中把任务适配全部走条件通路，冻结与观测无关的骨干作为可复用轨迹先验 | 动作；LIBERO、MimicGen | **未发现任何官方仓库**（第二十五轮复查） | "冻结骨干 + 只训条件"可大幅省算力，对应驾驶中多城市/多车型适配。**第二十五轮补全**：**Stage 1 用"无观测正运动学（FK）对"预训练动作头**；MimicGen **63.6%**、LIBERO **79.3%**；**5M MLP 65.9% / 84.7% ≥ 244M U-Net**；**调制式 vs 注意力式：DP-T 冻结后 60.4→19.4、76.4→5.9 崩溃**；随机初始化骨干 = **0%**；⚠ **无代码 → 结论不可复现** | 元数据 + 摘要（第二十五轮补全字段） |

## C. 导航（与驾驶最接近）

| ID | 论文 | 作者（首位） | 载体与版本 | 生成机制 | 输出与基准 | 代码 | 可迁移机制 | 证据状态 |
|---|---|---|---|---|---|---|---|---|
| DP-E17 | [NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration](https://arxiv.org/abs/2310.07896) | Ajay Sridhar | arXiv v1（2023-10） | DDPM，起点高斯；目标图像以 Bernoulli 掩码（p=0.5）条件化，一个策略同时做目标导航与无目标探索；K=10 步、1D U-Net | 未来动作序列（导航 waypoint）；6 个环境，摘要称无向探索超子目标扩散基线 >25% | [robodhruv/visualnav-transformer](https://github.com/robodhruv/visualnav-transformer) | 与驾驶最接近：前视相机 + 目标条件 → 2D waypoint 序列；"目标掩码"使同一策略兼容有/无目标两种模式 | 全文（HTML，逐节提取）+ 摘要 + [笔记](../notes/DP-E17-nomad.md) |
| DP-E18 | [MulDP: Multimodal Diffusion Policy for Autonomous Quadruped Parkour Navigation](https://arxiv.org/abs/2609.03984) | Kangmai Hu | IROS 2026；arXiv v1（2026-09） | 视觉 + 本体感知 + 目标条件，扩散生成时序一致的导航速度指令 | 速度指令；四足跑酷地形 | 未核验 | 把"长时程预判行为"写进扩散策略，与驾驶的滚动规划同构 | 元数据 + 摘要 |

## D. VLA 与生成式动作头

| ID | 论文 | 作者（首位） | 载体与版本 | 生成机制 | 输出与基准 | 代码 | 可迁移机制 | 证据状态 |
|---|---|---|---|---|---|---|---|---|
| DP-E19 | [π0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164) | Kevin Black | arXiv v4（2024-10） | 条件流匹配（非 DDPM），高斯起点、线性高斯路径、前向 Euler 10 步；PaliGemma VLM + 300M 动作专家（论文称**总 3.3B**；**⚠ 更正（第二十九轮）**：代码实测配置为 `gemma_2b` + `gemma_300m` = **2.3B**，全仓 grep 不到 3.3B 的来源——见 [transfer.md §1.4](../../../../autonomous-driving/topics/diffusion-planner/transfer.md)）；action chunk H=50 | 连续动作块；7 机器人 68 任务 | [Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) | VLA + 流匹配动作头的标准配方；摘要/全文称 VLM 预训练与 action chunking 是关键 | 全文（HTML，逐节提取）+ 摘要 + **代码静态检查（见 [transfer.md §1.4](../../../../autonomous-driving/topics/diffusion-planner/transfer.md)）** |
| | | | | **代码级补充**：`src/openpi/models/pi0.py` 的 `compute_loss` 实测 `x_t = t·noise + (1−t)·actions`、`u_t = noise − actions`、损失 `mean((v_t−u_t)²)`、`sample_actions(num_steps=10)` → **流匹配三项声称完全一致**；`action_horizon=50`、`action_expert_variant=gemma_300m` 一致。**但"总 3.3B"在配置里读不到**（配置是 `gemma_2b` + `gemma_300m` = 2.3B）。**另四条代码细节**：① 时间采样是 **`Beta(1.5,1)`** 而非均匀（偏向噪声端，驾驶侧是均匀）；② 代码时间约定与论文相反，**作者自承**（`pi0.py:226-227` "t=1 is noise… yes, this is the opposite of the pi0 paper, and I'm sorry."）；③ **π0.5 的核心改动是"状态从连续输入变成离散语言 token"**（`pi0_config.py:29` 注释原文）+ `max_token_len` 48→200 + 动作专家启用 adaRMS；④ `action_dim=32` 是统一动作空间的 padding。 | | | | |
| DP-E20 | [π0.5: a Vision-Language-Action Model with Open-World Generalization](https://arxiv.org/abs/2504.16054) | Physical Intelligence | arXiv v1（2025-04） | 在 π0 上做异构任务协同训练 + 高层子任务预测 | 连续动作块；开放世界家庭任务 | 同 openpi | 协同训练提升分布外泛化，对应驾驶的跨城市/长尾泛化。**第二十五轮补全**：**预训练用离散 token（FAST）+ 后训练用流匹配专家**（混合式）；真机 **50 Hz** 动作块；400 h 数据（**97.6% 非移动**）；真机未见新家清洁 **10–15 min**；受控对照 **π0 vs π0-FAST+Flow vs π0.5**（no WD / ME / CE / VI / HL 五组）；⚠ **全部结果为图（Fig.8–13），无表格数字可核** | 元数据 + 摘要（第二十五轮补全字段） |
| DP-E21 | [RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation](https://arxiv.org/abs/2410.07864) | Songming Liu | arXiv v2（2024-10） | 扩散 Transformer 基础模型（1.2B）+ 物理可解释的统一动作空间（128 维） | 双臂动作；双臂操作基准 | [thu-ml/RoboticsDiffusionTransformer](https://github.com/thu-ml/RoboticsDiffusionTransformer)（+ HF 权重 `rdt-1b` / `rdt-170m`） | 统一动作空间是跨本体迁移的前提，对应驾驶中跨车型/跨数据集的输出表示统一。**第二十五轮补全**：**动作块 DDPM 去噪（DiT）**；chunk 推理 **6 Hz**；**控制频率作为显式输入特征**（兼容异构采样率）；真机 ALOHA：未见杯 **50%**、未见房间 **62.5%**、1-shot Fold **68%**（ACT / OpenVLA / Octo ≈ 0）；**受控消融：`regress` 变体去掉扩散后 50→12.5 / 62.5→50 / 100→12.5**；⚠ 表 2「指令跟随=100」与表 3「correct amount=75」**口径不一致** | 元数据 + 摘要（第二十五轮补全字段） |
| DP-E22 | [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734) | NVIDIA | arXiv v2（2025-03） | 双系统：VLM 做 System 2 慢推理 + 扩散 Transformer 动作头做 System 1 | 连续动作；人形机器人多任务 | [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)（+ HF 权重） | "慢推理 + 快生成"的分工，对应驾驶中 VLM 决策 + 扩散规划的分层。**第二十五轮补全**：动作头是**流匹配（DiT，Euler K 步）**而非纯扩散；**System 1 最高 120 Hz；16 步 chunk 63.9 ms（L40）**；**2.2B（VLM 1.34B）**；训练用**潜动作（LAPA / IDM）辅助目标**；RoboCasa **49.6%** vs DP 43.2%、DexMG **74.2%** vs 68.4%、真机未见物 **72%** vs 30%；消融：数据量 30/100/300、**神经轨迹 +5.8%**；⚠ **仓库已漂移至 N1.7-3B，与论文 2.2B 非同一权重**；⚠ System 1 频率有 **120 Hz** 与 30 Hz 两说 | 元数据 + 摘要（第二十五轮补全字段） |

## E. 2026 年新机制（流匹配 + RL / 值引导 / 世界模型）

| ID | 论文 | 作者（首位） | 载体与版本 | 生成机制 | 输出与基准 | 代码 | 可迁移机制 | 证据状态 |
|---|---|---|---|---|---|---|---|---|
| DP-E23 | [Reverse Flow Matching: A Unified Framework for Online RL with Diffusion and Flow Policies](https://arxiv.org/abs/2601.08136) | Zeyang Li | ICML 2026 Spotlight；arXiv v2 | 统一"噪声期望族"与"梯度期望族"两类扩散策略 RL 目标 | 通用在线 RL | [azizanlab/ReverseFlowMatching](https://github.com/azizanlab/ReverseFlowMatching) | 给"扩散策略怎么用 RL 训"提供统一理论框架。**第二十五轮补全**：**在线 RL（最大熵）**，用**后验均值 + Langevin Stein** 构造目标；DMC 8 环境对比 DQS / MaxEntDP / QSM / QVPO / SAC；消融含**提案分布与控制变量设计**；⚠ **README 的 clone 地址写 `zeyang23`，与仓库归属 `azizanlab` 不符** | 元数据 + 摘要（第二十五轮补全字段） |
| DP-E24 | [Flow Matching Policy Optimization with Mirror Descent and Entropy Constraints](https://arxiv.org/abs/2603.17685)（FMER） | Ting Gao | arXiv v3（2026-03） | 论证 ODE 式流匹配可同时做到免模拟策略优化与可解熵，替代 SDE 扩散策略 | 通用在线 RL | 未核验 | 熵可控 = 探索可控，对应驾驶中"多样性可控"的需求 | 元数据 + 摘要 |
| DP-E25 | [VGFM: Expressive Robot Policies via Dense Value Guidance in Flow Matching](https://arxiv.org/abs/2609.14261) | Prajwal Koirala | IROS 2026；arXiv v1（2026-09） | 稠密值引导的流匹配离线 RL，避免 BPTT/辅助网络/蒸馏 | 机器人控制 | 未核验 | 用值函数引导生成而不引入 BPTT，降低 RL 微调成本 | 元数据 + 摘要 |
| DP-E26 | [ForeDiffusion: Foresight-Conditioned Diffusion Policy via Future View Construction](https://arxiv.org/abs/2601.12925) | Weize Xie | arXiv v1（2026-01） | 注入未来视角作为条件 + 双损失，缓解误差累积 | 操作动作；基准未核验 | 未核验 | "未来视角条件化"对应驾驶中的未来潜状态条件（对比 DP-A31） | 元数据 + 摘要 |
| DP-E27 | [Unifying Object-Centric World Models and Diffusion Policy](https://arxiv.org/abs/2606.08775)（WorldDP） | Raktim Gautam Goswami | arXiv v1（2026-06） | 高层世界模型做 MPC 选子目标，低层扩散策略执行 | 多阶段操作 | 未核验 | 层次化"世界模型选目标 + 扩散执行"，对应驾驶中导航指令 → 轨迹的两层结构 | 元数据 + 摘要 |

## 具身侧评价基准（登记到**本项目** [sources.md](../../../sources.md) 的 B009–B011）

> **⚠ 更正（第二十九轮）**：本节标题原链接指向 [autonomous-driving/sources.md](../../../../autonomous-driving/sources.md)，但**主项目 `sources.md` 已声明 B009–B011 归属平级项目具身智能**，实际登记在本项目 `sources.md`。

| 编号 | 基准 | 性质 | 与本项目的关系 |
|---|---|---|---|
| B009 | [RoboMimic](https://arxiv.org/abs/2108.03298)（CoRL 2021） | 离线人类示范的学习与基准 | Diffusion Policy 的主要基准之一；"什么因素重要"的结论可类比驾驶中监督信号设计 |
| B010 | [LIBERO](https://arxiv.org/abs/2306.03310) | 终身机器人学习的知识迁移基准 | 考察跨任务迁移，对应驾驶的跨场景泛化评价 |
| B011 | [EBench](https://arxiv.org/abs/2606.18239)（2026-06） | 通用移动操作策略的"要素级"诊断基准（26 任务 / 5 能力维度 / 4 泛化维度） | 反例参照：单一成功率标量不足以诊断策略，直接支持对 NAVSIM 单一 PDMS 的质疑 |

## 可迁移机制小结（AI 判断，非论文结论）

| 机制 | 来源 | 迁移到自动驾驶的对应物 | 已知风险 |
|---|---|---|---|
| receding horizon action chunk | DP-E09、DP-E17 | 预测 Tp 步轨迹、只执行 Ta 步并滚动重规划 | 驾驶规划频率与控制频率不同；视野过短会丢长时程意图 |
| 少步/一步生成与蒸馏 | DP-E11、DP-E04、DP-A14 | 满足实时性约束 | 少步化可能牺牲多模态多样性（DP-A03 的"多样性-质量两难"） |
| 引导式约束（可微目标 / CBF） | DP-E01、DP-E08 | 碰撞、可行驶区域、舒适性写成引导或硬约束 | 引导会破坏流形/运动学可行性（DP-A22 的反例）；硬约束有额外算力成本 |
| 3D 表示条件化 | DP-E10 | LiDAR/点云条件化的规划器 | 驾驶还需交互与规则语义，纯几何表示不足 |
| 统一动作空间 | DP-E21 | 跨车型/跨数据集的轨迹表示统一 | 驾驶轨迹表示已有多种（waypoint/控制量），统一会牵动基线 |
| 冻结骨干 + 条件通路适配 | DP-E16、DP-E14 | 在新城市/新数据集上低成本适配 | 是否适用于扩散规划器尚未核验 |
| 目标掩码的统一策略 | DP-E17 | 同一策略同时支持"有导航目标"与"自由探索" | 驾驶中无目标场景较少，但可用于多目标/多指令切换 |
| 值/RL 引导生成 | DP-E15、DP-E23、DP-E25 | 扩散规划器后训练 | 训练不稳定、算力成本；驾驶侧已有 DP-A16、DP-A03 尝试 |

## 影响力快照（OpenAlex 正式版记录，2026-09-22）

| 论文 / 基准 | 引用数 | 记录 |
|---|---|---|
| DP-E09 Diffusion Policy | **531** | IJRR 2024（10.1177/02783649241273668） |
| DP-E19 π0 | 236 | 会议论文 2025 |
| DP-E10 DP3 | 181 | RSS 2024（10.15607/rss.2024.xx.067） |
| DP-E17 NoMaD | 125 | 会议论文 2024 |
| DP-E11 Consistency Policy | 50 | RSS 2024（10.15607/rss.2024.xx.071）——**venue 取自 OpenAlex 正式版记录，论文正文未标注会议**（表内"载体与版本"列与本行口径不同，非矛盾） |
| DP-E01 Diffuser | 62 | **仅 arXiv 记录，被低估**（ICML/PMLR 无 DOI） |
| DP-E02 Decision Diffuser | 32 | 同上，被低估 |
| DP-E28 EDP | 12 | 会议论文 2023 |
| DP-E04 DiffuserLite | 10 | 会议论文 2024 |
| DP-E21 RDT-1B / DP-E22 GR00T N1 | 各 5 | arXiv 记录 |
| B010 LIBERO | 88 | 会议论文 2023 |
| B009 RoboMimic | 71 | arXiv 记录 |
| B003 nuPlan | 16 | arXiv 记录 |
| DP-S03 机器人操作扩散综述 | 30 | Frontiers 2025 |
| DP-S01 扩散+RL 综述 | 12 | 仅 arXiv 记录，被低估 |

**限制**：PMLR/ICML 类论文在 OpenAlex 只有 arXiv 记录，引用数被严重低估；本表不把引用数用于排序。

## 逐行质量依据（T 档，2026-09-30 补）

> 判据见 [literature-quality.md](../../../../../shared/literature-quality.md) §4；引用数口径见上节「影响力快照」。**标「待核」= venue/团队/代码信号不足，暂不归档**。具身侧多为摘要级（见 §证据边界），故 T 档判据主要靠 venue 与代码可用性两项。

| ID | T 档 | 依据（可复核） |
|---|---|---|
| DP-E01 Diffuser | T1 | ICML 2022（CCF-A）；引用 62（被低估） |
| DP-E02 Decision Diffuser | T1 | ICLR 2023（CCF-A）；引用 32（被低估） |
| DP-E03 Diffusion-QL | T1 | ICLR 2023（CCF-A） |
| DP-E04 DiffuserLite | T1 | NeurIPS 2024（CCF-A）；引用 10 |
| DP-E05 DIPOLE | T4 | 仅 arXiv；有代码（主仓占位、真代码在 submodule） |
| DP-E06 MPDiffuser | T4 | 仅 arXiv；有代码（权重/数据不可得） |
| DP-E07 SDGD | 待核 | 仅 arXiv（ICLR 2026 被拒）；无官方代码 |
| DP-E08 SafeFlowMatcher | T2 | ICLR 2026 poster（CCF-A）；**无公开仓库** |
| DP-E09 Diffusion Policy | T1 | RSS 2023 + IJRR 2024（白名单）；引用 531 |
| DP-E10 DP3 | T1 | RSS 2024（白名单）；引用 181 |
| DP-E11 Consistency Policy | T1 | RSS 2024（白名单，venue 取自 OpenAlex）；引用 50 |
| DP-E12 Equivariant DP | T1 | CoRL 2024 **Oral**（白名单） |
| DP-E13 DiT Policy | 待核 | 仅 arXiv；代码未核验 |
| DP-E14 FLOWER | T1 | CoRL 2025（白名单）；有代码（两仓） |
| DP-E15 DPPO | T4 | 仅 arXiv；代码未核验（项目页） |
| DP-E16 Freeze/Share/Shrink | 待核 | 仅 arXiv（RSS2026-Diff4RL workshop）；**无代码** |
| DP-E17 NoMaD | T4 | 仅 arXiv；有代码（L1）；引用 125 |
| DP-E18 MulDP | T2 | IROS 2026（白名单） |
| DP-E19 π0 | T4 | 仅 arXiv；有代码（L1）；引用 236 |
| DP-E20 π0.5 | T4 | 仅 arXiv；同 openpi 代码 |
| DP-E21 RDT-1B | T4 | 仅 arXiv；有代码 + HF 权重 |
| DP-E22 GR00T N1 | T4 | 仅 arXiv；有代码 + HF 权重（⚠ 仓库已漂移） |
| DP-E23 Reverse Flow Matching | T2 | ICML 2026 **Spotlight**（CCF-A）；有代码 |
| DP-E24 FMER | 待核 | 仅 arXiv；代码未核验 |
| DP-E25 VGFM | T2 | IROS 2026（白名单）；代码未核验 |
| DP-E26 ForeDiffusion | 待核 | 仅 arXiv；代码未核验 |
| DP-E27 WorldDP | 待核 | 仅 arXiv；代码未核验 |
| B009 RoboMimic | T1 | CoRL 2021（白名单）；引用 71 |
| B010 LIBERO | T1 | 会议论文；引用 88 |
| B011 EBench | 待核 | 仅 arXiv（2026-06） |

## 证据边界

- 标注 `全文` 的条目为子代理抓取 arXiv HTML 并逐节提取，**HTML 表格数值常丢失**，凡正文未复述的数字标"未获取"。
- 具身侧全部结果均**未经本地复现**；其动作空间、控制频率、动力学与驾驶差异显著，本表"可迁移机制"列是**待验证假设**，不是已成立结论。
- 四篇核心论文（DP-E09/E10/E17/E19）的共同硬伤：均无他车博弈、车辆动力学与交通规则约束。
