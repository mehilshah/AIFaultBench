# Reproduction Trajectory — Bug 467: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1207](https://github.com/huggingface/accelerate/issues/1207)
- **Repository:** huggingface/accelerate @ `901ab69a1601ba1a7c63523356c5acb1d66b7ea9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtual environment and installed torch 2.6.0+cpu plus the pinned accelerate source from codebase/.
2. Executed repro.py via run_repro.sh.
3. Observed that accelerator.unwrap_model(accelerator.prepare(model)) returned the OptimizedModule wrapper unchanged instead of the original ToyModel.

## Observed behavior

- Running Accelerator(dynamo_backend='eager') against the pinned accelerate source produced prepared_type=torch._dynamo.eval_frame.OptimizedModule and unwrapped_type=torch._dynamo.eval_frame.OptimizedModule, with is_same_object=True. stderr also reported: BUG: unwrap_model returned the compiled wrapper instead of the original module.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
