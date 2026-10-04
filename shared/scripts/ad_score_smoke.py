import json
import lzma
import os
import pickle
from pathlib import Path

os.environ['OMP_NUM_THREADS'] = '1'
os.environ['PROGRESS_MODE'] = 'eval'

import numpy as np
from navsim.common.dataclasses import Trajectory
from navsim.evaluate.pdm_score import pdm_score
from navsim.planning.simulation.planner.pdm_planner.scoring.pdm_scorer import PDMScorer, PDMScorerConfig
from navsim.planning.simulation.planner.pdm_planner.simulation.pdm_simulator import PDMSimulator
from navsim.traffic_agents_policies.log_replay_traffic_agents import LogReplayTrafficAgents
from nuplan.planning.simulation.trajectory.trajectory_sampling import TrajectorySampling

workspace = Path(__file__).resolve().parents[2]
cache_path = next((workspace / 'inbox/scratch/metric-cache-smoke').rglob('metric_cache.pkl'))
with lzma.open(cache_path, 'rb') as stream:
    cache = pickle.load(stream)
sampling = TrajectorySampling(num_poses=40, interval_length=0.1)
trajectory = Trajectory(np.zeros((8, 3)))
result, _ = pdm_score(cache, trajectory, sampling, PDMSimulator(sampling), PDMScorer(sampling, PDMScorerConfig()), LogReplayTrafficAgents(sampling))
assert np.isfinite(result.select_dtypes(include='number').to_numpy()).all()
print(result.to_json(orient='records'))
output_path = workspace / 'inbox/scratch/score-smoke.json'
output_path.write_text(json.dumps({'type': 'stationary-trajectory environment smoke; non-reactive Stage-1 only', 'cache': str(cache_path), 'result': json.loads(result.to_json(orient='records'))}), encoding='utf-8')
