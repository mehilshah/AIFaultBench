# Reproduction Trajectory — Bug 474: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3172](https://github.com/pyro-ppl/pyro/issues/3172)
- **Repository:** pyro-ppl/pyro @ `19e32df3a8620d99193d66ccc04ba3e2f1d3a840`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.10 virtual environment.
2. Install pyro-ppl==1.8.4 and torch==2.4.0.dev20240605+cpu.
3. Patch torch.nn.ModuleList to use an incompatible metaclass.
4. Import pyro.distributions and observe the TypeError during AutoGuideList definition.

## Observed behavior

- Importing pyro.distributions after replacing torch.nn.ModuleList with an incompatible metaclass raises the same metaclass conflict in pyro.infer.autoguide.guides.AutoGuideList.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash ./run_repro.sh > repro_stdout.log 2> repro_stderr.log
```
