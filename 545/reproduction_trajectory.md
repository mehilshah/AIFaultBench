# Reproduction Trajectory — Bug 545: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21488](https://github.com/Lightning-AI/pytorch-lightning/issues/21488)
- **Repository:** Lightning-AI/pytorch-lightning @ `79a39c04d37434f2234d9b518a145854d7c1e642`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean Python 3.12 virtual environment and install the pinned runtime dependencies.
2. Run repro.py against codebase/src so Lightning is imported from the local snapshot.
3. Observe that the child call to save_hyperparameters(ignore='arg2') does not remove arg2 from model.hparams.

## Observed behavior

- ChildModel(arg1=1, arg2=2) produced hparams={'arg1': 1, 'arg2': 2}; arg2 remained after save_hyperparameters(ignore='arg2').

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
