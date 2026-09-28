# E2E-06 · ChauffeurNet（监督方式转折：扰动增强 + 环境损失）

- **原题**：Learning to Drive in a Day / ChauffeurNet: Learning to Drive by Imitating the Best and Synthesizing the Worst
- **作者/载体**：Mayank Bansal 等（Waymo）；arXiv [1812.03079](https://arxiv.org/abs/1812.03079) v1（2018-12）；被后续工作引作 RSS 2019
- **代码**：无官方开源（已核实）
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **笔记日期**：2026-09-22

## 关键事实（已核验）

| 项 | 内容 | 来源 |
|---|---|---|
| 输入 | **mid-level 自顶向下特权 BEV**：400×400px、0.2m/px、视野 80m×80m（前向 64m）；通道含 roadmap、红绿灯时序、限速、route、自车框、动态物体框时序、历史位姿 | §3.1、Fig.1 |
| 输出 | 未来轨迹 N=10、δt=0.2s（≈2s），含 x,y,heading,speed + 自车框热图；交由控制器转转向/加速 | §3.1、Table 1 |
| 监督 | IL + **扰动增强**（中点抖动 ±0.5m、航向 ±π/3、权重 1/10）+ **环境损失**（碰撞/在路/几何/物体/道路掩码）+ past-motion dropout 50% + imitation dropout p=0.5 | Eq.13–15 |
| 关键设计 | 合成"最坏情况"扰动样本 + 环境损失——**用合成失败样本弥补纯 IL 的分布覆盖不足** | 摘要、§5 |
| 评价 | 无 CARLA/nuScenes。闭环仿真 20 场景：绕停靠车通过 **90%**/碰撞 10% | Fig.7 |
| 推理成本 | **160ms（≈6.3 FPS，P100）** | Table 2 |
| 自述局限 | 前向 64m/侧 40m 限制 merge 与高速转弯；不支持 U-turn/cul-de-sac；低速卡顿、转弯半径过大、对慢车过激 | §6.5 |

## 在脉络中的位置

- **继承**：ALVINN / NVIDIA PilotNet 式 IL、CIL 的条件化、MP3 的规划思想。
- **转折意义**：它是**监督方式**的第一次转折——从"纯 IL"走向"IL + 合成扰动 + 环境代价"，也是"输入即特权"阶段的代表。

## 对本项目的意义

2025–2026 的 DIVER（DP-A16）用"多参考轨迹 + 负样本"、DP-A34 用"扰动样本设计评分器数据"，本质上是**同一条思路（合成困难样本）在十年后的回归**。这条线值得在 idea 讨论中作为先例引用。
