# E2E-02 · VAD（全向量化表征）

- **原题**：VAD: Vectorized Scene Representation for Efficient Autonomous Driving
- **作者/载体**：Bo Jiang 等（hustvl，与 DiffusionDrive 同一实验室）；arXiv [2303.12077](https://arxiv.org/abs/2303.12077) v3（2023-08）；ICCV 2023
- **代码**：[hustvl/VAD](https://github.com/hustvl/VAD)（已下载，VAD 与 VADv2 同仓；v1 代码完整，172 个 `.py`）
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22

## 代码核验（2026-09-23）

- `projects/mmdet3d_plugin/VAD/VAD_head.py:405`：**`self.ego_query = nn.Embedding(1, self.embed_dims)`** —— **单模规划**，无词表、无锚点。
- `loss_plan_reg` 为 `L1Loss`（`VAD_base_e2e.py:287` 权重 **1.0**，head 默认 0.25）——**轨迹回归**是唯一规划监督。
- 由此确立对照：**VAD（v1）= 单模回归 → VADv2 = 4096 词表纯分类**，这是"轨迹词表/锚点"机制线的起点。完整谱系见 [e2e_trunk_code_traces.md](../../code/traces/e2e_trunk_code_traces.md) §C。

## 为什么它是转折点

**把场景表征从 BEV 栅格转为全向量化**：map 向量 + agent 运动向量，明确抛弃稠密栅格与代价图（Fig.1、§3.1）。这是"去掉手写后处理"的关键一步。

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 场景表征 | **全向量化**（实例级向量），无栅格 | §3.1 |
| 规划输出 | **单条轨迹** V̂ego∈R^{Tf×2}；2s 历史、规划 3s 未来；agent 侧输出多模态运动向量 | §4.1 |
| 规划架构 | Transformer decoder 做 ego-agent / ego-map 交互 + MLP Planning Head；与在线建图、运动预测端到端联合（另有红绿灯分支） | §3.2–3.4 |
| 监督 | IL + **三条向量化规则约束**：L=ω₁L_map+ω₂L_mot+ω₃L_col+ω₄L_bd+ω₅L_dir+ω₆L_imi（非蒸馏/RL） | Eq.8 |
| 主结果 | nuScenes 开环 **L2 0.72m / 碰撞 0.22%**（Tab.1）；CARLA Town05 Short DS 64.29、Long DS 30.31（Tab.4） | Tab.1/4 |
| 推理成本 | VAD-Base **224.3ms / 4.5 FPS**；VAD-Tiny **59.5ms / 16.8 FPS** | Tab.1、Tab.5 |
| 自述局限 | 多模态运动预测**未用于规划**（只取最高置信）；未纳入车道图/路牌/红绿灯/限速等交通信息 | §5 |

## 继承关系

- **基于**：BEVFormer、MapTR、PIP。
- **被谁继承**：SparseDrive（进一步去 BEV）、VADv2（同组，把输出改为词表分布）。
- **对本项目的直接关联**：VAD/VADv2 与 DiffusionDrive **同一实验室（hustvl）**，代码同仓；DiffusionDrive 的锚点先验在思想上承接 VADv2 的动作词表（见 [VADv2 笔记](E2E-03-vadv2.md)）。

## 对本项目的意义

- 它的自述局限里有一条**至今仍未被解决**："多模态运动预测未用于规划"——即预测的多样性没有进入规划决策。扩散规划器（DIVER、DiffusionDriveV2）用"多候选 + 选择"部分回应了这一点，但**选择环节本身成了新瓶颈**（本项目 [preparation.md](../../ideas/preparation.md) P4）。
- VAD-Tiny 的 **16.8 FPS** 说明：在向量化表征下，实时性早已不是生成式方法的专利。
