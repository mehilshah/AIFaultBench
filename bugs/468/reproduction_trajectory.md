# Reproduction Trajectory — Bug 468: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7807](https://github.com/deepspeedai/DeepSpeed/issues/7807)
- **Repository:** microsoft/DeepSpeed @ `15ad92b459c6c39b7c5527efe1e42080eb4ab99f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load DeepSpeed's Muon update function from the pinned codebase checkout.
2. Feed it the fully reduced gradient that would exist if reduce_scatter=false.
3. Feed it two rank-local mixed buffers that model reduce_scatter=true for a cross-partition parameter.
4. Compare the partition slices and reconstructed update.

## Observed behavior

- Muon sees different gradients depending on whether the full reduce-scatter result was available before orthogonalization. Using codebase/deepspeed/runtime/zero/muon/original_muon.py, the rank-0 partition differs from the correct update by 0.351562, the rank-1 partition differs by 0.578125, and the reconstructed full update differs by 0.578125.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
