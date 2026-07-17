# Reproduction Trajectory — Bug 023: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/10972](https://github.com/tensorflow/models/issues/10972)
- **Repository:** tensorflow/models @ `e871d4739e89bcc2b6b16c8e8a8d3eea3eaf1bae`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Run `bash setup_env.sh` to install the notebook dependencies into `.deps`.
2. Run `bash run_repro.sh` to execute the mirrored import cell.
3. Observe that the script prints module locations and exits with status 0 instead of raising the reported import error.

## Observed behavior

- The mirrored notebook import cell ran to completion in a clean environment. `tensorflow`, `orbit`, `tensorflow_models`, and the official vision imports all loaded successfully and the script exited 0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported notebook import failure is not reproducible here after installing the required packages; the import cell succeeds.
