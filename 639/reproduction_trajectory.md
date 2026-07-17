# Reproduction Trajectory — Bug 639: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/46798](https://github.com/vllm-project/vllm/issues/46798)
- **Repository:** vllm-project/vllm @ `63e161f2965e77b2c3ffcd159ce45b2157a21b43`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated CPU torch environment with `bash setup_env.sh`.
2. Ran `bash run_repro.sh`.
3. Observed the failing tensor-index operation in `repro.py`.

## Observed behavior

- Running `bash run_repro.sh` exits with code 1.
- The traceback ends at `TypeError: only integer tensors of a single element can be converted to an index`.
- This matches the upstream failure mode in the dummy-run/speculator indexing path.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
