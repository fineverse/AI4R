# E2E 主干代码脉络（第二册：§K–§M）

更新时间：2026-09-23  
证据等级：**代码静态检查**（本册为重建版，内容取自同一批 **L1 逐文件核验**记录；级别定义见 [ai/rules.md §代码静态检查](../../../../ai/rules.md)）。  
**⚠ 本册为重建版**：原 `e2e_trunk_code_traces.md` 的 §K–§M 在一次机械拆分中因脚本 bug 被丢弃（该文件 67 KB、超 Read 工具 64 KB 上限）。本册内容**逐节取自轮次记录**（`history/rounds-24a.md` 的 §11/§13/§16），**事实与 `文件:行号` 完整保留**，措辞与原文不完全一致。  
本册承接 [e2e_trunk_code_traces.md](e2e_trunk_code_traces.md)（§A–§J）。

---

## K. CARLA 系 6 个基线的规划/控制输出——把 §G 的对照表补全到 13 个仓库

CARLA 系 6 个基线的规划/控制输出（把 §G 的规划头对照补全到 13 个仓库）

**动因**：§G 的"非生成式基线规划头对照"只覆盖 **nuScenes 系 4 个**（UniAD / SparseDrive / VAD v1 / VADv2），13 个主干仓库里还有 **CARLA 系 6 个**（TransFuser / TCP / ST-P3 / LBC / CIL / NEAT）从未核过。这批仓库**已在本地**，纯静态阅读，结论写入 [C005 第二册 §K](../../code/traces/e2e_trunk_code_traces-2.md)。

**五条发现**：

- **ST-P3 是"预测占据 → cost → 选优"在 CARLA 侧的早期实例，比 Drive-OccWorld（AAAI'25）早 3 年**：`carla_agent.py:458` `cost_volume=output['costvolume'][:, n_present:].detach()`——**`costvolume` 是模型输出的一路**（与未来占据预测同源）→ `stp3.py:384 select_best_traj` → **7 项规则代价**（`safetycost` / `headwaycost` / `lrdividercost` / `comfortcost` / `progresscost` / `rulecost` / **`costvolume`**，全部 clamp 到 [0,100]）→ **`torch.topk(CS, k, largest=False)` 取代价最小**；采样数 **CARLA 2400 / nuScenes 1800**（`configs/*/Planning.yml`；`config.py:145` 默认 600 是第三个值）。
- **"命令喂不喂给模型"在 CARLA 系内部就不一致**：**TransFuser 与 NEAT 都算了 `next_command` 却从未传给模型**（TransFuser `submission_agent.py:222` 只写进 `result`；`:294-295` 的模型调用参数是 `image, lidar_bev, target_point, target_point_image, velocity`——**没有 command**）；而 **TCP 真的把 `next_command` 传进了 `process_action`**（`tcp_agent.py:204`）。→ 与 nuScenes 系（UniAD / SparseDrive 的 eval 用 GT 命令）合起来：**13 个仓库对命令有三种处理方式**（显式输入 / 算了不用 / 只用 `target_point`）。
- **6 个仓库全部零锚点 / 零词表**，但 **`anchor` 在 TransFuser / NEAT 里指 transformer 的空间 attention 网格**（5×22、8×8）——**极易误判为"轨迹锚点"**。
- **ST-P3 带 VAE 但规划不是生成式（最易误标的一个）**：`distributions.py::DistributionModule` 的 latent 混合分布**只服务未来占据预测头**，规划器是"采样 + 规则代价 argmin"。→ 与 GenAD 形成**位置相反的对照**：**同为 CVAE 式隐变量，一个长在感知侧（ST-P3）、一个长在规划侧（GenAD）**。
- **TCP 是唯一"轨迹 + 控制量双分支"的**：`process_action`（Beta 分布头）与 `control_pid(pred_wp, ...)` 各出一套控制量，按 **`alpha=0.3` 融合**（`tcp_agent.py:216-224`，**两处条件不同的 alpha 赋值**）。

**判断**：**"非生成式基线"的分类从三种扩到五种**——新增 ④ **采样 + 规则代价选优**（ST-P3）与 ⑤ **按命令切分支**（LBC / CIL）。→ **ST-P3 的"采样 + 代价选优"与 DiffusionDrive 的"扩散 + scorer 选优"结构最接近，是最容易被误标成"生成式"的一类**；同时 **"把世界模型输出当 cost 去选优"不是新机制**（ST-P3 ECCV'22 已有）。

**产出（续）**：[C005](../../code/traces/e2e_trunk_code_traces.md) 新增 **§K（6 仓库对照表 + 五条发现 + §G.2 分类补正）**、文件头规模描述更新；[state.md](../../state.md) 的"非生成式基线"一条扩到五种、"命令维"补进输入权限一条；[sources.md](../../sources.md) C005 / [index.md](../../index.md) / [README.md](../../../../README.md) 同步。

## L. TransFuser / TCP / ST-P3 的主张—代码对照（补 §B）

TransFuser / TCP / ST-P3 的主张—代码对照（补 §B 的 5 项）

**动因**：§B 的主张—代码对照只有 **5 项**（VAD / VADv2 / DiffusionDrive / V2），而这三个 CARLA 系代表工作的**架构与损失主张**从未逐条核过。它们既是领域基线，也是 NAVSIM 系扩散规划器所复用主干（TransFuser）的来源。**仓库在本地，纯静态阅读**，结论写入 [C005 第二册 §L](../../code/traces/e2e_trunk_code_traces-2.md)。

**五条发现**：

- **TransFuser 有两个"声明但零权重"的头**：`config.py:134-136` 的 `detailed_losses_weights = [1.0,1.0,1.0,1.0, 0.2,0.2,0.2,0.2,0.2, **0.0, 0.0**]`，末两位正是 **`loss_velocity` 与 `loss_brake`** → 两个头照常计算但**监督权重为 0**；且 `--use_velocity` 默认 **0**。
- **TransFuser 的 `n_layer` 有两套冲突默认值**：`config.py:177` 写 **8**，而 `train.py:56 --n_layer default=4` 且 `:120 config.n_layer = args.n_layer` **覆盖之** → **实际生效的是 4**。→ 与 ST-P3 的 `INSTANCE_SEG/FLOW` 一起，构成"**配置有覆盖链**"这一类陷阱。
- **ST-P3 的 "dual attention" 名不符实**：代码里是 `Dual_GRU`（`layers/temporal.py:59`）= 两个 `gru_cell` + `trusting_gate`（`nn.Conv2d(hidden, 2, 1)`）+ `torch.softmax`，最后 `cur_state = rnn_state2 * trust_gate[:,0:1] + rnn_state1 * trust_gate[:,1:]` → **全仓无任何 attention 运算**（无 QKV、无 multi-head）。→ 引用时必须改写为"**双 GRU 门控混合**"。
- **ST-P3 官方配置关掉了两个头**：`configs/nuscenes/Planning.yml:35-38` 把 `INSTANCE_SEG` / `INSTANCE_FLOW` 置为 **False**，而 `config.py:133,136` 默认 **True** → **单看 `config.py` 会误判多任务规模**；另 `cost_volume` **无直接监督**，仅经规划的 **max-margin 损失**间接学习。
- **TCP 的"轨迹引导"分两层，论文强调的那层在推理脚本里**：网络内是 `wp_att` 注意力（可学习）；**分支主次切换（`alpha=0.3`）是推理启发式**，由转向检测的 `status` 决定（`tcp_agent.py:213-224,237-253`）。→ 复现 TCP 时若只搬网络、不搬这段启发式，行为会不同。

**判断**：**"配置默认值 ≠ 实际生效值"在本工作空间累计到 6 例**（ORION 的 `use_diff_decoder`、HDP 的零权重投影项、Flow Planner 的 `alpha/beta`、WoTE 的 `num_fut_timestep`、**TransFuser 的 `n_layer`**、**ST-P3 的 `INSTANCE_SEG/FLOW`**）→ 已升级为一条判断边界：**读配置必须同时看覆盖链**。

**产出（续）**：[C005](../../code/traces/e2e_trunk_code_traces.md) 新增 **§L（三张主张对照表 + 五条发现）**、文件头规模描述更新；[state.md](../../state.md) 的"代码里有这个名字≠这条路径被走到"一条扩到 **8 例**并补入"配置覆盖链"陷阱；[sources.md](../../sources.md) C005 / [index.md](../../index.md) / [README.md](../../../../README.md) 同步。

## M. LBC / CIL / NEAT / DriveLM 的主张—代码对照（补 §B）

LBC / CIL / NEAT / DriveLM 的主张—代码对照（补 §B；并更正 `lineage.md` 的一个数字来源）

**动因**：§K 只覆盖了这四个仓库的**规划/控制输出**，§L 覆盖了另外三篇的**架构与损失主张**。这四个的主张与代码范围仍空着。**仓库在本地**，纯静态阅读，结论写入 [C005 第二册 §M](../../code/traces/e2e_trunk_code_traces-2.md)。

**五条发现**：

- **"attention"这个词在同一批仓库里有真有假**（本工作空间已有正反例）：**NEAT 的编码器是真 multi-head self-attention**——`architectures/encoder.py:10-46` 的 `SelfAttention` 有显式 `self.key/query/value = nn.Linear(...)`、`n_head` 切分、`att = (q @ k.transpose(-2,-1)) * (1/sqrt(hs))` → softmax → `att @ v`，`config.py:86/89` 是 `n_layer=2 / n_head=4`；而 **ST-P3 的 "dual attention" 实为 `Dual_GRU` + 门控 softmax**（§L.3）。→ **同一批仓库里"attention"必须逐篇看 QKV**。
- **LBC 的学生蒸馏是"全分支输出级 L1"，不是特征回归**：全仓**不存在 `imitation_loss`**；`train_image_phase1.py:195-199` 比较的是**学生 4 分支路点 vs 教师 4 分支路点**。→ 转述 LBC 时**不能说"蒸馏教师特征"**。
- **CIL 缺的是整个运行时**：`.gitmodules` **实测 0 字节**；`carla` 包（`driving_benchmark`/`agent`/`carla_server_pb2`）、训练脚本、数据加载器**全部缺失** → 只剩"网络定义 + 推理 + 一个 ckpt"，**端到端不可复现**。
- **两处"命令条件"的语义被削弱**：**CIL 的命令不是网络输入**，而是推理时 if/elif **选分支**；**4 维 `input_control` 占位符定义后从未被喂入**（全仓只在 `imitation_learning.py:47` 出现一次）。→ 与 §K 的 TransFuser/NEAT"算了 `next_command` 却不传"是**同一类落差**；**"命令条件"在 CARLA 系早期工作里普遍不是真正的网络条件**。
- **`direction/lineage.md` 的 "DriveLM 0.16 FPS" 在本仓库不可核验**：仓库**全无 FPS/latency 代码**，唯一数字是 README 的"**约 2 小时 / 4072 帧（batch 8）≈ 0.57 fps**"（`challenge/README.md:116-119`）——**与 0.16 FPS 不一致**。→ **已就地更正 `lineage.md` 的两处**（补"来源待补"标注 + 说明仓库内数字）。

**判断**：本轮把 E2E 主干侧的主张—代码对照从 §B 的 5 项扩到**覆盖全部 13 个仓库**（§L 三篇 + §M 四篇 + §K 的规划输出），并**顺带修掉一处无来源的引用数字**。

**产出（续）**：[C005](../../code/traces/e2e_trunk_code_traces.md) 新增 **§M（四张主张对照表 + 五条发现）**、文件头规模描述更新；[direction/lineage.md](../../direction/lineage.md) **两处 DriveLM 0.16 FPS 补"来源待补"**；[state.md](../../state.md) 的"代码里有这个名字≠这条路径被走到"一条新增**第六类陷阱（命名与实现语义不符）**、"命令维"一条补入 CIL；[sources.md](../../sources.md) C005 / [index.md](../../index.md) / [README.md](../../../../README.md) 同步。
