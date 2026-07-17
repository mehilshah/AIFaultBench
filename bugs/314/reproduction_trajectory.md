# Reproduction Trajectory — Bug 314: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/39108](https://github.com/jax-ml/jax/issues/39108)
- **Repository:** jax-ml/jax @ `6d9a2a2a2fc6a586404ee29ea665bc5b2adfa13f`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a virtual environment with `bash setup_env.sh`.
2. Run `bash run_repro.sh` to execute the minimal example on CPU.
3. Observe that the output is `[1.]` and the script exits with status 1, so the bug is absent here.

## Observed behavior

- With the supported runtime set used by this bundle, `jax.scipy.special.gammaincc(np.inf, 2.0)` returned `[1.]` instead of `NaN`.
- Trying to downgrade to `jaxlib==0.10.1` is blocked by the checked-in source tree: it raises `RuntimeError: jaxlib is version 0.10.1, but this version of jax requires version >= 0.10.2`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The local codebase is newer than the buggy release and requires `jaxlib >= 0.10.2`; with the supported 0.10.2 wheel the issue is already fixed, and the older 0.10.1 wheel from the report is rejected by the version gate.
