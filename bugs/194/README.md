# Bug 194 Reproduction

Reported issue: `filter_vmap` produces output with the wrong `out_axes` arrangement when `out_axes=-1`.

Observed locally with the bundled codebase:

- `jax.vmap(foo, out_axes=-1)(x)` returns shape `(3, 4, 2)`
- `eqx.filter_vmap(foo, out_axes=-1)(x)` returns shape `(4, 3, 2)`

## Run

```bash
bash run_repro.sh
```

`run_repro.sh` creates a local virtualenv, installs the pinned dependencies, installs the local `codebase/` editable, and then runs `repro.py`.
