# Reproduction Trajectory — Bug 246: pyro-ppl

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3371](https://github.com/pyro-ppl/pyro/issues/3371)
- **Repository:** pyro-ppl/pyro @ `0678b35`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the minimal Pyro/Torch/graphviz dependencies.
2. Ran the issue's deterministic model and a probabilistic control through pyro.render_model(render_params=True).
3. Observed that the deterministic graph source omits the parameter node while the probabilistic control includes it.

## Observed behavior

- Running render_model(..., render_params=True) on the deterministic example prints a graph with only the deterministic node and no parameter node. The probabilistic control prints a graph that includes `param` and a `param -> probabilistic` edge.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
