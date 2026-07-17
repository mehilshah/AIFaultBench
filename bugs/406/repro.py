#!/usr/bin/env python3
"""Source-level repro for diffusers issue 13979.

The pinned codebase defines `Ideogram4LoraLoaderMixin` but `Ideogram4ModularPipeline`
does not inherit it, so `load_lora_weights()` is missing from the modular pipeline API.
This script inspects the vendored source directly to avoid unrelated local torch import
failures in the execution environment.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase" / "src" / "diffusers"


def read_ast(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def class_bases(tree: ast.AST, class_name: str) -> list[str]:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            bases: list[str] = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Attribute):
                    parts = []
                    current = base
                    while isinstance(current, ast.Attribute):
                        parts.append(current.attr)
                        current = current.value
                    if isinstance(current, ast.Name):
                        parts.append(current.id)
                    bases.append(".".join(reversed(parts)))
                else:
                    bases.append(ast.dump(base, include_attributes=False))
            return bases
    raise RuntimeError(f"Class {class_name} not found in {tree}")


def has_method(tree: ast.AST, class_name: str, method_name: str) -> bool:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return any(isinstance(child, ast.FunctionDef) and child.name == method_name for child in node.body)
    raise RuntimeError(f"Class {class_name} not found")


def main() -> int:
    ideogram_path = CODEBASE / "modular_pipelines" / "ideogram4" / "modular_pipeline.py"
    flux_path = CODEBASE / "modular_pipelines" / "flux" / "modular_pipeline.py"
    lora_path = CODEBASE / "loaders" / "lora_pipeline.py"

    ideogram_tree = read_ast(ideogram_path)
    flux_tree = read_ast(flux_path)
    lora_tree = read_ast(lora_path)

    ideogram_bases = class_bases(ideogram_tree, "Ideogram4ModularPipeline")
    flux_bases = class_bases(flux_tree, "FluxModularPipeline")
    lora_has_method = has_method(lora_tree, "Ideogram4LoraLoaderMixin", "load_lora_weights")

    result = {
        "ideogram4_modular_pipeline_bases": ideogram_bases,
        "flux_modular_pipeline_bases": flux_bases,
        "ideogram4_lora_loader_has_load_lora_weights": lora_has_method,
        "missing_lora_mixin": "Ideogram4LoraLoaderMixin" not in ideogram_bases,
    }

    print(json.dumps(result, indent=2, sort_keys=True))

    if "Ideogram4LoraLoaderMixin" not in ideogram_bases:
        print(
            "FAIL: Ideogram4ModularPipeline does not inherit Ideogram4LoraLoaderMixin, so "
            "load_lora_weights() is not available.",
            file=sys.stderr,
        )
        return 1

    print("PASS: Ideogram4ModularPipeline exposes load_lora_weights().")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
