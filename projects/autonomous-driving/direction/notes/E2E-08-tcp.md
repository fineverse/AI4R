# E2E-08 · TCP（监督转折：特权蒸馏 + 轨迹/控制双范式）

- **原题**：Trajectory-guided Control Prediction for End-to-end Autonomous Driving
- **作者/载体**：Penghao Wu 等（OpenDriveLab）；arXiv [2206.08129](https://arxiv.org/abs/2206.08129) v2（2022-10）；NeurIPS 2022
- **代码**：[OpenDriveLab/TCP](https://github.com/OpenDriveLab/TCP)（已下载）
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 输入 | 单目前视 + 速度 + 高层导航；**特权只存在于教师 Roach**（RL 训练，BEV 渲染道路/车道/车/人/灯/停止线） | §3.1 |
| 输出 | **双分支**：K 步航点（经 PID）+ 多步控制 a_t…a_{t+K}（throttle/brake/steer），由"情况融合"合并 | §3.2、§3.4 |
| 监督 | **特权蒸馏**（教师 Roach 的 feature loss L2 + value loss）+ IL（轨迹 L1、控制 beta 分布 KL）+ speed 辅助；L=λ_traj·L_traj+λ_ctl·L_ctl+λ_aux·L_aux | Eq.4–6 |
| 关键设计 | 轨迹引导的多步控制预测 + 情况融合（解决"轨迹准但控制抖 / 控制稳但偏航"的互补性） | §1、§3 |
| 主结果 | CARLA Leaderboard：TCP-Ens **DS 75.137**/RC 85.629/IS 0.873；TCP 69.714 | Table 1 |
| 消融 | 无融合 → 57.01；仅控制 32.45 vs 仅轨迹 28.29（**融合远好于任一单支**） | Table 3、Table 2 |
| 推理成本 | TCP 25.77M 参数 / 8.54G FLOPs / **125.71 FPS**；TCP-Ens 73.03M / 44.70 FPS | Table 4 |
| 自述局限 | 规则化融合需先验；单目视野有限，高速切入刹不住；**不预测他车轨迹**导致阻塞/碰撞 | 附录 D.1 |

## 在脉络中的位置

- **继承**：TransFuser 的自回归航点 + Roach 的 RL 教师。
- **转折意义**：**监督方式**的转折——把 RL 教师作为特权蒸馏信号；同时它是"轨迹 vs 控制"两种输出范式的**融合尝试**，这在后来的脉络里被"多候选轨迹 + 选择"取代。

## 对本项目的意义

TCP 的 125.71 FPS 说明 **CARLA 系的轻量模型早已远超实时**；扩散规划器在 NAVSIM 上追求 45–59 FPS 并不是"实时性突破"，而是**在更强感知/更高指标下的实时性**。这一点在立项叙事里要写准。
