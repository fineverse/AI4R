# DP-E09 · Diffusion Policy

- **原题**：Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
- **作者/载体**：Cheng Chi 等（Stanford）；arXiv [2303.04137](https://arxiv.org/abs/2303.04137) v5（2023-03-07 首发，RSS 2023 的期刊扩展版）
- **代码**：[real-stanford/diffusion_policy](https://github.com/real-stanford/diffusion_policy)（见 [code/repositories.md](../../../../autonomous-driving/code/repositories.md)）
- **证据等级**：全文（arXiv HTML 逐节提取）+ 摘要
- **笔记日期**：2026-09-22

## 摘要原文（节选）

> ...we benchmark Diffusion Policy across 12 different tasks from 4 different robot manipulation benchmarks and find that it consistently outperforms existing state-of-the-art robot learning methods with an average improvement of 46.9%.

## 关键事实（已核验）

| 项 | 内容 | 来源位置 |
|---|---|---|
| 观测 | 最近 To 步多相机 RGB 序列 + 本体状态 | §2.3、§3.2 |
| 动作空间 | **位置控制**，显著优于速度控制 | §4.2、§5.3、Fig.4 |
| 控制频率 | 真机预测 10 Hz，线性插值到 125 Hz | §6.1 |
| 扩散机制 | DDPM；起点高斯噪声 A_t^K；视觉作**条件**而非联合建模 p(A_t\|O_t) | §2.3 |
| 步数 | 训练 100 步 / 推理 10 步（DDIM）；3080 上 0.1 s；**无蒸馏** | §3.4 |
| action chunk | 预测 Tp 步、执行 Ta 步（receding horizon）；**Ta=8 最优**，存在一致性-响应性权衡 | §5.3、Fig.5 |
| 抗延迟 | 对最多 4 步延迟仍稳健 | §5.3 |
| 编码器消融 | 微调预训练视觉编码器最好、冻结最差、ViT 从头仅 22% | Table 5 |
| 数据 | Robomimic 每任务 200 PH、Kitchen 656 演示、真机 4 任务 | Table 3 |
| 结果 | 15 任务平均提升 46.9%；真机 Push-T 95%（Table 6）、Mug Flip 90%、Pour IoU 0.74 / Succ 0.79 | 摘要、Table 6、Fig.9/10 |

## 作者自述局限

- 正文无独立 Limitations 章节（未获取）；仅提 Transformer 变体对超参敏感（§3.1）。

## 对本项目的意义（AI 判断）

- **可直接对应**：多相机 → 自车环视；本体状态 → 里程计/速度；位置控制动作块 → 轨迹点序列；成功率 → 碰撞率/舒适度/进度。
- **明显不成立**：8 步 @10 Hz ≈ 0.8 s 的视野对驾驶过短；无他车意图与交互条件；接触式精密操作与车辆动力学差异大。
- **最值得借的是"设计结论"而不是模型**：位置控制优于速度控制、Ta 存在最优值、编码器必须微调、对延迟有容忍上限——这些在驾驶侧是否成立都还没有系统验证。

## 待核验

- To/Tp 的具体数值（正文截断处未获取）。
- 驾驶任务上是否有人做过同类的"Ta 扫描"实验（本轮检索未见）。
