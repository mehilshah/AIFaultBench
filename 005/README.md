# Bug 005

Reproduction bundle for https://github.com/tensorflow/models/issues/11206.

## What is checked

This bug report says the failure happens while importing `tensorflow` and
`tf_keras`, before the MobileNet test body runs:

```python
import tensorflow as tf, tf_keras
from tensorflow.python.framework import tensor
```

The local probe in `repro.py` executes that same import chain and prints the
result.

## Current result on this host

The issue did not reproduce here. Under the pinned issue-era versions
`tensorflow==2.16.1` and `tf-keras==2.16.0`, the internal
`tensorflow.python.framework.tensor` module exists and imports successfully on
this Linux/Python 3.12 host.

## Files

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```
