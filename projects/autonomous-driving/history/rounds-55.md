# 第五十五轮（2026-09-29）· 网络排查与论文检索工具的固化

**性质**：非专题研究轮——不改任何研究方向与结论，修的是**取数能力**（"能不能访问"与"用什么工具取"）。

## 一、GitHub 访问：根因是代理的 fake-ip，不是网络不通

排查链条（全部有实测）：

1. `github.com` 秒级 `连接被拒绝`，而 `api.github.com`、`codeload.github.com` 正常 → 只有它一个域名坏
2. **根因**：Clash Verge 的 `enhanced-mode: fake-ip` 把 `github.com` 解析成 **`198.18.0.1`——正是 TUN 网卡自身的地址**，连它等于连本地网卡（443 无监听）→ 秒拒。`api` / `codeload` 拿到真实 IP 所以正常
3. 用户**开 TUN 无效**（假 IP 依旧），**关 TUN 也无效**（DNS 分配已缓存）
4. **解法**：改用**「系统代理」+ 显式环境变量**，走 `127.0.0.1:7897`（Clash Verge 的 mixed-port——其"系统代理"只改 GNOME 设置，**不导出到 shell**）

**实测结果**（走 7897）：`github.com` 200、**真实 `git clone` 成功（198 文件 / 16 MB）**、`git ls-remote` 成功、`codeload` 2.97 MB/s。

**顺带纠正两处旧记录**：
- 第二十四轮记的"Flow Planner 在约 4.5 MB 处稳定截断"——**不是截断，是 `github.com` 压根没连上**
- 沙箱与外网的差异：沙箱内 `codeload` 仅 80 KB/s，沙箱外 3.97 MB/s（**差 46 倍**）→ 大文件下载应走非沙箱

**不依赖 `github.com` 的绕行**（已验证）：`curl -L https://api.github.com/repos/{owner}/{repo}/tarball/{ref}` → 302 到 codeload，2.3 MB/s。

**GitHub token**：fine-grained（`Contents: Read-only` + 自动的 `Metadata: Read-only`，账户权限全留空）可用。**同时更正一条误判**——此前"token 缺 Metadata 权限、`/repos/*` 稳定 500、必须换 classic"是**错的**：同一 token 复查为 **5/5 全 200**，当时的 500 是 GitHub 侧瞬时故障或权限传播延迟。

## 二、`huggingface.co` 阻塞解除（关闭待续清单第 17 项的网络部分）

- **直连 `http 000`、走代理 `200`**（与第三十八轮的 `000` 相比，差异在代理）
- **文件下载实测成功**：`bert-base-uncased/resolve/main/config.json` → 200 / 570 字节
- **更正一处路径**：官方排行榜是 **Space**（`spaces/AGC2025/e2e-driving-navhard`，200 可达），不是 dataset（`datasets/...` 返回 401）——旧记录写成 dataset
- **待下一轮核**：SimScale / GTRS 的 checkpoint 仓库 ID。按 `OpenDriveLab/SimScale`、`OpenDriveLab/GTRS` 查询均返回 401，且 `OpenDriveLab` 组织下**没有**这两个模型 → **仓库名需重新确认，不能沿用当前记录**

## 三、论文检索工具：盘清四个工具的真实能力，并固化成本纪律

**Semantic Scholar 官方 API——未认证不可用，成因已查明**：429 是**全局共享池饱和**（非本地配额），**等待无效**。实测：隔 15 秒重试 3 次全 429；单条 GET 连续 7 次仅 1 次穿透。唯一解法是[申请免费 key](https://www.semanticscholar.org/product/api)（1 req/s 独占）。

**Consensus**：**MCP 通道不可用**（返回类型不兼容，2026-09-20 起），但 **REST API 可用**（`x-api-key`；固定 20 条/次；Free 档 30 次/月）。其 `sjr_best_quartile` / `is_preprint` / `study_type` 三个字段**可信**，直接对应文献质量分档的 T1–T5 判据。

**Ai4Scholar**（用户付费）：是 S2 / PubMed / Google Scholar / arXiv 的**转售代理**，价值在自带高配 key、把 S2 的 429 变成稳定服务。
- 调用规范：Base `https://ai4scholar.net/graph/v1`、认证 `Authorization: Bearer`（**不是** `x-api-key`）
- **免费端点** `GET /api/credits` 查余额；计费响应带 `x-credits-charged` / `x-credits-remaining`；**失败不扣费**
- 实测成本：`paper/batch` 查 7 篇 = **2 积分**；本轮结束余额 **487**
- **数据质量坑（本轮实测）**：`publicationTypes` **全标 `JournalArticle`**（含 CoRL / RSS 会议论文）→ 不可信；`isOpenAccess` **有误**（OpenVLA / Octo 标"否"）→ 不可信。**判会议/期刊只看 `venue`，判预印本用 `venue == 'arXiv.org'`**

**产出**：新建 [shared/tools.md](../../../shared/tools.md)（工具与凭据的调用方式 / 额度 / 成本 / 坑）；[shared/index.md](../../../shared/index.md) 由 58 行收敛为 **36 行**（只留速查表 + 指针，遵守"index 只做导航"）；凭据入 [shared/tools.env](../../../shared/tools.env)（**已 gitignore，未进版本历史**）。

## 四、具身侧：VLA 表补引用数

VLA 表 §3 原记"**引用数不可用**"（OpenAlex 命中 arXiv 存根、系统性低估，如 OpenVLA 仅 43）。本轮用 Ai4Scholar 取到 **7 篇的 S2 口径**（[papers.md §4](../../../projects/embodied-ai/topics/vla/papers.md)）：RT-2 4352 / OpenVLA 3527 / π0-FAST 679 / ACT 2447 / OFT 913 / Octo 1897 / CogACT 452，并附**影响力引用数**（`influentialCitationCount`，S2 独有字段）。

§3 那条改为"**两个口径不可混用**"——S2 数含预印本引用、与 OpenAlex 正式版记录可差一到两个数量级（GR00T N1 的 1342 vs 5），**不可直接比较、也不用于排序**。

## 五、发现的既有失真（本轮未修，仅记录）

**README 与 `state.md` 的"当前态"停在第四十八轮，而 `rounds-49` 至 `rounds-54` 六个轮次文件均已存在**：
- README「最近动态」写"最新一轮：第四十八轮"，同节另一处写"第五十一轮"——**自相矛盾**
- `state.md`「当前阶段」写"文献调研已完成**四十八轮**"，正文段落止于第四十八轮

轮次收尾第 1 条要求"细节写进 `rounds-NN.md`"，第 2/3 条要求 `state.md` 与 README 同步——**第 49 至 54 轮的收尾漏了第 2/3 条**。本轮只补第 55 轮，**未回头补写 49–54 轮的摘要**（那需要先读那 6 个文件，属下一轮的事）。

## 六、清理

[inbox/cleanup.md](../../../inbox/cleanup.md) 登记 **20 条目 / 约 16 MB**（全在 `/tmp`，含 16 MB 的 navsim 重复克隆副本）。**本轮违反第四十八轮约定**（临时根应为 `inbox/scratch/`）——因本次为跨会话长任务、前段沿用旧习惯，已在清单中就地标注。
