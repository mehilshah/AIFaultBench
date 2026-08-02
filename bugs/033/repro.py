#!/usr/bin/env python3
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
