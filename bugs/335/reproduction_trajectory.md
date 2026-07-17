# Reproduction Trajectory — Bug 335: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7925](https://github.com/deepspeedai/DeepSpeed/issues/7925)
- **Repository:** microsoft/DeepSpeed @ `62c3e6d8d7b28f6554548e87a5fdc8f05f0fbbb8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a single dummy parameter and split it with `_create_fp16_sub_groups`; it returns 1 subgroup(s).
2. Observe that `sub_group_to_param_num` stays empty: {}.
3. Call `reduce_independent_p_g_buckets_and_remove_grads` for that parameter and hit `KeyError: 0`.

## Observed behavior

- KeyError reproduced as expected: KeyError(0). After `_create_fp16_sub_groups`, sub_group_to_param_num={}; the first bucket reduction set _cur_bucket_index=0 and then indexed the empty map.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
