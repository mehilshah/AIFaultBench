# Bug 365

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- The bug is in `codebase/deepspeed/runtime/superoffload/superoffload_stage3.py:53-77` and `:96-120`.
- `_create_fp16_sub_groups()` stores counts under local subgroup indices.
- `reduce_independent_p_g_buckets_and_remove_grads()` later looks up `sub_group_to_param_num` with the global bucket index from `grad_position`.
- `codebase/deepspeed/runtime/zero/stage3.py:1507-1517` shows that `grad_position` uses a global subgroup index across all optimizer groups.
- The harness in `repro.py` reproduces the mismatch and logs `KeyError: 2`.

Source summary:
- issue URL: `https://github.com/deepspeedai/DeepSpeed/issues/7905`
- commit hash: `5f7b687018bd1e0340c661859820fd97aa80a616`
- inferred library: `DeepSpeed`
- inferred library version: `0.18.7`
- bug report source: `bug_report.txt`
- codebase source: `microsoft/DeepSpeed@5f7b687018bd1e0340c661859820fd97aa80a616`
