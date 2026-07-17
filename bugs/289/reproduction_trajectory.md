# Reproduction Trajectory — Bug 289: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/2477](https://github.com/huggingface/peft/issues/2477)
- **Repository:** huggingface/peft @ `7dcdf7b311007b90ab085bb5dcd69f10ff32a30c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a BERT sequence-classification model from configuration.
2. Constructed PromptEncoderConfig(task_type='SEQ_CLS', num_virtual_tokens=20).
3. Called get_peft_model(base_model, ptuning_config).

## Observed behavior

- Raised AttributeError: 'PromptEncoderConfig' object has no attribute 'modules_to_save'
- The crash occurs while PeftModelForSequenceClassification.__init__ accesses peft_config.modules_to_save.
- The resulting traceback points to peft_model.py line 1506.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
