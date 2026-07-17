#!/usr/bin/env python3
from __future__ import annotations

import sys
import threading
import time

import torch
from tensordict import TensorDict
from torchrl.data import LazyTensorStorage, SliceSampler, TensorDictReplayBuffer


def normalize_index(index) -> list[tuple[int, int]]:
    if isinstance(index, tuple):
        coords = zip(*(x.detach().cpu().tolist() for x in index))
        return [tuple(map(int, coord)) for coord in coords]
    return [tuple(map(int, row.tolist())) for row in index.detach().cpu()]


def main() -> int:
    if not torch.cuda.is_available():
        print("BLOCKED: CUDA is not available in this environment.")
        return 2

    device = torch.device("cuda:0")
    storage = LazyTensorStorage(10000, device=device, ndim=2)
    sampler = SliceSampler(
        slice_len=10,
        strict_length=False,
        traj_key=("collector", "traj_ids"),
    )
    rb = TensorDictReplayBuffer(storage=storage, sampler=sampler, batch_size=1000)

    expected: dict[tuple[int, int], int] = {}
    expected_lock = threading.Lock()
    stop = threading.Event()
    writer_error: list[BaseException] = []

    def writer() -> None:
        try:
            i = 0
            while not stop.is_set():
                obs = torch.full((4, 100), float(i), device="cpu")
                td = TensorDict({"obs": obs}, batch_size=[4, 100])
                td["collector", "traj_ids"] = torch.full((4, 100), i, dtype=torch.long)
                index = rb.extend(td)
                with expected_lock:
                    for coord in normalize_index(index):
                        expected[coord] = i
                i += 1
        except BaseException as err:  # noqa: BLE001
            writer_error.append(err)
            stop.set()

    thread = threading.Thread(target=writer, daemon=True)
    thread.start()

    try:
        time.sleep(1.0)

        for step in range(3000):
            if writer_error:
                raise writer_error[0]

            sample, info = rb.sample(return_info=True)
            coords = normalize_index(info["index"])
            obs = sample["obs"].detach().cpu()
            traj = sample["collector", "traj_ids"].detach().cpu()

            with expected_lock:
                exp = [expected.get(coord) for coord in coords]

            if any(value is None for value in exp):
                print(f"UNSEEN_INDEX step={step}")
                print(f"coords={coords[:8]}")
                return 1

            exp_obs = torch.tensor(exp, dtype=obs.dtype)
            exp_traj = torch.tensor(exp, dtype=traj.dtype)

            if not torch.equal(obs, exp_obs) or not torch.equal(traj, exp_traj):
                obs_bad = (obs != exp_obs).nonzero(as_tuple=False)
                traj_bad = (traj != exp_traj).nonzero(as_tuple=False)
                bad_idx = int(obs_bad[0, 0]) if obs_bad.numel() else int(traj_bad[0, 0])
                print(f"CORRUPTION step={step}")
                print(f"sample_idx={bad_idx}")
                print(f"storage_coord={coords[bad_idx]}")
                print(f"expected={exp[bad_idx]}")
                print(f"got_obs={float(obs[bad_idx].item())}")
                print(f"got_traj={int(traj[bad_idx].item())}")
                return 1

            if step % 300 == 0:
                print(f"ok step={step} sample_len={obs.numel()}")

        print("NO_CORRUPTION")
        return 0
    finally:
        stop.set()
        thread.join(timeout=5)


if __name__ == "__main__":
    sys.exit(main())
