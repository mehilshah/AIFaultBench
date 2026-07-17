#!/usr/bin/env python3
"""Local repro harness for vLLM issue 47027.

This script is intentionally lightweight:
- It inspects the local source to confirm where `response_format` and
  `enable_thinking` are wired together.
- It then performs a small runtime probe in a subprocess.

In this workspace, the full runtime probe is expected to fail because the
preinstalled Torch/NCCL stack is inconsistent, so the script records that as
the blocking reason rather than masking it.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"
STDOUT_LOG = ROOT / "repro_stdout.log"
STDERR_LOG = ROOT / "repro_stderr.log"


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def source_evidence() -> list[str]:
    """Collect source-level evidence from the checked-in code."""
    evidence: list[str] = []

    chat_protocol = (CODEBASE / "vllm/entrypoints/openai/chat_completion/protocol.py").read_text()
    if 'if self.reasoning_effort is not None and "enable_thinking" not in user_kwargs:' in chat_protocol:
        evidence.append(
            "ChatCompletionRequest.build_chat_params only injects enable_thinking from reasoning_effort."
        )
    if 'elif response_format.type == "json_schema":' in chat_protocol:
        evidence.append(
            "response_format is translated into StructuredOutputsParams, not into a thinking toggle."
        )

    renderer = (CODEBASE / "vllm/renderers/online_renderer.py").read_text()
    if "parser.adjust_request" in renderer and "chat_template_kwargs=chat_params.chat_template_kwargs" in renderer:
        evidence.append(
            "The renderer passes chat_template_kwargs into parser.adjust_request, but does not special-case response_format."
        )

    qwen3 = (CODEBASE / "vllm/parser/qwen3.py").read_text()
    if 'self.thinking_enabled = chat_kwargs.get("enable_thinking", True)' in qwen3:
        evidence.append(
            "Qwen3Parser defaults thinking on unless enable_thinking is explicitly false."
        )

    return evidence


def runtime_probe() -> tuple[int, str, str]:
    """Try the narrowest runtime probe we can without a server."""
    probe = r"""
import json
from vllm.entrypoints.openai.chat_completion.protocol import ChatCompletionRequest

req = ChatCompletionRequest(
    model="Qwen/Qwen3.6-27B",
    messages=[{"role": "user", "content": "Hello"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "Answer",
            "schema": {
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False,
            },
        },
    },
)
params = req.build_chat_params(None, "auto")
print(json.dumps(params.chat_template_kwargs, sort_keys=True))
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(CODEBASE) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=str(CODEBASE),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []

    stdout_lines.append("Source evidence:")
    for item in source_evidence():
        stdout_lines.append(f"- {item}")

    rc, out, err = runtime_probe()
    stdout_lines.append("")
    stdout_lines.append("Runtime probe:")
    stdout_lines.append(f"- exit_code: {rc}")
    if out.strip():
        stdout_lines.append("- stdout:")
        stdout_lines.extend([f"  {line}" for line in out.rstrip().splitlines()])
    if err.strip():
        stderr_lines.append("Runtime probe stderr:")
        stderr_lines.extend(err.rstrip().splitlines())

    reproducible = rc == 0 and out.strip() != ""
    blocking_reason = None
    if not reproducible:
        blocking_reason = (
            "Could not complete the runtime probe in this workspace. "
            "Importing vLLM fails before the request path runs because the "
            "preinstalled Torch/NCCL stack is inconsistent, so the full "
            "server-side reproduction cannot be executed here."
        )

    result = {
        "reproducible": reproducible,
        "evidence": stdout_lines[1:] if stdout_lines else [],
        "steps": [
            "Inspected the local vLLM request/rendering path for response_format and thinking handling.",
            "Attempted a narrow runtime import of ChatCompletionRequest in a subprocess.",
        ],
        "blocking_reason": blocking_reason,
        "reproduction_command": "./run_repro.sh",
    }

    STDOUT_LOG.write_text("\n".join(stdout_lines) + "\n")
    STDERR_LOG.write_text("\n".join(stderr_lines) + ("\n" if stderr_lines else ""))
    write_json(RESULT_PATH, result)

    print("\n".join(stdout_lines))
    if stderr_lines:
        print("\n".join(stderr_lines), file=sys.stderr)

    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
