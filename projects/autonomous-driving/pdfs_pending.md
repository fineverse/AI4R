# 待下载 PDF 清单（需要用户协助的部分）

更新时间：2026-09-23  
说明：本线程已能自行获取 arXiv 论文（HTML 或 PDF + `pdftotext`），因此本清单**只列我无法自行获取的部分**，按优先级排列。  
存放方式建议：PDF 放进 Zotero 对应 collection（工作空间规则是"PDF 留 Zotero，工作空间只放笔记"），我用 Zotero 本地连接器读全文后写笔记。

## A. 需要你协助下载（我无法获取，付费墙且无预印本）

| 优先级 | 编号 | 论文 | 载体与年 | DOI / 入口 | 为什么需要 |
|---|---|---|---|---|---|
| P1 | S034 | Diffusion Models for End-to-End Autonomous Driving: A Survey of Perception, Prediction, Planning, and Control | IEEE Access，2026 | [10.1109/ACCESS.2026.3704955](https://doi.org/10.1109/ACCESS.2026.3704955) | 与本研究最贴合的驾驶侧扩散综述；arXiv 未检索到预印本，IEEE Access 通常开放，可先试直接下载 |
| P1 | S035 | A Comprehensive Review of End-to-End Autonomous Driving: Architectures and Emerging Trends | MDPI Actuators 15(8):427，2026 | [10.3390/act15080427](https://doi.org/10.3390/act15080427) | 最新的 E2E 全景综述（function-oriented taxonomy）；**MDPI 对 curl/WebFetch 均返回 403，浏览器可打开** |
| P1 | S019 | Survey of General End-to-End Autonomous Driving: A Unified Perspective | TechRxiv v3，2025 | [10.36227/techrxiv.176523315.56439138/v3](https://doi.org/10.36227/techrxiv.176523315.56439138/v3) | 200+ 篇；vision-centric / VLM-centric / hybrid 三分类；**TechRxiv 403** |
| P1 | S020 | A Survey on End-to-End Autonomous Driving Training from the Perspectives of Data, Strategy, and Platform | TechRxiv v1，2025 | [10.36227/techrxiv.176523171.14650662/v1](https://doi.org/10.36227/techrxiv.176523171.14650662/v1) | Data–Strategy–Platform 三维度；**TechRxiv 403** |
| P2 | S016 | A Survey of Autonomous Driving from a Deep Learning Perspective | ACM Computing Surveys，2025 | [10.1145/3729420](https://doi.org/10.1145/3729420) | ACM 标注 hybrid OA，但 pdf 端点对 curl 返回 403；浏览器可下载 |
| P2 | S018 | End-to-End Autonomous Driving: From Classic Paradigm to Large Model Empowerment | IEEE IoT-J，2025 | [10.1109/JIOT.2025.3635092](https://doi.org/10.1109/JIOT.2025.3635092) | OpenAlex 标注 closed；无 arXiv 预印本 |
| P2 | DP-S10 | A Survey on Flow Matching for Robotic Trajectory Generation and Control | ICTC 2025 | [10.1109/ICTC66702.2025.11388651](https://doi.org/10.1109/ICTC66702.2025.11388651) | 流匹配是主方向主要竞争路线；Crossref 已核验存在，但 arXiv 无预印本、OpenAlex 无记录，需 IEEE 全文 |
| P2 | DP-S12 | A Survey on Diffusion Policy for Robotic Manipulation: Taxonomy, Analysis, and ... | TechRxiv，2025 | [10.36227/techrxiv.174378343.39356214](https://doi.org/10.36227/techrxiv.174378343.39356214) | OpenAlex 已确认记录存在（3 次引用），但 TechRxiv 页面返回 403；若你能打开，可取到分类框架 |

**注**：S016/S019/S020/S035 的 OA 入口我都试过（ACM pdf 端点、MDPI /pdf、TechRxiv /doi/pdf，并换用浏览器 UA），**一律 403**。这几篇是"浏览器能打开、命令行不行"的类型，需要你下载。

## A2. 已通过预印本自行解决（原 P0 两项，**不需要你下载**）

| 编号 | 论文 | 正式载体 | 预印本 | 处理 |
|---|---|---|---|---|
| S001 | End-to-End Autonomous Driving: Challenges and Frontiers | IEEE TPAMI 2024 | [arXiv 2306.16927](https://arxiv.org/abs/2306.16927) | 已自取全文并提取分类框架与开放问题 |
| S031 | Diffusion Models for Intelligent Transportation Systems: A Survey | IEEE TITS 2025 | [arXiv 2409.15816](https://arxiv.org/abs/2409.15816) | 同上 |
| DP-S11 | Generative AI for Autonomous Driving: Frontiers and Opportunities | ACM Computing Surveys 2026 | [arXiv 2505.08854](https://arxiv.org/abs/2505.08854) | 同上 |
| DP-S15 | Generative AI for Autonomous Driving: A Review | 投 IEEE（comments） | [arXiv 2505.15863](https://arxiv.org/abs/2505.15863) | 本轮新发现的同题综述，一并提取 |

## B. 已自行获取完成（2026-09-22）

以下论文的 arXiv HTML 表格单元格丢失，已改用 PDF + `pdftotext -layout` 补齐，**不需要你处理**。PDF 放在 `/tmp` 未入工作空间，笔记里的数字已标注表号。

| 编号 | 论文 | 补齐了什么 |
|---|---|---|
| DP-A08 | BridgeDrive（[2509.23589](https://arxiv.org/abs/2509.23589)） | Table 2 消融、Table 4 NAVSIM PDMS 88.0、Table 5 Bench2Drive、Table 7 推理时间 0.10 s / 20 步 |
| DP-A14 | MeanFuser（[2602.20060](https://arxiv.org/abs/2602.20060)） | Table 1/2 主结果、Table 3 参数量与速度、Table 4 消融（含 M3 −17.8） |
| DP-A16 | DIVER（[2507.04049](https://arxiv.org/abs/2507.04049)） | Table 1–5 全部结果、FPS 41 |
| DP-E08 | SafeFlowMatcher（[2509.24243](https://arxiv.org/abs/2509.24243)） | Table 1/2/3/10/11（安全、延迟、α 与 T_p 消融） |
| DP-A31 | DriveFuture（[2605.09701](https://arxiv.org/abs/2605.09701)） | Table 1 navhard 55.5（已核实为表内最高）、Table 2/3 主结果、Table 4/5 消融 |
| DP-A12 | GuideFlow（[2511.18729](https://arxiv.org/abs/2511.18729)） | Eq.14/16/17–18 三机制、Table 1/3/5/6（navhard 43.0、3.6 FPS、λ 与 k_c 消融） |
| DP-A21 | PC-Diffuser（[2603.10330](https://arxiv.org/abs/2603.10330)） | Eq.1/7/11/16/17、Thm.1/Cor.1、Table I/II（CR 100%→10.29%、5× 延迟） |
| DP-A22 | G2SD（[2608.09484](https://arxiv.org/abs/2608.09484)） | Eq.3/4、Thm.3/6、Table 1/2/3（非驾驶域） |
| DP-A18 | FeaXDrive（[2604.12656](https://arxiv.org/abs/2604.12656)） | Eq.14/15/22/23/26/28、Table 2/3/4/5（违规率与消融） |
| DP-A04 / DP-A05 | AnchDrive（[2509.20253](https://arxiv.org/abs/2509.20253)）、DriveAnchor（[2606.00519](https://arxiv.org/abs/2606.00519)） | Table 1/2/3（EPDMS 85.5、锚点消融、2.06 ms） |
| DP-E01/E02/E03/E04/E11/E12/E15/E28 | 具身奠基 8 篇（Diffuser、Decision Diffuser、Diffusion-QL、EDP、DiffuserLite、Consistency Policy、Equivariant DP、DPPO） | 各自的引导尺度、步数、频率、延迟与消融表 |

## C. 代码仓库（已全部获取，**不需要你处理**）

此前因 TLS 中断（`gnutls_handshake() failed`）未获取的 4 个仓库，已用"8–10 次重试 + `git ls-remote` 取默认分支 + codeload tarball 兜底"全部补齐：

| 目标目录 | 论文 / 编号 | 仓库 | 状态 |
|---|---|---|---|
| `DiffusionDriveV2` | DiffusionDriveV2（DP-A03） | [hustvl/DiffusionDriveV2](https://github.com/hustvl/DiffusionDriveV2)（默认分支 master） | tarball 已获取 |
| `Diffusion-Planner` | Diffusion Planner（DP-A01） | [ZhengYinan-AIR/Diffusion-Planner](https://github.com/ZhengYinan-AIR/Diffusion-Planner) | commit `a3a621f` |
| `GoalFlow` | GoalFlow（DP-A09） | [YvanYin/GoalFlow](https://github.com/YvanYin/GoalFlow) | commit `411fdbd` |
| `MeanFuser` | MeanFuser（DP-A14） | [wjl2244/MeanFuser](https://github.com/wjl2244/MeanFuser) | commit `8de8ba6` |

代码快照现为 **37 个仓库（约 1.65 GB，全部未安装未运行）**，见 [code/repositories.md](code/repositories.md)。

## D. 已确认无需下载

- **已有 arXiv 全文并完成提取**：DP-A01、DP-A02、DP-A03、DP-A08、DP-A09、DP-A14、DP-A16、DP-A20、DP-E01（Diffuser 思想）、DP-E08、DP-E09、DP-E10、DP-E17、DP-E19。
- **代码快照已保存**：见 [code/repositories.md](code/repositories.md)（**当时 32 个**官方仓库已获取，含 commit 或 tarball 标注，无待重试项；**现共 37 个，1.65 GB**）。
- **全文覆盖已核验（2026-09-23）**：本轮抓取的 **37 个 arXiv 全文 ID 全部已在工作空间登记，无遗漏**；其中 6 篇未建笔记（DP-A04/A05、DP-E02/E03/E12/E28），事实写在论文表格行内。

## E. 后续若进入 idea 阶段需要补的全文（届时按需自取）

具身侧目前多为摘要级（DP-E11–E27 中的多数）；若某个 idea 落在"流匹配 + RL 微调""世界模型条件化""约束注入"上，再针对性拉取对应论文的 PDF，而不是一次全下。
