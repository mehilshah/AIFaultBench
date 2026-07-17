# Reproduction Trajectory — Bug 462: torch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10138](https://github.com/pyg-team/pytorch_geometric/issues/10138)
- **Repository:** pyg-team/pytorch_geometric @ `afffee9f089ac0fe1eb8c1600c6e0b2e07ca6f80`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python 3.12 venv and installed `torch==2.4.1+cpu` plus the local editable `torch_geometric` checkout at commit `afffee9f089ac0fe1eb8c1600c6e0b2e07ca6f80`.
2. Ran the minimal subclass from `repro.py`, which declares `message(self, x_j: Tensor, edge_attr: Tensor | None = None)`.
3. Observed the constructor crash inside `MessagePassing.__init__` when `Inspector.type_repr` tried to read `__qualname__` from a `types.UnionType` instance.

## Observed behavior

- Running `bash setup_env.sh && bash run_repro.sh` in a clean venv reaches `codebase/torch_geometric/inspector.py:481` and raises `AttributeError: 'types.UnionType' object has no attribute '__qualname__'`.
- The traceback starts from `tmp = Tmp(123, 123)` in `repro.py`, enters `MessagePassing.__init__`, and fails while formatting the `Tensor | None` annotation in `Inspector.type_repr`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
