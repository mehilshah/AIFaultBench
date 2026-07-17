# Reproduction Trajectory — Bug 580: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/9899](https://github.com/pyg-team/pytorch_geometric/issues/9899)
- **Repository:** pyg-team/pytorch_geometric @ `ab2b458f0c0f72d3cb573350b324db563066a7ee`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load the real glem.py module from the local codebase with minimal stdlib-based stubs for unavailable runtime modules.
2. Instantiate GLEM without running its heavy __init__ and set the small set of attributes needed by train().
3. Call GLEM.train('gnn', ..., pseudo_labels=None, ...) to mirror the train_without_ext_pred=True pretraining path.
4. Observe the AttributeError raised by pseudo_labels.to(self.device).

## Observed behavior

- Running the minimal loader in repro.py triggers AttributeError: 'NoneType' object has no attribute 'to' from codebase/torch_geometric/nn/models/glem.py:147, matching the train_without_ext_pred path where ext_pseudo_labels is None.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
