# Reproduction Trajectory — Bug 380: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7885](https://github.com/deepspeedai/DeepSpeed/issues/7885)
- **Repository:** microsoft/DeepSpeed @ `a41a96b19f2b5e75567c85ff9155e4bb09c8e539`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a dependency directory and install torch/numpy/packaging.
2. Install deepspeed==0.18.4 and run the CPU ZeRO-2 benchmark.
3. Install deepspeed==0.18.5 and rerun the same benchmark.
4. Compare hook-count calls and step time; 0.18.5 regresses from one count refresh per backward to one per hook.

## Observed behavior

- DeepSpeed 0.18.4 made 6 hook-count calls and averaged 0.006119s/step, while DeepSpeed 0.18.5 made 384 hook-count calls and averaged 0.018013s/step on the same CPU ZeRO-2 workload (2.94x slower).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
