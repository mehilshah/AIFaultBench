# Bug 481 Reproduction

This bundle reproduces the `WishartCholesky.infer_shapes` bug reported in
NumPyro issue 2041.

## Contents

- `repro.py`: minimal reproducer
- `requirements.txt`: dependency list for the local checkout
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: executes the reproducer

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```
