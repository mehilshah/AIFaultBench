# Reproduction Bundle

This bundle reproduces NumPyro issue 2123 from `bug_report.txt`.

## What it shows

- A mixture built from a batched `Uniform` prints `theta.shape == (2,)` twice.
- The equivalent mixture built from a list of two `Uniform`s prints `theta.shape == ()` twice.

That matches the reported regression: the batched `Uniform` mixture behaves like a 2-variate variable when it should be scalar.

## How to run

```bash
./run_repro.sh
```

The setup script creates `.venv/`, installs the pinned runtime, and installs the local `codebase/` in editable mode.
