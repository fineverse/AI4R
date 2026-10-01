# 第七十三轮：重点代码继承关系系统梳理（三批）+ 决策文件消化

日期：2026-10-01

## 起因

用户指出："现有重点代码之间的继承关系是否梳理过"——工作流 [workflows.md §代码脉络梳理](../../../ai/workflows.md) 第 2 步、[templates.md 代码脉络读法](../../../ai/templates.md) 均把"继承关系"列为要素，但实测**只有扩散规划器一侧成体系**：E2E 未成体系、世界模型侧还留了一个指向空章节的悬空指针、VLA/具身无。

用户定：**先明确口径 → 按决策影响度分三批 → 梳理出的有用信息消化进决策文件**。

## 口径（先明确要梳什么）

在 [ai/workflows.md](../../../ai/workflows.md) §代码脉络梳理 定 **S1–S4 继承强度分级**（唯一事实源，其余文件只引用）：

- **S1 硬继承**（`class X(Y)` / fork / 逐行对照坐实）
- **S2 自述派生**（README / 论文 `based on` / `built upon` / `following`）
- **S3 模块复用**（抄损失函数 / vendored 代码 / 同名锚点·词表）
- **S4 团队延续**（仅同团队/同机构，须标"推断"）

边界：继承关系只写"整体血统 / 基线来源"；"模块来自哪篇论文"（组合关系）仍归 `code/traces/`。

## 做了什么

### 批次 1（最高）：E2E 主干 + 扩散规划器

- [direction/lineage.md](../direction/lineage.md) 新增「继承关系（代码层面已核验）」节（**12 行**，含 VADv2←VAD、GenAD←VAD 两处 S1）；原「代表基线」表内的「继承」行升级为指针，不再两处各写一份。
- [diffusion-planner/lineage.md](../topics/diffusion-planner/lineage.md) §继承关系 **增"强度"列**（11 行逐条定级），并加"扩散侧轨线两端"桥接。
- **消化进决策文件**：[preparation.md](../ideas/preparation.md) §6.1 读法 + §6.2「同条件比较」、[judgments.md](../judgments.md) B 组、[judgments-2.md](../judgments-2.md) G 组、[sota-plan.md](../ideas/sota-plan.md) §10.1 —— **四者均引同一份继承事实源**。

### 批次 2：世界模型

- [world-model/lineage.md](../topics/world-model/lineage.md) 新增「继承关系」节（**7 行**，含 `class W4D(VAD)`、LAW 长在 VAD 库两处 S1）。
- **修复悬空指针**：[world_model_code_traces.md](../code/traces/world_model_code_traces.md) 读法行写"继承关系见 `lineage.md`"，而该文件此前**无此节**——本批补齐后指引可达。
- 消化：[judgments-2.md](../judgments-2.md) F 组补事实源指针。

### 批次 3：VLA / 具身（论文级）

- [vla/lineage.md](../topics/vla/lineage.md)（驾驶侧）新增「继承关系」表（**6 行**，无代码核验，上限标 S2/S3）。
- 具身三处按各自"**脉络写判断、事实见 papers.md**"的约定，加**血统判断 + 指针**（不复制论文表）：[embodied-ai/direction/lineage.md](../../embodied-ai/direction/lineage.md)、[embodied-ai/topics/vla/lineage.md](../../embodied-ai/topics/vla/lineage.md)、[embodied-ai/topics/world-model/lineage.md](../../embodied-ai/topics/world-model/lineage.md)；并顺延其后小节编号。

> 说明：计划原列的 `embodied-ai/topics/diffusion-policy/lineage.md` **不存在**（该小方向状态为"未写脉络"），故批次 3 实际落在 **4 份**现有 lineage 上；未新建脉络文件。

## 更正

- **无推翻既有结论**。本轮的实质更正只有一处：确认 [C004](../code/traces/world_model_code_traces.md) 的"继承关系见 lineage.md"此前是**悬空引用**，本批补齐后消解。
- 数处"两处各写一份"的冗余被收敛：direction/lineage.md 表内「继承」行 → 独立节 + 指针。

## 产出

- 新增/改写：`ai/workflows.md`、`direction/lineage.md`、`topics/diffusion-planner/lineage.md`、`topics/world-model/lineage.md`、`topics/vla/lineage.md`、`embodied-ai/` 3 份 lineage、`ideas/preparation.md`、`ideas/sota-plan.md`、`judgments.md`、`judgments-2.md`。
- 分 3 次提交（`8af9421` / `1fc7ac0` / `25a3a37`），逐批可回溯。

## 已知告警（未消除）

- `check_links.py` 仍 **exit 1**，原因仅两项**体积超限**：`ideas/sota-plan.md`（67,243 B）与 `history.md`（66,025 B 起）超 64 KB。
- **两项均为第七十二轮遗留**：`sota-plan.md` 在 `HEAD~3` 已达 66,711 B（本轮只加了约 0.5 KB 引用）；`history.md` 本轮未改其正文（仅按约定加一行索引）。
- 处置：已记入 [state.md](../state.md) 待续清单，作为**独立的结构性任务**（瘦身 / 拆册）处理，不在本轮强改决策核心文件。
