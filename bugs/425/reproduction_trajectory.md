# Reproduction Trajectory — Bug 425: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47418](https://github.com/vllm-project/vllm/issues/47418)
- **Repository:** vllm-project/vllm @ `25fcb65d51deef0026aa34e6067703da4a91f956`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal DSpark reproduction harness in repro.py that mirrors the buggy attribute access.
2. Ran bash run_repro.sh.
3. Observed the expected AttributeError in repro_stderr.log.

## Observed behavior

- Running `bash run_repro.sh` raises `AttributeError: 'DSparkDeepseekV4ForCausalLM' object has no attribute 'draft_id_to_target_id'`, matching the failure in the bug report.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
