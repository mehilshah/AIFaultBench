# Reproduction Trajectory — Bug 424: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7830](https://github.com/deepspeedai/DeepSpeed/issues/7830)
- **Repository:** microsoft/DeepSpeed @ `0ccb2bb6746bd8c5294ea9dd4761d72c8d7f48e7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean Python 3.12 virtual environment and install the CPU torch build plus minimal dependencies from `requirements.txt`.
2. Load `codebase/deepspeed/runtime/utils.py` from the checked-out DeepSpeed source using minimal import stubs so the repro stays focused on the target helper.
3. Register a backward hook on a leaf parameter and monkeypatch `torch.autograd.graph._get_grad_fn_or_grad_acc` to reject calls made with grad mode disabled.
4. Run `loss.backward()` and observe the unpatched DeepSpeed helper fail inside the hook.

## Observed behavior

- Running `bash run_repro.sh` exits with code 1. The traceback shows `deepspeed.runtime.utils.count_used_parameters_in_backward()` calling `torch.autograd.graph._get_grad_fn_or_grad_acc` from a backward hook while grad mode is disabled, which triggers `RuntimeError: grad mode must be enabled for grad-acc lookup`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
