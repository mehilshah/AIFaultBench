# Reproduction Trajectory — Bug 190: NeMo

- **Bug report:** [https://github.com/NVIDIA-NeMo/NeMo/issues/15305](https://github.com/NVIDIA-NeMo/NeMo/issues/15305)
- **Repository:** NVIDIA-NeMo/NeMo @ `0d69e53`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Set up a local Python environment with CPU PyTorch and the NeMo ASR runtime dependencies.
2. Loaded the reporter-provided `timestamp.wav` from `timestamp.zip`.
3. Ran `EncDecMultiTaskModel.from_pretrained('nvidia/canary-1b-v2')` and transcribed the clip with `timestamps=True`.
4. Observed that the returned hypothesis had empty `timestamp['word']` and `timestamp['segment']` lists.

## Observed behavior

- On the reporter's `timestamp.wav`, `EncDecMultiTaskModel.from_pretrained('nvidia/canary-1b-v2')` restored successfully, but `model.transcribe(..., timestamps=True, batch_size=1, return_hypotheses=True)` returned `Hypothesis(timestamp={'word': [], 'segment': []})`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
