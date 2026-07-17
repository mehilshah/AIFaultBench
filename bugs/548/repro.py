#!/usr/bin/env python3
"""Source-level reproduction check for the pause_generation multimodal cache bug."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "vllm" / "v1" / "engine" / "async_llm.py"


def find_method_source(tree: ast.AST, class_name: str, method_name: str, source: str):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, ast.AsyncFunctionDef) and child.name == method_name:
                    return child.lineno, child.end_lineno, ast.get_source_segment(
                        source, child
                    )
    raise AssertionError(f"Could not find {class_name}.{method_name} in {SOURCE}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))

    pause_lineno, pause_end_lineno, pause_src = find_method_source(
        tree, "AsyncLLM", "pause_generation", source
    )
    reset_lineno, reset_end_lineno, reset_src = find_method_source(
        tree, "AsyncLLM", "reset_mm_cache", source
    )

    assert pause_src is not None
    assert reset_src is not None

    pause_clear = "await self.renderer.clear_mm_cache_async()" in pause_src
    pause_engine = "await self.engine_core.pause_scheduler_async(" in pause_src
    reset_clear = "await self.renderer.clear_mm_cache_async()" in reset_src
    reset_engine = "await self.engine_core.reset_mm_cache_async()" in reset_src

    assert pause_clear, "pause_generation() does not clear the renderer cache"
    assert pause_engine, "pause_generation() does not call pause_scheduler_async()"
    assert reset_clear, "reset_mm_cache() does not clear the renderer cache"
    assert reset_engine, "reset_mm_cache() does not clear the engine cache"

    pause_clear_pos = pause_src.index("await self.renderer.clear_mm_cache_async()")
    pause_engine_pos = pause_src.index("await self.engine_core.pause_scheduler_async(")
    reset_clear_pos = reset_src.index("await self.renderer.clear_mm_cache_async()")
    reset_engine_pos = reset_src.index("await self.engine_core.reset_mm_cache_async()")

    assert pause_clear_pos < pause_engine_pos, (
        "pause_generation() still has the renderer cache clear after the engine "
        "pause call"
    )
    assert reset_clear_pos < reset_engine_pos, (
        "reset_mm_cache() unexpectedly changed cache ordering"
    )

    print(f"source: {SOURCE}")
    print(f"pause_generation lines: {pause_lineno}-{pause_end_lineno}")
    print(f"reset_mm_cache lines: {reset_lineno}-{reset_end_lineno}")
    print("pause_generation() clears frontend and backend state in this checkout.")
    print("reset_mm_cache() also clears frontend and backend state.")
    print("RESULT: non-reproducible here; the reported bug is already fixed.")


if __name__ == "__main__":
    main()
