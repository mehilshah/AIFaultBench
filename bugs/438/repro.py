import json
import os
import sys
import tempfile
import traceback


EXPECTED_SUBSTR = "requires dynamic loss scaling"


class DummyBackend:
    name = "dummy"

    def is_initialized(self):
        return True

    def get_rank(self, group=None):
        return 0

    def get_world_size(self, group=None):
        return 1

    def get_global_rank(self, group=None, group_rank=0):
        return 0


def _cleanup(cfg_path):
    try:
        import torch.distributed as dist

        if dist.is_available() and dist.is_initialized():
            dist.destroy_process_group()
    except Exception:
        pass

    try:
        if cfg_path and os.path.exists(cfg_path):
            os.remove(cfg_path)
    except Exception:
        pass


def main():
    try:
        import torch
        import torch.nn as nn
        import torch.distributed as dist
        import deepspeed
        import deepspeed.comm.comm as ds_comm
    except Exception as e:
        print(f"HARNESS_ERROR: {e}")
        return 1

    # Avoid DeepSpeed's unrelated CPU shared-memory comm op path so the repro
    # reaches the constructor assertion from the bug report.
    ds_comm.cdb = DummyBackend()

    if not dist.is_initialized():
        dist.init_process_group(backend="gloo", init_method="env://")

    class TinyModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.lin = nn.Linear(8, 4)

        def forward(self, x):
            return self.lin(x)

    model = TinyModel()

    fd, cfg_path = tempfile.mkstemp(prefix="ds_cfg_", suffix=".json")
    os.close(fd)
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "train_batch_size": 1,
                "train_micro_batch_size_per_gpu": 1,
                "gradient_accumulation_steps": 1,
                "optimizer": {"type": "Lamb", "params": {"lr": 1e-3}},
                "fp16": {"enabled": False, "loss_scale": 128},
                "bf16": {"enabled": True},
                "zero_optimization": {"stage": 0},
            },
            f,
            indent=2,
            sort_keys=True,
        )

    try:
        deepspeed.initialize(
            model=model,
            model_parameters=list(model.parameters()),
            config=cfg_path,
            dist_init_required=False,
        )
        print("UNEXPECTED: initialize() returned successfully")
        _cleanup(cfg_path)
        return 2
    except BaseException as e:
        if EXPECTED_SUBSTR in str(e).lower():
            print(f"EXPECTED_INIT_FAILURE: {e}")
            print("Test Passed")
            _cleanup(cfg_path)
            return 0

        print(f"UNEXPECTED_EXCEPTION: {type(e).__name__}: {e}")
        traceback.print_exc()
        _cleanup(cfg_path)
        return 3


if __name__ == "__main__":
    sys.exit(main())
