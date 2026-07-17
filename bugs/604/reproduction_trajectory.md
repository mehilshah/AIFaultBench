# Reproduction Trajectory — Bug 604: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/2870](https://github.com/pyro-ppl/pyro/issues/2870)
- **Repository:** pyro-ppl/pyro @ `005032f10099188fea86f63b6baa46a27867983f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean Python 3.10 virtualenv and installed the pinned CPU Torch + Pyro runtime dependencies.
2. Installed the local `codebase/` in editable mode so imports resolve to this checkout.
3. Ran `./run_repro.sh`, which executes `repro.py` and triggers the quantile broadcast error.

## Observed behavior

- Using Python 3.10.13 with torch 1.13.1+cpu and pyro 1.6.0, `AutoNormal.quantiles([0.05, 0.5, 0.95])` fails deterministically for a vector latent site with `RuntimeError: The size of tensor a (85) must match the size of tensor b (3) at non-singleton dimension 0`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
