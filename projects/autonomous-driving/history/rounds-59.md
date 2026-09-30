# 第五十九轮（2026-09-30）· 用免费 S2 官方 API 补齐之前拿不到的信息

> **轮次号说明**：本轮原按"第五十七轮"起草，但该号已被另一会话占用（[rounds-57.md](rounds-57.md) 是"按需补齐 8 张论文表"）。写入时覆盖了对方的文件，已用 `git checkout HEAD --` 完整恢复。**同一项目并行两会话是本工作空间明令禁止的**（[workspace-design.md](../../../shared/workspace-design.md) 运行纪律第 8 条），本轮踩了这条线，故改号为第五十九轮以避让。

**动因**：前几轮反复出现"引用数不可用""venue 取不到""无法定论"这类**取数能力**造成的缺口。本轮 S2 官方 API 可用（第五十八轮前完成配置，配套的 [fetch_citations.py](../../../shared/scripts/fetch_citations.py) 封装了 429 退避重试），先把**具身侧 VLA 表**的缺口一次补齐，验证"能力到位后能补多少"。

## 一、VLA 表的三个缺口：两个已补、一个确认无解

| 原缺口（表里原话） | 结果 |
|---|---|
| §4 引用数只覆盖 **7/14**，"其余 7 篇本次未查" | ✅ **补齐 14/14**，单一来源、同一日期 |
| "venue 取不到（按 T4 处理）：CogACT、GR00T N1、GR-3、SmolVLA" | ✅ **四篇都取到了**，S2 里**均为 `arXiv.org`** → **T4 判定得到确认** |
| "GR00T N1 在 Semantic Scholar 记 1342，与 OpenAlex 差两个数量级 → **无法定论**" | ✅ **悬案关闭**：S2 官方 API 记 **1390**，与 1342 一致 → **S2 数字为真，OpenAlex 的 5 是 arXiv 存根** → **原"无法定论"撤回** |

**新增字段**：`influentialCitationCount`（S2 独有，OpenAlex / Crossref / Consensus 均无）——14 篇全部取得。两处值得注意：**Diffusion Policy 877 为全表最高**；**OpenVLA 的影响力引用 522 高于 RT-2 239**，与"OpenVLA 是开源基线、被大量工作微调"的定性判断一致。

## 二、发现 S2 的 `venue` 字段本身也有可靠性问题（不能盲信）

S2 给四篇记了与既有三渠道核验**冲突**的 venue：

| 论文 | 表里（arXiv comments + OpenAlex + Crossref） | S2 |
|---|---|---|
| π0-FAST | RSS'25 / T1 | 期刊 **`Robotics`**（MDPI） |
| OpenVLA-OFT | RSS'25 / T1 | 期刊 **`Robotics`** |
| SpatialVLA | RSS'25 / T1 | 期刊 **`Robotics`** |
| DexVLA | CoRL'25 / T2 | `arXiv.org` |

三篇不同会议论文被同一个 S2 记成同一本 MDPI 期刊，**属系统性误记而非个别噪声**。→ **S2 只作第四渠道，不替代前三渠道；冲突处保留原判定并标记**。这与 [tools.md](../../../shared/tools.md) 已记的"S2 的 `publicationTypes` 全标 JournalArticle、`isOpenAccess` 误标"属同一来源。

## 三、取数成本

| 操作 | 耗时 / 成本 |
|---|---|
| 14 篇一次 batch | **1 次调用**（含 1 次 429 退避重试，3 秒后成功） |
| 费用 | **免费**（官方 API，非 Ai4Scholar 积分） |

→ **能免费拿到的，就不要用付费的 Ai4Scholar**。Ai4Scholar 保留给 S2 拿不到的部分（Google Scholar、引用网络）与 S2 反复 429 时的兜底。

## 四、产出

- [vla/papers.md](../../embodied-ai/topics/vla/papers.md)：§4 重写为 14/14，附三条解决说明与 S2 venue 警告；§3 两条缺口条目改写为"已解决"
- [vla/README.md](../../embodied-ai/topics/vla/README.md)：产出与更新时间同步

## 五、待办（同一能力可继续补的）

本表**只做了具身侧 VLA**。同样能用免费 S2 补的口径缺口还有：

1. **世界模型表**与 **DP-E 表**的引用数口径未统一
2. **E2E 综述表**（S001–S045）的引用数是 **OpenAlex 2026-09-20 快照**，且挂着"引用数不用于排序"的警告
3. 驾驶侧 **VLA 表**（28 篇）与**世界模型表**（24 篇）的引用数

→ 是否补、补哪张，等用户定；**不建议无差别全补**（引用数只是辅助判据，本工作空间的排序依据是 T 档与代码可得性）。
