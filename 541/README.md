# Bug 541 Reproduction Bundle

This folder reproduces GitHub issue `pyg-team/pytorch_geometric#9965`.

Issue summary:
- `Inspector.type_repr(Final[Optional[Tensor]])` was reported to return `typing.Final[Optional[typing.Any]]`.
- `coalesce` and `sort_edge_index` were reported to fail TorchScript compilation for `Optional[Tensor]` arguments.

Local result in this checkout:
- The reported behavior does not reproduce.
- `Inspector.type_repr(Final[Optional[Tensor]])` returns `typing.Final[Optional[Tensor]]`.
- File-backed TorchScript wrappers around `coalesce` and `sort_edge_index` compile and run successfully.

Run:
```bash
bash setup_env.sh
bash run_repro.sh
```
