# Bug 065 Reproduction

This bundle reproduces the `FeatureSpace` import failure reported for the
`structured_data_classification_with_feature_space.py` example.

## Failure

The repro exercises:

```python
from keras.utils import FeatureSpace
```

With TensorFlow 2.11 and its bundled Keras, that import fails with:

```text
ImportError: cannot import name 'FeatureSpace' from 'keras.utils'
```

## Files

- `repro.py`: minimal import-only reproducer
- `requirements.txt`: pinned runtime dependencies used by the container
- `setup_env.sh`: builds the local Docker image
- `run_repro.sh`: runs the reproducer in the Docker image

## Usage

```bash
bash setup_env.sh
bash run_repro.sh
```
