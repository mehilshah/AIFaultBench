# Bug 052

Reproduction bundle for Keras-IO issue 1795:
`Named Entity Recognition using Transformers`.

## Result

The reported `Softmax.call()` graph error was **not reproducible** in this
environment with:

- TensorFlow 2.16.1
- Keras 3.1.0

The minimal NER model fit completed successfully on a small variable-length
token/tag dataset.

## Files

- `repro.py` - self-contained minimal training script
- `requirements.txt` - pinned runtime dependencies
- `setup_env.sh` - creates a local virtualenv and installs dependencies
- `run_repro.sh` - runs the reproducer
- `reproduction.json` - schema-constrained result
- `repro_stdout.log` / `repro_stderr.log` - captured command output

## Run

```bash
bash ./setup_env.sh
bash ./run_repro.sh
```
