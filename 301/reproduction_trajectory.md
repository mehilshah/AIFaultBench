# Reproduction Trajectory — Bug 301: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21778](https://github.com/Lightning-AI/pytorch-lightning/issues/21778)
- **Repository:** Lightning-AI/pytorch-lightning @ `fe6b1cc4e80ae0396e2e404c16e6b6968ad5437e`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a one-process distributed environment with `backend=gloo`.
2. Constructed `lightning.pytorch.strategies.FSDPStrategy()` and forced `parallel_devices=[torch.device('cpu')]`.
3. Called `strategy._setup_model(nn.Linear(2, 2))` on CPU.

## Observed behavior

- Ran `FSDPStrategy._setup_model()` on a CPU-only one-process `gloo` setup with `root_device.index == null`.
- In this environment (`torch 2.13.0+cu130`), the call completed successfully and only emitted FSDP CPU-init warnings; no `RuntimeError` was raised.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

This checkout is using `torch 2.13.0+cu130`, which does not reproduce the torch 2.5+/2.6 CPU guard described in the report. The reported `RuntimeError: FSDP needs a non-CPU accelerator device` does not occur here.
