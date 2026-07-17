# Reproduction Bundle

This bundle reproduces the PEFT bug where `PromptEncoderConfig(task_type="SEQ_CLS")`
causes `get_peft_model` to fail with:

`AttributeError: 'PromptEncoderConfig' object has no attribute 'modules_to_save'`

The repro is offline and uses a freshly constructed BERT sequence-classification
model, so it does not depend on Hugging Face Hub downloads.

## Run

```bash
bash run_repro.sh
```

## Files

- `repro.py`: minimal reproducer and result writer
- `requirements.txt`: pinned Python dependencies
- `setup_env.sh`: local virtualenv setup
- `run_repro.sh`: entrypoint for the repro
- `manifest.json`: bundle metadata
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log` and `repro_stderr.log`: command output from the final run
