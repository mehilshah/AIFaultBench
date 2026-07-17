# Reproduction Trajectory — Bug 243: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2029](https://github.com/pyro-ppl/numpyro/issues/2029)
- **Repository:** pyro-ppl/numpyro @ `17cf5a7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a 4-device CPU JAX runtime so the reported parallel/vectorized chain methods can execute.
2. Run the local NumPyro 0.18.0 checkout on the Poisson-with-Uniform-prior model from the bug report.
3. Compare lag-1 autocorrelation of flattened posterior draws for NUTS, AIES, and ESS.

## Observed behavior

- With XLA forced to 4 CPU devices, the reproduced run matched the report's pattern: NUTS lag-1 autocorrelation was 0.449453, AIES was 0.940259, and ESS was 0.022275. ESS is the clear outlier and has much lower autocorrelation than both comparison samplers.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
