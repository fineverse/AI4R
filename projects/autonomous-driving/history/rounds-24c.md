# 自动驾驶项目 · 逐轮工作记录 · 第二十四轮（续，§22–§27）

本卷范围：**第二十四轮（续，§22–§27）**。内容：GuideFlow、LCS 与 BridgeDrive、MPDiffuser 与 DIPOLE、NeMo 与 OccVAR 结账、VLA 边界外清单复核、AutoMoT 全文 + 代码核验。
索引见 [../history.md](../history.md)；上一卷见 [rounds-24b.md](rounds-24b.md)；当前状态见 [../state.md](../state.md)。

---

### 22. GuideFlow（DP-A12）的代码级核验——navhard SOTA 的三条机制，**两条不在评测路径上**

**动因**：GuideFlow 是**与本项目研究对象同基准（NAVSIM v2 `navhard_two_stage`）的当前 SOTA**（EPDMS **43.0**，同表 DiffusionDrive 只有 24.2），论文卖点"受约束流匹配"正对**方向 A（约束注入层级）**。它的代码此前只被记为"arXiv 指向的仓库是占位"——本轮按 §20 的指向链找到真仓库 **[adept-thu/GuideFlow](https://github.com/adept-thu/GuideFlow)**（`main`，1513 个 blob），走 `raw` 逐文件取证（**未克隆**，缓存 57 个文件）。

**论文三条机制与代码的对应**：

| 论文主张 | 代码实况 |
|---|---|
| **CVF**（Eq.14）：速度场朝约束方向**投影**，λ=0.1，每步 | 只在 `navsim_train/agents/flowdrive_unet/transfuser_model_v8.py`：`:556 limited_v_pred = limited_anchors − zt`（**在采样循环之外算一次**）→ `:579 zt = zt + (v_pred + 0.11*limited_v_pred) * dt`，紧跟注释 **`# 0.05 ,0.08 ,0.15, 0.10, 0.12 , 0.11 best`**。→ **不是投影**（全库无 `v − (v·n)n` 之类算子），是**朝初始锚点方向的常数速度偏置**；**λ 实取 0.11 且是调参选出的**；"约束"= **GTRS 给的整条专家轨迹**，不是可行驶区/车道/障碍物梯度 |
| **CF**（Eq.16）：第 `k_c=50` 步替换为 anchor，只做一次 | `navsim_test/agents/flowdrive/transfuser_model_v6.py:505-506` `if i_step < k_num: zt = limited_anchors` —— **`k_num` 全仓只此一处引用、无定义** → **按此文件运行会立即 `NameError`**；语义也变成"前 `k_num` 步都替换"。`k_c=50` 的唯一痕迹是**死代码**（各版本 `self.num_inference_steps = 50` 从未被读取） |
| **RFE**（Eq.17–18）：**训练期**能量项 | **训练损失里没有能量项**：`transfuser_loss.py:30-35` 只有 `trajectory/agent_class/agent_box/bev_semantic` 四项。v10 的 "rfe Module" 是**推理期**：`:203-207` 从**网络预测的 BEV 语义图**算 `distance_transform_edt` 双向 SDF → `:290 ESDFEncoder` → `:558-560` 作为**条件**喂进模型，`v_pred = v_pred_no_cond + 2.5·(v_pred_cond − v_pred_no_cond)`（**这是 CFG**） |
| **K = 100** | ✅ 成立且未被覆盖（`dp_config.py:43 denoising_timesteps = 100`；代码写死 `range(0,100)`、`dt = 1/100`） |

**本轮最重要的一条**：仓库里是**两套并列代码树**（`navsim_test/` 与 `navsim_train/`），**版本切换靠注释 import 行**。**评测侧 `navsim_test/agents/flowdrive/transfuser_agent.py:12` import 的是 `v6`**，而 **`navsim_test/agents/flowdrive/` 只发布到 v6，没有 v8/v9/v10**；**CVF 只在 v8、RFE 模块只在 v10**（训练侧 import v10）→ **按仓库给的评测脚本（`scripts/testing/test_flow.sh`）直接跑，命中 v6：既无 CVF 也无 RFE，且会撞上未定义的 `k_num`**。三条机制的开关全是模型 `__init__` 里的 Python 常量（`use_guidance_limit` / `use_condition_limit`），**没有任何 yaml/sh 字段** → **"配置覆盖链"这条老陷阱在这里不适用，真正的坑在 import 层**。

**其余硬发现**：① **`flow_matching.py` 是三处 11 字节占位文件**（全文 `# step = 50`）——**该放流匹配实现的位置是空的**；② **100 条候选默认取 `proposals[0]`**（`agent_lightning_module.py` 注释写 `# randomly choose a dp proposal`，**实际不是随机**），**学到的 scorer 只在 `combined_inference=True`（默认 False）时启用**，全仓无 `no_scorer` 字面量；③ **代码真正依赖的两个资产都不在仓库内**（`transfuser_config.py:17 plan_anchor_path = /nas/.../fps_navsim_traj_768_3.npy` 与 CF 的 GTRS `navhard_two_stage.pkl`，都是**硬编码作者本机绝对路径**），而仓库里反而有 2 个**零引用**的词表（`traj_final/16384.npy` / `8192.npy`）；④ **v10 推理时把 `EP SCORE` 写死为常数 `1.0`**（`:513`），README 自称的 "v10 = command + EP SCORE as condition + rfe Module" 里 **EP 条件并未真正注入**；⑤ README 的 Model Zoo 表里链接名与实际文件名不符。

**四条判断**：① **GuideFlow 的 43.0 目前无法从发布代码复现**（评测路径与论文机制不在同一文件，且 v6 有未定义变量）→ **引用时必须标"仅论文自述 + 发布代码不可直接复现"**；② **"受约束流匹配"要打折扣**：**没有投影算子、没有约束梯度、没有训练期能量项**，实际是"朝一条 GTRS 专家轨迹做常数速度偏置 + 推理期 ESDF 条件 CFG"；③ **λ 与 `k_c` 两个论文超参都无法从发布代码复现**；④ **同类陷阱的第三种形态**——此前记过"配置覆盖链"（TransFuser 的 `n_layer`）与"配置全量关闭"（ORION 的扩散消融），**GuideFlow 是"两套并列代码树 + 靠注释切换 import，而论文机制落在未被评测路径 import 的版本里"** → **读这类仓库必须先确认"评测入口 import 的是哪个文件"**。

**产出**：[C003 §N](../code/traces/diffusion_planner_code_traces-2.md) 新增一节（对照表 + N.1–N.4），文件头同步；[papers/diffusion_planner_ad.md](../topics/diffusion-planner/papers/diffusion_planner_ad.md) DP-A12 行补代码级结论；[state.md](../state.md) 新增**第七类陷阱**（判断边界）与待续第 13 项状态更新；[preparation.md 方向 A](../ideas/preparation.md) 新增一条"把最像投影的那一篇也打掉了"的补充；[repositories.md §F](../code/repositories.md) / [README.md](../../../README.md) 同步。**未克隆任何仓库**（走 `raw` 取证）。

### 23. LCS（DP-A26）与 BridgeDrive（DP-A08）的代码级核验

**动因**：上一节（§20）的全表核验新发现 6 个仓库；§21、§22 已核完 ReCogDrive 与 GuideFlow。本轮把**与研究对象接点最紧的两个**也补上：**LCS**（"引导成本"——单次前向替代两次前向的 CFG）与 **BridgeDrive**（扩散桥，且同时报 NAVSIM 与 Bench2Drive）。两篇都走 `raw` 逐文件取证（**未克隆**）。

**LCS（[C003 §O.1](../code/traces/diffusion_planner_code_traces-2.md)）——"单次前向"是真的，但"省算力"没有代码证据**：

- **确实少跑一次模型调用**：标准 CFG 路径 `agent_lcs.py:941` 跑 cond、`:962` 跑 uncond、`:969` `pred_route = pred_route_uncond + cfg_scale*(cond − uncond)`；**LCS 默认路径 `:929-931` 只调用一次**（注释原文 "Standard forward pass with conditional prompt - LCS is applied inside model"）。**关键确认：全仓无 `torch.cat([cond, uncond])` 式的 CFG 批拼接**（`driving.py` 里三处 `torch.cat` 分别是 token 拼接、跨样本累积、loss 拼接）→ **省掉的确实是第二次前向**，代之以**离线预计算的隐空间方向向量**（`driving.py:194-198` `driving_features + lmsi_scale * shift`；`mean_shift_scale = 0.1`；`data/mean_shift_deltas_cfg03.pt` **在仓库内，1.4 MB**，键为 6 个导航命令各自的质心 − 全局质心）。
- **但代码里没有任何 FPS / FLOPs / latency 数字**（全仓 grep 只命中 `agent_lcs.py:1104-1106` 一处 `print("[TIMING] ...")`，**只打印、不落盘、也不对比单/双前向**）→ **"省一半算力"只有机制推论，无代码证据**。
- **四处陷阱**：① `use_cfg_latent`（`config_lcs.py:11`）**全仓只此一处出现、从未被读取**（声明未接线）；② `use_mean_shift_cfg` 的环境变量**只能置 True、无法关**（要关得改源码）；③ **`mean_shift_deltas_path` 是相对路径**，而评测脚本从不 `cd` 到仓库根 → **cwd 不对时只打印 `Prior file not found, steering disabled` + 一个 WARNING，评测照常跑完** → **引导被静默关闭、分数照出**（最隐蔽的一条）；④ `cfg_scale = 3.0` 在 LCS 模式下是**死参数**。
- 附带查明：**`dropout03` = 训练期命令丢弃概率 0.30**（`train_lcs.yaml:41-42` + `dataset_driving.py:235-240`）；生成质心文件的 `extract_mean_shift_centers.py` **不在仓库内** → 质心如何统计不可核验。

**BridgeDrive（[C003 §O.2](../code/traces/diffusion_planner_code_traces-2.md)）——桥是真的，但步数与锚点路径都硬编码**：

- **桥核与论文一致**：`model_diffusion_head_ddbm_v5.py:204-223` 注释原文 `# 1. add truncated noise to the plan anchor`，`x_T = plan_anchor`、`x_0 = targets["trajectory"]`；`get_abc:38-49` 是 **DDBM 的 VP-SDE 桥核**（`a_t = exp(logsnr_T − logsnr_t + logs_t − logs_T)` 等），合成 `samples = a_t·xT + b_t·x0 + c_t·noise`。→ **但代码里没有任何 "Doob" / "h-transform" 字样**，也没有独立 SDE 求解器。
- **论文的"PF-ODE / 一阶 DDIM 足够"在代码里没有对应命名**：`sample_step`（`:59-76`）里是**一个未命名的确定性一阶更新式**（只在首步 t=T 注入噪声）。**全仓无 `PF-ODE` / `Euler` / `Heun` 字面量**。
- **三处硬编码/失效**：① **NAVSIM 侧 `step_num = 20` 是硬编码**（`:272-273`，**任何 yaml/sh 都改不了**；LEAD 侧是配置项但脚本覆盖值与默认值相同，等于没覆盖）；② **锚点 yaml 指向作者机器绝对路径**（`bridgedrive_agent_k80_beta10.yaml:17` = `/data/workspace/shuliu/...`），类默认又指向**不存在**的 `kmeans_navsim_traj_20.npy`，而**仓库内实际提供的是 `kmeans_navsim/navsim_anchor_k80.npy`（10368 B）** → 需手改；③ **`ddbm_training`**（`config_training.py:262 = True`）被 `planning_decoder_bridgedrive.py:182/196` 依 `'route' in data` **强制改写**；④ `beta_d` **三套值**（类默认 2.0 / `DDBMScheduler` 里 19.9 死默认 / yaml 1.0）。
- **无任何引导/约束项**（全仓 `cbf|guidance|reinforce|penalty` 只命中 README 叙述文字）→ 与论文"约束只来自锚点先验"一致。
- **两个数字本仓都不可闭环复现**：**Bench2Drive 87.99/74.99** 需外部 Bench2Drive 指标模块（本仓只 vendor 了 `leaderboard_evaluator_v2.py`，依赖 `3rd_party/Bench2Drive/scenario_runner` 等外部目录）；**NAVSIM 88.0** 的权重不在仓内（`run_main_testing_...sh:11` 是占位符 `CKPT=/change/to/your/ckpt/path`）。**"补丁式发布"**：README 要求先 clone DiffusionDrive / LEAD 再覆盖文件；仓内还残留 `model_diffusion_head_ddbm{,_v8,_v8v5}.cpython-310.pyc` —— **v8/v8v5 的 `.py` 源文件不在仓库里**。

**两条判断**：① **LCS 的 single-pass CFG 是目前看到的"省算力"里最干净的实现**（真的少一次前向），但**没有算力实测** → 若本项目要做"引导的成本"这条线，LCS 可作对照实现，**延迟必须自己测**；② **BridgeDrive 是"理论叙述 > 代码实现"的又一例**（桥核真、但 PF-ODE 无对应命名、步数与锚点硬编码、两个基准数字都不可闭环复现）→ **引用其 88.0 / 87.99 时必须加限定**。

**产出**：[C003 §O](../code/traces/diffusion_planner_code_traces-2.md) 新增一节（O.1 LCS / O.2 BridgeDrive / O.3 两条判断），文件头同步；[papers/diffusion_planner_ad.md](../topics/diffusion-planner/papers/diffusion_planner_ad.md) 的 **DP-A26 与 DP-A08 两行**补代码级结论；[state.md](../state.md) 待续第 13 项更新（6 个新仓库已核 4 个）；[repositories.md §F](../code/repositories.md) / [README.md](../../../README.md) 同步。**未克隆任何仓库**。

### 24. MPDiffuser（DP-A23）与 DIPOLE（DP-A17）的代码级核验——6 个新仓库全部核完

**动因**：§20 新发现的 6 个仓库已核 4 个（§21–§23）。本轮补最后两个，**把"研究对象侧代码可用性"这条线彻底结账**。两篇都走 `raw` 逐文件取证（**未克隆**）。

**MPDiffuser（[C003 §P.1](../code/traces/diffusion_planner_code_traces-2.md)）——"非梯度可行性注入"是真的，但仓库是 JAX 且两个入口是坏的**：

- **动力学模型是"学出来的扩散转移模型"**（不是解析式、也不是环境真值）：`mpdiffuser/model/dyn_model.py:8-30`，条件 `(x_t, t, x0, u, conds)`，目标是预测噪声；**训练入口在仓库内**（`scripts/train.py model=dynamics`）。
- **"参与去噪"发生在每一个去噪步，方式是替换状态子块**：`mpdiffuser/policy/mpdiffuser.py:65-73` —— 动力学预测噪声 → 用**动力学自己的扩散后验** `p_mean_variance` 推进一步 → **替换状态块（动作块不变）** → 规划器再做自己的后验去噪；且 `:75` 的 **`use_pmean_var=False` 是硬编码**（`diff_utils.py:135` 默认是 True）→ 这是机制成立的前提。动力学那一步**也走 CFG**。
- **"非梯度"成立，但理由要写清**：全程只有 `apply`（前向），**没有显式 `no_grad`/`detach`**（JAX，压根没构造计算图）；全仓 `jax.grad` 只有两处，**都不在 MPDiffuser 路径上**。
- **三处硬问题**：① **`Planner` 类自身是坏的**——`model/planner.py:125` 的**嵌套** `sample_step` 在 `:127/:129` 调用 **`self.sample_step`，而该类里没有这个方法**（全文件只有 `:125` 一处 `def sample_step`）→ **`--method planner` 必 `AttributeError`**；② **`GuidedSampler`（`diff_utils.py:183`）只有 `__init__` 与 `__call__`**，而 `diffuser_policy.py:58` 取 `sampler.sample_step` → **`--method guided` 也坏**；③ `sample_cond` 是死代码。**好消息：论文方法主路径不受影响。**
- **权重与数据都不可得**：树清单**无任何 `.pt/.ckpt`**；README `:157` "coming soon" **仍成立**、`:3` Project Page 仍是 `TODO`；**无数据下载入口**；**README 无结果表**。

**DIPOLE（[C003 §P.2](../code/traces/diffusion_planner_code_traces-2.md)）——不是策略梯度，是 IQL + 有界优势加权 flow 回归**：

- 主仓 `LRMbbj/DIPOLE` 确为**占位**；实现在 **git submodule** → `Whiterrrrr/dipole-rl`（**默认分支是 `master`**）。
- **RL 形态**：**无 `log_prob`、无重要性比率、无比率裁剪、无 KL**；**有 critic 与 value**；优势是 **IQL 型逐样本 `q − v`**（`dipole.py:122`）；总损失 `v_loss + c_loss + pos_loss + neg_loss`。→ **IQL + 优势加权 flow-matching 回归（RWR 型）+ 正/负对偶 actor + CFG 推理**。
- **与 DIVER 的"名实不符"不同**：DIPOLE **从不自称 GRPO**（它声称"KL 正则 RL 的 greedified 重构"）→ **自称与代码自洽**。→ "RL 词义核验"清单补一条注记。
- **"稳定训练"的机制可核**（论文关键主张）：核心是**有界 sigmoid 权重** `sigmoid(beta·value + k)`（`dipole.py:14-19`）替代 IQL 的 `exp(α·adv)`——**权重恒在 (0,1)，指数项才是 loss explosion 的源头**；配套 **Q 集成取 min（悲观）**、**Polyak 目标网 `tau=0.005`**、**IQL expectile 值**。
- **奖励全部来自离线数据集**（`:64`），**无奖励模型**。
- **三处接线缺陷**：① **`q_agg` 半接线**（`value_loss` 遵守 `:39`，但 **actor 加权处硬编码 `min`** `:121`，而 README 要求两个域用 `mean`）；② **`seed`（`get_config():331`）声明后从未被读取**；③ **`encoder` 是未回填的 `placeholder(str)`**（`:332`），而 `create():250` 直接访问它。
- **可跑性最干净的一篇**（无未定义变量、无硬编码本机路径、无 pdb 残留），代价是依赖栈老（`mujoco-py` + `d4rl==1.1` + `gym==0.23.1`）且**不含权重与数据**。
- **一处缺口**：主 README `:74-88` 有 **NavSim 结果表（`DP-VLA w/ DIPOLE navtest` EPDMS 94.8）**，但 submodule **只含 ExORL 与 OGBench，没有任何 NavSim/驾驶代码** → **该表对应配置在发布物中不存在**。

**三条判断**：① **MPDiffuser 是"生成过程内注入可行性"的第四条实现路线**（前三条：PC-Diffuser 逐去噪步 CBF-QP、FeaXDrive SDF 软引导、GuideFlow 常数速度偏置）→ **只能作机制参考，不能作可复现基线**；② **DIPOLE 给"RL 稳定训练扩散策略"提供了一个可核的具体机制**，且**自称与代码自洽**；③ **两个仓库都不适合直接跑**（一个坏入口 + 无资产，一个老依赖 + 无驾驶代码）→ **静态核验的边际收益已接近零**。

**产出**：[C003 §P](../code/traces/diffusion_planner_code_traces-2.md) 新增一节（P.1 / P.2 / P.3），文件头与"6 个全部已核"的注记同步；[papers/diffusion_planner_ad.md](../topics/diffusion-planner/papers/diffusion_planner_ad.md) 的 **DP-A23 与 DP-A17 两行**补代码级结论；[state.md](../state.md) **待续第 13 项标记为可关闭**；[repositories.md §F](../code/repositories.md) / [README.md](../../../README.md) / [inbox/cleanup.md](../../../inbox/cleanup.md) 同步。**未克隆任何仓库**。→ **研究对象侧"代码可用性 + 代码级核验"这条线至此全部结账：34 篇论文表 + 18 个有代码的仓库（13 已克隆逐文件 + 5 走 raw）。**

### 25. 世界模型 arXiv ID 补录结账：NeMo 与 OccVAR 都"没有 arXiv 版本"

**动因**：这两条从第八轮起就一直挂在待续清单上（"arXiv 按标题找不到，需回综述原文核对全称"），是**待续清单里最老的两个小缺口**。

**结论——两条都不是抄错，而是"根本没有 arXiv 版本"**：

| 名称 | 真实全称 / 出处 | 为什么搜不到 |
|---|---|---|
| **NeMo** | **Neural Volumetric World Models for Autonomous Driving**（Zanming Huang、Jimuyang Zhang、Eshed Ohn-Bar，Boston University） | **只有会议版**：**ECCV 2024**（LNCS vol. 15075 Part XVII, pp. 195–213；dblp `conf/eccv/HuangZO24`；OpenReview `mWazUXaT6d`）。**arXiv 实测 0 命中**（`ti:"Neural Volumetric World Models"` 与 `all:"Neural Volumetric World Models"`）→ 撞名的是 NVIDIA **NeMo** 工具链，与本文无关 |
| **OccVAR** | **OccVAR: Scalable 4D Occupancy Prediction via Next-Scale Prediction**（Bu Jin、Xiaotao Hu、Songen Gu、Yupeng Zheng 等） | **是未中稿并已撤稿的 ICLR 2025 投稿**（OpenReview `X2HnTFsFm8`，2024-11-15 作者主动撤稿），**从未上传 arXiv**。→ **同作者组的后继工作改名为 [OccTENS](https://arxiv.org/abs/2509.03887)（`2509.03887`，"OccTENS: 3D Occupancy World Model via Temporal Next-Scale Prediction"）**，**已实测确认该 arXiv 页的 `<title>` 与 `citation_title` 均为 OccTENS** |

**方法论收获（已写进论文表）**：**按标题在 arXiv 找不到时，先怀疑"根本没有 arXiv 版本"（只有会议版 / 撤稿投稿），再去 OpenReview 与出版社目录页反查——不要只反复换关键词搜 arXiv。**

**产出**：[world-model/papers.md §3](../topics/world-model/papers.md) 的"仍未解决（2 项）"表改为"**已全部解决（2/2）**"，两条各自给出真实全称、出处与引用建议；[state.md](../state.md) 待续**第 1 项标记为已全部解决（8/8）**；[README.md](../../../README.md) 同步。**未克隆任何仓库、未新增临时目录**。

### 26. VLA 边界外清单复核：15 条里 9 条升为正式收录（VLA-20–28）

**动因**：`vla/papers.md` §3 的边界外清单长期挂着两行"未逐一核验团队"的条目（4 个方法 + 11 篇预印本），是待续清单第 2 项。

**做法**：按 [literature-quality.md](../../../shared/literature-quality.md) 的口径（已发表看 CCF/白名单；预印本看**强团队 +（官方代码 或 方法独特）**）逐条核 venue / 团队 / 代码。

**结果：15 条 → 9 条升为正式收录、2 条继续留在边界外、4 条仍不确定。**

**T1 两条（venue 硬证据）**：
- **AutoMoT**（`2603.14851`）→ **VLA-20**：**ICML 2026 Spotlight Poster**。**venue 独立核实**：ICML 官方 slides `icml.cc/media/icml-2026/Slides/64489.pdf` + poster 页 `659594` + 一作（Wenhui Huang，Harvard）LinkedIn 明示 accepted。团队 = **NTU AutoMan Lab + Harvard + 小米汽车**；代码 `OscarHuangWind/AutoMoT` + HF 模型 + HF 数据集 `nuSync`。**与本项目最相关**：它有 **"Generative (Diffusion) Head" / diffusion-based action refiner** → **Bench2Drive 87.34 DS / 70.00% SR，加 refiner 后 89.42 DS / 74.09% SR**（**高于 SimLingo 的 85.07**）→ **VLA 侧"带扩散头"的实证**。
- **NuInteract**（`2505.08725`）→ **VLA-21**：**IEEE TIP 2026（CCF-A）**。**venue 独立核实**：DOI `10.1109/tip.2026.3719473` 经 **Crossref 反查**确认为 "IEEE Transactions on Image Processing, 2026"，标题与 arXiv 一致。团队 = HUST（Xiang Bai）+ 小米汽车。

**T4 七条**（强团队 + 代码或方法独特）：**VaViM/VaVAM**（valeo.ai，官方代码 + **权重**）、**UniDriveVLA**（HUST + 小米汽车，官方代码/模型）、**LaST-VLA**（清华 + 小米汽车，NAVSIM v1 91.3 / v2 87.1）、**Reasoning-VLA**（NUS Tat-Seng Chua 等，官方代码）、**SpanVLA**（UCLA + **Motional** + Northeastern，**flow-matching + GRPO**）、**Counterfactual VLA**（**NVIDIA + UCLA + Stanford**，自反思机制，无仓库）、**DriveAction**（**Li Auto**，开源数据集，但**是基准不是规划器**）。

**继续留在边界外 2 条**：**LangCoop**（原"无录用信息"的理由已失效——查到 **CVPRW 2025**，但 **Workshop 不在白名单**）、**StyleVLA**（TUM + NTU，但**匿名投稿** + 无公开代码）。

**仍不确定 4 条**：**HiST-VLA**（Bosch Corporate Research + 上海大学，NAVSIM v2 EPDMS 88.6，**无代码**）、**SAMoE-VLA**（清华 AIR，代码仅 "will be released soon"）、**LVDrive**（HKUST + 小米汽车，无代码无录用）、**AutoDrive-R²**（阿里 AMAP，无代码无录用）——**团队都不弱，但既无代码也无录用，未同时满足 T4 双条件** → 留待复检。

**一条方法论收获（已写进论文表）**：**"取不到 venue"常常不是"没有 venue"，而是"arXiv `comments` 里没写"**——AutoMoT 与 NuInteract 的 `comments` **都不含录用信息**，venue 分别来自 **ICML 官方 slides/poster 页** 与 **Crossref 按 DOI 反查**。→ **venue 核验要三渠道并行：arXiv `comments` + OpenAlex 按标题 + Crossref 按 DOI**（且 OpenAlex 匿名查询会 **429 限流**，需备用渠道）。

**产出**：[vla/papers.md](../topics/vla/papers.md) **新增 VLA-20–28 共 9 行**（表内从 19 篇扩到 **28 篇**）、§2 证据边界与 §3 边界外清单整段重写；[state.md](../state.md) 待续**第 2 项标记为已完成**、VLA 篇数与摘要级计数同步；[README.md](../../../README.md) 同步。**未克隆任何仓库**。

### 27. AutoMoT（VLA-20）的全文 + 代码核验：**扩散头没有发布**

**动因**：§26 把 AutoMoT 从边界外升为 VLA-20 时，理由是"**ICML 2026 Spotlight + 带扩散动作精修头 + Bench2Drive 89.42 DS**"——**这三条合起来就是对"扩散生成"这条路线最强的证据**。所以补做全文 + 代码双侧核验（**未克隆**，走 `raw` 逐文件取证，缓存 47 个文件）。

**全文口径**：架构是 MoT 三件套——**UE = Qwen3-VL-4B 冻结**、**AE ≈1.6B 从零训练**、**AR = DiT 扩散策略**；UE 出 CoT，AE 出 **3 个 meta-action（1 s 间隔）+ 6 个 waypoints（0.5 s）+ 20 个 route points**。**异步推理**把 UE 写进 persistent KV cache 后，延迟从同步版 **117.3 ms（8.5 Hz）** 降到 **37.0 ms（27 Hz）**；**开 AR 后是 143.3 / 63.0 ms（7.0 / 16.0 Hz）** → **"37 ms · 27 Hz" 是不含 AR 的口径**。扩散头是**独立后置模块**（不是接在 AE 内部），以 **AE 的轨迹 proposal 为 informative prior（anchor）** 做**截断反向去噪**（起点既非白噪声也非聚类词表），扰动是**乘性高斯噪声**，条件经 **AdaLN** 注入、另两路条件用 **MoA** 并联融合，**损失 = L1 重建误差**。→ **步数与噪声日程，全文（正文 + 附录 + 表格）都没给**。

**数字**：**AutoMoT+（含 AR）89.42 DS / 74.09% SR；AutoMoT（不含 AR）87.34 / 70.00** → **扩散精修头净收益 +2.08 DS / +4.09 SR**（论文注明 AutoMoT+ 是多次运行均值）。同表 SimLingo 85.07 / 67.27、AutoVLA 78.84 / 57.73、MindDrive 78.04 / 55.09、ORION 77.74 / 54.62、DiffusionDrive 77.68 / 57.72。**该表只有 DS/SR，没有 Effi/Comf，也没有 5 项 Ability 分解**。nuScenes 开环（**ST-P3 协议**）L2 avg 0.32 / 碰撞率 avg 0.07。**UE 微调会灾难性遗忘**（TallyQA 81.40→52.40、InfographicVQA 89.30→50.20）。

**代码核验（本轮最要紧的一条）：扩散头根本没有发布。**
- **仓库 TODO `README.md:33 - [ ] Release the Action Refiner` 未勾选**（其余四项 `[x]` 已勾）；README 自报的数字是 **"DS=87.34 / SR=70.00"，即不含 AR 的那个口径**。
- **全仓 grep `diffusion` / `refiner` / `denois` / `adaln` / `num_inference_steps` —— 零命中**。实际规划头是**纯 MLP 回归**：`automot.py:183 class WaypointsHead(nn.Module)`（6 点，(B,6,2)，含可学习 query）、`:141 class RouteHead`（20 点 cumsum）；推理 `evaluation/inference.py:112 action = self.model.waypoints_head(...)` → `:244 cumsum` → `leaderboard/team_code/mot_b2d_agent.py:1156 pred_traj = output['traj']` **直接送 PID，无任何精修**。
- 只剩三处**脚手架**：`modeling_utils.py:63 class TimestepEmbedder`（抄自 DiT，仅被 FSDP auto-wrap 登记）、`cache_utils/taylorseer.py:117 cache_init(num_steps)`（抄自 TaylorSeer，**全仓无人 import → 孤儿文件**）。
- **配置侧**：`configs/automot_traj_{train,eval}.yaml` 只有 dataset/frame/image 参数，**没有任何 diffusion/refiner 键** → **不是"论文有、配置里关了"（ORION 式），而是"论文有、代码里根本不存在"，比 ORION 更彻底**。
- 其余核对：异步频率是 `slow_update_interval`（默认 2，**B2D agent 从不传**）；`action_tokens = 26`；**无硬编码本机路径、无未定义变量、只有 `release` 一个分支**（没有藏 refiner 的分支）；数据量对得上（`num_used_data: 599852` vs 论文 >70 万）。

**输入权限第三层口径**：论文写 "multi-view and multi-frame RGB"，**代码只有 4 帧历史前视 RGB（每 5 步采 1 帧）+ 1 帧 LiDAR BEV**，数据标记只有 `<image>`/`<front>`/`<bev>`，**无环视相机** → **"输入权限必须按使用层标注"的第三次印证**（前两次：AutoVLA 的三层口径、`use_external` 两个方向都错）。

**三条判断**：① **"VLA + 扩散头拿到 B2D SOTA"这条证据目前不可用**——**89.42 / 74.09 无法从发布代码复现**，引用时必须写"来自未发布的 Action Refiner，仅论文自述"；② **但它给了一个有价值的机制描述**：扩散头是**独立后置模块**、以 **VLA 的 proposal 为 anchor** 做截断去噪（**anchor 不是 K-means 词表**——这是与 DiffusionDrive 的关键差别），且**"异步推理 + KV cache"把 UE 成本压到 0** → 对"**扩散精修 vs 端到端扩散生成**"这个对照有参考价值；③ **输入权限要按代码标**。

**产出**：[vla/papers.md](../topics/vla/papers.md) 新增 **§9（9.1–9.5）**、VLA-20 行加"⚠ 必须降级"标注、§2 证据边界更新（已读全文 14、代码核验 7）；[state.md](../state.md) 与 [README.md](../../../README.md) 同步。**未克隆任何仓库**。

### 28. DriveFuture 的 "24.2→55.5" 是一处误读——**更正一条设计前提**；并读 SpanVLA / LaST-VLA / UniDriveVLA / FutureX 全文

**动因**：`preparation.md` 第 2 节有一条"已验证事实"：**"改条件输入的收益大于改生成日程"**，其唯一量化依据是"DriveFuture 换条件后在 navhard 上把 DiffusionDrive 从 24.2 提到 55.5"。本轮读 DriveFuture 全文时发现**这是误读**。

**更正内容（已改 6 处）**：

| 项 | 原记 | 实际 |
|---|---|---|
| 24.2 与 55.5 的关系 | "条件化把 24.2 提到 55.5" | **是 Table 1（navhard SOTA 对比）里两行不同方法**，且 **55.5 含 GTRS-Dense scorer** |
| 受控收益 | （隐含 +31.3） | **Table 4（navhard，不含 scorer）：30.9 → 34.6，即 +3.7** |
| "条件 vs 辅助损失" | 未记 | **条件化 34.6 vs 直接 future-latent MSE 32.1（+2.5）**（Table 4） |
| 规划器实现 | 未记 | **条件扩散（DDPM，DiT 5 层）+ 100 条候选 + GTRS-Dense 选优**；**去噪步数论文未给** |
| 接口位 | 未细分 | **②隐状态级条件**：**16 个 future query token（d=256）** 喂进去噪器 `ε_θ(a_s, s, C_scene, Z̃)` |

→ **"24.2→55.5"混入了"换方法 + 换选优器"两重差异**，不能当作条件化的收益。**修正后还翻出一个新判断**：**navhard 上的高分离不开选优器**（DriveFuture 55.5、WoTE 88.3/87.1 都靠 scorer）→ **"选优器"这一环在困难基准上的权重可能被低估**。

**同轮的关键对照（新证据，来自 SpanVLA）**：**SpanVLA 的 Table 4 是"回归头 → flow matching"的受控消融：85.1 → 90.3（+5.2 PDMS）**，同一 VLM 编码下只换动作头，代价是动作生成 0.02→0.08 s（5 步）。→ **"生成机制"这一维的受控收益（+5.2）与"改条件"（GoalFlow +4.7 / DriveFuture +3.7）同量级** → **`preparation.md` 那条"改条件远大于改生成日程"的判断被推翻，改写为"两侧都在 +3 ~ +5，没有一方远大于另一方"**。

**三篇 VLA 全文的新事实**：
- **SpanVLA（VLA-26）**：起点是**历史轨迹嵌入经 MLP（不是纯高斯）**、**5 步**；RFT **82.1→90.3（+8.2）**；**其 "GRPO" 论文自己声明取消了 clip**（§4.1 原文 "single policy update per step … eliminates the need for clipping or maintaining an old policy"）→ **"RL 词义核验"第 7 种，但属"论文明确说明的简化"而非名实不符**；奖励是**复合式**（PDMS + 负样本 L2 + 恢复 + 推理长度 + 一致性规则）；**无 Bench2Drive、无 GitHub 仓库**。
- **LaST-VLA（VLA-24）**：**纯自回归离散 token，无扩散/流匹配/VAE**（waypoints 用**文本 token**）；**GRPO 较完整**（组内标准化优势 + clip + KL）→ **第 8 种**；消融 **去 WM+3D 的 RL 87.2 vs 91.3（+4.1）**、**文本 CoT 87.2 vs 潜 CoT 91.3（+4.1）**；**README "Currently Supported Features" 四项全未勾选** → 实际不可复现。
- **UniDriveVLA（VLA-23）**：**MoT 三专家 + Action 分支内嵌 flow matching，全文无 RL**；**B2D DS 78.37 / SR 51.82**；**代码/权重/数据均已发布**（只差 `Release model on Navsim`）→ **本批四篇里唯一接近可复现的**。

**世界模型侧（FutureX，WM-19）全文**：接口位 **②隐状态级条件**（潜世界模型出推理链 `Z_CoT`，Summarizer 以 `Z_CoT` + 初始轨迹回归修正量）；**规划器是非生成式纯回归**；**"条件 + 辅助损失并存"**（`L_lat` 把预测未来潜对齐 GT 未来潜）；NAVSIM navtest PDMS **LTF 83.8→89.2（+5.4）**、**TransFuser 84.0→90.2（+6.2）**，CARLA Longest6 DS **+11.0/+18.6**；**无官方代码** → "条件 vs 辅助损失"只能按论文文字判断。

**另更正一处判断边界**：此前写"**VLA 侧没有一篇用扩散出轨迹**"——**已不成立**：SpanVLA 有 flow-matching 动作专家、UniDriveVLA 的 Action 分支内嵌 flow matching、AutoMoT 有（未发布的）扩散精修头 → **VLA 侧"VLM + 生成式动作头"已成主流配置之一**。

**产出**：更正落在 6 处——[preparation.md 第 2 节](../ideas/preparation.md)（那条"已验证事实"整段重写）、[DP-A31 全文笔记](../topics/diffusion-planner/notes/DP-A31-drivefuture.md)、[world-model/papers.md](../topics/world-model/papers.md) WM-09 行、[transfer.md](../topics/diffusion-planner/transfer.md)、[diffusion_planner/lineage.md](../topics/diffusion-planner/lineage.md)（两处）、[DP-A12 笔记](../topics/diffusion-planner/notes/DP-A12-guideflow.md)、[diffusion_planner_ad.md](../topics/diffusion-planner/papers/diffusion_planner_ad.md) 的"主要基准"行；新增 [vla/verification-2.md §10](../topics/vla/verification-2.md)（三篇全文核验）、WM-19 行全文级更新、state.md 的"RL 词义核验"清单扩到八种与"VLA 侧没有一篇用扩散"的更正。**未克隆任何仓库**。
