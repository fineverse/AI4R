
## 已提交的产出

- 本轮目标：下载 NAVSIM v2 navhard 所需资产，准备名为 `AD` 的运行环境；尚未完成正式评测。
- `.gitignore` 排除 `AD/`，防止依赖进入知识工作空间版本库。
- SimScale 运行副本：`inbox/scratch/simscale-runtime`，commit `07c3305c5cd4c4d517ce913749bb6f713b81e9b1`。
- nuPlan v1.2 副本：`inbox/scratch/nuplan-devkit`，commit `ce3c323af01c0d7ec5672f7832ef53f9c679aab0`。

## 待安装的规则

无。服务器直连 Hugging Face 不可达，ModelScope 与 hf-mirror 实测可达；不沿用旧机器的 localhost 代理。

## 待处理的遗留

- `AD` 已重建为 Python 3.9.25；旧 Python 3.8 环境保留在 `inbox/scratch/AD-python38-backup`。PyTorch 2.2.1 与 torchvision 0.17.1 安装进行中，完整依赖与 agent 启动尚待验证。
- navhard 当前/历史传感器压缩文件分别为 12,804,089,546 / 25,521,966,184 字节；下载进程正在数据盘传输，不代表完成。
- 场景文件已解包至数据盘 `ai4r_navsim/navhard/scene_pickles`；还需地图、backbone 权重、完整传感器、metric cache。
- SimScale 运行副本不能自动视为协议固定的 NAVSIM commit `0a380a9`；正式评价前必须核验兼容性及评价路径。

## 证据等级

- 成功运行：RTX 4090 D CUDA 可用；checkpoint 已加载到 GPU，`state_dict` 含 764 个条目。这不是模型推理或复现结果。
- checkpoint：`inbox/scratch/diffusiondrive_sim_navhard.ckpt`，243,596,717 字节；SHA-256 `8fdbdb3fdfa7b496e7d7a438efbb5c2022377e59cbfd7095270d89623c5d963f`，与 ModelScope `X-Linked-ETag` 一致。
- 场景包：`inbox/scratch/navsim_v2.2_navhard_two_stage_scene_pickles.tar.gz`，211,118,643 字节；SHA-256 `a2e429a01e9a93afd9d1f753ed306f469c094292627467182d35fae9fb2ecad7`，与 HF 元数据一致；解包成功。
- 此记录为环境准备中间交付，不能认定实验已完成。
