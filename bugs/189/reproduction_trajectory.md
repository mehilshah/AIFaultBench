# Reproduction Trajectory — Bug 189: open_clip_torch

- **Bug report:** [https://github.com/mlfoundations/open_clip/issues/998](https://github.com/mlfoundations/open_clip/issues/998)
- **Repository:** mlfoundations/open_clip @ `49eac2f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the local venv with ./setup_env.sh.
2. Run ./run_repro.sh from the bug folder root.
3. Observe the UnpicklingError in repro_stderr.log while loading epoch_1.pt through open_clip.factory.load_state_dict().

## Observed behavior

- Running open_clip.factory.load_state_dict() on codebase/logs/repro_train1/checkpoints/epoch_1.pt under torch 2.6.0+cpu raises _pickle.UnpicklingError: Weights only load failed. The traceback in repro_stderr.log shows torch.load(..., weights_only=True) rejecting numpy._core.multiarray.scalar as an unsupported global.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
