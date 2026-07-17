# Reproduction Trajectory — Bug 046: fairseq

- **Bug report:** [https://github.com/facebookresearch/fairseq/issues/5242](https://github.com/facebookresearch/fairseq/issues/5242)
- **Repository:** facebookresearch/fairseq @ `100cd91db19bb27277a06a25eb4154c805b10189`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.11 virtualenv and install `torch==2.5.1`, `torchaudio==2.5.1`, and `numpy` from `requirements.txt`.
2. Execute `bash run_repro.sh`.
3. Observe the forced-alignment call fail because the emission tensor is 2-D instead of the required 3-D batch tensor.

## Observed behavior

- Running `bash run_repro.sh` in this folder produced `RuntimeError: log_probs must be 3-D (batch_size, input length, num classes)` from `torchaudio.functional.forced_align`. The captured traceback is in `repro_stderr.log` and the setup context is in `repro_stdout.log`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
