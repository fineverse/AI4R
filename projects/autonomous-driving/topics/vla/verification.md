# VLA（自动驾驶侧）· 全文与代码核验详细结论

更新时间：2026-09-23  
用途：保存 VLA 表 28 篇的**逐篇全文核验与代码级核验结论**（§4–§14）。  
来源：2026-09-23 从 [papers.md](papers.md) 机械拆分，内容未改动。

## 4. 已读全文

### 4.1 第一轮（2026-09-23，3 篇，有独立笔记）

| 编号 | 笔记 | 本次读到的关键新增事实 |
|---|---|---|
| VLA-06 | [DiffVLA](notes/VLA-06-diffvla.md) | **性质澄清：这是 Bosch 的 NAVSIM v2 竞赛技术报告，非正式论文**；锚点 **32 个**（vs DiffusionDrive 20）；**加了扩散规划器后碰撞（95.71→81.27）与车道保持（97.14→59.85）子指标显著变差**；用"y 轴 2% 减速"后处理避碰 |
| VLA-07 | [ReCogDrive](notes/VLA-07-recogdrive.md) | **推理 13.3 Hz**（对比 VLM 直出轨迹仅 0.9–1.7 Hz）；NAVSIM PDMS **90.8 且纯相机**，超相机+LiDAR 的 DiffusionDrive +2.7；EP 87.3（+5.1）；但 Bench2Drive **Comfort 仅 17.45** |
| VLA-08 | [KnowDiffuser](notes/VLA-08-knowdiffuser.md) | 把 **GPT-4o 放进规划回路**；nuPlan Test NR 86.94 / R 81.10；**未与 DP-A01（Diffusion Planner）对比**；只给定性延迟声明，无 Hz/ms |

### 4.2 第二轮（2026-09-23 第二十一轮，4 篇，并入本表不另开笔记）

| 编号 | 论文 | 全文核验到的关键事实（表号/节号为论文原文位置） |
|---|---|---|
| VLA-03 | OpenDriveVLA | **自回归离散 token**（非扩散、非回归），nuScenes 开环 **3 s / 6 waypoint @0.5 s**（§III-E）。纯视觉（ResNet-101 + FPN + BEVFormer），**无 LiDAR**；特权 = ego 状态（文本）+ 高层命令 + 历史轨迹；**无轨迹词表/锚点、无多模态候选、无 selector**。数字（Table I）：**同一模型在两套口径下差一倍**——OpenDriveVLA-7B 按 **ST-P3 口径** L2 Avg **0.33 m** / 碰撞 0.10%，按 **UniAD 口径** L2 Avg **0.66 m** / 碰撞 0.25%（3B / 0.5B 同量级）。训练 4×H100 约 2 天（§VI）。**未报延迟/FPS** |
| VLA-04 | DriveMoE | **直接建在 π0 之上**（§3.1 标题即 "Drive-π0 Baseline"）——把**具身侧的 π0 VLA 基础模型**搬到驾驶再加 MoE，是"具身 → 驾驶"迁移的现成案例。输出是 **flow matching 生成的连续轨迹、10 个 waypoint**；Action MoE = **1 共享 + 6 非共享专家、top-3 激活**（§4.2），门控用**技能标签交叉熵**监督（Eq.5）+ 负载均衡损失。输入 = 2 张连续前视 + **路由选出的 top-1 动态视角**，无 LiDAR、无地图；特权 = 路线规划器给的 goal waypoint（§3.3）。Bench2Drive 闭环 **DS 74.22 / SR 48.64%**（Table 2），对比扩散类 **DiffAD 67.92**、GenAD、VAD 42.35。**未报延迟/FPS**；**论文与项目页均未给 GitHub 仓库**，只写 "will release" |
| VLA-11 | AutoVLA | 自回归**离散 action token**：5 s 轨迹 = **10 个 token** @0.5 s（§3.1）。先验是 **K-disk 聚类的 action codebook、K=2048**（Table 4 / App. A.1），**只作最近邻离散化目标**（既非扩散起点、也非候选池）。**best-of-N（N=6）+ oracle scorer**（Table 1、§4.2）——**"oracle scorer"是论文原文，选优需真值侧打分**，见 §5.1 的口径限定。**NAVSIM PDMS 92.12（best-of-N）/ 89.11（RFT）/ 80.54（one-shot）**；nuScenes L2 0.71 / 碰撞 0.35；Bench2Drive DS 78.84 / SR 57.73%；Waymo RFS 7.5566。论文写 **GRPO**：奖励 `r = r_Driving − λ·r_CoT`、KL β=0.04（§3.4），并用 **CoT 长度惩罚**做快慢思考切换；延迟 fast **1.072 s** / slow **10.518 s**（Table 2）。**官方代码已发布**（`ucla-mobility/AutoVLA`）→ **代码核验发现两处与论文不符（无 clip、组是跨 GPU 的批），见 §5.1** |
| VLA-18 | ExploreVLA | **生成与回归解耦**：自回归离散 token 生成**未来 RGB 与深度**（MAGVIT-v2 码本 **K=8192**、16×16 patch，**只用于图像 token 化**，不是轨迹先验），轨迹由**轻量 MLP head 回归连续 waypoint**（§3.3）。**单前视相机**（当前 + 0.5 s 前一张）+ 语言命令 + ego status，**无 LiDAR、无地图、无其他智能体轨迹**。**best-of-N N=6**；GRPO 用 **G=8 组内相对优势** + 世界模型预测不确定性作**内在奖励** + **PDMS 安全门控**（§3.5 Eq.5–8）。**NAVSIM v1 PDMS 93.7（best-of-N）/ 90.4（无 best-of-N）；v2 EPDMS 88.8**；4×H200。**论文与项目页均无 GitHub 仓库**（§1 的"有代码"已更正） |

### 4.3 第三轮（2026-09-23 第二十二轮，4 篇，并入本表不另开笔记）

| 编号 | 论文 | 全文核验到的关键事实（表号/节号为论文原文位置） |
|---|---|---|
| VLA-15 | ORION | **非自回归**：LLM 只出 **1 个 planning token**（§3.2 Eq.3），再由 **VAE + GRU** 解码成轨迹（§3.3 Eq.4–5）；**anchor-free**，输出 **6 条模态**（对应 6 个导航命令，§4.2）。multi-view 图像、**不用 LiDAR**、**HD map-free**；额外用 **memory bank + history queries**（§3.1；Tab.5 最优 `N_h=16`）、文本指令、交通状态/运动预测辅助头（Tab.4）。**无词表/码本**（仅其**扩散消融版**用 K-means 轨迹锚点 20 模态，§4.5 Tab.3）；**无 selector/scorer/best-of-N、无 RL**。Bench2Drive base **DS 77.74 / SR 54.62%**、L2 0.68（Tab.1），mean ability 54.72%（Tab.2）；nuScenes 开环 L2 **0.34 m** / 碰撞 0.37%（Tab.A1）。**未报 FPS/延迟**；**无与扩散规划器的数字对比**——只自比 diffusion 71.97/46.54 vs VAE 77.74/54.62（Tab.3）。训练 **32×A800 80GB**（§4.2）。**官方代码已发布**（`xiaomi-mlab/Orion`，ICCV'25）→ **代码核验见 §7.1** |
| VLA-16 | MindDrive | **两段式**：Decision Expert 自回归出**离散 meta-action**（**7 速度 + 6 路径**，§0.C）；Action Expert 用 `<speed_waypoints>/<path_waypoints>` token 取 logits，再 **VAE + GRU** 解码（§3.2 Eq.6–7）。speed **6 点 / 3 s / 2 Hz**；path **20 点 / 1 m 间隔 / 共 20 m**（§4.1）。multi-view 图像 + instruction，**无 LiDAR**；IL 阶段用 GT 轨迹与 GT command 造 meta-action 标注（§0.C）。**无轨迹码本**（决策空间 7+6 = 13 个 meta-action）。**有"学到的选择器"π_d**（§3.1 Eq.1–3）+ **RL**：稀疏奖励 **±1**（到达 +1；碰撞/闯红灯/偏航 >30 m/不停车 −1，Eq.9）、**用仿真事件而非真值**。Bench2Drive：0.5B **DS 78.04 / SR 55.09%**、3B **DS 80.59 / SR 58.26%**（Tab.1）。**有延迟**：A100 上约 **540 ms**（视觉编码器 ~400 ms、两专家各 ~50 ms），对比 ORION ~1106 ms、ReCogDrive ~750 ms（Tab.7）。**无与扩散规划器对比**。**官方代码已发布**（`xiaomi-mlab/Minddrive`，ECCV'26）→ **代码核验见 §7.2（是完整 PPO）** |
| VLA-17 | Drive My Way | **基座 + 残差**：**基座就是 SimLingo**（出 waypoint → 基动作），残差解码器（MLP + **categorical action head**）出两个离散残差（速度/转向），再过 **PID**（§5.1–5.2、Fig.3）；数据采集 5 Hz。**单路前视相机**、无 LiDAR、无地图；输入含语言指令、路线目标点、**用户 profile（长期偏好 embedding）**；**特权 PDM-Lite 仅作训练监督**。**无词表/锚点**。**训练期 GRPO 每输入采 4 条响应**（§6.1），奖励 = 与真人/增强动作的行为相似度（§5.3），**风格奖励权重由 GPT-5 推断 + 专家复核**（§5.4）；**推理端无学习式 selector**。Bench2Drive（Tab.1）：**Aggressive DS 79.50 / SR 67.36、Neutral 82.03 / 70.95、Conservative 82.72 / 71.56**；SimLingo 对应 78.56/65.83、78.15/65.85、78.18/65.56；DMW-Vanilla 82.19/70.97。**未报 FPS**。训练 8×RTX A6000（每卡 batch 8）。**代码已发布但关键部分标 "to be released"**（`tasl-lab/DMW`，HF 数据集 `tasl-lab/PDD`）→ **代码核验见 §7.3（GRPO 与 checkpoint 均未发布）** |
| VLA-19 | SimLingo | **见 §6（本轮做了代码级核验）**——语言**自回归**、动作**非自回归**；**N_w = 10 个未来点 @0.25 s（2.5 s）+ N_p = 20 个 route 点 @1 m（20 m）**（论文未给点数，**代码给出**）；**单前视相机**（`num_cameras=[0]`）；**无词表/码本**；LoRA r=32。Bench2Drive **DS 85.07±0.95 / SR 67.27±2.11**（Tab.2）；Leaderboard 2.0 DS **6.25（Map）/ 6.87（Sensor）**（Tab.1）；**Action Dreaming 把 SR 从 28.22 抬到 72.96**（Tab.5）。**未报 FPS**。训练 14 epoch / 8×A100 / batch 12 / 24 h（附录 B.1） |

**第三轮最有价值的三点**：

1. **"1 个 token → VAE + GRU 解码轨迹"成了 VLA 侧的主流范式**：ORION 与 MindDrive **独立收敛到同一结构**（都是 LLM 出极少 token，再由 **VAE + GRU** 解码），且 MindDrive 的 VAE 损失类型名 **`ProbabilisticLoss` 与 GenAD 完全相同**（[C005 §J](../../code/traces/e2e_trunk_code_traces.md)）——**三者都长在 VAD 系代码库上**（MindDrive 仓内有 `mmcv/models/vad_utils/`、`memory_len=600`/`num_query=600`）。→ **"隐变量生成"这条路在 VLA 侧也被复用了**，与研究对象侧的 GenAD 是同一支。
2. **RL 在 VLA 侧的三种形态**：ORION **无 RL**；MindDrive 是**"先离散决策、再连续生成"**（把 RL 的探索空间压到 13 个 meta-action，π_d 是**学到的选择器**，奖励**来自仿真事件**）；Drive My Way 是 **GRPO 对齐人类风格**（奖励 = 行为相似度，风格权重**用 GPT-5 推断 + 专家复核**）。→ **与研究对象侧"RL 词义核验"清单可并列**：DIVER（奖励加权）< HDP（RWR）< AutoVLA（REINFORCE+组归一化）< FeaXDrive（完整 GRPO）；**VLA 侧只有 Drive My Way 用 GRPO，且奖励不是 PDM 而是行为相似度**。
3. **SimLingo 是这一轮的"锚"**：它既是 CVPR'25 Highlight + CARLA Challenge 2024 冠军，**又是 Drive My Way 的基座**——**同一基座被"加语言"（SimLingo 自身）与"加风格对齐"（DMW）两条路各推了一步**。→ 若本项目要做"生成式规划器 + 下游对齐"，**这是一条已有完整对照的实验线**。

### 4.4 第四轮（2026-09-24 第三十六轮，1 篇，结论写在笔记里）

| 编号 | 笔记 | 本次核到的关键新增事实 |
|---|---|---|
| VLA-06 | [DiffVLA](notes/VLA-06-diffvla.md) | **代码状态更正**：有官方代码 [boschresearch/DiffVLA](https://github.com/boschresearch/DiffVLA)（36★ / Apache-2.0 / 最后推送 2025-12-08；`DiffVLA/DiffVLA` 是空壳）。**⚠ 但发布版与论文不同**——轨迹头已从 Diffusion Drive 换成自研 Transformer 头 + EPDM 子指标 reward loss → **发布代码里没有论文的那个扩散头**，**45.0 不可由发布代码复现**。发布版实为 **8192 词表 + 8 个 EPDM 子指标打分头（BCE against 离线 GT）+ 手调权重 argmax 选优** 的"选优器"（`ep`/`hc` 算了但没进最终分）。详见 [笔记 §代码核验](notes/VLA-06-diffvla.md) 与 [sota-plan.md §7.6](../../ideas/sota-plan.md) |

> **本轮同时更正 VLA-07 ReCogDrive 的代码字段**——有官方代码 [xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive)（**611★**，ICLR 2026，2026-09-22 仍在更新）；但其**代码级核验是在研究对象侧完成的**（[C003 §M](../../code/traces/diffusion_planner_code_traces-2.md)），故**不计入 §5–§12 的名单**，本节只计入 VLA-06。

**这一轮最有价值的四点**：

1. **具身 → 驾驶的迁移已经有人做了**：DriveMoE 的底座就是 **π0**（工作空间里有 π0 的官方代码 `openpi`，已完成代码级核验）。→ "把具身 VLA 基础模型搬到驾驶"不再是假设，而是**既有事实**；本项目要问的应变成"**搬到哪一层**"。
2. **NAVSIM v2 有了第三方完整复评表**（ExploreVLA Table 2，含 9 个子指标）——这是本工作空间**第一份第三方给出的 v2 navtest 全子指标对照**，直接可用于"评价可行"判断。已写入 [preparation.md §6.1](../../ideas/preparation.md)。
3. **"同一模型两套口径"再次出现**：OpenDriveVLA 在 **ST-P3 口径**下 L2 Avg 0.33 m、在 **UniAD 口径**下 0.66 m，**差一倍**。→ 与 P8（口径不可比）同源，且是**同一篇论文内部的两种口径**。
4. **边界外清单不是"永久排除"，而是"待补 venue"**：复检 4 条后 **SimLingo 升为 T1 收录（VLA-19，CVPR'25）**，并意外查清 **CarLLaVA 就是 SimLingo 的 preliminary 挑战赛技术报告**；LMDrive / RAG-Driver 的 venue 仍不可核，继续留在边界外。

## 5. 代码级核验（第二十一轮新增）

两个仓库已核验：**AutoVLA 代码完整发布**、**OpenDriveVLA 部分发布**。核验方式均为**静态检查，未安装、未运行**；两仓库的克隆/落盘状态见 [repositories.md](../../code/repositories.md) §E。

### 5.1 AutoVLA（VLA-11）：代码完整，GRPO 需三处限定

仓库 `ucla-mobility/AutoVLA`（2025-06-14 建，**最后推送 2026-05-29**，654 stars，38.9 MB / 217 文件，含 vendored 的 `navsim`）。**git clone 在本机连续 5 次 TLS 失败**，改用 GitHub API + raw 逐文件取证。

| 论文声称 | 代码级实测 | 判定 |
|---|---|---|
| action codebook **K=2048**（K-disk 聚类） | `codebook_cache/agent_vocab.pkl` 实测形状 **`(2048, 6, 4, 2)` × 3 类（`veh`/`ped`/`cyc`）**；`action_token_cluster.py` 的 `--num_cluster` 默认 **2048**、`--n_trajs` 默认 **2048000**、`--tol_dist` 默认 **0.05** | **一致**，并补上三个论文未给的参数 |
| 5 s 轨迹 = **10 个 token** @0.5 s | 配置 `num_poses: 10 / interval_length: 0.5 / time_horizon: 5.0`；`rollout` 每 token 追加 1 点、共 11 点，`predict` 用 `[0, 1:]` 去掉初始点 → **10 poses** | **一致** |
| 真 GRPO（组内相对优势 + **KL β=0.04**） | `config/training/qwen2.5-vl-3B-nuplan-grpo-cot.yaml` 的 `rl.kl_beta: 0.04` **与论文一致**；`models/autovla.py:88` `advantage = (reward − all_gather(reward).mean()) / (std + 1e-4)`；`:119-120` KL 用**标准 k3 估计量** `exp(ref−cur) − (ref−cur) − 1` | **一致，但有三处需限定**（见下） |
| 奖励来自 PDM 分数 | `models/utils/score.py` 的 `PDM_Reward.rl_pdm_score` **真跑 NAVSIM 的 `pdm_score`**（`TrajectorySampling(num_poses=40, interval_length=0.1)` + `PDMScorer`） | **一致**——这是本工作空间证据里**最强的"真奖励"实现**（对比 DIVER 的 dummy 项、HDP 的 RWR） |
| **3 路相机纯视觉** | 三层口径不同：`SensorConfig` 声明 **8 路相机**、`AutoVLAAgentFeatureBuilder` 组装 **6 路**、`get_prompt` 的 `camera_types` **只有 3 路 × 4 帧 @2 Hz** 真正喂给 VLM；`lidar_pc=False` | **一致（按使用层）**，但印证"输入权限必须按**使用层**标注" |

**三处必须限定的 GRPO 细节**：

1. **"组"是跨 GPU 的 batch，不是同一 prompt 的 G 次采样**：`groupped_rewards = self.all_gather(reward)`，而 `generate_sample` **每个 prompt 只调用一次**（`RFTDataset.collate_fn` 注释原文 "Only work for batch size = 1"）；配置 `devices: [0, 1]` → **组大小 = 2**。→ 标准 GRPO 是"同 prompt 采 G 次、组内比"，这里是**跨 prompt 的批归一化优势**。项目页的 "Larger groups lead to better performance" 在此实现下等价于"**更多 GPU**"。
2. **无 PPO clip**：`:114-115` `per_policy_loss = exp(per_token_logps − per_token_logps.detach()) * advantage` —— 比值**恒等于 1**（只保留梯度），**没有 clip、没有概率比、每样本只更新一次**。→ 实质是 **REINFORCE + 组归一化优势 + KL 惩罚**。
3. **RFT 时验证被禁用**：`tools/run_rft.py:191` `limit_val_batches=0`；`val_critic` 建了但训练循环不用。

→ **"RL 词义核验"清单现有四种**：DIVER（奖励加权损失，最弱）< HDP（RWR）< **AutoVLA（REINFORCE + 组归一化优势 + k3 KL，无 clip）** < FeaXDrive（完整 GRPO：clip + log-prob + BC 项）。**只有 FeaXDrive 是完整的 PPO 式策略梯度。**

**两处论文与代码不符**（读论文 Eq.3/Eq.4 与代码逐条对照）：

| 论文（Eq.3 / Eq.4） | 代码（`models/autovla.py`） | 判定 |
|---|---|---|
| **每个 query 采 G 个候选** `O = {o₁…o_G} ~ π_θold(O\|q)` | 每 prompt **只采 1 次**（`generate_sample` 单次调用），组由 `all_gather(reward)` **跨 GPU** 组成 | **不符**：论文写"组内 G 次采样"，代码是"跨 GPU 的批归一化" |
| **标准 PPO-clipped 目标** `J_i^R = min(ratio·A_i, clip(ratio, 1−ε, 1+ε)·A_i)`，ratio = π_θ/π_θold | `per_policy_loss = exp(logp − logp.detach()) · A`；**全文件无 `clip`/`epsilon`/`ratio`/old policy**（唯一的 `clip` 是 `clip_grad_value_` 梯度裁剪） | **不符**：代码无 clip、无概率比、无 old policy → 退化为 REINFORCE |

> 与工作空间已记录的模式同源（"论文声称的机制在代码里打了折扣"）：**引述"AutoVLA 用 GRPO（带 clip 的策略梯度）"时必须限定为"REINFORCE + 组归一化优势 + KL 惩罚"。** 其 Eq. S3 的奖励公式 `r_Driving = NC × DAC × ((5·TTC + 2·C + 5·EP)/12)` **与 NAVSIM 的 PDMS 完全一致** ✓，这部分是可信的。

**best-of-N 的口径限定（必须标注）**：论文 §4.2 原文 "In best-of-N planning, we use an **oracle scorer** to select the optimal trajectory from **six generated candidates**"。→ **92.12 是"6 选 1 + 用 oracle scorer 选优"的结果**，而 oracle scorer 需要**真值侧的打分信息**（与工作空间已记录的 **UniAD 测试时优化** `use_col_optim=True`、**DiffusionDriveV2 的 scorer 选优**同类）。**引用 92.12 时必须与 one-shot 的 80.54 并列，不能当作单次前向可比数字。**

**一处正文与自身表格不一致**：正文写 best-of-N "achieving the highest PDMS"，但 **Table 1 里 TrajHF 是 93.95 > AutoVLA (Best-of-N) 92.12 > Centaur 92.10**（Hydra-MDP 91.26）。→ 该表述**与自己的表 1 矛盾**（可能是"最高"有未写明的限定范围）。另注：**Table 1 的列名是 Collision / Area / Direction / Progress / TTC / Comfort（六项 + PDMS）**，与 devkit 的 v1 五项（NC/DAC/EP/TTC/C）和 v2 九项**都不完全对应** → **引用其 PDMS 前必须自行核对 PDM 口径**。

**四条代码比论文多的实现细节**：

1. **码本的 6 步结构只在聚类时有用，解码时只用末步**：`rollout` 里 `pos_a_next = token_traj_global[:, -1].mean(dim=1)`（**末步包围盒 4 个角点的均值**），`head_a_next = arctan2(corner0 − corner3)`。→ **一个 token 的 6 步段里，前 5 步不参与解码**。
2. **非 action token 静默变成"零位移"**：`decode_token_ids_to_trajectory` 里 `if token_ids[i] < self.action_start_id: action_token_ids.append(0)`，而 K-disk 的第一个中心被固定为 `[0,0,0]` → **任何非 action token 都映射到索引 0**。
3. **码本是三类智能体共用的**：`token_all` 有 `veh`/`ped`/`cyc` 三个键、各 2048 条；ego 规划只用 `veh` 分支 → 词表来自**多智能体运动数据集**，不是 ego 专用。
4. **轨迹长度口径在提交路径上被改写**：`AutoVLAAgent.compute_trajectory` 里 `submission = False` **硬编码** → `upsample_trajectory(..., old_total_time=5.0, new_total_time=4.0, new_interval=0.1)` 这条"5 s → 4 s @10 Hz"的路径**不可达**；实际返回 `poses[:num_poses]`，即 **10 poses @0.5 s（5 s）**。而 NAVSIM 打分按 **4 s** 采样 → **最后 1 s 不打分**（与 GoalFlow 的"训练 5.5 s、评测 4 s"同类）。

**一处 docstring 与实现"看起来"不符——⚠ 已于第三十九轮更正为"其实相符"**：`PDM_Reward.rl_pdm_score` 的 docstring 写 "excluding the two_frame_extended_comfort metric"，而代码**直接取 `result.score`、没有显式排除任何指标** → 原先据此记为"docstring 与实现不符"。**但第三十九轮在本地 devkit 上核到：`result.score`（EPDMS）本身就把 EC mask 掉了**（`pdm_scorer.py` 原文 "Exclude the two-frame extended comfort metric from the weighted metrics calculation"，见 [benchmarks.md §2.3](../../direction/benchmarks.md)）→ **排除发生在上游 devkit 里，这个 wrapper 不需要再排除** → **docstring 是对的**，原判是**误读**。**仍然成立的只有后半句**：`except Exception` 时**静默返回 0 奖励**。

### 5.2 OpenDriveVLA（VLA-03）：训练脚本未发布，轨迹靠正则从文本抠出

仓库 `DriveVLA/OpenDriveVLA`（2025-03-18 建，最后推送 2026-02-16，811 stars，11.7 MB）。

- **README 的 TODO 里 `Release training scripts` 未勾选**（环境 / 推理代码 / 权重已勾选）。→ 论文的四阶段训练（Stage 1 分层视觉-语言对齐 / Stage 2 指令微调 / **Stage 2.5 agent-env-ego 交互** / Stage 3 轨迹微调）**只有论文自述级，不可代码核验**。
- **只发布了 0.5B 权重**（HF `OpenDriveVLA/OpenDriveVLA-0.5B`，2025-11-14），而论文表格把 3B / 7B 与 0.5B 并列 → **头条数字（7B）无权重可复现**。
- **无轨迹词表/锚点**：`drivevla/` 全目录 grep `vocabulary|codebook|plan_anchor|kmeans` **零命中** ✓
- **轨迹是从自由文本里用正则抠出来的**：`drivevla/utils/trajectory_utils.py` 的 `retrieve_traj` 是一段**多步正则清洗流水线**（去英文字母、去中文、修连续小数点、补缺失逗号、修中缀负号、把 `(x,y,z)` 去成 `(x,y)`……），最后 `re.findall` 取坐标对；**不足 6 个点用最后一个点补齐**（`coords_list.append(coords_list[-1])`），**多于 6 个点直接截断**；`trajectory_is_valid` 要求 `len == 6`。→ **"生成 6 个点"不是模型保证的**。
- **单样本贪心解码**：`inference_drivevla.py` 用 `do_sample=False, temperature=0, num_beams=1` → **无多模态候选、无 selector** ✓（同文件另有一段被注释掉的 `do_sample=True, temperature=0.1`）。

**这条发现的意义**：它与 [C003 §H.2](../../code/traces/diffusion_planner_code_traces.md) 记录的 **WAM-Flow"把坐标量化成文本数字串"** 是同一类做法（**轨迹即文本**）；OpenDriveVLA 的正则清洗代码给出了这类做法**脆弱性的直接证据**。→ 本项目若考虑"语言接口出轨迹"，必须把**解析失败率**当一等指标。

### 5.3 本节结论

- **"有代码"要分三档**：完整发布（AutoVLA）/ 部分发布（OpenDriveVLA：只有推理与 0.5B 权重）/ 只有项目页（ExploreVLA、DriveMoE）。本表 19 篇里**已核验 4 篇的代码状态**（2 有仓库 + 2 只有项目页），**其余 15 篇的代码状态未核**。
- **VLA 侧的"生成机制"与扩散规划器侧完全不同**：本表没有任何一篇用扩散/流匹配出轨迹（唯一例外是 VLA-06 DiffVLA / VLA-07 ReCogDrive / VLA-08 KnowDiffuser，它们正是与研究对象的交集）。主流是 **自回归离散 token** 或 **VLM 出 waypoint 后回归**。
- **两篇都在 NAVSIM 上把扩散规划器当对照**（AutoVLA PDMS 92.12、ExploreVLA EPDMS 88.8 vs DiffusionDrive 84.5）→ **"VLM/VLA 规划器已经超过扩散规划器"这件事已有第三方数字**，本项目选题时必须正面处理这个对照。

## 6. SimLingo 的代码级核验（第二十二轮新增）

仓库 [`RenzKa/simlingo`](https://github.com/RenzKa/simlingo)（**453 stars**，98.6 MB，`created 2025-03-12` / `pushed 2025-08-25`，默认分支 `main`）。**未克隆全仓**（沿用 §5 的 API 逐文件取证法），已核验文件：`simlingo_training/models/driving.py`(35,383 B)、`simlingo_training/models/adaptors/adaptors.py`(14,565 B)、`simlingo_training/config.py`(4,981 B)、`simlingo_training/utils/custom_types.py`(2,341 B)、`simlingo_training/dataloader/dataset_dreamer.py`(9,089 B)、`team_code/config_simlingo.py`(3,063 B)、`README.md`(17,893 B)。

**论文声称 vs 代码实测**：

| 论文声称 | 代码级实测 | 判定 |
|---|---|---|
| 语言自回归、**动作非自回归**（一次前向出全部 waypoint） | `driving.py:131-176`：语言走 `language_model.greedy_sample(..., max_new_tokens=100)`；动作**另起一次** `language_model.forward(input_embed_concat)`，取 `features[:, -len_driving:]` → `adaptors.driving.get_predictions(...)` | **一致** |
| **单前视相机** | `team_code/config_simlingo.py:53` **`self.num_cameras = [0] #,3] #,1,2]`**——**只用相机 0，多相机是被注释掉的选项** | **一致**（且说明多相机属被放弃的分支） |
| 时序 waypoint 每 **0.25 s** | `config.py:60` **`pred_len: int = 11 # including the current time step`**；`carla_fps = 20` / `data_save_freq = 5` → **4 Hz = 0.25 s**；`adaptors.py:128` **`self.future_speed_waypoints = 10`** | **一致**：**N_w = 10 个未来点 / 2.5 s**（论文未给点数） |
| 几何 route 每 **1 m** | `config.py:71` **`num_route_points: int = 20`**；`dataset_base.py:551` `equal_spacing_route` 里 **`x = np.arange(0, 20, 1)`**；`adaptors.py:111` **`self.future_waypoints = 20`** | **一致**：**N_p = 20 个点 / 20 m**（论文未给点数） |
| **LoRA r=32** | `config.py:21` **`lora_r: int = 32`**、`lora_alpha: int = 64`、`lora_dropout: float = 0.1` | **一致** |
| 512 视觉 token | `config.py:10` **`embed_dim: int = 512`**（`VLMEncoderConfig`） | 一致（口径为 embed 维度） |
| 无轨迹词表 | 全仓 6,238 个文件里，**`.npy` 只出现在 CARLA 的 `speed_limits/Town*.npy`**（vendored Bench2Drive / `team_code`，与轨迹无关），**无 `.pkl`/`.ckpt`，无 vocab/anchor/kmeans/codebook 类资产** | **一致** |
| Action Dreaming（指令-轨迹对合成） | 仓库确有 `simlingo_training/dataloader/dataset_dreamer.py`（`Data_Dreamer`，`dreamer_answer = "Following the given instruction. Waypoints:"`、`dreamer_instruction`、另有 `dreamer_answer_safety`）；README 原文亦写 "**dreaming data generation**" | **一致** |

**四条代码比论文多的实现细节**：

1. **动作头就是两个纯 MLP，输出连续 2D 坐标**（`adaptors.py:113-132`）：`route_head = Linear(h→2m) → SiLU → Linear(2m→m) → SiLU → Linear(m→2, bias=False)`；`speed_wps_head = Linear(h→m) → SiLU → Linear(m→dim, bias=False)`。查询是**可学习参数** `query_embeds_wps (1,20,h)` 与 `query_embeds_speed (1,10,h)`（`0.02*randn` 初始化）。→ **这是"非自回归 + 无词表"的最硬证据**：没有分类头、没有码本、没有 argmax。
2. **`future_speed_waypoints` 硬编码 10，带 TODO**：`adaptors.py:128` 原文 `self.future_speed_waypoints = 10 #TODO: read from config`——**config 里有 `pred_len`，这里没读**（与工作空间已记录的"声明未接线"同类）。
3. **`cross_track_error` 函数存在但调用被注释掉**（`adaptors.py:10` 定义，`:211-213` 的 `# cte = cross_track_error(prediction, label_waypoints)` 整段注释）→ **横向误差损失在已发布配置里不生效**。
4. **`DrivingLabel.waypoints` 的注释与配置矛盾**：`custom_types.py:54` 写 `# [B, F, 2] 11 future waypoints **0.2s apart**`，而配置是 **4 Hz（0.25 s）** → **注释疑似从 CarLLaVA/TransFuser 沿用未改**，属需运行确认的项。

**README 里的两条额外事实**：

- **README 原文写 "We provide code for the smaller model SimLingo-Base (**previously CarLLaVA** - without language capabilities) in the folder `simlingo_base_training`"** → **"CarLLaVA = SimLingo-Base"由官方 README 直接确认**（比 §3 里从 `comments` 推断更硬）；仓库描述里也保留 "SimLingo (CarLLava)"。
- **数据由 PDM-Lite 生成**（README：专家来自 **DriveLM** 论文的 PDM-Lite，数据采集代码取自 Carla Garage）→ 与本工作空间已有的 [DriveLM 笔记](../../direction/notes/E2E-11-drivelm.md) 同源。
- 发布历史：**2025/05/08 首发代码 → 2025/05/26 完整数据集 → 2025/06/25 模型权重 + 推理代码** → **代码与权重都已发布**（与 ExploreVLA/DriveMoE 只有项目页形成对照）。

**§6 的结论**：**SimLingo 是本工作空间第一个"论文声称与代码逐条一致"的 VLA 工作**（上表 8 条声称全部一致，且补上了论文没给的 **N_w/N_p** 两个关键数字）；发现的 3 处不一致都属于**工程细节**（硬编码 + TODO、注释掉的损失、过期注释），**不影响其机制主张的可信度**——这与 AutoVLA（论文写了 clip 而代码没有）形成鲜明对照。

## 7. ORION / MindDrive / Drive My Way 的代码级核验（第二十三轮新增）

三个仓库均为**源码逐文件核验**（未 `git clone`，走 GitHub API / raw 抓取；ORION 的 tarball 被完整解出后 grep）。仓库元数据见 [repositories.md §E](../../code/repositories.md)。

### 7.1 ORION（VLA-15）：机制成立，但扩散消融在配置层被全量关闭

| 论文声称 | 代码级实测 | 判定 |
|---|---|---|
| LLM 只出 **1 个 planning token** | `constants.py:18` 只注册 1 个特殊 token `EGO_WAYPOINT_TOKEN = "<waypoint_ego>"`；`llava_llama.py:143` 用掩码 `loc_positions = (new_input_ids == self.config.waypoint_token_idx)` 取出其 hidden state；`use_gen_token = True`（stage2/stage3，stage1 为 False） | **一致** |
| **VAE + GRU** 解码 | `orion.py:215-239`：`latent_dim = 32`、`N_GRU_BLOCKS = 3`、`present_distribution` / `future_distribution` = `DistributionModule`、`predict_model = PredictModel`（内含 `nn.GRU`） | **一致** |
| **anchor-free**、**6 条模态** | VAE 分支 `self.ego_fut_mode = 6`（`orion.py:222`），测试期按导航命令掩码选模态 | **一致**（只对 VAE 分支成立） |
| **memory bank + history queries**（最优 `N_h=16`） | `orion_head.py:104` **`num_memory = 16`**；`memory_query = nn.Embedding(16, ...)`；FIFO 用 `torch.cat` + `memory_refresh(...)` 实现 | **一致** |
| 扩散消融版：K-means 锚点、**20 模态** | `diffusions.py:41/104` 确为 `ego_fut_mode=20`；但 **7 个 stage 配置全部 `use_diff_decoder = False`**（stage1 / 2 / 3 / 3_cot / 3_fp16 / 3_agent / 3_infer），且**没有任何配置传 `plan_anchor_path`** | **需限定**：20 模态扩散消融**在代码里存在但无法由已发布配置启用** → 论文的扩散对照（Tab.3）**不可直接复现** |

### 7.2 MindDrive（VLA-16）：**教科书式 PPO**，但 π_d 的"路径"分支不是学到的

| 论文声称 | 代码级实测 | 判定 |
|---|---|---|
| meta-action = **7 速度 + 6 路径** | `minddrive.py:339-340` `self.ego_fut_mode = 7` / `self.pw_ego_fut_mode = 6`；`:1130-1131` `command2hot(speed_value, max_dim=7)` / `command2hot(path_value, max_dim=6)`；`SPEED_MAPPING` / `PATH_MAPPING` 在 `:79` / `:89` | **一致** |
| 有**学到的选择器 π_d** | **只对了一半**——速度分支是学到的：`action_distribution.proba_distribution(action_logits=...)` → RL 时 `sample()`、否则 `argmax`（`:974-979`）；**路径分支不是**：`:981-985` `std_cmd_tensors = data['ego_fut_cmd'][:,0,0]` → **`path_idx = torch.argmax(cmd_tensor)`**，即**直接取导航命令** | **需限定**：π_d 只有"速度"维度是策略，"路径"是给定输入 |
| **RL**、稀疏奖励 **±1**、来自**仿真事件** | `carla_env_scenario.py:447-458`：命中 `PENALTY_CONFIG` → `reward=-1`；`ROUTE_COMPLETION` 且 `score_route>=100` → `reward=1`；惩罚项 = 碰撞/闯红灯/不停车/偏航/出车道；偏航阈值 `offroad_max=30` | **一致** |
| （论文未给具体算法） | **是完整 PPO**：`iter_based_runner.py:314` `class RLIterBasedRunner`，`:323-331` `gamma=0.99, clip_range=0.2, vf_coef=0.5, kl_coef=0.5, normalize_advantage=True`；`:465-470` **真 clip**（`clamp(ratio, 1±clip_range)` 取 min）；`:481-482` **value loss**（MSE + 独立 critic `value_net`）；`buffers.py:273` **GAE** `delta + gamma*gae_lambda*next_non_terminal*last_gae_lam`（`gae_lambda=1.0`） | **代码给出论文未写的算法细节** |
| **双 LoRA** 解耦 | `minddrive.py:245` `load_model(..., adapter_names=["action_expert","decision_expert"])`；`:957` `set_adapter("decision_expert")`（决策）、`:1013` `set_adapter("action_expert")`（动作）；**RL 只训 `decision_expert` 的 LoRA + value head** | **一致**，且**生成器在 RL 阶段冻结** |
| **KL 正则**防灾难性遗忘 | `kl_coef=0.5` + `F.kl_div`；但**参考分布是 rollout 时的旧 logits**，**没有独立冻结的参考模型** | **需限定**：是"旧策略 KL"而非标准 PPO 的参考模型 KL |
| **VAE + GRU**、`ProbabilisticLoss` | `minddrive.py:344-356` `DistributionModule(latent_dim=32, min/max_log_sigma=±5)` + `PredictModel`（内含 `nn.GRU`）；`ProbabilisticLoss` 权重 **3.0**（stage 配置） | **一致** |

**三处"声明未接线"**：① RL 配置写 **`no_use_kl_and_entro = True`**，但该开关的接线**被注释掉** → **KL 实际按 0.5 开启，与配置意图相反**；② RL 配置里 `workflow = [('ppo_train', 1)]` 与 `type='EpochBasedRunner'` 并存 → **runner 类型与 workflow 不一致，疑为遗留**；③ `carla_env_scenario.py:505` 另有 `_compute_reward`（route_progress + `collision_penalty=-10`），但 **`step` 里未调用它** → 实际生效的是 ±1 稀疏奖励。

### 7.3 Drive My Way（VLA-17）：**GRPO 代码未发布**，"基座 + 残差 + PID"成立

- **README 的目录树原文写 `├── grpo/ # GRPO post-training (**to be released**)` 与 `├── checkpoints/ # Checkpoints (**to be released**)`**；README 另写 "This repo contains a stripped-down TRL fork with only GRPO training support" 并让用户 `cd grpo` —— **但全仓 14,508 个文件里没有 `grpo/` 目录**。
- **全仓搜索无任何 reward / advantage / GRPO 源文件**；`team_code/long_term_preference.py:138` 只读 `.hydra/config_grpo_human.yaml`、`:162` 注释 `# Load the GRPO checkpoint` → **推理侧只能加载别人训好的 checkpoint**。
- → **论文的 GRPO 机制（每输入采 4 条、奖励 = 行为相似度、风格权重由 GPT-5 推断）在已发布代码里完全不可核验**。仓库里唯一的 GPT 产物是 `models/utils/gpt_eval.py`，模型是 **`gpt-4o-2024-08-06`**（**不是 GPT-5**），用途是给 QA 答案打 0–100 分。
- **成立的部分**：① **离散残差头**——`adaptors.py:103` `DreamingActionDiscreteHead`，`speed_list = [0.7…1.3]`（**7 档**）× `steer_list = [-0.3…0.3]`（**7 档**）= 49，非 `use_user_profile` 时再加 `[[1.0, 0.0]]` → **50 个联合动作**；`dist = Categorical(logits=logits/temperature)`，温度**可学习**（`log_temperature`）；② **残差语义**：speed 是**乘性尺度**（`clip(..., 0.5, 1.5)`）、steer 是**加性增量**（`clip(..., -0.3, 0.3)`）；③ **下游确为 PID**（`control_pid_personalization` + `PIDController` / `LateralPIDController`）；④ **基座是 SimLingo**——`DrivingAdaptor` 等与 SimLingo 同名同构，`team_code/` 沿用 SimLingo 的 PID 与路线规划组件。

### 7.4 本节结论

- **"有代码"要再细一档**：**完整**（AutoVLA / SimLingo / ORION / MindDrive）/ **关键部分未发布**（**Drive My Way：GRPO 与 checkpoint 都标 "to be released"**）/ **训练脚本未发布**（OpenDriveVLA）/ **只有项目页**（ExploreVLA、DriveMoE）。
- **"RL 词义核验"清单扩到五种，并出现第一个完整 PPO**：DIVER（奖励加权损失）< HDP（RWR）< AutoVLA（REINFORCE + 组归一化优势 + KL，无 clip）< FeaXDrive（GRPO：clip + log-prob + BC 项）< **MindDrive（完整 PPO：`clip_range=0.2` + 独立 `value_net` + GAE λ=1 + KL 0.5）**。→ **只有 MindDrive 同时有 critic 与 GAE**，且它的奖励是**仿真事件稀疏 ±1**，与 FeaXDrive / AutoVLA 的"真 PDM 分数"都不同。
- **"论文声称 vs 代码实测"的三种新形态**：① **机制在代码里但被配置全量关闭**（ORION 的 20 模态扩散消融）；② **机制只实现了一半**（MindDrive 的 π_d 只有速度是策略）；③ **机制根本没发布**（DMW 的 GRPO）。→ 前两种只有**读代码**才能发现，第三种只有**查目录树**才会发现。

## 8. 剩余 6 篇的代码可用性 + 两篇的源码核验（第二十四轮新增）

**动因**：VLA 侧 19 篇里 13 篇已读全文、6 篇已源码核验（**当时的口径**；第三十六轮后为 28 篇全文 / 14 篇源码核验），但**仍有 6 篇停在摘要级且从未核过代码可用性**（VLA-01/02/05/09/10/12）。本轮派子代理用 `raw.githubusercontent.com` + GitHub trees API 逐仓核实（**不克隆**）。

| 编号 | 论文 | 官方仓库 | 最后推送 | 体积 / 文件数 | 代码范围 |
|---|---|---|---|---|---|
| VLA-01 | DriveGPT4 | **未找到**（正文原文 "code and dataset will be **publicly available**"，作者 GitHub 无此项；仅有第三方复现） | — | — | **承诺未兑现** |
| VLA-02 | ADriver-I | **未找到**（abs/HTML 无任何 code 链接） | — | — | **无** |
| VLA-05 | SafeAuto | [AI-secure/SafeAuto](https://github.com/AI-secure/SafeAuto) | 2026-08-02 | ~100 MB / 217 | **完整**（训练 + RAG + PGM + HF 权重） |
| VLA-09 | EMMA | **未找到**（项目页是 Waymo blog，无代码）；**arXiv ID 本轮核定为 `2410.23262`** | — | — | **无** |
| VLA-10 | CoVLA | **未找到**（组织 35 个仓无此项；只有 HF **数据集** `turing-motors/CoVLA-Dataset`） | — | — | **仅数据集** |
| VLA-12 | Impromptu VLA | [ahydchh/Impromptu-VLA](https://github.com/ahydchh/Impromptu-VLA) | 2025-10-29 | ~178 MB / 464 | **部分**（数据生成 + 推理 + HF 权重齐全；**训练委派 LLaMA-Factory**，仓内只有一个示例 yaml，README 引用的训练配置目录不存在） |

### 8.1 VLA-12 Impromptu VLA：**"轨迹即文本"的第三个实例，且暴露 prompt/parser 口径不一致**

- **轨迹从自然语言里用正则抠出**：`neuroncap_evaluation/Impromptu/inference/server.py:102-113` 的 `extract_trajectory` 用 `re.findall(r"\[([\-\d\.]+),\s*([\-\d\.]+)\]", answer)` 抽点，**`return traj[:6]  # Limit to 6 steps`**；**解析失败直接返回 `[[0.0, 0.0]] * 6`（全零点）**，并打印 `⚠️ Failed to extract trajectory from response, returning default 0`。
- **口径不一致（本轮新发现）**：同一文件的固定 prompt（`:272`）写 "predict future waypoints for the vehicle over the **next 3 timesteps**"，而解析器允许到 **6 步** → **要 3 步、收 6 步**。
- → 与 **OpenDriveVLA**（"不足 6 点用最后一点补齐、多于 6 点截断"）和 **WAM-Flow**（坐标量化成文本数字串）同类：**"轨迹即文本"这一路线的脆弱性是系统性的**，三个工作各自暴露一种失败模式（补齐 / 截断 / 补零）。

### 8.2 VLA-05 SafeAuto：**唯一可读的"神经符号安全否决层"实现**

- **动作空间分三层**（`pgm/config.py`）：**16 个高层动作**（`action_list`：Keep / Accelerate / Decelerate / Stop / Reverse / MakeLeftTurn / MakeRightTurn / MakeUTurn / Merge / LeftPass / RightPass / Yield / ChangeToLeftLane / ChangeToRightLane / Park / PullOver）；**5 个速度控制信号**（`velocity_cs_list`）；**3 个方向控制信号**（`direction_cs_list`）。
- **硬规则 10 条**（`hardrule_num: int = 10`），规则以 **MLN（Markov Logic Network）一阶逻辑**形式写成 lambda：`1 - a + a*b`（a 为条件谓词、b 为约束项）——**⚠ 措辞更正（第二十五轮）**：论文全篇用 "**MLN / 一阶逻辑**"、**没有 "fuzzy" 字样**，故此前记的"模糊逻辑"应改为"**MLN 一阶逻辑的可微松弛**"（该 lambda 是**乘积 t-范数松弛**，**规则本身无阈值，权重靠训练学习**，见 §14.3）。规则**分两类**——① **环境 → 动作**（`SolidRedLight → ¬Accelerate ∧ ¬LeftPass ∧ ¬Yield`、`MergingTrafficSign → Decelerate`、`StopSign → ¬PullOver` 等）；② **控制信号自洽**（`KEEP_CS`、`ACCELERATE_CS`、`LEFT_CS`、`LEFT_CS × CHANGETORIGHTLANE_LLM → …`）→ **不只有环境规则，还有"高层动作与控制信号必须一致"的规则**。
- 谓词表含 **16 个未观测动作谓词 + 环境谓词（红/黄灯、各类交通标志、行人）**。
- **判断**：这是 VLA 侧**唯一能逐行核验的"安全门控"实现**——对研究对象的接点（**扩散规划器 + 安全层**）最紧，且与 DP-A21 PC-Diffuser 的"去噪内 CBF-QP"是**两种不同的注入位置**（SafeAuto 在**输出端否决**，PC-Diffuser 在**去噪过程中约束**）。
- **注意**：SafeAuto **不输出轨迹**（出的是控制信号 + 高层动作），因此**不能直接与 NAVSIM 系规划器比指标**。

### 8.3 本节结论

- **"有代码"分档在本轮再补两档**：**完整**（VLA-05 SafeAuto）/ **部分**（VLA-12 Impromptu：训练委派外部框架）/ **仅数据集**（VLA-10 CoVLA）/ **承诺未兑现**（VLA-01 DriveGPT4）/ **无**（VLA-02 ADriver-I、VLA-09 EMMA）。→ **VLA 侧 19 篇至此全部核过代码可用性**。
- **VLA 侧"轨迹即文本"路线现已有三个实例**（OpenDriveVLA / WAM-Flow / Impromptu VLA），**三种不同的失败模式**。
- **"安全层注入位置"已有两个可代码核验的对照**：**输出端否决**（SafeAuto 的 PGM 硬规则）vs **去噪过程内约束**（PC-Diffuser 的逐去噪步 CBF-QP）。

---

**§9–§14 见 [verification-2.md](verification-2.md)**（本册为 §4–§8）。
