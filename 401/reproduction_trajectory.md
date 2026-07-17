# Reproduction Trajectory — Bug 401: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3263](https://github.com/pyro-ppl/pyro/issues/3263)
- **Repository:** pyro-ppl/pyro @ `0e82cad30f75b892a07e6c9a5f9e24f2cb5d0d81`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the venv and install the CUDA-enabled torch build plus the editable local Pyro checkout.
2. Run `bash run_repro.sh` or `python repro.py --cuda --num-data 10 --batch-size 10 --num-epochs 1` in the venv.
3. Observe the DataLoader shuffle path fail inside `pyro/contrib/cevae/__init__.py` before the first training step completes.

## Observed behavior

- Running the CEVAE synthetic example with --cuda on this checkout raises RuntimeError: Expected a 'cuda' device type for generator but found 'cpu'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
