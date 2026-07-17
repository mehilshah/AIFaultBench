# Bug 424

This folder is the reusable standardized benchmark input for DeepSpeed issue
`#7830`.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction approach:
- imports the checked-out DeepSpeed source from `codebase/`
- monkeypatches `torch.autograd.graph._get_grad_fn_or_grad_acc` to fail when
  called with grad mode disabled
- triggers `deepspeed.runtime.utils.count_used_parameters_in_backward()` from a
  backward hook, which is the code path fixed in `bffaf457`

Source summary:
- issue URL: `https://github.com/deepspeedai/DeepSpeed/issues/7830`
- codebase commit: `0ccb2bb6746bd8c5294ea9dd4761d72c8d7f48e7`
- fixing commit: `bffaf457457e08a003b0ce8ed371d49678a77d57`
