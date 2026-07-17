from torch import nn
from tensordict.nn import TensorDictModule

from torchrl.collectors import MultiSyncDataCollector
from torchrl.envs.libs.gym import GymEnv


def main():
    env_maker = lambda: GymEnv("Pendulum-v1", device="cpu")
    policy = TensorDictModule(nn.Linear(3, 1), in_keys=["observation"], out_keys=["action"])
    collector = MultiSyncDataCollector(
        create_env_fn=[env_maker, env_maker],
        policy=policy,
        total_frames=2000,
        max_frames_per_traj=50,
        frames_per_batch=200,
        init_random_frames=-1,
        reset_at_each_iter=False,
        device="cpu",
        storing_device="cpu",
        cat_results=0,
        split_trajs=True,
    )
    collector.set_seed(42)
    try:
        for i, data in enumerate(collector):
            print(f"iter={i} shape={tuple(data.shape)}")
            if i == 2:
                print(data)
                break
    finally:
        collector.shutdown()
        del collector


if __name__ == "__main__":
    main()
