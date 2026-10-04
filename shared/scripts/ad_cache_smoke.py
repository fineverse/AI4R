import os
import argparse
from pathlib import Path

os.environ['OMP_NUM_THREADS'] = '1'
os.environ['NUPLAN_MAPS_ROOT'] = '/root/autodl-tmp/ai4r_navsim/maps/nuplan-maps-v1.0'
os.environ['PROGRESS_MODE'] = 'eval'

from hydra.utils import instantiate
from omegaconf import OmegaConf
from navsim.common.dataloader import SceneLoader
from navsim.planning.scenario_builder.navsim_scenario import NavSimScenario
from navsim.planning.metric_caching.metric_cache_processor import MetricCacheProcessor
from nuplan.planning.simulation.trajectory.trajectory_sampling import TrajectorySampling

workspace = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--max-scenes', type=int, default=1)
args = parser.parse_args()
config = OmegaConf.load(workspace / 'inbox/scratch/simscale-runtime/navsim/planning/script/config/common/train_test_split/scene_filter/navhard_two_stage.yaml')
config.max_scenes = args.max_scenes
config.include_synthetic_scenes = False
loader = SceneLoader(
    data_path=Path('/root/autodl-tmp/ai4r_navsim/dataset/openscene-v1.1/meta_datas/test'),
    synthetic_sensor_path=None,
    original_sensor_path=None,
    scene_filter=instantiate(config),
)
processor = MetricCacheProcessor(
    str(workspace / 'inbox/scratch/metric-cache-smoke'),
    False,
    TrajectorySampling(num_poses=40, interval_length=0.1),
)
for token in loader.tokens:
    scene = loader.get_scene_from_token(token)
    scenario = NavSimScenario(scene, os.environ['NUPLAN_MAPS_ROOT'], 'nuplan-maps-v1.0')
    result = processor.compute_and_save_metric_cache(scenario)
    print(result, flush=True)
