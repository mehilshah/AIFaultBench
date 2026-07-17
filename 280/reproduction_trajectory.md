# Reproduction Trajectory — Bug 280: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/418](https://github.com/PythonOT/POT/issues/418)
- **Repository:** PythonOT/POT @ `0411ea22a96f9c22af30156b45c16ef39ffb520d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create the isolated environment and install POT against the active NumPy/SciPy stack.
2. Run `bash run_repro.sh` to execute the repro script with runtime shims for NumPy/SciPy compatibility.
3. Observe that the seeded and explicit-projection calls share identical projections but return different sliced Wasserstein distances.

## Observed behavior

- The repro script confirms the same projection matrix is used in both calls (projections_equal_norm=0.0, projection_count=10) but the costs differ: cost_with_seed=21.887428414187593 and cost_with_custom_projections=9.788355557356775. The custom-projection path matches the buggy normalization using 50 projections instead of the provided 10.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
