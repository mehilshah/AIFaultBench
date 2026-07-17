#!/usr/bin/env python3
import json
import warnings
from pathlib import Path

from lightning.pytorch import Trainer
from lightning.pytorch.callbacks.throughput_monitor import ThroughputMonitor
from lightning.pytorch.demos.boring_classes import BoringModel


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def main() -> int:
    model = BoringModel()
    monitor = ThroughputMonitor(batch_size_fn=lambda batch: 1)

    trainer = Trainer(
        devices=1,
        max_steps=2,
        limit_val_batches=0,
        num_sanity_val_steps=0,
        log_every_n_steps=1,
        enable_checkpointing=False,
        enable_model_summary=False,
        enable_progress_bar=False,
        logger=False,
        callbacks=[monitor],
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        trainer.fit(model)

    messages = [str(w.message) for w in caught if "flops_per_batch" in str(w.message)]
    reproducible = len(messages) == 2
    result = {
        "reproducible": reproducible,
        "evidence": (
            "A 2-step Trainer.fit run with ThroughputMonitor and no flops_per_batch attribute emitted the same "
            f"warning {len(messages)} times."
        ),
        "steps": [
            "Create the virtual environment and install the pinned dependencies with bash setup_env.sh.",
            "Run bash run_repro.sh to execute the Lightning training loop and capture the warnings.",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"warning_count={len(messages)}")
    for idx, message in enumerate(messages, 1):
        print(f"warning[{idx}]={message}")
    print(f"wrote={RESULT_PATH}")

    if not reproducible:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
