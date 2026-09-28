# 第三十二轮（§3 / §4 / §5 溯源收尾 + DriveWorld-VLA 的 ID 错配，2026-09-24）

**动因**：第三十轮把 `preparation.md` 的 **§2（S1–S30）/ §6.1 / §6.2 / §2b** 逐条溯源核验过，但 **§3（明确未解决的问题）/ §4（可迁移机制）/ §5（潜在方向空间，含 §5.0 与方向 A–G）** 与 `judgments.md` 58 条里上一轮未抽查的剩余约 37 条**还没查过**。本轮补上，把 idea 讨论地基的溯源做到 100%。

## 1. 结论

派 1 个只读子代理逐条回溯（数字 + 编号引用 DP-Axx / VLA-xx / WM-xx / Cxxx §X / Bxxx / Pxx 全部落到具体行号）：

| 范围 | 一致 | 矛盾 | 找不到 | 口径错标 |
|---|---|---|---|---|
| §3 / §4 / §5（含 §5.0 与方向 A–G） | ≈100 条 | 1 | 1 | 2 |
| `judgments.md` 剩余 ~37 条 | 全部一致 | 1（ID 配错） | 0 | 1 |

**编号引用的册别与章节号全部正确**（§I=PC-Diffuser、§N=GuideFlow、§J.5/§J.6 均在 C003 第二册、§K 在 C005 第二册）——第三十轮加的第五项检查已经生效。

## 2. 最要紧的一条：**DriveWorld-VLA 的 arXiv ID 配错了**

`judgments.md` 与 `world-model/verification.md`（**两处**：§4.3 的三条判断、§1 的 WM-02 表格行）都写：「`liulin815/DriveWorld-VLA` 又是**另一篇**（`2506.08052`）」。

但 **`2506.08052` 是 ReCogDrive**（[vla/papers.md](../topics/vla/papers.md) VLA-07 / [DP-A28](../topics/diffusion-planner/papers/diffusion_planner_ad.md)）。DriveWorld-VLA 的正确 ID 是 **`2602.06521`**（arXiv 标题页 + ICML 2026 poster 页**双渠道核验**，仓库即 `github.com/liulin815/DriveWorld-VLA`，91.3 PDMS / 86.8 EPDMS）。

**这条更正的讽刺之处值得记下**：那条 bullet 的内容正是「**查代码时必须核对 arXiv ID，不能只核标题**」——**而它自己配错了 ID**，且**同一句话在工作空间里复制了三处**（`judgments.md` §C、`world-model/verification.md` 的 §4.3 与 §1 表格行）→ 三处已全部改并就地标 ⚠，并把"这条更正本身正是该陷阱的实例"写进正文。

## 3. 其余 5 处

| # | 位置 | 问题 | 处理 |
|---|---|---|---|
| 1 | `preparation.md` §4 | "`transfer.md` 收录 **16 条机制**"，但同句的逐条拆解 11+3+1=**15**，且 `transfer.md` §1 表**只有 15 行** | 改为 **15 条**并标 ⚠ |
| 2 | `preparation.md` §5 方向 A | "GuideFlow 是同一基准 navhard 的 **SOTA**（EPDMS 43.0）"——同文件 §6.1 与 `sota-plan.md` 都标为**自报**，且 43.0 不可复现、navhard 榜首是 DriveFuture 55.5 | 改为"**自报** SOTA（43.0；⚠ 社区口径 27.1、不可复现）"，方向 A 的"依据"行同步加"自报" |
| 3 | `preparation.md` §5 方向 B | "DP-A34 用'**横向推向可行驶边界、纵向推向领车**'构造更有信息的样本"——该具体机制在论文表/来源索引里**查不到**（DP-A34 只有 `元数据 + 摘要` 级证据） | 降级为摘要级可核表述（"指出强规划器的候选集中在安全模式、边界附近监督不足"）并标 ⚠ |
| 4 | `preparation.md` §5.0 行 G | 把"**DriveMoE 底座 = π0**"整体挂在 **S22** 上，但 S22 只讲"世界模型 + 扩散规划器两种接法" | 补上真实出处 [vla/verification.md](../topics/vla/verification.md) VLA-04 行与 §4 |
| 5 | `judgments.md` §F | "HDP 相对上游有**四处**未声明退化"引 `[C003 §J.6]`，但 §J.5 才是"四处退化"，§J.6 是"另外两处声明未接线" | 改指 **§J.5**（册别原本就对） |

## 4. 产出与状态

- **改动文件**：`ideas/preparation.md`（§4、§5.0 行 G、方向 A、方向 B）、`judgments.md`（§C 的 DriveWorld-VLA ID、§F 的 §J.5）、`topics/world-model/verification.md`（同 ID）、`history.md`、`state.md`、`README.md`
- **验证**：六项检查全绿（**死链 0 / 行数超限 0 / 表格不匹配 0 / 孤儿 0 / 弱引用 0 / 错册引用 0 / 缺「对本项目的意义」节 0**，退出码 0）；无第一方文档超 64 KB
- **idea 讨论地基的溯源至此 100% 覆盖**：§2 / §2b / §3 / §4 / §5（含 §5.0 与方向 A–G）/ §6.1 / §6.2 / §7 全部核过一遍，`judgments.md` 58 条分两轮全部抽查完
- **待用户**（未变）：① **7.1 可用 GPU 与预算** ② **7.2 是否把"扩散规划器"升级为正式课题**
