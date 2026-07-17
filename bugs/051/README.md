# Reproduction Bundle

This folder captures the issue reported in `bug_report.txt` for the KerasNLP translation example.

The minimal reproducer uses the same sampler call path as the notebook, but passes `end_token_id` to `keras_nlp.samplers.GreedySampler()`, which raises:

`TypeError: Sampler.__call__() got an unexpected keyword argument 'end_token_id'`

## Files

- `repro.py`: minimal failing call
- `setup_env.sh`: staged dependency install for the compatible Python 3.12 stack
- `run_repro.sh`: one-command entrypoint
- `requirements.txt`: dependency pinning used by the bundle
- `manifest.json`: bundle metadata

## Run

```bash
bash run_repro.sh
```

The expected outcome is a nonzero exit with the `TypeError` above.
