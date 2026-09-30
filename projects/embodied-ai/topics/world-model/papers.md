# 世界模型（具身侧）论文表

更新时间：2026-09-30  
检索范围：2018–2026，按 [literature-quality.md](../../../../shared/literature-quality.md) 分档后收录 **14 篇**（含奠基工作）。  
证据状态：**全部为摘要级**（arXiv 摘要 + `comments` + OpenAlex/Crossref 的 venue 记录 + 官方 README；**未读正文**）。  
**质量依据**：T 档含义见 [literature-quality.md](../../../../shared/literature-quality.md) §4；venue 三渠道并行核验。**引用数按 OpenAlex「标题」查得，多数命中 arXiv 存根、系统性低估**，**不用于排序**。  
相关：[lineage.md](lineage.md)、[大方向脉络](../../direction/lineage.md)、驾驶侧同名小方向 [autonomous-driving/topics/world-model](../../../autonomous-driving/topics/world-model/papers.md)（24 篇全文级）

## 1. 代表工作

| 编号 | 论文 | arXiv | 年 | venue / T 档 | 预测表示 | 训练目标 | 与策略的耦合 | benchmark | 官方代码 |
|---|---|---|---|---|---|---|---|---|---|
| E-WM-01 | **World Models** | `1803.10122` | 2018 | NeurIPS'18 / T1 | 潜特征（VAE + RNN） | **重建** | **潜空间 rollout**（在"梦"里训策略） | CarRacing / VizDoom | [hardmaru/world-models](https://github.com/hardmaru/world-models)（无权重） |
| E-WM-02 | **PlaNet** | `1811.04551` | 2019 | ICML'19 / T1 | 潜状态（RSSM） | **重建** | **潜空间 rollout**（CEM 规划选动作） | DMC / Atari | [google-research/planet](https://github.com/google-research/planet)（无权重） |
| E-WM-03 | **Dreamer v1** | `1912.01603` | 2020 | ICLR'20 / T1 | 潜状态 | **重建** | **潜空间 rollout**（想象中 actor-critic） | DMC / Atari | [danijar/dreamer](https://github.com/danijar/dreamer)（无权重） |
| E-WM-04 | **Dreamer v3** | `2301.04104` | 2023 | **Nature 2025**（DOI `10.1038/s41586-025-08744-2`）/ T1 | 潜状态（symlog） | **重建 + 奖励** | **潜空间 rollout** | 150+ 任务 / Minecraft | [danijar/dreamerv3](https://github.com/danijar/dreamerv3)（**有权重**） |
| E-WM-05 | **Dreamer 4** | `2509.24527` | 2025 | venue 未取到 / **T4** | 视频 token（扩散） | 重建 / 预测 | **潜空间 rollout + 联合**（在视频 WM 内部做 RL） | Minecraft | **未找到官方仓库** |
| E-WM-06 | **TD-MPC2** | `2310.16828` | 2023 | ICLR'24 / T1 | **隐式潜特征（无解码器）** | **预测 + TD** | **潜空间 rollout**（MPC 局部轨迹优化） | 104 任务（4 域） | [nicklashansen/tdmpc2](https://github.com/nicklashansen/tdmpc2)（**有权重**） |
| E-WM-07 | **Genie** | `2402.15391` | 2024 | ICML'24 / T1 | 视频 token + **潜动作** | 重建 / 预测 | **当环境**（可玩生成环境） | 平台游戏（**无动作标签视频**） | 无官方代码 |
| E-WM-08 | **UniSim** | `2310.06114` | 2023 | **ICLR'24 oral** / T1 | 视频（扩散） | **预测** | **当环境 + 当预训练** | 真机（零样本迁移） | 无官方代码 |
| E-WM-09 | **iVideoGPT** | `2405.15223` | 2024 | NeurIPS'24 / T1 | 视频 token（压缩） | **预测（自回归）** | 当环境 + 当预训练 | RoboNet / 真机 | [thuml/iVideoGPT](https://github.com/thuml/iVideoGPT)（**有权重**） |
| E-WM-10 | **Genie Envisioner** | `2508.05635` | 2025 | venue 未取到 / **T4** | 视频潜（扩散） | 重建 / 预测 | **当环境 + 联合训练**（GE-Act flow matching） | 真机（AgiBot）/ CALVIN | [AgibotTech/Genie-Envisioner-V1](https://github.com/AgibotTech/Genie-Envisioner-V1)（**有权重**） |
| E-WM-11 | **V-JEPA 2** | `2506.09985` | 2025 | venue 未取到 / **T4** | 特征（预测）+ 潜动作 | **预测（无重建）** | **当预训练 + 潜空间规划** | 真机（Franka） | [facebookresearch/vjepa2](https://github.com/facebookresearch/vjepa2)（**有权重**） |
| E-WM-12 | **DINO-WM** | `2411.04983` | 2024 | ICML'25 / T1 | **frozen DINOv2 特征** | **预测（无重建）** | 潜空间 rollout（test-time 规划） | 6 环境 / 真机 | [gaoyuezhou/dino_wm](https://github.com/gaoyuezhou/dino_wm)（无权重） |
| E-WM-13 | **WorldVLA** | `2506.21539` | 2025 | venue 未取到 / **T4** | 图像 token + 动作 | **预测（自回归）** | **联合训练**（动作 ↔ 未来帧互促） | 真机抓取 | [alibaba-damo-academy/WorldVLA](https://github.com/alibaba-damo-academy/WorldVLA)（**有权重**） |
| E-WM-14 | **DiWA** | `2508.03645` | 2025 | CoRL'25 / T1 | 潜特征 | **预测 + 奖励** | **联合训练**（WM 微调扩散策略） | 真机 | [acl21/diwa](https://github.com/acl21/diwa)（**有权重**） |

**未入表但质量可**：Dreamer v2（`2010.02193`，ICLR'21）、DIAMOND（`2405.12399`，NeurIPS'24 Spotlight，Atari 扩散 WM）、VPP（`2412.14803`，ICML'25 Spotlight）、NWM（`2412.03572`，CVPR'25）、WMPO（`2511.09515`）、RoboDreamer（`2404.12377`）、DreamGen（`2505.12705`）、Aether（`2503.18945`，ICCV'25）、EnerVerse（`2501.01895`，NeurIPS'25）、Cosmos（`2501.03575`）、Wan（`2503.20314`）、Emu3（`2409.18869`）、RoboVerse（`2504.18904`）、DayDreamer（`2206.14176`，CoRL'22）。

## 1.1 逐行证据等级与代码状态（2026-09-30 补，供跨表检索）

> 证据等级定义见 [rules.md](../../../../ai/rules.md) §证据等级；代码状态取自本表「官方代码」列与 §3，**未新查**（体例同驾驶侧 [world-model/papers.md §1.1](../../../autonomous-driving/topics/world-model/papers.md)）。
> **本表 14 篇全部为摘要级**（未读正文，见 §3）。

| 编号 | 证据等级 | 代码状态 |
|---|---|---|
| E-WM-01 World Models | 摘要级 | 有代码（**无权重**） |
| E-WM-02 PlaNet | 摘要级 | 有代码（**无权重**） |
| E-WM-03 Dreamer v1 | 摘要级 | 有代码（**无权重**） |
| E-WM-04 Dreamer v3 | 摘要级 | **有代码 + 权重** |
| E-WM-05 Dreamer 4 | 摘要级 | **未找到官方仓库** |
| E-WM-06 TD-MPC2 | 摘要级 | **有代码 + 权重** |
| E-WM-07 Genie | 摘要级 | 无官方代码 |
| E-WM-08 UniSim | 摘要级 | 无官方代码 |
| E-WM-09 iVideoGPT | 摘要级 | **有代码 + 权重** |
| E-WM-10 Genie Envisioner | 摘要级 | **有代码 + 权重** |
| E-WM-11 V-JEPA 2 | 摘要级 | **有代码 + 权重** |
| E-WM-12 DINO-WM | 摘要级 | 有代码（**无权重**） |
| E-WM-13 WorldVLA | 摘要级 | **有代码 + 权重** |
| E-WM-14 DiWA | 摘要级 | **有代码 + 权重** |

**小结**：**11/14 有官方代码**，其中 **7 篇同时有可下载权重**；无代码 3 篇（Genie、UniSim、Dreamer 4——均为 DeepMind / 作者未开源）。**全部为摘要级** → **代码状态是自述未验证**。**注意与驾驶侧的差别**：本表奠基工作（World Models / PlaNet / Dreamer v1）**有代码但无权重**，是"经典但不可直接跑"的一类。

## 2. 四个结论

1. **"重建 → 预测 → 对比"这个顺序不成立**。成立的只有前半段：**重建主导 2018–2023**（World Models / PlaNet / Dreamer v1–v3 都带像素解码器）；**转折点是"特征预测"**——**V-JEPA（`2404.08471`，2024-02）**摘要明示 "without the use of … **reconstruction**"，**DINO-WM（`2411.04983`，2024-11）**明示 "**without reconstructing** the visual world"。**"对比"不是后一阶段，而是自 2020 年起的平行支线**（C-SWM `1911.12247` ICLR'20、DreamerPro `2110.14565`、ReCoRe `2312.09056` CVPR'24）；**VPP（`2412.14803`，ICML'25 Spotlight）摘要把"单图重建"与"双图对比"并列为"此前范式"** → **对比与重建是并列旧范式**。
2. **潜空间 rollout 没有被取代，而是与生成式环境"分化"**：**生成式环境服务"仿真与数据生成"**（UniSim `2310.06114` ICLR'24 oral 与 Genie `2402.15391` ICML'24 是起点，后接 DIAMOND、NWM、Genie Envisioner）；**潜空间 rollout 服务"决策优化"**（TD-MPC2 ICLR'24 仍在做 "local trajectory optimization **in the latent space**"；DINO-WM 做 test-time 规划）。**Dreamer 4（2025）把两者合流**——在视频世界模型**内部**做潜 rollout（Minecraft 实时）。
3. **"世界模型 + 策略"的耦合有 4 类，与驾驶侧的"接口五条路线"是不同切法**：① **潜空间 rollout**（E-WM-01~06）② **当环境**（E-WM-07~10）③ **当预训练**（E-WM-11/12）④ **联合训练**（E-WM-13/14、Dreamer 4）。**对照驾驶侧**：驾驶侧分的是"**未来以什么形式被消费**"（接口位置），具身侧分的是"**世界模型对策略扮演什么角色**"（功能角色）。映射：**具身① ↔ 驾驶⑤**（RL 想象 rollout）、**具身② ↔ 驾驶④**（当评价器/环境）、**具身③ ↔ 驾驶②③**（当条件）、**具身④ ↔ 驾驶①**（联合自回归）。**具身侧没有独立的"选优依据"类**——因动作是高维连续，选优被吸收进潜 rollout 内部（TD-MPC2 的 MPC、DINO-WM 的 test-time 规划）。
4. **输入与驾驶侧差在四点**：① **无固定 ego 坐标系、无 HD map**，靠第一视角视觉流；② 动作空间是**连续关节 / 末端位姿（高维）**，驾驶是 2D 轨迹（低维）；③ 具身的"未来"是**物体 / 接触的演化**，驾驶的是 BEV 占据 / agent 轨迹；④ **具身世界模型普遍 action-conditioned**（Genie 用无监督潜动作、NWM / UniSim 直接吃动作），**驾驶侧多以 ego 轨迹 / 导航命令为条件**。

## 3. 证据边界与不确定项

- **全部摘要级**：benchmark 与"权重可用性"均为 README / 摘要自述，**未本地运行**。
- **venue 取不到**：Dreamer 4、Genie Envisioner、V-JEPA 2、WorldVLA；DINO-WM 的 ICML'25 来自二手渠道（非三渠道之一）。
- **引用数不可用**：多为 arXiv 存根（VPP / UniVLA / Dreamer 4 / DreamGen / EnerVerse 显示 0，而它们实为 ICML'25 Spotlight / NeurIPS'25 等）；Genie Envisioner 与 DiWA 在 OpenAlex **无记录**（记为"无记录"，**不是 0**）；World Models 按标题命中的是 1956 年同名天文论文（**已剔除**）。
- **代码不确定**：Genie、UniSim、Dreamer 4 未找到官方仓库（DeepMind / 作者未开源）；World Models / PlaNet / Dreamer v1 有代码**无权重**。
