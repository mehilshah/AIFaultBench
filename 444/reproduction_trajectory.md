# Reproduction Trajectory — Bug 444: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2071](https://github.com/pyro-ppl/numpyro/issues/2071)
- **Repository:** pyro-ppl/numpyro @ `68d86dc0535c5488f497790af2305d19d74d924a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and populate the isolated environment with `bash setup_env.sh`.
2. Run `bash run_repro.sh` to execute the minimal `Predictive(..., parallel=True)` example.
3. Observe that the legacy PRNGKey path succeeds and the typed-key path fails with the reported ValueError.

## Observed behavior

- Ran the minimal repro under jax 0.7.1 and the local numpyro 0.19.0 checkout. Legacy `jax.random.PRNGKey(0)` succeeded, but `jax.random.key(0)` with `Predictive(..., parallel=True)` raised `ValueError: Cannot convert_element_type from int32 to key<fry>` from `numpyro/util.py:443` inside `soft_vmap`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
