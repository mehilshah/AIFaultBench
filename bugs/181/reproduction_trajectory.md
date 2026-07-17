# Reproduction Trajectory — Bug 181: lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/20848](https://github.com/Lightning-AI/pytorch-lightning/issues/20848)
- **Repository:** Lightning-AI/pytorch-lightning @ `dd2912a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- Running the repro from this folder prints available_accelerators=['cpu', 'cuda', 'mps', 'tpu'] and then raises ValueError: You selected an invalid accelerator name: `accelerator='xpu'`. Available names are: auto, tpu, cuda, cpu, mps.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
