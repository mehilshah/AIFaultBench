# Bug 361

This folder is the reusable standardized benchmark input for the Transformers DeepSpeed SP loss aggregation issue.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run the repro with:
`bash run_repro.sh`

Current result:
- The source contains the reported Python conditional in `src/transformers/integrations/deepspeed.py:738-744`.
- The local CUDA probe runs on `torch==2.7.1+cu128`, but the isolated single-process benchmark does not show a measurable host sync for the branch.
- The exact distributed sequence-parallel `all_gather` setup from the issue is not available in this folder, so the Nsight-observed behavior is not reproduced here.
