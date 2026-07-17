# Reproduction Trajectory — Bug 395: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47836](https://github.com/vllm-project/vllm/issues/47836)
- **Repository:** vllm-project/vllm @ `b4cfbc24d33ca17bc764a75ffe749654654521c1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspect the bug report and local vLLM snapshot in `codebase/`.
2. Run `bash setup_env.sh`.
3. Run `bash run_repro.sh` and capture the traceback in `repro_stderr.log`.

## Observed behavior

- Running `bash run_repro.sh` exits with code 1 and captures a traceback ending in `IndexError: index 0 is out of bounds for dimension 0 with size 0` from the `expert_data = param.data if full_load else param.data[expert_id]` access in the routed-experts loader path.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
