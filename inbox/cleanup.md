# 待清理清单

用途：AI 在工作流程中**不执行删除**，把待删项累积到本文件；会话收尾（或一天一次）时合并成**一条命令**，用户只授权一次。
规则来源：[ai/rules.md](../ai/rules.md)「执行与清理纪律」。

## 当前待清理

**第二十九至三十一轮（2026-09-24）产生的中间产物**——均在 `/tmp/ai4r/`，可一条命令删：

| 路径 | 内容 | 是否已落盘 |
|---|---|---|
| `/tmp/ai4r/add_embodied_note_links.py` | 给具身表 8 行补笔记指针的脚本 | 是（结论已写入论文表） |
| `/tmp/ai4r/emb_table.bak` | 改动前的具身表备份（27.4 KB） | 是（改动已就地写入并校验） |
| `/tmp/ai4r/c005_bak/` | 5 个文件的改动前备份（judgments / lineage / e2e_trunk-2 / preparation / rounds-24a） | 是（改动已就地写入并校验） |
| `/tmp/ai4r/fix_c005_volume_refs.py` | 修 C005 错册引用的脚本 | 是（已并入第五项检查，可复跑） |
| `/tmp/ai4r/scan_volume_refs.py`、`scan_c005_volume_refs.py` | 错册引用的清点脚本（已被 `check_links.py` 第五项取代） | 是 |
| `/tmp/ai4r/unify_note_section.py` | 统一笔记节名的脚本（第三十一轮） | 是 |
| `/tmp/ai4r/notes_bak/` | 47 篇笔记的批量改写前备份（316 KB） | 是（已逐文件比对体积确认无丢失） |
| `/tmp/ai4r/judgments_bak_36.md` | `judgments.md` 拆分前备份（62.8 KB，第三十六轮） | 是（拆分已校验：28+31 = 59 条 bullet 守恒） |
| `/tmp/ai4r/split_judgments_36.py` | `judgments.md` 分册拆分脚本（第三十六轮） | 是（已跑第五项检查确认册别 0 错） |
| `/tmp/ai4r/simscale.pdf`、`gtrs.pdf` + 同名 `.txt` | SimScale 与 GTRS 两篇论文（第三十七轮，仅用于逐表核对；PDF 11.7 MB / 1.7 MB） | 是（结论已写入 `sota-plan.md §7.7`、`judgments.md §B`、`preparation.md` P2c/P8、`code/repositories.md` §下一步第 4 条） |
| `/tmp/ai4r/df.pdf` + `df.txt` | DriveFuture 论文（第三十八轮，逐表核 `EPDMS` vs `EPDMS*`；PDF 9.4 MB） | 是（结论已写入 `benchmarks.md §2.9`、`judgments.md §B`、`sota-plan.md §7.7.5`、`DP-A31` 笔记） |
| `/tmp/ai4r/hf_probe.txt`、`hf2.txt`、`odl.html`、`c37.txt`、`final_check.txt` | 第三十七/三十八轮的网络探测与检查输出（HF 不可达的实测记录、挑战页 HTML） | 是（HF 不可达已记入 `state.md` 待续清单第 17 项） |
| `/tmp/ai4r/ddv2.pdf` + `ddv2.txt` | DiffusionDriveV2 论文（第四十一轮，用于把 `PDMS@K` 的语义核到原文；PDF 3.6 MB） | 是（结论已写入 `DP-A02`/`DP-A03` 笔记、`sota-plan.md §8.3`、`judgments.md §D`、`preparation.md` P4） |
| `/tmp/ai4r/state_bak_44.md`、`state_bak_44b.md`、`emb_state_bak_44.md`、`emb_index_bak_44.md` | 四个负向测试临时备份（第四十四轮，验证第八、九项检查与具身侧规则能报错；测完均已 `cp` 回） | 是（两个 `state.md` 与 `embodied-ai/index.md` 均已逐字回滚，`diff` 确认） |
| `/tmp/ai4r/fix_stale_sec_refs_45.py` | 修 17 处悬空章节引用的脚本（第四十五轮，逐条 `assert` 后替换链接文字与目标） | 是（已跑第五项检查确认 0 处不可达） |
| `/tmp/ai4r/fix_stale_sec_refs_45/` | 该脚本的 **6 个改写前备份**（state / repositories / world_model_code_traces / rounds-18-23 / rounds-24c / rounds-24a） | 是（改写为纯指针替换，正文零改动） |
| `/tmp/ai4r/repos_bak_45.md` | `code/repositories.md` 的负向测试临时备份（第四十五轮，验证第五项两条路径都能报错；测完已 `cp` 回） | 是（已逐字回滚） |
| `/tmp/ai4r/dpa_csv_bak_46.csv`、`dpa_md_bak_46.md` | `diffusion_planner_ad` 的 CSV 与 md 负向测试临时备份（第四十六轮，验证第十项双向都能报错；测完均已 `cp` 回） | 是（两份均已逐字回滚） |

> **`judgments_bak_36.md` 在第四十四轮被用作取证**：第四十三轮末尾那个"64 vs 65"就是靠它**逐条指纹比对**才定位到"DIVER 的 `num_cmd` 口径"那条被静默删掉。**恢复已完成并逐字校验，该备份不再需要**（它是 `judgments.md` 拆分前的重复副本，长期保留会与"单一事实源"冲突）。

```bash
rm -rf /tmp/ai4r/add_embodied_note_links.py /tmp/ai4r/emb_table.bak /tmp/ai4r/c005_bak \
       /tmp/ai4r/fix_c005_volume_refs.py /tmp/ai4r/scan_volume_refs.py /tmp/ai4r/scan_c005_volume_refs.py \
       /tmp/ai4r/unify_note_section.py /tmp/ai4r/notes_bak \
       /tmp/ai4r/judgments_bak_36.md /tmp/ai4r/split_judgments_36.py \
       /tmp/ai4r/simscale.pdf /tmp/ai4r/simscale.txt /tmp/ai4r/gtrs.pdf /tmp/ai4r/gtrs.txt \
       /tmp/ai4r/df.pdf /tmp/ai4r/df.txt /tmp/ai4r/hf_probe.txt /tmp/ai4r/hf2.txt \
       /tmp/ai4r/odl.html /tmp/ai4r/c37.txt /tmp/ai4r/final_check.txt \
       /tmp/ai4r/ddv2.pdf /tmp/ai4r/ddv2.txt \
       /tmp/ai4r/state_bak_44.md /tmp/ai4r/state_bak_44b.md \
       /tmp/ai4r/emb_state_bak_44.md /tmp/ai4r/emb_index_bak_44.md \
       /tmp/ai4r/fix_stale_sec_refs_45.py /tmp/ai4r/fix_stale_sec_refs_45 /tmp/ai4r/repos_bak_45.md \
       /tmp/ai4r/dpa_csv_bak_46.csv /tmp/ai4r/dpa_md_bak_46.md
```

（`/tmp/ai4r/` 下另有第二十八轮的 `fix_c003_volume_links.py`、`regroup_judgments.py` 等，同批可删。第三十二至三十五轮、第四十二至四十四轮只做只读核验或就地改写，**未产生新的中间产物**——第四十四轮多了四个负向测试备份，第四十五轮多了"一个修引用脚本 + 它的 6 个备份 + 一个负向测试备份"，第四十六轮多了两个负向测试备份。）

## 执行记录

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

1. 后续每轮产生的中间产物一律放 `/tmp/ai4r/`，流程中不删除；新待删项追加到「当前待清理」。
2. 收尾时只跑本表给出的命令，不改权限、不逐条确认。
3. 清理完成后把「当前待清理」清空（保留标题与说明），把过程记入「执行记录」，避免累积过期条目。
