# Reproduction Trajectory — Bug 434: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46932](https://github.com/huggingface/transformers/issues/46932)
- **Repository:** huggingface/transformers @ `dd192bad352f5fbe2d2141ece8a9390071fd895c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- repro_stdout.log shows the unsafe Gemma4 cast sites in codebase/src/transformers/models/gemma4/modeling_gemma4.py and the local numeric repro: [0.73, 1.25, -0.4] float32 becomes [0, 1, 0] int8 after the buggy cast. repro_stderr.log contains: BUG REPRODUCED: float activations are silently truncated when cast to an integer weight dtype. Recorded exit code: 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
