# Reproduction Trajectory — Bug 284: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/14146](https://github.com/huggingface/diffusers/issues/14146)
- **Repository:** huggingface/diffusers @ `208704a27a6f362b67cd1a04fa1db0b98036d26f`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read `bug_report.txt` and the local `codebase/` implementation of `Krea2Pipeline` and `Krea2Transformer2DModel`.
2. Created a repro harness that follows the report's exact pipeline call sequence when a ROCm backend is present.
3. Ran `python3 repro.py` in this environment; it stopped at the ROCm gate because the host has CUDA PyTorch but no ROCm build.

## Observed behavior

- Running `python3 repro.py` on this host printed `{"cuda_available": true, "cuda_version": "13.0", "hip_version": null, "torch_version": "2.13.0+cu130"}` to stdout and exited with `blocking_reason: this repro requires a ROCm build of PyTorch on gfx1201; the local environment is not ROCm.` on stderr.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
python3 repro.py
```

## Why it does not reproduce on the reference machine

The reported failure is specific to ROCm/gfx1201, but this environment is not running a ROCm build of PyTorch, so the actual image-corruption behavior cannot be exercised here.
