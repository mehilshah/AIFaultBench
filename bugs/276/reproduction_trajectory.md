# Reproduction Trajectory — Bug 276: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3919](https://github.com/pytorch/rl/issues/3919)
- **Repository:** pytorch/rl @ `74abd6c38c065a17aeaa4bd617167055e434fdad`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Launch `bash run_repro.sh` from the standardized bug folder.
2. Observe the script write a dataset into a temporary cache path.
3. Observe `minari.load_dataset` use the restored default cache path instead of the temporary download cache.
4. Observe the resulting `FileNotFoundError` in `repro_stderr.log`.

## Observed behavior

- Running `bash run_repro.sh` reproduces the failure: the script downloads into a temporary Minari cache, restores `MINARI_DATASETS_PATH`, then `minari.load_dataset` looks in `/users/grad/mehil/.minari/datasets` and raises `FileNotFoundError` for `D4RL/door/human-v2`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
