# Bug 062 Reproduction

This folder contains a minimal reproduction for the `masked_language_modeling` example failing under pandas 2.x.

The failure is caused by:

`codebase/examples/nlp/masked_language_modeling.py:114`

which calls:

`train_df.append(test_df)`

## Files

- `repro.py`: minimal script that triggers the failure
- `requirements.txt`: reproduction dependencies
- `setup_env.sh`: creates a local virtual environment and installs dependencies
- `run_repro.sh`: runs the repro
- `manifest.json`: bug metadata

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```
