# Bug 469

Reproduction bundle for:

- https://github.com/vllm-project/vllm/issues/47300
- title: Gemma4 gibberish output for long inputs with images on SM90 FlashAttn4

## What this bundle does

- Recreates the exact multimodal conversation shape from the bug report.
- Generates the long NIAH-style final turn used to trigger the regression.
- Provides a server/client repro path for `vllm serve` with `FLASH_ATTN` and `TRITON_ATTN`.
- Detects the local hardware blocker when SM90/H100 or a running vLLM server is missing.

## Files

- `repro.py`: builds the prompt and, when a server is available, sends the conversation.
- `run_repro.sh`: gated launcher for the real repro.
- `setup_env.sh`: installs the Python dependencies and local vLLM source tree.
- `requirements.txt`: client-side Python dependencies.
- `manifest.json`: standardized metadata for this bug folder.
- `reproduction.json`: final verdict from the local run.
- `repro_stdout.log` / `repro_stderr.log`: captured command output.

## Local verdict

This machine does not provide the H100/SM90 environment described in the bug report, so the full accuracy regression cannot be exercised here.

The repro harness still emits the exact request payload and the server launch command needed on a matching system.
