# Bug 408 Reproduction Bundle

This folder reproduces the Accelerate TensorBoard logging bug from
[`huggingface/accelerate#1546`](https://github.com/huggingface/accelerate/issues/1546).

Observed behavior:
- `accelerator.log({"loss": torch.tensor(1.0)}, step=1)` writes no `loss` scalar to TensorBoard.
- `accelerator.log({"loss": 1.0}, step=1)` writes the expected scalar event.

Files of interest:
- [`repro.py`](./repro.py)
- [`requirements.txt`](./requirements.txt)
- [`setup_env.sh`](./setup_env.sh)
- [`run_repro.sh`](./run_repro.sh)
- [`manifest.json`](./manifest.json)

Usage:
1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`
3. Inspect `repro_stdout.log`, `repro_stderr.log`, and `reproduction.json`
