# Reproduction Trajectory — Bug 365: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7905](https://github.com/deepspeedai/DeepSpeed/issues/7905)
- **Repository:** microsoft/DeepSpeed @ `5f7b687018bd1e0340c661859820fd97aa80a616`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspect `codebase/deepspeed/runtime/superoffload/superoffload_stage3.py` and `codebase/deepspeed/runtime/zero/stage3.py` to confirm the subgroup bookkeeping mismatch.
2. Run `bash run_repro.sh` to execute the standalone harness in `repro.py`.
3. Observe the logged `KeyError: 2` in `repro_stdout.log`.

## Observed behavior

- Running `bash run_repro.sh` prints `sub_group_to_param_num: {0: 1, 1: 1}` for four global subgroups and then fails at the third subgroup with `KeyError: 2`, matching the bug report's bad global-vs-local subgroup lookup.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
