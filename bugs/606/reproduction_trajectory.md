# Reproduction Trajectory — Bug 606: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/9888](https://github.com/pyg-team/pytorch_geometric/issues/9888)
- **Repository:** pyg-team/pytorch_geometric @ `ab2b458f0c0f72d3cb573350b324db563066a7ee`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Data object with x and edge_index.
2. Define a model whose forward signature is forward(self, data).
3. Wrap the model in Explainer and pass data=data alongside x and edge_index.
4. Call explainer(data.x, data.edge_index, data=data).

## Observed behavior

- build_repro.<locals>.ToyModel.forward() got multiple values for argument 'data'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
