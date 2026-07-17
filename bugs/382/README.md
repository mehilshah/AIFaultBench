# Bug 382

Repro for PEFT issue 850: loading an adapter with `modules_to_save` and then disabling the adapter loses the original module weights.

## What this repro does

- Builds a tiny local `BertForSequenceClassification` model.
- Wraps the classifier with `modules_to_save`.
- Saves and reloads the adapter into a fresh base model whose classifier head is initialized differently.
- Shows that adapter-enabled logits still match, but adapter-disabled logits no longer match the original base model.

## Files

- `repro.py`: minimal failing script.
- `requirements.txt`: runtime dependencies.
- `setup_env.sh`: creates a local virtualenv and installs dependencies.
- `run_repro.sh`: runs the repro and captures logs.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is expected to fail on the final assertion because the original classifier weights are not preserved across save/load.
