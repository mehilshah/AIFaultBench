# Reproduction Trajectory — Bug 155: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/43009](https://github.com/huggingface/transformers/issues/43009)
- **Repository:** huggingface/transformers @ `9971e41`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Set `PYTHONPATH` to `codebase/src` so the repro uses the bundled transformers source tree.
2. Run `python3 repro.py` (or `bash run_repro.sh`).
3. The import `from transformers.configuration_utils import ALLOWED_LAYER_TYPES` fails with the reported ImportError.

## Observed behavior

- Running the repro against the bundled transformers source raises `ImportError: cannot import name 'ALLOWED_LAYER_TYPES' from 'transformers.configuration_utils'` from `codebase/src/transformers/configuration_utils.py`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
