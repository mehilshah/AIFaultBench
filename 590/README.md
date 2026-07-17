# Bug 590 Reproduction Bundle

This folder reproduces NumPyro issue 2013:
`TraceEnum_ELBO` crashes when the guide contains an `infer={"is_auxiliary": True}`
sample site that is absent from the model.

## What fails

Running `TraceEnum_ELBO().loss(...)` on the minimal model/guide pair in
[`repro.py`](./repro.py) raises:

`KeyError: 'aux'`

The traceback points to `numpyro/infer/elbo.py` while iterating over guide sample
sites.

## How to run

1. Create the isolated environment:
   `bash setup_env.sh`
2. Run the repro:
   `bash run_repro.sh`

`run_repro.sh` writes stdout to [`repro_stdout.log`](./repro_stdout.log) and stderr
to [`repro_stderr.log`](./repro_stderr.log).

## Dependency notes

The checked-in NumPyro source needs an older JAX/NumPy/SciPy combination than the
latest wheels. The pinned versions in [`requirements.txt`](./requirements.txt) are
the set that reproduces the crash in this folder:

- `jax==0.4.25`
- `jaxlib==0.4.25`
- `numpy<2`
- `scipy==1.11.4`
- `funsor==0.4.7`

