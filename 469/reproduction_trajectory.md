# Reproduction Trajectory — Bug 469: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47300](https://github.com/vllm-project/vllm/issues/47300)
- **Repository:** vllm-project/vllm @ `5c4db60f019a183231cf020e5679baaf1e8c293f`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Built the Gemma-4 multimodal conversation from the issue report: 3 image turns followed by the long text-only turn.
2. Validated the bundle locally with the offline dry-run path.
3. Stopped before server launch because this machine does not provide the required CUDA GPU / SM90 Hopper environment.

## Observed behavior

- `run_repro.sh` completed the dry-run prompt construction and printed the exact 4-turn Gemma-4 multimodal payload shape, including the long final NIAH-style prompt with `final_prompt_token_count` 144480. The script then exited with `Blocked: no CUDA GPU is available, so the SM90 FlashAttention 4 path cannot be exercised here.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

No CUDA GPU is available in this environment, so the H100/SM90 FlashAttention 4 code path described in the bug report cannot be exercised.
