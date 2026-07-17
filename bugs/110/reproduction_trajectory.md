# Reproduction Trajectory — Bug 110: safetensors

- **Bug report:** [https://github.com/huggingface/safetensors/issues/492](https://github.com/huggingface/safetensors/issues/492)
- **Repository:** huggingface/safetensors @ `079781f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtualenv and install `numpy==1.26.4`, `safetensors==0.4.4`, and `torch==2.3.0`.
2. Run `repro.py`, which writes a tiny safetensors file and then iterates a `torch.utils.data.DataLoader` with `num_workers=2`.
3. Trigger an out-of-range tensor lookup in the worker and observe the pickling failure in multiprocessing queue handling.

## Observed behavior

- Running `timeout 20s .venv/bin/python repro.py` exits with code 124.
- stderr shows `_pickle.PicklingError: Can't pickle <class 'safetensors_rust.SafetensorError'>: import of module 'safetensors_rust' failed`.
- The dataloader does not surface the underlying `File does not contain tensor 5` exception from the worker.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
