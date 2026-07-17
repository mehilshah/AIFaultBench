# Reproduction Trajectory — Bug 552: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3018](https://github.com/pyro-ppl/pyro/issues/3018)
- **Repository:** pyro-ppl/pyro @ `319c515de2a82ac002516ccd4b44dda8e32f7ac4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.10 virtual environment.
2. Install numpy<2, torch==1.13.1+cpu, pyro-api, opt_einsum, and tqdm.
3. Run repro.py through ./run_repro.sh with the local codebase on sys.path.
4. Observe the AttributeError: __enter__ raised from pyro/poutine/messenger.py:_context_wrap.

## Observed behavior

- Running ./run_repro.sh under Python 3.10 with torch 1.13.1+cpu prints 'pyro 1.8.0', 'torch 1.13.1+cpu', and 'starting run', then fails with Traceback in codebase/pyro/poutine/messenger.py line 11: 'with context:' -> AttributeError: __enter__.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
