# Reproduction Trajectory — Bug 511: torch-geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10019](https://github.com/pyg-team/pytorch_geometric/issues/10019)
- **Repository:** pyg-team/pytorch_geometric @ `1ab39939d3ef44afa816b1bec4a84c957ad990f2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a destination-sorted temporal graph whose neighborhood for dst=2 is not sorted by source timestamp.
2. Instantiated NeighborSampler with time_attr='time' and is_sorted=True so the graph is not re-sorted by PyG.
3. Called node_sample() and observed the backend RuntimeError from pyg-lib.

## Observed behavior

- NeighborSampler on a destination-sorted temporal graph raised RuntimeError: Found invalid non-sorted temporal neighborhood

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && ./run_repro.sh
```
