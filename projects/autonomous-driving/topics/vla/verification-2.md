# VLA（自动驾驶侧）· 全文与代码核验详细结论（第二册：§9–§14）

本册承接 [verification.md](verification.md)（§4–§8），保存 §9–§14。

## 9. AutoMoT（VLA-20）的全文 + 代码核验（第二十四轮新增）

**为什么核这一篇**：VLA-20 AutoMoT 是**与研究对象最相关的一篇 VLA**——它带一个 **"Generative (Diffusion) Head" / Action Refiner**，且 Bench2Drive 报 **89.42 DS / 74.09% SR**（高于 SimLingo 的 85.07）。如果"VLA + 扩散头"能拿到 B2D SOTA，那是**对"扩散生成"这条路线的强证据**。→ 于是做了全文 + 代码双侧核验（**未克隆**，走 `raw` 逐文件取证，缓存 47 个文件）。

### 9.1 全文口径：扩散头是**独立后置模块**，且**步数全文未给**

**架构（MoT 三件套）**：**UE = Qwen3-VL-4B dense，全程冻结**；**AE ≈ 1.6B，从零训练**；**AR = DiT 扩散策略**。UE 出 CoT 语义推理，AE 出三类动作侧输出——**meta-action（3 个，1 s 间隔 / 3 s 视野）+ temporal waypoints（6 个，0.5 s 间隔）+ spatial route points（20 个）**。

- **layer-wise joint attention sharing**：每层把 UE 的 K/V 与 AE 的 K/V 按序列维拼接后做联合注意力（Eq.3–5）→ AE 在共享隐空间里条件于 UE 的推理表征。
- **cross-task causal mask**（Fig.3）：语言 / 跨模态 / 跨任务交互走 causal（decision 条件于 understanding，planning 条件于 understanding + decision），任务内与自模态走 bidirectional。
- **异步推理**：UE 低频更新并写 **persistent KV cache**，AE 高频复用。延迟（Table 6/10，RTX 5090）：**同步版 117.3 ms（UE 80.3 + AE 37.0）= 8.5 Hz；异步版 37.0 ms = 27 Hz**（降 68.5%）；**开 AR 后 143.3 ms / 63.0 ms（AR 单次 26 ms）= 7.0 / 16.0 Hz** → **"37 ms · 27 Hz" 是"不含 AR"的口径**。对比：SimLingo 430 ms、AutoVLA 1072 ms、OpenEMMA 7683 ms。异步代价：L2 avg 0.322 → 0.324（+0.62%）。

**扩散头（Action Refiner）全文口径**：**是标准 DiT 截断反向去噪，不是流匹配**。
1. **不接在 AE 内部**，是**独立后置模块**，以 AE 的时空轨迹 proposal 为 **informative prior（anchor）** 做截断反向去噪 → **起点既不是白噪声、也不是聚类轨迹**；
2. 扰动是**乘性高斯噪声**（引 DiffusionDriveV2）；
3. temporal + spatial queries 拼接后过 L 个 DiT decoder block；
4. 条件 = 扩散 timestep + 当前自车状态 + 低维状态历史，经 **AdaLN** 注入；
5. 另两路条件（AE 的 latent decision states 与 BEV feature）用 **MoA（Mixture-of-Attention）** 并联融合（主路 self-attn + 两路 cross-attn，残差旁路取 BEV 均值池化与 reasoning token 注意力池化）；
6. **损失 = L1 重建误差**；数据 PDM-Lite（自述 >70 万样本 / 5000+ 场景，4 帧历史 @2 Hz）。

→ **步数与噪声日程，全文（正文 + 附录 + 表格）都没有给**（DDPM/DDIM 只出现在参考文献里）。

### 9.2 数字与消融

| 方法 | Bench2Drive DS | SR |
|---|---|---|
| **AutoMoT+（含 AR）** | **89.42** | **74.09** |
| AutoMoT（不含 AR） | 87.34 | 70.00 |
| SimLingo | 85.07 | 67.27 |
| AutoVLA | 78.84 | 57.73 |
| MindDrive | 78.04 | 55.09 |
| ORION | 77.74 | 54.62 |
| DiffusionDrive | 77.68 | 57.72 |

→ **加扩散精修头的净收益 = +2.08 DS / +4.09 SR**；论文注明 AutoMoT+ 是**多次运行均值**（"扩散随机性在闭环里会被放大"）。**该表只有 DS/SR，没有 Effi/Comf，也没有 5 项 Ability 分解**。

nuScenes 开环（**ST-P3 协议**）：L2 0.14/0.29/0.54、avg **0.32**；碰撞率 0.01/0.06/0.15、avg **0.07**（自述碰撞率 SOTA）。组件消融：随机初始化 UE（AutoMoT-R）L2 avg 0.36；去掉决策目标（AutoMoT-P）0.34。**UE 微调会灾难性遗忘**：TallyQA 81.40 → 52.40、InfographicVQA 89.30 → 50.20。

### 9.3 输入权限：论文写 "multi-view"，**代码只有前视**

- 论文口径：UE 吃 "multi-view and multi-frame RGB"，AE 吃 LiDAR BEV。
- **代码口径**：**4 帧历史前视 RGB**（每 5 步采 1 帧，t0 / t−5 / t−10 / t−15）+ **1 帧 LiDAR BEV**；BEV encoder 输入 `rgb + lidar_bev`，输出 1512×8×8 → 64 tokens；数据标记只有 `<image>` / `<front>` / `<bev>`，**没有环视相机**。
- → **论文的输入权限描述比代码更宽**（与 AutoVLA 的"三层口径"同类问题）。

### 9.4 代码核验：**扩散头根本没有发布**（本轮最要紧的一条）

**全仓 grep `diffusion` / `refiner` / `denois` / `adaln` / `num_inference_steps` —— 零命中。** 实际规划头是**纯 MLP 回归，没有采样循环**：

```
Automot/mot/modeling/automot/automot.py:183   class WaypointsHead(nn.Module)      # 6 点，(B,6,2)，含可学习 query
Automot/mot/modeling/automot/automot.py:141   class RouteHead(nn.Module)          # 20 点，cumsum
Automot/evaluation/inference.py:112           action = self.model.waypoints_head(action_hidden_states)
Automot/evaluation/inference.py:244           traj = self._predict_trajectory(...).cumsum(dim=1)
leaderboard/team_code/mot_b2d_agent.py:1156   pred_traj = output['traj']          # 直接送 control_pid，无任何精修
```

只剩三处**脚手架**：`modeling_utils.py:63 class TimestepEmbedder(nn.Module)`（抄自 DiT，仅被 FSDP auto-wrap 类集合登记）、`cache_utils/taylorseer.py:117 cache_init(num_steps)`（抄自 TaylorSeer，**全仓无人 import → 孤儿文件**）。

**仓库自己的 TODO 也没勾**：`README.md:33 - [ ] Release the Action Refiner`（其余四项 `[x]` 已勾）；README 里报的数字是 **"DS=87.34 / SR=70.00"（即不含 AR 的那个口径）**。

**配置侧**：`configs/automot_traj_train.yaml` / `_eval.yaml` 只有 dataset / frame / image 参数，**没有任何 diffusion / refiner 键**；`train_automot.sh` 只覆盖训练超参。→ **不是"论文有、配置里关了"（ORION 式），而是"论文有、代码里根本不存在"——比 ORION 更彻底。**

**其余核对**：异步频率在代码里是 `slow_update_interval`（`inference.py:260` 默认 `2`，`:270 if frame_idx % slow_update_interval == 0`），而 **B2D agent 从不传该参数** → 实际用默认 2；`action_tokens = 26`（20 route + 6 waypoints）；`reasoning_query_max_num_tokens` 默认 8。**无硬编码作者本机路径**（全走环境变量 + `require_var` 校验），**无未定义变量**，**只有 `release` 一个分支**（没有藏 refiner 的分支）。数据量对得上（`num_used_data: 599852` vs 论文 >70 万）。

### 9.5 三条判断

1. **"VLA + 扩散头拿到 B2D SOTA"这条证据目前不可用**：**AutoMoT+ 的 89.42 DS / 74.09% SR 无法从发布代码复现**——扩散头未发布、规划头是 MLP、README 自报的是 87.34/70.00。→ **引用时必须写"AutoMoT+ 的 +2.08 DS / +4.09 SR 来自未发布的 Action Refiner，仅论文自述"**。
2. **但它给了一个有价值的机制描述**：扩散头是**独立后置模块**、以 AE 的轨迹 proposal 为 **anchor** 做**截断去噪**（起点既非白噪声也非聚类词表），且**"异步推理 + KV cache"把 UE 成本从 80.3 ms 压到 0** → 对"**扩散精修 vs 端到端扩散生成**"这个对照有参考价值。**注意它的"anchor"来源是 VLA 的 proposal，而不是 K-means 词表**——这是与 DiffusionDrive 的关键差别。
3. **输入权限要按代码标**：论文写 multi-view，**代码只有 4 帧前视 + LiDAR BEV** → 这是"输入权限必须按使用层标注"（第十八/二十一轮结论）的**第三次印证**。

## 10. SpanVLA / LaST-VLA / UniDriveVLA 的全文核验（第二十四轮新增）

**为什么核这三篇**：它们是第二十四轮从边界外补入的 VLA 里**机制与研究对象直接重叠**的三篇——SpanVLA 用 **flow matching 动作专家 + GRPO**、LaST-VLA 用 **GRPO**、UniDriveVLA 用 **MoT 内嵌 flow matching**。三篇都**未克隆**，走 `WebFetch` 读 arXiv HTML 全文。

### 10.1 SpanVLA（VLA-26）——**"回归头 → flow matching"的受控消融 +5.2 PDMS**，且它的 "GRPO" **取消了 clip**

**生成机制（混合）**：VLM（Qwen2.5VL-3B）自回归出推理 token，训练时也出**离散 action token**（**2048 词表，来自 Waymo Open Motion**）；轨迹由**独立的 action bridging 用 flow matching** 生成。

- **起点不是纯高斯**：论文原文 "Unlike the prior approaches that **start from pure Gaussian noise** … our method **initializes from the historical trajectory embedding** with MLP layers"，训练时**往历史轨迹嵌入里注入高斯噪声**；用 **optimal transport displacement map**。
- **5 步**（Table 4 记 `0.08 (5 steps)`；L1 头是 `0.02`）→ **flow matching 的动作生成慢 4×**。
- 条件 = **VLM 稀疏层 KV cache（间隔 2 层）** + 历史轨迹嵌入 + flow 时间嵌入。
- 损失 = conditional flow matching loss（Eq.4）；**对 VLM 与 bridging 双向 stop-gradient**，先训 VLM 再单独微调 bridging。
- 动作专家接法：**独立后置模块**（不是 π0 式内嵌）。

**RL 六项核对（"RL 词义核验"第 7 种）**：log-prob ✅；优势 = **group-relative**（Eq.5–6）✅；KL ✅（权重 β，参考 = SFT 策略）；无 critic/GAE；**比率裁剪 ❌——但这是论文自己声明的**：§4.1 原文 "**single policy update per step … eliminates the need for clipping or maintaining an old policy**"（公式里含 ε 但实现上取消）→ **属"论文明确说明的简化"，不是"名实不符"**。奖励 = **PDMS 为主 + 负样本 L2 惩罚 + 恢复奖励 + 推理长度惩罚 + 动作-推理一致性规则惩罚**（Eq.7）；仅 LoRA 微调 VLM。

**数字与消融（这一节是本项目最需要的受控对照）**：

| 项 | 值 | 来源 |
|---|---|---|
| NAVSIM v1 navtest PDMS | **90.3** | Table 1 |
| NAVSIM v2 navtest EPDMS | **86.4** | Table 2 |
| NAVSIM v2 **navhard** EPDMS | **40.1** | Table 3 |
| **动作头：flow matching vs L1 回归** | **90.3 vs 85.1（+5.2）** | **Table 4**（同一 VLM 编码下只换动作头） |
| 起点：历史轨迹初始化 vs 纯高斯 | **90.3 vs 86.4（+3.9）** | Table 5 |
| **RFT（RL 后训练）vs SFT** | **82.1 → 90.3（+8.2）** | Table 1 |

→ **"生成机制本身"（回归 → flow matching）有 +5.2 的受控收益，与"改条件"（GoalFlow +4.7 / DriveFuture +3.7）同量级** —— 这条直接修正了 [preparation.md](../../ideas/preparation.md) 第 2 节此前那条"改条件远大于改生成日程"的判断。

**输入权限**：**3 相机（前 / 前左 / 前右），每路 4 帧 @2 Hz，无 LiDAR**（Table 1 的 Lid. 列为 `-`）。
**代码**：**仅项目页 `spanvla.github.io`，无 GitHub 仓库，也未承诺发布**（附录 E 只谈部署加速与奖励设计）。

### 10.2 LaST-VLA（VLA-24）——**纯自回归离散 token，但 GRPO 是最完整的一种**

**生成机制**：**纯自回归离散 token，无扩散 / 流匹配 / VAE**。InternVL3 自回归生成**连续隐时空 CoT**（H_dyn 对齐 Cosmos、H_geo 对齐 VGGT），再 "autoregressively predicts the future waypoints (**represented as textual tokens**)"。→ **与 WAM-Flow / OpenDriveVLA 的"轨迹即文本"同类**。

**RL 六项核对（第 8 种，也是**继 FeaXDrive / MindDrive 之后**第三完整的一种）**：log-prob ✅；优势 = **组内标准化 `(r−mean)/std`** ✅；**clip ✅（有 ε）**；**KL ✅（参考 π_ref）**；无 critic/GAE。奖励 = 复合 `R_traj`（PDMS 归一）+ `R_fmt`（格式）+ `R_goal`（终点分层）；**GRPO 时冻结 dynamics / geometry adapter**。

**数字与消融**：v1 navtest **91.3 PDMS**（8B-RL；2B 91.1）；v2 **87.1 EPDMS**（2B 86.8）。消融：**去掉 WM+3D 的 RL：87.2 vs 全量 91.3（+4.1）**；有监督潜 CoT 91.3 vs 无监督 89.8（+1.5）vs **文本 CoT 87.2（+4.1）**；结构化因果掩码 +2.0。**无 Bench2Drive / navhard**。
**输入权限**：**单目前视相机** + 指令 / 自车状态 / 历史轨迹，无 LiDAR。
**代码**：`luo-yc17/LaST-VLA`，**README "Currently Supported Features" 四项全部未勾选**——`LaST-VLA Inference Code` / `Checkpoint` / `Training Code` / `Training Dataset`（原文）→ **实际不可复现**。

### 10.3 UniDriveVLA（VLA-23）——MoT **内嵌** flow matching，且**无 RL**

**生成机制**：MoT 三专家（Understanding / Perception / Action），masked joint attention 协调；**Action 分支用 flow-matching 生成轨迹**（Eq.8）。→ **动作专家是内嵌的第三个专家**（不是后置）。**采样步数、起点分布、损失细节论文均未给**。**全文无 RL / GRPO**。

**数字**：**Bench2Drive DS 78.37 / SR 51.82 / Effi 198.86 / Comf 11.78**（Table 1）；多能力均值 51.53；nuScenes 开环 Avg L2 0.51。消融：**MoT vs shared-weight → L2 0.533 vs 0.641、CR 0.140 vs 0.175**（Table 7）。**无"去 flow matching"消融**。
**输入权限**：多视角相机（B2D 6 视图 / nuScenes 多视图），**论文未提 LiDAR、未明帧数**。
**代码**：`xiaomi-research/unidrivevla`，**代码 / 权重 / 数据均已发布**；Updates 唯一未完成项是 **`Release model on Navsim`**。

**与 AutoMoT（VLA-20）的四处差别**：① **专家划分**——UniDriveVLA 是"理解/感知/规划"三专家 + 稀疏感知；AutoMoT 是 MoT + **扩散动作精修头**；② **动作头定位**——UniDriveVLA 是 **MoT 内嵌** flow matching、**无 RL**；AutoMoT 是**独立后置**扩散精修头（anchor = AE 的轨迹 proposal）；③ **数字**——UniDriveVLA B2D **78.37 / 51.82**，AutoMoT+ **89.42 / 74.09**（**后者来自未发布的 Action Refiner，仅论文自述**，见 §9）；④ **团队**——UniDriveVLA = HUST + 小米 EV + 澳大；AutoMoT = NTU AutoMan + Harvard + 小米汽车。

### 10.4 三篇合起来的三条判断

1. **"生成机制"这一维的受控收益被低估了**：SpanVLA 的 **+5.2（回归 → flow matching）** 是**同 VLM、只换动作头**的干净对照，量级与"改条件"（+3.7 ~ +4.7）相当甚至更大。→ **不能再说"生成日程已经调到头、只剩条件可做"**。
2. **"RL 后训练"的收益在三篇里不一致**：SpanVLA **+8.2**（82.1→90.3，SFT→RFT）、LaST-VLA **+4.1**（去 WM+3D 的 RL 对照）、UniDriveVLA **无 RL**。→ 但 SpanVLA 的 RFT 奖励里含**负样本 L2 惩罚 + 恢复奖励 + 一致性规则惩罚**（**不只有 PDMS**）→ 与 FeaXDrive 的"直接用 PDMS 做奖励会破坏可行性"一致，**这类"复合奖励"才是当前能提分的形式**。
3. **"有代码"这一档要继续细分**：**SpanVLA 无仓库**（只项目页）/ **LaST-VLA 有仓库但四项全未发布**（推理代码、权重、训练代码、数据）/ **UniDriveVLA 基本齐全**（只差 Navsim 权重）/ **AutoMoT 缺核心模块**（扩散头未发布）。→ **四篇里只有 UniDriveVLA 接近可复现**。

## 11. VaViM/VaVAM、Reasoning-VLA、Counterfactual VLA 的全文 + 代码核验（第二十五轮新增）

三篇均为**第二十四轮从边界外补入的 VLA-22 / 25 / 27**，本轮由子代理读 arXiv 全文（HTML + PDF 交叉补全）并核验代码（GitHub API ≤5 次，其余走 `raw`，**未克隆**）。

### 11.1 VaViM / VaVAM（VLA-22）——**flow matching + 逐层 joint attention，但主干被冻结**

- **架构**：**VaViM** = LlamaGen **VQGAN（16384 词表，stride 16）+ GPT-2 自回归 next-token**，24 层、8 帧上下文 = 4608 token；**VaVAM** = VaViM + **动作专家（flow matching，Euler 10 步）**，输出 **6 waypoint @2 Hz = 3 s**（§3.1–3.2、§4.4–4.5）。
- **接口位**：**逐层 joint attention**——每层共享 attention 维度、FFN 分离，**动作 token 看全部视觉 token，视觉 token 保持因果掩码**（Fig 2b；`joint_model.py:121-187`）→ **不是"仅共享编码器"，也不是隐状态拼接**。
- **⚠ 名实不符（本轮新增的陷阱形态）**：论文称"完整 perception-to-action pipeline"，但代码 `video_action_model.py:64` 有 **`self.gpt.requires_grad_(False)`** → **VaViM 在模仿学习阶段被冻结**，只训约 21–150 M 的动作头；**论文全文未出现 frozen / freeze 字样**。→ 与 ORION（配置全关）、AutoMoT（模块不存在）并列的**第四种"论文声称 vs 代码实测"形态**：**机制在代码里且被走到，但训练被冻结而论文未声明**。
- **数字**：开环 minADE@5（nuScenes / nuPlan）**S 1.00/0.68、B 0.85/0.53、L 0.80/0.52**（Table 4）；**NeuroNCAP 闭式** VaVAM-L avg **2.46** / 碰撞 **57.9%**，Frontal NNS **2.38（SOTA）** / 56.8%（Table 5），同表 **UniAD（无后处理）0.73 / 88.6、VAD 0.66 / 92.5**，而 **UniAD+后处理 1.84 / 68.7、VAD+后处理 2.75 / 50.7** → **其"SOTA"是闭式口径 + 基线全无后处理的结果**。
- **⚠ 规模越大反而越差**：Frontal 扩展里 **B 139k 仅 1.781 / 70.0**（Table 6）；生成质量侧 **mIoU Cityscapes 17.9–21.2，全面低于 DINOv2**（Table 3）。
- **无受控消融**：全文**无 ablation 章节**，**没有"视频预训练 vs 从零训练"的对照** → **"视频预训练本身带来多少收益"无法量化**（代码其实支持：`video_action_model.py:67-69` 在 `gpt_checkpoint_path=null` 时随机初始化，但无对应配置/实验）。
- **输入权限**：**仅前视单目 512×288、8 帧历史 @2 Hz**；**无 LiDAR / 地图 / 自车运动学**；用高层命令 {left, right, straight}（§4.1、§4.5）。
- **代码**：**完整**（训练 `vam/train.py` + 推理 + 配置 + 权重，权重在 **GitHub Releases v1.0.0**，非 HF）；**闭式评测不在本仓库**——依赖外部 fork `F-Barto/neuro-ncap`（`trajectory_metrics` 分支）→ 复现需自行搭建。
- **零碎不符**：配置 `vocabulary_size: 16385` vs 论文 16384；配置默认 `lr=1e-4` / `init_std=0.01` 与论文/README 的 0.0194 / 0.0086 不符（靠命令行覆盖）；`action_scaling: 70.` 论文未提。

### 11.2 Reasoning-VLA（VLA-25）——**动作是并行回归，"GRPO"作用在 token 上，且仓库是空壳**

- **架构**：**Qwen2.5-VL（3B / 7B）** + **可学习 action queries**（`AQ ∈ T×N×D`，由训练集 GT 轨迹的均值/方差高斯初始化）；AQ 与 VLM token 解耦，先 self-attention 再与 VLM hidden states cross-attention，**双向 mask 一次前向并行输出全部轨迹**，再经 ARM（MLP + attention）精修（§3.2–3.5）→ **动作是连续回归**，论文明确对比 π0 / OpenVLA 的离散 action token。
- **RL 声明（论文级，不可核验）**：§3.6 原句 "we apply the **GRPO** [39] during RL fine-tuning. Unlike conventional policy-based methods, GRPO replaces the critic model … with an estimation of group scores"；附录超参 `beta 0.04`（KL 系数）、`num_generations 8`、`lr 1e-6`、`num_train_epochs 1`；**ratio / clip(ε) / advantage 归一化论文均未声明**。
- **奖励是规则分**（§3.7）：轨迹加权 L2（Eq.1）+ 转向阶跃（|Δy/Δx| < 0.84 给 1，Eq.2）+ 加速度阶跃（|acc| < 6 给 1，Eq.4），加权求和（Eq.5）→ **不是 PDM 分、不是人类偏好**，且两个阈值是**硬 0/1 阶跃**，易被 hack。
- **⚠ 结构性疑点**：动作是连续回归，而 GRPO 作用于 token 序列（`max_completion_length 768`）→ **奖励梯度如何回流到动作头论文未说明**，疑似 RL 只优化 CoT token；且 §8.2 的 CoT 是模板化占位（"let's derive the waypoints… `<|place_holder|>`×20"），**推理内容与数值动作无实质关联**。
- **数字**：nuScenes 开环 **R-VLA-7B Avg L2 0.23 m / 碰撞 0.08%**（7B+ 0.22 / 0.07，3B 0.30 / 0.13；基线最佳 DriveVLM-Dual 0.31 / 0.10）；**NeuroNCAP 闭环 Score 2.25 / 碰撞 59.4%**；**NAVSIM PDMS 91.7**（TTC 98.1 / EP 80.7）；效率 10 条轨迹 **0.089 s/次**。**⚠ 7B+ 开环变好但闭环变差**（2.25→2.19，59.4→59.8），与"进一步提升"的表述矛盾（§5.2.2 自认泛化下降）。
- **消融（Table 4）**：原始 Qwen2.5-VL-7B Avg L2 **1.45** → w/o AQ **0.32** → w/o AQ-Init **0.29** → w/o ARM **0.29** → 完整 **0.26（SFT）/ 0.23（SFT+RL）** → **每个组件增益都很小，且没有 RL-only 的同数据同算力受控对照**。
- **输入权限**：**3 路相机**（nuScenes 实为 6 路，只取 FRONT/LEFT/RIGHT）+ 自车状态 + 固定 prompt；历史 **3.0 s @0.5 s（7 帧）**，未来 10 步 @0.5 s；**无 LiDAR、无 HD 地图**；分辨率未给。
- **代码**：`xipi702/Reasoning-VLA` **存在但是空壳**——文件树**只有 `README.md`（113 B）**，内容为 "… # Comming Soon."，**无 RL 脚本、无奖励实现、无权重**。

### 11.3 Counterfactual VLA（VLA-27）——**"反事实"是事后诊断文本的 SFT，全文无仿真/世界模型**

- **核心机制**（§3.1 原句）："instead of mapping meta-actions to trajectories (meta→traj), CF-VLA performs a self-reflective loop: **meta-actions → CF reasoning → updated meta-actions → trajectory**"；是否反思由模型自己生成 `Action:` 还是 `Thinking:` 决定。
- **数据构造**（§3.3）：先 rollout 基座 VLA，每场景采 **6 条轨迹 × 2 种条件**（free / pre-filled），用 `minADE(x_pf, x*) < minADE(x_free, x*) 且 minADE(x_free, x*) > 0.5` 筛出瓶颈场景，再由 **Qwen2.5-VL-72B 教师**生成 ≤80 词诊断文本。
- **⚠ 名不副实**：摘要称 "simulates potential outcomes"，但**全文无任何前向仿真 / 世界模型 / verifier**（§1 自述 "without an external world model or verifier"）→ 实质是**用 GT meta-action 事后诊断文本做 SFT**；且教师 prompt 明令 "Never mention ground truth/expert/GT"，**同时又喂入 expert meta-action** → **存在 GT 泄漏面**。
- **架构**：Qwen2.5-VL-3B；**生成式自回归离散 token**（未来 **6.4 s 用 6 个离散 token**，10 Hz → 64 waypoints），词表靠扩展 VLM 词表加入（大小未给）；meta-action 空间 **11 个原子动作**（纵 5 / 横 3 / 车道 3），IOU 用 64×3 bins 计算（§3.2、§4.1、§8）。
- **⚠ 无任何公开 benchmark**：仅在内部私有数据（**80,000 h / 25 国**）的验证子集上**开环**评测，**全文未出现 NAVSIM / Bench2Drive / nuScenes / CARLA**；collision / off-road 由预测轨迹与记录他车轨迹比对（§4.1），**非闭环反应式仿真**，且数据不可复现。
- **数字（Table 1，MinADE）**：traj-only **0.9283** → meta-act 0.8411 → lang-meta-act 0.8021 → **CF-VLA（无 route）0.7650** / **CF-VLA（有 route）0.6712**（Avg 1.4574 / Collision 0.0177 / Off-road 0.0593 / IOU 0.9231 / think 0.219）。
- **⚠ 数字口径混用**：摘要的 **17.6%** 相对的是**无 route 版**，而表中最佳 0.6712 是**有 route 版**（相对 traj-only 实为 **27.7%**，相对 meta-act(w/route) 仅 **7.6%**）；20.5% 与 14.7% 各指不同对照与不同指标。
- **⚠ 受控对照削弱主张（Table 2）**：meta-act 0.8411 → **multi-round（丢弃推理文本、仅复用高分样本）0.7906** → CF-VLA **0.7650** → **"反思推理"本身的边际收益只有约 3%**；且 **force-think 0.9319 比 traj-only 还差**、"修正后"IOU 反降（0.9132→0.8565）。
- **输入权限**：**两路前视**（wide 120° / tele 30°），每路 **4 帧 @2 Hz、448×796**；自车历史 1.6 s @10 Hz → 1 个 token；可选 route 20 waypoints / 未来 80 m；**无 LiDAR、无地图、无自然语言指令**。
- **代码**：**未找到官方仓库**；唯一命中 `pengzhenghao/cfvla` 是 **CVPR'26 项目主页**（只有 `.gitignore` / `README.md`(130 B) / `index.html` / `static/`），**无代码/权重/数据链接**。

### 11.4 四条判断（本轮）

1. **"VLA + 生成式动作头"再添一例，且这例接得更深**：**VaVAM 是 flow matching + 逐层 joint attention**（动作 token 与视觉 token 在同一 transformer 的每一层交互）→ 与 SpanVLA（换动作头）、UniDriveVLA（MoT 内嵌）、AutoMoT（独立后置扩散头）合计**四例**，"VLM + 生成式动作头"已是主流配置之一这条判断再加固。
2. **但"联合训练"多数名不副实**：**VaVAM 代码冻结 VaViM**（论文未声明）→ 新增第四种形态：**机制在代码里且被走到，但训练被冻结**（前三种：配置全关 / 只实现一半 / 根本没发布）。
3. **两篇新补论文都不可复现，但原因不同**：Reasoning-VLA 是**空壳仓库**（有名无内容），CF-VLA 是**项目主页冒充仓库**。加上 AutoMoT（核心模块未发布）、LaST-VLA（功能项全未勾选）、SpanVLA（无仓库）→ **"有代码"这一档到本轮已积累七种形态**：完整 / 关键部分未发布 / 训练脚本未发布 / 只有项目页 / 核心模块未发布 / 有仓库但功能项全未勾选 / **仓库为空壳**。
4. **"反事实 / 自反思"这类机制引用前必须看有没有真仿真**：CF-VLA 的 "counterfactual" 是**教师模型的 hindsight 诊断文本**，不是反事实前向仿真；其受控对照显示**推理本身只值约 3%，而"重采样高分样本"就值 5%** → 与 DriveFuture 的"条件化 +2.5 vs 直接辅助损失"同类，**"看起来更高级的机制"往往被更朴素的数据/后处理对照吃掉**。

## 12. NuInteract（VLA-21）的全文 + 代码核验（第二十五轮新增）

**结论：它是"理解侧"的数据集 + 理解侧模型，不是 VLA 规划器。** 论文自己承认这一点，代码也印证。

- **是什么**：**NuInteract 是数据集**（基于 nuScenes **全自动标注**：**850 场景 / 34 K 帧 / 239 K 图 / 1.5 M pairs**，§III-A/B、Tab.I）；**DriveMonkey 是建在其上的框架**——LLaVA 式 LVLM + **可插拔 spatial processor**（取预训练 **PETR** 的 backbone + 位置编码作 spatial encoder、检测头作 decoder），用 **30 个可学习 query** 桥接 LLM 与检测器（§IV-B、Fig.4、式(3)）。**3D grounding** = 依指代表达式定位目标并回归 3D bbox（focal + L1，式(4)）。
- **⚠ 与规划的关系（最关键的一条）**：**它是理解侧，不是规划器**。三条依据——① §III-A 明确 **planning 的答案是 high-level command（左转 / 右转 / 直行），不是轨迹**；② **§VI Limitation 自述** "planning tasks only concentrate on **high-level commands rather than specific trajectories**, without comparison with advanced end-to-end autonomous driving systems"；③ **源码印证**——planning 集合的 `max_new_tokens: 10`（`internvl_chat/eval/nuscene/evaluate_nuscene_bev.py:38-43`），**全仓 243 文件无任何 trajectory / waypoint 代码**，输出只有文本 + 2D/3D box。
- **关键数字（Tab.II，NuInteract test）**：DriveMonkey（InternVL2-8B）Avg **52.12**；**3D VG Pr 51.90 / mAP 34.53 / F1 20.86** vs 同 backbone InternVL2-8B **31.47 / 24.67 / 14.70**（mAP +9.86、Pr +20.43）；**Plan Acc 82.64 vs 46.93**。**⚠ 2D VG 反而略低**（mAP 19.47 vs 20.61、MIoU 59.36 vs 61.90）。数据来源是 **nuScenes train+val 自动标注**，测试集取自 nuScenes val（§V-A），**非自采**。
- **消融**：**backbone（Tab.IV）** MiniCPM-V2 Pr 31.80 / mAP 11.39、Qwen2VL-7B 23.79 / 11.06、InternVL2-8B 51.90 / 34.53；**检测器（Tab.V）** BEVFormer（单帧）mAP 30.87 / F1 17.85、CAPE 31.51 / 19.00、**PETR 34.26 / 20.48**；**query 数（Tab.VI）10 → 900**：Pr 43.94 → 58.47 **但 mAP 33.10 → 7.12**（默认 30）→ **存在精度—召回权衡**；**去 3D PE（Tab.VII）**：Pr/mAP 42.13 / 21.10 → 51.66 / 34.26；**随机初始化优于 avg / max**（mAP 34.26 vs 25.50 / 30.91）。
- **输入权限**：**6 路环视**（FL/F/FR/BL/B/BR，`evaluate_nuscene_bev.py:192-213`）、**448×448**、**单帧无历史**（§VI）；**无 LiDAR、无地图、无自车状态 / 导航命令输入**（建模侧虽有 `can_bus` 形参，**eval 调用只传 cams / pixel_values**）。PETR encoder 需相机标定。
- **代码核验：真实发布**——`zc-zhao/DriveMonkey`，47 star，创建 2025-01-15 / 最后推送 2026-03-20，Apache-2.0；README `[2026/03/20] DriveMonkey code and dataset are now released!`；**数据在 GitHub Releases**（tag `NuInteract_Dataset`：`cap_public.tar.gz` 85.2 MB、`NuInteract.zip` 203.3 MB）、**权重在 HF `zczhao/DriveMonkey`**（2B/8B + Pretrain 2B/8B）、**含训练 / 评估脚本与 4 个 finetune shell**。硬编码本机路径：`evaluate_nuscene_bev.py:52-59` 为 `/mnt/vol1/zhaozc_workspace/...`。
- **可疑点**：① **arXiv 仍是 v1（2025-05-13）**，`comments` 仍写 "will be released"、无 `journal_ref` → **TIP 2026 未在 arXiv 体现**；② §V-C 称 accuracy 提升 5.8%，**Tab.III(a) 实为 64.3→69.1 / 65.1→69.9（+4.8），对不上**；③ **评测脚本 `--data_lenth` 默认 None → val 只随机取 500 条**，与论文全测试集口径可能不一致；④ **无 planning 指标脚本**（`calculate_metric/` 只有 2D COCO 与 3D map/pr3d）。

**本条判断**：**"数据集论文"在 VLA 侧要单独归类**——NuInteract 的 venue（TIP 2026 / CCF-A）与数据规模都是真的，但**它不产出轨迹**，**不能计入"VLA 规划器"这条线**。→ 与 VLA-28 DriveAction（Li Auto 的动作决策基准）同类：**都是"理解 / 决策侧"资产，可作为评测或辅助数据，不是对手也不是基线**。

## 13. EMMA（VLA-09）与 CoVLA（VLA-10）的全文核验（第二十五轮新增）

两篇都在本表最早期（第一轮建表时）收录、长期只有摘要级；本轮补全文。**两篇恰好构成"语言中间层"的两种对照做法**。

### 13.1 EMMA（VLA-09）——**"轨迹即文本"的第二个实例，且语言中间层有受控消融**

- **它是什么**：**模型，不是数据集**——基于 **Gemini 1.0 Nano-1** 微调的 MLLM（另有 PaLI-X 变体 EMMA†），是**多任务通用模型**：端到端规划 + 3D 检测 + 道路图估计 + 场景理解（临时封路检测）（§2.3、§3.5）。**规划只是其中一个任务**，不是专门的规划器。
- **与规划的关系**：**纯生成式、自回归 next-token**——所有非传感器输入与输出**统一表示为自然语言文本**（§2 原文 "representing all non-sensor inputs and outputs as **natural language text**"）；**轨迹被写成纯文本浮点数** `{(x_t, y_t)}`，作者明确在"直接文本数字 vs 特殊 token"两种表示中**选择了文本**（§2.1）→ **无回归头、无特殊 token、无扩散 / 流匹配**，是"**轨迹即文本**"的**第二个实例**（第一个是 VLA-12 Impromptu VLA，见 §8.1）。
- **关键数字**：nuScenes 开环（Table 3）EMMA 1/2/3 s L2 = 0.14 / 0.29 / 0.54，**Avg 0.32**；**EMMA+ Avg 0.29**；基线 UniAD 0.66、DriveVLM 0.40、VAD 0.37、OmniDrive 0.33、BEV-Planner 0.35。WOMD（Table 2）EMMA+ (w/ CoT) 1/3/5 s L2 = 0.027 / 0.203 / 0.543，优于 MotionLM 0.696、Wayformer 0.628（5 s 相对提升 13.5%）。**⚠ 未在 NAVSIM 上评测**（NAVSIM 只作为"更可信开环评测"的 future work 被引用，§A.5）。
- **✅ 语言中间层的受控消融（Table 4）**：基线 **+0.0%** → 场景描述 +0.0%（中性）→ **关键物体 +1.5%** → **元决策 +3.0%** → 物体 + 元决策 **+5.7%** → **四项全开 +6.7%**。→ **这是本工作空间第一条"语言中间层值多少分"的量化证据**，且**与"世界模型 +5.0 / 换动作头 +5.2 / 加 goal 条件 +4.7"同一量级**。**换 backbone**（Table 2）：Gemini → PaLI-X 在 1 s/3 s 更好、**5 s 反而退化到 0.797（劣于 Wayformer 0.628）**。
- **输入权限**：**环绕相机视频（最多 4 帧）** + 高层路由指令 + 历史自车状态（BEV 路点文本，可扩展速度 / 加速度）；**相机-only、HD-map-free**；**无 LiDAR / 雷达 / 地图**（§A.5 列为局限）；**分辨率、帧率、相机路数均未给出**。
- **⚠ venue 更正**：**arXiv `comments` 显示 "Accepted by TMLR"**（并附 OpenReview `kH3t5lmOU8`）→ 本表此前记的"**仅预印本（T4）**"应更正为 **TMLR 录用**（TMLR 不在 CCF 目录，但属正式期刊）。
- **代码**：确认**无官方代码**，项目页是 Waymo blog；GitHub 搜索只返回第三方（LightEMMA、OpenEMMA 等）。
- **可疑点**：① **口径冲突**——§3.2.2 与 Table 3 表题给"相对 BEV-Planner +17.1%、相对 OmniDrive +12.1%"，这两个数对应的是 **EMMA+（0.29）** 而非表中 "EMMA" 行（0.32）；表题又另写 "supervised +6.4%"，该数在 Table 3 中**找不到对应基准**；② Table 2 表题写 "internal planning benchmark"，正文 §3.2.1 却在 WOMD 上并称 "align with WOMD"；③ **检测 F1 口径不对等**（EMMA 用单点 precision/recall，其他方法取 F1-max，§3.4）；④ **Table 5 的 e2e planning 增益 "+1.4% (±2.8%)" 标准差大于均值**，统计上不显著；⑤ nuScenes 只报 top-1、WOMD 用 K=24 取中位数，**两基准协议不同**。

### 13.2 CoVLA（VLA-10）——**数据集为主，附带基线；轨迹用"特殊 token + 回归头"（与 EMMA 相反）**

- **它是什么**：**以数据集为主**（CoVLA-Dataset），附带一个基线模型 **CoVLA-Agent**（§4.1）；贡献顺序也是数据集优先（§1 三条贡献）。
- **数据规模**：**10,000 个 30 秒场景、83.3 小时、6,000,000 帧**（原始数据 1,000+ 小时）。标注**全自动、无人工**：轨迹由 GNSS/IMU 经**卡尔曼滤波**估计；红绿灯用 OpenLenda-s、前车用雷达 + 相机融合；字幕先规则生成再由 **VideoLLaMA2-7B** 增强 → **100,000 条 VLM 字幕 + 6,000,000 条合并字幕**。
- **与规划的关系**：CoVLA-Agent 是**自回归 VLM**（Llama-2 7B + CLIP ViT-L 224×224），**有轨迹输出**：字幕用自回归文本生成，**轨迹用"特殊 token 作 query → MLP 回归头 → 10 个 (x,y,z) 坐标**（§4.1），3 秒时域。→ **语言是中间层（先生成字幕再出轨迹），但轨迹不是自由文本而是回归头**——**与 EMMA 的"轨迹即文本"正好相反**，构成同一问题的两种做法对照。**非扩散 / 非流匹配**。
- **关键数字**：**只在自有数据集上评 ADE / FDE，无任何外部 benchmark（无 NAVSIM / nuScenes）、无基线方法对比**（Table 2）。ADE / FDE 公式**含 z 项**（§4.2）→ 而轨迹 z 分量近 0，**口径非常规**。条件对比：预测字幕 ADE 0.955 / FDE 2.239；**GT 字幕 ADE 0.814 / FDE 1.655**。
- **✅ 语言中间层的受控对照 = "预测字幕 vs GT 字幕"**：用 GT 字幕时 **ADE 降 14.8%、FDE 降 26.1%**（Table 2）→ 与 EMMA 的 Table 4 是同一问题的两种测法，**结论一致：语言中间层的质量直接影响轨迹**。另有逐词误差分析（Table 3：deceleration / left / acceleration 等**运动词**误差最大）。
- **输入权限**：**单路前视相机**（原始 1928×1208、20 FPS；模型用 CLIP ViT-L 224×224）+ **自车速度标量** + 文本指令；**单帧、无历史帧**（作者归因于此导致"意图难估计"，§4.4）；**无导航命令、无 LiDAR、无地图**。
- **代码**：确认**无代码**；数据在 HF `turing-motors/CoVLA-Dataset`；项目页 `turingmotors.github.io/covla-ad/`。
- **可疑点**：① §4.3 写 "we present **qualitative** results in Table 2"，但 Table 2 实为**定量表**；② **ADE 定义含 z** 而 z 近 0；③ Table 1 的 Action 列标 "GPS/IMU"，方法列与 Vision 列排版混乱；④ 数据集 80 vs 83.3 小时、6 M 帧 vs "10,000 clips" 属**口径混用**。

### 13.3 两条判断（本批）

1. **"语言中间层"的收益第一次被两篇独立量化，且量级与"世界模型 / 生成机制 / 条件"三维相当**：**EMMA Table 4 四项全开 +6.7%**、**CoVLA 用 GT 字幕 ADE 降 14.8% / FDE 降 26.1%**。→ 加上已有的 **DriveLaW 世界模型 +5.0 PDMS**、**SpanVLA 换动作头 +5.2**、**GoalFlow 加 goal 条件 +4.7**、**DriveFuture 加未来条件 +3.7** → **四条"机制轴"的受控收益都在同一量级（+4 ~ +7）**，**没有任何一轴"远大于"其他轴**。这是本工作空间到目前为止**最稳定的一条跨论文结论**。
2. **"轨迹怎么表示"至少有四种做法，且各有失败模式**：**纯文本数字**（EMMA、Impromptu VLA → **依赖解析器，格式脆弱**）/ **特殊 token + 回归头**（CoVLA）/ **离散轨迹词表**（VADv2 → DiffusionDrive，4096 / 20 锚点）/ **连续回归或生成**（SpanVLA、VaVAM）。→ **引用任何"VLA 输出轨迹"的说法前，必须先问"轨迹是以什么形式生成的"**，因为这决定了它的失败模式（解析失败 vs 词表覆盖不足 vs 回归平滑过度）。

## 14. 剩余 5 篇的全文核验（第二十五轮新增，**本表 28 篇至此全部读过全文**）

### 14.1 DriveGPT4（VLA-01）——**单步控制，且开源承诺只写在项目网页上**

- **架构与动作输出**：MLLM / VLM 路线——CLIP ViT + Valley 式视频 tokenizer + **LLaMA2**（§IV-A）。**属生成式、自回归文本 token**：语言解释与控制信号**共用同一个 text de-tokenizer**（仿 RT-2），控制量以固定格式数字嵌在文本里（Tab. II 例：`speed 2.09`、`turning 0.00`）→ **不是连续回归、不是轨迹坐标**。**控制量 = 下一时刻车速（m/s）+ 转向角（度，相邻帧相对角），单步、非多点、非轨迹**；帧率论文未给（8 帧/clip）。
- **与规划的关系**：**仅开环单步控制**（Tab. VI），**无闭环**；§VI 明言闭环留待将来。
- **关键数字**：Tab. IV/V 全测试集 **CIDEr 99.10 / B4 18.32 / ROUGE 44.73**，优于 ADAPT 85.38 / 17.40 / 43.04（Hard 子集优势最大）；Tab. VI 控制 **speed RMSE 1.30 / turning 8.98**（ADAPT 3.02 / 11.98）；Tab. VII 附加问答 ChatGPT 评分 81.62 vs Valley 43.23。
- **受控消融（Tab. VIII）**：**去 mix-finetune → CIDEr 99.10→76.51、speed RMSE 1.30→4.67**；去 ChatGPT QA → 问答 CIDEr 56.34→9.96；**无换 backbone 消融**。
- **输入权限**：**前置单目 RGB、8 帧均匀采样**；文本输入含当前车速与视频时长；**不用 LiDAR / 地图 / 导航命令**。
- **⚠ 承诺开源的原文位置更正**：**"The code and dataset will be publicly available" 只出现在项目网页上、不在论文里**（论文正文只写 "The webpage … is available at …"，原文措辞已确认）→ 引用其"承诺开源"时必须写明出处是项目页。**官方 GitHub 无此仓**（作者 `tonyxuqaq` 无；GitHub 搜索只有第三方 `tljcpa/drivegpt4-mini`，0 star）；**项目页的 Code 链接指向清华云盘 Seafile 分享**（非 GitHub）。
- **可疑点**：① 量化仅 BDD-X，nuScenes / 游戏只做零样本定性（Fig. 4/5），**未在 CARLA / NAVSIM / Bench2Drive 上评测**；② 控制是**开环单步**；③ ChatGPT 评分"不稳定"，取 3 次均值；④ **8 帧 vs ADAPT 32 帧**，作者自认局限。

### 14.2 ADriver-I（VLA-02）——**"扩散预测未来帧 + MLLM 出动作"是两件事，只部分落在世界模型线上**

- **架构与动作输出**：MLLM（**Vicuna-7B-1.5 + CLIP-ViT-L + 2×MLP adapter**）+ **视频潜扩散 VDM**（SD2.1 + temporal）。**动作由 MLLM 自回归出文本 token 数字**（**不是 MLP 回归**；MLP 只是 baseline "a"，Fig. 4）；控制量 = 当前帧 speed（m/s）+ steer angle（rad），3 位小数、×1000 转整数（§4.1）。
- **⚠ 与规划的关系（要拆开）**：**VDM 预测的是未来帧图像，不是动作**（Fig. 1 / §3.1，4F→4F）；**单步控制实验用的是真实帧，动作不经过扩散中间产物**；**只有"无限驾驶"（§4.5）里生成帧才回灌 MLLM 出下一步动作**。→ **判定：仅部分落在"世界模型 → 规划器"这条线上**——VDM 是**隐式闭环模拟器**，规划本身仍由 MLLM 直接完成（依据 Tab. 1、Fig. 1、Discussion (1)(3)）。
- **关键数字**：Tab. 2 nuScenes **speed L1 0.072 / steer 0.091**，优于 MLP / CNN / ViT baseline（0.122 / 0.101 等）；**私有集 0.035 / 0.015**。Tab. 6 **FID 5.5 / FVD 97.0**（vs DriveDreamer 52.6 / 452.0、DriveGAN 73.4 / 502.3）。
- **消融**：Tab. 3 编码方式（Absolute 0.072 最优、Num2English 2.094 最差）；Tab. 4 小数位（2 ≈ 3 位）；Tab. 5 多轮对话优于单轮（0.072 vs 0.078）。
- **输入权限**：前置单目、输入 336×336、**3 组历史 vision-action pair + 当前帧**；**不用 LiDAR / HD 地图 / 框**（Tab. 1 自称 w/o Box、w/o HD Map）；VDM 256×512、长度 8。数据 = **自采私有高速约 1.4 M 对 + 公开 nuScenes**（VDM 微调约 23 K 视频），**未给小时数**。**训练 / 推理不同**：训练多轮监督 `{A'_{t−2..t}}`、推理单步出 `A'_t`；两模块分开训练、推理合体。
- **可疑点**：① 摘要 FID 5.52 vs Tab. 6 的 5.5（口径微差）；② **FID / FVD 与 DriveDreamer / DriveGAN 的输入输出帧数不同**（4F→4F vs 1F→12F）→ **跨设置比较不公平**；③ **最优数字在私有集、头条数字在 nuScenes，两口径并存**；④ **训练多轮 / 推理单步不一致**；⑤ "无限驾驶"仅定性（Fig. 7），自认 VDM 快变向时画质差。

### 14.3 SafeAuto（VLA-05）——**⚠ 是 MLN 一阶逻辑，不是"模糊逻辑"；否决靠重新 prompt**

- **它是什么**：MLLM 驾驶框架（**Video-LLaVA + Vicuna-7B**），三件套 = **PDCE 损失 / MLN 安全核 / 多模态 RAG**；论文自称"可插拔安全层"（§3–4），**非闭环规划器**。
- **与规划的关系**：**非生成式规划架构**——LLM 自回归生成**文本**控制信号（BDD-X：下一帧 speed / course；DriveLM：3 s 轨迹文本），再由符号层否决高层动作。
- **⚠ 更正（本轮）**：**论文全篇用 "MLN / 一阶逻辑"，没有 "fuzzy" 字样** → 此前记的"**10 条模糊逻辑硬规则**"应更正为"**10 条 MLN 一阶逻辑硬规则**"。
- **10 条硬规则原文**（论文 Tab. 17 前 10 条 = 代码 `pgm/config.py:48-98`，`hardrule_num=10`）：`SolidRedLight ⟹ ¬Accelerate ∧ ¬LeftPass ∧ ¬Yield`；`SolidYellowLight ⟹ TurnLeft ∨ TurnRight ∨ Keep ∨ Stop ∨ Decelerate ∧ ¬Accelerate`；`YellowLeftArrowLight ⟹ Stop ∨ Decelerate`；`RedLeftArrowLight ⟹ ¬(TurnLeft ∨ UTurn)`；`MergingTrafficSign ⟹ Decelerate`；`NoLeftTurnSign ⟹ ¬TurnLeft`；`NoRightTurnSign ⟹ ¬TurnRight`；`RedYieldSign ⟹ Decelerate`；`SlowSign ⟹ ¬Accelerate`；`StopSign ⟹ Stop ∨ Decelerate ∧ ¬PullOver`。
- **⚠ 规则无阈值**：规则是**乘积 t-范数的可微松弛**，**权重靠训练学习**（`pgm/ckpts/pgm/bddx_weights.npy`）；论文只给 lr / 正则 1e-5、300 epoch，**未报权重值**。注意 **DriveLM 侧 `hardrule_num=15`**（`config.py:214`），共 29 条公式。
- **⚠ "否决"的实现方式**：**不改数值输出，而是重写高层动作查询并重新 prompt**（§3.2、A.5：BDD-X 追加 "The ego vehicle should stop"；DriveLM 删错选项后重生成）→ **是重采样 / 重提示，不是降级到安全动作**。
- **PGM 结构**：MLN——未观测动作谓词 U + 观测谓词 O（MLLM 动作 + 环境），`argmax_U P(U|O)`，枚举有限可能世界（Tab. 18/21）。BDD-X：16 动作 / 20 环境 / 35 公式；DriveLM：7 / 29 / 29。
- **关键数字**：BDD-X action **CIDEr 337.4**（SOTA 260.8）、speed RMSE 0.65、course 3.85；DriveLM Acc 74.60、ADE 0.84。**规则违例率 11.64%→4.50%**（BDD-X）、1.03%→0.75%（DriveLM）（Tab. 15）。
- **⚠ 受控对照的边界**：有"去否决层"对照（Base vs PDCE+MLN+RAG），但**无碰撞率、无闭环**——只评 BDD-X 与 DriveLM 开放集，**未评 NAVSIM / CARLA / nuScenes 闭环**；且 **MLN 的边际极小**（action Acc **91.00→92.18**、74.01→74.60）。
- **输入权限**：BDD-X 视频 8 帧 + 过去 7 帧控制信号（speed / curvature / accel / course）；DriveLM 当前帧 **6 路环视**（谓词只用前 / 左前 / 右前）+ 过去 3 s 轨迹，并用 nuScenes 地图车道线（A.3）。**无 LiDAR**；有自车历史状态；导航命令未取得。
- **代码**：`AI-secure/SafeAuto` **完整**（训练 + RAG + `pgm/` + 权重，217 文件），`pgm/config.py` 与论文 Tab. 17/20 **逐条对应**。
- **可疑点**：① 摘要 CIDEr "28.0%" vs §4 "29.4%"（Tab. 1 算得 29.4%）；② §4 BLEU4 "11.6%" vs Tab. 1 算得 12.5%；③ 摘要 "13.0%" 绝对 / 相对口径混用；④ **Tab. 2 的 SafeAuto Speed 81.61 vs Tab. 5 同配置 79.85 冲突**；⑤ Tab. 14 表头 BDDX / DriveLM 数值错位；⑥ justification 实际低于 RAGDriver。

### 14.4 Impromptu VLA（VLA-12）——**prompt / parser / 论文三方口径不一致（本轮补上第三方）**

- **它是什么**：**数据集 + 微调配方**（**不是新规划架构**）。核心 **Impromptu VLA Dataset**：约 **80 k clips**（由 8 个开源数据集 2 M clips 蒸馏，四类非结构化场景）+ 规划导向 Q&A；模型 **Qwen2.5-VL 3B / 7B**（LLaMA-Factory 微调）。"Impromptu" = 非结构化 / 临时 corner case（边界不清、临时交规、非常规障碍、恶劣路况）。
- **与规划的关系**：**生成式，VLM 直接自回归出文本轨迹**（trajectory-as-text），**无 diffusion、无候选选择**。
- **⚠ 轨迹口径三方不一致（本轮补全）**：**论文**称数据集"过去 1.5 s + 未来 5 s"（§2.3、附录 C），nuScenes 评估"过去 / 未来各 3 s"（A.1）；**代码训练 prompt** 写 "next 3 seconds（0.5 s 间隔）" = 6 点（`prompt_planning.py:225-233`），**闭环推理 prompt 仅 "next 3 timesteps"**（`server.py:272`），**解析器 `traj[:6]`、失败返回全零 6 点**（`server.py:102-113`）。→ **prompt(3 步) / parser(6 点) / 论文(5 s) 三方不一致**；且**训练 prompt 用 `[displacement, theta]`（米 / 度）、推理 prompt 用 `[x, y]`，语义亦不一致**。
- **关键数字**：NeuroNCAP **NNS 1.77→2.15、碰撞率 72.5%→65.5%**（Tab. 2）；nuScenes 开环 avg **L2 0.30 m**（EMMA+ 0.29 m）（Tab. 4）。
- **⚠ 受控消融的缺口**：**只有"Base vs Base+Impromptu"的数据消融**，**无"CoT 对齐动作"的受控消融**——`<PLANNING>` / `<DYNAMIC_OBJECTS>` 特殊 token 仅定性说明（附录 C）；且 Tab. 2/4 多为**借用的外部数字**（论文注明 sourced from）。
- **输入权限**：图像**仅前视**（nuScenes 训练 "only front-camera"，A.1），**闭环推理用前 / 左前 / 右前 3 路**（`server.py:272`）；2 Hz；分辨率超参 262144（=512²）；自车状态 = 过去 1.5 s / 3 s 位移 + 速度 + 加速度，nuScenes 另加方向盘角；**无 LiDAR、无地图**；导航命令字段存在（`server.py:57`）**但未入 prompt**。
- **可疑点**：① Tab. 1 源数据集列 NAVSIM，正文却引 nuPlan（[8]）；② **Tab. 2 的 Static 子项反而变差**（NNS 1.80→1.77、碰撞 68%→70%），摘要只报均值改善；③ 借用数字与自测混排；④ **前视训练 vs 3 路推理**。

### 14.5 DriveAction（VLA-28）——**动作根树三层结构，且明确不含轨迹**

- **它是什么**：**首个"动作驱动"VLA 基准**，**16,185 QA / 2,610 场景**；数据由公司运营自动驾驶车的**驾驶员主动贡献**（driver-contributed），覆盖 **148 城**、量产全车型（§3.1），7 类场景（Tab. 2）。
- **动作根树结构**（§3.3.1 / Fig. 1）：**三层树**——**顶层动作节点（决策输出）→ 中层语言任务 → 底层视觉任务**；动作是根，动作决定所需语言任务，语言任务再映射视觉任务，**但推理仍按 V-L-A 顺序**。共 **14 个任务（7 视觉 + 7 语言）**；Table 1 的评价逻辑列为 "Tree"。离散动作示例：forward-left/right、lane change L/R、bypass L/R、left/right/straight/U-turn/stop/decelerate、keep（Tab. 2）。**动作类别总数论文未给**。
- **QA 与标签生成**：动作标签取自**驾驶员实时操作 + 多轮人工校验**（§3.2）；QA 由两阶段 LLM prompting 生成候选、再人工筛选（App. B.2）。
- **⚠ 是否含轨迹：否**。§3.2 明示**放弃高频轨迹、只取关键点离散决策**；HF 数据集字段仅 **QA + `image_0-2`**（HF API / App. A），**无轨迹字段**。→ **不能做轨迹级规划评测**（无 waypoint、无闭环仿真、无 L2 / 碰撞率，只有 accuracy）。
- **关键数字**：12 个 VLM，最好 **o1 V-L-A 93.56%**、Gemini 2.5 Pro 91.86%、GPT-4.1 mini 91.43%（Tab. 3）；四模式均值 90.71 / 86.63 / 87.42 / 82.69。自研车端模型 Non-MOE 0.5B **67.40** vs MOE 8×0.4B **79.78**（Tab. 6）。
- **输入权限**：**3 张连续帧 + 导航指令 + 自车 / 目标车速度**（§3.3.2、App. A）；**分辨率、帧率、相机路数、LiDAR、地图、CAN 状态均未提及**。
- **可疑点**：**Table 3 与 Table 19 数字冲突**（GPT-4.1 mini V-L-A 91.43 vs 91.67；Gemini 91.86 vs 91.30；A 模式 85.72 vs 84.66）。**无代码仓库**（只有 HF 数据集 `LiAuto-DriveAction/drive-action`，16,185 条、CC-BY-4.0、5.5 GB）。

### 14.6 三条判断（本表结账）

1. **"VLA 阶段 1（解释器）"两篇的代表作都不是规划器**：**DriveGPT4 只做开环单步控制**（车速 + 转向角，非轨迹，且闭环是 future work）、**ADriver-I 的规划由 MLLM 直接完成**（VDM 只生成未来帧）。→ **引用"VLA 能做规划"时，不能从这两篇取证**；它们对研究对象的直接价值是**"文本即控制"的早期形态**（与 EMMA / Impromptu 的"轨迹即文本"同源）。
2. **"安全层"这一类目前只有 SafeAuto 一个可读实现，而它的证据强度被两件事限制**：① **否决 = 重新 prompt**（不是数值级投影或降级）；② **只评开放集、无碰撞率、无闭环**，且 **MLN 的边际只有 ~1.2 个准确率点**。→ 对方向 A（约束注入）而言，**"符号否决层"仍是一个未在闭环下被验证的选项**。
3. **"基准"与"规划器"必须分开引用**：本表末尾三篇（**NuInteract / DriveAction / CoVLA**）都是**数据集或基准**，其中 **DriveAction 明确不含轨迹**、**NuInteract 的 planning 只出 high-level command**、**CoVLA 只在自有数据上评 ADE/FDE**。→ **VLA 侧"能当规划基线"的资产，比表里看起来的少**。
