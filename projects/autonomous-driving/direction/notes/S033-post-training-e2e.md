# S033 · Post-Training in End-to-End Autonomous Driving（预印本全文）

- **原题**：Post-Training in End-to-End Autonomous Driving
- **作者/载体**：Ruining Yang 等；arXiv [2607.08072v2](https://arxiv.org/abs/2607.08072)（2026-07-13）
- **代码/列表**：[RYNing/Awesome-Post-Training-In-Autonomous-Driving-Papers](https://github.com/RYNing/Awesome-Post-Training-In-Autonomous-Driving-Papers)
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **笔记日期**：2026-09-22
- **定位**：对应扩散规划器的 RL/GRPO 后训练支线（DiffusionDriveV2、DIVER 都属于这一类）

## 分类框架（全文核验）

post-training 定义为 IL 之后的精炼阶段，按监督形式分四族：

| 章节 | 内容 |
|---|---|
| §3 蒸馏 | — |
| §4 偏好对齐 | DPO 类 |
| §5 RL | 5.1 奖励设计 / 5.2 rollout 收集 / 5.3 策略优化 |
| §6 测试时精炼 | — |
| §7 评测；§8 开放问题 | — |

规模：101 条参考文献（子代理统计）。

## 与扩散/流匹配规划器直接相关的部分（§5.3、§6）

- 明确指出策略**输出空间包含 diffusion outputs 与 flow-based generators**，因此 GRPO 这类"模板适配 token 序列"的方法**需要专门适配**。
- 列出的代表：**Flow-GRPO**（组相对优化适配流匹配生成器）、**WAM-Diff**（GSPO + 掩码扩散策略）、**VDRive**（扩散策略头 + actor-critic）、**Fast-dDrive**（块扩散解码，效率导向）。

## 关键数字（附表号）

| 表 | 内容 |
|---|---|
| Table 1（开环） | AutoDrive-R2 L2 **0.19** / Col **0.07**；Fast-dDrive L2 0.32 / RFS 7.823；AutoVLA 0.40 / 7.557 |
| Table 2（闭环） | EvaDrive PDMS v1 **94.9**；Reasoning-VLA 91.7；TakeVLA DS 89.72 / SR 73.73；AutoVLA 78.84 / 57.73 |
| §7.3 推理成本 | Alpamayo-R1 **99 ms**、DriveAnchor **2.06 ms**、BPF 在 Jetson AGX Orin 吞吐 **+27%** |

## 对评价协议的两条判断（§7.3）

1. **基准饱和**：PDMS/EPDMS 已经聚集，区分度下降（与本项目从 navtest 88–91 得出的结论一致）。
2. **真实车评测稀缺、推理成本普遍漏报**——后者直接支持本项目"必须把延迟与违规率一起报告"的做法。

## 开放问题（§8）

- 奖励与探索的耦合设计；
- 世界模型信号是否具有 behavior-level 相关性；
- 从"一次性精炼"走向**数据反馈闭环**；
- **超越 GRPO 的驾驶感知更新**（局部反馈、分维度约束）——作者认为 GRPO 主导但**非最优**；
- 不限于 RL（蒸馏/偏好对齐）。

## 对本项目的意义

- 若走方向 D（多样性/质量）或"RL 后训练"，S033 是现成的分类与批评来源。
- §8 的"超越 GRPO"是一条**由 2026 年综述明确点名**的空白，比我们自己推断更有说服力。
