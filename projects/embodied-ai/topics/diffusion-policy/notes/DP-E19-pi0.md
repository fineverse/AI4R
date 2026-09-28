# DP-E19 · π0

- **原题**：π0: A Vision-Language-Action Flow Model for General Robot Control
- **作者/载体**：Kevin Black 等（Physical Intelligence）；arXiv [2410.24164](https://arxiv.org/abs/2410.24164) v4（2024-10-31 首发）
- **代码**：[Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi)（见 [code/repositories.md](../../../../autonomous-driving/code/repositories.md)）
- **证据等级**：全文（arXiv HTML 逐节提取）+ 摘要
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 观测 | 2–3 路 RGB + 语言指令 + 本体关节 q | §IV |
| 动作 | 连续动作块 A_t=[a_t…a_{t+H−1}]，**H=50**，各机器人动作维 7–17；控制频率最高 50 Hz | §IV、§V-C |
| 生成机制 | **条件流匹配**（非 DDPM）：起点高斯 A_t^0、线性高斯路径、前向 Euler **10 步**（δ=0.1）；无蒸馏 | §IV |
| 架构 | PaliGemma VLM + 300M 动作专家（论文称总 3.3B）。**⚠ 更正（第二十九轮）**：代码实测配置为 `gemma_2b` + `gemma_300m` = **2.3B**，全仓 grep 不到 3.3B 的来源——见 [transfer.md §1.4](../../../../autonomous-driving/topics/diffusion-planner/transfer.md) | §IV + 代码静态检查 |
| 关键设计 | VLM 预训练重要（π0 vs π0-small）；**action chunking + 流匹配对高频灵巧任务关键**（OpenVLA 无 chunk 而失败） | §VI-A |
| 数据 | **>10,000 小时真机数据**（903M timesteps：106M 单臂 + 797M 双臂），7 机器人/68 任务；OXE/Bridge/DROID 占 9.1% | §V-A |
| 结果 | 基座 5 任务全部超过 OpenVLA/Octo（Fig.7）；复杂任务平均分 >50% 满分（Fig.13）；语言跟随优于 π0-small（Fig.9） | 各图 |

## 作者自述局限（§VII）

- 预训练数据配比未公开说明。
- **跨域（驾驶/导航/腿足）正迁移待验证**——作者自己承认这是未验证问题。

## 对本项目的意义（AI 判断）

- 最适合直接改为驾驶 VLA 的一篇：多相机 + 语言 → 轨迹块，接口最顺。
- **明显不成立**：动作为关节角而非轨迹；50 Hz 远高于规划层频率，需改表示；无多智能体交互与动力学约束。
- 对本项目最关键的一条：作者明确把"驾驶/导航的跨域迁移"列为未验证——如果本项目想走"具身机制迁移到驾驶"，这条自述正好说明空白存在，但同时也说明**没有现成证据可借用**。

## 待核验

- Fig.7/13 的具体分值（图中数字未获取）。
- openpi 代码是否包含可直接迁移到轨迹规划的抽象（需代码静态检查，尚未做）。
