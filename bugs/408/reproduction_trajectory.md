# Reproduction Trajectory — Bug 408: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1546](https://github.com/huggingface/accelerate/issues/1546)
- **Repository:** huggingface/accelerate @ `62357f218f72cce88b8e086cc372b15c119b590b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv with torch 2.13.0+cpu, tensorboard, numpy, packaging, psutil, and pyyaml.
2. Ran repro.py against codebase/src from the pinned Accelerate checkout.
3. Compared TensorBoard event files for a tensor value and a float control value.
4. Observed that the tensor case wrote no scalar summary while the float case wrote the expected scalar.

## Observed behavior

- In the local Accelerate checkout, logging torch.tensor(1.0) to TensorBoard produced no 'loss' scalar events, while logging the float 1.0 produced [('loss', step=1, value=1.0)]. The captured stdout shows 'BUG_REPRODUCED: tensor input is silently ignored while float input is logged.'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
