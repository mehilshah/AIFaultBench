from __future__ import annotations

import argparse
import sys
from contextlib import contextmanager
from pathlib import Path

import torch


ROOT_DIR = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT_DIR / "codebase" / "src"
if str(CODEBASE_SRC) not in sys.path:
    sys.path.insert(0, str(CODEBASE_SRC))

from diffusers.models.attention_dispatch import (  # noqa: E402
    AttentionBackendName,
    _HUB_KERNELS_REGISTRY,
    _flash_attention_3_varlen_hub,
)


class SkipRepro(RuntimeError):
    pass


def _fake_flash_attn_3_varlen_func(
    q,
    k,
    v,
    cu_seqlens_q,
    cu_seqlens_k,
    max_seqlen_q,
    max_seqlen_k,
    softmax_scale,
    causal,
):
    # The reported contract mismatch is that the hub kernel returns a single tensor.
    return q + 1000


def _make_inputs(device: str):
    batch_size = 2
    seq_len = 4
    heads = 2
    dim = 64

    query = torch.randn(batch_size, seq_len, heads, dim, device=device, dtype=torch.bfloat16)
    key = query.clone()
    value = query.clone()
    return query, key, value


@contextmanager
def _temporary_kernel(kernel_fn):
    registry_entry = _HUB_KERNELS_REGISTRY[AttentionBackendName._FLASH_3_VARLEN_HUB]
    original_kernel_fn = registry_entry.kernel_fn
    registry_entry.kernel_fn = kernel_fn
    try:
        yield
    finally:
        registry_entry.kernel_fn = original_kernel_fn


def _run_diffusers_wrapper(query, key, value, kernel_fn):
    with _temporary_kernel(kernel_fn):
        return _flash_attention_3_varlen_hub(query, key, value)


def _run_mock_repro():
    query, key, value = _make_inputs("cpu")
    expected = query + 1000
    out = _run_diffusers_wrapper(query, key, value, _fake_flash_attn_3_varlen_func)

    print("mode: mock tensor-returning FA3 varlen function")
    print(f"expected shape: {tuple(expected.shape)}")
    print(f"actual shape:   {tuple(out.shape)}")
    print(f"actual tensor equals expected: {torch.equal(out, expected)}")

    if tuple(out.shape) != tuple(expected.shape):
        print("BUG REPRODUCED: tensor return was destructured as if it were a tuple.")
        return

    raise RuntimeError("Bug did not reproduce; _flash_attention_3_varlen_hub preserved the full tensor output.")


def _require_sm90():
    if not torch.cuda.is_available():
        raise SkipRepro("CUDA is unavailable, so the real FA3 repro cannot run here.")

    major, minor = torch.cuda.get_device_capability()
    device_name = torch.cuda.get_device_name()
    if major != 9:
        raise SkipRepro(
            f"The real FA3 repro requires an NVIDIA SM90 GPU, but got {device_name} with capability {major}.{minor}."
        )

    return f"{device_name} sm{major}{minor}"


def _run_real_repro():
    device_description = _require_sm90()

    from kernels import get_kernel

    kernel_module = get_kernel("kernels-community/flash-attn3", version=1)
    kernel_fn = kernel_module.flash_attn_varlen_func

    query, key, value = _make_inputs("cuda")
    batch_size, seq_len, _, _ = query.shape

    cu_seqlens = torch.arange(
        0,
        (batch_size + 1) * seq_len,
        step=seq_len,
        device=query.device,
        dtype=torch.int32,
    )
    query_packed = query.flatten(0, 1)
    key_packed = key.flatten(0, 1)
    value_packed = value.flatten(0, 1)

    direct = kernel_fn(
        q=query_packed,
        k=key_packed,
        v=value_packed,
        cu_seqlens_q=cu_seqlens,
        cu_seqlens_k=cu_seqlens,
        max_seqlen_q=seq_len,
        max_seqlen_k=seq_len,
        softmax_scale=None,
        causal=False,
    )

    if isinstance(direct, tuple):
        raise SkipRepro(
            "The loaded hub kernel returned a tuple in this environment, so the reported contract mismatch is not present."
        )

    expected = direct.unflatten(0, (batch_size, seq_len))
    out = _run_diffusers_wrapper(query, key, value, kernel_fn)

    print("mode: real kernels-community/flash-attn3 flash_attn_varlen_func")
    print(f"device: {device_description}")
    print(f"direct kernel return type: {type(direct).__name__}")
    print(f"direct kernel shape:      {tuple(direct.shape)}")
    print(f"expected wrapper shape:   {tuple(expected.shape)}")
    print(f"actual wrapper shape:     {tuple(out.shape)}")
    print(f"actual tensor equals expected: {torch.equal(out, expected)}")

    if tuple(out.shape) != tuple(expected.shape):
        print("BUG REPRODUCED: Diffusers destructured the tensor return as if it were a tuple.")
        return

    raise RuntimeError("Bug did not reproduce; _flash_attention_3_varlen_hub preserved the full tensor output.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["auto", "mock", "real"],
        default="auto",
        help="auto uses the real path on SM90 CUDA and falls back to the mock tensor-returning kernel on CPU.",
    )
    args = parser.parse_args()

    if args.mode == "mock":
        _run_mock_repro()
        return

    if args.mode == "real":
        try:
            _run_real_repro()
        except SkipRepro as error:
            print(f"SKIPPED: {error}", file=sys.stderr)
            sys.exit(77)
        return

    if torch.cuda.is_available():
        try:
            _run_real_repro()
        except SkipRepro as error:
            print(f"SKIPPED: {error}", file=sys.stderr)
            sys.exit(77)
    else:
        _run_mock_repro()


if __name__ == "__main__":
    main()
