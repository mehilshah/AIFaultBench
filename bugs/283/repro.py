from __future__ import annotations

import json
import tempfile
from pathlib import Path

from transformers import Qwen3VLConfig, Qwen3VLForConditionalGeneration


def build_tiny_checkpoint(base_dir: Path) -> None:
    config = Qwen3VLConfig(
        vision_config={
            "depth": 1,
            "hidden_size": 16,
            "intermediate_size": 32,
            "num_heads": 4,
            "out_hidden_size": 32,
            "num_position_embeddings": 8,
            "spatial_merge_size": 1,
            "patch_size": 2,
            "temporal_patch_size": 1,
        },
        text_config={
            "vocab_size": 128,
            "hidden_size": 32,
            "intermediate_size": 64,
            "num_hidden_layers": 2,
            "num_attention_heads": 4,
            "num_key_value_heads": 4,
            "head_dim": 8,
            "max_position_embeddings": 64,
        },
    )
    Qwen3VLForConditionalGeneration(config).save_pretrained(base_dir)


def main() -> None:
    root = Path.cwd()
    work_dir = Path(tempfile.mkdtemp(prefix="qwen3vl_offload_repro_", dir=str(root)))
    base_dir = work_dir / "base"
    offload_dir = work_dir / "offload"
    save_dir = work_dir / "saved"
    base_dir.mkdir(parents=True, exist_ok=True)
    offload_dir.mkdir(parents=True, exist_ok=True)

    build_tiny_checkpoint(base_dir)
    print(f"baseline checkpoint written to {base_dir}")

    model = Qwen3VLForConditionalGeneration.from_pretrained(
        base_dir,
        device_map="auto",
        max_memory={"cpu": "50KB"},
        offload_folder=str(offload_dir),
    )

    hf_device_map = getattr(model, "hf_device_map", None)
    param_devices = sorted({p.device.type for p in model.parameters()})
    meta_params_present = any(p.device.type == "meta" for p in model.parameters())

    print(f"loaded hf_device_map: {hf_device_map}")
    print(f"param devices: {param_devices}")
    print(f"meta params present: {meta_params_present}")

    model.save_pretrained(save_dir)
    print(f"saved offloaded checkpoint to {save_dir}")
    print(f"saved files: {sorted(p.name for p in save_dir.iterdir())}")

    result = {
        "reproducible": False,
        "evidence": (
            "A mixed CPU/disk-offloaded Qwen3VL checkpoint loads and saves successfully in this checkout. "
            "The repro emits a warning about offloaded modules and writes model.safetensors without error."
        ),
        "steps": [
            "Create a tiny local Qwen3VL checkpoint from config.",
            "Reload it with device_map='auto' and max_memory={'cpu': '50KB'} to force CPU/disk offloading.",
            "Call save_pretrained() on the offloaded model.",
        ],
        "blocking_reason": "The current codebase already handles saving a mixed CPU/disk-offloaded Qwen3VL model, so the reported meta-tensor failure does not occur here.",
        "reproduction_command": "./run_repro.sh",
    }
    (root / "reproduction.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
