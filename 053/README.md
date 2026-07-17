# Bug 053

Minimal repro bundle for [keras-team/keras-io#1747](https://github.com/keras-team/keras-io/issues/1747).

## What fails

With the historical Keras/TensorFlow/KerasNLP stack used by the report, enabling
`keras.mixed_precision.set_global_policy("mixed_float16")` and then loading
`keras_nlp.models.BertClassifier.from_preset("bert_tiny_en_uncased_sst2")`
raises:

`AttributeError: 'LossScaleOptimizerV3' object has no attribute 'name'`

## Files

- `bug_report.txt`: source issue description
- `codebase/`: local copy of the keras-io docs repo
- `repro.py`: minimal reproducer
- `requirements.txt`: pinned dependency set for the repro
- `setup_env.sh`: local environment bootstrap
- `run_repro.sh`: runs the repro and writes logs
- `repro_stdout.log`: stdout from the verified repro run
- `repro_stderr.log`: stderr from the verified repro run
- `reproduction.json`: schema-constrained reproduction result

## Reproduce

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro exits non-zero after printing the optimizer attribute error.
