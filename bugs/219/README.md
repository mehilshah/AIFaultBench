# Bug 219 Reproduction

This folder reproduces the `transformers` bug reported in:
`https://github.com/huggingface/transformers/issues/29566`

The failure occurs when loading `bert-base-uncased` into `TFBertModel` with a
modified `BertConfig`.

Files:
- `repro.py`: minimal Python reproducer
- `requirements.txt`: pinned runtime dependencies
- `setup_env.sh`: creates a Python 3.10 virtual environment and installs deps
- `run_repro.sh`: runs the reproducer and writes logs
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log`, `repro_stderr.log`: captured run output

Run locally:
```bash
bash run_repro.sh
```

Run in Docker:
```bash
```

