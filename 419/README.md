# Bug 419 Reproduction

Issue: `jax.scipy.stats.chi2.logpdf` returns `nan` at the boundary values `x=0.0` and `x=inf` when `df=2.0`.

Repository snapshot:
- JAX commit: `4250605d1e353e8f3e5f943abc485d5bbe1fb250`
- Issue: https://github.com/jax-ml/jax/issues/38620

## Repro steps

1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

## Expected

For `df=2`, the chi-square log density has the closed form:

`log f(x; df=2) = -log(2) - x/2`

So:
- `x=0.0` should produce `-0.6931471805599453`
- `x=inf` should produce `-inf`

## Actual

The bundled `repro.py` prints JAX returning `nan` for both cases and exits with status `1`.
