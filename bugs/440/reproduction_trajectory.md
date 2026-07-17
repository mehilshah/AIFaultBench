# Reproduction Trajectory — Bug 440: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/424](https://github.com/huggingface/peft/issues/424)
- **Repository:** huggingface/peft @ `b1059b73aab9043b118ff19b0cf96263ea86248a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a tiny local torch.nn.Module with a single linear layer.
2. Wrap it with peft.get_peft_model using LoraConfig(r=87, target_modules=['linear']).
3. Deep-copy the wrapped model.
4. Inspect the copied adapter config and observe that r falls back to 8 instead of staying at 87.

## Observed behavior

- Running `bash run_repro.sh` against the checked-out b1059b73aab9043b118ff19b0cf96263ea86248a snapshot prints original_r=87 and copied_r=8 for the deep-copied adapter.
- The failure happens without downloading any external model because a tiny local nn.Module is enough to exercise `get_peft_model` and `copy.deepcopy`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
