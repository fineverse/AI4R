import json
import os
from pathlib import Path

os.environ['OMP_NUM_THREADS'] = '1'

import torch
from navsim.agents.diffusiondrive.transfuser_agent import TransfuserAgent
from navsim.agents.diffusiondrive.transfuser_config import TransfuserConfig

workspace = Path(__file__).resolve().parents[2]
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
with torch.inference_mode():
    outputs = agent(features)
summary = {key: {'shape': list(value.shape), 'finite': bool(torch.isfinite(value).all())} for key, value in outputs.items() if torch.is_tensor(value)}
print(json.dumps(summary))
assert summary['trajectory']['finite']
