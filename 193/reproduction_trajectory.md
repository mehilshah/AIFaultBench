# Reproduction Trajectory — Bug 193: equinox

- **Bug report:** [https://github.com/patrick-kidger/equinox/issues/1172](https://github.com/patrick-kidger/equinox/issues/1172)
- **Repository:** patrick-kidger/equinox @ `09e19a6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a virtual environment in the bug folder.
2. Install the local Equinox checkout and pinned runtime dependencies.
3. Run `repro.py` with `JAX_TRACEBACK_FILTERING=off`.
4. Observe the reported `TypeError`.

## Observed behavior

- Running the report's minimal example in this checkout raises `TypeError: can only concatenate str (not "_Sentinel") to str`.
- The traceback enters `jax/_src/api.py` at `vmap`, on the line `docstr += fun.__doc__`.
- The failure is triggered by `jax.lax.scan(scan_fn, critic, batch)` where `scan_fn` calls `jax.vmap(carry)(x)` on an `eqx.Module` with a static default field.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
