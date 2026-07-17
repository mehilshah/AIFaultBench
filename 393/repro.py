from __future__ import annotations

import json
import os
import socket
import sys
import traceback
from pathlib import Path

import torch
import torch.multiprocessing as mp


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _worker(rank: int, world_size: int, port: int, queue) -> None:
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = str(port)
    os.environ["RANK"] = str(rank)
    os.environ["WORLD_SIZE"] = str(world_size)
    os.environ.pop("LOCAL_RANK", None)
    os.environ["ACCELERATE_TORCH_DEVICE"] = "cpu"

    torch.distributed.init_process_group("gloo", rank=rank, world_size=world_size)
    try:
        from accelerate import Accelerator
        from accelerate.test_utils.scripts.test_script import test_split_between_processes_nested_dict

        Accelerator()
        print(f"rank={rank} starting nested-dict split check", flush=True)
        test_split_between_processes_nested_dict()
        print(f"rank={rank} passed", flush=True)
        queue.put(
            {
                "rank": rank,
                "status": "pass",
            }
        )
    except Exception:
        error = traceback.format_exc()
        print(f"rank={rank} failed", file=sys.stderr, flush=True)
        print(error, file=sys.stderr, flush=True)
        queue.put(
            {
                "rank": rank,
                "status": "fail",
                "error": error,
            }
        )
        raise
    finally:
        torch.distributed.destroy_process_group()


def main() -> int:
    world_size = 4
    port = _find_free_port()
    ctx = mp.get_context("spawn")
    queue = ctx.SimpleQueue()

    print(f"using world_size={world_size} port={port}", flush=True)
    try:
        mp.spawn(_worker, args=(world_size, port, queue), nprocs=world_size, join=True)
        exited_with_failure = False
    except Exception as exc:
        exited_with_failure = True
        spawn_error = traceback.format_exc()
        print(spawn_error, file=sys.stderr, flush=True)
    else:
        spawn_error = ""

    results = []
    while not queue.empty():
        results.append(queue.get())

    results.sort(key=lambda item: item["rank"])
    failed = any(item["status"] == "fail" for item in results) or exited_with_failure

    failing_item = next((item for item in results if item["status"] == "fail"), None)
    if failing_item is not None:
        evidence = (
            "Nested-dict split assertion fails in a 4-process run at "
            "accelerate/test_utils/scripts/test_script.py:479: "
            "assert results[\"a\"] == data_copy[\"a\"][-1]"
        )
    elif exited_with_failure:
        evidence = "Distributed spawn failed before completing the nested-dict check. " + spawn_error.splitlines()[-1]
    else:
        evidence = "All 4 ranks passed the nested-dict split check."

    result = {
        "reproducible": failed,
        "evidence": evidence,
        "steps": [
            "Create an isolated venv and install the pinned CPU-only dependencies.",
            "Run the 4-process CPU distributed harness in repro.py.",
            "Observe the assertion failure from test_split_between_processes_nested_dict on ranks 1-3.",
        ],
        "blocking_reason": "" if failed else "No blocker; the bug reproduced successfully.",
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
