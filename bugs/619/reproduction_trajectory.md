# Reproduction Trajectory — Bug 619: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/9829](https://github.com/pyg-team/pytorch_geometric/issues/9829)
- **Repository:** pyg-team/pytorch_geometric @ `bd5ae45c74a3fbb6b6ff818476f7651d84313d2a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a single-graph PyG `Data` object with 3161 nodes.
2. Run `pytorch_lightning.Trainer.validate` on a module whose `validation_step` calls `self.log('val_loss', loss)` without `batch_size`.
3. Observe Lightning warn that it inferred batch size 3161 from an ambiguous collection, even though the other metric log passes `batch_size=batch.num_graphs`.

## Observed behavior

- Lightning emitted the ambiguous batch-size warning during validation. Captured warning(s): ['Trying to infer the `batch_size` from an ambiguous collection. The batch size we found is 3161. To avoid any miscalculations, use `self.log(..., batch_size=batch_size)`.']

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
