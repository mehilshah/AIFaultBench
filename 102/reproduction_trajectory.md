# Reproduction Trajectory — Bug 102: vector-quantize-pytorch

- **Bug report:** [https://github.com/lucidrains/vector-quantize-pytorch/issues/191](https://github.com/lucidrains/vector-quantize-pytorch/issues/191)
- **Repository:** lucidrains/vector-quantize-pytorch @ `ac5d63174dd234ab75259a68a4ab246774863f6e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the local venv with `bash setup_env.sh`.
2. Run `bash run_repro.sh` to instantiate `ResidualSimVQ` and call its forward method.
3. Observe the traceback ending in `NameError: name 'return_loss' is not defined`.

## Observed behavior

- Running ResidualSimVQ with quantize_dropout=True raises NameError: name 'return_loss' is not defined at codebase/vector_quantize_pytorch/residual_sim_vq.py:153.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
