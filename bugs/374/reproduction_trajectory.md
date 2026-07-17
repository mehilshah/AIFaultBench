# Reproduction Trajectory — Bug 374: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10396](https://github.com/pyg-team/pytorch_geometric/issues/10396)
- **Repository:** pyg-team/pytorch_geometric @ `a0f9e8fe469ef50760ae0c9a2702bf8443017b0c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python 3.12 virtualenv and installed torch==2.6.0+cpu plus the runtime dependencies from requirements.txt.
2. Ran PYTHONPATH=codebase .venv/bin/python repro.py from the bug folder.
3. The run reached torch_geometric.data.download.download_url() with http://vision.princeton.edu/projects/2014/3DShapeNets/ModelNet10.zip and failed with HTTP 404.

## Observed behavior

- With a clean Python 3.12 virtualenv and the local codebase on PYTHONPATH, instantiating ModelNet(root='repro_data/modelnet10', name='10', train=True) prints the download URL and raises urllib.error.HTTPError: HTTP Error 404: Not Found from torch_geometric/datasets/modelnet.py:115.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
