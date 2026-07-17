# Reproduction Bundle

This bundle reproduces NumPyro issue 1719 from `bug_report.txt`.

## What it does

The repro runs the report's NUTS model:

```python
x = numpyro.sample("x", dist.Normal())
numpyro.factor("jump", jnp.where(x > 0, 1000.0, 0))
```

With the local `codebase/` snapshot, the posterior samples are biased relative to the half-normal target on the positive side.

## How to run

```bash
bash run_repro.sh
```

The run script creates `.venv_repro/`, installs the pinned dependencies from `requirements.txt`, and executes `repro.py`.

## Expected output

The current snapshot produces output like:

```text
sample_mean=0.739689
expected_halfnormal_mean=0.797885
mean_error=-0.058196
sample_std=0.614824
frac_positive=1.000000
num_diverging=8522
```

That mean error is the evidence that the bug is reproducible here.
