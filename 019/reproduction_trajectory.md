# Reproduction Trajectory — Bug 019: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/11018](https://github.com/tensorflow/models/issues/11018)
- **Repository:** tensorflow/models @ `5f0f949de9667552d85f0922191a05a0c9d0a99c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` in the standardized folder.
2. The script creates a Python 3.10 virtualenv, installs TensorFlow 2.15.1, forces `tensorflow-text` 2.20.1, installs the small supporting set (`tensorflow-datasets`, `gin-config`, `scipy`, `pyyaml`).
3. The repro script imports `tensorflow_models` from `codebase/` and then imports `tensorflow_text`, which raises the undefined-symbol error.

## Observed behavior

- `import tensorflow_text` in the prepared environment fails with `tensorflow.python.framework.errors_impl.NotFoundError` and `undefined symbol: _ZN10tensorflow12OpDefBuilder10SetShapeFnESt8functionIFN4absl12lts_202501276StatusEPNS_15shape_inference16InferenceContextEEE`.
- `import tensorflow_models as tfm` from the local `codebase/` traverses the repo import chain and logs the same TF-Text mismatch before failing on an unrelated missing `sentencepiece` dependency.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
