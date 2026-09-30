# VLA（具身侧）论文表

更新时间：2026-09-30  
检索范围：2023–2026，按 [literature-quality.md](../../../../shared/literature-quality.md) 分档后收录 **14 篇**。  
证据状态：**全部为摘要级**（arXiv 摘要 + `comments` 元数据 + OpenAlex/Crossref 的 venue 记录 + 官方 README；**未读正文**）。工作空间另有 **π0 / π0.5 的全文级笔记**（[DP-E19](../diffusion-policy/notes/DP-E19-pi0.md)），以及 DP-E14 FLOWER、DP-E20 π0.5、DP-E21 RDT-1B、DP-E22 GR00T N1 的摘要级条目。  
**质量依据**：T 档含义见 [literature-quality.md](../../../../shared/literature-quality.md) §4；venue 三渠道并行核验（arXiv `comments` / OpenAlex 按标题 / Crossref 按 DOI）。引用数原按 OpenAlex「标题」查得、**多数命中 arXiv 存根、系统性低估**（**不用于排序**）；**2026-09-30 起 §4 改用 S2 官方口径（覆盖 14/14）**，两个口径**不可混用**。逐行证据等级与代码状态见 §1.1。  
相关：[lineage.md](lineage.md)、[大方向脉络](../../direction/lineage.md)

## 1. 代表工作

| 编号 | 论文 | arXiv | 年 | venue / T 档 | 动作输出 | 是否生成式（哪一类） | 基座 | benchmark | 控制频率 / 延迟 | 官方代码 |
|---|---|---|---|---|---|---|---|---|---|---|
| E-VLA-01 | **RT-2** | `2307.15818` | 2023 | CoRL'23 / T1 | **离散 token**（动作 = 文本） | 自回归离散 token | PaLI-X 55B | 真机 Google Robot，100+ 任务 | 330–1000 ms（**<3 Hz**，二手） | 无（闭源） |
| E-VLA-02 | **OpenVLA** | `2406.09246` | 2024 | CoRL'24 / T1 | **离散 token**（每维 256 bin） | 自回归离散 token | Prismatic（DINOv2 + SigLIP + Llama2-7B） | LIBERO / SimplerEnv / 真机 | **3–5 Hz**（A100） | [openvla/openvla](https://github.com/openvla/openvla) + HF 权重 |
| E-VLA-03 | **π0-FAST** | `2501.09747` | 2025 | RSS'25 / T1 | **离散 token**（DCT 压缩） | 自回归离散 token | PaliGemma | 真机高频灵巧、DROID | 约 750 ms/chunk | openpi + 权重 |
| E-VLA-04 | **ACT** | `2304.13705` | 2023 | RSS'23 / T1 | **动作块**（一次 k 步） | **非生成式**（CVAE + 回归） | 无 VLM | ALOHA 真机双臂 6 任务 | **50 Hz** | [tonyzhaozh/act](https://github.com/tonyzhaozh/act)（无权重） |
| E-VLA-05 | **OpenVLA-OFT** | `2502.19645` | 2025 | RSS'25 / T1 | **动作块 + 连续回归（L1）+ 并行解码** | **非生成式**（回归） | OpenVLA 7B | LIBERO **97.1%**、ALOHA 真机 | 吞吐 **26×**（OFT+ 43×），延迟 1/3 | [moojink/openvla-oft](https://github.com/moojink/openvla-oft) + HF |
| E-VLA-06 | **Diffusion Policy** | `2303.04137` | 2023 | RSS'23 + IJRR'24 / T1 | **连续动作块** | **扩散**（DDPM / DDIM） | 无 VLM | 4 基准 12 任务、真机 | 真机 **10 Hz**（插值 125 Hz） | [real-stanford/diffusion_policy](https://github.com/real-stanford/diffusion_policy) |
| E-VLA-07 | **Octo** | `2405.12213` | 2024 | RSS'24 / T1 | 连续动作块 | **扩散**（动作头） | 自建 Transformer（27M / 93M） | OXE 800k、WidowX 真机 | 20–30 Hz（二手） | [octo-models/octo](https://github.com/octo-models/octo) + HF |
| E-VLA-08 | **CogACT** | `2411.19650` | 2024 | 仅 arXiv / **T4** | 连续动作块 | **扩散**（DiT 动作头，组件化） | CogVLM + DiT 模块 | LIBERO / SimplerEnv | 未取得 | [microsoft/CogACT](https://github.com/microsoft/CogACT) + HF |
| E-VLA-09 | **SpatialVLA** | `2501.15830` | 2025 | RSS'25 / T1 | 连续动作块（自适应动作网格） | **回归**（非扩散 / 流匹配） | PaliGemma | SimplerEnv / LIBERO / WidowX | 未取得 | [SpatialVLA/SpatialVLA](https://github.com/SpatialVLA/SpatialVLA) + HF |
| E-VLA-10 | **DexVLA** | `2502.05855` | 2025 | CoRL'25 / T2 | 连续动作块 | **扩散**（1B 扩散专家） | VLM + 扩散专家 | 真机跨本体长时程 | 未取得 | [juruobenruo/DexVLA](https://github.com/juruobenruo/DexVLA) |
| E-VLA-11 | **SmolVLA** | `2506.01844` | 2025 | 仅 arXiv / **T4** | 连续动作块 | **flow matching** | SmolVLM2（210M） | LIBERO / SimplerEnv / SO-100 真机 | 边缘 **140–260 ms**（二手） | [huggingface/lerobot](https://github.com/huggingface/lerobot) + HF |
| E-VLA-12 | **RT-H** | `2403.01823` | 2024 | RSS'24 / T1 | **分层**：语言运动 → 动作块 | **非生成式**（分层回归） | 无 VLM | 真机多任务 | 未取得 | **未找到** |
| E-VLA-13 | **GR00T N1** | `2503.14734` | 2025 | 仅 arXiv（tech report）/ **T4** | 连续动作块 | **扩散**（DiT） | NVIDIA-Eagle + SmolLM-1.7B | 仿真 + GR-1 / 1X Neo 真机 | System 1 最高 **120 Hz**；16 步 chunk **63.9 ms**（L40） | [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) + HF |
| E-VLA-14 | **GR-3** | `2507.15493` | 2025 | 仅 arXiv（tech report）/ **T4** | 连续动作块 | **flow matching**（MoT + DiT） | 自建 4B MoT VLA | 真机 ByteMini（餐桌整理 / 挂衣） | 未取得 | **无公开代码 / 权重** |

**未入表但质量可**：TinyVLA（`2409.12514`，RA-L 2025，扩散解码器）、InternVLA-M1（`2510.13778`，技术报告）、RoboMamba（`2406.04339`，NeurIPS'24）。

## 1.1 逐行证据等级与代码状态（2026-09-30 补，供跨表检索）

> 证据等级定义见 [rules.md](../../../../ai/rules.md) §证据等级；代码状态取自本表「官方代码」列与 §3，**未新查**（体例同驾驶侧 [vla/papers.md §1.1](../../../autonomous-driving/topics/vla/papers.md)）。
> **本表 14 篇全部为摘要级**（未读正文，见 §3）。

| 编号 | 证据等级 | 代码状态 |
|---|---|---|
| E-VLA-01 RT-2 | 摘要级 | 无代码（闭源） |
| E-VLA-02 OpenVLA | 摘要级 | **有代码 + 权重** |
| E-VLA-03 π0-FAST | 摘要级 | **有代码 + 权重**（openpi） |
| E-VLA-04 ACT | 摘要级 | 有代码（**无权重**） |
| E-VLA-05 OpenVLA-OFT | 摘要级 | **有代码 + 权重** |
| E-VLA-06 Diffusion Policy | 摘要级 | **有代码** |
| E-VLA-07 Octo | 摘要级 | **有代码 + 权重** |
| E-VLA-08 CogACT | 摘要级 | **有代码 + 权重** |
| E-VLA-09 SpatialVLA | 摘要级 | **有代码 + 权重** |
| E-VLA-10 DexVLA | 摘要级 | 有代码（未记权重） |
| E-VLA-11 SmolVLA | 摘要级 | **有代码 + 权重**（lerobot） |
| E-VLA-12 RT-H | 摘要级 | **未找到** |
| E-VLA-13 GR00T N1 | 摘要级 | **有代码 + 权重** |
| E-VLA-14 GR-3 | 摘要级 | **无公开代码 / 权重** |

**小结**：**11/14 有官方代码**，其中 **8 篇同时有可下载权重**；无代码 2 篇（RT-2 闭源、GR-3）＋「未找到」1 篇（RT-H）。**但全部为摘要级** → **代码状态是自述未验证**（本工作空间的代码核验只覆盖驾驶侧）。引用数见 §4（S2 口径）。

## 2. 三个结论

1. **"动作 token → 动作块 → 连续动作头"这个顺序在 VLA 血统里成立，在整个具身侧不成立**——**动作块（ACT）与生成式连续头（Diffusion Policy）同在 2023 年出现**；VLA 血统**滞后一年**（RT-2 / OpenVLA 仍是离散 token + 单步自回归）。**转折点是 π0（RSS'25）与 OpenVLA-OFT（RSS'25）**：OFT 原文即把"AR 单步"列为瓶颈（"3-5 Hz … too slow for 25-50+ Hz"）。
2. **生成式动作头在这批里占 50%**（14 篇中 7 篇）：**扩散 5 篇**（Diffusion Policy、Octo、CogACT、DexVLA、GR00T N1）+ **流匹配 2 篇**（SmolVLA、GR-3）；并入工作空间已有的 π0 / FLOWER（流匹配）与 RDT-1B（扩散）→ **flow matching 4 篇、diffusion 6 篇**。**π0 之外用流匹配的还有 FLOWER、SmolVLA、GR-3，均晚于 π0** → **flow matching 是 π0 之后的新增量**，diffusion 主要来自 2023–2024 的**非 VLA 血统**。注意 **SpatialVLA 是"连续动作"但用自适应网格回归，不算生成式**。
3. **控制频率跨两个数量级（~1 Hz 到 ~120 Hz），但真实推理频率普遍在 5–15 Hz**：自回归大模型最低（RT-2 <3 Hz、OpenVLA 3–5 Hz）、连续头 / 轻量模型居中（Diffusion Policy 10–20 Hz、Octo 20–30 Hz）、分块 + 专用头最高（ACT 50 Hz、GR00T N1 System 1 120 Hz）。**⚠ 陷阱：π0 的"50 Hz"是执行 chunk 的控制频率，不是模型前向频率**（20 Hz 重规划时执行 16/50 步）。

## 3. 证据边界与不确定项

- **全部摘要级**：本表 14 篇**均未读正文**；频率数字除 π0（50 Hz）、OpenVLA（3–5 Hz，OFT 正文引）、OFT（26×）、FAST（750 ms）外，**多为二手来源**（博客 / 聚合站）。
- **venue**：CogACT、GR00T N1、GR-3、SmolVLA 四篇原记"取不到（按 T4 处理）"，**2026-09-30 经 S2 补到，均为 `arXiv.org`** → **T4 判定得到确认**；但 S2 的 `venue` 本身也有误记（π0-FAST / OpenVLA-OFT / SpatialVLA 被记成期刊 `Robotics`），**只作第四渠道**，详见 §4 第 3 条。
- **引用数两个口径不可混用**：OpenAlex 侧 OpenVLA 43、RT-2 273、GR00T N1 5 等均为 **arXiv 存根**（系统性低估）；而 S2 侧同一篇 GR00T N1 记 **1390** → **S2 数字为真，原"无法定论"已撤回**（见 §4）。**两个口径不可直接比较，也不用于排序**。
- **频率冲突**：GR00T N1 System 1 有 **120 Hz**（NVIDIA 博客）与 30 Hz（他源）两说。
- **未找到官方代码**：RT-H、GR-3。
- **候选名不存在**：arXiv 全库无独立 "RoboVLM"（疑指 RoboMamba）；"GR00T N1.5" 无 arXiv（仅模型卡更新）。

## 4. 引用数（Semantic Scholar 口径）

**覆盖 14/14**（此前只覆盖 7 篇）。2026-09-30 经 S2 官方 API 一次 batch 取得，**单一来源、同一日期**，工具见 [fetch_citations.py](../../../../shared/scripts/fetch_citations.py)。

| 编号 | 论文 | S2 引用数 | 影响力引用数 |
|---|---|---|---|
| E-VLA-01 | RT-2 | 4407 | 239 |
| E-VLA-02 | OpenVLA | 3597 | 522 |
| E-VLA-03 | π0-FAST | 695 | 102 |
| E-VLA-04 | ACT | 2482 | 388 |
| E-VLA-05 | OpenVLA-OFT | 936 | 190 |
| E-VLA-06 | Diffusion Policy | 4410 | **877** |
| E-VLA-07 | Octo | 1925 | 139 |
| E-VLA-08 | CogACT | 462 | 54 |
| E-VLA-09 | SpatialVLA | 567 | 62 |
| E-VLA-10 | DexVLA | 238 | 9 |
| E-VLA-11 | SmolVLA | 573 | 101 |
| E-VLA-12 | RT-H | 253 | 14 |
| E-VLA-13 | GR00T N1 | 1390 | 208 |
| E-VLA-14 | GR-3 | 118 | 3 |

- **`influentialCitationCount` 为 S2 独有字段**（OpenAlex / Crossref / Consensus 均无），可作"实际影响力"的补充判据。两处值得注意：**Diffusion Policy 877 为全表最高**；**OpenVLA 的影响力引用（522）高于 RT-2（239）**，与"OpenVLA 是开源基线、被大量工作微调"的定性判断一致
- **口径警告**：S2 数为全版本合并（含预印本引用），与 OpenAlex 正式版记录可差一到两个数量级 → **两个口径不可混用、不可直接比较**
- **取数日期**：引用数随时间变化（同一篇 RT-2，09-29 记 4352、09-30 记 4407）→ 引用类数字必须标注日期

**本轮解决的遗留问题**：

1. **GR00T N1 的引用数悬案关闭**：§3 原记"OpenAlex 5 vs Semantic Scholar 1342，差两个数量级 → **无法定论**"。现在 S2 官方 API 记 **1390**，与之前的 1342 一致 → **S2 的数字是真实的，OpenAlex 的 5 是 arXiv 存根记录**（该模式本表已多处记录）。**"无法定论"可撤回**
2. **四篇"venue 取不到"的补上了**：CogACT / SmolVLA / GR00T N1 / GR-3 在 S2 里**均为 `arXiv.org`** → **与表里 T4 的判定一致**，该分档得到第四个渠道确认
3. ⚠ **但 S2 的 `venue` 字段本身也有可靠性问题，不能盲信**：π0-FAST / OpenVLA-OFT / SpatialVLA 三篇在 S2 里被记成期刊 **`Robotics`**（MDPI），而表里依 arXiv `comments` + OpenAlex + Crossref 记的是 RSS'25 / RSS'25 / RSS'25；DexVLA 在 S2 记 `arXiv.org`，而表里记 **CoRL'25 / T2**。→ **S2 只作第四渠道，不替代前三渠道；冲突处保留原判定并标记**
