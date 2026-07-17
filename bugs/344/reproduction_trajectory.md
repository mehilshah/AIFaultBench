# Reproduction Trajectory — Bug 344: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10497](https://github.com/pyg-team/pytorch_geometric/issues/10497)
- **Repository:** pyg-team/pytorch_geometric @ `125202736759d37ec1bc1ce8f4de67d6ddc9c8b0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a torch_geometric.data.Data object.
2. Remove its internal _store attribute before pickling to simulate an older PyG payload.
3. pickle.load() the object and print it.
4. Observe the RuntimeError: The 'data' object was created by an older version of PyG.

## Observed behavior

- A pickle that mimics an older PyG Data object without _store loads successfully, but printing it raises RuntimeError from torch_geometric/data/data.py:557 while __repr__ accesses self._store.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
