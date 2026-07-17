# Reproduction Trajectory — Bug 234: equinox

- **Bug report:** [https://github.com/patrick-kidger/equinox/issues/1156](https://github.com/patrick-kidger/equinox/issues/1156)
- **Repository:** patrick-kidger/equinox @ `d171883`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtual environment with python3 -m venv .venv
2. Install the bundle dependencies with ./setup_env.sh
3. Run ./run_repro.sh and observe the second call raising ValueError

## Observed behavior

- On JAX 0.8.2 and Equinox 0.13.2, calling the jitted function first with a non-error input and then with an error input produced second_call_exception=ValueError instead of EquinoxRuntimeError.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
