# Reproduction Trajectory — Bug 630: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/2815](https://github.com/pyro-ppl/pyro/issues/2815)
- **Repository:** pyro-ppl/pyro @ `74742df3da89e5aeb3965ebcb512b96432f29d79`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.11 virtual environment and install the CPU torch 1.13.1 dependency set from `requirements.txt`.
2. Run `repro.py` through `run_repro.sh` using the local `codebase/` checkout on `sys.path`.
3. Observe the expected `log_prob` failure at the `measurement` site when the conditioned value is a Python float.

## Observed behavior

- Running the notebook's SVI cell with `pyro.condition(scale, data={"measurement": 9.5})` under Python 3.11 and torch 1.13.1+cpu raises `ValueError: Error while computing log_prob at site 'measurement': The value argument to log_prob must be a Tensor`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
