#!/usr/bin/env python3
"""Self-contained reproduction of the duplicated value-rotation bug.

The source implementation rotates values once before the weighted sum and then rotates the
already rotated tensor again inside the `einsum` call. With identity attention, the correct
behavior should reconstruct the original values after the reverse rotation. The buggy path
returns a rotated tensor instead.
"""

from __future__ import annotations

import json
import math
from typing import List


Vector = List[float]
Tensor = List[Vector]


def rotate_forward(vec: Vector, position: int, thetas: Vector) -> Vector:
    half = len(vec) // 2
    left = vec[:half]
    right = vec[half:]
    rotated: Vector = []
    for idx in range(half):
        angle = position * thetas[idx]
        c = math.cos(angle)
        s = math.sin(angle)
        rotated.append(left[idx] * c - right[idx] * s)
    for idx in range(half):
        angle = position * thetas[idx]
        c = math.cos(angle)
        s = math.sin(angle)
        rotated.append(right[idx] * c + left[idx] * s)
    return rotated


def rotate_reverse(vec: Vector, position: int, thetas: Vector) -> Vector:
    half = len(vec) // 2
    left = vec[:half]
    right = vec[half:]
    rotated: Vector = []
    for idx in range(half):
        angle = position * thetas[idx]
        c = math.cos(angle)
        s = math.sin(angle)
        rotated.append(left[idx] * c + right[idx] * s)
    for idx in range(half):
        angle = position * thetas[idx]
        c = math.cos(angle)
        s = math.sin(angle)
        rotated.append(right[idx] * c - left[idx] * s)
    return rotated


def matmul_identity(values: Tensor) -> Tensor:
    return [row[:] for row in values]


def max_abs_diff(a: Tensor, b: Tensor) -> float:
    return max(abs(x - y) for row_a, row_b in zip(a, b) for x, y in zip(row_a, row_b))


def format_tensor(t: Tensor) -> str:
    return json.dumps([[round(v, 8) for v in row] for row in t], indent=2)


def main() -> int:
    # A small example with two rotary pairs, matching the split-half pairing in the source.
    thetas = [0.37, 0.73]
    values: Tensor = [
        [1.0, 2.0, 3.0, 4.0],
        [5.0, 6.0, 7.0, 8.0],
        [9.0, 10.0, 11.0, 12.0],
    ]

    # Identity attention isolates the value path.
    attn = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]

    # Correct path: rotate once before the weighted sum, then reverse-rotate the result.
    rotated_once = [rotate_forward(v, pos, thetas) for pos, v in enumerate(values)]
    weighted_once = matmul_identity(rotated_once)
    correct = [rotate_reverse(v, pos, thetas) for pos, v in enumerate(weighted_once)]

    # Buggy path from the source: rotate before attention, then rotate again inside the einsum.
    rotated_twice_input = [rotate_forward(v, pos, thetas) for pos, v in enumerate(values)]
    rotated_twice = [rotate_forward(v, pos, thetas) for pos, v in enumerate(rotated_twice_input)]
    weighted_twice = matmul_identity(rotated_twice)
    buggy = [rotate_reverse(v, pos, thetas) for pos, v in enumerate(weighted_twice)]

    diff_buggy_vs_input = max_abs_diff(buggy, values)
    diff_correct_vs_input = max_abs_diff(correct, values)
    diff_buggy_vs_correct = max_abs_diff(buggy, correct)

    print("Identity attention matrix:")
    print(format_tensor(attn))
    print()
    print("Input values:")
    print(format_tensor(values))
    print()
    print("Correct output (single value rotation):")
    print(format_tensor(correct))
    print()
    print("Buggy output (double value rotation):")
    print(format_tensor(buggy))
    print()
    print(f"max_abs_diff(correct, input) = {diff_correct_vs_input:.12g}")
    print(f"max_abs_diff(buggy, input) = {diff_buggy_vs_input:.12g}")
    print(f"max_abs_diff(buggy, correct) = {diff_buggy_vs_correct:.12g}")

    if diff_buggy_vs_correct <= 1e-9:
        print("Unexpected: buggy and correct outputs match.")
        return 1

    if diff_correct_vs_input > 1e-9:
        print("Unexpected: the correct output should reconstruct the input under identity attention.")
        return 1

    print()
    print("Conclusion: the current implementation applies the value rotary embedding twice.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
