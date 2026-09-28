# DP-A12 · GuideFlow（约束引导的直接竞争者）

- **原题**：GuideFlow: Constraint-Guided Flow Matching for Planning in End-to-End Autonomous Driving
- **作者/载体**：Lin Liu 等；arXiv [2511.18729](https://arxiv.org/abs/2511.18729) v3（2025-11 首发，2026-02 更新）
- **代码**：论文称 "code will be released"（**当前未见**）
- **证据等级**：全文（PDF + `pdftotext -layout`；"43.0 EPDMS / 直接施加约束"等关键句已由本线程 grep 复核）
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> ...prevailing Imitative E2E Planners often suffer from multimodal trajectory mode collapse... Meanwhile, Generative E2E Planners struggle to incorporate crucial safety and physical constraints directly into the generative process, necessitating an additional optimization stage to refine their outputs. ... Our core contribution lies in directly enforcing explicit constraints within the flow matching generation process, rather than relying on implicit constraint encoding.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 问题定位 | 生成式规划器无法把安全/物理约束直接写进生成过程，只能靠额外优化阶段修补 | 摘要、§I |
| 机制 1：CVF | 速度场向约束方向投影：v_t* = v_t − 2λ(v_t·v_t^c)/‖v_t^c‖² · v_t^c，λ=0.1，**每个积分步**作用 | Eq.14 |
| 机制 2：CF | 在 k_c=50 处把 x 替换为满足约束的 anchor（**仅推理期一次**，约束满足性由 anchor 保证） | Eq.16 |
| 机制 3：RFE | 能量项 E_θ=‖ȷ(f(x_t))−ȷ(x_t)‖²，L_RFE=E_θ(x(1))−E_θ(x_1)，**训练期** | Eq.17–18 |
| 采样预算 | K=100 步、k_c=50 | Eq.15–16 |
| 主结果 | Navhard **EPDMS 43.0（SOTA，+1.3）**；no-scorer 变体 27.1（Table 1） | Table 1 |
| 其他基准 | nuScenes CR 0.07%、ADV-NuS 0.73%（Table 3） | Table 3 |
| 与 DiffusionDrive 对比 | **有直接对比**：Table 1 记 DiffusionDrive 24.2（navhard）；Table 3 记 ADV 1.67 | Table 1/3、Fig.4 |
| 推理成本 | **FPS 3.6**（RTX4090）；同表 SparseDrive 9.0 | Table 3 |
| 消融 | Table 5：CF 单独 +1.6 EPDMS / +0.45% SR；CVF+CF+RFE 27.1 vs 23.1。Table 6：λ 0.1→0.5 时 EPDMS 24.5→13.5；k_c 10→50→100 为 24.2→27.1→25.0 | Table 5/6 |
| 理论 | 无编号定理（Eq.14 称 proof 在附录，正文 PDF 未见附录） | — |
| 自述局限 | **加速采样损害性能** | §V |

## 判定（AI 判断）

**生成内软引导，不是硬约束**：CVF 是加性投影项、RFE 是能量正则、CF 是单次 anchor 截断，三者都没有 QP 求解或可行性证书。与 DP-A21（PC-Diffuser，逐去噪步 CBF-QP + Thm.1/Cor.1）在严格程度上差一档。

## 对本项目的意义

- 它占了"约束引导 + navhard"这个位置，且拿到 43.0 的 SOTA——若本项目走"引导式约束"，必须与它正面比较。
- 但它留下两个明显缺口：**3.6 FPS（远低于实时）**、**无形式化保证**。
- 与 DP-A16（DIVER navhard Stage2 43.4）、DP-A31（DriveFuture 55.5）对照可知：navhard 上 43 分区间已经拥挤。**⚠ 更正**：此前写"55 分只有 DriveFuture 达到（且靠条件输入而非约束）"**归因有误**——**55.5 含 GTRS-Dense scorer**，其不含 scorer 的受控消融只有 34.6（未来条件 +3.7）。→ **不能据此说"条件比约束有效"**。

## 待核验

- 代码是否已发布（论文承诺但当前未见）。
- Eq.14 的证明（附录在 arXiv HTML 版本中可能存在，PDF 正文未见）。
