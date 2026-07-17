# Bug 196 Reproduction

This bundle reproduces the shape-checking inconsistency reported in
https://github.com/patrick-kidger/jaxtyping/issues/290.

Observed behavior in this checkout:
- A `jaxtyped` function taking a `chex.dataclass` argument returns successfully even
  though the returned dataclass contains arrays of shape `2` after the input bound
  `B` was inferred as `10`.
- The equivalent plain-tensor function raises a `TypeCheckError` as expected.

Files:
- `repro.py` runs both cases.
- `requirements.txt` lists the runtime dependencies.
- `setup_env.sh` installs the dependencies.
- `run_repro.sh` executes the repro and records logs.
