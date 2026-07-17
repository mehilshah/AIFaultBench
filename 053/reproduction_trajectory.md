# Reproduction Trajectory — Bug 053: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1747](https://github.com/keras-team/keras-io/issues/1747)
- **Repository:** keras-team/keras-io @ `6623a072e7eef484c3defa44dc16d824eac434cb`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run bash run_repro.sh from a clean checkout.
2. The script bootstraps a Python 3.11 venv, installs tensorflow==2.15.0, keras==2.15.0, keras-nlp==0.7.0, tensorflow-text==2.15.0, and setuptools<70, then executes repro.py.
3. The repro reaches BertClassifier.from_preset("bert_tiny_en_uncased_sst2") and raises the reported LossScaleOptimizerV3 AttributeError.

## Observed behavior

- With KERAS_BACKEND=tensorflow and keras.mixed_precision.set_global_policy("mixed_float16"), keras_nlp.models.BertClassifier.from_preset("bert_tiny_en_uncased_sst2") fails during weight loading. repro_stderr.log captures AttributeError: 'LossScaleOptimizerV3' object has no attribute 'name' at keras/src/optimizers/optimizer.py:820.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
