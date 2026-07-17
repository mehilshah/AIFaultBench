# Reproduction Trajectory — Bug 489: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2546](https://github.com/huggingface/pytorch-image-models/issues/2546)
- **Repository:** huggingface/pytorch-image-models @ `b2034bb6c57fa6b41fda7398140bf21405361df7`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a clean Python virtual environment.
2. Install CPU wheels for torch/torchvision plus `huggingface_hub`, `safetensors`, `numpy`, and `pyyaml`.
3. Run `python repro.py` with the local `codebase/` on `PYTHONPATH`.
4. Observe that `timm.create_model('lsnet_t')` fails before the custom package is imported, then succeeds after registration.

## Observed behavior

- Running `bash run_repro.sh` in an isolated venv produced `before_import_error=RuntimeError: Unknown model (lsnet_t)`.
- The same run then imported a local package that registers `lsnet_t`, after which `registered_after_import=True` and `after_import_model=LSNetTiny`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported failure is caused by the custom architecture not being registered in the Python process before `create_model()` is called. In this codebase, `timm` only knows model names after their module has been imported and decorated with `@register_model`.
