# Reproduction Trajectory — Bug 389: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38632](https://github.com/jax-ml/jax/issues/38632)
- **Repository:** jax-ml/jax @ `faf677af0abec7ea25c7a33831fcabf30a795796`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated virtual environment with Python 3.12.3.
2. Install numpy==2.4.6, jax==0.10.1, and jaxlib==0.10.1.
3. Run repro.py with JAX_PLATFORMS=cpu.
4. Observe that jax.lax.mul(-inf, 1.401298464324817e-45) returns nan.

## Observed behavior

- Running the reproduced script under jax==0.10.1, jaxlib==0.10.1, numpy==2.4.6 on Python 3.12.3 prints 'third_element_is_negative_inf: False' and 'third_element_is_nan: True'; the third multiply result is nan instead of -inf.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
