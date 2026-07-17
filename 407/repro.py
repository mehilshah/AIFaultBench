#!/usr/bin/env python3
"""Minimal reproduction for the Hopper FLOPs table inconsistency."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "src" / "lightning" / "fabric" / "utilities" / "throughput.py"


def eval_node(node: ast.AST):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Dict):
        return {eval_node(key): eval_node(value) for key, value in zip(node.keys, node.values)}
    if isinstance(node, ast.Attribute):
        base = eval_node(node.value)
        if isinstance(base, str):
            return f"{base}.{node.attr}"
        raise TypeError(f"Unsupported attribute base: {ast.dump(node.value)}")
    if isinstance(node, ast.Name):
        return node.id
    raise TypeError(f"Unsupported AST node: {ast.dump(node)}")


def extract_cuda_flops(source: str):
    tree = ast.parse(source, filename=str(SOURCE))
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "_CUDA_FLOPS" for target in stmt.targets):
                return eval_node(stmt.value)
        if isinstance(stmt, ast.AnnAssign):
            if isinstance(stmt.target, ast.Name) and stmt.target.id == "_CUDA_FLOPS":
                return eval_node(stmt.value)
    raise RuntimeError("Could not locate _CUDA_FLOPS in throughput.py")


def fmt(value):
    return f"{value:.4g}"


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    cuda_flops = extract_cuda_flops(source)

    hopper = {name: values for name, values in cuda_flops.items() if name.startswith("h100") or name.startswith("h200")}
    float32_key = "torch.float32"
    float16_key = "torch.float16"
    bfloat16_key = "torch.bfloat16"

    h100_sxm = hopper["h100 sxm"]
    h100_nvl = hopper["h100 nvl"]
    h100_pcie = hopper["h100 pcie"]
    h200_sxm1 = hopper["h200 sxm1"]
    h200_nvl1 = hopper["h200 nvl1"]

    report = {
        "h100_sxm": {
            "float32": h100_sxm[float32_key],
            "float16": h100_sxm[float16_key],
            "bfloat16": h100_sxm[bfloat16_key],
        },
        "h100_nvl": {
            "float32": h100_nvl[float32_key],
            "float16": h100_nvl[float16_key],
            "bfloat16": h100_nvl[bfloat16_key],
        },
        "h100_pcie": {
            "float32": h100_pcie[float32_key],
            "float16": h100_pcie[float16_key],
            "bfloat16": h100_pcie[bfloat16_key],
        },
        "h200_sxm1": {
            "float32": h200_sxm1[float32_key],
            "float16": h200_sxm1[float16_key],
            "bfloat16": h200_sxm1[bfloat16_key],
        },
        "h200_nvl1": {
            "float32": h200_nvl1[float32_key],
            "float16": h200_nvl1[float16_key],
            "bfloat16": h200_nvl1[bfloat16_key],
        },
        "ratios_vs_h100_sxm": {
            "h100_nvl_float32": h100_nvl[float32_key] / h100_sxm[float32_key],
            "h100_pcie_float32": h100_pcie[float32_key] / h100_sxm[float32_key],
            "h200_sxm1_float32": h200_sxm1[float32_key] / h100_sxm[float32_key],
            "h200_nvl1_float32": h200_nvl1[float32_key] / h100_sxm[float32_key],
        },
    }

    print("Extracted Hopper FLOPs table from:")
    print(f"  {SOURCE}")
    print(json.dumps(report, indent=2, sort_keys=True))
    print()
    print("Observation:")
    print(
        "  H100 SXM and PCIE use the lower dense values, while H100 NVL and the H200 entries are in a different"
        " Hopper-tier band. The table mixes dense and sparse-style values across the H100/H200 variants."
    )
    print(
        "  Example: H100 NVL float32 = "
        f"{fmt(h100_nvl[float32_key])} vs H100 SXM float32 = {fmt(h100_sxm[float32_key])} "
        f"(ratio {h100_nvl[float32_key] / h100_sxm[float32_key]:.2f}x)."
    )
    print(
        "  H200 SXM1 float16 ratio vs H100 SXM is "
        f"{h200_sxm1[float16_key] / h100_sxm[float16_key]:.2f}x, and H200 NVL1 is "
        f"{h200_nvl1[float16_key] / h100_sxm[float16_key]:.2f}x."
    )


if __name__ == "__main__":
    main()
