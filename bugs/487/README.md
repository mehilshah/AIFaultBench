# Bug 487

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` pinned to `microsoft/DeepSpeed@5aa2d17dd71ab71d129719ba25e261a92f677d80`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro mode:
- This bundle uses a pure-Python state-machine reproducer for the ZeRO-2 IPG buffer index regression described in the issue.
- The full DeepSpeed multi-GPU CUDA trace could not be executed in this container because the local PyTorch install is broken and the issue requires a working CUDA/distributed stack.
