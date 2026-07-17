# Reproduction Trajectory — Bug 236: equinox

- **Bug report:** [https://github.com/patrick-kidger/equinox/issues/898](https://github.com/patrick-kidger/equinox/issues/898)
- **Repository:** patrick-kidger/equinox @ `15a800d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtualenv and installed jax[cpu]==0.4.38, jaxtyping==0.3.11, typing_extensions==4.16.0, and equinox==0.11.8 from the pinned requirements.
2. Ran the minimal example from the bug report using a plain class and an eqx.Module subclass that both define __array__.
3. Confirmed that jnp.asarray(MyArray(...)) succeeds and jnp.asarray(MyEqxArray(...)) raises the reported TypeError.

## Observed behavior

- With jax==0.4.38 and equinox==0.11.8, a plain class implementing __array__ converts with jnp.asarray, but an eqx.Module subclass with the same __array__ method raises TypeError: Unexpected input type for array: <class '__main__.MyEqxArray'>.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
