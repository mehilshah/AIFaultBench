# Reproduction Trajectory — Bug 320: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/48217](https://github.com/vllm-project/vllm/issues/48217)
- **Repository:** vllm-project/vllm @ `e5588e49bc2642670116664a7fc4096e27adb179`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load the real vLLM Gemma4 parser module through a stubbed package shell.
2. Call non-streaming extract_reasoning() on plain text without channel markers.
3. Stream the same text in chunks after a prompt ending with <|turn> and observe all chunks labeled as reasoning.

## Observed behavior

- non-streaming=(None, 'This is a direct final answer without channel markers.'); streaming_chunks=[{'reasoning': 'This is a'}, {'reasoning': ' direct final answer'}, {'reasoning': ' without channel markers.'}]; finished=None

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
