# Reproduction Trajectory — Bug 042: imagen-pytorch

- **Bug report:** [https://github.com/lucidrains/imagen-pytorch/issues/378](https://github.com/lucidrains/imagen-pytorch/issues/378)
- **Repository:** lucidrains/imagen-pytorch @ `0d34fe31df013d9c0be072062e224e0df10b1044`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated virtual environment.
2. Installed the pinned dependency set from requirements.txt.
3. Ran `python repro.py`, which imports `imagen_pytorch` from the local `codebase/` checkout.

## Observed behavior

- With beartype pinned to 0.18.0, `from imagen_pytorch import Unet, Imagen` fails during import with `BeartypeDecorHintParamDefaultViolation` because `Imagen.sample()` annotates `texts` as `List[str]` while defaulting it to `None`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
