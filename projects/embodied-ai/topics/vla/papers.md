# VLA（具身侧）论文表

更新时间：2026-09-23  
检索范围：2023–2026，按 [literature-quality.md](../../../../shared/literature-quality.md) 分档后收录 **14 篇**。  
证据状态：**全部为摘要级**（arXiv 摘要 + `comments` 元数据 + OpenAlex/Crossref 的 venue 记录 + 官方 README；**未读正文**）。工作空间另有 **π0 / π0.5 的全文级笔记**（[DP-E19](../diffusion-policy/notes/DP-E19-pi0.md)），以及 DP-E14 FLOWER、DP-E20 π0.5、DP-E21 RDT-1B、DP-E22 GR00T N1 的摘要级条目。  
**质量依据**：T 档含义见 [literature-quality.md](../../../../shared/literature-quality.md) §4；venue 三渠道并行核验（arXiv `comments` / OpenAlex 按标题 / Crossref 按 DOI）。**引用数按 OpenAlex「标题」查得，多数命中 arXiv 存根、系统性低估**，故**不用于排序**。  
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

## 2. 三个结论

1. **"动作 token → 动作块 → 连续动作头"这个顺序在 VLA 血统里成立，在整个具身侧不成立**——**动作块（ACT）与生成式连续头（Diffusion Policy）同在 2023 年出现**；VLA 血统**滞后一年**（RT-2 / OpenVLA 仍是离散 token + 单步自回归）。**转折点是 π0（RSS'25）与 OpenVLA-OFT（RSS'25）**：OFT 原文即把"AR 单步"列为瓶颈（"3-5 Hz … too slow for 25-50+ Hz"）。
2. **生成式动作头在这批里占 50%**（14 篇中 7 篇）：**扩散 5 篇**（Diffusion Policy、Octo、CogACT、DexVLA、GR00T N1）+ **流匹配 2 篇**（SmolVLA、GR-3）；并入工作空间已有的 π0 / FLOWER（流匹配）与 RDT-1B（扩散）→ **flow matching 4 篇、diffusion 6 篇**。**π0 之外用流匹配的还有 FLOWER、SmolVLA、GR-3，均晚于 π0** → **flow matching 是 π0 之后的新增量**，diffusion 主要来自 2023–2024 的**非 VLA 血统**。注意 **SpatialVLA 是"连续动作"但用自适应网格回归，不算生成式**。
3. **控制频率跨两个数量级（~1 Hz 到 ~120 Hz），但真实推理频率普遍在 5–15 Hz**：自回归大模型最低（RT-2 <3 Hz、OpenVLA 3–5 Hz）、连续头 / 轻量模型居中（Diffusion Policy 10–20 Hz、Octo 20–30 Hz）、分块 + 专用头最高（ACT 50 Hz、GR00T N1 System 1 120 Hz）。**⚠ 陷阱：π0 的"50 Hz"是执行 chunk 的控制频率，不是模型前向频率**（20 Hz 重规划时执行 16/50 步）。

## 3. 证据边界与不确定项

- **全部摘要级**：本表 14 篇**均未读正文**；频率数字除 π0（50 Hz）、OpenVLA（3–5 Hz，OFT 正文引）、OFT（26×）、FAST（750 ms）外，**多为二手来源**（博客 / 聚合站）。
- **venue 取不到**（按 T4 处理）：CogACT、GR00T N1、GR-3、SmolVLA。
- **引用数不可用**：OpenVLA 43、RT-2 273、GR00T N1 5 等均为 **arXiv 存根**；**GR00T N1 在 Semantic Scholar 记 1342，与 OpenAlex 差两个数量级** → 无法定论。
- **频率冲突**：GR00T N1 System 1 有 **120 Hz**（NVIDIA 博客）与 30 Hz（他源）两说。
- **未找到官方代码**：RT-H、GR-3。
- **候选名不存在**：arXiv 全库无独立 "RoboVLM"（疑指 RoboMamba）；"GR00T N1.5" 无 arXiv（仅模型卡更新）。
