# 第五十六轮（2026-09-29）· 补齐轮次指针 + HF checkpoint 定位

**性质**：收尾补账轮。两件事——补上第四十九至五十四轮漏掉的 README 指针，以及关闭待续清单第 17 项里"下载 checkpoint"这个阻塞。

## 一、补齐第四十九至五十四轮的指针（收尾漏了第 2/3 步）

README「最近动态」与 `state.md`「当前阶段」此前停在**第四十八轮**，而 `rounds-49`~`rounds-54` 六个文件均已存在。逐份读回后补入 README 指针表：

| 轮次 | 做了什么 |
|---|---|
| 第四十九轮 | 把路线 B 的第一步写成**预注册实验协议**（四项纯推理测量；未运行） |
| 第五十轮 | 明确**只读任务优先走内置 Read/Grep/Glob**，禁止 shell 承担读取/搜索/统计 |
| 第五十一轮 | 当前态传播核查（README / state / project.md 三处旧表述） |
| 第五十二轮 | 收敛等待项为两类真实阻塞（checkpoint + navhard 数据；正式立项） |
| 第五十三轮 | 修正选优协议的聚合口径：`C_N` 降级为 oracle 诊断量 |
| 第五十四轮 | 把完整政策分与候选池诊断分开（协议重组为两层） |

**根因**：第五十一轮已发现并修了"最新一轮停在第四十八轮"，但只**追加**了第五十一轮指针、**没删**那行旧表述；第五十二轮"同步根 README"改的是「等待用户」节、不是「最近动态」表；第五十三、五十四轮未动 README。→ **三轮各修一半，结果是 README 同时出现"第五十一轮"与"最新一轮：第四十八轮"。**

## 二、HF checkpoint 定位（关闭待续清单第 17 项的下载阻塞）

**结论：目标 checkpoint 可下载，且在 HF `datasets` 仓库里——不是 `models`。**

- 数据集仓库 `datasets/OpenDriveLab/SimScale`：**446 文件 / 12 个 `.ckpt`**，HTTP 可达
- **目标**：`SimScale_ckpts/DiffusionDrive/diffusiondrive_sim_navhard.ckpt` —— HTTP 200，`x-linked-size` **243,596,717 字节（243.6 MB）**
- 同批 12 个 ckpt：DiffusionDrive（navhard / navtest）、GTRS_Dense 8 个（`resnet`/`vov` × `expert`/`reward` × `navhard`/`navtest`）、LTF（navhard / navtest）
- ModelScope 有镜像（README 给 `modelscope.cn/datasets/OpenDriveLab/SimScale`）

**为什么之前找不到**（本轮两次走弯路，记下来）：
1. 搜索 `models` 端点 —— 而它在 `datasets` 端点下。第六版记录只写"HF 上发布好的 `diffusiondrive_sim_navhard.ckpt`"，**没写清是 dataset 还是 model**
2. 先猜 `OpenDriveLab/SimScale`、`OpenDriveLab/GTRS` 作为 model 仓库 → 均 401（**HF 对不存在的 model 返 401 而非 404**，容易被误读成"无权限"）
3. 另有**同名不同内容的近邻仓库**：`datasets/OpenDriveLab-org/SimScale` 是**另一个仓库**（388 文件、**0 个 ckpt**，只放 `SimScale_data/` 合成数据）——**带 `-org` 与否是两个仓库**，容易混

**顺带确认**：DiffusionDrive 套 SimScale 后的 navhard 分数 = **32.6（+5.1）**，与 [sota-plan.md §7.7](../ideas/sota-plan.md) 的记载一致。

**对路线 ②③ 的意义**：第 17 项记的"路线 ②③ 的第一步（用它的 ckpt 跑评测）需要用户协助下载或调整沙箱"——**网络与定位两部分都已解除**（HF 走代理可达见[第五十五轮](rounds-55.md)），**只剩"243.6 MB 下载 + 环境搭建"的执行成本**。

## 三、官方 navhard 排行榜的准确入口

- **是 Space，不是 dataset**：`spaces/AGC2025/e2e-driving-navhard`（标题 "[navhard] NAVSIM v2 End-to-End Driving"，HTTP 200）
- 其仓库含评测应用本体（`competitions/app.py`、`compute_metrics.py`、CLI `create`/`run`/`submit`）——即官方榜单的计算代码可直接取
- `datasets/AGC2025/e2e-driving-navhard` **不存在**（401）
