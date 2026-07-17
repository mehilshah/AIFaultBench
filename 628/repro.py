from __future__ import annotations

import os
import threading
from contextlib import suppress

import torch
import torch.nn as nn
from tensordict.nn import TensorDictModule
from torchrl.collectors import MultiSyncDataCollector
from torchrl.data import LazyTensorStorage, RandomSampler, TensorDictReplayBuffer
from torchrl.envs import EnvCreator, GymEnv, ParallelEnv


TIMEOUT_SECONDS = 30


def create_env():
    return GymEnv("Pendulum-v1")


create_env_new = EnvCreator(create_env)


def build_parallel_env():
    return ParallelEnv(4, create_env_new, device="cpu")


def build_policy():
    policy_net = nn.Linear(3, 1)
    return TensorDictModule(
        policy_net, in_keys=["observation"], out_keys=["action"]
    )


def manual_extend_smoke_test() -> None:
    env = build_parallel_env()
    policy = build_policy()
    replay_buffer = TensorDictReplayBuffer(
        storage=LazyTensorStorage(1024, ndim=1),
        sampler=RandomSampler(),
        batch_size=16,
    )
    batch = env.rollout(2, policy)
    replay_buffer.extend(batch.reshape(-1))
    print(
        f"manual_extend_ok len={len(replay_buffer)} write_count={replay_buffer.write_count}",
        flush=True,
    )
    env.close()


def _timeout_handler() -> None:
    print(
        f"collector_timeout: collector did not yield a batch within {TIMEOUT_SECONDS} seconds",
        flush=True,
    )
    os._exit(1)


def main() -> None:
    torch.manual_seed(0)
    manual_extend_smoke_test()

    replay_buffer = TensorDictReplayBuffer(
        storage=LazyTensorStorage(2_000_000, ndim=1),
        sampler=RandomSampler(),
        batch_size=128,
    )
    policy = build_policy()

    timer = threading.Timer(TIMEOUT_SECONDS, _timeout_handler)
    timer.daemon = True
    timer.start()
    collector = None
    try:
        collector = MultiSyncDataCollector(
            [build_parallel_env],
            policy,
            frames_per_batch=64,
            total_frames=256,
            extend_buffer=True,
            replay_buffer=replay_buffer,
            device="cpu",
            storing_device="cpu",
            env_device="cpu",
            policy_device="cpu",
        )
        print("collector_created", flush=True)
        for i, _ in enumerate(collector):
            print(
                f"iter={i} len={len(replay_buffer)} write_count={replay_buffer.write_count}",
                flush=True,
            )
            break
        print("collector_completed", flush=True)
    finally:
        timer.cancel()
        if collector is not None:
            with suppress(Exception):
                collector.shutdown()


if __name__ == "__main__":
    main()
