# Reproduction Trajectory — Bug 173: kubeflow-katib

- **Bug report:** [https://github.com/kubeflow/katib/issues/2346](https://github.com/kubeflow/katib/issues/2346)
- **Repository:** kubeflow/katib @ `87aec69`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a virtual environment.
2. Run `python -m pip install kfp==2.7.0 kubeflow-katib==0.17.0rc0`.
3. Observe pip's ResolutionImpossible error on the kubernetes dependency.

## Observed behavior

- pip failed to resolve kfp==2.7.0 and kubeflow-katib==0.17.0rc0 together because kfp requires kubernetes<27 and kubeflow-katib requires kubernetes>=27.2.0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
