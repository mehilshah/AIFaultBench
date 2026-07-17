# Reproduction Trajectory — Bug 129: Ax

- **Bug report:** [https://github.com/facebook/Ax/issues/4076](https://github.com/facebook/Ax/issues/4076)
- **Repository:** facebook/Ax @ `708ace0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create the isolated Python environment and install dependencies.
2. Run `bash run_repro.sh` from the bug folder.
3. Observe the traceback in `repro_stderr.log` ending at `ParameterType.FLOAT`.

## Observed behavior

- Running the bundle prints 'Starting Ax homepage sample repro' and then fails with NameError: name 'ParameterType' is not defined at `parameter_type=ParameterType.FLOAT`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
