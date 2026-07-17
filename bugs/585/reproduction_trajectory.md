# Reproduction Trajectory — Bug 585: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/996](https://github.com/huggingface/accelerate/issues/996)
- **Repository:** huggingface/accelerate @ `b22f088ff662de748cf3f97c7ad8bf5a6dd6a7b9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the venv with ./setup_env.sh.
2. Run ./run_repro.sh, which launches accelerate with a patched torch.distributed.run.run that raises RuntimeError.
3. Observe that the inner `accelerate launch` command reports return code 0 instead of propagating the failure.

## Observed behavior

- Injected a RuntimeError into torch.distributed.run.run via sitecustomize; `accelerate launch --multi_gpu --num_processes 2` still printed an injected-failure marker and exited with code 0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
