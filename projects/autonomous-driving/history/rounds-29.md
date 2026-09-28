# 第二十九轮（具身侧知识层审计 + 引用可达性入检查脚本，2026-09-24）

**动因**：继续执行"整理消化现有内容、迭代工作空间和工作流"。第二十八轮审的是**主项目**的知识层；本轮把同一套五问（① 同一事实的不同说法 ② 悬空引用 ③ 论文表空字段 ④ 笔记可达性 ⑤ 与主项目的一致性）**搬到平级项目 `embodied-ai`**，并把第二十八轮末尾发现的"**笔记孤岛**"彻底收口。

## 1. 先收口"笔记孤岛"：19 篇 → 0 篇

第二十八轮末尾查出 **19 篇笔记只被 `sources.md` 引用**——读论文表的人根本看不到这些论文有全文笔记。当时的约定只存在于 `code/repositories.md` 与 `surveys/`，**论文表没有这个约定**。

| 侧 | 做法 |
|---|---|
| 驾驶侧 | `diffusion_planner_ad.md` **12 行**在「证据状态」列末补一个指向 `../notes/DP-Axx-*.md` 的笔记链接；`code/repositories.md` 的 `TCP` / `ST-P3` / `transfuser` / `ChauffeurNet` **4 行**补笔记链接 |
| 具身侧 | `diffusion_planner_embodied.md` **8 行**（DP-E01/E04/E08/E09/E10/E11/E15/E17）补同一形式的指针 |

**新成文的约定**（写进 [ai/workflows.md](../../../ai/workflows.md) §轮次收尾第 7 条）：**一篇论文有笔记，就要在它出现的论文表行、脉络或 `repositories.md` 里留一个指针**。

## 2. 把"笔记孤岛"这类问题变成可自动发现：`check_links.py` 三项 → 四项

给 [shared/scripts/check_links.py](../../../shared/scripts/check_links.py) 新增**第四项「引用可达性」**：报告「完全无引用（孤儿）」与「只被 `sources.md` 引用（弱引用）」，退出码把**孤儿**计入失败、弱引用只报警告。

**并豁免 `raw/`**：检索日志的唯一正当入口就是 `sources.md` 的登记行，不要求反向链接。若不豁免，其固定 2 条弱引用会永久淹没真正的新弱引用——与死链检查豁免 `archive` 同理。

**另修一个链接扫描的假阳性**：脚本此前只跳过 ``` 围栏代码块，**不跳行内代码跨度**——于是"在文档里举例说明链接写法"（如 `` `[笔记](../notes/x.md)` ``）会被误报成死链（本轮写轮次记录时当场踩到）。→ 加 `strip_code()`，死链与引用可达性两处扫描都先剥掉 `` `...` ``。

→ 现在四项检查全绿：**死链 0 / 行数超限 0 / 表格不匹配 0 / 孤儿 0 / 弱引用 0（豁免 2）**。

## 3. 具身侧查出的问题与处理

### 3.1 八处"同一事实的不同说法"

| # | 冲突 | 处理 |
|---|---|---|
| 1 | **DP-E08 的代码级别三处互相矛盾**（最严重）——具身表文件头写「DP-E08 …为 **L1**（仓库已落盘）」，但同表该行"代码"列写"未核验"、笔记也写"未核验"，而 AD 表 DP-A20 明确「**无公开仓库**」 | **实为 `DP-E01`**：`transfer.md` 列出的 4 个落盘仓库是 `diffuser / diffusion_policy / 3D-Diffusion-Policy / visualnav-transformer` → 文件头改为 **DP-E01**，并就地标 ⚠ 更正 |
| 2 | **"未取得控制频率"与已登记频率冲突**——`direction/lineage.md` 与 `vla/lineage.md` 都列「未取得 RDT-1B / FLOWER / π0.5 的控制频率」，但三者频率**都已登记**（6 Hz / 50 Hz / 50 Hz） | 两份脉络的"未取得"清单**只保留 DP3**，并注明其中的 "50 Hz" 是**执行动作块的控制频率**、不是模型前向频率 |
| 3 | **Consistency Policy 的 venue 两说**——表内"载体与版本"写"正文未标注会议"，影响力快照却记 "RSS 2024" | 快照注明"**venue 取自 OpenAlex 正式版记录，非论文自述**"（口径不同，非矛盾） |
| 4 | **DP-E10 编码器层数**——表与笔记都断言"**3 层 MLP** > PointNeXt"，而 `transfer.md §1.1` 已代码级更正为 **4 层 Linear** | 表与笔记**回填该更正**，并写明仓库的 "simple" 变体改的是 **U-Net 宽度** |
| 5 | **DP-E19「总 3.3B」**——表与笔记直接写 3.3B，而代码实测配置只有 `gemma_2b` + `gemma_300m` = **2.3B** | 两处改为"论文称 3.3B；⚠ 代码实测 2.3B，3.3B 在代码里无法确认" |
| 6 | **具身项目 `history.md` 写"当前 3 轮"，实含 4 轮** | 改为 **4 轮**（第七、八、二十五、二十六轮） |
| 7 | **B009–B011 的归属指错项目**——具身表的节标题把链接指向**主项目** `sources.md`，但主项目已声明 B009–B011 **归属具身智能** | 改指本项目 `sources.md`，并就地标 ⚠ 更正 |
| 8 | **"第二十五轮新增 6 条"被两边各认领一次**——`vla/README.md` 与 `world-model/README.md` 都写"回填 transfer.md 第 1 节（第二十五轮新增 6 条候选）"，而 `transfer.md §1.5` 只有**一份** 6 条清单 | 两份 README 都注明"**§1.5 是 VLA 侧与世界模型侧合并计**，不是各 6 条" |

**另加一处口径差**：`direction/lineage.md` 用 GR00T N1「120 Hz」未带"30 Hz 两说"注，而论文表与 `vla/papers.md` 都注了 → 已补注。

### 3.2 悬空引用三处

1. 上表 #7 的跨项目指错。
2. `world-model/lineage.md` 的「本页 §3 的第三问」——本页 §3 无"第三问"，实为 **`README.md`「要回答的问题」第 3 条** → 改指正确位置。
3. AD 表 §A 的 **DP-E01 指针行漏列**在"指针行"清单里 → 清单补为 **5 行**，并写明"该行**没有 AD 编号，行 ID 直接用具身编号**"。

### 3.3 论文表"未核验"落后于"指针"侧

AD 表的 DP-A17/A20/A23/A24 四行**已给出 2026-09-23 的代码结论**，而"完整登记"的具身表 DP-E05/E06/E07/E08 四行"代码"列仍写"未核验"——**指针侧比完整登记侧更新**，方向反了。

→ 四行回填真实代码状态，**并回指 AD 编号**（`= AD 表 DP-Axx`）；证据状态列同步改为"元数据 + 摘要 + **代码可用性已核（L2/L3/无官方代码/无公开仓库）**"。

## 4. 顺手修掉两处"规则已定但没执行"

1. **`README.md` 的「最近动态」违反了自己定的规则**——[ai/workflows.md](../../../ai/workflows.md) §轮次收尾第 3 条要求"**只留 1–2 行指针，不写结论**"，实际是一张 **11 行结论表**（与 `history.md` / `state.md` 大量重复）。→ 收敛为**一张纯指针表**（6 行，只给轮次 → 卷文件），并把"本节只留指针"写进正文。
2. **`navhard 12 行` 残留 5 处**（第二十八轮只改了 4 处）——`index.md`、`state.md`（2 处）、`preparation.md`（2 处）。实为 **13 行**（[sota-plan.md §1](../ideas/sota-plan.md) 逐行可数）→ 全部改为 13 行。

## 5. 产出与状态

- **改动文件**：`shared/scripts/check_links.py`（三项 → 四项）、`ai/workflows.md` §轮次收尾、`shared/index.md`、`README.md`（最近动态收敛为指针）、`projects/autonomous-driving/topics/diffusion-planner/papers/diffusion_planner_ad.md`（指针行清单）、`index.md` / `state.md` / `ideas/preparation.md`（navhard 行数）、`projects/embodied-ai/` 的 `topics/diffusion-policy/papers/diffusion_planner_embodied.md`、`topics/diffusion-policy/notes/DP-E08|E10|E19*.md`、`direction/lineage.md`、`topics/vla/lineage.md`、`topics/world-model/lineage.md`、`topics/vla/README.md`、`topics/world-model/README.md`、`history.md`、`state.md`、`index.md`
- **验证**：`check_links.py` **死链 0 / 表格不匹配 0 / 孤儿 0 / 弱引用 0 / 退出码 0**；所有 `index.md` / `state.md` ≤100 行；无第一方文档超 64 KB
- **待用户**（未变）：① **7.1 可用 GPU 与预算** ② **7.2 是否把"扩散规划器"升级为正式课题**
