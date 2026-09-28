# 世界模型（具身侧）脉络

更新时间：2026-09-23  
状态：**初稿**（第二十五轮）。写**判断**，事实见 [papers.md](papers.md)。  
相关：[大方向脉络](../../direction/lineage.md)、驾驶侧同名小方向 [autonomous-driving/topics/world-model/lineage.md](../../../autonomous-driving/topics/world-model/lineage.md)

## 1. 三段

| 段 | 时期 | 分界标志 | 代表 | 耦合方式 |
|---|---|---|---|---|
| **W1 重建式潜空间 rollout** | 2018–2023 | **World Models（`1803.10122`，NeurIPS'18）** → PlaNet → Dreamer v1/v2/v3 | Dreamer v3（**Nature 2025**） | 在潜动力学里想象 → 学策略 / MPC |
| **W2 特征预测（去重建）** | 2024–至今 | **V-JEPA（`2404.08471`，2024-02）**"without reconstruction"；**DINO-WM（`2411.04983`）**"without reconstructing the visual world" | V-JEPA 2、DINO-WM、TD-MPC2（隐式潜特征） | 当预训练 / 潜空间规划 |
| **W3 生成式环境 + 联合训练** | 2023–2026 | **UniSim（ICLR'24 oral）与 Genie（ICML'24）**把世界模型变成"可玩的生成环境"；**WorldVLA / DiWA / Dreamer 4（2025）**转向联合训练 | Genie 系列、Genie Envisioner、iVideoGPT、Cosmos、WorldVLA、DiWA | 当环境（造数据）/ 联合优化 |

## 2. 三条判断

1. **W1 → W2 的驱动力是"重建像素是浪费"**：Dreamer v3 到 2023 年仍带像素解码器；**2024 年 V-JEPA 与 DINO-WM 明确把"不做重建"写成卖点**。→ **这与驾驶侧"从 4D 占据转向潜特征"（WM-02 → WM-06/07/08）是同一转向，时间也接近（2024）**——**两侧独立收敛到"特征预测优于像素/占据重建"**。
2. **W3 是"功能"变化，不是"表示"变化**：W2 与 W3 可以并存（V-JEPA 2 既是 W2 的预训练表征、也做 W3 的规划）。**真正的分界是"世界模型是否与策略联合优化"**——WorldVLA（动作促未来帧）、DiWA（世界模型微调扩散策略）、Dreamer 4（在视频 WM 内做 RL）。
3. **具身侧"选优"这一环被吸收了**：**驾驶侧有独立的"选优依据"接口（WM-01 / WM-24 / WM-04 / WM-07），具身侧没有**——因为具身动作是高维连续、候选集难以枚举，**选优被折进潜 rollout 内部**（TD-MPC2 的 MPC 局部轨迹优化、DINO-WM 的 test-time 规划）。→ **这是两侧接口分类的最大结构差异**。

## 3. 与驾驶侧同名小方向的关系

- **切法不同**：驾驶侧按"**未来以什么形式被消费**"分五条接口路线；具身侧按"**世界模型对策略扮演什么角色**"分四类。映射关系见 [papers.md §2 结论 3](papers.md)。
- **最易搬的一支**：**具身③"当预训练"（V-JEPA 2 / DINO-WM / VPP）与驾驶侧 WM-07 / WM-09"只预训练表征"同构**。
- **最难搬的一支**：**具身①"潜空间 rollout"**——驾驶侧对应的是路线 ⑤（RL 的 reward/next-state 来源），而这条在驾驶侧**是五条里唯一"零可核验代码"的**（WM-23 Imagine-2-Drive、WM-16 Raw2Drive 都无可用代码）。

## 4. 待补

- **全文级证据**：本小方向 14 篇**全部摘要级**，无一读过正文。
- **未回答**：**"世界模型 + 扩散策略"的接口**（即 [README.md](README.md)「要回答的问题」第 3 条）目前只有 WorldVLA / DiWA 两个摘要级线索，**无代码级证据**。（**⚠ 更正（第二十九轮）**：原文写"本页 §3 的第三问"，但本页 §3 无"第三问"，实为 README 的问题清单第 3 条。）
- **候选待收**：DIAMOND（NeurIPS'24 Spotlight）、VPP（ICML'25 Spotlight）、NWM（CVPR'25）、DreamGen 等（见 [papers.md](papers.md) 末尾）。
