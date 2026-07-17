# Reproduction Trajectory — Bug 350: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7913](https://github.com/deepspeedai/DeepSpeed/issues/7913)
- **Repository:** microsoft/DeepSpeed @ `5f7b687018bd1e0340c661859820fd97aa80a616`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean Python 3.12 virtual environment and install the bundle requirements.
2. Load the local DeepSpeed ZeRO linear implementation from codebase/deepspeed/runtime/zero/linear.py with minimal deepspeed shims.
3. Call torch.func.grad_and_value on a function that uses LinearFunctionForZeroStage3 through zero3_linear_wrap.
4. Observe the RuntimeError complaining that autograd.Function must override setup_context.

## Observed behavior

- Running ./run_repro.sh exited with status 1.
- repro_stdout.log contains the expected RuntimeError: "In order to use an autograd.Function with functorch transforms (vmap, grad, jvp, jacrev, ...), it must override the setup_context staticmethod."
- The failure was triggered while calling torch.func.grad_and_value on code loaded from codebase/deepspeed/runtime/zero/linear.py.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
