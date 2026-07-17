# Reproduction Trajectory — Bug 196: jaxtyping

- **Bug report:** [https://github.com/patrick-kidger/jaxtyping/issues/290](https://github.com/patrick-kidger/jaxtyping/issues/290)
- **Repository:** patrick-kidger/jaxtyping @ `bd84aed`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Activate the environment or install dependencies with `bash setup_env.sh`.
2. Run `bash run_repro.sh` from the bug folder.
3. Observe that the dataclass case returns normally while the plain-tensor case raises `TypeCheckError`.

## Observed behavior

- Running `bash run_repro.sh` produced `DATACLASS_CASE=NO_ERROR:Vector(x=Array([0., 1.], dtype=float32), y=Array([0., 1.], dtype=float32))` and `PLAIN_CASE=ERROR:TypeCheckError:Type-check error whilst checking the return value of __main__.test.` with `B=10` in scope.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
