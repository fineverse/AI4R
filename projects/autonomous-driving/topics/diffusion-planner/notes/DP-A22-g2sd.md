# DP-A22 · G2SD（反对"去噪内注入安全力"的一派）

- **原题**：Graph-Guided Safe Diffuser: Topological Graph Guidance for Safe Diffusion Planning
- **作者/载体**：Nakgyu Yang 等；arXiv [2608.09484](https://arxiv.org/abs/2608.09484) v1（2026-08-10）
- **代码**：未核验
- **证据等级**：全文（PDF + `pdftotext -layout` 逐表核对）
- **笔记日期**：2026-09-22
- **注意**：**非驾驶域**（Maze2D、Walker2D/Hopper），价值在于它与 PC-Diffuser 构成的技术路线对立。

## 摘要原文（节选）

> Many diffusion-based planners enforce safety through inference-time guidance, but such interleaved trajectory deformations often degrade kinematic feasibility due to manifold rupture. We propose Graph-Guided Safe Diffuser (G2SD), a hierarchical framework that leverages a high-level topological graph planner to guide a low-level diffusion model.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 核心主张 | 推理期引导会造成**流形破裂**（manifold rupture），破坏运动学可行性 | 摘要、§I |
| 机制 | 安全前移到**结构层**：VQ-VAE 隐图 → 节点剪枝 + 边权 W=λ_dist·c + λ_prob(−log P)（Eq.3）→ Dijkstra（Eq.4）得合规节点序列；低层扩散只生成端点锚定的**短 bridge**（不是整条轨迹） | §III–IV、Eq.3/4 |
| 理论 | Thm.3（流形破裂条件）、Lemma 5、**Thm.6（违反概率上界 P(Violation) ≤ 2M·exp(−2Mδ²/σ²H)）** | §IV |
| 主结果 | **无驾驶基准**。Maze2D SR 0.98、Safety-SPEC 0.770（Table 1）；Walker 0.497、Hopper 0.528（Table 2） | Table 1/2 |
| 成本 | Maze2D 0.99 s vs Diffuser 0.70 s、**SafeDiffuser 40.69 s**（Table 1）；locomotion 0.38 s（Table 2）；T_diff=256/20、段长 N=32/20（Table 4） | Table 1/2/4 |
| 消融 | α_usage 非单调、最佳 [0.3,0.4]（SR 97–98%，Table 3）；几何连接器（插值/spline）**不可行**（App. Table 8） | Table 3、App. Table 8 |
| 自述局限 | 仅导航/运动、不适用操作；单路径**无多样性**；bridge 不保证 100% 安全 | §VI |

## 判定（AI 判断）

**不是生成内硬约束**：安全由生成前的图剪枝（硬）+ 生成后受数据支撑的短 bridge 保证；论文本身明确反对在去噪循环内注入安全力。

## 对本项目的意义

- 它提供了"约束应该放在哪一层"的第二种答案，与 DP-A21 正面对立：
  - **PC-Diffuser（DP-A21）**：约束进去噪循环，逐路点 CBF-QP，有前向不变性证书，代价 5× 延迟。
  - **G2SD（DP-A22）**：约束不进生成，改结构（图剪枝 + 短 bridge），代价是**单路径、无多样性**，且只在小规模域验证。
- 这个对立本身就是一个可讨论的研究问题：**"约束在哪一层注入，代价与保证如何取舍"**——目前没有人把两种路线在同一基准上比较过（本轮检索未见）。

## 待核验

- 是否有官方代码。
- Thm.3 的"流形破裂"条件是否适用于高维轨迹空间（当前只在低维域验证）。
