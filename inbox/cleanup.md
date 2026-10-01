# 待清理清单

用途：AI 在工作流程中**不执行删除**，把待删项累积到本文件；会话收尾（或一天一次）时合并成**一条命令**，用户只授权一次。
规则来源：[ai/rules.md](../ai/rules.md)「执行与清理纪律」。

## 当前待清理

> **当前无待清理项。**
>
> **⚠ 第四十八轮（2026-09-28）起**：临时产物根 = **`inbox/scratch/`**（**工作空间内**，见 [ai/rules.md](../ai/rules.md) §执行与清理纪律第四十八轮修正）——`/tmp` 在权限自动允许范围之外，**每一次访问都会弹授权**，故 `/tmp` 下**不再产生**中间产物。
> **另注（第七十七轮更新口径）**：`inbox/scratch/` 内**已完成使命的一次性产物**按 [ai/rules.md](../ai/rules.md) §执行与清理纪律第 7 条**收尾批量清除即可、不必登记本表**；git 跟踪的工作空间文件删除走 `git rm` 也不登记；**本表常态只留工作空间外**的清理。
> **投递物 ≠ 待清理**：`inbox/` 根下的支线投递物由 §轮次收尾第 9 步处理（采纳/否决/搁置后移入 `archive/`），**不登记本表**；另有机器检查兜底（`check_links.py` 第 11 项）。

## 执行记录

**2026-10-01 清理（第 77 轮登记项，用户授权后由 AI 执行）**

| 路径 | 清理前 | 结果 |
|---|---|---|
| `inbox/scratch/` | 37 个文件 / 26 个条目 | 已删除，复查残留 **0** |
| `shared/ccf/scripts/__pycache__/` | 1 个 `.pyc`（未被 git 跟踪） | 已删除 |

- **命令**：`rm -rf /home/verse/dev/AI4R/inbox/scratch/* /home/verse/dev/AI4R/shared/ccf/scripts/__pycache__`（即第 77 轮登记原文，一条一次授权）。
- **范围**：第 77 轮登记的 34 个文件（周扫 API 缓存 xml ×10、9-30 改表备份 ×9（git 有前置版本）、Zotero 对账脚本与样本 ×12、榜单探测 ×2、`xorg.conf.2k60` ×1）＋ **第 78 轮产生的 `r78_baseline/`**（规则重构前基线 ×3——验证已完成，原件在提交 `e1e8d8e` 可随时取回，随本条一并清除）。
- **安全网**：删除前的 `tar` 备份仍在 **`/tmp/ai4r_scratch_backup_20261001.tar.gz`**（210 KB，仅覆盖第 77 轮的 34 个文件）——**/tmp 重启即失**：下次重启前可从 tar 恢复，重启后以 git 提交 `e1e8d8e` 为最终回滚点。
- **结论落盘已核**（第 77/78 轮两轮巡查双确认）：榜单结论在 `sota-plan.md §1.0`、周扫机制在 `ai/workflows.md §周扫`、其余为一次性脚本/测试样本。
- **复查**：Glob `inbox/scratch/**` 无文件；`shared/ccf/scripts/` 仅剩 `parse_ccf_2026.py`（保留项）。

**2026-09-30 清理（第六十二轮收尾；命令由用户执行）**

| 路径 | 清理前 | 结果 |
|---|---|---|
| `/tmp/ai4r-clonetest/` | 16 MB（GitHub 连通性测试所克隆的 navsim） | 已删除 |
| `/tmp/ai4r-*`（a4s / consensus / s2 等 19 个） | 约 88 KB（API 连通性测试与检索样本） | 已删除 |

**核实**：用户执行 `rm -rf /tmp/ai4r-clonetest /tmp/ai4r-*` 后，主线程以**只读方式**复查（Glob `/tmp/ai4r*`）**残留 0**。

**违规留档（不是疏漏，是教训）**：该批落在 `/tmp`，**违反第四十八轮「临时根 = `inbox/scratch/`」的约定**——当时是跨会话长任务，前段沿用旧习惯。**规则层面已堵住**：见 [ai/rules.md](../ai/rules.md) §支线协作纪律**第 7 条**（"支线的临时产物同样进 `inbox/scratch/`，不得落 `/tmp`"）。

| 被删内容 | 体积 | 删除不丢信息的依据 |
|---|---|---|
| `ai4r-clonetest/` | 16 MB | **同一仓库已在 `code/repos/navsim`**（此处是重复副本） |
| `ai4r-a4s-*`（4 个） | 32 KB | 7 篇引用数已入 [具身 VLA 表 §4](../projects/embodied-ai/topics/vla/papers.md)；计费规则已入 [tools.md](../shared/tools.md) |
| `ai4r-consensus-*`（3 个） | 52 KB | 字段与端点已入 [tools.md](../shared/tools.md) |
| `ai4r-s2*`（12 个） | 4 KB | 429 实测与 **S2 `venue` 字段会系统性误记**已入 [tools.md](../shared/tools.md) |

**2026-09-28 遗留清理（第四十八轮，用户一次授权，已执行）**

| 路径 | 清理前 | 结果 |
|---|---|---|
| `/tmp/ai4r/` | **28 MB / 65 条目** | 已删除 |
| `/tmp/ai4r-*` | 0（散件已于 2026-09-24 清完） | 无需处理 |

**为什么只需跑一次**：临时根迁到 `inbox/scratch/` 后，这一批就是**最后一批** `/tmp/ai4r/` 产物（第二十九至四十七轮累积的脚本、备份、论文 PDF+txt、负向测试备份等）。
**清理后复查**：`/tmp/ai4r*` 残留 **0**。

**2026-09-24 收尾清理（用户一次授权，已执行）**

| 路径 | 清理前 | 结果 |
|---|---|---|
| `/tmp/ai4r/` | 877 MB / 205 条目 | 已删除 |
| `/tmp/ai4r-*` | 47 个 / 约 14 MB | 已删除 |
| `projects/diffusiondrive/`（11 个空目录） | 0（树状重构残留） | 已 `rmdir` |
| `shared/domain/`（1 个空目录） | 0（CCF 上提后的空壳） | 已 `rmdir` |

**执行前做了三件核验**：

1. 派 1 个**只读子代理**抽查 `/tmp/ai4r` 的结论类缓存（`navhard_top_probe`、`automot_probe`、`codecheck`、`dd_anchor`、`digest`、`surv`、`pdf*`、`vla`、`clone_*` 等），确认**结论全部已落盘**到论文表、`code/traces/`、`verification*.md`、`judgments.md`、`sota-plan.md`，**无"只在缓存里"的内容**。
2. **两个维护脚本先抢救到 [shared/scripts/](../shared/scripts/)**（`check_links.py`、`normalize_links.py`），未随删除丢失。
3. 空壳目录用 **`rmdir` 而非 `rm -rf`**——若非空（说明迁移有遗漏）会报错而不是静默删内容。

**清理后复查**：`/tmp` 下 `ai4r*` 残留 **0**；`projects/diffusiondrive` 与 `shared/domain` 均不存在；全库空目录只剩 `code/repos/` 下 **3 个未初始化的 submodule**（`GoalFlow/nuplan-devkit`、`openpi/third_party/{aloha,libero}`，属正常）与 3 个**有意占位**（`experiments/records`、`experiments/results`、`writing`）。

**已知的既定取舍**（不是疏漏）：原始检索输出与检索脚本未保留——`candidates.tsv`（510 篇去重候选）、`triage.tsv`（68 篇 venue 核验）、`search.sh`、`triage.py`、`normalize_links.py` 之外的修复脚本。按现行规则（工作空间不放批量原始数据），需要时重跑一次检索即可。

## 不在清理范围（长期）

- `projects/autonomous-driving/code/repos/` 的 **37 个代码仓库（1.65 GB）**——交付物，保留。其中有 **3 个未初始化的 submodule 空目录**，属正常；其余空目录都在各仓库的 `.git/` 内部（git 自身结构）。
- `/tmp/trae-agent-toolhost-*/` 下的任务日志——由工具宿主管理，非 AI 产物。

## 使用说明

1. 后续每轮产生的中间产物一律放 **`inbox/scratch/`**（**⚠ 第四十八轮起；此前为 `/tmp/ai4r/`**），流程中不删除；新待删项追加到「当前待清理」。
   - `inbox/scratch/` 在工作空间内 → **不触发授权弹窗**，且已被 [`.gitignore`](../.gitignore) 忽略、被 `check_links.py` 的 `SKIP_DIRS` 跳过。
   - **工作空间内的文件删除已不需要在此登记**（工作空间已 git，见 [ai/rules.md](../ai/rules.md) §执行与清理纪律第 9 条）；本表只留**工作空间外**的清理。
2. 收尾时只跑本表给出的命令，不改权限、不逐条确认。
3. 清理完成后把「当前待清理」清空（保留标题与说明），把过程记入「执行记录」，避免累积过期条目。
