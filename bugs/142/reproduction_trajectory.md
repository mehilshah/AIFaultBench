# Reproduction Trajectory — Bug 142: safetensors

- **Bug report:** [https://github.com/huggingface/safetensors/issues/492](https://github.com/huggingface/safetensors/issues/492)
- **Repository:** huggingface/safetensors @ `079781f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean virtual environment and installed safetensors==0.4.3 from the bundled requirements.
2. Imported safetensors.SafetensorError and instantiated the exception.
3. Serialized the exception with multiprocessing.reduction.ForkingPickler.dumps to match the dataloader worker pickling path.
4. Observed a PicklingError instead of a pickleable exception object.

## Observed behavior

- SafetensorError pickles as module safetensors_rust, but that module is not importable in this environment. Running ForkingPickler.dumps(SafetensorError('boom')) raises PicklingError: Can't pickle <class 'safetensors_rust.SafetensorError'>: import of module 'safetensors_rust' failed.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
