# Reproduction Trajectory — Bug 278: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3430](https://github.com/pyro-ppl/pyro/issues/3430)
- **Repository:** pyro-ppl/pyro @ `bfe88ed8f000b88a546dc1c8848ecf5905082df2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the local virtual environment and install `requirements.txt`.
2. Run `bash run_repro.sh` from the bug folder with `PYTHONPATH` pointing at `codebase/`.
3. Observe that the original guide fails after `torch.save`/`torch.load`, but the loaded guide still works.

## Observed behavior

- Running `bash run_repro.sh` in this folder reproduces the bug. The saved guide reports `original_after_save_load=TypeError: PickleGuide.guide() missing 3 required positional arguments: 'batch', 'subsample', and 'full_size'`, while the deserialized guide prints `loaded_after_save_load=ok`. See `repro_stdout.log`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
