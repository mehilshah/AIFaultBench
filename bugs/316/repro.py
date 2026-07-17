#!/usr/bin/env python3
from __future__ import annotations

import math
import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from diffusers.models.attention_dispatch import (  # noqa: E402
    AttentionBackendName,
    _HUB_KERNELS_REGISTRY,
    _flash_attention_3_varlen_hub,
)


def reference_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: torch.Tensor,
    scale: float | None = None,
) -> torch.Tensor:
    if scale is None:
        scale = query.shape[-1] ** -0.5

    query_bh = query.permute(0, 2, 1, 3)
    key_bh = key.permute(0, 2, 1, 3)
    value_bh = value.permute(0, 2, 1, 3)
    scores = torch.matmul(query_bh, key_bh.transpose(-1, -2)) * scale
    scores = scores.masked_fill(~attn_mask[:, None, None, :], torch.finfo(scores.dtype).min)
    probs = torch.softmax(scores, dim=-1)
    return torch.matmul(probs, value_bh).permute(0, 2, 1, 3)


def packed_attention_kernel(
    *,
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    cu_seqlens_q: torch.Tensor,
    cu_seqlens_k: torch.Tensor,
    max_seqlen_q: int,
    max_seqlen_k: int,
    softmax_scale: float | None = None,
    causal: bool = False,
):
    del max_seqlen_q, max_seqlen_k, causal

    if softmax_scale is None:
        softmax_scale = q.shape[-1] ** -0.5

    outputs = []
    for batch_idx in range(cu_seqlens_q.numel() - 1):
        q_start = int(cu_seqlens_q[batch_idx].item())
        q_end = int(cu_seqlens_q[batch_idx + 1].item())
        k_start = int(cu_seqlens_k[batch_idx].item())
        k_end = int(cu_seqlens_k[batch_idx + 1].item())

        q_b = q[q_start:q_end].permute(1, 0, 2)
        k_b = k[k_start:k_end].permute(1, 0, 2)
        v_b = v[k_start:k_end].permute(1, 0, 2)

        scores = torch.matmul(q_b, k_b.transpose(-1, -2)) * softmax_scale
        probs = torch.softmax(scores, dim=-1)
        out_b = torch.matmul(probs, v_b).permute(1, 0, 2)
        outputs.append(out_b)

    return torch.cat(outputs, dim=0)


def run_case(name: str, attn_mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    batch_size, seq_len = attn_mask.shape
    num_heads = 1
    head_dim = 4

    query = torch.arange(batch_size * seq_len * num_heads * head_dim, dtype=torch.float32).reshape(
        batch_size, seq_len, num_heads, head_dim
    )
    key = query + 1000.0
    value = query + 2000.0

    query_backend = query.clone().requires_grad_(True)
    key_backend = key.clone().requires_grad_(True)
    value_backend = value.clone().requires_grad_(True)

    query_ref = query.clone().requires_grad_(True)
    key_ref = key.clone().requires_grad_(True)
    value_ref = value.clone().requires_grad_(True)

    original_kernel = _HUB_KERNELS_REGISTRY[AttentionBackendName._FLASH_3_VARLEN_HUB].kernel_fn
    _HUB_KERNELS_REGISTRY[AttentionBackendName._FLASH_3_VARLEN_HUB].kernel_fn = packed_attention_kernel
    try:
        backend_out = _flash_attention_3_varlen_hub(
            query_backend,
            key_backend,
            value_backend,
            attn_mask=attn_mask,
            scale=None,
            is_causal=False,
            return_lse=False,
        )
    finally:
        _HUB_KERNELS_REGISTRY[AttentionBackendName._FLASH_3_VARLEN_HUB].kernel_fn = original_kernel

    reference_out = reference_attention(query_ref, key_ref, value_ref, attn_mask)

    backend_loss = backend_out.square().sum()
    reference_loss = reference_out.square().sum()
    backend_loss.backward()
    reference_loss.backward()

    forward_diff = (backend_out - reference_out).abs().max().item()
    grad_diff = max(
        (query_backend.grad - query_ref.grad).abs().max().item(),
        (key_backend.grad - key_ref.grad).abs().max().item(),
        (value_backend.grad - value_ref.grad).abs().max().item(),
    )

    print(f"{name}: forward_max_abs_diff={forward_diff:.6f}")
    print(f"{name}: grad_max_abs_diff={grad_diff:.6f}")

    return backend_out, reference_out, torch.tensor([forward_diff, grad_diff])


def main() -> None:
    torch.manual_seed(0)
    print(f"torch={torch.__version__}")
    print(f"backend={AttentionBackendName._FLASH_3_VARLEN_HUB.value}")

    contiguous_mask = torch.ones(2, 6, dtype=torch.bool)
    run_case("contiguous", contiguous_mask)

    non_contiguous_mask = torch.tensor(
        [
            [True, False, True, False, True, False],
            [False, True, True, False, True, False],
        ],
        dtype=torch.bool,
    )

    _, _, diffs = run_case("non_contiguous", non_contiguous_mask)
    if diffs[0].item() > 1e-5 or diffs[1].item() > 1e-5:
        raise AssertionError("Tensor-likes are not close!")


if __name__ == "__main__":
    main()
