#!/usr/bin/env python3
import os
import sys
import time
import torch.multiprocessing as mp

WORLD_SIZE = 4
MASTER_ADDR = os.environ.get("MASTER_ADDR", "127.0.0.1")
MASTER_PORT = os.environ.get("MASTER_PORT", "29580")


def worker(rank: int, world_size: int, results):
    # Force the CPU distributed path. The original bug is in the context-manager
    # wrappers, so this exercises the same `Accelerator` code without requiring
    # more than one visible GPU.
    os.environ.pop("LOCAL_RANK", None)
    os.environ["RANK"] = str(rank)
    os.environ["WORLD_SIZE"] = str(world_size)
    os.environ["MASTER_ADDR"] = MASTER_ADDR
    os.environ["MASTER_PORT"] = MASTER_PORT

    from accelerate import Accelerator

    accelerator = Accelerator()

    with accelerator.main_process_first():
        if accelerator.is_main_process:
            time.sleep(1)
        print(f"main:{accelerator.process_index}:{accelerator.is_main_process}", flush=True)
        results.append(("main", accelerator.process_index, accelerator.is_main_process))

    with accelerator.local_main_process_first():
        if accelerator.is_local_main_process:
            time.sleep(1)
        print(f"local:{accelerator.process_index}:{accelerator.is_local_main_process}", flush=True)
        results.append(("local", accelerator.process_index, accelerator.is_local_main_process))


def main():
    ctx = mp.get_context("spawn")
    manager = ctx.Manager()
    results = manager.list()
    mp.spawn(worker, args=(WORLD_SIZE, results), nprocs=WORLD_SIZE, join=True)

    ordered = list(results)
    print("ordered_results:", ordered)

    main_first = next(item for item in ordered if item[0] == "main")
    local_first = next(item for item in ordered if item[0] == "local")

    if main_first[1] != 0 or local_first[1] != 0:
        raise RuntimeError(
            "main_process_first/local_main_process_first misordered: "
            f"main={main_first}, local={local_first}"
        )

    print("No misordering observed.")


if __name__ == "__main__":
    sys.exit(main())
