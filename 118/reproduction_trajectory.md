# Reproduction Trajectory — Bug 118: clearml

- **Bug report:** [https://github.com/clearml/clearml/issues/1440](https://github.com/clearml/clearml/issues/1440)
- **Repository:** clearml/clearml @ `7d882dd`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh Python virtual environment.
2. Upgrade pip inside the virtual environment.
3. Run pip install --dry-run -r requirements.txt with clearml==2.0.0 and clearml-agent==1.9.3.
4. Observe pip fail with a requests version conflict.

## Observed behavior

- Pip reported that clearml 2.0.0 requires requests>=2.32.0 while clearml-agent 1.9.3 requires requests<=2.31.0, making the resolver fail.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
