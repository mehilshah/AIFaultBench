# Reproduction Trajectory — Bug 364: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/3087](https://github.com/huggingface/accelerate/issues/3087)
- **Repository:** huggingface/accelerate @ `5ad982ac517b6e686be6461242313c55755a9dbf`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a CPU-only virtual environment with `bash setup_env.sh`.
2. Run `bash run_repro.sh`.
3. Observe the traceback from `load_checkpoint_and_dispatch()` -> `find_tied_parameters()` -> `_get_named_parameters()`.
4. Confirm the crash is the reported `NoneType._parameters` failure.

## Observed behavior

- Running `bash run_repro.sh` inside the isolated venv prints the model modules including `broken: None`, then fails in `accelerate.utils.modeling._get_named_parameters()` with `AttributeError: 'NoneType' object has no attribute '_parameters'` while `load_checkpoint_and_dispatch()` calls `find_tied_parameters()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
