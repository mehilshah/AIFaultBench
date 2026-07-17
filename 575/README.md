# Bug 575 Repro

This folder contains a source-level reproduction bundle for:
`https://github.com/huggingface/pytorch-image-models/issues/2457`

Observed result in this standardized tree:
- `train.py` already defines `--validation-batch-size`
- the reported `AttributeError` is not reproducible here

Run:
```bash
bash setup_env.sh
bash run_repro.sh
```

The output is also written to:
- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`
