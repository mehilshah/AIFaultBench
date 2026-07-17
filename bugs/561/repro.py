#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"

REPRODUCTION_COMMAND = """MODEL="openai/gpt-oss-120b"
TP_SIZE=2
CPU_BYTES=26843545600

KV_TRANSFER_CONFIG=$(cat <<EOF
{
  "kv_connector": "OffloadingConnector",
  "kv_role": "kv_both",
  "kv_connector_extra_config": {
    "enable_cross_layers_blocks": "True",
    "spec_name": "CPUOffloadingSpec",
    "cpu_bytes_to_use": ${CPU_BYTES},
    "eviction_policy": "lru"
  }
}
EOF
)

vllm serve "${MODEL}" \
      --tensor-parallel-size="${TP_SIZE}" \
      --kv-transfer-config "${KV_TRANSFER_CONFIG}" \
      --enable-prefix-caching \
      --no-disable-hybrid-kv-cache-manager

lm_eval \
  --model local-completions \
  --model_args "base_url=http://127.0.0.1:8000/v1/completions,model=${MODEL},tokenized_requests=False,num_concurrent=1000,trust_remote_code=True" \
  --tasks gsm8k \
  --seed 42 \
  --num_fewshot 5 \
  --gen_kwargs temperature=0.0"""


@dataclass(frozen=True)
class KVCacheGroup:
    layer_names: list[str]
    page_size_bytes: int


@dataclass(frozen=True)
class KVCacheTensor:
    size: int
    shared_by: list[str]
    offset: int = 0
    block_stride: int = 0


def show_snippet(path: Path, marker: str, radius: int = 5) -> None:
    try:
        lines = path.read_text().splitlines()
    except OSError as exc:
        print(f"[snippet-missing] {path}: {exc}")
        return

    for idx, line in enumerate(lines):
        if marker in line:
            start = max(0, idx - radius)
            end = min(len(lines), idx + radius + 1)
            print(f"\n--- {path.relative_to(ROOT)}:{start + 1}-{end} ---")
            for lineno in range(start, end):
                print(f"{lineno + 1:4d}: {lines[lineno]}")
            return

    print(f"[snippet-missing] marker {marker!r} not found in {path}")


def dtype_size_bytes(dtype_name: str) -> int:
    sizes = {
        "float16": 2,
        "bfloat16": 2,
        "float32": 4,
        "uint8": 1,
    }
    return sizes[dtype_name]


def full_attention_page_size_bytes(
    block_size: int,
    num_kv_heads: int,
    head_size: int,
    head_size_v: int | None = None,
    dtype_name: str = "float16",
) -> int:
    if head_size_v is None:
        head_size_v = head_size
    return (
        block_size
        * num_kv_heads
        * (head_size + head_size_v)
        * dtype_size_bytes(dtype_name)
    )


def bucket_layers_by_page_size(
    kv_cache_groups: list[KVCacheGroup],
) -> dict[int, list[list[str]]]:
    buckets: dict[int, list[list[str]]] = defaultdict(list)
    for group in kv_cache_groups:
        slot_count: dict[int, int] = defaultdict(int)
        for layer_name in group.layer_names:
            ps = group.page_size_bytes
            slot_idx = slot_count[ps]
            slot_count[ps] += 1
            if slot_idx == len(buckets[ps]):
                buckets[ps].append([])
            buckets[ps][slot_idx].append(layer_name)
    return buckets


def get_packed_layout(kv_cache_groups: list[KVCacheGroup], available_memory: int) -> tuple[int, list[KVCacheTensor]]:
    buckets = bucket_layers_by_page_size(kv_cache_groups)
    total_num_bytes_per_block = sum(ps * len(slots) for ps, slots in buckets.items())
    num_blocks = available_memory // total_num_bytes_per_block
    total_size = total_num_bytes_per_block * num_blocks

    kv_cache_tensors: list[KVCacheTensor] = []
    byte_offset = 0
    for ps, slots in buckets.items():
        for slot in slots:
            kv_cache_tensors.append(
                KVCacheTensor(
                    size=total_size,
                    shared_by=slot,
                    offset=byte_offset,
                    block_stride=total_num_bytes_per_block,
                )
            )
            byte_offset += ps
    return num_blocks, kv_cache_tensors


def gpu_info() -> dict[str, Any]:
    info: dict[str, Any] = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }
    try:
        import torch

        info["torch_version"] = torch.__version__
        info["cuda_available"] = bool(torch.cuda.is_available())
        if torch.cuda.is_available():
            info["cuda_device_count"] = torch.cuda.device_count()
            info["cuda_device_name"] = torch.cuda.get_device_name(0)
            info["cuda_capability"] = ".".join(
                str(v) for v in torch.cuda.get_device_capability(0)
            )
        else:
            info["cuda_device_count"] = 0
    except Exception as exc:  # pragma: no cover - environment-specific
        info["torch_import_error"] = f"{type(exc).__name__}: {exc}"
    return info


def main() -> int:
    print("Bug report reproduction summary")
    print(f"Repo root: {ROOT}")
    print(f"Codebase path: {CODEBASE}")
    print()

    info = gpu_info()
    for key, value in info.items():
        print(f"{key}: {value}")

    print("\nSource evidence:")
    show_snippet(CODEBASE / "vllm" / "v1" / "core" / "kv_cache_utils.py", "_get_kv_cache_config_packed")
    show_snippet(CODEBASE / "vllm" / "v1" / "attention" / "backends" / "flash_attn.py", "kv_cache.unbind(1)")

    full_page_size = full_attention_page_size_bytes(
        block_size=16,
        num_kv_heads=2,
        head_size=64,
        dtype_name="float16",
    )
    sw_page_size = full_page_size
    available_memory = full_page_size * 2 * 32

    default_groups = [
        KVCacheGroup(["full.0", "full.1"], full_page_size),
        KVCacheGroup(["sw.0", "sw.2"], sw_page_size),
        KVCacheGroup(["sw.1", "sw.3"], sw_page_size),
    ]
    packed_num_blocks, packed_tensors = get_packed_layout(default_groups, available_memory)

    dtype_size = dtype_size_bytes("float16")
    page_size_elems = full_page_size // dtype_size

    print("\nDerived packing math:")
    print(f"full_attention_page_size_bytes: {full_page_size}")
    print(f"available_memory: {available_memory}")
    print(f"packed_num_blocks: {packed_num_blocks}")
    print(f"page_size_elems: {page_size_elems}")
    for idx, tensor in enumerate(packed_tensors):
        print(
            f"packed_tensor[{idx}]: size={tensor.size}, offset={tensor.offset}, "
            f"block_stride_bytes={tensor.block_stride}, "
            f"block_stride_elems={tensor.block_stride // dtype_size}"
        )

    print("\nRoot-cause check:")
    print(
        "packed block_stride bytes == 2 * page_size bytes:",
        packed_tensors[0].block_stride == 2 * full_page_size,
    )
    print(
        "key/value cache stride used by FlashAttention would be larger than a single layer page:",
        packed_tensors[0].block_stride // dtype_size > page_size_elems,
    )

    gpu_name = str(info.get("cuda_device_name", "unknown"))
    reproducible = False
    blocking_reason = (
        "The exact issue report is not reproduced here: the local GPU is "
        f"{gpu_name}, not the Hopper H100 reported in the bug, and the full "
        "vllm serve + lm_eval workload was not executed."
    )

    evidence = [
        f"Source-derived packed layout uses block_stride={packed_tensors[0].block_stride} bytes for a page size of {full_page_size} bytes.",
        "That is exactly the 2x-page stride mismatch described in the issue report.",
        f"Local CUDA device: {gpu_name} ({info.get('cuda_capability', 'n/a')}), which is not the reported H100 Hopper setup.",
    ]

    steps = [
        "Inspect the source-tree packing logic in vllm/v1/core/kv_cache_utils.py.",
        "Compute the cross-layer packed KV cache layout for the reported HMA group structure.",
        "Compare the resulting block stride against the single-layer page size.",
    ]

    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": REPRODUCTION_COMMAND,
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(f"\nWrote {RESULT_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
