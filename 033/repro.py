#!/usr/bin/env python3
"""Minimal repro for the ConvSE3 multiplication error.

The upstream issue reports a failure in the `ConvSE3` path when a separate
degree-1 input type is introduced. The runtime error is raised by a batched
matrix multiplication whose second operand has degree-1 width 3 while the
kernel expects width 1.

This script reproduces the exact error message without requiring the full DGL
stack or dataset download.
"""

from __future__ import annotations

import sys

import torch


def main() -> int:
    num_edges = 8910

    # Mirrors the self-interaction branch in
    # se3_transformer/model/layers/convolution.py:
    #   dst_features = node_feats[str(degree_out)][dst]
    #   kernel_self @ dst_features
    #
    # The degree-1 slot is shaped like a vector representation, so the batch
    # dimension is 3. The kernel expects a scalar-width input channel.
    kernel_self = torch.zeros(1, 1)
    dst_features = torch.zeros(num_edges, 3, 1)

    print("Running ConvSE3-style self interaction")
    print(f"kernel_self.shape={tuple(kernel_self.shape)}")
    print(f"dst_features.shape={tuple(dst_features.shape)}")
    print("About to execute kernel_self @ dst_features")

    # This line reproduces the reported RuntimeError.
    _ = kernel_self @ dst_features

    print("Unexpected success")
    return 0


if __name__ == "__main__":
    sys.exit(main())
