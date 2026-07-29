# Reproduction Trajectory — Bug 715: langflow

- **Bug report:** [https://github.com/langflow-ai/langflow/issues/12228](https://github.com/langflow-ai/langflow/issues/12228)
- **Repository:** langflow-ai/langflow @ `38eed35ffb70bda2f9ee02b84eaa311d537ae5ae`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and completed checkout of the requested historical commit.
2. Verified that `src/backend/base/pyproject.toml` declares `litellm>=1.60.2,<2.0.0` without `[proxy]`, while its lockfile resolves LiteLLM 1.80.0.
3. Ran `bash setup_env.sh` to install LiteLLM 1.80.0 and the base dependencies that Langflow already supplies to LiteLLM's proxy import, intentionally excluding `litellm[proxy]`.
4. Ran `bash run_repro.sh`. The script reads the pinned metadata and then performs LiteLLM's local proxy-module import only; it makes no model or network call.

## Observed behavior

- `run_repro.sh` exited with status 1.
- LiteLLM raised `ImportError: Missing dependency No module named 'apscheduler'. Run \`pip install 'litellm[proxy]'\``.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
