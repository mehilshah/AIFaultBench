# Reproduction Trajectory — Bug 643: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/2724](https://github.com/pyro-ppl/pyro/issues/2724)
- **Repository:** pyro-ppl/pyro @ `5e198f24a286017914c78efd94422bf7c2817da5`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Set up a Python 3.12 venv with Torch 2.13 CPU, pyro-api, and Funsor 0.4.7.
2. Patched Torch version and two compatibility points in-process so the recovered Pyro snapshot can import.
3. Ran the issue's guide/model pair from tests/contrib/funsor/test_enum_funsor.py.
4. Compared TraceEnum_ELBO(max_plate_nesting=0) against TraceEnum_ELBO(max_plate_nesting=1).

## Observed behavior

- expected_loss=2.393253803253174, actual_loss=2.393253803253174, abs_err=0.0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The standardized environment does not reproduce the mismatch; after minimal compatibility shims, the expected and actual losses are identical.
