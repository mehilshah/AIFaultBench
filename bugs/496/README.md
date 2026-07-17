# Bug 496

This folder is the reusable standardized benchmark input for the JAX `heaviside`
NaN regression from issue `https://github.com/jax-ml/jax/issues/38105`.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`

Observed failure:
- `np.heaviside(nan, -1.0)` returns `nan`
- `jnp.heaviside(nan, -1.0)` returns `-1.0`
- the same mismatch appears under `jax.jit`

Environment used for verification:
- `jax==0.10.1`
- `jaxlib==0.10.1`
- `numpy==2.5.1`
