# Reproduction Trajectory — Bug 700: smolagents

- **Bug report:** [https://github.com/huggingface/smolagents/issues/1767](https://github.com/huggingface/smolagents/issues/1767)
- **Repository:** huggingface/smolagents @ `83ff2f7ed09788e130965349929f8bd5152e507e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` to clone the repository and check out the pinned buggy commit.
2. Created `.venv` and installed the exact dependencies in `requirements.txt` plus the local checkout; `ddgs`, an optional `toolkit` dependency, was intentionally not installed.
3. Ran `bash run_repro.sh`, which instantiates `DuckDuckGoSearchTool` directly, avoiding agent execution, model clients, and all runtime network calls.

## Observed behavior

- `run_repro.sh` exited with status 1 after `DuckDuckGoSearchTool()` raised `ImportError: You must install package \`ddgs\` to run this tool: for instance run \`pip install ddgs\`.`
- The script also asserted the chained cause was `ModuleNotFoundError: No module named 'ddgs'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
