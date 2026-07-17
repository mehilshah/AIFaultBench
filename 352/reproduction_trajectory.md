# Reproduction Trajectory — Bug 352: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/1938](https://github.com/huggingface/peft/issues/1938)
- **Repository:** huggingface/peft @ `52684952136b3dcc1120834f8af2d8f5aaa1c16a`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a tiny GPT-2 causal LM and wrapped it with PrefixTuningConfig.
2. Called PeftModelForCausalLM.forward() with a caller-supplied past_key_values kwarg.
3. The call completed successfully, so the historical duplicate-keyword bug was not reproduced.

## Observed behavior

- No TypeError was raised when passing past_key_values through prefix tuning.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The current PEFT snapshot appears to already handle the prefix-tuning past_key_values path.
