# Reproduction Trajectory — Bug 436: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21611](https://github.com/Lightning-AI/pytorch-lightning/issues/21611)
- **Repository:** Lightning-AI/pytorch-lightning @ `6805188c711094339e76d81668a4037dd56f7c7a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Verified `codebase/src/lightning/pytorch/plugins/precision/amp.py` line 116 contains `return torch.autocast(self.device, dtype=dtype, cache_enabled=False)`.
2. Imported torch 2.8.0+cu128.
3. CUDA device: NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition.
4. Ran a repeated decoder-style forward/backward benchmark under bf16 autocast with cache_enabled=True and False.
5. Observed a large peak-memory increase when cache_enabled=False was used.

## Observed behavior

- See the captured logs below for the observed output.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
