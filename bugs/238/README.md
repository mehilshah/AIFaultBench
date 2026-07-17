# Bug 238 Reproduction

This folder reproduces the `jaxtyping`/`typeguard==2.13.3` bug where a PEP 604
optional annotation accepts an array with the wrong dtype.

Observed behavior:
- `Optional[Int[jnp.ndarray, " N"]]` rejects the float array.
- `Union[Int[jnp.ndarray, " N"], None]` rejects the float array.
- `Int[jnp.ndarray, " N"] | None` accepts the float array.

Setup:
- `setup_env.sh` creates a local `.venv` and installs the dependencies.
- `run_repro.sh` runs `repro.py`.

Reproduction command:
```bash
bash setup_env.sh
bash run_repro.sh
```
