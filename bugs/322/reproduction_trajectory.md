# Reproduction Trajectory — Bug 322: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2663](https://github.com/huggingface/pytorch-image-models/issues/2663)
- **Repository:** huggingface/pytorch-image-models @ `9171d82efc525766706a00cd3d1f292af12f910a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh virtual environment and install the local package dependencies from `requirements.txt`.
2. Run `python -W error repro.py` from the standardized bug folder.
3. The import fails while loading `timm.models.hrnet` because `@torch.jit.interface` raises a deprecation warning that is promoted to an exception.

## Observed behavior

- Running `python -W error repro.py` in a clean venv fails during `import timm` with `DeprecationWarning: `torch.jit.interface` is deprecated. Please use `torch.compile` instead.` The traceback points to `codebase/timm/models/hrnet.py:521`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
