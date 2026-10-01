# 端到端自动驾驶发展脉络（1989 → 2026）

更新时间：2026-09-22  
读法：只写已核验事实；arXiv ID 与 GitHub 仓库均已用 API 核实；标注"判断"处为 AI 推断。  
证据边界（重要）：本轮尝试读的 6 篇 E2E 综述中，**只有 S002 拿到全文**；S018/S016/S019/S020/S035 的正式全文均不可得（IEEE/ACM/MDPI/TechRxiv 返回 403 或被 Cloudflare 拦截，arXiv 无预印本）。因此本文的宏观分期以 **S001/S002/S032/S033 全文 + 逐条核实的时间线**为准，其余综述仅作旁证。

## 一句话总结

领域主线是**三段式**：模块化流水线 → 端到端（IL 为主）→ 大模型/VLM 赋能。**这个宏观三段在可读来源中高度收敛**（S002 §1 路线图、S018 §I、S019 三范式、S035 旁证）；但**细分期界、转折点归因、评价协议三件事至今没有收敛**。

## 阶段划分

| 阶段 | 时间 | 标志性变化 | 代表工作 | 关键局限 |
|---|---|---|---|---|
| I 起源：像素直连控制 | 1989–2018 | 网络直接从传感器回归转向 | ALVINN（1989）、PilotNet（[1604.07316](https://arxiv.org/abs/1604.07316)，2016）、ChauffeurNet（[1812.03079](https://arxiv.org/abs/1812.03079)，2018） | 无场景理解、无多模态、纯 IL 易漂移 |
| II 条件化与特权蒸馏 | 2018–2022 | 引入导航命令条件化、特权信息蒸馏、多传感器融合 | CIL（[1710.02410](https://arxiv.org/abs/1710.02410)）、LBC（[1912.12294](https://arxiv.org/abs/1912.12294)，2019）、NEAT（[2109.04456](https://arxiv.org/abs/2109.04456)）、TransFuser（[2104.09224](https://arxiv.org/abs/2104.09224)）、TCP（[2206.08129](https://arxiv.org/abs/2206.08129)）、ST-P3（[2207.07601](https://arxiv.org/abs/2207.07601)） | CARLA 闭环为主，输出仍是控制量或航点；感知-规划耦合弱 |
| III 规划导向 + 向量化 | 2023–2024 | **把"规划"作为主优化目标**；BEV 光栅化 → 全向量化；单轨迹 → 概率分布；**并出现第一条"生成式"路线（隐变量）** | UniAD（[2212.10156](https://arxiv.org/abs/2212.10156)，CVPR'23 最佳论文）、VAD（[2303.12077](https://arxiv.org/abs/2303.12077)）、VADv2（[2402.13243](https://arxiv.org/abs/2402.13243)）、SparseDrive（[2405.19620](https://arxiv.org/abs/2405.19620)）、Hydra-MDP（[2406.06978](https://arxiv.org/abs/2406.06978)）、**GenAD（[2402.11502](https://arxiv.org/abs/2402.11502)，生成式）** | 输出仍以回归/分类为主，多模态质量差。**代码级更正（见 [C005 §J](../code/traces/e2e_trunk_code_traces.md)）：GenAD 不能与"回归/分类"并列**——它是**32 维对角高斯隐变量 + spatial GRU + 解析 KL** 的 CVAE 式生成器（基于 VAD 代码库，**非扩散、无词表**），是本领域**第一条生成式规划路线**，早于 DiffusionDrive |
| IV 大模型 / VLM 赋能 | 2024–2026 | 引入语言与世界知识、推理时可选 LLM；后训练与 RL 兴起 | DriveVLM（[2402.12289](https://arxiv.org/abs/2402.12289)）、DriveLM（[2312.14150](https://arxiv.org/abs/2312.14150)）、DiMA（[2501.09757](https://arxiv.org/abs/2501.09757)）、DiffusionDrive（[2411.15139](https://arxiv.org/abs/2411.15139)）、DriveFuture（[2605.09701](https://arxiv.org/abs/2605.09701)） | 实时性、评价协议、形式化安全三者均未解（见下） |

## 三条轴的变化（脉络读法）

### 轴 1：输入表示
原始像素直连（ALVINN / PilotNet）→ **图像 + LiDAR 注意力融合**（TransFuser，转折）→ **BEV 隐式表征**（NEAT 注意力场）→ **全向量化**（VAD，转折：去掉 BEV 栅格）→ **稀疏 query**（SparseDrive）→ **加入语言/文本模态**（DriveVLM / DriveLM，转折）。

### 轴 2：输出形式
转向/油门控制（ALVINN、PilotNet、CIL、LBC、TransFuser、TCP）→ 显式轨迹/航点并作为**优化目标**（ChauffeurNet、ST-P3、UniAD，转折）→ 向量化轨迹（VAD）→ **动作词表上的概率分布**（VADv2，转折）→ 多候选 + 规则/教师打分（Hydra-MDP）→ **扩散/流匹配生成的多模态轨迹集合**（DiffusionDrive、GoalFlow）→ 语言接地的轨迹（DiMA）。

### 轴 3：监督方式
纯 IL / BC → **两阶段特权蒸馏**（LBC、NEAT，转折）→ IL + 多任务辅助损失（UniAD、VAD）→ **规则/多教师蒸馏**（Hydra-MDP，转折）→ **LLM 蒸馏**（DiMA，转折）→ RL 后训练（2025 后的新分支，见 [S033 笔记](notes/S033-post-training-e2e.md)）。

## 评价协议的演进

| 时期 | 协议 | 指标 | 已知缺陷（出处） |
|---|---|---|---|
| 开环 | KITTI / nuScenes | L2、碰撞率、MinADE/FDE | **不测恢复能力**；多模态场景会惩罚未观测选项（S001 §3.3）；无法捕捉误差累积与因果混淆（S018 §四A，二手） |
| CARLA 闭环 v1 | CARLA Leaderboard / NoCrash | RC、IS、**DS = RC × IS** | 初始配置复杂、域差（S002 §10、Table 7） |
| CARLA v2 / Bench2Drive | 闭环反应式 | DS、SR、多能力 | 路线方差大、训练数据各自采集（本项目 [context.md](../context.md)） |
| NAVSIM v1 | **非反应式伪仿真** | **PDMS** | 不测交互；子指标饱和（S032 §VII.C） |
| NAVSIM v2 | 两阶段伪闭环（**默认反应式 IDM 交通**） | **EPDMS**（代码里叫 `extended_pdm_score_*`）、**`navhard_two_stage`** 困难子集 | 与 v1 不可混用；NAVSIM 仍只是**代理证据**（S032 §VII.C）。口径详见 [benchmarks.md §2](benchmarks.md) |

**跨综述一致性**：开环 → 闭环 → 伪闭环这条**方向**一致；但**具体协议与指标至今没有统一分期**（S002 止于 CARLA v1 的 DS；S019 用 NAVSIM；S018 追加"干湿结合"与语言增强评估）。这与本项目从数字里发现的"GoalFlow 90.3 vs 85.7"相互印证。

## 2025–2026 仍活跃的基线（含代码可用性）

| 基线 | 为什么仍是基线 | 代码 |
|---|---|---|
| UniAD（CVPR'23） | 规划导向多任务的开创者，几乎所有新工作都列它 | [OpenDriveLab/UniAD](https://github.com/OpenDriveLab/UniAD) ✅ 已下载，**122 个 `.py`，代码完整** |
| VAD / VADv2 | 全向量化 + 概率规划，是 DiffusionDrive 的多模态前身 | [hustvl/VAD](https://github.com/hustvl/VAD) ✅ 已下载；**v1 完整（172 个 `.py`），VADv2 仅 config + head 两个文件**，且词表 `carla_plan_vocabulary_4096.npy` 未发布 |
| SparseDrive | 稀疏表征 + 并行规划，DIVER 直接基于它 | [swc-17/SparseDrive](https://github.com/swc-17/SparseDrive) ✅ 已下载，**75 个 `.py`，代码完整** |
| Hydra-MDP | 多教师蒸馏，NAVSIM 系基准；其 PDMS 奖励被 DIVER 复用 | [NVlabs/Hydra-MDP](https://github.com/NVlabs/Hydra-MDP) ⚠️ 已下载但**零代码**（仅 README + 一张图，README 自述因公司政策延迟发布） |
| TransFuser(++) | CARLA 系感知主干，GoalFlow 沿用其融合方式 | [autonomousvision/transfuser](https://github.com/autonomousvision/transfuser) ✅ 已下载，133 个 `.py`；**已代码级确证 GoalFlow 沿用**（`resnet_backbone.py` docstring 原文 "Implements the TransFuser vision backbone."，其配置与 navsim 的 `transfuser_config.py` 逐字段相同，但按 NAVSIM 重参数化：相机 1024×256、`pixels_per_meter=4.0`、`n_layer=2`，与 CARLA 原版不同） |
| TCP / ST-P3 / NEAT / CIL / LBC | 2021–2022 的 CARLA 系主干，被后续工作反复引用 | 均已下载（OpenDriveLab/TCP、OpenDriveLab/ST-P3、autonomousvision/neat、carla-simulator/imitation-learning、dotchen/LearningByCheating）；**除 CIL 仅 5 个 `.py`（子模块未接入）外均完整** |
| DriveVLM / DriveLM | VLM 支线的代表 | DriveLM ✅ 已下载（23 个 `.py`，以数据/文档为主）；**DriveVLM ⚠️ 仓库是项目主页，零代码** |
| DiMA | LLM 蒸馏到视觉规划器；**NAVSIM 上扩散规划器的常用非扩散对照** | **无官方代码**（GitHub API 已核实 404） |
| PARA-Drive | 全并行模块化栈 | **无官方代码**（GitHub API 已核实 404） |

> **代码可用性已逐个核验（2026-09-23）**：13 个主干仓库中 **2 个零代码**（Hydra-MDP、DriveVLM）。逐仓库结论见 [code/traces/e2e_trunk_code_traces.md](../code/traces/e2e_trunk_code_traces.md) §A。

## 论文明确写出的开放问题（按来源）

- **S001（TPAMI）**：稀疏奖励 RL、世界模型该建模什么、蒸馏效率、注意力可解释性的 faithfulness、**缺形式化安全保证**、因果混淆在 SOTA 下未解、长尾场景生成、LiDAR 域自适应、数据引擎。
- **S002（TIV）**：IL 分布漂移与 RL 不稳定、安全、可解释、协同感知、大视觉/语言模型（§12.1–12.5）。
- **S032（2026）**：指标有效性、长尾鲁棒、师生不对称、世界模型校准、语言-动作落地、形式与经验安全、算力部署、可复现性；**§IV.D 把"如何评估生成式规划"单列**。
- **S033（2026）**：奖励与探索的耦合、世界模型信号的行为级相关性、数据反馈闭环、**超越 GRPO 的更新方式**。
- **S018（二手）**：多模态融合复杂、样本效率低、安全风险；未来=世界模型统一数据生成与推理优化、基础模型模块化/稀疏激活/知识蒸馏。

## 早期主干的技术细节（本轮读全文核验，2024 年之前）

| 项 | ChauffeurNet（[1812.03079](https://arxiv.org/abs/1812.03079)，2018） | TransFuser（[2104.09224](https://arxiv.org/abs/2104.09224)，CVPR'21） | TCP（[2206.08129](https://arxiv.org/abs/2206.08129)，NeurIPS'22） | ST-P3（[2207.07601](https://arxiv.org/abs/2207.07601)，ECCV'22） | DriveVLM（[2402.12289](https://arxiv.org/abs/2402.12289)，CoRL'24） | DriveLM（[2312.14150](https://arxiv.org/abs/2312.14150)，ECCV'24） |
|---|---|---|---|---|---|---|
| 输入 | **mid-level 特权 BEV**（400×400px、0.2m/px、80m×80m；含 roadmap/红绿灯时序/限速/route/动态物体框/历史位姿） | 前视 RGB 256×256 + LiDAR BEV 32m×32m；**输入侧无特权**，仅稀疏 GPS + 导航命令 | 单目前视 + 速度 + 高层导航；特权只在教师 Roach 内 | 6 路环视视频（过去 1s）+ 命令；**不用 HD 地图** | 多视角图像序列 + 可选 3D 感知 + route/ego pose 文本提示 | 低分辨率前视图 + 文本 QA 图（无 LiDAR、无时序） |
| 输出 | 轨迹 N=10、δt=0.2s（≈2s），含 x,y,heading,speed | BEV 差分航点 T=4 → PID 转控制 | **双分支**：K 步航点 + 多步控制（throttle/brake/steer），情况融合 | BEV 轨迹，规划 horizon 3.0s | 语言（描述/分析）+ 17 类 meta-actions + 航点（3s） | 语言 QA + 行为（速度/转向 5 bins）+ 航点（256 bins token 化） |
| 监督 | IL + **扰动增强**（中点 ±0.5m、航向 ±π/3）+ 环境损失（碰撞/在路/几何）+ past-motion 与 imitation dropout | 纯 IL/BC，L1 航点损失；训练数据来自特权专家 | **特权蒸馏**（Roach 的 feature + value loss）+ IL（轨迹 L1、控制 beta 分布 KL） | 多任务端到端 IL（感知/预测/规划三项可学习权重） | VLM 监督微调 + co-tuning；Dual 版引入 3D 检测/占用/VAD | VLM 监督微调（LoRA）+ 图提示 |
| 主结果 | 闭环仿真 20 场景：绕停靠车通过 90%/碰撞 10% | CARLA 0.9.10 Town05：Short DS 54.52、Long DS 33.15；碰撞较几何融合降 **76.11%** | CARLA Leaderboard：TCP-Ens **DS 75.137**/RC 85.629 | nuScenes 开环 L2 1.33/2.11/2.90m；CARLA Town05 Long DS 11.45 | nuScenes：Dual† L2 **0.31m**/Col 0.10%（UniAD 1.03/0.31） | nuScenes 开环 Graph ADE 1.74m/Col 1.89%；Waymo zero-shot ADE 2.63 |
| 推理成本 | 160ms（≈6.3 FPS，P100） | 未获取 | **125.71 FPS**（TCP）/ 44.70 FPS（Ens） | 未获取 | OrinX **410ms** | **0.16 FPS**（3.955B 参数，约 10× 慢于 UniAD 的 1.8 FPS）**⚠ 来源待补**：第二十四轮代码级核验发现 DriveLM 仓库内**无任何 FPS/latency 代码**，唯一可核验的吞吐是 README 的"**约 2 小时 / 4072 帧（batch 8）≈ 0.57 fps**"（`challenge/README.md:116-119`）——**与 0.16 FPS 不一致**，故该数字属**仓库外来源**，引用时须补测量口径（batch / 硬件 / 是否含解码），见 [C005 第二册 §M.5](../code/traces/e2e_trunk_code_traces-2.md) |
| 自述局限 | 前向 64m/侧 40m 限制 merge 与高速转弯；U-turn/cul-de-sac 不支持 | 红灯在对侧难见，未用语义监督 | 规则化融合需先验；单目视野有限；不预测他车轨迹 | 未获取 | VLM 空间定位与推理弱、算力大；GPT-4V 场景描述有幻觉 | 效率低、仅前视、仅开环 |

## 一条新的结构观察：**特权信息的三段式**

这是本轮读早期工作后新增的脉络读法（AI 归纳，依据上表的"输入"列；**2026-09-23 已做代码级核验，见 [C005 §I](../code/traces/e2e_trunk_code_traces.md)**）：

1. **输入即特权**（ChauffeurNet，2018）：BEV 语义 + HD 地图 + 规则直接进网络。
2. **输入侧去特权**（TransFuser 2021、TCP 2022、ST-P3 2022）：网络只见相机（+LiDAR），特权只留在**训练教师或离线标签**里；ST-P3 更进一步去掉 HD 地图。
3. **特权作为可选辅助/提示**（DriveVLM 2024、DriveLM 2024）：3D 检测/占用/VAD 结果作为语言提示或 GT-context 上界重新出现，但不是网络的唯一输入。

> **代码级修正（2026-09-23）**：第 2 段的"**相机（+LiDAR）**"在代码层站不住——三个工作里**只有 TransFuser 真的吃 LiDAR**（`submission_agent.py:sensors()` 里有 `sensor.lidar.ray_cast`）；**ST-P3 是 4 视角纯相机**（`carla_agent.py:sensors()`），**TCP 也是纯相机**（其 `base_agent.py:170` 的 `sensor.lidar.ray_cast` **整段被注释掉**）。准确表述是"**只见相机，LiDAR 仅 TransFuser 有**"。另：nuScenes 四家（UniAD / VAD v1 / VAD v2 / SparseDrive）**一致** `use_lidar=False` + `use_map=False`——**感知侧去特权是彻底的**。

对本项目的含义：**评价协议里的"输入权限"差异不是新问题，而是这条十年级别的取舍在反复摆动**——这也是为什么本项目坚持在比较表中标注"输入权限"（[preparation.md 第 6 节](../ideas/preparation.md)）。**且标注方式要按实测字段而非配置文件**：`use_external` 这个 flag **两个方向都错**（UniAD 声明 `True` 却全仓未消费；SparseDrive 声明 `False` 却实际消费 CAN bus 的 `ego_status`），详见 [C005 §I.2](../code/traces/e2e_trunk_code_traces.md)。

## VLM 支线与传统 E2E 的接口差异（本轮核验）

| 维度 | 传统 E2E（TransFuser / TCP / UniAD / VAD） | VLM 支线（DriveVLM / DriveLM） |
|---|---|---|
| 输出 | 直接输出航点或控制 | **以语言为中间接口**（QA/描述/meta-actions），再映射到航点或行为 |
| 评测 | CARLA DS/RC/IS 或 nuScenes L2/Col | nuScenes L2/Col + **自建语言指标**（BLEU/METEOR/CIDEr/ROUGE/SPICE/GPT 打分）+ 行为准确率 |
| 数据 | 专家轨迹/控制（TransFuser 特权专家、TCP Roach） | **语言标注**（DriveLM-nuScenes 144k QA、CARLA 697k QA；DriveVLM 长尾挖掘 + 人工标注） |
| 实时性 | TCP 125.71 FPS、UniAD 1.8 FPS | DriveVLM 410ms、DriveLM **0.16 FPS**（**仓库内不可核验**，见 [C005 第二册 §M.5](../code/traces/e2e_trunk_code_traces-2.md)：仓库里只有 ~0.57 fps 的 README 数字） |

**判断**：语言支线用"可解释的中间接口"换来了**一个数量级以上的延迟代价**，且目前只报开环。这解释了为什么 2026 年的扩散规划器仍然以"轨迹直接输出"为主——**实时性与评价成熟度都更占优**。

## 代表基线的技术细节（本轮读全文核验）

| 项 | UniAD（[2212.10156](https://arxiv.org/abs/2212.10156)，CVPR'23） | VAD（[2303.12077](https://arxiv.org/abs/2303.12077)） | VADv2（[2402.13243](https://arxiv.org/abs/2402.13243)，**ICLR 2026**） | SparseDrive（[2405.19620](https://arxiv.org/abs/2405.19620)） | Hydra-MDP（[2406.06978](https://arxiv.org/abs/2406.06978)） |
|---|---|---|---|---|---|
| 场景表征 | **BEV 栅格**（BEVFormer）+ 多任务 query | **全向量化**（map/agent 向量），弃用栅格 | 向量化 + **场景 token 化**（map/agent/traffic element/image） | **全稀疏**（对称稀疏感知，无稠密 BEV） | 沿用 Transfuser 的 LiDAR BEV + 前视拼接 |
| 规划输出 | **单条轨迹**（ego query 解码 waypoint） | **单条轨迹** V̂ego∈R^{Tf×2}，2s 历史/3s 未来 | **动作词表上的概率分布**（V，N=4096），取最高概率 | **多候选轨迹**：Kp=6 模态 × 3 命令 = 18 提案 + 分层选择与碰撞重打分 | **词表概率分布 + 多目标子分数**（词表由 nuPlan 采 700K 轨迹 K-means 得 4096/8192） |
| 规划架构 | 3 层 Transformer Planner，与感知/预测/占用**五任务联合**（两阶段训练） | Transformer decoder 交互 + MLP Planning Head，与建图/运动预测联合 | 级联 Transformer decoder，query=轨迹 token、key/value=scene token + sigmoid MLP | **并行运动规划器**：ego 实例初始化 + 时空交互 + 分层选择 | 多 head 轨迹解码器，感知沿用 Transfuser |
| 监督 | IL + 占用碰撞项（λ_imi=1、λ_col=2.5） | IL + 三条**向量化规则约束** | IL（分布，KL/CE）+ 冲突负样本 | IL（winner-takes-all + ego 状态回归） | IL + **规则教师多目标蒸馏**（对 NC/DAC/TTC/C/EP 子分数做 BCE） |
| 主结果 | nuScenes 开环 **L2 1.03m / Col 0.31%**（Tab.7） | nuScenes **0.72m / 0.22%**（Tab.1）；CARLA Town05 Short DS 64.29、Long 30.31（Tab.4） | CARLA Long **DS 85.1**；Bench2Drive DS 76.15/SR 50.46；**NAVSIM navtest PDMS 89.3**；NAVSIMv2 EPDMS 85.8 | nuScenes **0.58m / 0.06%**（Tab.2b） | NAVSIM PDMS 82.6（V4096）→ 86.5（V8192-W-EP）→ 扩模型后 **91.0**（Tab.1/2） |
| 推理成本 | **1.8 FPS**、125.0M 参数（Tab.13） | VAD-Base 4.5 FPS / VAD-Tiny **16.8 FPS**（Tab.1） | 未获取 | SparseDrive-S **9.0 FPS**、-B 7.3 FPS（Tab.3） | 未获取 |
| 自述局限 | 多任务协调算力需求大，轻量化待探索 | 多模态运动预测未用于规划；未纳入车道图/路牌/红绿灯/限速 | 仿真与 3DGS 闭环中 agent 行为朴素、真实感不足 | 单任务性能落后专用方法；数据规模不足、开环评测不充分 | 无独立局限章节；提到 PDM 分数分布不规则需多目标学习 |

> 本表原有一行「继承」，第七十三轮已升级为独立节，见下 [§继承关系（代码层面已核验）](#继承关系代码层面已核验)。

**首次把"规划"作为主优化目标的是 UniAD**（证据：标题即 Planning-oriented；摘要明言各任务须 contribute to planning；Table 2 用规划 L2/碰撞率为终点逐模块验证，并给出 ID-12 vs 纯 MTL 的规划优势）。

## 继承关系（代码层面已核验）

读法：本节汇总主干各方法的**代码/基线血统**；强度分级 S1–S4 的定义见 [workflows.md §代码脉络梳理](../../../ai/workflows.md)。**逐篇细节仍在各笔记的 `## 在脉络中的位置`**，本节只做汇总与定级；扩散规划器侧的续段见 [topics/diffusion-planner/lineage.md §继承关系](../topics/diffusion-planner/lineage.md)。

| 工作 | 基线 / 来源库 | 强度 | 证据 |
|---|---|---|---|
| ChauffeurNet | ALVINN / NVIDIA PilotNet 式 IL、CIL 的条件化、MP3 的规划思想 | S2 | [E2E-06](notes/E2E-06-chauffeurnet.md) |
| TransFuser | LBC（蒸馏设定）+ ContFuse（几何融合） | S2 | [E2E-07](notes/E2E-07-transfuser.md) |
| TCP | TransFuser（自回归航点）+ Roach（RL 教师） | S2 | [E2E-08](notes/E2E-08-tcp.md) |
| ST-P3 | LSS / FIERY / MP3 / NMP / P3（Transfuser 作 LiDAR 对照） | S2 | [E2E-09](notes/E2E-09-st-p3.md) |
| UniAD | BEVFormer / Panoptic SegFormer / DETR / MOTR | S2 | [E2E-01](notes/E2E-01-uniad.md) |
| VAD | BEVFormer / MapTR / PIP | S2 | [E2E-02](notes/E2E-02-vad.md) |
| VADv2 | **VAD（同组，同一仓库 `hustvl/VAD` 两代）** + MapTRv2 / BEVFormer | **S1** | [E2E-03](notes/E2E-03-vadv2.md)、[repositories.md §B](../code/repositories.md) |
| SparseDrive | Sparse4Dv3（ID 分配）/ MapTR | S2 | [E2E-04](notes/E2E-04-sparsedrive.md) |
| Hydra-MDP | **VADv2（明确 "Following VADv2"）** + Transfuser（感知） | S2（代码未公开，仅论文） | [E2E-05](notes/E2E-05-hydra-mdp.md)、[C005 §C](../code/traces/e2e_trunk_code_traces.md) |
| GenAD | **VAD 代码库（同库派生）** | **S1** | [C005 §J.1](../code/traces/e2e_trunk_code_traces.md)——配置目录名就叫 `VAD`、`ego_query` 与 VAD v1 同款、README 以 VAD 作基线 |
| DriveVLM | UniAD / VAD（Dual 版与 VAD 协作） | S2 | [E2E-10](notes/E2E-10-drivevlm.md) |
| DriveLM | BLIP-2 / RT-2 的 token 化思路 | S2 | [E2E-11](notes/E2E-11-drivelm.md) |

**五环桥接**：「轨迹词表 / 锚点」谱系 **VAD → VADv2 → Hydra-MDP → DiffusionDrive → DiffusionDriveV2** 横跨主干与研究对象，完整代码证据见 [C005 §C](../code/traces/e2e_trunk_code_traces.md)；其中 ④DiffusionDrive 与 ⑤DiffusionDriveV2（扩散侧两环）的继承条目归 [topics/diffusion-planner/lineage.md §继承关系](../topics/diffusion-planner/lineage.md)，本节不重复。

**对决策的含义**：只有同源（同一代码库/基线）的方法才能把分差归因到机制；跨库者（如 VADv2 navtest PDMS 89.3 vs DiffusionDrive 88.1）**不可横比**——本表即 [preparation.md §6 比较口径](../ideas/preparation.md) 与 [judgments.md B/G 组](../judgments.md) 所引用的事实源。

## 与"扩散规划器"的接点（本项目主线）

1. **它站在轴 2 的末端，且有一个明确的思想前身**：VADv2（ICLR 2026）把规划输出变成**动作词表上的概率分布**（N=4096），Hydra-MDP 明写 "Following VADv2" 沿用其词表与解码器，而 DiffusionDrive 的**锚点先验**正是这一词表思路的延续。也就是说，**"多模态候选 + 先验词表"不是扩散模型带来的，扩散带来的是"如何在词表上生成/精修"**。
2. **一条必须正视的对照**：VADv2（**非生成式**，分类式概率规划）在 NAVSIM navtest 报 PDMS **89.3**，高于 DiffusionDrive 的 88.1；Hydra-MDP 扩模型后达 91.0。**注意**：三者的 backbone 与输入权限不同，不能直接横比（本项目 [preparation.md 第 6 节](../ideas/preparation.md) 已列出该限制），但这足以说明"生成式机制本身"并非性能的充分条件。
3. **它继承轴 3 的最新一支**：从 IL → 规则教师蒸馏（Hydra-MDP）→ RL 后训练（DIVER、DiffusionDriveV2）。
4. **它的评价困境来自本领域**：NAVSIM 的"代理证据"属性、协议不可比，都是 E2E 领域级问题，不是扩散规划器自身造成的。
5. **代码生态**：驾驶扩散规划器几乎全部长在 NAVSIM 生态（DiffusionDrive 家族、GoalFlow、MeanFuser、WAM-Flow）或 nuPlan/PLUTO 生态（Diffusion Planner、FlowDrive、PC-Diffuser）上。**更正**：我此前说"跨生态迁移无人做过"是错的——**HDP（DP-A06）仓库同时提供 navsim 与 nuplan 两套实现**，代码层面已打通；**限定（2026-09-23 代码核验）**：两套实现**不是同一个模型的移植**（nuPlan 侧基于 Diffusion Planner 但退化为 ego-only、删掉 `guidance/` 模块；NAVSIM 侧是 Florence-2 + DiT 的 VLA 结构）；仍成立的是"**没有工作在同一基准上对比两个生态的方法**"（见 [diffusion_planner_lineage.md](../topics/diffusion-planner/lineage.md)）。

## 证据边界

- 时间线的 arXiv ID、GitHub 仓库均已核验；**代表性工作 11 篇已读全文**（ChauffeurNet、TransFuser、TCP、ST-P3、UniAD、VAD、VADv2、SparseDrive、Hydra-MDP、DriveVLM、DriveLM），笔记见 [notes/](notes)。
- **代码可用性已于 2026-09-23 逐个核验**（13 个主干仓库）：**2 个零代码**（Hydra-MDP、DriveVLM），**VADv2 为部分发布且词表未随仓库提供**。详见 [code/traces/e2e_trunk_code_traces.md](../code/traces/e2e_trunk_code_traces.md)。
- 综述方面：**除 S001/S002/S032/S033 外，其余未读全文**（S016/S018/S019/S020/S035 的 OA 入口一律 403），其论断标"二手"或不采用；S035 的同作者另一篇（arXiv 2603.16050）**不是同一篇**，未用于代填。
- 表中指标数字只在核验到来源时写出；本文不把"阶段划分"当作定论：S002/S016 按主题而非年份分期，S020 用 Data–Strategy–Platform 三维度替代时间轴——**分期方式本身存在分歧**。
- 早期工作（ALVINN/PilotNet/ChauffeurNet 等）**无官方开源**，因此它们的"输入/输出/监督"描述来自论文原文，代码层面无法交叉验证。
