# 自动驾驶端到端模型综述（2024–2026）

更新时间：2026-09-20  
检索对象：以端到端自动驾驶（E2E-AD）为核心，补充直接影响 E2E 研究设计的规划、扩散模型、世界模型、VLM/VLA、数据集、仿真和评测综述。  
本表不是“已经穷尽所有综述”的证明，而是截至查询日从 arXiv、OpenAlex、Crossref、出版社页面和可访问全文中检索、去重、核验后的工作清单。

## 纳入与证据规则

- **A：直接 E2E 综述**：标题或主要分类直接围绕端到端驾驶；包括全栈 E2E、规划导向 E2E、E2E 训练、E2E 后训练和 E2E 扩散模型。
- **B：广义自动驾驶综述**：覆盖多个自动驾驶模块，但对 E2E、深度学习或系统架构有明确章节。
- **C：专题补充**：数据集、仿真、评测、规划、世界模型、VLM/VLA、轨迹预测或扩散模型；不等于完整 E2E 综述。
- **D：低优先级/待全文核验**：主题相关但范围较宽、会议/技术报告证据较少，或正式出版信息仍需复核。

证据状态只表示本次检索实际做到的程度：`元数据`（DOI/OpenAlex/Crossref）、`摘要`（出版社/arXiv 摘要）、`全文目录`（可访问 HTML 的章节目录）、`项目页`（摘要或页面明确给出的仓库）。公开代码/项目页不代表本文已被独立复现。**本表用的是"综述专用"的窄词表；通用证据等级（含代码核验 L1/L2/L3）的定义见 [ai/rules.md](../../../../ai/rules.md) §证据等级。**

引用数为 OpenAlex 快照（查询日 2026-09-20），不同索引会不同；`0` 表示当前 OpenAlex 未返回引用，不表示没有引用。

## 2024

| ID | 级别 | 综述（原题） | 作者（首位/等） | 载体、正式年与链接 | 核心范围与分类框架 | 数据/评测/工程资产 | 引用数；证据与用途 |
|---|---|---|---|---|---|---|---|
| S001 | A | [End-to-End Autonomous Driving: Challenges and Frontiers](https://doi.org/10.1109/TPAMI.2024.3435937)（[arXiv 2306.16927v3](https://arxiv.org/abs/2306.16927)） | Li Chen et al. | IEEE TPAMI，2024 | 270+ 篇；从 raw sensor 到 motion plan；多模态、可解释性、因果混淆、鲁棒性、world/foundation models、视觉预训练 | 摘要提到大规模数据和闭环评测；[OpenDriveLab 目录](https://github.com/OpenDriveLab/End-to-end-Autonomous-Driving) | 569；OpenAlex+arXiv 摘要+项目页。最适合作为总览主线 |
| S002 | A | [Recent Advancements in End-to-End Autonomous Driving Using Deep Learning: A Survey](https://doi.org/10.1109/TIV.2023.3318070)（[arXiv 2307.04370](https://arxiv.org/abs/2307.04370)） | Pranav Singh Chib、Pravendra Singh | IEEE TIV，正式卷期 2024；DOI 前缀为 2023 | 传感器输入、主/辅助输出、IL 到 RL、评价、可解释性与安全 | 作者维护的[开源实现/文献目录](https://github.com/Pranav-chib/Recent-Advancements-in-End-to-End-Autonomous-Driving-using-Deep-Learning) | 294；**2026-09-22 已读 arXiv 全文（v2）**，历史路线图、CARLA 指标（RC/IS/DS=RC×IS）与开放问题见 [S002 笔记](../notes/S002-e2e-ad-survey.md)。注意 arXiv 首发为 2023，正式出版按 2024 计 |
| S003 | A | [End-to-End Autonomous Driving in CARLA: A Survey](https://doi.org/10.1109/ACCESS.2024.3473611) | Youssef Al Ozaibi et al. | IEEE Access，2024 | 专门整理 CARLA 中 E2E 的输入、输出、网络架构与训练范式 | CARLA；论文称有大型汇总表和方法评测；未在摘要中核验独立代码仓库 | 13；OpenAlex+出版社摘要。适合仿真和公平比较入口 |
| S004 | C | [Vision Language Models in Autonomous Driving: A Survey and Outlook](https://doi.org/10.1109/TIV.2024.3402136)（[arXiv 2310.14414](https://arxiv.org/abs/2310.14414)） | Xingcheng Zhou et al. | IEEE TIV，2024 | VLM 在感知理解、导航规划、决策控制、E2E 与数据生成中的任务和指标 | 语言增强数据集与常用指标；[Awesome-VLM-AD-ITS](https://github.com/ge25nab/Awesome-VLM-AD-ITS) | 122；摘要+项目页。VLM/E2E 交叉入口 |
| S005 | C | [A Survey on Multimodal Large Language Models for Autonomous Driving](https://doi.org/10.1109/WACVW60836.2024.00106) | Can Cui et al. | WACV Workshop，2024 | MLLM/VFM 的发展、驾驶任务、数据集与 benchmark；偏 VLM/MLLM，不是纯 E2E | 摘要明确提到数据集和 benchmark；未核验统一代码仓库 | 316；OpenAlex+会议摘要。引用较高但需注意 workshop 定位 |
| S006 | C | [World Models for Autonomous Driving: An Initial Survey](https://doi.org/10.1109/TIV.2024.3398357)（[arXiv 2403.02622](https://arxiv.org/abs/2403.02622)） | Yanchen Guan et al. | IEEE TIV，2024 | world model 的理论基础、感知/记忆/动作模块和驾驶应用 | 面向未来事件预测与决策；具体 benchmark 需全文核验 | 73；摘要+元数据。适合闭环、反事实和生成式规划背景 |
| S007 | C | [A Survey for Foundation Models in Autonomous Driving](https://arxiv.org/abs/2402.01105) | Haoxiang Gao et al. | arXiv 预印本，2024 | 40+ 篇；按模态与功能整理 LLM、VLM、规划、仿真、3D 感知和数据生成 | 摘要涉及 planning/simulation；未核验正式期刊版本 | 7；arXiv 摘要+OpenAlex。作为基础模型补充，不替代 E2E 主综述 |
| S008 | C | [Large Language Models for Human-like Autonomous Driving: A Survey](https://doi.org/10.1109/ITSC58415.2024.10919629)（[arXiv 2407.19280](https://arxiv.org/abs/2407.19280)） | Yun Li et al. | IEEE ITSC，正式记录 2024 | 从规则/优化/深度 RL 到 LLM；讨论模块化与 E2E、实时性、安全、部署成本 | 未在摘要中给出统一 benchmark/代码 | 20；摘要+元数据。适合 LLM 驱动驾驶背景 |
| S009 | C | [A Survey on Autonomous Driving Datasets: Statistics, Annotation Quality, and a Future Outlook](https://doi.org/10.1109/TIV.2024.3394735) | Mingyu Liu et al. | IEEE TIV，2024 | 265 个数据集；传感器、规模、任务、上下文、地理/对抗环境和标注质量 | 数据集选择、监督信息和标注质量；未等同于 E2E benchmark | 97；摘要+元数据。直接对应“数据是否支持创新”问题 |
| S010 | C | [Virtual Tools for Testing Autonomous Driving: A Survey and Benchmark of Simulators, Datasets, and Competitions](https://doi.org/10.3390/electronics13173486) | Tantan Zhang et al. | Electronics，2024 | 22 个主流 simulator、35 个开源数据集、10 个竞赛；比较可访问性、物理/渲染引擎 | 仿真器、数据集、竞赛的选型信息 | 40；摘要+元数据。适合平台与评测协议筛选 |
| S011 | C | [A survey of autonomous driving frameworks and simulators](https://doi.org/10.1016/j.aei.2024.102850) | Hui Zhao et al. | Advanced Engineering Informatics，2024 | 开源/商业框架和 simulator 的功能、算法、硬件、场景生成、V2X、共仿真 | 仿真框架与工程约束；具体 E2E 模型需全文核对 | 24；摘要+元数据。适合跨平台适配 |
| S012 | C | [Survey on Simulation Testing of Autonomous Driving System](https://doi.org/10.1109/DSA63982.2024.00038) | Chunyan Xia et al. | DSA conference，2024 | 仿真测试技术与测试用例生成 | 测试生成、复杂系统验证；摘要信息较短 | 2；会议摘要+元数据。仿真测试补充，优先级低于 S010/S011 |
| S013 | C | [A Survey on Recent Advancements in Autonomous Driving Using Deep Reinforcement Learning](https://doi.org/10.1109/TITS.2024.3452480) | Rui Zhao et al. | IEEE TITS，2024 | 六类系统集成模式；状态/动作/奖励空间、网络、训练、验证 | 覆盖 full-stack 与策略学习，未专门限定 E2E | 93；摘要+元数据。适合 RL 后训练和闭环目标 |
| S014 | C | [Recent advances in reinforcement learning-based autonomous driving behavior planning: A survey](https://doi.org/10.1016/j.trc.2024.104654) | Jingda Wu et al. | Transportation Research Part C，2024 | RL 行为规划方法、建模和评价 | 规划/行为重点；E2E 关联需全文确认 | 104；元数据+摘要索引。适合规划目标和奖励设计 |
| S015 | C | [A Survey of Autonomous Vehicle Behaviors: Trajectory Planning Algorithms, Sensed Collision Risks, and User Expectations](https://doi.org/10.3390/s24154808) | Taokai Xia、Hui Chen | Sensors，2024 | 轨迹规划、碰撞风险和用户期望 | 侧重行为与风险，不是 E2E 架构综述 | 26；元数据+摘要。安全/舒适度指标补充 |

## 2025

| ID | 级别 | 综述（原题） | 作者（首位/等） | 载体、正式年与链接 | 核心范围与分类框架 | 数据/评测/工程资产 | 引用数；证据与用途 |
|---|---|---|---|---|---|---|---|
| S016 | B | [A Survey of Autonomous Driving from a Deep Learning Perspective](https://doi.org/10.1145/3729420) | Jingyuan Zhao et al. | ACM Computing Surveys，2025 | 感知、定位建图、决策控制；CNN/RNN/Transformer；监督/无监督/RL；模块化到 E2E | 广义 AD 综述，未专门统一 E2E benchmark | 73；摘要+元数据。ACM 页面另出现 `10.1145/3697207`，暂按一个 DOI 记录。**全文不可得（ACM 403，arXiv 无预印本）** |
| S017 | A（子任务） | [A Survey on End-to-end Perception and Prediction for Autonomous Driving](https://doi.org/10.1007/s11633-025-1558-0) | Yufan Hu et al. | Machine Intelligence Research，2025 | 端到端 perception-and-prediction（PnP）；按 LiDAR、camera、multi-modal 和架构分类 | PnP 管线与新场景方向；与完整 planning/control E2E 不同 | 7；出版社摘要+元数据。适合感知-预测接口和监督设计 |
| S018 | A | [End-to-End Autonomous Driving: From Classic Paradigm to Large Model Empowerment—A Comprehensive Survey](https://doi.org/10.1109/JIOT.2025.3635092) | Wei Dong et al. | IEEE Internet of Things Journal，2025 | IL、RL、foundation model、LLM/VLM；规划、推理、数据生成、场景理解；展望 world model、蒸馏、稀疏激活和可部署性 | 摘要未列具体 benchmark | 6；摘要+元数据。较新的 E2E—大模型总览。**全文不可得（IEEE 403，arXiv 无预印本）** |
| S019 | A | [Survey of General End-to-End Autonomous Driving: A Unified Perspective](https://doi.org/10.36227/techrxiv.176523315.56439138/v3) | Yixiang Yang et al. | TechRxiv，v1/v2/v3 均为 2025；保留 v3 | 200+ 篇；vision-centric、VLM-centric、hybrid 三类 GE2E；设计哲学、训练策略、benchmark | 统一 benchmark 与比较分析；[GE2EAD](https://github.com/AutoLab-SAI-SJTU/GE2EAD) | 0；Crossref 摘要+v3 版本元数据+项目页。三版本合并，不重复计数。**全文不可得（TechRxiv Cloudflare 403）** |
| S020 | A | [A Survey on End-to-End Autonomous Driving Training from the Perspectives of Data, Strategy, and Platform](https://doi.org/10.36227/techrxiv.176523171.14650662/v1) | Chengkai Xu et al. | TechRxiv，2025-12-08 | Data–Strategy–Platform 三层训练生态；数据价值、学习策略、训练基础设施与训练-测试闭环 | 直接对应数据、训练策略、平台/仿真约束；项目页需从正文进一步核验 | 未被 OpenAlex 收录；Crossref 摘要+版本元数据。实验投入评估的关键入口。**全文不可得（TechRxiv 403）** |
| S021 | A/C | [A Survey on Vision-Language-Action Models for Autonomous Driving](https://doi.org/10.1109/ICCVW69036.2025.00476)（[arXiv 2506.24044](https://arxiv.org/abs/2506.24044)） | Shan Jiang et al. | ICCV Workshop，2025；arXiv 同题版本 | 20+ 代表性 VLA；视觉/语言/动作模块、训练、数据集、benchmark、instruction fidelity 与安全 | BDD100K/BDD-X、nuScenes、Bench2Drive、Reason2Drive 等在全文表中出现；[Awesome-VLA4AD](https://github.com/JohnsonJiang1996/Awesome-VLA4AD) | 15（DOI 记录）；摘要+HTML 章节/项目页。新一代 E2E/VLA 入口 |
| S022 | C | [A Survey on Large Language Model-Powered Autonomous Driving](https://doi.org/10.1016/j.eng.2025.07.038)（相关预印本：[arXiv 2409.14165](https://arxiv.org/abs/2409.14165)） | Yuxuan Zhu et al. | Engineering，2025 | LLM 在模块化与 E2E AD、长尾、推理、优化中的应用；安全与安全性风险 | 具体数据集/代码需全文核验；与 2024 预印本存在作者重合，但版本关系未完全确认 | 14；摘要+元数据。作为 LLM 方向补充 |
| S023 | C | [Deep Reinforcement and IL for Autonomous Driving: A Review in the CARLA Simulation Environment](https://doi.org/10.3390/app15168972) | Piotr Czechowski et al. | Applied Sciences，2025 | CARLA 中 RL/IL 的状态、动作、奖励、架构和组合方式；讨论泛化与鲁棒性 | CARLA；摘要报告未见环境外独立复现 | 10；摘要+元数据。适合 CARLA、IL/RL 和失败成本分析 |
| S024 | C | [A survey of decision-making and planning methods for self-driving vehicles](https://doi.org/10.3389/fnbot.2025.1451923) | Jun Hu et al. | Frontiers in Neurorobotics，2025 | 知识驱动、数据驱动（IL/RL/IRL）与混合方法；规则、博弈、搜索、采样、优化 | 讨论实验平台和验证策略 | 41；摘要+元数据。规划基线和评价协议补充 |
| S025 | C | [A Survey of Autonomous Driving Trajectory Prediction](https://doi.org/10.3390/machines13090818) | Miao Xu et al. | Machines，2025 | 输入表示、输出形式、方法范式、交互建模；包含 diffusion/LLM | 关注多主体轨迹、地图/场景上下文、数据集和指标 | 16；摘要+元数据。与 DiffusionDrive 的轨迹输出直接相关 |
| S026 | C | [Recent Advances in Interactive Driving of Autonomous Vehicles: Comprehensive Review of Approaches](https://doi.org/10.1007/s42154-024-00332-w) | Yanwen Yang et al. | Automotive Innovation，正式记录 2025 | LSTM、Transformer、APF、博弈论、RL/DRL、POMDP；人与车交互 | 只聚焦 AV 与 human-driven vehicles 的互动 | 18；出版社摘要+元数据。闭环交互与社会性评价补充 |
| S027 | C | [Understanding World or Predicting Future? A Comprehensive Survey of World Models](https://doi.org/10.1145/3746449) | Jingtao Ding et al. | ACM Computing Surveys，2025 | 世界模型的“理解当前状态”与“预测未来状态”二分；覆盖 AD、机器人和社会模拟 | [World-Model 代码/论文目录](https://github.com/tsinghua-fib-lab/World-Model) | 57；出版社摘要+项目页。适合世界模型可靠性与闭环规划 |
| S028 | C | [Survey of research on autonomous driving testing with large models](https://doi.org/10.1016/j.commtr.2025.100179) | Songyan Liu et al. | Communications in Transportation Research，2025 | 大模型辅助自动驾驶测试；具体分类需全文核验 | 重点是测试而非训练模型；适合测试用例和长尾场景 | 22；Crossref/OpenAlex 元数据。摘要不可得，证据较弱 |
| S029 | C | [Foundation Models for Autonomous Driving Perception: A Survey Through Core Capabilities](https://doi.org/10.1109/OJVT.2025.3604823) | Rajendramayavan Sathyam、Yueqi Li | IEEE Open Journal of Vehicular Technology，2025 | 按 foundation model 核心能力整理感知任务 | 主要是感知，不能直接替代 E2E 规划综述 | 8；Crossref/OpenAlex 元数据。需全文核验 benchmark 与代码 |
| S030 | C | [Efficient and real-time perception: a survey on end-to-end event-based object detection in autonomous driving](https://doi.org/10.3389/frobt.2025.1674421) | Kamilya Smagulova et al. | Frontiers in Robotics and AI，2025 | event camera 的 dense/spiking/graph 网络、编码和硬件；从 raw event 到检测输出 | GEN1、1MP；摘要报告 RTX 4090 系统吞吐比较 | 3；出版社摘要+元数据。是传感器/实时性专题，不是全栈 E2E |
| S031 | C | [Diffusion Models for Intelligent Transportation Systems: A Survey](https://doi.org/10.1109/TITS.2025.3613178)（[arXiv 2409.15816v3](https://arxiv.org/abs/2409.15816)） | Mingxing Peng et al. | IEEE TITS，2025；arXiv 首发 2024 | diffusion 基础、conditional/latent 变体；自动驾驶、交通仿真、轨迹预测、交通安全 | 摘要覆盖 ITS 多模态数据和可控生成；[survey repo](https://github.com/Pemixing/Diffusion-Models-in-ITS-A-Survey) | 20；摘要+项目页。与 DiffusionDrive 最相关的专题综述之一，但范围大于 E2E |

## 2026

| ID | 级别 | 综述（原题） | 作者（首位/等） | 载体、正式年与链接 | 核心范围与分类框架 | 数据/评测/工程资产 | 引用数；证据与用途 |
|---|---|---|---|---|---|---|---|
| S032 | A | [Planning-Oriented End-to-End Autonomous Driving: Architectures, Evaluation, and Emerging Paradigms](https://arxiv.org/abs/2608.20111) | Yanchen Guan et al. | arXiv，2026-08-20 | 按 input representation、planning output、supervision、evaluation 四轴；从 neural control/conditional IL/privileged distillation 到 BEV/vector planning、world model、VLA | 讨论 open-loop、pseudo/closed-loop、non-reactive log、long-tail、人类偏好指标；HTML 目录已核验 | 未被 OpenAlex 收录；arXiv 摘要+全文目录。当前最适合研究脉络和公平评测的入口 |
| S033 | A | [Post-Training in End-to-End Autonomous Driving](https://arxiv.org/abs/2607.08072) | Ruining Yang et al. | arXiv v2，2026-07-13 | distillation、preference-based alignment、RL post-training、test-time refinement；后训练监督的四类组织方式 | 专门区分 open-loop、pseudo-closed-loop、closed-loop；[Awesome-Post-Training](https://github.com/RYNing/Awesome-Post-Training-In-Autonomous-Driving-Papers) | 未被 OpenAlex 收录；arXiv 摘要+全文目录+项目页。适合从 BC 走向闭环优化 |
| S034 | A | [Diffusion Models for End-to-End Autonomous Driving: A Survey of Perception, Prediction, Planning, and Control](https://doi.org/10.1109/ACCESS.2026.3704955) | J. Choi et al. | IEEE Access，2026 | 按 perception、prediction、planning、control、scenario diffusion 五类；比较数据集和评价协议 | 讨论采样多模态候选、约束引导、实时性、安全和 open/closed-loop 差异 | 0；OpenAlex+摘要。DiffusionDrive 直接专题，需进一步获取全文表 |
| S035 | A | [A Comprehensive Review of End-to-End Autonomous Driving: Architectures and Emerging Trends](https://doi.org/10.3390/act15080427) | Yunxing Chen et al. | Actuators，2026 | function-oriented taxonomy：perception-integrated 与 planning-integrated；兼顾解释性、安全、工业部署 | 数据、闭环 workflow、simulation testing、延迟/算力和长尾 | 0；MDPI 摘要+元数据。偏工程部署的最新全景综述。**全文不可得（MDPI 403）** |
| S036 | D | [A Review of End to End Autonomous Driving: Existing Systems, Learning Methods, Challenges and Future Directions](https://doi.org/10.56028/aetr.16.1.267.2026) | Haolan Hong | Advances in Engineering Technology Research，2026 | 传统模块化对比 E2E；代表系统、学习方法、挑战与方向 | 摘要信息较短，期刊影响和全文质量需单独核验 | 0；OpenAlex 摘要+元数据。保留作检索完整性记录，暂不作为主入口 |
| S037 | A/C | [From Proxy Metrics to Driving-Level Objectives: A Survey of End-to-End Architectures for Autonomous Driving](https://doi.org/10.1109/AQTR70159.2026.11577855) | Rareş Lemnariu et al. | AQTR conference，2026 | 标题聚焦代理指标到驾驶级目标；具体分类和实验协议待全文 | 直接对应 open-loop 指标与驾驶级目标的公平性问题 | 0；OpenAlex 元数据，摘要未取到。优先补全文 |
| S038 | A | [Research progress in end-to-end autonomous driving systems](https://doi.org/10.1117/12.3109910) | Chenhao Qi | SPIE conference，2026 | PilotNet、ChauffeurNet、TransFuser 等经典路线；再到 DriveLM、GPT-Driver 等大模型路线 | 摘要明确讨论数据集、评价方法和闭环标准 | 0；OpenAlex 摘要+元数据。适合快速建立历史路线，但需核验会议全文 |
| S039 | C | [Explainable and Safe Learning-Based Autonomous Driving: A Survey from Modular to End-to-End Planning](https://doi.org/10.36227/techrxiv.177084714.46890967/v1) | Tim Puphal | TechRxiv，2026-02-11 | 分离式 prediction/planning、联合 prediction/planning、E2E planning；物理先验、风险预测、安全屏蔽、可解释网络、LLM 推理 | 重点是安全与解释性；未核验代码 | 0；Crossref 摘要+元数据。安全约束与 E2E 结合的补充 |
| S040 | C | [Foundation Models in Autonomous Driving: A Survey on Scenario Generation and Scenario Analysis](https://doi.org/10.1109/OJITS.2026.3660686) | Yuan Gao et al. | IEEE Open Journal of ITS，2026 | foundation model 在场景生成与场景分析中的方法路线 | 直接关联仿真数据、长尾场景和测试生成 | 18；Crossref/OpenAlex 元数据。适合数据生成/仿真适配 |
| S041 | C | [Beyond Textual Chain-of-Thought: A Survey on Action-Grounded Reasoning in Autonomous Driving](https://arxiv.org/abs/2609.01659) | Zhengxu Tang et al. | arXiv，2026-08-31；标注 accepted by EMNLP 2026 | 171 篇（130 方法、41 benchmark/dataset/survey）；language-based、visual-spatial、latent-dynamic、externalized reasoning 四类、13 个子类 | 关注中间表示、实时动作耦合和安全验证；[awesome-av-cot](https://github.com/tangzhengxu/awesome-av-cot) | 未被 OpenAlex 收录；arXiv 摘要+项目页。适合 VLA/推理型 E2E |
| S042 | C | [A Survey on Interaction-Aware Decision-Making for Autonomous Driving](https://doi.org/10.1109/TITS.2026.3678531) | Shen Li et al. | IEEE TITS，2026 | 交互感知决策、挑战与解决方案 | 适合分析闭环中其他交通参与者反应；摘要未取到 | 4；Crossref/OpenAlex 元数据，全文待核验 |
| S043 | C | [Vehicle Trajectory Prediction for Autonomous Driving Applications: State-of-the-Art Review](https://doi.org/10.1007/s42154-025-00382-8) | Yongjun Yan et al. | Automotive Innovation，2026-01-10 | 物理/概率、深度学习、RL 三类；交互、意图、多模态融合、轨迹多样性 | 预测是决策控制核心；不等于 E2E 规划综述 | 9；出版社摘要+元数据。适合轨迹头与评测补充 |
| S044 | C | [A survey of transformer architectures for autonomous driving](https://doi.org/10.1016/j.eswa.2025.130338) | Fulin Chu et al. | Expert Systems with Applications，卷期 2026-03；online record 2025-11 | 按检测、融合、预测、规划、意图预测分类；摄像头/LiDAR/radar/HD map；讨论 E2E、CoT、神经符号和边缘部署 | 系统级 Transformer 与多模态输入；具体 benchmark 需全文核验 | 13；Crossref/OpenAlex 摘要。DOI 年份与卷期年份不同，按一条记录 |
| S045 | C | [Ranging from prediction to planning via machine learning approaches for autonomous driving: a survey](https://doi.org/10.1007/s10462-026-11604-8) | Ding Li、Qichao Zhang、D. M. Zhao | Artificial Intelligence Review，2026-06-08 | marginal/conditional/interactive prediction-and-planning；涉及 modular 与 E2E、LLM、world model、蒸馏、RLHF、长尾 | 强调交互式预测规划和评价平台 | 0；OpenAlex+Crossref+出版社摘要。作为交互预测与 E2E 规划的待复核补充 |

## 去重与版本关系

1. `S001`、`S002`、`S004`、`S006`、`S008`、`S017`、`S019`、`S021`、`S031` 同时保留正式 DOI 与可访问预印本，但每个研究只占一行。
2. `S019` 的 TechRxiv v1/v2/v3 是同一综述，最新可见版本为 v3（2025-12-29），不要按三个版本计数。
3. `S021` 的 arXiv 与 ICCV Workshop 版本同题，作为一个版本链；正式会议条目优先用于出版信息。
4. `S022` 与 `arXiv:2409.14165` 有作者和主题重合，但当前没有足够证据断言是同一正式版本，因此在备注中保留“相关预印本”，不做硬合并。
5. `S031` 的 arXiv 首发为 2024，IEEE TITS 正式记录为 2025；按正式出版年放在 2025，同时保留首发链接。
6. `S044` DOI 创建于 2025-11，但 Crossref 正式卷期为 2026-03；按正式卷期列入 2026。

## 优先阅读顺序（面向当前 E2E/DiffusionDrive 问题）

1. **先建立总框架**：S001 → S019 → S032。
2. **再固定公平比较协议**：S003、S009、S010、S011、S020、S032、S033、S037。
3. **DiffusionDrive 专题**：S031 → S025 → S034；重点比较生成对象、条件输入、约束/引导、训练监督、推理预算和 open/closed-loop 指标。
4. **闭环与失败成本**：S013、S014、S023、S026、S033、S042、S045。
5. **大模型/VLA/世界模型**：S004、S005、S006、S018、S021、S027、S040、S041。

## 检索日志与局限

- 使用过 arXiv API、OpenAlex、Crossref、Semantic Scholar（本次受限于 429）、出版社摘要/HTML；Consensus 工具本次返回异常并触发限流，未作为唯一证据。
- Zotero 本地库已按 `end-to-end autonomous driving`、`autonomous driving survey/review`、`VLA autonomous driving` 等关键词检索，当前没有匹配条目，因此本表不是从用户 Zotero 库导出的。
- 出版商页面、OpenAlex 与 Crossref 对 online-first/卷期年份可能不同；表中保留这种差异，不把 DOI 前缀年份直接当作正式出版年。
- 摘要/元数据不能替代全文阅读；尤其是 S028、S029、S037、S038、S042、S045 尚未完成全文表格和代码链接核验。
- 综述被列入本表不等于其中的性能结论、代码或 benchmark 已被独立复现。下一步应固定论文版本、仓库 commit、数据集版本和评价协议。
