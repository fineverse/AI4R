# 自动驾驶探索项目

项目性质：探索案例，尚未选定为正式课题。  
命名：目录名 `autonomous-driving` 取自**大方向**，因此后续新增小方向时不必再改名。原名为 `diffusiondrive`（第一个案例名），已于 2026-09-23 更正。

## 目标

以大方向**自动驾驶端到端**为背景，以研究对象**扩散规划器（Diffusion Planner）**为核心：建立领域地图与小方向脉络，梳理论文与代码，评估是否存在值得投入实验的可验证方向。

## 范围

- **大方向**：端到端自动驾驶的整体发展脉络、基准与评价协议（见 `direction/`）
- **研究对象（小方向）**：扩散 / 流匹配 / 扩散桥作为自车规划器；轨迹集合生成、约束注入、选优机制、条件来源、评价协议（见 `topics/diffusion-planner/`）
- **借鉴来源（小方向）**：VLA、世界模型（见 `topics/vla/`、`topics/world-model/`）；具身智能作为平级领域见 [embodied-ai](../embodied-ai/index.md)，只取可迁移机制
- 重点基准：NAVSIM v1 navtest（PDMS）、NAVSIM v2 navtest/navhard（EPDMS）、Bench2Drive、nuPlan
- 案例基线：DiffusionDrive（NAVSIM，2 步截断扩散 + 锚点先验）

## 结构约定

项目内固定两层（约定见 [workspace-design.md](../../shared/workspace-design.md)「领域—专题骨架」）：

- `direction/` — 大方向：脉络、基准、领域级综述与笔记
- `topics/<小方向>/` — 小方向：`README.md`（角色/边界/待回答问题）、`lineage.md`、论文表、笔记

跨专题资产放项目根：`sources.md`（来源索引）、`pdfs_pending.md`、`raw/`（检索日志）、`code/`（仓库快照与代码脉络，含三个层级的仓库）。

## 当前边界

- 当前优先做资料、代码和评价协议核验，不自动启动大规模训练或数据下载。
- 扩散规划器是当前聚焦方向，但**未选定为正式课题**；[ideas/preparation.md](ideas/preparation.md) 中的潜在方向均为待验证假设。
- 代码仓库只做克隆与静态阅读，未安装依赖、未运行模型。
- `topics/vla/` 与 `topics/world-model/` 作为**借鉴来源**已建表并**全部读成全文**（VLA 28 篇、世界模型 24 篇，其中 **28** 篇另有代码级核验）；`topics/diffusion-planner/` 为**研究对象**。
- 当前范围和研究约束详见 [context.md](context.md)。

## 当前状态

**进度、待续清单与判断边界一律以 [state.md](state.md) 为准**（本文件不重复，避免失真）。一句话：文献调研完成**二十七轮**，四条发展脉络、**37 个官方代码仓库快照**（1.65 GB，仅克隆未运行）、三份代码脉络与 [idea 讨论准备材料](ideas/preparation.md) 均已就绪；**下一阶段是按 [sota-plan.md](ideas/sota-plan.md) 的四条路线选一个起点、冲 NAVSIM v2 navhard 的 SOTA**（待用户确认资源与是否立项）。
