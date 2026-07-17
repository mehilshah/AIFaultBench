# Bug 335

This folder is the reusable standardized benchmark input for the DeepSpeed SuperOffload single-GPU bug.

Relevant source files:
- `bug_report.txt`
- `codebase/deepspeed/runtime/superoffload/superoffload_stage3.py`
- `codebase/deepspeed/runtime/zero/stage3.py`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- `SuperOffloadOptimizer_Stage3._create_fp16_sub_groups()` returns early for a single subgroup and never fills `sub_group_to_param_num`.
- `reduce_independent_p_g_buckets_and_remove_grads()` then indexes `self.sub_group_to_param_num[self._cur_bucket_index]` on the first gradient bucket, which raises `KeyError: 0`.
- The included repro is a pure-Python harness that mirrors the relevant control flow and makes the failure deterministic in this folder.

Run the repro with:
`bash run_repro.sh`
