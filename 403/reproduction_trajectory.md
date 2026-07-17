# Reproduction Trajectory — Bug 403: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10276](https://github.com/pyg-team/pytorch_geometric/issues/10276)
- **Repository:** pyg-team/pytorch_geometric @ `fed2253c4a807e85ba61887efd0bb10ee869d094`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Cloned the referenced upstream snapshot into `codebase/` at commit `fed2253c4a807e85ba61887efd0bb10ee869d094`.
2. Vendored the issue's `GConvGRU` helper as `gconv_gru.py` and recreated the issue body as `repro.py`.
3. Validated the bundle syntax with `bash -n` and `python3 -m py_compile`.
4. Attempted the launcher locally and captured the environment failure in `repro_stdout.log` and `repro_stderr.log`.

## Observed behavior

- The reported script requires `lightning_fabric.Fabric(devices=[0, 1], strategy='ddp')`, but this host only exposes one CUDA device via `nvidia-smi -L`.
- Running `bash run_repro.sh` here fails earlier during `import torch` with `ImportError: ... libtorch_cuda.so: undefined symbol: ncclCommResume`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The bug report depends on a multi-GPU DDP execution path, but this machine only exposes one GPU. The local Python environment also has a broken torch CUDA install, so the repro cannot be exercised end to end here.
