#!/usr/bin/env python3
"""Static reproducer for the FlashInfer residual quant fusion bug.

The report describes a silent corruption caused by two residual quant fusion
patterns matching mixed BF16/FP32 RMSNorm inputs. In this checkout, the
relevant residual quant registrations do not include the dtype compatibility
guard that the neighboring non-residual quant registrations use.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "vllm" / "compilation" / "passes" / "fusion" / "allreduce_rms_fusion.py"

TARGET_CLASSES = {
    "AllReduceFusedRMSNormStaticQuantFP8Pattern": True,
    "AllReduceFusedAddRMSNormStaticQuantFP8Pattern": False,
    "AllReduceFusedRMSNormStaticQuantNVFP4Pattern": True,
    "AllReduceFusedAddRMSNormStaticQuantNVFP4Pattern": False,
}


@dataclass(frozen=True)
class Registration:
    class_name: str
    lineno: int
    has_extra_check: bool
    extra_check_repr: str | None


def _keyword_value_name(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parts: list[str] = []
        cur: ast.AST | None = node
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
        return ".".join(reversed(parts))
    return None


def _iter_register_calls(class_node: ast.ClassDef) -> Iterable[ast.Call]:
    for stmt in class_node.body:
        if not isinstance(stmt, ast.FunctionDef) or stmt.name != "register":
            continue
        for inner in ast.walk(stmt):
            if isinstance(inner, ast.Call):
                func = inner.func
                if isinstance(func, ast.Attribute) and func.attr == "register_replacement":
                    yield inner


def main() -> int:
    source_text = SOURCE.read_text()
    module = ast.parse(source_text, filename=str(SOURCE))

    classes = {
        node.name: node for node in module.body if isinstance(node, ast.ClassDef)
    }

    registrations: list[Registration] = []
    for class_name in TARGET_CLASSES:
        class_node = classes.get(class_name)
        if class_node is None:
            raise SystemExit(f"Missing class in source: {class_name}")
        calls = list(_iter_register_calls(class_node))
        if len(calls) != 1:
            raise SystemExit(
                f"Expected exactly one register_replacement call in {class_name}, "
                f"found {len(calls)}"
            )
        call = calls[0]
        extra_check = next((kw.value for kw in call.keywords if kw.arg == "extra_check"), None)
        registrations.append(
            Registration(
                class_name=class_name,
                lineno=call.lineno,
                has_extra_check=extra_check is not None,
                extra_check_repr=_keyword_value_name(extra_check),
            )
        )

    print(f"Source: {SOURCE}")
    print()
    print("Registration summary:")
    for reg in registrations:
        expected_extra_check = TARGET_CLASSES[reg.class_name]
        status = "OK" if reg.has_extra_check == expected_extra_check else "MISMATCH"
        print(
            f"- {reg.class_name}: line {reg.lineno}, "
            f"extra_check={reg.extra_check_repr!r}, expected={expected_extra_check} -> {status}"
        )

    buggy = [
        reg.class_name
        for reg in registrations
        if reg.class_name.startswith("AllReduceFusedAdd")
        and not reg.has_extra_check
    ]
    guarded = [
        reg.class_name
        for reg in registrations
        if reg.class_name.startswith("AllReduceFusedRMSNorm")
        and reg.has_extra_check
    ]

    print()
    print("Interpretation:")
    print(
        "- The residual quant patterns are missing the dtype guard, so a mixed "
        "BF16 input / FP32 norm-weight graph can still match."
    )
    print(
        "- The adjacent non-residual quant patterns do carry a guard, which "
        "matches the bug report's diagnosis."
    )
    print(f"- Buggy residual quant patterns: {buggy}")
    print(f"- Guarded non-residual quant patterns: {guarded}")

    if buggy and guarded:
        print()
        print("BUG REPRODUCED: the unsafe fusion registration is present in this checkout.")
        return 0

    raise SystemExit("Expected the unsafe residual quant registrations to be present.")


if __name__ == "__main__":
    raise SystemExit(main())
