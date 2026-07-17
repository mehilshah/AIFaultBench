#!/usr/bin/env python3
"""Minimal reproduction for the RequestOutput / set_list_to_stack bug."""

from __future__ import annotations

import dataclasses
import importlib.util
import pathlib
import sys
import traceback
import types

from tensordict import set_list_to_stack


ROOT = pathlib.Path(__file__).resolve().parent
DATATYPES_DIR = ROOT / "codebase" / "torchtune" / "dev" / "rl" / "datatypes"


def _install_fake_vllm() -> None:
    """Provide the small subset of vLLM needed by the dataclass bridge."""

    vllm_mod = types.ModuleType("vllm")
    outputs_mod = types.ModuleType("vllm.outputs")

    @dataclasses.dataclass
    class CompletionOutput:
        text: str = ""
        token_ids: list[int] = dataclasses.field(default_factory=list)
        logprobs: list | None = None

    outputs_mod.CompletionOutput = CompletionOutput
    vllm_mod.outputs = outputs_mod
    sys.modules["vllm"] = vllm_mod
    sys.modules["vllm.outputs"] = outputs_mod


def _install_package_scaffold() -> None:
    """Create the parent package chain needed for relative imports."""

    for name in [
        "torchtune",
        "torchtune.dev",
        "torchtune.dev.rl",
        "torchtune.dev.rl.datatypes",
    ]:
        module = types.ModuleType(name)
        module.__path__ = []
        sys.modules[name] = module


def _load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _build_request_output_class():
    _install_fake_vllm()
    _install_package_scaffold()
    _load_module(
        "torchtune.dev.rl.datatypes.vllm_completion_output",
        DATATYPES_DIR / "vllm_completion_output.py",
    )
    request_output_mod = _load_module(
        "torchtune.dev.rl.datatypes.request_output",
        DATATYPES_DIR / "request_output.py",
    )
    return request_output_mod.RequestOutput


@dataclasses.dataclass
class FakeRequest:
    request_id: str
    prompt: str
    prompt_token_ids: list[int]
    prompt_logprobs: list | None
    outputs: list
    finished: bool
    metrics: dict
    lora_request: None = None
    encoder_prompt: None = None
    encoder_prompt_token_ids: None = None
    num_cached_tokens: int = 0


def _make_request():
    completion_output = sys.modules[
        "vllm.outputs"
    ].CompletionOutput(
        token_ids=[10, 11],
        logprobs=[{10: {"logprob": -1.0}}, {11: {"logprob": -2.0}}],
    )
    return FakeRequest(
        request_id="1",
        prompt="hello",
        prompt_token_ids=[1, 2],
        prompt_logprobs=None,
        outputs=[completion_output],
        finished=True,
        metrics={},
    )


def _exercise_case(RequestOutput, enabled: bool) -> tuple[bool, str]:
    set_list_to_stack(enabled).set()
    try:
        RequestOutput.from_request_output([_make_request()])
        return True, "ok"
    except Exception as exc:  # noqa: BLE001
        traceback.print_exc()
        return False, f"{type(exc).__name__}: {exc}"


def main() -> int:
    RequestOutput = _build_request_output_class()

    baseline_ok, baseline_msg = _exercise_case(RequestOutput, enabled=False)
    print(f"set_list_to_stack(False): {baseline_msg}")

    bug_ok, bug_msg = _exercise_case(RequestOutput, enabled=True)
    print(f"set_list_to_stack(True): {bug_msg}")

    if not baseline_ok:
        print("Baseline without list-to-stack should succeed, but it did not.")
        return 2

    if bug_ok:
        print("BUG NOT REPRODUCED")
        return 3

    print("BUG REPRODUCED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
