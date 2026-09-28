# S031 · Diffusion Models for Intelligent Transportation Systems: A Survey（预印本全文）

- **原题**：Diffusion Models for Intelligent Transportation Systems: A Survey
- **作者/载体**：Mingxing Peng 等；正式版 IEEE TITS 2025（[DOI](https://doi.org/10.1109/TITS.2025.3613178)）；本笔记读的是预印本 [arXiv 2409.15816v3](https://arxiv.org/abs/2409.15816)（2025-05-08）
- **代码/论文列表**：[Pemixing/Diffusion-Models-in-ITS-A-Survey](https://github.com/Pemixing/Diffusion-Models-in-ITS-A-Survey)
- **证据等级**：全文（PDF + `pdftotext -layout`）
- **引用数**：20（OpenAlex TITS 正式版记录）
- **笔记日期**：2026-09-22

## 分类框架（全文核验）

| 章节 | 内容 |
|---|---|
| §II 基础与变体 | DDPM / DDIM / LDM / ADM / VLDM / EDM / FDM / D3PM / CARD |
| §III 挑战 vs 优势 | 挑战：数据质量、隐私、稀有事件、复杂动态、可扩展、交互；优势：高保真、可控、灵活、概率建模、多模态 |
| §IV 四个应用域 | **自动驾驶**、交通仿真、交通预测、交通安全 |
| §V 未来方向 | 五条 |

规模：正文称此前"无 ITS 领域扩散模型的综合综述"；附录 Table I 逐条汇总应用（子代理统计 >60 条）。

## 与扩散规划器直接相关的部分（§IV.A.3）

- 该节把"Planning and Decision-making"分为 Robotics 与 AVs 两支；AVs 支列出 **Diffusion-ES**（进化搜索 + 截断去噪）、**Drive-WM**、**GenAD**、**Diffusion-QL**、actor-critic 扩散。
- Table I 另列 Diffuser、Decision Diffuser、MPD 等通用决策扩散。
- **它对实时性的判断（可直接引用）**：扩散擅长不确定性与多模态建模，但 MID 在 **100 步去噪下需 17 秒**，**不可实时**；PriorNet 可把推理时间降 **2/3**（§IV.A.2、Fig.7）。

## 评价协议

- **没有统一 benchmark 协议**；Table I 逐条列各工作使用的数据集（nuPlan、nuScenes、WOMD、D4RL、PEMS 等）。
- 对本项目的含义：扩散规划器"跨工作可比性差"不是本项目的新发现，该综述（2024 年投稿）已经指出。

## 论文明确写出的未来方向（§V）

1. **LLM + 扩散**（CLIP 长文本受限）；
2. **先验知识 guidance**；
3. 去噪网络架构（U-Net → DiT/U-ViT）；
4. 大模型微调（ControlNet / T2I-Adapter）；
5. **提速**（DDIM、渐进蒸馏、一致性模型）。

## 对本项目的意义

- 这是"扩散 + 驾驶规划"最直接的上位综述，可用它证明：**实时性与统一评测在 2024 年就已被列为未解问题**，而到 2026 年（见 S032/S033）仍未解决。
- 它的"五条未来方向"里，只有"提速"在本批论文中被大幅推进（2 步截断、MeanFlow 一步），**"先验知识 guidance"与"架构选择"仍有空间**。
