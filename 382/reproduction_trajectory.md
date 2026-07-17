# Reproduction Trajectory — Bug 382: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/850](https://github.com/huggingface/peft/issues/850)
- **Repository:** huggingface/peft @ `bbaafc2feff22ba696b517773a96c24443de3678`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Build a tiny local Bert sequence-classification model with a separately initialized classifier head.
2. Wrap the classifier with PEFT LoRA and `modules_to_save`, then verify adapter-on and disabled outputs match before saving.
3. Save the adapter, load it into a fresh base model with a different classifier initialization, and compare disabled outputs.

## Observed behavior

- Running `bash run_repro.sh` produced `loaded disabled == original disabled: False` with `max abs diff: 0.781838`, while `original adapter-on == original disabled: True` and `loaded adapter-on == original adapter-on: True`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
