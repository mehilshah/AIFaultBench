# Reproduction Trajectory — Bug 658: langchain

- **Bug report:** [https://github.com/langchain-ai/langchain/issues/38741](https://github.com/langchain-ai/langchain/issues/38741)
- **Repository:** langchain-ai/langchain @ `bc1540084b19eda40a44885d8eaa0a5804b061c8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` twice. Both attempts ended before checkout and left an unborn Git repository, making the full checkout impractically large for this environment.
2. Used the allowed released-package fallback and created `.venv` with the pinned issue-era `langchain-fireworks==1.4.4` dependency set.
3. Ran `repro.py`, which patches `langchain_fireworks.llms.ClientSession` with an offline session returning a deterministic HTTP 400 response whose async `text()` returns `{"error":"invalid model"}`.
4. Executed `bash run_repro.sh` and captured its stdout and stderr.

## Observed behavior

- `Fireworks._acall` raised `ValueError: Fireworks received an invalid payload: <bound method _Resp.text of <fake Fireworks 400 response>>`.
- The actual fake response body, `{"error":"invalid model"}`, was absent. `repro.py` asserts both conditions, prints the observation, and exits non-zero to mark the buggy behavior.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
