import json
import os
import argparse
from pathlib import Path

os.environ['OMP_NUM_THREADS'] = '1'

import torch
from navsim.agents.diffusiondrive.transfuser_agent import TransfuserAgent
from navsim.agents.diffusiondrive.transfuser_config import TransfuserConfig

workspace = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--sensor-root', type=Path)
parser.add_argument('--log-root', type=Path)
args = parser.parse_args()
config = TransfuserConfig()
config.bkb_path = str(workspace / 'inbox/scratch/resnet34_model.bin')
config.plan_anchor_path = str(workspace / 'inbox/scratch/simscale-runtime/traj_final/kmeans_navsim_traj_20.npy')
agent = TransfuserAgent(config, lr=6e-4)
checkpoint = torch.load(workspace / 'inbox/scratch/diffusiondrive_sim_navhard.ckpt', map_location='cpu')
weights = {key.replace('agent.', ''): value for key, value in checkpoint['state_dict'].items()}
agent.load_state_dict(weights, strict=True)
agent = agent.cuda().eval()
features = {
    'camera_feature': torch.zeros(1, 3, config.camera_height, config.camera_width, device='cuda'),
    'status_feature': torch.zeros(1, 8, device='cuda'),
}
if args.sensor_root:
    if args.log_root is None:
        parser.error('--log-root is required with --sensor-root')
    from navsim.common.dataloader import SceneLoader
    from hydra.utils import instantiate
    from omegaconf import OmegaConf
    scene_filter = OmegaConf.load(workspace / 'inbox/scratch/simscale-runtime/navsim/planning/script/config/common/train_test_split/scene_filter/navhard_two_stage.yaml')
    scene_filter.max_scenes = 1
    scene_filter.include_synthetic_scenes = False
    loader = SceneLoader(data_path=args.log_root, original_sensor_path=args.sensor_root, scene_filter=instantiate(scene_filter), sensor_config=agent.get_sensor_config())
    agent_input = loader.get_agent_input_from_token(loader.tokens[0])
    features = agent.get_feature_builders()[0].compute_features(agent_input)
    features = {key: value.unsqueeze(0).cuda() for key, value in features.items()}
with torch.inference_mode():
    outputs = agent(features)
summary = {key: {'shape': list(value.shape), 'finite': bool(torch.isfinite(value).all())} for key, value in outputs.items() if torch.is_tensor(value)}
print(json.dumps(summary))
assert summary['trajectory']['finite']
