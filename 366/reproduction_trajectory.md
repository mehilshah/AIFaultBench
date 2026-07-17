# Reproduction Trajectory — Bug 366: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47956](https://github.com/vllm-project/vllm/issues/47956)
- **Repository:** vllm-project/vllm @ `dd127d82ed29c40b7daf6e751add49ff371b1d9d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a checkpoint-style config.json matching the issue report.
2. Loaded it with transformers.AutoConfig in an isolated env.
3. Verified that the top-level Qwen3-VL config keeps num_labels=20 while the nested text config stays at 2.
4. Captured the reproduction output in repro_stdout.log and repro_stderr.log.

## Observed behavior

- AutoConfig.from_pretrained() on a Qwen3-VL checkpoint-style config loads Qwen3VLConfig with top-level num_labels=20 and problem_type=multi_label_classification.
- The nested Qwen3-VL text config still reports num_labels=2 and problem_type=None, so the serving path derives a 2-class head where the checkpoint expects 20 labels.
- The captured repro output shows the mismatch explicitly: checkpoint score.weight shape (20, 4096) versus vLLM-side head shape (2, 4096).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
VENV_DIR=/tmp/bug366-venv bash run_repro.sh
```
