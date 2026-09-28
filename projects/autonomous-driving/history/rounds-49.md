# 第四十九轮（2026-09-28）· 把路线 B 的第一步写成预注册实验协议

**动因**：用户要求继续消化现有内容并迭代工作空间与工作流。项目待续第 7 项仍是“候选收敛后再写实验协议”，但候选、资源与主基准已明确；路线 B 的第一步也已在 sota-plan.md §8.5 写成四项纯推理测量。实验目录却仍为空，入口索引还标注待建设。

## 整理与决定

将已达成的决定落为 experiments/protocol.md 的**预注册草案**，限定为冻结 DiffusionDrive 的路线 B 第一阶段，不把研究方向升级为正式立项，也不声称已经运行。协议包含：

1. 固定 NAVSIM v2 navhard 与 devkit commit 0a380a9 的 EPDMS 口径；
2. 分清已发布选优输出、固定候选 0 的 floor、离线 oracle ceiling，以及扩至 100 候选后的 ceiling；
3. 定义 floor gap、selection loss、pool gain，并明确 oracle 使用 GT、仅作离线诊断，不能作为 agent 推理输入或部署成绩；
4. 记录 checkpoint / 数据 / 代码版本、候选张量语义、种子、时延、失败数和逐场景原始结果；
5. 把 HF checkpoint、navhard 数据、环境搭建和 100 候选机制列为启动阻塞；小样本重复后再确定运行噪声判据。

**重要限制**：只从作战计划与已有基准核验摘录协议前提；没有 checkpoint、数据或可运行环境，因此本轮没有模型运行结果。100 候选扩池在协议中是条件测量，必须先核实生成机制与可比性，不能默认改配置即可实现。

## 工作空间更新

- state.md 待续第 7 项改为第一版协议已建、尚未运行，保留数据与环境阻塞。
- index.md 将实验协议从待建设改为可点击入口，标明四项测量及未运行状态。
- 根 README.md 的轮次表增加第四十九轮指针。

## 产出

| 类别 | 文件 |
|---|---|
| 实验协议 | [experiments/protocol.md](../experiments/protocol.md) |
| 项目状态 | [state.md](../state.md) |
| 导航 | [index.md](../index.md)、[README.md](../../../README.md) |

**待验证**：链接检查与工作区检查尚未执行；轮次收尾前需运行项目检查脚本并审阅 diff。
