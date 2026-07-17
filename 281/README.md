# Bug 281 Reproduction

This folder reproduces the `knn_graph` export failure from
https://github.com/pyg-team/pytorch_geometric/issues/10703 using the local
`codebase/` checkout.

## Observed result

`torch.export.export(...)` on a module that calls
`torch_geometric.nn.knn_graph(...)` fails with:

`torch._subclasses.fake_tensor.UnsupportedOperatorException: pyg.knn.default`

## Environment used for verification

- `torch 2.8.0+cu128`
- `torch-geometric 2.8.0`
- `pyg-lib 0.6.0+pt28cu126`

## Reproduction

1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

`run_repro.sh` also writes the command output to `repro_stdout.log` and
`repro_stderr.log`.
